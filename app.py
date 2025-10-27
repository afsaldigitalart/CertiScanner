from flask import Flask, render_template_string, request, send_from_directory, jsonify
from web3 import Web3
import json, os
from dotenv import load_dotenv

app = Flask(__name__, static_folder="front_end", template_folder="front_end")

# Load environment variables
load_dotenv()

INFURA_URL = os.getenv("INFURA_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

# Connect to Web3
web3 = Web3(Web3.HTTPProvider(INFURA_URL))
print("Connected:", web3.is_connected())

if not web3.is_connected():
    raise Exception("Failed to connect to blockchain")

with open("abi.json") as f:
    abi = json.load(f)

contract = web3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=abi)

# ---------- ROUTES ---------- #

@app.route("/")
def home():
    return send_from_directory("front_end", "index.html")

@app.route("/style.css")
def style():
    return send_from_directory("front_end", "style.css")

@app.route("/verify", methods=["GET"])
def verify_certificate():
    # Example: /verify?code=ABC123
    cert_code = request.args.get("code")
    if not cert_code:
        return jsonify({"error": "Missing certificate code"}), 400

    try:
        # Contract function that fetches details by code
        cert_data = contract.functions.certificates(cert_code).call()

        name, code, event_name, event_date, issued_by, is_valid = cert_data

        if not is_valid:
            return jsonify({"valid": False, "message": "Certificate revoked or invalid"})

        return jsonify({
            "valid": True,
            "name": name,
            "code": code,
            "event_name": event_name,
            "event_date": event_date,
            "issued_by": issued_by
        })

    except Exception as e:
        print("Error verifying certificate:", e)
        return jsonify({"valid": False, "error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
