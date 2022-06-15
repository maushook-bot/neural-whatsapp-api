import os
from flask import Flask, jsonify, request
from app.whatsapp_client import WhatsAppWrapper

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("WHATSAPP_HOOK_TOKEN")


@app.route("/")
def home():
    return "Home Route"


@app.route("/send_template_message/", methods=['POST'])
def send_template_message():
    """
    SENDS A MESSAGE WITH TEMPLATE FROM PHONE NO
    """
    print("[POST]: send_template_message")
    if "language_code" not in request.json:
        return jsonify({
            "error": "Language code is missing"
        }), 400
    elif "template_name" not in request.json:
        return jsonify({
            "error": "Template Name is missing"
        }), 400
    elif "phone_number" not in request.json:
        return jsonify({
            "error": "Phone Number is missing"
        }), 400

    client = WhatsAppWrapper()
    response = client.send_template_message(
        template_name=request.json["template_name"],
        language_code=request.json["language_code"],
        phone_number=request.json["phone_number"],
    )
    print(f"POST: {response}")

    return jsonify({
        "data": response,
        "status": "success"
    }), 200


@app.route("/webhook/", methods=["POST", "GET"])
def webhook_whatsapp():
    """
    RECEIVE NOTIFICATION FROM META SERVER
    """
    print("[POST/GET]: /webhook")

    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            print("[GET]: /webhook, TOKEN VERIFIED!")
            return request.args.get('hub.challenge')
        print("[GET]: /webhook, TOKEN NOT VERIFIED")
        return jsonify({
          'message': "Authentication Failed: Token is Invalid",

        }), 401

    client = WhatsAppWrapper()
    print(f"[DATA /webhook] => {request.get_json()}")
    response = client.process_webhook_notification(request.get_json())
    result = {
        "status": "success",
        "status_code": 200,
        "data": response,
    }
    print(f"RESPONSE DATA => {result}")

    return jsonify(result), 200
