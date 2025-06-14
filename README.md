# Invite App

A simple **FastAPI** + **SQLite** application that lets registered users invite others via email. Each successful invite grants the inviter credits. Built with modular routers, Jinja2 templates, and Bootstrap 5 for a clean, responsive UI.

## 🚀 Features

- ✅ User sign-up & login with email-based 2FA
- ✅ Invitation system with unique codes
- ✅ Invite validation endpoint
- ✅ Per-user credits tracking
- ✅ Session management via secure cookies
- ✅ Fully async frontend calls with Bootstrap spinners
- ✅ Modular FastAPI routers (auth, invite, user, views)
- ✅ SQLite for local dev (switch to Postgres/Docker easily)

## 🛠️ Tech Stack

- **Backend**: FastAPI, SQLAlchemy, SQLite
- **Frontend**: Bootstrap 5, Vanilla JS (async fetch + spinners)
- **Templates**: Jinja2
- **Auth**: OAuth2PasswordRequestForm + custom 2FA
- **Password hashing**: bcrypt via Passlib
- **Session store**: in-memory (demo)
- **Env vars**: `python-dotenv`

## 📂 Project Structure

```
├── app/
│ ├── api/
│ │ ├── auth.py
│ │ ├── invite.py
│ │ ├── user.py
│ │ └── deps.py
│ ├── db.py
│ ├── main.py
│ ├── models.py
│ ├── security.py
│ ├── seed.py
│ ├── templates/
│ │ ├── base.html
│ │ ├── landing.html
│ │ └── profile.html
│ └── static/
│ ├── css/
│ │ └── styles.css
│ └── js/
│ └── main.js
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## ⚙️ Setup & Installation

1. **Clone the repo**

   ```bash
   git clone https://github.com/yourusername/invite-app.git
   cd invite-app
   ```

2. **Create & activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate # macOS/Linux
   venv\Scripts\activate # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Copy & configure environment variables**

   ```bash
   cp .env.example .env

   # then edit .env with your settings (DB_URL, SMTP creds, etc.)
   ```

5. **Seed the database**

   ```bash
   python app/seed.py
   ```

## 🏃‍♂️ Running Locally

    ```bash
    uvicorn app.main:app --reload
    Open your browser at http://127.0.0.1:8000.
    ```

## 🐳 Docker & PostgreSQL (optional)

1. **Edit docker-compose.yml to enable Postgres service**

2. **Build & run**

   ```bash
   docker-compose up --build
   ```

   Env vars for Postgres are already mapped in .env.example.

## 🔐 Environment Variables

```dotenv
# Database
DATABASE_URL=sqlite:///./invite_app.db

# Or for Postgres:
# DATABASE_URL=postgresql://user:pass@db:5432/invite_db

# SMTP (for real email invites/2FA)
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USERNAME=your_email@example.com
MAIL_PASSWORD=your_smtp_password
MAIL_FROM=your_email@example.com
MAIL_STARTTLS=True
MAIL_SSL_TLS=False
```

## 🤝 Contributing

1. **Fork the repo**
2. **Create a feature branch (git checkout -b feat/awesome)**
3. **Commit your changes (git commit -m "feat: add awesome")**
4. **Push to your branch (git push origin feat/awesome)**

## 📄 License

This project is licensed under the MIT License.
