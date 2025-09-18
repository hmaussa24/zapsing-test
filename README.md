## ZapSign — Reglas y configuración de Cursor

### Rules del workspace
- Archivo principal: `/.cursor/rules/rules.mdc` (aplica a todo el workspace: `alwaysApply: true`, `globs: ["**/*"]`).
- Guía de contribución como rule: `/.cursor/rules/contributing.mdc`.
- Referencias en `CONTRIBUTING.md` y `PLAN_DE_EJECUCION.md` apuntan a estas rules.

### Recargar rules en Cursor
1. Abre la paleta de comandos y ejecuta: "Cursor: Reload Workspace Rules".
2. O reinicia la ventana de Cursor.
3. Verifica en la barra lateral de Rules que se carguen los archivos `.mdc`.

### Alcance de las rules
- Arquitectura hexagonal por módulo (backend) y módulos con servicios/facade (frontend).
- SOLID, TDD, patrones (Adapter, Strategy, Repository, Factory, Decorator; Facade/Adapter en FE).
- OpenAPI como fuente de verdad; LLMs/MCP con puertos/herramientas seguras.

### Base de datos (PostgreSQL con Docker Compose)
- Requisitos: Docker y Docker Compose instalados.
- Levantar la base:
```bash
docker compose up -d db
```
- Puerto expuesto: `55432` (mapeado a `5432` del contenedor).
- Variables por defecto del servicio `db`:
  - `POSTGRES_USER=zapsign`
  - `POSTGRES_PASSWORD=password`
  - `POSTGRES_DB=zapsign`
- `DATABASE_URL` local sugerido:
```bash
export DATABASE_URL=postgres://zapsign:password@localhost:55432/zapsign
```
- Apagar la base:
```bash
docker compose down
```

### Variables de entorno
- Archivos de ejemplo:
  - Backend: `backend/.env.example`
  - Frontend: `frontend/.env.example`
- Copiar y ajustar:
```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```
- Asegúrate de que `DATABASE_URL` apunte al puerto `55432` si usas Docker Compose.

### Backend (Django + DRF)
- Requisitos: Python 3.12+, virtualenv
- Instalar dependencias:
```bash
python3 -m venv backend/.venv
backend/.venv/bin/pip install -U pip
backend/.venv/bin/pip install -r backend/requirements.txt
```
- Variables de entorno:
  - Copia `backend/.env.example` a `backend/.env` y ajusta:
    - `DATABASE_URL=postgres://zapsign:password@localhost:55432/zapsign`
    - `AUTOMATION_API_KEY=...` (mismo secreto configurado en n8n)
    - `N8N_WEBHOOK_URL=https://<tu-n8n-cloud>/webhook/analysis-in`
    - `RABBITMQ_URL=amqp://zapsign:zapsign@localhost:5672/%2F` (o tu vhost)
    - `AUTOMATION_QUEUE=document_created`
    - `START_AUTOMATION_WORKER=true` (opcional: arranca el worker con el backend)
- Migraciones y arranque:
```bash
backend/.venv/bin/python backend/manage.py migrate
backend/.venv/bin/python backend/manage.py runserver
```
- Autenticación (JWT con SimpleJWT):
  - Endpoints:
    - `POST /api/auth/register` → crea compañía. Request:
      ```json
      { "name": "Acme Corp", "email": "admin@acme.com", "password": "SecurePassword123" }
      ```
      Response 201:
      ```json
      { "id": 1, "name": "Acme Corp", "email": "admin@acme.com" }
      ```
    - `POST /api/auth/login` → devuelve tokens. Request:
      ```json
      { "email": "admin@acme.com", "password": "SecurePassword123" }
      ```
      Response 200:
      ```json
      { "access": "<jwt>", "refresh": "<jwt>" }
      ```
    - `POST /api/auth/refresh` → refresca el access token. Request:
      ```json
      { "refresh": "<jwt>" }
      ```
      Response 200:
      ```json
      { "access": "<jwt>" }
      ```
    - `GET /api/auth/me` → perfil de la compañía autenticada (Bearer access).
  - Notas:
    - El claim `company_id` viaja en los tokens; el backend usa este claim para scopear recursos.
    - Swagger usa esquema Bearer y documenta estos endpoints en la sección "Company Auth".
  - Variables relacionadas (en `backend/.env`):
    - `ACCESS_TOKEN_LIFETIME_SECONDS=60` (por defecto 60s en dev para probar refresh)
    - `REFRESH_TOKEN_LIFETIME_SECONDS=86400` (24h por defecto)
- Worker (opciones):
  - Autostart: `START_AUTOMATION_WORKER=true` y `runserver`
  - Manual:
  ```bash
  backend/.venv/bin/python backend/manage.py run_automation_worker
  ```

### Servicios con Docker Compose
- Postgres y RabbitMQ:
```bash
docker compose up -d db rabbitmq
```
- RabbitMQ Management UI: http://localhost:15672 (user/pass por defecto `zapsign/zapsign`).

### Frontend (Angular 17)
- Requisitos: Node.js 18+ y pnpm/npm
- Variables: copia `frontend/.env.example` a `frontend/.env` (API base `http://localhost:8000`).
- Instalar y arrancar:
```bash
cd frontend
npm install
npm start
```
- Autenticación en FE:
  - `AuthService` almacena `access` y `refresh` en `localStorage`.
  - El interceptor adjunta `Authorization: Bearer <access>` a cada request.
  - Si recibe 401 y hay `refresh`, llama a `/api/auth/refresh`, guarda el nuevo `access` y reintenta la petición automáticamente.
- Material Icons (si no se ven íconos): agrega en `frontend/src/index.html` dentro de `<head>`:
```html
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
```

### n8n (Cloud)
- Configura un webhook de entrada (production URL) y variable `AUTOMATION_API_KEY` en n8n.
- El backend envía `X-Automation-Key` y recibe el callback en `/api/webhooks/analysis/`.


