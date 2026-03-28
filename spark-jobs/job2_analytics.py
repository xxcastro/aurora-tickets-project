from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, sum as _sum, lit, when, to_date

# --- CONFIGURACIÓN ---
S3_CURATED = "s3a://aurora-tickets-alexgavilanezcastro/curated/events_refined/"
RDS_ENDPOINT = "aurora-db.c1maqiq4mto2.us-east-1.rds.amazonaws.com"
JDBC_URL = f"jdbc:mysql://{RDS_ENDPOINT}:3306/aurora_db"

spark = SparkSession.builder \
    .appName("Aurora_Job2_Analytics") \
    .getOrCreate()

# 1. LEER DATOS CURADOS
df = spark.read.parquet(S3_CURATED)

# CREAR COLUMNA 'dt' a partir del timestamp si no existe
if "dt" not in df.columns:
    df = df.withColumn("dt", to_date(col("timestamp")))

# --- PRODUCTO A: FUNNEL DIARIO ---
funnel_df = df.groupBy("dt", "event_type").agg(count("*").alias("sessions_total"))

# --- PRODUCTO B: RANKING DE EVENTOS ---
rank_df = df.groupBy("dt", "event_id").agg(
    count(when(col("event_type") == "view", 1)).alias("detail_views"),
    count(when(col("event_type") == "purchase", 1)).alias("purchases"),
    _sum("base_price").alias("revenue_total")
)

# --- PRODUCTO C: DETECCIÓN DE ANOMALÍAS ---
anomalies_df = df.groupBy("dt", "user_id").agg(count("*").alias("requests")).filter("requests > 500") \
    .withColumn("is_anomaly", lit(True)) \
    .withColumn("reason", lit("High request volume"))

# --- ESCRITURA EN RDS MYSQL ---
db_properties = {
    "user": "admin",
    "password": "Aurora2026!",
    "driver": "com.mysql.cj.jdbc.Driver"
}

print("Enviando métricas finales a RDS MySQL...")

try:
    funnel_df.write.jdbc(url=JDBC_URL, table="metrics_funnel_daily", mode="overwrite", properties=db_properties)
    rank_df.write.jdbc(url=JDBC_URL, table="metrics_event_rank", mode="overwrite", properties=db_properties)
    anomalies_df.write.jdbc(url=JDBC_URL, table="metrics_anomalies", mode="overwrite", properties=db_properties)
    print("¡ÉXITO TOTAL! Las tablas están en el RDS.")
except Exception as e:
    print(f"Error RDS: {e}")

spark.stop()

