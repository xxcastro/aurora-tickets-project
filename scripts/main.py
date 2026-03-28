from fastapi import FastAPI, HTTPException
import boto3
import pandas as pd
from io import BytesIO

app = FastAPI(title="Aurora Tickets API", description="Dashboard de KPIs de Big Data")

# Configuración del Data Lake
BUCKET_NAME = "aurora-tickets-alexgavilanezcastro"
S3_PATH = "curated/events_refined/" # La carpeta que creó Spark

s3 = boto3.client('s3')

@app.get("/")
def home():
    return {"status": "online", "endpoint": "/kpis", "message": "Infraestructura Aurora Lista"}

@app.get("/kpis")
def get_metrics():
    try:
        # 1. Listamos los archivos en la carpeta curated de S3
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=S3_PATH)
        
        # 2. Buscamos el primer archivo .parquet generado por Spark
        parquet_files = [obj['Key'] for obj in response.get('Contents', []) if obj['Key'].endswith('.parquet')]
        
        if not parquet_files:
            raise HTTPException(status_code=404, detail="No se han encontrado datos procesados en S3")

        # 3. Leemos el archivo directamente desde S3 a un DataFrame de Pandas
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=parquet_files[0])
        df = pd.read_parquet(BytesIO(obj['Body'].read()))

        # 4. Calculamos el KPI en tiempo real sobre los datos curados
        total_value = float(df['base_price'].sum())
        total_events = len(df)

        return {
            "kpi_name": "Valor Total en Carritos (Add to Cart)",
            "total_value_eur": round(total_value, 2),
            "processed_records": total_events,
            "data_source": f"s3://{BUCKET_NAME}/{S3_PATH}",
            "currency": "EUR"
        }
    except Exception as e:
        return {"error": str(e), "tip": "Asegúrate de que el Web Server tenga el IAM Role asignado"}

