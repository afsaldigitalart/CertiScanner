# ⫘⫘⫘ CertiChain ⫘⫘⫘

CertiChain is a blockchain-based certificate issuing and verification system.\
It allows organizations to **issue verifiable certificates** on-chain, generate **QR-embedded digital certificates**, and host a **web verification portal** for authenticity checks.

Hosted live on Render: [**https://certiscanner.onrender.com/**](https://certiscanner.onrender.com/)

---

## Why I Built This?

I’m a graphic designer, and I often create certificates for college events. Over time, I realized how easy it is for anyone to **forge or duplicate** digital certificates. That bothered me - authenticity should mean something.

So I decided to solve it by building **CertiChain**, a system that uses **blockchain technology** to make every certificate **verifiable, immutable, and tamper-proof**.\
It also became a great way for me to **learn about blockchain development** hands-on - connecting smart contracts, Flask, and Python with real-world design work.

---

## Flow of the Project

CertiChain  anchors each certificate’s data (like recipient name, event, date, and issuer) on the **Polygon blockchain (Layer 2)**, making verification **trustless and permanent**.

Here’s what happens behind the scenes:

1. The admin runs a script (`main.py`) that:

   - Reads certificate images from a folder.
   - Generates a unique certificate code.
   - Uploads the details to a **smart contract** deployed on the blockchain.
   - Embeds a **QR code** on the certificate image that links to a verification page.

2. The smart contract stores all issued certificates permanently.

3. Anyone can scan the QR or visit the `/verify?code=...` link to check authenticity — served via Render (`app.py`).

---

## The Whole Project Structure

```
CertiChain/
│
├── SmartContract/
│   └── certificateRegistry.sol           # Solidity smart contract
│
├── core/
│   ├── BlockChain.py             # Handles blockchain transactions and certificate issuance
│   └── BlockFunctions.py         # Handles QR generation, image placement, and code creation
│
├── Certificates/                 # Raw certificate images (input)
│
├── generated/                    # Certificates with QR (output)
│
├── front_end/
│   ├── index.html                # Home page
│   ├── verification.html         # Success page for valid certificates
│   └── invalid.html              # Error page for invalid/unknown codes
│
├── abi.json                      # ABI file generated after compiling Certificate.sol
├── main.py                       # Issues certificates and generates QR images
├── app.py                        # Web server for verification
├── .env                          # Environment variables 
└── LOGtx_hashes.json             # Logs blockchain transaction hashes
```

---

## How It is Working?

### 1. Smart Contract (certificateRegistry.sol)

Defines functions like:

- `issueCertificate(...)` → Records a certificate on-chain.
- `verifyCertificate(code)` → Returns details of a given certificate. Each record includes:

```
name, code, eventName, eventDate, issuedBy, issuerAddress, timestamp, valid
```

---

### 2. Blockchain Interaction (`core/BlockChain.py`)

This class:

- Connects to the blockchain using **Web3.py**
- Loads ABI and contract address from `.env`
- Builds and signs transactions to call `issueCertificate`
- Waits for blockchain confirmation
- Returns the transaction hash

Key environment variables used:

```env
AMOY_URL=       # Polygon Amoy Testnet RPC URL (via Infura or Alchemy)
PRIVATE_KEY=    # Your MetaMask private key
WALLET_ADDRESS= # Your wallet address (public)
CONTRACT_ADDRESS= # Deployed smart contract address
```

---

### 3. Certificate Handling (`core/BlockFunctions.py`)

Handles the visual and QR side:

- `UniCode()` → Creates a unique code like `CHT1234567`
- `makeQR()` → Generates a QR image containing the verification link
- `placeQR()` → Pastes the QR and code text on the certificate image

Output is saved under `/generated`.

---

### 4. Render Verification (`app.py`)

This small web server:

- Connects to the blockchain (read-only)
- Handles `/verify?code=XYZ`
- Calls `verifyCertificate()` on-chain
- If valid → renders `verification.html` with certificate details
- If invalid → shows `invalid.html`

This app is deployed live on Render at:\
[**https://certiscanner.onrender.com/**](https://certiscanner.onrender.com/)

You can also run it locally.

---

## Setting up Locally

### 1. Clone and Install

```bash
git clone https://github.com/yourusername/CertiChain.git
cd CertiChain
pip install -r requirements.txt
```

---

### 2. Create `.env` file in project root

```bash
AMOY_URL=https://polygon-amoy.infura.io/v3/YOUR_INFURA_PROJECT_ID
PRIVATE_KEY=YOUR_METAMASK_PRIVATE_KEY
WALLET_ADDRESS=0xYourWalletAddress
CONTRACT_ADDRESS=0xYourDeployedContractAddress
```

Make sure:

- The contract is deployed on **Polygon Amoy Testnet**
- The wallet has a small amount of test MATIC for gas

---

### 3. Prepare Your Certificates

!**Put blank certificates (PNG/JPG) inside ********************************************************************************an Empty Folder********************************************************************************.The filename should match the recipient’s name, for example:**

```
Certificates/
├── Alice.png
├── Bob.png
└── Charlie.jpg
```

---

### 4. Run the Issuance Script

```bash
python main.py
```

This will:

- Connect to the blockchain
- Issue certificates
- Log TX hashes to `LOGtx_hashes.json`
- Generate QR-embedded certificates inside `/generated`

---

## Future Improvements

- UI Implementatio
- Add MetaMask login for issuing directly from UI
- Integrate IPFS for certificate storage
- Build an admin dashboard for issued certificates

---

## Author

**Afsal**\
Engineering Student & Graphic Designer



CertiChain ties together blockchain, QR codes, and Flask —\
turning digital certificates into **trustworthy, verifiable records**.

No middlemen, no forgery, just cryptographic truth.



---

