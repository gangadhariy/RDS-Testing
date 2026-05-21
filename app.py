from flask import Flask, render_template, request, jsonify
import pymysql
import os

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")


def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )


def create_table():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                age INT,
                country VARCHAR(100)
            )
        """)
    conn.commit()
    conn.close()


create_table()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/users", methods=["GET"])
def users():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users")
        data = cursor.fetchall()
    conn.close()
    return jsonify(data)


@app.route("/save", methods=["POST"])
def save():
    data = request.json
    conn = get_connection()

    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO users (name, age, country) VALUES (%s,%s,%s)",
            (data["name"], data["age"], data["country"])
        )

    conn.commit()
    conn.close()

    return jsonify({"message": "User Created Successfully 🚀"})


@app.route("/update/<int:id>", methods=["PUT"])
def update(id):
    data = request.json
    conn = get_connection()

    with conn.cursor() as cursor:
        cursor.execute(
            "UPDATE users SET name=%s, age=%s, country=%s WHERE id=%s",
            (data["name"], data["age"], data["country"], id)
        )

    conn.commit()
    conn.close()

    return jsonify({"message": "User Updated Successfully ✨"})


@app.route("/delete/<int:id>", methods=["DELETE"])
def delete(id):
    conn = get_connection()

    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM users WHERE id=%s", (id,))

    conn.commit()
    conn.close()

    return jsonify({"message": "User Deleted Successfully ❌"})


if __name__ == "__main__":
    app.run(debug=True)
