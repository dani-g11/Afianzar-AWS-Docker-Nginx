# 1. Usamos una imagen base oficial de Python ligera (Slim es ideal para producción/dev)
#    Django 6.1.2 requiere Python >= 3.12, por eso usamos 3.12-slim.
FROM python:3.12-slim

# 2. Evitamos que Python escriba archivos .pyc y aseguramos que los logs se vean en tiempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Establecemos el directorio de trabajo dentro del contenedor (el "quirófano")
WORKDIR /app

# 4. Copiamos los requerimientos e instalamos dependencias de Python
#    (Opcion A: SQLite, no necesitamos librerias del sistema para Postgres)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos el resto del código fuente del proyecto
COPY . /app/

# 6. Exponemos el puerto 8000
EXPOSE 8000

# 7. Comando por defecto al iniciar el contenedor
# Importante: 0.0.0.0 permite que el contenedor sea accesible desde fuera
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]