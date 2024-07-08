# Usa la imagen oficial de Rasa como base
FROM rasa/rasa:latest

USER root

# Copia los archivos de tu proyecto Rasa (modelos, data, etc.) al contenedor
COPY ./app /app

# Copia los modulos de python necesarios para instalar con PIP
COPY ./requirements.txt /app

# Copia el script de entrada al contenedor
COPY ./app/entrypoint.sh /app/entrypoint.sh

# Da permisos de ejecución al script de entrada
#RUN chmod +x /app/entrypoint.sh

# Establece el directorio de trabajo
WORKDIR /app
RUN apt-get update && \
    apt-get install -y gcc g++ unixodbc-dev default-libmysqlclient-dev curl wget && \
    wget  https://dev.mysql.com/get/Downloads/Connector-ODBC/9.0/mysql-connector-odbc-9.0.0-linux-glibc2.28-x86-64bit.tar.gz

RUN tar -xzf mysql-connector-odbc-9.0.0-linux-glibc2.28-x86-64bit.tar.gz
RUN mv mysql-connector-odbc-9.0.0-linux-glibc2.28-x86-64bit/lib/libmyodbc9w.so /usr/local/lib/
RUN mv mysql-connector-odbc-9.0.0-linux-glibc2.28-x86-64bit/lib/libmyodbc9a.so /usr/local/lib/
RUN mv mysql-connector-odbc-9.0.0-linux-glibc2.28-x86-64bit/bin/myodbc-installer /usr/bin/ && \
    rm -rf mysql-connector-odbc-9.0.0-linux-glibc2.28-x86-64bit.tar.gz mysql-connector-odbc-9.0.0-linux-glibc2.28-x86-64bit && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Configurar el DSN ODBC
RUN echo "[ODBC Driver 17 for MySQL]" > /etc/odbcinst.ini
RUN echo "Description=MySQL ODBC driver" >> /etc/odbcinst.ini
RUN echo "Driver=/usr/local/lib/libmyodbc9w.so" >> /etc/odbcinst.ini
RUN echo "UsageCount=1" >> /etc/odbcinst.ini


RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expone los puertos en los que Rasa y las acciones correrán
EXPOSE 5005 5055

USER rasa
# Configura el script de entrada como el comando por defecto
ENTRYPOINT ["/app/entrypoint.sh"]

