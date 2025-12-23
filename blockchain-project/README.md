# Blockchain Data Management System

Simple blockchain application for storing and reading data using Ganache local blockchain.

## Quick Setup

### 1. Install Requirements
```bash
pip install web3 py-solc-x colorama
```

### 2. Start Ganache
- Download and install Ganache: https://trufflesuite.com/ganache/
- Open Ganache and click "Quickstart Ethereum"
- Copy an account address and its private key

### 3. Update config.json
```json
{
    "ganache_url": "http://127.0.0.1:7545",
    "account_address": "YOUR_ACCOUNT_ADDRESS_FROM_GANACHE",
    "private_key": "YOUR_PRIVATE_KEY_FROM_GANACHE",
    "solc_version": "0.8.20",
    "gas_limit": 3000000
}
```

## Usage

### Step 1: Deploy Smart Contract
```bash
python deploy_contract.py
```
This compiles and deploys the smart contract to Ganache.

### Step 2: Add and Read Data
```bash
python manage_data.py
```

This will:
- Store data on blockchain
- Read data from blockchain
- Display all information

## Files

- `deploy_contract.py` - Deploy smart contract to Ganache
- `manage_data.py` - Add and read data from blockchain
- `contracts/DataStorage.sol` - Solidity smart contract
- `config.json` - Configuration file
- `requirements.txt` - Python dependencies

## Features

✓ Deploy smart contract to Ganache  
✓ Store data on blockchain  
✓ Read data from blockchain  
✓ Automatic gas estimation  
✓ Transaction verification  

## Technology

- Python 3.8+
- Web3.py
- Solidity 0.8.20
- Ganache (Local Ethereum)

## For Internship Application

This project demonstrates:
- Python programming
- Blockchain integration
- Smart contract deployment
- Data management
- Clean, simple code
