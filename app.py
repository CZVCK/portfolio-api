import os
import resend
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

resend.api_key = os.getenv("RESEND_API_KEY")

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

@app.route("/contact", methods=["POST"])
@limiter.limit("5 per hour")
def contact():
    data = request.get_json()

    if data.get("website"):
        return jsonify({"success": True}), 200

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    message = data.get("message", "").strip()

    if not name or not email or not message:
        return jsonify({"error": "[ERROR] All fields required"}), 400

    if len(message) > 2000:
        return jsonify({"error": "I aint got time to read all that."}), 400

    resend.Emails.send({
        "from": os.getenv("SENDER_ADDRESS"),
        "to": os.getenv("CONTACT_RECIPIENT"),
        "subject": f"Portfolio contact from {name}",
        "html": (
            f"<p><strong>Name:</strong> {name}</p>"
            f"<p><strong>Email:</strong> {email}</p>"
            f"<p><strong>Message:</strong> {message}</p>"
        ),
    })

    return jsonify({"success": True}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5051)
