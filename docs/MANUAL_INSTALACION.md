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

## ⚙️ Paso 2: Configuración del Backend (API REST)

El backend de la aplicación proporciona la lógica de transcripción a través de una API.

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
4. Instale las dependencias necesarias. Si existe un archivo `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
   _(Si están usando Flask, sería `pip install flask` o similar)._
5. Inicie el servidor local:
   ```bash
   python app.py
   ```
   _La consola indicará que el servidor está corriendo (usualmente en `http://localhost:5000` o `http://127.0.0.1:5000`). ¡No cierre esta terminal!_

## 🌐 Paso 3: Ejecución del Frontend

Como la arquitectura del frontend está completamente desacoplada (HTML, CSS y Vanilla JavaScript), no se requieren compiladores complejos.

1. Abra una **nueva pestaña** en su explorador de archivos.
2. Navegue hacia la carpeta `frontend/` del proyecto.
3. Haga doble clic en el archivo `index.html` para abrirlo directamente en su navegador web.
   - _Alternativa recomendada:_ Si usa VS Code, haga clic derecho sobre `index.html` y seleccione **"Open with Live Server"**.

¡Listo! Si su servidor backend está corriendo en la configuración por defecto y abrió el Frontend, ya puede interactuar con la aplicación.
