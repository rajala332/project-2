from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__,template_folder='template')
app.secret_key = "your_secret_key"  # Change this!

# ----------------------------
# DATABASE CONNECTION
# ----------------------------
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",          # change to your MySQL username
        password="rajalxx33@A",  # change to your MySQL password
        database="hospital_db"
    )

# ----------------------------
# ROUTES
# ----------------------------
@app.route("/")
def home():
    return render_template("HMS_frontend.html")  # your HTML file

# ---------- USER AUTH ----------
@app.route("/register", methods=["POST"])
def register():
    name = request.form["name"]
    email = request.form["email"]
    role = request.form["role"]
    password = generate_password_hash(request.form["password"])

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, role, password) VALUES (%s, %s, %s, %s)",
            (name, email, role, password),
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash("Registration successful! Please log in.")
    except Error as e:
        flash(f"Error: {e}")
    return redirect(url_for("home"))

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email=%s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user and check_password_hash(user["password"], password):
        session["user"] = {"id": user["id"], "name": user["name"], "role": user["role"]}
        flash("Login successful!")
    else:
        flash("Invalid credentials")
    return redirect(url_for("home"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out successfully.")
    return redirect(url_for("home"))

# ---------- PATIENT ----------
@app.route("/patients/save", methods=["POST"])
def save_patient():
    patient_id = request.form["patient_id"]
    name = request.form["name"]
    dob = request.form["dob"]
    sex = request.form["sex"]
    phone = request.form["phone"]
    blood = request.form["blood"]
    allergies = request.form["allergies"]
    history = request.form["history"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO patients (patient_id, name, dob, sex, phone, blood_group, allergies, medical_history) 
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
        (patient_id, name, dob, sex, phone, blood, allergies, history),
    )
    conn.commit()
    cursor.close()
    conn.close()
    flash("Patient saved successfully")
    return redirect(url_for("home"))

# ---------- STAFF ----------
@app.route("/staff/save", methods=["POST"])
def save_staff():
    staff_id = request.form["staff_id"]
    name = request.form["name"]
    role = request.form["role"]
    department = request.form["department"]
    specialization = request.form["specialization"]
    availability = request.form["availability"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO staff (staff_id, name, role, department, specialization, availability) 
           VALUES (%s,%s,%s,%s,%s,%s)""",
        (staff_id, name, role, department, specialization, availability),
    )
    conn.commit()
    cursor.close()
    conn.close()
    flash("Staff saved successfully")
    return redirect(url_for("home"))

# ---------- APPOINTMENTS ----------
@app.route("/appointments/book", methods=["POST"])
def book_appointment():
    patient_id = request.form["patient_id"]
    doctor = request.form["doctor"]
    date = request.form["date"]
    time = request.form["time"]
    reason = request.form["reason"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO appointments (patient_id, doctor, date, time, reason) VALUES (%s,%s,%s,%s,%s)",
        (patient_id, doctor, date, time, reason),
    )
    conn.commit()
    cursor.close()
    conn.close()
    flash("Appointment booked successfully")
    return redirect(url_for("home"))

# ---------- BILLING ----------
@app.route("/billing/create", methods=["POST"])
def create_invoice():
    patient_id = request.form["patient_id"]
    desc = request.form["desc"]
    amount = request.form["amount"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO invoices (patient_id, description, amount) VALUES (%s,%s,%s)",
        (patient_id, desc, amount),
    )
    conn.commit()
    cursor.close()
    conn.close()
    flash("Invoice created successfully")
    return redirect(url_for("home"))

# ---------- PHARMACY ----------
@app.route("/pharmacy/save", methods=["POST"])
def save_medicine():
    sku = request.form["sku"]
    name = request.form["name"]
    stock = request.form["stock"]
    form = request.form["form"]
    expiry = request.form["expiry"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO pharmacy (sku, name, stock, form, expiry) VALUES (%s,%s,%s,%s,%s)",
        (sku, name, stock, form, expiry),
    )
    conn.commit()
    cursor.close()
    conn.close()
    flash("Medicine saved successfully")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
