###############################
# PACKAGE: WhatsAppWrapper
# Path: app/whatsapp_client.py
###############################
import os
import requests as r
import json


class WhatsAppWrapper:
    API_URL = "https://graph.facebook.com/v13.0/"
    API_TOKEN = os.environ.get("WHATSAPP_API_TOKEN")
    NUMBER_ID = os.environ.get("WHATSAPP_NUMBER_ID")

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {self.API_TOKEN}",
            "Content-Type": "application/json"
        }
        self.API_URL = self.API_URL + self.NUMBER_ID

    def send_template_message(self, template_name, language_code, phone_number):
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": language_code
                }
            }
        })

        response = r.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)

        assert response.status_code == 200, "Error sending message"

        return response.status_code

    def process_webhook_notification(self, data):
        ################################################
        # RECEIVES NOTIFICATION DATA FROM META WEBHOOKS
        ################################################
        response = []

        for entry in data["entry"]:
            for change in entry["changes"]:
                for contact, message in zip(change["value"]["contacts"], change["value"]["messages"]):
                    response.append({
                        "type": change["field"],
                        "receiver_name": change["value"]["messaging_product"],
                        "receiver_phone": change["value"]["metadata"]["display_phone_number"],
                        "sender_name": contact["profile"]["name"],
                        "sender_phone": contact["wa_id"],
                        "message_content": message["text"]["body"],

                    })
        return response



