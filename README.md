# ⚡ TerraMake

> **AI-powered DevOps assistant for generating, reviewing, and improving Terraform infrastructure using a feedback-driven learning loop.**

---

## Overview

TerraMake is designed to bridge the gap between **infrastructure generation** and **infrastructure intelligence**.

Instead of just creating Terraform code, TerraMake:

* Understands your infrastructure
* Reviews it for best practices
* Suggests improvements
* Learns from your feedback over time

---

## Features

### Infrastructure Generation

* Generate Terraform configurations from structured JSON input

### AI-Powered Review

* Analyze infrastructure for:

  * Security issues
  * Missing configurations
  * Best practice violations

### Smart Suggestions

* Provides actionable Terraform fixes
* Outputs ready-to-use code snippets

### Feedback System

* Accept or reject suggestions
* Fine-grained feedback per suggestion

### Feedback Analytics

* Track:

  * Acceptance rate
  * Suggestion quality

### Adaptive Learning Loop

* Improves future suggestions using past feedback (MLOps-style loop)

---

## How It Works

```
Input → Generate → Review → Suggest → Feedback → Learn
```

1. User provides infrastructure input (JSON)
2. Terraform is generated
3. AI reviews generated infra
4. Suggestions are created
5. User gives feedback
6. System adapts future outputs

---

## Architecture

```
CLI
 │
 ▼
Generator ──▶ AI Engine (Groq)
 │               │
 ▼               ▼
Terraform     Suggestions
 │               │
 ▼               ▼
Feedback Logger ──▶ Analyzer ──▶ Adaptive Prompt System
```

---

## Installation

```bash
git clone <your-repo-url>
cd terramake
pip install -r requirements.txt
```

---

## Usage

### 1. Generate Terraform

```bash
python main.py generate data/sample_input.json
```

### 2. Review Infrastructure

```bash
python main.py review data/sample_input.json
```

### 3. Get Suggestions

```bash
python main.py suggest data/sample_input.json
```

### 4. Give Feedback (Single Suggestion)

```bash
python main.py feedback data/sample_input.json <index> <accept/reject>
```

Example:

```bash
python main.py feedback data/sample_input.json 0 accept
```

### 5. Bulk Feedback

```bash
python main.py feedback-all data/sample_input.json accept
```

### 6. View Feedback Stats

```bash
python main.py stats
```

### 7. Run Full Demo

```bash
python main.py demo data/sample_input.json
```

---

## 🧩 Example

### Input (JSON)

```json
{
  "s3": {
    "bucket_name": "my-bucket"
  }
}
```

### Output (AI Suggestion)

```
Problem: Missing encryption

Fix:
Add:

resource "aws_s3_bucket_server_side_encryption_configuration" ...
```

---

## Feedback Loop (Core Idea)

TerraMake improves over time:

* Accepted suggestions → Reinforced
* Rejected suggestions → Avoided
* Patterns → Used to refine prompts

This creates a **self-improving DevOps assistant**.

---

## Future Roadmap

* AWS integration using `boto3`
* Smarter Terraform patching (auto-editing code)
* Multi-resource & multi-cloud support
* CI/CD pipeline integration (GitHub Actions, Jenkins)
* Model fine-tuning for infra-specific intelligence

---

## 💥 Why TerraMake?

> TerraMake doesn’t just generate infrastructure — it **learns how to improve it**.

---

## 🛠️ Tech Stack

* Python
* Terraform
* Groq API (LLM inference)
* CLI-based workflow

---

## 👨‍💻 Author

**Arjun Kapoor**

* Building intelligent infrastructure tools

---

## ⭐ Contributing

Contributions are welcome!

1. Fork the repo
2. Create a new branch
3. Make your changes
4. Submit a PR

---

## 📜 License

MIT License

---
