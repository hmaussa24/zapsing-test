## Guía de Contribución — Proyecto ZapSign

### Objetivo
Estandarizar cómo trabajamos en este repositorio utilizando Cursor, con foco en TDD, arquitectura hexagonal, SOLID, patrones, LLMs/MCP y repos FE/BE independientes.

### Flujo de trabajo en Cursor
- **Status update breve** en cada turno: qué harás y por qué.
- **Descubrimiento antes de editar**: búsquedas semánticas y exactas en paralelo.
- **Edits pequeños y atómicos**: cambios mínimos, enfocados y revertibles.
- **Resumen corto** al cierre: cambios y su impacto.

### Gestión de tareas (TODOs)
- Tareas atómicas, verb-led y claras.
- Solo una tarea `in_progress` a la vez.
- Marcar `completed` inmediatamente tras finalizar.

### Arquitectura y principios
- **Hexagonal (puertos/adaptadores)**: dominio y casos de uso aislados de frameworks.
- **SOLID** y patrones: Repository, UoW, Strategy, Adapter/Facade, Builder, Circuit Breaker.
- **Repos separados**: frontend y backend evolucionan con pipelines propios.

### TDD y pruebas
- Ciclo **Red → Green → Refactor** en todas las capas.
- Backend (Django/DRF): Pytest, `pytest-django`, `factory_boy`, `respx`, `pytest-cov`.
- Frontend (Angular): Jest + Testing Library, `HttpClientTestingModule`/MSW, coverage gates.
- Contratos: OpenAPI como fuente de verdad; generación de tipos para FE.

### Estilo de código
- Nombres descriptivos; early returns; manejo real de errores.
- Evitar nesting profundo y comentarios triviales.
- Respetar formato existente; no mezclar refactors no solicitados.

### Commits, ramas y PRs
- Ramas por feature: `feat/<area>-<breve-desc>`; fixes: `fix/<area>-<desc>`.
- Commits atómicos con mensaje claro (imperativo): `feat(api): crear documento via ZapSign`.
- PR checklist:
  - [ ] Tests pasan y cobertura OK.
  - [ ] Linter sin errores.
  - [ ] Contratos OpenAPI actualizados (si aplica).
  - [ ] Documentación/README ajustada (si aplica).
  - [ ] Impactos en seguridad/observabilidad considerados.

### Uso de herramientas (Cursor)
- Búsqueda principal: `codebase_search`; para exactos: `grep`.
- Paralelizar lecturas/búsquedas independientes.
- Proponer comandos no interactivos y con flags adecuados.
- Citas de código: usar bloques con ruta/líneas; código nuevo con bloque y lenguaje.

### LLMs y MCP
- LLMs para análisis de documentos: salidas validadas por JSON Schema; logs con masking.
- MCP servers sugeridos: `zapsign-mcp`, `db-mcp`, `llm-mcp`, `n8n-mcp` con scopes mínimos.
- Seguridad: API keys en entorno seguro; auditoría de uso.

### Observabilidad y seguridad
- Logging estructurado JSON; métricas básicas (latencias, tasas de error, llamadas externas).
- Autenticación y autorización por `Company` (multitenancy lógico).
- CORS, rate limiting y validación estricta de entrada/salida.

### Convenciones FE/BE
- Backend: DRF ViewSets y Serializers como adaptadores; casos de uso en capa aplicación.
- Frontend: Angular con componentes reactivos, servicios, estado con RxJS.

### Estructura recomendada del Frontend (Angular)
```
src/
 ├── app/
 │    ├── core/                  # Servicios globales, guards, interceptors, layouts, config
 │    │    ├── guards/
 │    │    ├── interceptors/
 │    │    ├── services/
 │    │    ├── layouts/
 │    │    └── core.module.ts    # O, si usas standalone, un provider central
 │    │
 │    ├── shared/                # Componentes, directivas y pipes reutilizables
 │    │    ├── components/
 │    │    ├── directives/
 │    │    ├── pipes/
 │    │    └── shared.module.ts
 │    │
 │    ├── features/              # Cada feature (dominio) en un módulo/carpeta separado
 │    │    ├── auth/             # Ejemplo: autenticación
 │    │    │    ├── components/
 │    │    │    ├── pages/
 │    │    │    ├── services/
 │    │    │    ├── models/
 │    │    │    └── auth.module.ts
 │    │    │
 │    │    ├── dashboard/        # Ejemplo: dashboard
 │    │    │    ├── components/
 │    │    │    ├── pages/
 │    │    │    ├── services/
 │    │    │    └── dashboard.module.ts
 │    │    │
 │    │    └── ...               # Más features
 │    │
 │    ├── app.routes.ts          # Configuración de rutas principales
 │    ├── app.config.ts          # Providers globales (con provideX)
 │    └── app.component.ts
 │
 ├── assets/                     # Imágenes, fuentes, estilos globales
 ├── environments/               # Archivos de configuración por entorno
 ├── main.ts                     # Punto de entrada
 └── styles.scss                 # Estilos globales
```

### Cómo empezar
1. Lee `INSTRUCTION.MD` y `PLAN_EJECUCION.md`.
2. Abre una rama `feat/<tu-feature>`.
3. Escribe tests (rojo), implementa (verde), refactoriza.
4. Ejecuta linters y cobertura.
5. Abre PR con checklist completa.

### Reglas de Cursor (unificadas)
- Regla maestra en la raíz: `/.cursor/rules/rules.mdc`.
- Resume y unifica convenciones de backend (Django/DRF) y frontend (Angular), arquitectura hexagonal, SOLID, TDD, patrones, OpenAPI y LLMs/MCP.
- Se aplica automáticamente en todo el workspace (`alwaysApply: true`, `globs: ["**/*"]`).
- Las reglas específicas por stack se interpretan a partir de las secciones `backend` y `frontend` dentro del archivo.

### Arquitectura hexagonal por módulos (backend)
- Guía: `backend/ARCHITECTURE.md`.
- Módulos requeridos: `modules/company`, `modules/document`, `modules/signer`.
- Capas por módulo: `domain`, `application`, `infrastructure`, `api`.
- Los ViewSets DRF delegan siempre en casos de uso de `application` y no contienen reglas de negocio.

#### Diagrama (Mermaid) — vista modular y hexagonal por módulo
```mermaid
flowchart LR
  subgraph FE[Frontend Angular]
    FE_UI[UI Reactiva]
    FE_SRV[Servicios HTTP / Facade]
  end

  subgraph BE[Backend Django + DRF]
    direction TB
    subgraph MCompany[Módulo Company]
      C_API[API]
      C_APP[Application]
      C_DOM[Domain]
      C_INF[Infrastructure]
    end
    subgraph MDocument[Módulo Document]
      D_API[API]
      D_APP[Application]
      D_DOM[Domain]
      D_INF[Infrastructure (ORM, ZapSign Adapter, Analyzer Strategy)]
    end
    subgraph MSigner[Módulo Signer]
      S_API[API]
      S_APP[Application]
      S_DOM[Domain]
      S_INF[Infrastructure]
    end
  end

  FE_SRV -->|REST| C_API
  FE_SRV -->|REST| D_API
  FE_SRV -->|REST| S_API
  D_INF -->|HTTP Adapter| ZAPSIGN[(ZapSign API)]
  D_INF -->|Strategy| AI[(Proveedor IA/LLM)]
  BE --> DB[(PostgreSQL)]
  BE --> N8N[(n8n)]
```

```mermaid
flowchart TB
  subgraph Hex_Document[Módulo Document — Puerto/Adaptador]
    IN_AD[Entradas (DRF, CLI, Jobs)] --> IN_PORT[Puertos Entrada]
    IN_PORT --> APP[Aplicación (Casos de uso)]
    APP --> DOMAIN[Dominio]
    APP --> OUT_PORT[Puertos Salida (Repos, ZapSign, IA)]
    OUT_PORT --> OUT_AD[Adaptadores (ORM, HTTP, Strategy IA)]
  end
```

### Commits y hooks de verificación
- Convenciones de commits: **Conventional Commits** (ej.: `feat(api): crear documento vía ZapSign`). La validación está configurada con Commitlint.
- Hooks (Husky):
  - `commit-msg`: valida el mensaje con Commitlint (`.commitlintrc.json`).
  - `pre-commit`: ejecuta `make lint` (linters de backend y frontend).
  - `pre-push`: ejecuta `make test` con gates de cobertura:
    - Backend: Pytest con `--cov-fail-under=80`.
    - Frontend: Jest con `coverageThreshold` global ≥ 70% (ver `frontend/jest.config.js`).
- Umbrales y comandos viven en el `Makefile` y config de cada subproyecto; ajústalos allí si cambian.
- Commit asistido: puedes usar **Commitizen** (`npx cz`) para guiar el formato del mensaje.
- Omitir temporalmente (solo urgencias): añade `--no-verify` al comando de `git commit` o `git push`. Evítalo salvo casos justificados y crea follow-up para subsanar.


