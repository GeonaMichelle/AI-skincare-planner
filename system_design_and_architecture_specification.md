# SkinIQ Platform: End-to-End System Engineering Specification

---

## 1. Ideation & Product Vision

### 1.1 Problem Statement
Modern skincare management is fragmented. Consumers face information overload, marketing hyperbole, and confusing ingredient lists (INCI), often leading to damaged skin barriers, mismatched product routines, and counter-productive ingredient interactions (e.g., mixing retinoids with high-concentration AHA/BHA). Furthermore, access to dermatologists is bottlenecked by cost and wait times, while esthetician consultations lack standardized tracking data.

### 1.2 Product Vision
**SkinIQ** is an intelligent, multi-persona skin intelligence platform that bridges the gap between daily consumer habits, esthetician consultations, and clinical dermatological care. By combining holistic habit tracking (hydration, sleep, lifestyle, environmental factors) with an algorithmic routine prescription engine and medical contraindication triage, SkinIQ delivers precision skincare recommendations with safety guardrails.

### 1.3 Target Personas
1. **Consumer**: Individuals seeking personalized skincare routines, daily habit accountability, and quantifiable skin progress tracking.
2. **Skincare Consultant (Esthetician)**: Licensed professionals managing client dossiers, reviewing lifestyle logs, and curating professional regimens.
3. **Dermatologist (MD)**: Medical practitioners performing triage, diagnostic severity grading (e.g., Acne vulgaris grading I-IV, Rosacea subtype staging), and prescribing clinical Rx topicals with automated contraindication detection.
4. **System Administrator**: Compliance officers monitoring INCI ingredient regulatory standards, system telemetry, and user RBAC permissions.

---

## 2. Feature Matrix

| Module | Feature | Target Role | Description |
| :--- | :--- | :--- | :--- |
| **Auth & Security** | JWT Authentication | All | Stateless bearer token authentication, secure password hashing via bcrypt, and RBAC enforcement. |
| **Profile** | Skin Profiling | Consumer | Fitzpatrick skin typing, barrier integrity analysis, sensitivity grading, and primary concerns. |
| **Habit Tracking** | 4-Pillar Daily Log | Consumer | Quantitative tracking of hydration (ml), sleep duration/quality, lifestyle stressors, and UV/humidity metrics. |
| **Routine Engine** | AI Routine Generator | Consumer | Context-aware AM/PM routine builder tailored to seasonal variations, skin type, and budget limits. |
| **Ingredients** | Contraindication Engine | Consumer / Derm | Real-time conflict detection (e.g., Retinol + Glycolic Acid, Benzoyl Peroxide + Vitamin C). |
| **Consultant Suite** | Client Dossier Studio | Consultant | Comprehensive client history timeline, regimen prescription editor, and professional notes. |
| **Dermatology** | Medical Triage & Rx | Dermatologist | Clinical severity grading, prescription titration, and active medical warnings. |
| **Analytics** | Progress & Adherence | Consumer / Derm | 30-day adherence index, skin health scoring (0-100), and historical comparison metrics. |
| **Reporting** | Multi-Format Export | Consumer / Consultant | Structured CSV and clinical TXT/PDF report generation for doctor visits. |
| **Administration** | RBAC & INCI Monitor | Administrator | User role escalation/de-escalation, system telemetry, and INCI database audit. |

---

## 3. Product Requirements Document (PRD)

### 3.1 User Stories & Acceptance Criteria

#### US-1: Consumer Intelligent Routine Generation
* **As a** consumer with sensitive combination skin,
* **I want** the system to generate an AM and PM routine matching my specific budget,
* **So that** I don't use incompatible actives or overspend.
* **Acceptance Criteria**:
  1. Routine generator must accept optional `max_budget` parameter.
  2. Products returned must strictly exclude known irritants for sensitive skin types.
  3. Routine must separate AM (protective/SPF focused) from PM (recovery/active focused).

#### US-2: Clinical Contraindication Detection
* **As a** dermatologist prescribing high-strength tretinoin,
* **I want** the system to alert me if the patient's existing routine contains conflicting exfoliants,
* **So that** I prevent chemical burns or severe barrier disruption.
* **Acceptance Criteria**:
  1. System checks pairwise ingredient conflict rules in real time.
  2. High-severity conflicts return immediate visual warning badges and 400 validation if unsafe.

#### US-3: Holistic Progress Scoring
* **As a** user logging daily hydration and sleep,
* **I want** my overall skin health score to dynamically adjust based on rolling 14-day data,
* **So that** I understand the lifestyle drivers behind my skin clarity.
* **Acceptance Criteria**:
  1. Score calculated between 0-100 based on weighted adherence, sleep, hydration, and assessment records.
  2. Score recalculated on every tracking log update.

### 3.2 Non-Functional Requirements (NFRs)
* **Performance**: API responses must resolve in $< 150\text{ ms}$ under normal load; static assets served with GZip compression.
* **Security**: OWASP Top 10 compliance; strict Content Security headers (`X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `HSTS`, `XSS Protection`).
* **Reliability**: Resilient database connector with automatic reconnection and fallback handling.
* **Scalability**: Stateless backend design permitting horizontal scaling across multiple container replicas.

---

## 4. System Architecture & Component Design

### 4.1 High-Level Architecture Diagram

```mermaid
graph TD
    Client[Browser / Client SPA] -->|HTTPS:8000| Nginx[Reverse Proxy / SSL]
    Nginx -->|Proxy Pass| Uvicorn[ASGI Server: Uvicorn]
    Uvicorn --> FastAPI[FastAPI Core Application]
    
    subgraph FastAPI Application Stack
        FastAPI --> MW[Middleware Pipeline: GZip, SecurityHeaders, CORS]
        MW --> Router[API Router /api/v1]
        MW --> Static[Static File Mount / & /css & /js]
        
        Router --> AuthRoute[/auth]
        Router --> ProfileRoute[/profiles]
        Router --> TrackRoute[/tracking]
        Router --> RoutineRoute[/routine]
        Router --> ProductRoute[/products]
        Router --> DermRoute[/dermatologist]
        Router --> AdminRoute[/users & /admin]
        
        AuthRoute --> AuthService[Auth Service]
        TrackRoute --> TrackingService[Tracking Service]
        RoutineRoute --> RoutineService[Routine & AI Service]
        ProductRoute --> ProductService[Product & INCI Service]
    end
    
    subgraph Data & Storage Tier
        AuthService --> MongoSession[DB Session Manager]
        TrackingService --> MongoSession
        RoutineService --> MongoSession
        ProductService --> MongoSession
        
        MongoSession -->|mongodb+srv| Atlas[(MongoDB Atlas Cloud Cluster)]
    end
```

### 4.2 Middleware Pipeline Execution Order
1. **CORS Middleware**: Evaluates origins (`BACKEND_CORS_ORIGINS`), methods, and headers.
2. **GZip Middleware**: Automatically compresses payloads $> 1,000$ bytes for high-throughput responses.
3. **Security Headers Middleware**: Injects `nosniff`, `DENY` for clickjacking protection, and `HSTS`.
4. **JWT Authentication Bearer**: Validates authorization header tokens, decoding `sub` claims and verifying user activity status.
5. **RBAC Role Dependency**: Guards administrative, dermatologist, and consultant endpoints with strict role barriers.

---

## 5. Database Design (MongoDB Atlas)

### 5.1 Collection Schema & Data Dictionary

#### 1. `users`
* `id` *(Integer, Unique Index)*: Auto-incremented user ID.
* `email` *(String, Unique Index)*: Primary account email address.
* `hashed_password` *(String)*: Bcrypt-hashed password.
* `full_name` *(String)*: User display name.
* `role` *(String)*: `USER`, `SKINCARE_CONSULTANT`, `DERMATOLOGIST`, `ADMINISTRATOR`.
* `is_active` *(Boolean)*: Account status flag.
* `created_at` *(DateTime)*: Account creation timestamp.

#### 2. `skin_profiles`
* `id` *(Integer, Unique Index)*: Profile record ID.
* `user_id` *(Integer, Unique Index)*: Foreign key reference to `users.id`.
* `skin_type` *(String)*: `OILY`, `DRY`, `COMBINATION`, `NORMAL`, `SENSITIVE`.
* `concerns` *(Array of Strings)*: e.g. `["Acne", "Hyperpigmentation", "Barrier Damage"]`.
* `sensitivity_level` *(Integer)*: 1 (Resilient) to 5 (Extremely Reactive).
* `barrier_status` *(String)*: `HEALTHY`, `COMPROMISED`, `CRITICAL`.
* `updated_at` *(DateTime)*: Last modification timestamp.

#### 3. `tracking_*` Collections (`sleep_logs`, `hydration_logs`, `lifestyle_logs`, `environment_logs`)
* **Compound Unique Index**: `(user_id: 1, log_date: 1)` — Guarantees exactly one log entry per user per day.
* `user_id` *(Integer)*: Reference to user.
* `log_date` *(String YYYY-MM-DD)*: Target tracking date.
* *Specific metrics*: `hours_slept`, `water_amount_ml`, `uv_index_max`, `stress_level`, etc.

#### 4. `skincare_routines`
* `id` *(Integer, Unique Index)*: Routine ID.
* `user_id` *(Integer)*: Reference to user.
* `season` *(String)*: `SUMMER`, `WINTER`, `SPRING`, `FALL`.
* `morning_steps` *(Array of Step Objects)*: Step number, product category, active ingredients.
* `evening_steps` *(Array of Step Objects)*: Recovery steps, treatments, barrier creams.
* `created_at` *(DateTime)*: Generation timestamp.

---

## 6. API Design & Endpoint Contracts

All routes prefixed under `/api/v1`:

| Method | Endpoint | Access Level | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/auth/login` | Public | Authenticates credentials and returns JWT bearer token. |
| `POST` | `/auth/register` | Public | Registers a new account with email validation. |
| `GET` | `/auth/me` | Authenticated | Retrieves current authenticated user profile and role. |
| `GET` | `/profiles/me` | Authenticated | Retrieves current user's skin profile. |
| `POST` | `/profiles/me` | Authenticated | Creates or updates current user's skin profile. |
| `POST` | `/tracking/hydration` | Authenticated | Logs daily water consumption with target comparison. |
| `POST` | `/tracking/sleep` | Authenticated | Logs sleep duration and sleep quality grade. |
| `GET` | `/routine/latest` | Authenticated | Fetches latest active AM/PM routine. |
| `POST` | `/routine/generate` | Authenticated | Triggers AI routine generation based on latest profile. |
| `GET` | `/products/recommendations` | Authenticated | Returns budget-filtered, skin-type compatible products. |
| `POST` | `/products/compare` | Authenticated | Performs pairwise ingredient contraindication analysis. |
| `GET` | `/consultant/clients` | Consultant / Admin | Lists client queue with profile summaries. |
| `POST` | `/consultant/clients/{id}/prescribe` | Consultant / Admin | Issues custom professional product prescription. |
| `GET` | `/dashboard/dermatologist` | Dermatologist / Admin | Clinical triage queue and patient condition statistics. |
| `GET` | `/dashboard/admin` | Admin | Telemetry, error rates, and user RBAC overview. |
| `GET` | `/api/health` | Public | System health status and version identifier. |

---

## 7. Development & Structural Refactoring Plan

### 7.1 Identified Structural Deficiencies
1. **Root Directory Clutter**: Legacy milestone implementation scripts (`implement_features.py`, `implement_features_v2.py`, `implement_milestone4.py`) residing in root.
2. **Fragmented Test Scripts**: Standalone test runners (`e2e_test.py`, `edge_case_tester.py`, `test_api.py`) floating outside the test suite.
3. **Redundant Requirements Files**: Discrepancies between root `requirements.txt` and `backend/requirements.txt`.
4. **Duplicate Inner Workspace**: An unlinked historical directory (`AI skincare planner`) causing confusion.

### 7.2 Resolution Architecture
```
AI skincare planner V1/
├── backend/
│   ├── app/
│   │   ├── api/v1/          # Modular API routers
│   │   ├── core/            # Config, security, logging, dependencies
│   │   ├── db/              # Session management, indexes, seeding
│   │   ├── models/          # Data models & Enums
│   │   ├── schemas/         # Pydantic request/response schemas
│   │   └── services/        # Business logic & AI algorithms
│   ├── tests/               # Consolidated test suite (Unit, Integration, E2E)
│   └── requirements.txt     # Single source of truth dependencies
├── frontend/                # Glassmorphism SPA (HTML, CSS, JS)
├── scripts/
│   └── archive/             # Archived milestone migration utilities
├── .env                     # Local environment configuration
├── Dockerfile               # Production container definition
├── docker-compose.yml       # Cloud/Local container orchestration
├── render.yaml              # Cloud infrastructure blueprint
└── run.py                   # Production ASGI application launcher
```

---

## 8. Verification & Deployment Runbook

1. **Local Test Execution**: `pytest backend/tests/` verifies all unit and integration contracts.
2. **Database Verification**: Live MongoDB Atlas connection verified (`skiniq_prod_db`).
3. **Container Build**: `docker build -t skiniq-platform .` builds cleanly.
4. **Cloud Launch**: Render pulls Dockerfile and launches service with zero-downtime healthcheck verification.
