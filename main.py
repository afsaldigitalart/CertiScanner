import os
from BlockFunctions import Helper
from BlockChain import BlockChain

folder_path = r"Certificates/"
event_name = "DESIGNX"
event_date = "25/11/2025"
issued_by = "Inspira IEDC, Marian Engineering College"
PREFIX = "AFS"

bf = Helper()
bc = BlockChain()

for file in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file)

    if not os.path.isfile(file_path):
        continue
    if not file.lower().endswith(('.png', '.jpg', '.jpeg')):
        continue

    name = os.path.splitext(file)[0]
    code = bf.UniCode(PREFIX)
    
    BCcode = bc.issue_certificate(name, code, event_name, event_date, issued_by)
    try:
        with open('temp.txt', 'w') as file:
            file.write(BCcode)
    except:
        print("Error Occured")
    finally:
        os.remove(r"temp.txt")
    qr = bf.makeQR(f"https://certiscanner.onrender.com/verify?code={code}")
    bf.placeQR(file_path, qr, code, X=1465, Y=379)

