import os
import resend
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import sqlite3

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


#MTG Tracker end point

MTG_DB = os.path.expanduser("~/Projects/mtg-tracker/db/mtg.db")

@app.route("/mtg/prices", methods=["GET"])
def mtg_prices():
    conn = sqlite3.connect(MTG_DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
        SELECT c.name, ph.price_usd, ph.recorded_at
        FROM price_history ph
        JOIN cards c ON ph.card_id = c.id
        ORDER BY c.name, ph.recorded_at ASC
    """)

    rows = cur.fetchall()
    conn.close()

    # Group prices by card name
    cards = {}
    for row in rows:
        name = row["name"]
        if name not in cards:
            cards[name] = []
        cards[name].append({
            "price": row["price_usd"],
            "date": row["recorded_at"]
        })

    return jsonify(cards)

#At the bottom of everything - Bright Eyes
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5051)
