from flask import Flask, request, send_from_directory
from web3 import Web3
import os, json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder="front_end", static_url_path="")

# Blockchain connection
INFURA_URL = os.getenv("INFURA_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

web3 = Web3(Web3.HTTPProvider(INFURA_URL))
print("✅ Connected to blockchain:", web3.is_connected())

# Load contract ABI
with open("abi.json") as f:
    abi = json.load(f)

contract = web3.eth.contract(
    address=Web3.to_checksum_address(CONTRACT_ADDRESS),
    abi=abi
)


@app.route("/")
def home():
    """Serve homepage"""
    return send_from_directory("front_end", "index.html")


@app.route("/verify", methods=["GET"])
def verify_certificate():
    """Verify certificate by unique code"""
    code = request.args.get("code")

    if not code:
        return send_from_directory("front_end", "invalid.html")

    try:
        print(f"🔍 Checking blockchain for certificate code: {code}")

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

        print("📦 Blockchain returned:", cert_data)

        if not valid or cert_code == "":
            print("❌ Certificate not valid or not found")
            return send_from_directory("front_end", "invalid.html")

        # ✅ Verified page (mobile-friendly)
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Certificate Verified</title>
            <link rel="stylesheet" href="/style.css">
        </head>
        <body>
            <div class="container success">
                <div class="icon">✅</div>
                <h1>Certificate Verified</h1>
                <div class="card">
                    <p><strong>Name:</strong> {name}</p>
                    <p><strong>Unique Code:</strong> {cert_code}</p>
                    <p><strong>Event:</strong> {eventname}</p>
                    <p><strong>Date:</strong> {eventdate}</p>
                    <p><strong>Issued By:</strong> {issuedBy}</p>
                    <p><strong>Issuer Address:</strong> {issuer}</p>
                    <p><small>Timestamp:</small> {timestamp}</p>
                </div>
                <a href="/" class="btn">Verify Another</a>
            </div>
        </body>
        </html>
        """

    except Exception as e:
        print("⚠️ Error verifying certificate:", e)
        return send_from_directory("front_end", "invalid.html")


@app.route("/<path:path>")
def static_files(path):
    """Serve static files (CSS, etc.)"""
    return send_from_directory("front_end", path)


@app.errorhandler(404)
def not_found(e):
    """Fallback for invalid URLs"""
    return send_from_directory("front_end", "invalid.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
