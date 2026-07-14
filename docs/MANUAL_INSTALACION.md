# Manual de Instalación y Despliegue

Este documento sirve como guía paso a paso para configurar y ejecutar el **Transcriptor de Español a Braille** en un entorno de desarrollo local.

## 📋 Requisitos Previos

Antes de comenzar, asegúrese de tener instalado el siguiente software en su equipo:

- **Git** (para clonar el repositorio)
- **Python 3.8+** (para ejecutar el servidor backend)
- Un navegador web moderno (Chrome, Firefox, Edge, Safari)
- _Opcional:_ Visual Studio Code con la extensión "Live Server" para el frontend.

## 🚀 Paso 1: Clonar el Repositorio

Abra su terminal o consola de comandos y ejecute la siguiente instrucción para obtener una copia local del código:

```bash
git clone https://github.com/MarceloTorres70/transcriptor-braille.git
cd transcriptor-braille
```

## ⚙️ Paso 2: Configuración del Backend y Frontend

La aplicación se ejecuta desde un único servidor Flask que expone la interfaz web y la API REST.

1. Navegue hacia el directorio del backend:
   ```bash
   cd backend
   ```
2. Cree un entorno virtual de Python (recomendado):
   ```bash
   python -m venv venv
   ```
3. Active el entorno virtual:
   - En Windows: `venv\Scripts\activate`
   - En Mac/Linux: `source venv/bin/activate`
4. Instale las dependencias necesarias del entorno activo.
5. Inicie la aplicación desde la raíz del proyecto:
   ```bash
   python app.py
   ```
6. Abra la interfaz en el navegador en:
   ```
   http://127.0.0.1:5000/
   ```
7. El proyecto está estructurado bajo **Clean Architecture**. Puede ejecutar las pruebas con:
   ```bash
   pytest
   ```
   _La consola indicará el estado de las pruebas unitarias del dominio._

## 🌐 Paso 3: Ejecución del Frontend

El frontend está integrado en el servidor Flask, pero también puede abrirse directamente si desea revisar la vista estática.

1. Abra una **nueva pestaña** en su explorador de archivos.
2. Navegue hacia la carpeta `frontend/` del proyecto.
3. Haga doble clic en el archivo `index.html` para abrirlo directamente en su navegador web.
   - _Alternativa recomendada:_ Si usa VS Code, haga clic derecho sobre `index.html` y seleccione **"Open with Live Server"**.

Si el servidor Flask ya está activo, la opción recomendada es usar la URL principal del proyecto en `http://127.0.0.1:5000/`, porque esa ruta evita el error 404 y mantiene el frontend y la API en el mismo origen.

¡Listo! El frontend puede abrirse y probarse visualmente en local; la validación funcional del backend se realiza mediante pruebas unitarias hasta integrar el entrypoint REST.
