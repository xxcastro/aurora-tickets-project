# 🌌 Aurora Tickets: End-to-End Cloud Data Pipeline

Este proyecto implementa una arquitectura de datos completa en **AWS**, diseñada para procesar y analizar eventos de clickstream de una plataforma de venta de tickets. Utiliza un clúster de **Apache Spark** para la transformación de datos y **AWS RDS** para el almacenamiento de métricas de negocio.

## 🏗️ Arquitectura del Sistema
La solución sigue el flujo de datos **S3 (Raw) ➔ Spark (ETL) ➔ S3 (Curated) ➔ Spark (Analytics) ➔ RDS (MySQL)**.

* **Ingesta:** AWS S3 (Capa Raw en formato JSON).
* **Procesamiento:** Clúster Spark Standalone (1 Master + 2 Workers) sobre EC2.
* **Almacenamiento:** AWS RDS MySQL para métricas finales y S3 Parquet para datos curados.
* **Observabilidad:** CloudWatch Logs + Dashboards personalizados.
* **Acceso:** API REST construida con FastAPI.

## 📂 Estructura del Repositorio
* `spark-jobs/`: Scripts de PySpark para limpieza (`job1`) y analítica (`job2`).
* `api/`: Código fuente de la API FastAPI.
* `infrastructure/`: Configuración del Agente de CloudWatch y esquemas SQL.
* `docs/`: Memoria técnica bajo metodología CRISP-DM y capturas de evidencia.

## 🚀 Guía de Ejecución

### 1. Preparación del Entorno
Debido a las limitaciones de espacio en disco de los nodos (8GB), los Jobs de Spark están configurados para usar la memoria RAM (`/run`) como almacenamiento temporal de artefactos:
```bash
sudo mkdir -p /run/spark-ivy /run/spark-tmp
sudo chmod -R 777 /run/spark-*
```

### 2. Lanzamiento del Pipeline de Analítica
Para procesar los datos y enviarlos al RDS MySQL:
```bash
spark-submit \
  --master spark://<MASTER_IP>:7077 \
  --conf "spark.driver.extraJavaOptions=-Divy.default.ivy.user.dir=/run/spark-ivy" \
  --conf "spark.local.dir=/run/spark-tmp" \
  --packages org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262,mysql:mysql-connector-java:8.0.28 \
  job2_analytics.py
```

## 📊 Dashboard de Monitorización
Se ha configurado un Dashboard en **CloudWatch** que permite visualizar:
1.  **Volumen de Ingesta:** Eventos procesados por minuto.
2.  **Detección de Errores:** Filtro en tiempo real de excepciones de Spark y la API.
3.  **Métricas de Éxito:** Confirmación de cargas completadas en la base de datos.

## 🛠️ Retos Técnicos Superados
* **Optimización de Almacenamiento:** Resolución del error `No space left on device` mediante la redirección de directorios temporales de Spark a `tmpfs` (RAM).
* **Conectividad JDBC:** Configuración de Security Groups y reglas de red para la comunicación segura entre el clúster y el RDS.
* **Evolución de Esquema:** Gestión de transformaciones de datos para asegurar la creación de columnas de fecha (`dt`) necesarias para el reporte de KPIs.

---
**Autor:** Alex Gavilanez Castro  
**Entorno:** AWS Academy - Cloud Computing Project

