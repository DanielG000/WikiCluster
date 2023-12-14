FROM python:3.11

#
ENV PYTHONUNBUFFERED=1

#Crea la carpeta dentro del contenedor
RUN mkdir -p /app
WORKDIR ./app

#Librerias de python necesarias
RUN pip install --upgrade pip
COPY requirements.txt /app
COPY .env /app
RUN pip install --no-cache-dir -r requirements.txt


#pone el codigo dentro del contenedor
#COPY . /app

#Expone el puerto para acceder
#EXPOSE ${BACKEND_PORT}

#Comandos que inician el servidor backend
CMD ["python", "runserver.py"]
