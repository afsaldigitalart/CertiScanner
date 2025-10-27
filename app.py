from flask import Flask, request, render_template
from web3 import Web3
import json, os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

INFURA_URL = os.getenv("INFURA_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

web3 = Web3(Web3.HTTPProvider(INFURA_URL))
with open("contractABI.json") as f:
    abi = json.load(f)

contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

@app.route("/")
def home():
    return "Certificate Verification API is running."

@app.route("/verify")
def verify():
    hash_value = request.args.get("hash")
    if not hash_value:
        return render_template("verify.html", error="No hash provided")

    try:
        # Call the smart contract function (example)
        cert = contract.functions.certificates(hash_value).call()

        if cert[0] == "":
            return render_template("verify.html", valid=False)

        data = {
            "name": cert[0],
            "eventName": cert[1],
            "eventDate": cert[2],
            "issuedBy": cert[3],
            "hash": hash_value
        }
        return render_template("verify.html", valid=True, data=data)

    except Exception as e:
        return render_template("verify.html", error=str(e))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
