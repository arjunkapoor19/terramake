## 🚀 TerraMake — Scope & Features

### 📦 Supported Resources (MVP)

* **S3** — basic configuration
* **CloudFront** — basic configuration

---

### ⚙️ Features (MVP)

* **Generate Terraform from JSON**
  Convert structured input into clean, minimal Terraform code (using heurisitics)

* **CLI Interface**
  Simple command-line workflow for generating and validating infrastructure

* **AI Validation (planned)**
  Intelligent suggestions to improve Terraform configurations and using AI as a validation layer to help users make better informed decisions

* **Feedback Logging (planned)**
  Capture user decisions to build a learning dataset

---

### 🔮 Post-MVP Plans

* **AWS API Integration**
  Automatically fetch infrastructure using AWS APIs (e.g., boto3)

* **Full Terraform Coverage**
  Expand support beyond S3 and CloudFront to additional AWS services

---

### 🧠 Core Focus

Make an easy to use AWS to terraform code CLI tool. Initially the tool uses heuristics rules to convert AWS configurations to terraform code, further an AI layer validates the code detecting any drift and advising the user on possible and best corrective measures. The tool also logs user responses to feed to its ML model in order to train it to give better suggestions going forward.
