from flask import Flask, request, send_from_directory
from web3 import Web3
import os, json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder="front_end", static_url_path="")

INFURA_URL = os.getenv("INFURA_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

web3 = Web3(Web3.HTTPProvider(INFURA_URL))

with open("abi.json") as f:
    abi = json.load(f)

contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

@app.route("/")
def home():
    return send_from_directory("front_end", "index.html")

@app.route("/verify", methods=["GET"])
def verify_certificate():
    code = request.args.get("code")
    if not code:
        return send_from_directory("front_end", "invalid.html")

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
            return send_from_directory("front_end", "invalid.html")

        # ✅ Mobile-friendly verified page
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <meta charset="UTF-8">
            <title>Certificate Verified</title>
            <link rel="stylesheet" href="/style.css">
        </head>
        <body>
            <div class="container success">
                <div class="icon">✅</div>
                <h1>Certificate Verified</h1>
                <div class="card">
                    <p><strong>Name:</strong> {name}</p>
                    <p><strong>Certificate Code:</strong> {cert_code}</p>
                    <p><strong>Event:</strong> {eventname}</p>
                    <p><strong>Date:</strong> {eventdate}</p>
                    <p><strong>Issued By:</strong> {issuedBy}</p>
                    <p><strong>Issuer Address:</strong> {issuer}</p>
                    <p><small>Timestamp: {timestamp}</small></p>
                </div>
                <a href="/" class="btn">Verify Another</a>
            </div>
        </body>
        </html>
        """

    except Exception as e:
        print("Verification error:", e)
        return send_from_directory("front_end", "invalid.html")


@app.route("/<path:path>")
def static_files(path):
    return send_from_directory("front_end", path)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
