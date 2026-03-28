import pandas as pd
import numpy as np
import boto3
from datetime import datetime, timedelta

# --- CONFIGURACIÓN ---
BUCKET_NAME = "aurora-tickets-alexgavilanezcastro"  
NUM_EVENTOS = 200000

print(f"Generando {NUM_EVENTOS} registros para Aurora Tickets...")

# 1. Generar Eventos Sintéticos
data = {
    'event_id': range(1, NUM_EVENTOS + 1),
    'user_id': np.random.randint(1000, 5000, size=NUM_EVENTOS),
    'event_type': np.random.choice(['view_ticket', 'add_to_cart', 'search', 'login'], NUM_EVENTOS),
    'timestamp': [datetime.now() - timedelta(minutes=np.random.randint(0, 43200)) for _ in range(NUM_EVENTOS)],
    'platform': np.random.choice(['mobile', 'web', 'app'], NUM_EVENTOS)
}

df = pd.DataFrame(data)

# 2. Guardar localmente
file_name = "events_raw.csv"
df.to_csv(file_name, index=False)
print(f"Archivo {file_name} creado localmente.")

# 3. Subir a S3 (Capa RAW)
s3 = boto3.client('s3')
try:
    s3.upload_file(file_name, BUCKET_NAME, f"raw/{file_name}")
    print(f"¡ÉXITO! Archivo subido a s3://{BUCKET_NAME}/raw/")
except Exception as e:
    print(f"Error al subir: {e}")