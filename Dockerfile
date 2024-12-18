FROM python:3.12-slim

WORKDIR /app

# Copier les fichiers nécessaires
COPY requirements.txt .
COPY pipelines/ pipelines/
COPY steps/ steps/
COPY src/ src/
COPY data/ data/
COPY run_deployment.py .
COPY config.yaml .
COPY init-mlflow.sh .
COPY streamlit/ streamlit/

# Rendre le script d'initialisation exécutable
RUN chmod +x init-mlflow.sh

# Installation des dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Initialize MLflow first
RUN ./init-mlflow.sh

# Create startup script
COPY <<EOF /app/start.sh
#!/bin/bash
# Keep container running
python run_deployment.py
streamlit run streamlit/app.py
EOF

RUN chmod +x /app/start.sh

# Exposer les ports MLflow et streamlit
EXPOSE 8000
EXPOSE 8501

# Use the startup script instead
CMD ["/app/start.sh"]