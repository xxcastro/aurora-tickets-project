
# 1. Actualizar el sistema e instalar dependencias base
sudo apt-get update -y
sudo apt-get install -y openjdk-11-jdk python3-pip wget curl

# 2. Instalar librerías de Python necesarias para el proyecto
# (Esto nos ahorrará fallos luego en el nodo Web y en Spark)
pip3 install pyspark==3.5.0 boto3 pandas mysql-connector-python fastapi uvicorn

# 3. Descargar Apache Spark 3.5.0 (Versión Hadoop 3)
cd /home/ubuntu
wget https://archive.apache.org/dist/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz

# 4. Descomprimir y mover a /opt/spark para que sea estándar
tar -xvzf spark-3.5.0-bin-hadoop3.tgz
sudo mv spark-3.5.0-bin-hadoop3 /opt/spark
sudo chown -R ubuntu:ubuntu /opt/spark

# 5. Configurar variables de entorno en .bashrc
# Usamos 'grep' para no duplicar líneas si ejecutas el script dos veces
if ! grep -q "SPARK_HOME" ~/.bashrc; then
  echo 'export SPARK_HOME=/opt/spark' >> ~/.bashrc
  echo 'export PATH=$PATH:/opt/spark/bin:/opt/spark/sbin' >> ~/.bashrc
  echo 'export PYSPARK_PYTHON=python3' >> ~/.bashrc
fi

# 6. Cargar los cambios en la sesión actual
export SPARK_HOME=/opt/spark
export PATH=$PATH:/opt/spark/bin:/opt/spark/sbin

echo "-----------------------------------------------"
echo " INSTALACIÓN COMPLETADA CON ÉXITO "
echo "-----------------------------------------------"
ls -l /opt/spark

