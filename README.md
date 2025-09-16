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


