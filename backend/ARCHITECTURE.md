## Arquitectura del Backend — Hexagonal por Módulos

Este backend aplica arquitectura hexagonal (puertos y adaptadores) de forma modular. Cada módulo encapsula su dominio, casos de uso y adaptadores, aislando el núcleo de frameworks (Django/DRF), integraciones (ZapSign, IA) y base de datos (PostgreSQL).

### Módulos obligatorios
- `modules/company`
- `modules/document`
- `modules/signer`

Cada módulo sigue la misma estructura de carpetas:
```
modules/<modulo>/
  domain/           # Entidades, valores, servicios de dominio (reglas puras)
  application/      # Casos de uso (puertos de entrada) y orquestación
  infrastructure/   # Adaptadores de salida (ORM/HTTP), repositorios, mappers
  api/              # Adaptadores de entrada (DRF ViewSets/Serializers)
```

### Principios y estándares
- **SOLID** en servicios/casos de uso y diseño de interfaces.
- **Patrones**: Adapter (ZapSign/HTTP), Strategy (IA), Repository (persistencia), Factory (resolución de implementaciones), Decorator (reintentos/log/metrics opcional).
- **TDD**: tests primero para casos de uso, repos y adaptadores; cobertura mínima ≥ 85% backend.
- **Repos separados**: este backend es independiente del frontend.
- **LLMs/MCP**: la integración de IA se realiza vía puertos; definir herramientas MCP para exponer contexto de forma segura y reproducible.

### Vista general (Mermaid)
```mermaid
flowchart LR
  subgraph BE[Backend Django + DRF]
    direction TB
    subgraph Company[modules/company]
      C_API[API]
      C_APP[Application]
      C_DOM[Domain]
      C_INF[Infrastructure]
    end
    subgraph Document[modules/document]
      D_API[API]
      D_APP[Application]
      D_DOM[Domain]
      D_INF[Infrastructure (ORM, ZapSign Adapter, Analyzer Strategy)]
    end
    subgraph Signer[modules/signer]
      S_API[API]
      S_APP[Application]
      S_DOM[Domain]
      S_INF[Infrastructure]
    end
  end

  BE --> DB[(PostgreSQL)]
  D_INF -->|HTTP Adapter| ZAPSIGN[(ZapSign API)]
  D_INF -->|Strategy| AI[(Proveedor IA/LLM)]
  BE --> N8N[(n8n)]
```

### Hexágono por módulo (ejemplo: `modules/document`)
```mermaid
flowchart TB
  subgraph Document_Hex[Módulo Document — Hexagonal]
    IN_AD[Adaptadores de Entrada\n(DRF ViewSets, Jobs)] --> IN_PORT[Puertos de Entrada]
    IN_PORT --> APP[Aplicación\n(Casos de Uso: CreateDocument, AnalyzeDocument, etc.)]
    APP --> DOM[Dominio\n(Entidades: Document, Signer; Servicios)]
    APP --> OUT_PORT[Puertos de Salida\n(Repository, ZapSignClient, Analyzer)]
    OUT_PORT --> OUT_AD[Adaptadores de Salida\n(Repository ORM, HTTP Adapter, Strategy IA)]
  end
```

### Contratos y puertos (interfaces)
- `application` expone puertos de entrada (p.ej., `CreateDocumentUseCase`) consumidos por `api`.
- `application` depende de puertos de salida:
  - `DocumentRepository`, `SignerRepository`, `CompanyRepository`.
  - `ZapSignClient` (Adapter HTTP) con operaciones mínimas: `create_doc`, `get_doc_status`.
  - `DocumentAnalyzer` (Strategy IA) con operación `analyze(text|url)`.

### Reglas de dependencia
- `domain` no depende de nada fuera del dominio.
- `application` depende de `domain` (y define interfaces de salida).
- `infrastructure` implementa interfaces de salida y depende de ORM/HTTP/SDK.
- `api` depende de `application` y mapea DTOs ↔ modelos externos (DRF Serializers).

### Convenciones de nombres (Python/Django)
- Archivos: `snake_case.py`
- Clases: `PascalCase`
- Funciones/variables: `snake_case`
- Constantes: `UPPER_SNAKE_CASE`
- Módulos de casos de uso: `use_cases/<verbo>_<sujeto>.py` (p.ej., `create_document.py`).
- Repositorios: `repositories/<agregado>_repository.py`.
- Adaptadores: `adapters/<proveedor>_client.py` (p.ej., `zapsign_client.py`).
- Serializers DRF: `serializers/<recurso>_serializer.py`.
- ViewSets DRF: `views/<recurso>_viewset.py`.

### Ejemplos mínimos (esqueleto)
```text
modules/document/domain/entities.py
  class Document(...), class Signer(...)

modules/document/application/ports.py
  class DocumentRepository(Protocol): ...
  class ZapSignClient(Protocol): ...
  class DocumentAnalyzer(Protocol): ...

modules/document/application/use_cases/create_document.py
  class CreateDocumentUseCase: def execute(self, dto: CreateDocumentDTO) -> DocumentDTO: ...

modules/document/infrastructure/repositories/document_repository_django.py
  class DjangoDocumentRepository(DocumentRepository): ...

modules/document/infrastructure/adapters/zapsign_client_http.py
  class HttpZapSignClient(ZapSignClient): ...

modules/document/infrastructure/adapters/analyzer_openai.py
  class OpenAIAnalyzer(DocumentAnalyzer): ...

modules/document/api/views/document_viewset.py
  class DocumentViewSet(ViewSet): ... # delega en casos de uso
```

### TDD y pruebas
- Tests de dominio: entidades/servicios puros.
- Tests de `application`: casos de uso con repos/adapters mockeados (fakes/stubs).
- Tests de `infrastructure`: repos con DB (marcados) y adapters HTTP con mocks.
- Tests de `api`: endpoints DRF, validaciones y permisos.
- Cobertura mínima: 85% (pipeline bloqueante).

### Observabilidad y resiliencia
- Decorator en adapters HTTP (retries, circuit breaker básico, métricas y logs JSON).
- Correlación de requests y trazas; límites de tasa si aplica.

### Seguridad y multitenancy
- Autenticación (JWT/Token) y autorización por `Company` (scoping en repos).
- Sanitización/validación estricta de entrada/salida (Serializers/DTOs).

### MCP y LLMs (puertos y herramientas)
- Definir herramientas MCP para exponer operaciones seguras: `get_document`, `list_documents`, `request_analysis`.
- Los LLMs consumen los puertos de `application` a través de MCP; nunca acceden directo a `infrastructure`.

### Relación con documentos del repo
- Este documento complementa `CONTRIBUTING.md` (flujo y reglas) y `PLAN_DE_EJECUCION.md` (fases, criterios y diagramas).


