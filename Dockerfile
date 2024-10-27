# Usar imagen base de Fedora
FROM fedora:latest

# Actualizar e instalar paquetes necesarios
RUN dnf -y update && \
    dnf -y install python3 python3-pip

# Copiar los archivos necesarios al contenedor
COPY main.py /app/main.py
COPY token.txt /app/token.txt
COPY token_open.txt /app/token_open.txt
COPY status.txt /app/status.txt

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar las dependencias del archivo requirements.txt si existen
COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Ejecutar el script main.py al iniciar el contenedor
CMD ["python3", "main.py"]
