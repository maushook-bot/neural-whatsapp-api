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

    return jsonify({
        "data": response,
        "status": "success"
    }), 200


@app.route("/webhook/", methods=["POST", "GET"])
def webhook_whatsapp():
    """
    RECEIVE NOTIFICATION FROM META SERVER
    """

    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get('hub.challenge')
        #return "Authentication Failed: Token is Invalid"

    client = WhatsAppWrapper()
    response = client.process_webhook_notification(request.get_json())

    return jsonify({
        "status": "success",
        "data": response,
    }), 200
