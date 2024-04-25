# Utiliza una imagen base de Python oficial
FROM python:3.9-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos requerimientos.txt en el contenedor
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install -r requirements.txt

# Copia el resto del código de la aplicación Flask en el contenedor
COPY . .

# Expone el puerto en el que se ejecutará la aplicación
EXPOSE 6000

# Comando para ejecutar la aplicación Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=6000"]
