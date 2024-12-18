# Price Predictor System

An ML-powered house price prediction system using MLflow for model tracking and deployment, ZenML for pipeline management, and Streamlit for the user interface.

## 🏗 Architecture

- **MLflow**: Model tracking and deployment
- **ZenML**: ML pipeline orchestration
- **Streamlit**: Web interface
- **Docker**: Containerization
- **GitHub Actions**: CI/CD

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
docker compose up --build
```

The application will be available at:
- Web UI: http://localhost:80
- MLflow UI: http://localhost:8000

### Manual Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/prices-predictor-system.git
cd prices-predictor-system
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize MLflow:
```bash
./init-mlflow.sh
```

5. Run the deployment:
```bash
python run_deployment.py
```

6. Start the Streamlit interface:
```bash
streamlit run streamlit/app.py
```

## 📊 Model Training

To train a new model:

```bash
python run_pipeline.py
```

## 🔄 CI/CD

The project includes GitHub Actions workflows for:
- Automated testing
- Docker image building
- Container registry publishing

## 📝 Project Structure

```
├── data/               # Training data
├── pipelines/         # ZenML pipelines
├── steps/             # Pipeline steps
├── src/              # Core functionality
├── streamlit/        # Web interface
├── tests/            # Unit tests
├── Dockerfile        # Container definition
├── docker-compose.yaml
├── requirements.txt
└── README.md
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Open a Pull Request

## 📜 License

MIT License - see LICENSE file for details