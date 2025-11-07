from flask import Flask, jsonify, render_template, request, abort
import os
import mysql.connector
from mysql.connector import Error

# ------------------------------
# Configuration
# ------------------------------
BASE_DIR = os.path.dirname(__file__)
STATIC_DIR = os.path.join(BASE_DIR, 'Satic')
TEMPLATES_DIR = os.path.join(BASE_DIR, 'Templates')

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "yourpassword",  # <-- change this
    "database": "spinner_db",
    "port": 3306
}

app = Flask(__name__, static_folder=STATIC_DIR, template_folder=TEMPLATES_DIR)

# ------------------------------
# Helper: MySQL Connection
# ------------------------------
def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"[MySQL Error] {e}")
        return None

# ------------------------------
# Routes
# ------------------------------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/group')
def group_page():
    return render_template('group.html')

@app.route('/images')
def images_page():
    return render_template('images.html')

@app.route('/api/status')
def status():
    return jsonify(status='ok', message='API is running')

@app.route('/api/templates')
def list_templates():
    try:
        files = [f for f in os.listdir(TEMPLATES_DIR) if f.endswith('.html')]
    except Exception as e:
        print(f"Template listing error: {e}")
        files = []
    return jsonify(templates=files)

@app.route('/api/template/<name>')
def get_template(name):
    if not name.endswith('.html'):
        name = f"{name}.html"
    path = os.path.join(TEMPLATES_DIR, name)
    if not os.path.exists(path):
        return abort(404, description='Template not found')
    as_html = request.args.get('html', 'false').lower() in ('1', 'true', 'yes')
    rendered = render_template(name)
    return rendered if as_html else jsonify(name=name, html=rendered)

@app.route('/api/entries', methods=['GET'])
def get_entries():
    conn = get_db_connection()
    if not conn:
        return jsonify(error="Cannot connect to MySQL server"), 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM entries")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(entries=rows)

@app.route('/api/entries', methods=['POST'])
def add_entry():
    data = request.json
    name = data.get('name')
    if not name:
        return jsonify(error="Missing 'name' field"), 400

    conn = get_db_connection()
    if not conn:
        return jsonify(error="Cannot connect to MySQL server"), 500

    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO entries (name) VALUES (%s)", (name,))
        conn.commit()
        entry_id = cursor.lastrowid
    except Error as e:
        conn.rollback()
        print(f"MySQL insert error: {e}")
        return jsonify(error=str(e)), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify(id=entry_id, name=name), 201

@app.route('/api/static/<path:filename>')
def static_file(filename):
    return app.send_static_file(filename)

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

# ------------------------------
# Main
# ------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
