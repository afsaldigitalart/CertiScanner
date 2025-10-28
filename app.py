from flask import Flask, request, send_from_directory
from web3 import Web3
import os, json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder="front_end", static_url_path="")

AMOY_URL = os.getenv("AMOY_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

web3 = Web3(Web3.HTTPProvider(AMOY_URL))
print("Connected to blockchain:", web3.is_connected())

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
        with open("tx_hashes.json", "r") as f:
            tx_map = json.load(f)
            tx_hash = tx_map.get(code, "")


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

        with open("front_end/verification.html", "r", encoding="utf-8") as f:
            template = f.read()
        
        html = template.replace("{name}", name)\
                       .replace("{cert_code}", cert_code)\
                       .replace("{eventname}", eventname)\
                       .replace("{eventdate}", eventdate)\
                       .replace("{issuedBy}", issuedBy)\
                       .replace("{issuer}", issuer)\
                       .replace("{timestamp}", str(timestamp))\
                       .replace("{tx_hash}", tx_hash)
        
        return html
        
    except Exception as e:
        print("Error verifying certificate:", e)
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