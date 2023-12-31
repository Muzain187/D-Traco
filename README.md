# DataInvestigo-BE

Brief project description.

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/MateehUllah/BotBlogR-BE.git
cd BotBlogR
```
## 2. Set up Virtual Environment

### On Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### On MacOs/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```
## 4. Configure Environment Variables

Create a .env file in the root directory and set the necessary environment variables:

```
SECRET_KEY=your_secret_key
ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30

DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=your_db_port
# PostgreSQL database configuration
DATABASE_URL=postgresql://your_db_user:your_db_password@your_db_host:your_db_port/your_db_name

# CORS configuration
FRONTEND_ORIGIN=http://your_frontend_url  # Replace with your actual frontend's URL

# Mail configuration
MAIL_USERNAME=your_mail_username
MAIL_PASSWORD=your_mail_password
MAIL_FROM=your_email@example.com
MAIL_PORT=587
MAIL_SERVER=smtp.example.com

```
## 5. Run the Application

```bash
python main.py
```
### Visit http://localhost:8000/ in your browser.

