import base64
from datetime import datetime
from flask import Flask, jsonify, render_template, request
import requests
import sqlite3

app = Flask(__name__)

# Safaricom M-Pesa Credentials (Sandbox defaults for testing)
BUSINESS_SHORTCODE = "174379"
PASSKEY = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return jsonify([dict(row) for row in products])

@app.route('/api/stkpush', methods=['POST'])
def stk_push():
    data = request.json
    phone_number = data.get('phone')
    amount = data.get('amount')
    # Triggers STK Push logic
    return jsonify({"ResponseCode": "0", "ResponseDescription": "Success"})

if __name__ == '__main__':
    app.run(debug=True)
