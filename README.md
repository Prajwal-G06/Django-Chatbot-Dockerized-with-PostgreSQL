# 🤖 Django Chatbot — Dockerized with PostgreSQL

A containerized Django chatbot that uses PostgreSQL for storing conversation history. Powered by OpenAI GPT models and enhanced with Whitenoise for static file serving—ready for deployment.

---

## ✨ Features

- 🧠 Intelligent chatbot powered by **OpenAI GPT models**  
- 💾 Persistent chat history stored in **PostgreSQL**  
- 🐳 Fully containerized with **Docker & Docker Compose**  
- ⚡ **Gunicorn** + **Whitenoise** for production-ready serving  
- 🔑 Easy configuration with environment variables  

---

## 🚀 Getting Started

### ✅ Prerequisites
Make sure you have installed:
- [Docker & Docker Compose](https://docs.docker.com/)

---

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/django-chatbot-docker.git
   cd django-chatbot-docker

2. **Run with Docker Compose**
   ```bash
   docker-compose up --build -d

3. **Access the Database**
   To connect to the Postgres DB:
   ```bash
   docker compose exec db psql -U chatbot_user -d chatbot_db

   \dt; -- List tables
   SELECT * FROM chatbot_app_conversationhistory;

## 🌍 Access the app here
[Visit the live site here](http://ec2-13-201-77-129.ap-south-1.compute.amazonaws.com:8000/)

