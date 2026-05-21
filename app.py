from flask import Flask, render_template, request, jsonify
import pymysql
import os
import re

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

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
        CREATE TABLE IF NOT EXISTS users(
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            age INT,
            country VARCHAR(100)
        )
        """)
    connection.commit()


create_table()


def validate(data):
    name = data["name"].strip()
    age = str(data["age"]).strip()
    country = data["country"].strip()

    if not name or not country or not age:
        return "Fields cannot be blank"

    if not re.match(r'^[A-Za-z ]+$', name):
        return "Name must contain letters only"

    if not age.isdigit():
        return "Age must be numeric"

    if int(age) < 1 or int(age) > 120:
        return "Invalid age"

    if not re.match(r'^[A-Za-z ]+$', country):
        return "Country must contain letters only"

    return None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/save", methods=["POST"])
def save():
    data = request.json
    err = validate(data)
    if err:
        return jsonify({"error": err}), 400

    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO users(name,age,country) VALUES(%s,%s,%s)",
            (data["name"], data["age"], data["country"])
        )
    connection.commit()

    return jsonify({"message": "User Created Successfully 🚀"})


@app.route("/users")
def users():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users ORDER BY id DESC")
        return jsonify(cursor.fetchall())


@app.route("/update/<int:id>", methods=["PUT"])
def update(id):
    data = request.json
    err = validate(data)
    if err:
        return jsonify({"error": err}), 400

    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE users
            SET name=%s, age=%s, country=%s
            WHERE id=%s
        """, (data["name"], data["age"], data["country"], id))
    connection.commit()

    return jsonify({"message": "User Updated Successfully ✨"})


@app.route("/delete/<int:id>", methods=["DELETE"])
def delete(id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM users WHERE id=%s", (id,))
    connection.commit()

    return jsonify({"message": "Deleted Successfully 🗑️"})


@app.route("/search/<name>")
def search(name):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM users WHERE name LIKE %s",
            (f"%{name}%",)
        )
        return jsonify(cursor.fetchall())


if __name__ == "__main__":
    app.run(debug=True)
