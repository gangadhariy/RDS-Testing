from flask import Flask, render_template, request, jsonify
import pymysql
import os

app = Flask(__name__)

# ==========================
# AWS RDS MySQL CONFIG
# ==========================
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# ==========================
# CONNECT TO MYSQL
# ==========================
connection = pymysql.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    cursorclass=pymysql.cursors.DictCursor
)


def create_table():
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                age INT,
                country VARCHAR(100)
            )
        """)
    connection.commit()


create_table()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/save", methods=["POST"])
def save():
    data = request.json
    name = data["name"]
    age = data["age"]
    country = data["country"]

    with connection.cursor() as cursor:
        sql = "INSERT INTO users (name, age, country) VALUES (%s, %s, %s)"
        cursor.execute(sql, (name, age, country))

    connection.commit()

    return jsonify({"message": "Saved successfully to AWS RDS 🚀"})


if __name__ == "__main__":
    app.run(debug=True)