# AI Workforce Scheduler 🚀

![Generate Synthetic Data](https://github.com/amachicielo/ai-workforce-scheduler/actions/workflows/generate.yml/badge.svg)

## Overview
This project is part of a university **Final Year Project (TFG)** and also designed as a professional portfolio piece.  
It demonstrates how to build an **AI/ML-powered workforce and transportation scheduler** with modern practices in **MLOps, DevOps, and Cloud**.

The system is **modular, reproducible, and scalable**, built with **Docker, Makefile, GitHub Actions**, and integrated with **Azure free services** and **Databricks Community Edition** for future scalability.

---

## Features
✅ Synthetic dataset generation (workers, drivers, workplaces, shifts, assignments)  
✅ Modular Python scripts (with Docker containers)  
✅ Single pipeline generator (`generate_all.py`)  
✅ Makefile for easy execution (`make generate-all`)  
✅ GitHub Actions CI/CD pipeline  
✅ Automatic dataset publishing as artifacts and GitHub Releases  
✅ Ready for future ML models, dashboards, and Azure integration  

---

## Project Structure
```
ai-workforce-scheduler/
│
├── data/                  # Generated datasets (CSV)
├── ml/                    # Data generation + ML models
│   ├── generate_all.py
│   ├── generate_workers.py
│   ├── generate_drivers.py
│   ├── generate_workplaces.py
│   └── generate_shifts.py
├── dash/                  # Visualization dashboard (Plotly Dash, future)
├── notifier/              # Email automation (future)
├── docker-compose.yml     # Container orchestration
├── Makefile               # Shortcuts for running scripts
└── .github/workflows/     # GitHub Actions (CI/CD)
```

---

## How to Run Locally

### 1. Requirements
- Linux or WSL2 (recommended)  
- Docker + Docker Compose  
- Make installed (`sudo apt install make`)

### 2. Generate All Datasets
```bash
make generate-all
```

### 3. Generate a Specific Dataset
```bash
make generate-workers
make generate-drivers
make generate-workplaces
make generate-shifts
```

### 4. Clean datasets
```bash
make clean
```

---

## CI/CD with GitHub Actions
Every push to `main` will:
1. Build the Docker image.  
2. Run `make generate-all`.  
3. Upload datasets as **artifacts**.  
4. Publish a GitHub Release with a downloadable ZIP file.  

---

## Download Latest Datasets
👉 [Download synthetic-datasets.zip (latest release)](https://github.com/amachicielo/ai-workforce-scheduler/releases/latest)

---

## Next Steps (Planned)
- 📊 Plotly Dash dashboard (map of workers, driver routes, KPIs)  
- 🧠 ML Models:
  - Worker clustering by location (KMeans)
  - Absence prediction (classification)
  - Driver allocation optimization (OR-Tools / Pyomo)
- ☁️ Azure Free Services:
  - Azure ML (model training & registry)
  - Azure Blob Storage (datasets)
  - Azure Logic Apps (schedule email notifications)
- 🚀 Deployment:
  - From Docker Compose → Azure Kubernetes Service (AKS)
  - Future reinforcement learning for real-time reallocation

---

## License
MIT License © 2025  