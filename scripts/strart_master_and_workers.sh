
# En la terminal del master
/opt/spark/sbin/start-master.sh

# En la terminal de los workers 
start-worker.sh spark://IP_MASTER_PRIVADA:7077

# Lanzar un trabajo a los clusters, desde la terminal del master
spark-submit \
  --master spark://172.31.93.4:7077 \
  --packages org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262 \
  process_aurora.py

# He añadido la configuración para que las descargas (ivy.home) también vayan a la RAM y no toquen el disco /dev/root
spark-submit \
  --master spark://172.31.93.4:7077 \
  --conf "spark.driver.extraJavaOptions=-Divy.default.ivy.user.dir=/run/spark-ivy" \
  --conf "spark.local.dir=/run/spark-tmp" \
  --packages org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262,mysql:mysql-connector-java:8.0.28 \
  job2_analytics.py