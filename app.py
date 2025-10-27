from flask import Flask, request, send_from_directory
from web3 import Web3
import os, json
from dotenv import load_dotenv

app = Flask(__name__, static_folder="front_end", static_url_path="")

load_dotenv()
INFURA_URL = os.getenv("INFURA_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

web3 = Web3(Web3.HTTPProvider(INFURA_URL))
print("Connected:", web3.is_connected())

with open("abi.json") as f:
    abi = json.load(f)

contract = web3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=abi)

@app.route("/verify")
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

        tx_hash = None
        event_filter = contract.events.CertificateIssued.create_filter(fromBlock=0, toBlock='latest')
        events = event_filter.get_all_entries()
        for e in events:
            if e.args.code == cert_code:
                tx_hash = e.transactionHash.hex()
                break

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
                    <p><small>Timestamp:</small> {timestamp}</p>
                    {"<p><strong>Transaction:</strong> <a href='https://sepolia.etherscan.io/tx/" + tx_hash + "' target='_blank'>" + tx_hash + "</a></p>" if tx_hash else ""}
                </div>
                <a href="/" class="btn">Verify Another</a>
            </div>
        </body>
        </html>
        """

    except Exception as e:
        print("Verification error:", e)
        return send_from_directory("front_end", "invalid.html")
