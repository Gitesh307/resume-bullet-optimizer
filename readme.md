# AI-Powered Resume Bullet Optimizer

A full-stack NLP application that analyzes a resume bullet against a job description and intelligently rewrites the bullet using **open-source NLP techniques**.

Built in **one day** using **React**, **Django REST Framework**, **spaCy**, **TF-IDF**, and **cosine similarity** — no paid APIs, no LLMs, no trials.

---

## 🚀 Features

- Input a resume bullet and a job description
- Extracts relevant keywords from the job description using NLP
- Measures semantic similarity using TF-IDF + cosine similarity
- Identifies matched and missing keywords
- Rewrites the resume bullet using:
  - POS tagging
  - verb strengthening
  - keyword-guided augmentation (no keyword stuffing)
- Fully deployable on Render free tier

---

## 🧠 NLP / AI Techniques Used

This project uses **real NLP**, not string replacement.

- **spaCy**
  - Tokenization
  - Lemmatization
  - POS tagging
  - Noun-chunk extraction
- **scikit-learn**
  - TF-IDF vectorization
  - Cosine similarity scoring
- **Rule-based NLP logic**
  - Weak → strong verb transformation
  - Keyword gap analysis
  - Controlled bullet rewriting

No OpenAI, no GPT, no paid services.

---

## 🏗️ Architecture

resume-bullet-optimizer/
├── backend/ # Django + DRF API
│ ├── optimizer/ # NLP logic + API views
│ ├── config/ # Django settings
│ ├── build.sh # Render build script
│ └── requirements.txt
├── frontend/ # React (Vite)
│ ├── src/
│ └── dist/ # Production build (Render)
└── README.md


### Flow
1. React UI collects user input
2. POST request sent to Django REST API
3. Backend runs NLP pipeline
4. Optimized bullet + metrics returned to frontend

---

## 🛠️ Tech Stack

### Frontend
- React (Vite)
- Fetch API
- CSS (no UI framework)

### Backend
- Python
- Django
- Django REST Framework
- spaCy
- scikit-learn
- Gunicorn

### Deployment
- Render (free tier)
  - Python Web Service (backend)
  - Static Site (frontend)

---

## ⚙️ Local Setup

### Backend
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python manage.py migrate
python manage.py runserver

### Backend
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python manage.py migrate
python manage.py runserver
