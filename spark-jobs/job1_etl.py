from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp

BUCKET = "s3a://aurora-tickets-alexgavilanezcastro"

spark = SparkSession.builder \
    .appName("AuroraAnalysis") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .getOrCreate()

# 1. Cargar Datos
events = spark.read.csv(f"{BUCKET}/raw/events_raw.csv", header=True, inferSchema=True)
prices = spark.read.csv(f"{BUCKET}/raw/prices.csv", header=True, inferSchema=True)

# 2. Transformación: Limpieza y Join
# Queremos saber el valor de lo que hay en los carritos (add_to_cart)
analysis = events.join(prices, "event_type") \
    .filter(col("event_type") == "add_to_cart") \
    .withColumn("processed_at", current_timestamp())

# 3. Guardar en Capa CURATED (Formato Parquet - Más eficiente)
analysis.write.mode("overwrite").parquet(f"{BUCKET}/curated/events_refined/")

# 4. Calcular un KPI simple: Total valor en carritos
total_value = analysis.agg({"base_price": "sum"}).collect()[0][0]

print(f"\n\n*****************************************")
print(f"ANÁLISIS COMPLETADO")
print(f"VALOR TOTAL EN CARRITOS: {total_value}€")
print(f"*****************************************\n\n")

spark.stop()
