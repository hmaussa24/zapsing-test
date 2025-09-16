## ZapSign — Desafío de Producto

En ZapSign, desarrollamos soluciones para hacer que el proceso de firma digital sea más simple, rápido y seguro. Queremos evaluar cómo enfrentas problemas reales de producto, yendo más allá del código: pensamos en arquitectura, integraciones, usabilidad, automatizaciones y comunicación con el equipo.

Este desafío simula una entrega real de un squad de ZapSign. Está enfocado en las siguientes habilidades:

### Habilidades evaluadas
- **Construcción de APIs e interfaces con buenas prácticas**
- **Integraciones con servicios externos (ZapSign y n8n)**
- **Aplicación práctica de análisis con IA**
- **Escritura de código testeable**
- **Capacidad de interpretar una user story y generar valor para el cliente final**
- **Comunicación técnica mediante documentación y debugging en vivo**

### User Story
Como gerente de una empresa cliente de ZapSign, quiero poder registrar y gestionar mis documentos y firmantes directamente desde la plataforma, para acelerar la creación de contratos, firmar con mayor agilidad y obtener insights automáticos sobre los documentos enviados.

### Objetivo
Implementar un nuevo módulo de gestión de documentos, con análisis inteligente de contenido e integración mediante automatizaciones externas (como n8n), permitiendo que las empresas clientes tengan mayor control y productividad en el flujo de firmas digitales.

### Criterios de aceptación
- **Panel de empresa**: crear, listar, editar y eliminar `Companies`, `Documents` y `Signers`, con una interfaz fluida (sin recarga).
- **Creación de documento**: al crear un documento, enviarlo automáticamente a la API de ZapSign y almacenar `token` y `open_id` devueltos.
- **Análisis con IA**: al guardar el documento, analizar el contenido con IA y presentar tópicos faltantes, un resumen e insights útiles.
- **Endpoints RESTful**: exponer endpoints autenticados para crear documentos, solicitar nuevos análisis e informes.
- **Pruebas automatizadas**: garantizar estabilidad de rutas y funcionalidades principales.
- **README claro**: explicar cómo levantar el sistema, ejecutar pruebas, consumir endpoints y entender la lógica de IA aplicada.

### Notas técnicas
- **Backend**: Django + DRF con PostgreSQL
- **Frontend**: Angular con componentes reactivos
- **Integraciones**:
  - **ZapSign API**: creación y estado de documentos
  - **IA**: OpenAI, HuggingFace, LangChain o spaCy
  - **n8n**: endpoints RESTful autenticados para automatizaciones
- **Pruebas**: Pytest (API) y Jest (frontend)
- **Infra**: Docker para configuración local
- **Bonus**:
  - **Panel con alertas automáticos**
  - **Workflow n8n demostrativo**
  - **Clean Architecture o DDD**
  - **TDD**

### Precondiciones
- Crear una cuenta en el ambiente sandbox de ZapSign: [`https://sandbox.app.zapsign.com.br/`](https://sandbox.app.zapsign.com.br/)
- Generar el `api_token` de ZapSign y almacenarlo en la tabla `Company`, columna `api_token`.
- Crear la base PostgreSQL y las tablas `Company`, `Documents` y `Signers` mediante migrations (ver diagrama de clases al final).

### Observaciones
1. **Documentación de la API**: [`https://docs.zapsign.com.br/`](https://docs.zapsign.com.br/)
2. **Diseño**: no será evaluado (puedes usar Lovable, Bootstrap/Material, etc.).
3. **Referencias**: se incluyen diagramas de flujo, clases y base de datos al final del documento.

### Flujo principal
1. **Creación de cuenta en el sandbox de ZapSign**: registrarse en [`https://sandbox.app.zapsign.com.br/`](https://sandbox.app.zapsign.com.br/).
2. **Obtención del API Token**: obtener el `api_token` y guardarlo en `Company.api_token`.
3. **Implementación del CRUD de documentos**: crear en el frontend (Angular/TypeScript) un CRUD que liste todos los documentos almacenados en la base.
4. **Formulario de creación de documento**: componente separado con campos para nombre del documento, datos del firmante (nombre y correo) y URL de un PDF.
5. **Envío a la API de ZapSign**: al enviar el formulario, llamar al endpoint `https://sandbox.api.zapsign.com.br/api/v1/docs/`.
6. **Respuesta y almacenamiento**: guardar en la base los datos devueltos (`open_id`, `token`, `status`, etc.).
7. **Actualización del frontend**: mostrar mensaje de éxito y refrescar el componente del CRUD sin recargar la página.

### Operaciones CRUD
1. **Create (Crear)**: crear documentos y firmantes enviando la información a la API de ZapSign.
2. **Read (Leer)**: listar todos los documentos en `Documents` con sus firmantes asociados en `Signers`.
3. **Update (Actualizar)**: actualizar detalles de documentos o firmantes.
4. **Delete (Eliminar)**: eliminar un documento y sus firmantes asociados de la base local.

### Gestión de la base de datos
- **Company**: información de la empresa, incluyendo el `api_token`.
- **Documents**: `open_id`, `token`, `name`, `status`, fecha de creación y usuario que lo creó.
- **Signers**: nombre, correo, estado y `token` asociado al documento.

### Integración con el Frontend
1. El frontend en Angular/TypeScript interactúa con el backend en Django mediante APIs RESTful.
2. Cuando un documento es creado con éxito, el frontend debe actualizar dinámicamente la lista de documentos sin necesidad de recargar la página completa, proporcionando una experiencia de usuario continua.
