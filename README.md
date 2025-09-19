## Cómo ejecutar el proyecto

### Opción A) Con Docker (recomendado)

Requisitos: Docker Desktop/Engine y Docker Compose.

1) Construir e iniciar servicios
```bash
docker compose build --no-cache
docker compose up -d
```

2) Ejecutar migraciones de la base de datos
```bash
docker compose exec backend python manage.py migrate
```

3) Configurar webhook de ZapSign con ngrok
- Instalar ngrok: https://ngrok.com/download
- En una terminal separada, crear túnel hacia el backend local:
  ```bash
  ngrok http 8000
  ```
- Copiar la URL HTTPS generada (ej: `https://abc123.ngrok-free.app`)
- En la plataforma ZapSign (https://sandbox.zapsign.com.br):
  - Ir a "Configurações" → "Webhooks"
  - Crear nuevo webhook con la URL: `https://abc123.ngrok-free.app/api/webhooks/zapsign/`
  - Seleccionar eventos: "Documento assinado", "Documento rejeitado", etc.
  - Guardar la configuración
- **Importante**: Mantener ngrok corriendo durante el desarrollo para recibir webhooks

4) Configurar n8n (requerido para análisis de documentos)
- Acceder a n8n: http://localhost:5678
- Registrar y llenar los datos que pide N8N
- Crear cuenta y configurar:
  - Ir a "Workflows" → "Import from file"
  - Importar el archivo `n8n/workflows/local-zapsing-ia.json`
  - Activar el workflow importado
  - Configurar API Key de Google AI Studio:
    - Obtener API key en: https://aistudio.google.com/apikey
    - En el workflow, editar el nodo "Message a model"
    - En "Credentials", configurar la API key de Google Gemini
    - Guardar y activar el workflow

5) Endpoints y accesos
- Frontend: http://localhost:4200
- Backend (API): http://localhost:8000
- Swagger UI: http://localhost:8000/api/docs/
- RabbitMQ UI: http://localhost:15672 (user/pass: zapsign/zapsign)
- n8n: http://localhost:5678 (user/pass: admin/admin123)
- ngrok: URL HTTPS generada (ej: https://abc123.ngrok-free.app)

6) Variables de entorno (ya definidas en docker-compose.yml)
- Backend:
  - `DJANGO_SECRET_KEY`: insecure-dev-key (dev)
  - `DJANGO_DEBUG`: "True"
  - `ALLOWED_HOSTS`: `127.0.0.1,localhost,.ngrok-free.app`
  - `CSRF_TRUSTED_ORIGINS`: `https://.ngrok-free.app`
  - `DATABASE_URL`: `postgres://zapsign:password@db:5432/zapsign`
  - `ZAPSIGN_API_BASE`: `https://sandbox.api.zapsign.com.br/api/v1`
  - `ZAPSIGN_AUTH_SCHEME`: `Bearer`
  - `AUTOMATION_API_KEY`: clave para n8n (ajusta)
  - `RABBITMQ_URL`: `amqp://zapsign:zapsign@rabbitmq:5672/%2F`
  - `AUTOMATION_QUEUE`: `document_created`
  - `START_AUTOMATION_WORKER`: `true` (ejecuta worker junto al backend)
  - `ACCESS_TOKEN_LIFETIME_SECONDS`: `60`
  - `REFRESH_TOKEN_LIFETIME_SECONDS`: `86400`
  - `N8N_WEBHOOK_URL`: URL de webhook en n8n (ajusta)
- Frontend:
  - `API_BASE_URL`: `http://backend:8000` (el proxy lee esta variable)

Notas:
- El servicio `rabbitmq` tiene healthcheck y `backend/worker` esperan a que esté "healthy".
- El frontend usa `proxy.conf.js` dinámico que reenvía `/api` a `API_BASE_URL`.

Comandos útiles
```bash
# Docker
docker compose logs -f backend
docker compose restart frontend backend worker
docker compose down

# ngrok (en terminal separada)
ngrok http 8000
# Ver tráfico de webhooks en: http://localhost:4040
```

---

### Opción B) Sin Docker (servicios individuales)

Puedes levantar Postgres y RabbitMQ con Docker y correr backend y frontend localmente.

1) Base de datos y cola (con Docker)
```bash
docker compose up -d db rabbitmq
# Postgres disponible en localhost:55432 (mapea 5432 del contenedor)
# RabbitMQ UI en http://localhost:15672 (zapsign/zapsign)
```

2) Backend (Django)
```bash
python3 -m venv backend/.venv
backend/.venv/bin/pip install -U pip
backend/.venv/bin/pip install -r backend/requirements.txt
```

Configura variables (archivo `backend/.env` recomendado) mínimas para dev:
```env
DJANGO_SECRET_KEY=insecure-dev-key
DJANGO_DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=http://localhost:4200
DATABASE_URL=postgres://zapsign:password@localhost:55432/zapsign
ZAPSIGN_API_BASE=https://sandbox.api.zapsign.com.br/api/v1
ZAPSIGN_AUTH_SCHEME=Bearer
RABBITMQ_URL=amqp://zapsign:zapsign@localhost:5672/%2F
AUTOMATION_QUEUE=document_created
START_AUTOMATION_WORKER=true
ACCESS_TOKEN_LIFETIME_SECONDS=60
REFRESH_TOKEN_LIFETIME_SECONDS=86400
N8N_WEBHOOK_URL=https://<tu-n8n>/webhook/document-analysis
```

Aplicar migraciones y arrancar:
```bash
backend/.venv/bin/python backend/manage.py migrate
backend/.venv/bin/python backend/manage.py runserver 0.0.0.0:8000
```

3) Frontend (Angular)
```bash
cd frontend
npm install
export API_BASE_URL=http://localhost:8000
npm start
# Abre http://localhost:4200
```

El frontend usa `proxy.conf.js`, que lee `API_BASE_URL` y redirige `/api` hacia ese backend.

---

### Tests (Backend)

Puedes ejecutar la suite de tests con pytest. Asegúrate de tener configurada la base de datos indicada en `DATABASE_URL` (o usar SQLite por defecto si no se define) y las dependencias instaladas.

Con Docker (recomendado):
```bash
# Instalar dependencias (si cambiaste requirements)
docker compose build backend
# Ejecutar tests dentro del contenedor backend
docker compose run --rm backend pytest -q
```

Local sin Docker (rápido con SQLite):
```bash
python3 -m venv backend/.venv
backend/.venv/bin/pip install -U pip
backend/.venv/bin/pip install -r backend/requirements.txt

# No definas DATABASE_URL para que use SQLite por defecto
unset DATABASE_URL 2>/dev/null || true

# Ejecutar tests
backend/.venv/bin/pytest -q
```

Local sin Docker (usando Postgres de Docker):
```bash
python3 -m venv backend/.venv
backend/.venv/bin/pip install -U pip
backend/.venv/bin/pip install -r backend/requirements.txt

# Variables mínimas (opcional si usas SQLite por defecto)
export DJANGO_DEBUG=False
export DATABASE_URL=postgres://zapsign:password@localhost:55432/zapsign

# Ejecutar tests
backend/.venv/bin/pytest -q
```

Cobertura:
```bash
# Generar y ver reporte de cobertura en terminal
backend/.venv/bin/pytest --cov=. -q
```

Ejemplos útiles:
```bash
# Ejecutar un archivo específico
backend/.venv/bin/pytest backend/tests/document/test_document_api.py -q

# Ejecutar con más detalle
backend/.venv/bin/pytest -vv

# Generar reporte HTML de cobertura
backend/.venv/bin/pytest --cov=. --cov-report=html
# Abrir htmlcov/index.html en tu navegador
```

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


