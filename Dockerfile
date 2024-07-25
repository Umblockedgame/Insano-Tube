# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && \
    apt-get install -y ffmpeg wget

# Copiar el archivo requirements.txt e instalar las dependencias de Python
COPY requirements.txt .
RUN pip install -r requirements.txt && \
    pip install --upgrade yt-dlp

# Instalar paquetes adicionales
RUN pip install yt-dlp flask waitress requests urllib3 timeago

# Actualizar yt-dlp a la última versión
RUN python3 -m pip install -U yt-dlp

# Copiar el resto del código de la aplicación
COPY . .

# Exponer el puerto que va a usar la aplicación
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python3", "main.py"]
