import os
import json
from BlockFunctions import Helper
from BlockChain import BlockChain

folder_path = r"Certificates/"
event_name = "Chatbot Building and Ideation"
event_date = "18/09/2025"
issued_by = "Inspira IEDC CSE, Marian Engineering College"
PREFIX = "CHT"
tx_hash_file = 'tx_hashes.json'

bf = Helper()
bc = BlockChain()

if os.path.exists(tx_hash_file):
    with open(tx_hash_file, 'r') as f:
        tx_hashes = json.load(f)
else:
    tx_hashes = {}

for file in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file)

    if not os.path.isfile(file_path):
        continue
    if not file.lower().endswith(('.png', '.jpg', '.jpeg')):
        continue

    name = os.path.splitext(file)[0]
    code = bf.UniCode(PREFIX)
    
    BCcode = bc.issue_certificate(name, code, event_name, event_date, issued_by)

    tx_hashes[code] = BCcode

    with open(tx_hash_file, 'w') as f:
        json.dump(tx_hashes, f, indent=2)
    
    print(f"Saved TX hash for {code}: {BCcode}")
    
    qr = bf.makeQR(f"https://certiscanner.onrender.com/verify?code={code}")
    bf.placeQR(file_path, qr, code, X=1465, Y=379)

if os.path.exists(tx_hash_file):
    os.remove(tx_hash_file)

print("\n===================================")
print("\nAll certificates issued!")
print("\n===================================")