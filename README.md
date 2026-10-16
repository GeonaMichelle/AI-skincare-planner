# SkinIQ — AI Skin Intelligence & Personalized Skincare Planner

[![Deployment Status](https://img.shields.io/badge/Deployment-Live%20on%20Render-brightgreen?style=for-the-badge&logo=render)](https://skiniq-backend-u83e.onrender.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas%20%7C%20PyMongo-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

An AI-powered clinical skincare intelligence platform that formulates personalized skincare regimens, analyzes skin health profiles, tracks daily biometric vitals, and monitors skin barrier recovery. Built with dedicated, role-tailored workstations for **Consumers**, **Skincare Consultants**, **Dermatologists (MD)**, and **Platform Administrators**.

---

## 🌐 Live Production Deployment

| Service | URL |
| :--- | :--- |
| **Live Web App** | [https://skiniq-backend-u83e.onrender.com](https://skiniq-backend-u83e.onrender.com) |
| **Interactive API Docs (Swagger UI)** | [https://skiniq-backend-u83e.onrender.com/docs](https://skiniq-backend-u83e.onrender.com/docs) |
| **ReDoc Technical Specification** | [https://skiniq-backend-u83e.onrender.com/redoc](https://skiniq-backend-u83e.onrender.com/redoc) |
| **Production Health Probe** | [https://skiniq-backend-u83e.onrender.com/api/health](https://skiniq-backend-u83e.onrender.com/api/health) |

---

## ✨ System Features & Workstations

### 1. Consumer Skin Health App (`USER`)
* **AI Skincare Formulation Engine**: Generates morning and evening multi-step routines tailored to skin type, oil characteristics, sensitivities, and clinical goals.
* **Daily Lifestyle & Vitals Tracking**: Logs daily water intake (with dynamic circular glass hydration meter), deep sleep duration, stress metrics, UV index, and pollution exposure.
* **Skin Recovery Scoring**: Calculates real-time composite recovery and barrier health scores.
* **Ingredient Intelligence**: Searches and analyzes active ingredients with compatibility checks, comedogenic ratings, and safety flags.

### 2. Consultant Suite (`SKINCARE_CONSULTANT`)
* **Client Intake Queue**: Manage incoming consultation requests and review comprehensive client skin dossiers.
* **Prescription Studio**: Prescribe custom ingredient formulations and product regimens.
* **Ingredient Synergy Matrix**: Evaluates chemical conflicts (e.g., Retinoids + High-strength AHAs/BHAs, Vitamin C stability).

### 3. Dermatologist Clinical Workstation (`DERMATOLOGIST`)
* **Diagnostic Triage**: Clinical staging for conditions such as Acne Vulgaris (Grade I-IV), Rosacea, and Hyperpigmentation.
* **Rx Active Titration**: Formulate medical-grade actives (Tretinoin, Hydroquinone, Azelaic Acid) with real-time contraindication warnings.

### 4. Platform Administration & Security (`ADMINISTRATOR`)
* **RBAC Management**: Real-time user directory with instant role updates and account audits.
* **Regulatory Compliance**: INCI compliance monitoring against European and FDA cosmetics registries.
* **Executive Telemetry**: Real-time system latency, database health metrics, and model telemetry.

---

## 🔐 Built-in 1-Click Demo Accounts

The live deployment includes pre-seeded demo accounts. Click any of the **1-Click Role Switcher** buttons on the sign-in modal, or log in manually:

| Role | Email | Password |
| :--- | :--- | :--- |
| **Consumer** | `user@skiniq.ai` | `Password123!` |
| **Skincare Consultant** | `consultant@skiniq.ai` | `ConsultantPass2026!` |
| **Dermatologist (MD)** | `derm@skiniq.ai` | `DermPass2026!` |
| **System Administrator** | `admin@skiniq.ai` | `AdminPass2026!` |

---

## 🏗️ Architecture & Technology Stack

* **Backend**: FastAPI (Python 3.11), PyMongo with SRV DNS resolver, Pydantic v2 schemas, JWT authentication (HS256 with 24-hr expiry), Bcrypt hashing.
* **Frontend**: Vanilla ES6+ JavaScript, Responsive CSS3 Glassmorphism design system, Chart.js telemetry visualizations, Canvas wave animations.
* **Database**: MongoDB Atlas (Cloud Managed Cluster) with automatic indexing, plus in-memory fallback for isolated testing.
* **Security Middleware**: Strict Content-Security and Transport headers (`nosniff`, `X-Frame-Options: DENY`, `HSTS`, `GZipMiddleware`).
* **Containerization**: Unified Docker container hosting both backend API and static frontend SPA on a single origin.

---

## 💻 Local Development Setup

### Prerequisites
* Python 3.11+
* Git
* (Optional) Docker & Docker Compose

### 1. Clone the Repository
```bash
git clone https://github.com/GeonaMichelle/AI-skincare-planner.git
cd AI-skincare-planner
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Update `.env` with your MongoDB URI:
```env
MONGO_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority
MONGO_DB_NAME=skiniq_prod_db
SECRET_KEY=your_jwt_secret_key
ENVIRONMENT=development
SEED_DEMO_DATA=true
```

### 3. Install Dependencies & Run
```bash
cd backend
pip install -r requirements.txt
cd ..
python run.py
```
Open **`http://localhost:8000`** in your browser.

---

## 🧪 Testing

Execute the comprehensive automated test suite:

```bash
pytest backend/tests
```

```text
============================= test session starts =============================
collected 16 items

backend/tests/test_api.py ....                                           [ 25%]
backend/tests/test_auth.py .....                                         [ 56%]
backend/tests/test_profiles.py ...                                       [ 75%]
backend/tests/test_tracking.py ....                                      [100%]

======================== 16 passed in 4.47s ========================
```

---

## 🐳 Docker Deployment

Run the complete multi-container stack locally:

```bash
docker compose up --build -d
```
Access the application at `http://localhost:8000`.

---

## 🚀 Cloud Deployment (Render Blueprint)

The repository contains a declarative Infrastructure-as-Code file ([render.yaml](render.yaml)):

1. Link your GitHub repository in the [Render Dashboard](https://dashboard.render.com).
2. Select **New +** → **Blueprint**.
3. Point to this repository and set Blueprint Name to `skiniq-ai-planner`.
4. Provide your `MONGO_URI` variable when prompted.
5. Render automatically builds the Dockerfile, runs database indexes, and exposes the production service with automated SSL.
