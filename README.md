# 🤖 ASHA Sahayi – AI-Powered Telegram Assistant for ASHA Workers

ASHA Sahayi is a **Telegram-based assistant** designed to support **ASHA (Accredited Social Health Activist) workers** by providing **safe medical guidance**, **patient visit logging**, **multilingual support**, **AI-assisted decision support**, and **basic admin monitoring**, while strictly following **ethical AI and data privacy principles**.

---


# Ethical AI Statement – ASHA Sahayi

- ASHA Sahayi functions only as a **decision-support tool** and does not replace qualified medical professionals.

- The AI provides **general health guidance** and consistently recommends referral to **Primary Health Centres (PHCs)** for serious or unclear cases.

- The system **does not provide medical diagnoses or prescribe medications**.

- Only **minimal, non-sensitive data** is collected for patient visit logging; **no personally identifiable patient information** is stored.

- All data is stored securely in a **managed database** with restricted access and **no third-party data sharing**.

- **Multilingual support** ensures inclusive access while maintaining consistent and responsible medical guidance.

- **AI interactions are logged** for transparency and system improvement, without compromising user privacy.

- **Human oversight** and ethical AI principles such as **safety, accountability, and transparency** are strictly followed.


---

## 🎯 Problem Statement

ASHA workers work in field conditions where:
- Quick access to reliable medical guidance is limited
- Patient visit records are often maintained manually
- Language barriers exist
- Digital tools must be simple, lightweight, and mobile-friendly

**ASHA Sahayi** addresses these challenges using a conversational Telegram bot.

---

## ✨ Key Features

### 👩‍⚕️ ASHA Worker Authentication
- Built-in authentication inside the bot
- ASHA ID + mobile number verification
- No passwords or Aadhaar required
- Verification stored securely in database

### 🌐 Multilingual Support
- English
- Hindi
- Tamil
- Malayalam
- Language preference stored permanently in MySQL

### 🩺 Medical Guidance (Ethical & Safe)
- Rule-based medical guidance
- AI-assisted responses (maximum **5 short lines**)
- No diagnosis
- No medicine prescription
- Referral-first approach (PHC)

### 📝 Patient Visit Logging
- Step-by-step visit form inside Telegram
- Logs:
  - Patient age
  - Symptoms
  - Visit category
  - Action taken
- Stored securely in MySQL

### 🤖 Generative AI Integration
- Uses **Google Gemini (google-genai SDK)**
- AI responses are:
  - Short and field-friendly
  - Non-diagnostic
  - Auditable
- AI usage metadata logged (no patient identity)

### 🛠 Admin Dashboard (Inside Telegram)
- Admin access using Telegram ID
- View registered ASHA workers
- View recent patient visits
- No patient identity exposure

---

## 🧱 Tech Stack

| Component | Technology |
|--------|-----------|
| Bot Platform | Telegram |
| Backend | Python |
| Database | MySQL |
| AI Model | Google Gemini (GenAI SDK) |
| Deployment | Railway / Cloud |
| Authentication | Telegram ID + ASHA ID |

---

## 📁 Project File Structure

```text
asha-sahayi/
│
├── bot.py
│   ├─ Main Telegram bot logic
│   ├─ Authentication, menus, AI, logging, admin dashboard
│
├── db.py
│   ├─ MySQL database connection and queries
│   ├─ ASHA verification, visit logging, AI audit logs
│
├── ai.py
│   ├─ Google Gemini integration
│   ├─ Ethical AI enforcement (max 5 lines)
│
├── texts.py
│   ├─ Multilingual UI messages
│   ├─ Rule-based medical guidance text
│
├── db.sql
│   ├─ Complete MySQL schema
│
├── requirements.txt
│   ├─ Python dependencies (pinned versions)
│
├── .env
│   ├─ Environment variables (not committed)
│
├── .gitignore
│
├── ethics.md
│   ├─ Ethical AI & data privacy statement
│
└── README.md


