from web3 import Web3
import json, os
from dotenv import load_dotenv

class BlockChain:
    
    def __init__(self):
        load_dotenv()
        self.AMOY_URL = os.getenv("AMOY_URL")
        self.PRIVATE_KEY = os.getenv("PRIVATE_KEY")
        self.WALLET_ADDRESS = Web3.to_checksum_address(os.getenv("WALLET_ADDRESS"))
        self.CONTRACT_ADDRESS = Web3.to_checksum_address(os.getenv("CONTRACT_ADDRESS"))


        self.web3 = Web3(Web3.HTTPProvider(self.AMOY_URL))
        print("Connected:", self.web3.is_connected())

        if not self.web3.is_connected():
            raise Exception("Could not connect to blockchain")

        with open("abi.json") as f:
            abi = json.load(f)

        self.contract = self.web3.eth.contract(address=self.CONTRACT_ADDRESS, abi=abi)


    def issue_certificate(self,name, code, eventname, eventdate, issued_by):

        nonce = self.web3.eth.get_transaction_count(self.WALLET_ADDRESS)

        txn = self.contract.functions.issueCertificate(
            name, code, eventname, eventdate, issued_by
        ).build_transaction({
            'from': self.WALLET_ADDRESS,
            'nonce': nonce,
            'gas': 400000,
            'maxFeePerGas': self.web3.to_wei('30', 'gwei'),
            'maxPriorityFeePerGas': self.web3.to_wei('25', 'gwei'),
        })

        signed_txn = self.web3.eth.account.sign_transaction(txn, private_key=self.PRIVATE_KEY)

        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        tx_hash_hex = self.web3.to_hex(tx_hash)

        print("Waiting for blockchain confirmation...")
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"▶ Confirmed in block #{tx_receipt.blockNumber}")


        print(f"Certificate {code} issued for {name}")
        
        return tx_hash_hex
