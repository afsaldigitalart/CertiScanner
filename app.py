from flask import Flask, request, send_from_directory
from web3 import Web3
import os, json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder="front_end", static_url_path="")

INFURA_URL = os.getenv("INFURA_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

web3 = Web3(Web3.HTTPProvider(INFURA_URL))
print("✅ Connected to blockchain:", web3.is_connected())

with open("abi.json") as f:
    abi = json.load(f)

contract = web3.eth.contract(
    address=Web3.to_checksum_address(CONTRACT_ADDRESS),
    abi=abi
)


@app.route("/")
def home():
    return send_from_directory("front_end", "index.html")


@app.route("/verify", methods=["GET"])
def verify_certificate():

    code = request.args.get("code")

    if not code:
        return send_from_directory("front_end", "invalid.html")

    try:

        with open ("temp.txt", "w") as f:
            hash = f.readline()

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

        if not valid or cert_code == "":
            return send_from_directory("front_end", "invalid.html")

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
                    <p><small>Transaction Code: </small>  <a href = "https://etherscan.io/tx/{hash}"> {hash} </a> </p>
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
    return send_from_directory("front_end", path)


@app.errorhandler(404)
def not_found(e):

    return send_from_directory("front_end", "invalid.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
