# SecureShare Production & Local Deployment Guide

## 1. Prerequisites
- **Local Native Run**:
  - Python 3.11+
  - Node.js 18+ & npm 9+
- **Containerized Run**:
  - Docker Desktop 24+ & Docker Compose v2+
- **Kubernetes Production Run**:
  - Kubernetes cluster 1.28+ (e.g. Minikube, Kind, GKE, EKS)
  - `kubectl` configured with cluster admin rights

---

## 2. Quick Local Native Run (Zero Docker Required)

The project includes pre-configured launcher scripts:

```cmd
:: 1. Launch complete stack (Backend + Frontend + Seed Data)
START_DEMO.bat

:: 2. Access the Application:
:: Frontend UI: http://localhost:5173
:: Live Presentation Demo: http://localhost:5173/demo
:: Swagger API Docs: http://localhost:8000/docs
:: Admin Portal: http://localhost:5173/admin

:: 3. Stop the running demo servers:
STOP_DEMO.bat

:: 4. Reset the database to pristine state:
RESET_DEMO.bat
```

---

## 3. Docker Compose Multi-Container Deployment

To deploy the production-hardened multi-service stack with PostgreSQL, ClamAV, Backend, and Frontend:

```bash
# 1. Copy environment template
cp .env.example .env

# 2. Build and launch all 4 services
docker compose up -d --build

# 3. View running container status
docker compose ps

# 4. View backend logs
docker compose logs -f backend
```

---

## 4. Kubernetes (K8s) Production Deployment

Deploy to a Kubernetes cluster using the hardened manifests in `k8s/`:

```bash
# 1. Create the dedicated restricted namespace
kubectl apply -f k8s/namespace.yaml

# 2. Deploy ConfigMap and Secrets
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.example.yaml

# 3. Apply Zero-Trust Network Policies
kubectl apply -f k8s/network-policy.yaml

# 4. Deploy Databases and Services
kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/clamav-deployment.yaml

# 5. Deploy Application Microservices
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/frontend-deployment.yaml

# 6. Apply Ingress and Autoscalers
kubectl apply -f k8s/ingress.yaml
kubectl apply -f k8s/hpa.yaml

# 7. Verify All Pods are Running
kubectl get pods -n secureshare
```

---

## 5. Pre-Seeded Demo User Accounts

| Persona Name | Email Address | Password | Role | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Sushmitha Reddy** | `sushmitha@example.com` | `Pass123!Secure` | `USER` | Product Owner & Security Lead |
| **Rahul Kumar** | `rahul@example.com` | `Pass123!Secure` | `USER` | Cryptography & Backend Engineer |
| **Priya Sharma** | `priya@example.com` | `Pass123!Secure` | `USER` | DevSecOps & QA Lead |
| **Arjun Rao** | `arjun@example.com` | `Pass123!Secure` | `USER` | UI/UX & Frontend Engineer |
| **System Admin** | `admin@example.com` | `Pass123!Secure` | `ADMIN` | SOC Operations & Quarantine Admin |
| **Security Auditor**| `auditor@example.com` | `Pass123!Secure` | `SECURITY_AUDITOR` | Compliance Officer & Ledger Auditor |
