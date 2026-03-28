import pandas as pd
import boto3

BUCKET_NAME = "aurora-tickets-alexgavilanezcastro"

# --- 1. Crear Campañas ---
campaigns_data = {
    'campaign_id': [1, 2, 3, 4],
    'campaign_name': ['Black Friday', 'Summer Festival', 'Winter Promo', 'New Year Gala'],
    'discount_percentage': [20, 15, 10, 25]
}
df_camp = pd.DataFrame(campaigns_data)
df_camp.to_csv("campaigns.csv", index=False)

# --- 2. Crear Precios de Entradas (Transactions) ---
# Simulamos precios para los tipos de eventos
prices_data = {
    'event_type': ['view_ticket', 'add_to_cart', 'search', 'login'],
    'base_price': [0, 45.50, 0, 0] # Solo 'add_to_cart' genera valor potencial
}
df_prices = pd.DataFrame(prices_data)
df_prices.to_csv("prices.csv", index=False)

# --- Subir a S3 ---
s3 = boto3.client('s3')
s3.upload_file("campaigns.csv", BUCKET_NAME, "raw/campaigns.csv")
s3.upload_file("prices.csv", BUCKET_NAME, "raw/prices.csv")

print("¡Archivos extra subidos con éxito a la capa RAW!")