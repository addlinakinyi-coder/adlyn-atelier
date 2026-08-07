from flask import Flask, render_template, request, jsonify
import requests
from requests.auth import HTTPBasicAuth
import datetime
import base64
import os

app = Flask(__name__)

# --- M-PESA DARAJA CONFIGURATION ---
CONSUMER_KEY = os.getenv("MPESA_CONSUMER_KEY", "your_consumer_key")
CONSUMER_SECRET = os.getenv("MPESA_CONSUMER_SECRET", "your_consumer_secret")
BUSINESS_SHORTCODE = os.getenv("MPESA_SHORTCODE", "174379") # Sandbox Lipa na M-Pesa Online
PASSKEY = os.getenv("MPESA_PASSKEY", "your_passkey")
CALLBACK_URL = os.getenv("MPESA_CALLBACK_URL", "https://your-domain.com/api/callback")

def get_mpesa_access_token():
    api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    r = requests.get(api_url, auth=HTTPBasicAuth(CONSUMER_KEY, CONSUMER_SECRET))
    json_response = r.json()
    return json_response.get("access_token")

# --- ROUTES ---

@app.route('/')
def home():
    products = [
        {"id": 1, "name": "Classic Apparel", "category": "Apparel", "price": 1500, "image": "apparel.jpg"},
        {"id": 2, "name": "Kids Wear", "category": "Kids Thrift", "price": 800, "image": "kids.jpg"},
        {"id": 3, "name": "Premium Detergent", "category": "Detergents", "price": 500, "image": "detergent.jpg"}
    ]
    return render_template('index.html', products=products)

@app.route('/api/stkpush', methods=['POST'])
def stk_push():
    data = request.get_json()
    phone_number = data.get('phone') # Format: 2547XXXXXXXX
    amount = data.get('amount')

    access_token = get_mpesa_access_token()
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    data_to_encode = BUSINESS_SHORTCODE + PASSKEY + timestamp
    online_password = base64.b64encode(data_to_encode.encode()).decode('utf-8')

    stk_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    payload = {
        "BusinessShortCode": BUSINESS_SHORTCODE,
        "Password": online_password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": BUSINESS_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": "AdlynAtelier",
        "TransactionDesc": "Payment for goods"
    }

    response = requests.post(stk_url, json=payload, headers=headers)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)
