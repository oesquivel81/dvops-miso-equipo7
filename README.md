# Microservicio Blacklist de Emails

Este proyecto es un microservicio en Python usando Flask, Poetry y PostgreSQL para gestionar una lista negra de emails.

## Características
- Arquitectura limpia (controllers, services, repositories, dtos, domain, infrastructure)
- Persistencia con SQLAlchemy y PostgreSQL
- Validación y serialización con Marshmallow
- Seguridad con token Bearer fijo
- Inyección de dependencias con dependency-injector
- Manejo global de errores y logging
- Ejemplos de uso con Postman y curl

## Estructura de carpetas
- api/controllers: Controladores Flask
- application/dtos/request: DTOs de entrada
- application/dtos/response: DTOs de salida
- application/services: Lógica de negocio
- domain/models: Modelos de dominio
- domain/repositories: Interfaces de repositorios
- domain/exceptions: Excepciones de dominio
- infrastructure/persistence/entities: Entidades SQLAlchemy
- infrastructure/persistence/repositories: Implementaciones repositorios
- infrastructure/security: Seguridad y autenticación
- infrastructure/container: Contenedor de dependencias
- infrastructure/config: Configuración y utilidades

## Instalación
1. Clona el repositorio
2. Instala Poetry si no lo tienes: https://python-poetry.org/docs/#installation
3. Ejecuta `poetry install` para instalar dependencias
4. Copia el archivo `.env.example` a `.env` y ajusta las variables si es necesario

## Base de datos y Docker
- Levanta PostgreSQL y pgAdmin con:
  `docker-compose up -d`
- Accede a pgAdmin en http://localhost:5050 (usuario: admin@admin.com, contraseña: admin)
- Crea las tablas ejecutando:
  `poetry run python -m scripts.create_tables`

## Ejecución del backend
`poetry run python main.py`

## Endpoints principales
- POST /blacklists/
  - email (obligatorio)
  - app_uuid (obligatorio, UUID)
  - blocked_reason (opcional, máx 255)
- GET /blacklists/<email>
  - Devuelve si el email está en blacklist y el motivo

## Seguridad
- Todas las rutas requieren header:
  `Authorization: Bearer fixedtoken`

## Pruebas con Postman
- Importa el archivo `blacklist_postman_collection.json` en Postman
- Prueba los endpoints con los ejemplos incluidos

## Pruebas con PowerShell
POST:
```
Invoke-RestMethod -Uri "http://localhost:5000/blacklists/" -Method Post -Headers @{Authorization="Bearer fixedtoken"; "Content-Type"="application/json"} -Body '{"email": "test@example.com", "app_uuid": "123e4567-e89b-12d3-a456-426614174000", "blocked_reason": "spam"}'
```
GET:
```
Invoke-RestMethod -Uri "http://localhost:5000/blacklists/test@example.com" -Method Get -Headers @{Authorization="Bearer fixedtoken"}
```

## Notas
- El backend usa logging para debug y errores
- El archivo .gitignore excluye cachés, entornos y archivos locales
- Puedes extender la lógica agregando más endpoints o reglas de negocio
