from flask import Flask, request, send_from_directory, jsonify
from web3 import Web3
import json, os
from dotenv import load_dotenv

app = Flask(__name__, static_folder="front_end", template_folder="front_end")

load_dotenv()

INFURA_URL = os.getenv("INFURA_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

web3 = Web3(Web3.HTTPProvider(INFURA_URL))
print("Connected:", web3.is_connected())

if not web3.is_connected():
    raise Exception("Could not connect to blockchain")

with open("abi.json") as f:
    abi = json.load(f)

contract = web3.eth.contract(
    address=Web3.to_checksum_address(CONTRACT_ADDRESS),
    abi=abi
)


@app.route("/")
def home():
    return send_from_directory("front_end", "index.html")

@app.route("/style.css")
def style():
    return send_from_directory("front_end", "style.css")

@app.route("/verify", methods=["GET"])
def verify_certificate():
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "Missing certificate code"}), 400

    try:
        cert_data = contract.functions.verifyCertificate(code).call()

        (
            name,
            cert_code,
            eventname,
            eventdate,
            issuedBy,
            issuer,
            timestamp,
            valid
        ) = cert_data

        if not valid:
            return jsonify({"valid": False, "message": "Certificate not found"})

        return jsonify({
            "valid": True,
            "name": name,
            "code": cert_code,
            "event_name": eventname,
            "event_date": eventdate,
            "issued_by": issuedBy,
            "issuer": issuer,
            "timestamp": timestamp
        })

    except Exception as e:
        print("Verification error:", e)
        return jsonify({"valid": False, "error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
