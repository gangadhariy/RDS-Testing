# AWS RDS MySQL Testing Dashboard

A professional Flask + AWS RDS MySQL dashboard application with:

- Beautiful animated UI
- AWS RDS Information page
- Create Users
- Update Users
- Delete Users
- Search Users live
- Validation Rules
- Popup Notifications
- Gunicorn Production Server
- Nginx Reverse Proxy
- Hosted on AWS EC2

---

# Project Architecture

```plaintext
Browser
   ↓
Nginx (Port 80)
   ↓
Gunicorn (127.0.0.1:5000)
   ↓
Flask App
   ↓
AWS RDS MySQL
```

---

# AWS Requirements

Create:

- **EC2 Ubuntu instance**
- **RDS MySQL instance**

RDS Settings:

- Publicly Accessible → YES
- Port → 3306

Security Group inbound rule:

```plaintext
MYSQL/Aurora
TCP
3306
YOUR_EC2_PRIVATE_IP/32
```

or

```plaintext
0.0.0.0/0
```

(for testing only)

---

# Connect to EC2

```bash
ssh -i "your-key.pem" ubuntu@YOUR_PUBLIC_IP
```

---

# Update Ubuntu

```bash
sudo apt update
sudo apt upgrade -y
```

---

# Install Python + Tools

```bash
sudo apt install python3 python3-pip python3-venv nginx -y
```

Check:

```bash
python3 --version
pip3 --version
nginx -v
```

---

# Create Project Folder

```bash
mkdir -p ~/RDS/RDS-Testing
cd ~/RDS/RDS-Testing
```

---

# Create Virtual Environment

```bash
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

You should see:

```bash
(venv)
```

---

# Install Python Packages

```bash
pip install flask pymysql gunicorn
```

Freeze requirements:

```bash
pip freeze > requirements.txt
```

---

# Project Structure

```plaintext
RDS-Testing/
 ├── app.py
 ├── requirements.txt
 ├── README.md
 ├── templates/
 │     └── index.html
 └── venv/
```

Create templates:

```bash
mkdir templates
```

---

# Add Application Files

Create:

```bash
nano app.py
```

Paste app.py code.

Save:

```plaintext
CTRL + X
Y
ENTER
```

Create HTML:

```bash
nano templates/index.html
```

Paste HTML code.

Save:

```plaintext
CTRL + X
Y
ENTER
```

---

# Configure Environment Variables

Replace with your RDS values:

```bash
export DB_HOST="your-rds-endpoint"
export DB_USER="admin"
export DB_PASSWORD="yourpassword"
export DB_NAME="mysqldb"
```

Verify:

```bash
echo $DB_HOST
```

---

# Run Flask Test

```bash
python3 app.py
```

Open:

```plaintext
http://EC2_PUBLIC_IP:5000
```

If working → stop:

```bash
CTRL+C
```

---

# Run Gunicorn

```bash
gunicorn -w 4 -b 127.0.0.1:5000 app:app
```

If successful:

```plaintext
Listening at: http://127.0.0.1:5000
```

Stop:

```bash
CTRL+C
```

---

# Configure Nginx

Edit config:

```bash
sudo nano /etc/nginx/sites-available/default
```

Replace with:

```nginx
server {
    listen 80;

    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5000;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Save.

---

# Test Nginx Config

```bash
sudo nginx -t
```

Expected:

```plaintext
syntax is ok
test is successful
```

---

# Restart Nginx

```bash
sudo systemctl restart nginx
sudo systemctl enable nginx
```

Check:

```bash
sudo systemctl status nginx
```

Should show:

```plaintext
active (running)
```

---

# Start Gunicorn

Activate venv:

```bash
source venv/bin/activate
```

Run:

```bash
gunicorn -w 4 -b 127.0.0.1:5000 app:app
```

---

# Access App

Open browser:

```plaintext
http://YOUR_EC2_PUBLIC_IP
```

You should see:

AWS RDS Dashboard

with:

- RDS Info tab
- Manage Users
- Search Users

---

# Common Errors

---

## gunicorn not found

Activate venv:

```bash
source venv/bin/activate
```

---

## Port already in use

Kill old process:

```bash
pkill gunicorn
```

Restart:

```bash
gunicorn -w 4 -b 127.0.0.1:5000 app:app
```

---

## RDS Timeout

Check:

- RDS public access enabled
- Security group allows 3306
- Correct endpoint

---

## Connection refused

Check exports:

```bash
echo $DB_HOST
echo $DB_USER
echo $DB_PASSWORD
echo $DB_NAME
```

---

# Features

## Create User

Validates:

- No blank fields
- Name letters only
- Country letters only
- Age numeric
- Age 1–120

---

## Update User

Click Update on card.

Edit values.

Save.

---

## Delete User

Deletes immediately with popup.

---

## Search User

Live search while typing.

Shows matching users instantly.

---

# Production Stop

Stop Gunicorn:

```bash
pkill gunicorn
```

---

# Production Start Again

```bash
cd ~/RDS/RDS-Testing
source venv/bin/activate

export DB_HOST="..."
export DB_USER="..."
export DB_PASSWORD="..."
export DB_NAME="..."

gunicorn -w 4 -b 127.0.0.1:5000 app:app
```

---

# Built With

- Python
- Flask
- PyMySQL
- Gunicorn
- Nginx
- AWS EC2
- AWS RDS MySQL
- HTML/CSS/JS

---

# Final Result

A fully production-style cloud dashboard demonstrating:

- AWS RDS Connectivity
- Flask Backend APIs
- MySQL CRUD
- Reverse Proxying
- Production Hosting
- Professional Animated Frontend
