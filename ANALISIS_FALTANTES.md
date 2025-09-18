## Análisis de faltantes y próximos pasos

### Autenticación
- Falta endpoint de refresh token (el plan menciona `POST /api/auth/refresh`). Hoy `login` retorna solo `access`.
- Inconsistencia: vistas actuales usan JWT propio en `auth_views.py` mientras `settings.py` tiene SimpleJWT configurado. Definir uno (recomendado SimpleJWT con `access` + `refresh`) y documentar.
- Estándar de errores: unificar payloads de error (p. ej., `{ "detail": "..." }`) y códigos por caso.

### Swagger / OpenAPI
- Estandarizar ejemplos (request/response) en todos los endpoints (Documents, Signers, Company, Auth). Para Auth, usar ejemplos compactos (a nivel serializer o descripción Markdown) para evitar sobrecargar la UI.
- Definir esquema de seguridad global Bearer y aplicarlo a endpoints protegidos.
- Añadir ejemplos de 400/401/404 consistentes.

### Flujo de Documentos vs INSTRUCTION.MD
- INSTRUCTION.MD indica envío automático a ZapSign al crear el documento. Implementación actual lo hace manualmente vía `send_to_sign`. Decidir: mantener manual (mejor UX con validaciones de signers) o volver automático. Ajustar documentación y criterios en consecuencia.

### Análisis con IA
- Modelo `DocumentAnalysis` no contempla todos los campos del plan (faltan `missing_topics`, `insights`, `model_info`).
- Falta endpoint para forzar reanálisis: `POST /api/documents/{id}/analyze`.
- Falta estrategia IA real (OpenAI/spaCy) con `AnalyzerFactory`; hoy el flujo depende de n8n (mock). Documentar roadmap para proveedor IA real.

### Automatizaciones (n8n / RabbitMQ)
- Documentar claramente la configuración de `AUTOMATION_API_KEY` y el flujo con RabbitMQ + worker (arranque del worker en local/prod).
- Añadir tests de integración que simulen el callback de n8n con auth y verifiquen upsert idempotente.

### Seguridad
- `Company.email` debería tener `UniqueConstraint` e índice a nivel de DB (además de validación en código).
- Rate limiting básico para `POST /api/auth/login` y `POST /api/auth/register`.
- Políticas de expiración/rotación de tokens y uso de `refresh` si se adopta SimpleJWT.

### Docker / Infraestructura
- `docker-compose.yml` no incluye servicios `backend` y `frontend` ni sus Dockerfiles. Agregar servicios y redes.
- Definir comando para lanzar el worker de automatización (`manage.py run_automation_worker`) en Docker/compose.
- Variables de entorno completas en `.env.example` y README (incluyendo JWT/IA/n8n/RabbitMQ).

### Frontend (Angular)
- Faltan pruebas (Jest/Testing Library) para Auth pages, guard e interceptor.
- Manejo de refresh token en interceptor si se adopta SimpleJWT con `refresh`.
- Accesibilidad (labels, aria) y mensajes de error consistentes.

### Pruebas y calidad
- Configurar umbrales de cobertura (backend ≥85%, frontend ≥80%) y CI/pre-commit hooks (lint + tests).
- Revisar y actualizar tests afectados por el cambio de contrato de `login` (si se añade `refresh`).

### Documentación
- README: agregar ejemplos de requests/responses (Auth, Documents, Signers), URL de Swagger y tabla exhaustiva de variables de entorno.
- Incluir colección Postman/Insomnia exportada.

### Priorización sugerida
1. Unificar autenticación con SimpleJWT (access + refresh), adaptar frontend e incrementar seguridad.
2. Completar módulo de análisis IA: campos faltantes y `POST /documents/{id}/analyze`.
3. Dockerizar backend/frontend y worker; scripts de arranque y documentación.
4. Estandarizar Swagger (seguridad global + ejemplos) y añadir colección Postman.

