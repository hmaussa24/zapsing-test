## Plan de Ejecución — Módulo de Gestión de Documentos ZapSign

### Resumen
Implementar un módulo end-to-end para crear, listar, actualizar y eliminar `Companies`, `Documents` y `Signers`, integrando la API de ZapSign, análisis con IA y automatizaciones via n8n. Se proveerán APIs REST autenticadas, frontend en Angular con UI reactiva, backend en Django + DRF + PostgreSQL, todo orquestado con Docker.

### Alcance y objetivos
- **CRUD completo**: `Companies`, `Documents`, `Signers` con relaciones y validaciones.
- **Integración ZapSign**: crear documentos y persistir `open_id`, `token`, `status` y metadatos.
- **Análisis con IA**: generar resumen, tópicos faltantes e insights del documento; endpoint para solicitar reanálisis.
- **Automatizaciones (n8n)**: endpoints autenticados aptos para flujos n8n; hook opcional de evento.
- **Frontend Angular**: panel con UI fluida sin recarga; formularios reactivos; feedback de estado.
- **Pruebas**: Pytest (API) y Jest (frontend).
- **Infra**: Docker Compose para entorno local; README claro.

### Arquitectura y lineamientos
- **Arquitectura**: estilo hexagonal (puertos y adaptadores) para separar dominios, aplicación e infra.
- **Repos**: frontend y backend en repos independientes.
- **Backend**: Django + DRF, PostgreSQL, autenticación (JWT o Token), drf-yasg/Schema para OpenAPI.
- **Frontend**: Angular con componentes y formularios reactivos; Testing Library + Jest.
- **Integraciones**: ZapSign (docs y estado), IA (OpenAI/HuggingFace/spaCy/LangChain), n8n.

### Diagrama de arquitectura (modular y hexagonal por módulo)
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
      C_INF[Infrastructure (ORM/Repository)]
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
      S_INF[Infrastructure (ORM/Repository)]
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

#### Hexágono por módulo (ejemplo `Document`)
```mermaid
flowchart TB
  direction TB
  subgraph Document_Hex[Módulo Document — Hexagonal]
    AD_IN[Adaptadores de Entrada\n(DRF ViewSets, Jobs)] --> PUERTOS_IN[Puertos de Entrada]
    PUERTOS_IN --> APP[Aplicación\n(Casos de uso)]
    APP --> DOM[Dominio\n(Entidades/Servicios)]
    APP --> PUERTOS_OUT[Puertos de Salida\n(Repos, ZapSign, IA)]
    PUERTOS_OUT --> AD_OUT[Adaptadores de Salida\n(Repository ORM, HTTP Adapter, Analyzer Strategy)]
  end
```

### Principios y estándares obligatorios
- **SOLID**: responsabilidades únicas por servicio, inyección de dependencias (puertos), sustitución segura de implementaciones y segregación de interfaces finas.
- **Patrones de diseño**:
  - **Adapter**: integración ZapSign y capa HTTP; mappers DTO ↔ dominio.
  - **Strategy**: selección de motor de IA (`DocumentAnalyzer`).
  - **Factory**: `AnalyzerFactory`/`HttpClientFactory` para instanciar implementaciones por configuración.
  - **Repository**: acceso a persistencia de `Document`, `Signer`, `Company`.
  - (Opcional) **Decorator**: logging/observabilidad, retries.
- **TDD**: ciclo red-green-refactor en servicios y endpoints críticos, con cobertura mínima backend 85% y frontend 80%.
- **Cursor**: uso para flujo de trabajo, revisiones, y edición dirigida por reglas del proyecto (commits pequeños, mensajes claros). Ver `/.cursor/rules/rules.mdc` para convenciones unificadas.
- **Rules del proyecto**: respetar arquitectura hexagonal, repos separados, no ejecutar acciones fuera de pedido del usuario, y pruebas automatizadas consistentes.
- **LLMs**: uso para análisis de documentos (funcional), y soporte a desarrollo con prompts versionados (no sustituyen pruebas).
- **MCP (Model Context Protocol)**: definir herramientas/puertos para que agentes consuman contexto (p.ej., fetch de documentos y análisis) de forma reproducible.

## Fase 0 — Preparación (Día 0)
### Tareas
- Crear cuenta en sandbox ZapSign y obtener `api_token`.
- Definir variables de entorno y secretos.
- Inicializar repos: `zapsign-backend` (Django) y `zapsign-frontend` (Angular).
- Crear `docker-compose.yml` para DB (PostgreSQL) y servicios.
- Definir diagramas de entidades y endpoints (borrador).
- Establecer convenciones SOLID y lista de patrones a aplicar (Adapter, Strategy, Factory, Repository, Decorator opcional).
- Configurar toolchain TDD: Pytest con coverage y Jest + Testing Library; pipelines que bloqueen merges si fallan tests o cobertura < umbral.
- Definir flujo con Cursor (ramas, PRs, templates) y registrar Rules del proyecto en el README.
- Especificar puertos MCP iniciales (p.ej., `get_document_text`, `submit_analysis`) y su seguridad.

### Variables de entorno (ejemplo)
```
BACKEND
DJANGO_SECRET_KEY=...
DJANGO_DEBUG=True
DATABASE_URL=postgres://zapsign:password@db:5432/zapsign
ZAPSIGN_API_BASE=https://sandbox.api.zapsign.com.br/api/v1
ZAPSIGN_API_TOKEN=<<por_company>>
AI_PROVIDER=openai|spacy|hf
OPENAI_API_KEY=...
N8N_WEBHOOK_URL=https://n8n.example.com/webhook/...
AUTH_JWT_SECRET=...

FRONTEND
API_BASE_URL=http://localhost:8000
```

## Fase 1 — Backend: dominio y persistencia (Días 1-2)
### Entidades principales
- `Company`: `id`, `name`, `api_token` (cifrado/guardado seguro), timestamps.
- `Document`: `id`, `company`, `name`, `status`, `open_id`, `token`, `pdf_url`, `created_by`, timestamps.
- `Signer`: `id`, `document`, `name`, `email`, `status`, `token`, timestamps.
- `DocumentAnalysis`: `id`, `document`, `summary`, `missing_topics` (JSON), `insights` (JSON), `model_info`, `created_at`.

### Trabajo
- Crear proyecto Django y app `documents`.
- Configurar PostgreSQL y migraciones iniciales.
- Definir repositorios/servicios de dominio (puertos) y adaptadores ORM.
- Registrar modelos en admin para soporte operativo.
- Aplicar **SOLID** en servicios de dominio y repositorios; definir interfaces finas por caso de uso.
- Implementar **Repository** para `Company`, `Document`, `Signer` y **mappers** DTO↔dominio.
- Iniciar con **TDD**: tests de modelo y repos antes de implementar lógica.

## Fase 2 — Backend: APIs REST y autenticación (Días 2-3)
### Endpoints (borrador)
- Autenticación: `POST /api/auth/login` (JWT/Token), `POST /api/auth/refresh`.
- Companies: `GET/POST /api/companies`, `GET/PATCH/DELETE /api/companies/{id}`.
- Documents: `GET/POST /api/documents`, `GET/PATCH/DELETE /api/documents/{id}`.
- Signers: `GET/POST /api/documents/{id}/signers`, `PATCH/DELETE /api/signers/{id}`.
- Análisis: `POST /api/documents/{id}/analyze`, `GET /api/documents/{id}/analysis`.
- n8n hooks: `POST /api/hooks/document-created` (opcional, autenticado con token).

### Trabajo
- Serializers, ViewSets y rutas con DRF; paginación, filtros básicos, validaciones.
- Permisos por empresa (scoping por `Company`).
- Documentación OpenAPI/Swagger y colección Postman.
- Aplicar **Factory** para resolución de servicios (p.ej., `AnalyzerFactory`) e inyección por configuración.
- Usar **Decorator** para logging y métricas alrededor de adaptadores HTTP.

## Fase 3 — Integración ZapSign (Día 3)
### Flujo de creación de documento
1. Frontend envía `name`, `pdf_url`, `signer { name, email }` al backend.
2. Backend crea `Document` y llama ZapSign `POST /docs/` con `api_token` de `Company`.
3. Almacena `open_id`, `token`, `status` devueltos.
4. Retorna DTO con datos consolidados y dispara análisis de IA (async recomendado).

### Consideraciones
- Adaptador HTTP robusto: reintentos, timeouts, logging, manejo de errores de negocio.
- Endpoint para consultar/actualizar `status` desde ZapSign (`GET /docs/{id}`) si se requiere sincronización.

## Fase 4 — Análisis con IA (Días 3-4)
### Objetivo
Generar: `summary`, `missing_topics`, `insights` al guardar el documento y permitir reanálisis bajo demanda.

### Diseño
- Puerto `DocumentAnalyzer` con implementación seleccionable por `AI_PROVIDER`.
- Implementación base: OpenAI (modelo GPT-4o-mini) o spaCy local para entorno offline.
- Persistir resultados en `DocumentAnalysis` vinculados a `Document`.
- Ejecutar en background (Celery + Redis) o síncrono si el tamaño es pequeño.
- Patrones: **Strategy** (selección de motor) + **Factory** (instanciación); pruebas por **TDD** con stubs/mocks.

### Endpoints
- `POST /api/documents/{id}/analyze`: fuerza nuevo análisis; idempotencia básica.
- `GET /api/documents/{id}/analysis`: retorna último análisis.

## Fase 5 — Automatizaciones n8n (Día 4)
### Objetivo
Habilitar flujos de n8n usando endpoints autenticados.

### Trabajo
- Definir `POST /api/hooks/document-created` para que n8n reaccione a creaciones (incluye `document_id`, `status`).
- Alternativa: n8n consume `GET /api/documents?status=pending` periódicamente.
- Autenticación mediante token de servicio o API Key header.
- Exponer puertos **MCP** para que agentes o n8n consulten contexto controlado.

## Fase 6 — Frontend Angular (Días 4-6)
### Páginas y componentes
- Panel de empresa: vista general de `Companies`, `Documents`, `Signers`.
- Lista de documentos: tabla reactiva con filtros y paginación.
- Formulario de creación de documento: `name`, `pdf_url`, `signer.name`, `signer.email`.
- Vista de análisis: mostrar `summary`, `missing_topics`, `insights` y botón de reanálisis.

### Trabajo
- Servicios HTTP tipados, interceptores de auth, manejo de errores y loaders.
- Formularios reactivos con validaciones.
- Actualización de lista sin recargar (state local o signals; NgRx opcional según complejidad).
- Pruebas con Jest y Testing Library para componentes clave.
- Aplicar principios **SOLID** en servicios/UI; usar **Facade** en capa de datos del frontend y **Adapter** para mapeo API↔UI.

## Fase 7 — Pruebas y calidad (Transversal, énfasis Días 2-6)
### Backend (Pytest)
- Tests de modelos y repositorios.
- Tests de servicios: ZapSign adapter (mock), analyzer (stub), n8n hook.
- Tests de API: autenticación, CRUD, análisis, permisos por `Company`.
- Enfoque **TDD**: escribir tests antes de la implementación en servicios críticos; usar coverage ≥85%.

### Frontend (Jest)
- Tests de servicios, componentes de formulario y tabla; mocks de HTTP.
- Enfoque **TDD** en componentes/servicios clave; coverage ≥80%.

### Calidad
- Linting, formateo y cobertura mínima (p.ej., 80%).
- Pre-commit hooks: lint + tests; CI bloquea merges si violan cobertura o fallan suites.

## Fase 8 — Infraestructura y ejecución local (Días 1-2 y cierre Día 6)
### Docker
- `Dockerfile` backend, `Dockerfile` frontend, `docker-compose.yml` con `db`, `backend`, `frontend`.
- Objetivos multi-stage para imágenes ligeras.

### Observabilidad
- Logging estructurado; captura de errores (Sentry opcional).

## Fase 9 — Documentación final (Día 7)
- README con instrucciones: levantar servicios, variables de entorno, migraciones, seeds.
- Documentación de endpoints (Swagger/OpenAPI + Postman).
- Explicación de la lógica de IA: prompts/modelos, límites y costos.
- Guía de flujos n8n de ejemplo.

## Cronograma sugerido (7 días)
- Día 0-1: Setup, modelos, migraciones, autenticación, OpenAPI.
- Día 2: Endpoints CRUD y permisos; pruebas backend iniciales.
- Día 3: Integración ZapSign; pruebas de integración (mocks).
- Día 4: Análisis IA y n8n hooks; Celery opcional.
- Día 5-6: Frontend Angular (UI, servicios, pruebas) y pulido UX.
- Día 7: Docker, README, pruebas E2E ligeras y cierre.
- Nota: aplicar **TDD continuo** en todas las fases; revisar cumplimiento de **SOLID** y patrones por checklist en PRs de Cursor.

## Criterios de aceptación (trazabilidad)
- Panel: CRUD completo sin recarga y feedback de estado.
- Creación de documento: alta en ZapSign, persistencia de `open_id` y `token`.
- Análisis IA: disponible tras guardar; reanálisis on-demand.
- Endpoints REST: autenticados, versionados y documentados.
- Pruebas automatizadas: rutas y funcionalidades críticas estables.
- README: claro y accionable.
- Cumplimiento de **SOLID** y aplicación de patrones (**Adapter**, **Strategy**, **Factory**, **Repository**; **Decorator** opcional).
- Evidencia de **TDD** (tests previos, cobertura mínima, pipeline bloqueante).
- Uso de **Cursor** y respeto de **Rules** del proyecto.
- Uso de **LLMs** en análisis y definición de prompts versionados; puertos **MCP** definidos.

## Mapeo de patrones y responsabilidades
- Backend ZapSign: **Adapter** HTTP con **Decorator** de retries/logging.
- Analizador IA: **Strategy** seleccionable + **Factory** para instancias.
- Persistencia: **Repository** por agregado (`Company`, `Document`, `Signer`).
- Frontend datos: **Facade** + **Adapter** para normalización de respuestas.

## Riesgos y mitigaciones
- Disponibilidad de ZapSign: usar reintentos y manejo de errores; colas para re-procesar.
- Costos/latencia IA: permitir proveedor local (spaCy) y caché por documento.
- Seguridad: scoping por `Company`, JWT expirable, rate limiting básico.
- UX: loaders y estados claros; validaciones estrictas en formularios.

## Entregables
- Backend Django + DRF con integraciones (ZapSign, IA, n8n) y pruebas.
- Frontend Angular con UI reactiva y pruebas.
- Docker Compose funcional.
- Documentación (README, OpenAPI, colección Postman, guía n8n).


