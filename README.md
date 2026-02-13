
# 🩺 Medical Chatbot with RAG  
Production-Ready RAG System with AWS CI/CD Deployment

A **Retrieval-Augmented Generation (RAG)** chatbot for medical question answering, powered by **OpenAI GPT-5 nano** and built using **LangChain**.

The system implements a **hybrid retrieval pipeline (dense + sparse)** over a trusted medical knowledge base (*The Gale Encyclopedia of Medicine*), integrates **persistent conversational memory**, and is deployed to **AWS using a fully automated CI/CD pipeline with GitHub Actions**.

This project demonstrates how to architect, containerize, deploy, and scale a real-world LLM-powered medical system.

---

# ⚠️ Medical Disclaimer

> **IMPORTANT:** This chatbot is for educational and informational purposes only.  
> It is NOT a substitute for professional medical advice, diagnosis, or treatment.

Always consult a licensed healthcare professional for medical concerns.

---

# ✨ Key Features

## 🚀 Efficient LLM
- Powered by **OpenAI GPT-5 nano**
- Optimized for concise, cost-effective responses

## 🧠 Hybrid Retrieval (Dense + Sparse)
- Dense embeddings: `text-embedding-3-large`
- Sparse retrieval: `pinecone-sparse-english-v0`
- Tunable hybrid scoring using `alpha`

## 📚 Trusted Knowledge Base
- Built from *The Gale Encyclopedia of Medicine*

## 🧩 Domain-Aware Chunking
- `RecursiveCharacterTextSplitter`
- Medical-aware chunk segmentation

## 🔍 Scalable Vector Search
- **Pinecone** vector database
- Efficient semantic + keyword retrieval

## 🧠 Smart Ingestion & Fingerprinting
- SHA-256 pipeline fingerprinting
- `rag_state.yaml` prevents unnecessary reprocessing
- Embeddings recomputed only if configuration changes

## 💬 Persistent Conversational Memory
- Session-based memory
- PostgreSQL-backed chat history
- Survives container restarts
- Accessible via `/rag/chathistory`

## 🔗 API-Driven RAG System
- `/rag/vectorstore` → embed & upsert documents
- `/rag/chat` → full RAG pipeline
- `/rag/chathistory` → retrieve conversation history

## 🖥️ Interactive UI
- Clean **Gradio** interface
- Multi-turn context-aware responses

---

# 🏗️ System Architecture

```

User Query
↓
Gradio Interface
↓
FastAPI (/rag/chat)
↓
LangChain Orchestrator
↓
Hybrid Retriever (Dense + Sparse)
↓
Pinecone Vector Database
↓
Context Assembly
↓
OpenAI GPT-5 nano
↓
Response
↓
Persist to PostgreSQL
```


---

# 🔧 Tech Stack

| Component | Technology |
|-----------|------------|
| LLM | OpenAI GPT-5 nano |
| Framework | LangChain |
| Vector DB | Pinecone |
| API | FastAPI |
| UI | Gradio |
| Database | PostgreSQL (Docker / AWS RDS) |
| Cloud | AWS (EC2, ECR, RDS) |
| CI/CD | GitHub Actions |
| Language | Python |

---

# 🐳 Local Development (Docker)

## Prerequisites

- Docker Desktop
- OpenAI API key
- Pinecone API key

---

## 1️⃣ Clone Repository

```bash
git clone https://github.com/jihangh/RAG-based-Medical-Chatbot.git
cd RAG-based-Medical-Chatbot
````



## 2️⃣ Configure System

Edit:

```yaml
config.yaml
```

Set:

```yaml
index_name: your_index_name
name_space: your_namespace
```

Optional: adjust chunk size, alpha score, and model settings.

---

## 3️⃣ Customize System Prompt

Edit:

```
system_prompt.txt
```

---

# ☁️ AWS CI/CD Deployment (Production)

This project includes automated cloud deployment using:

* AWS EC2
* AWS ECR
* AWS RDS (PostgreSQL)
* GitHub Actions (Self-hosted runner)

---

## 1️⃣ IAM Setup

Create IAM user with:

* `AmazonEC2ContainerRegistryFullAccess`
* `AmazonEC2FullAccess`
* `AmazonRDSFullAccess`

---

## 2️⃣ Create ECR Repository

Create a repository in ECR.

Save the repository URI:

```
<account-id>.dkr.ecr.<region>.amazonaws.com/<reponame>
```

---

## 3️⃣ Launch EC2 (Ubuntu)

Configure **Inbound Rules**:

| Port | Purpose               |
| ---- | --------------------- |
| 22   | SSH                   |
| 8888 | FastAPI / UI          |
| 5432 | PostgreSQL (from RDS) |

Install Docker:

```bash
sudo apt-get update -y
sudo apt-get upgrade -y

curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

sudo usermod -aG docker ubuntu
newgrp docker
```

---

## 4️⃣ Configure Self-Hosted Runner

Repository →
`Settings → Actions → Runners → New self-hosted runner`

Run setup commands on EC2.

Use runner name:

```
self-hosted
```

---

## 5️⃣ AWS RDS Setup (PostgreSQL)

### Create Database

AWS Console → RDS → Create Database

* Engine: PostgreSQL
* Easy create
* DB identifier: `database-rag`
* Username: `postgres`
* Password: yourpassword

---

### Configure Security

RDS → Connectivity & Security → Security Group → Inbound Rules

Add:

* Type: PostgreSQL
* Port: 5432
* Source: EC2 security group

---

### Find DB_HOST

RDS → Databases → database-rag → Connectivity & Security

Under:

```
Endpoint & Port
```

Example:

```
database-rag.xxxxxx.region.rds.amazonaws.com
```

Use this as:

```
DB_HOST
```

---

### Create Database from EC2

```bash
psql -h <DB_HOST> -U postgres
CREATE DATABASE "database-rag";
```

Test connection:

```bash
psql -h <DB_HOST> -U postgres -d database-rag
```

Exit:

```
\q
```

---

## 6️⃣ GitHub Secrets

Add:

```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_ACCOUNT_ID
AWS_DEFAULT_REGION
ECR_REPO

OPENAI_API_KEY
PINECONE_API_KEY

DB_HOST
DB_NAME
DB_USER
DB_PASSWORD
```

---

## 7️⃣ Deploy

Push to main branch.

GitHub Actions will:

1. Build Docker image
2. Push to ECR
3. Pull image on EC2
4. Restart container

---

## 8️⃣ Access Application

Open EC2 security group → add:

* Custom TCP → Port 8888 → Anywhere

Then visit:

```
http://<EC2_PUBLIC_IP>:8888/docs
```

or

```
http://<EC2_PUBLIC_IP>:8888/ui
```

---

# ⚠️ Limitations

## Technical

* Limited to The Gale Encyclopedia of Medicine
* Not real-time clinical updates
* Retrieval quality depends on query clarity

## Ethical

* Not for emergency use
* Not for diagnosis or treatment decisions
* Human oversight required

---

# 🤝 Contributing

Contributions and improvements are welcome.
Feel free to fork and submit a PR.

```

# 🙏 Acknowledgements

This project is inspired by the work from the following repository:

🔗 Build a Complete Medical Chatbot with LLMs, LangChain, Pinecone, Flask & AWS
https://github.com/entbappy/Build-a-Complete-Medical-Chatbot-with-LLMs-LangChain-Pinecone-Flask-AWS

