import json
from web3 import Web3
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

def load_config():
    with open("config.json", 'r') as f:
        return json.load(f)

def load_deployment():
    with open("deployment_info.json", 'r') as f:
        return json.load(f)

def connect_blockchain():
    config = load_config()
    deployment = load_deployment()
    
    w3 = Web3(Web3.HTTPProvider(config['ganache_url']))
    
    if not w3.is_connected():
        raise Exception("Failed to connect to Ganache")
    
    contract = w3.eth.contract(
        address=deployment['contract_address'],
        abi=deployment['abi']
    )
    
    print(f"{Fore.GREEN}✓ Connected to Ganache")
    print(f"{Fore.YELLOW}Contract: {deployment['contract_address']}\n")
    
    return w3, contract, config

def add_data_to_blockchain(w3, contract, config, data):
    print(f"{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}Adding Data to Blockchain")
    print(f"{Fore.CYAN}{'='*60}\n")
    
    print(f"{Fore.YELLOW}Data: {Fore.WHITE}{data}")
    
    nonce = w3.eth.get_transaction_count(config['account_address'])
    
    transaction = contract.functions.storeData(data).build_transaction({
        'from': config['account_address'],
        'nonce': nonce,
        'gas': 300000,
        'gasPrice': w3.eth.gas_price
    })
    
    signed_txn = w3.eth.account.sign_transaction(transaction, config['private_key'])
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    
    print(f"{Fore.YELLOW}Transaction Hash: {Fore.WHITE}{tx_hash.hex()}")
    print(f"{Fore.CYAN}Waiting for confirmation...")
    
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    data_id = contract.functions.getDataCount().call()
    
    print(f"{Fore.GREEN}✓ Data Added Successfully!")
    print(f"{Fore.YELLOW}Record ID: {Fore.WHITE}{data_id}")
    print(f"{Fore.YELLOW}Block Number: {Fore.WHITE}{receipt.blockNumber}")
    print(f"{Fore.YELLOW}Gas Used: {Fore.WHITE}{receipt.gasUsed}\n")
    
    return data_id

def read_data_from_blockchain(contract, record_id):
    print(f"{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}Reading Data from Blockchain")
    print(f"{Fore.CYAN}{'='*60}\n")
    
    print(f"{Fore.YELLOW}Fetching Record ID: {Fore.WHITE}{record_id}")
    
    result = contract.functions.getData(record_id).call()
    
    print(f"\n{Fore.GREEN}✓ Data Retrieved Successfully!\n")
    print(f"{Fore.CYAN}{'='*60}")
    print(f"{Fore.YELLOW}Record ID: {Fore.WHITE}{result[0]}")
    print(f"{Fore.YELLOW}Data: {Fore.WHITE}{result[1]}")
    print(f"{Fore.YELLOW}Creator: {Fore.WHITE}{result[2]}")
    print(f"{Fore.YELLOW}Timestamp: {Fore.WHITE}{datetime.fromtimestamp(result[3]).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{Fore.YELLOW}Status: {Fore.WHITE}{'Active' if result[4] else 'Deleted'}")
    print(f"{Fore.CYAN}{'='*60}\n")
    
    return result

def main():
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}Blockchain Data Management - Ganache")
    print(f"{Fore.CYAN}{'='*60}\n")
    
    try:
        w3, contract, config = connect_blockchain()
        
        print(f"{Fore.CYAN}Demo 1: Adding Data to Blockchain\n")
        data1 = "Student Record: Name=Ranveer, Roll=2023001, Grade=A+"
        record_id1 = add_data_to_blockchain(w3, contract, config, data1)
        
        print(f"{Fore.CYAN}Demo 2: Reading Data from Blockchain\n")
        read_data_from_blockchain(contract, record_id1)
        
        print(f"{Fore.CYAN}Demo 3: Adding More Data\n")
        data2 = "Document Hash: abc123def456 | Type: Invoice | Amount: Rs.5000"
        record_id2 = add_data_to_blockchain(w3, contract, config, data2)
        
        print(f"{Fore.CYAN}Demo 4: Reading Second Record\n")
        read_data_from_blockchain(contract, record_id2)
        
        total_records = contract.functions.getDataCount().call()
        print(f"{Fore.GREEN}{'='*60}")
        print(f"{Fore.GREEN}Total Records on Blockchain: {total_records}")
        print(f"{Fore.GREEN}{'='*60}\n")
        
        print(f"{Fore.CYAN}Reading All Records:\n")
        for i in range(1, total_records + 1):
            result = contract.functions.getData(i).call()
            print(f"{Fore.YELLOW}Record {i}: {Fore.WHITE}{result[1][:50]}...")
        
        print(f"\n{Fore.GREEN}{'='*60}")
        print(f"{Fore.GREEN}Demo Completed Successfully!")
        print(f"{Fore.GREEN}{'='*60}\n")
        
    except FileNotFoundError as e:
        print(f"{Fore.RED}Error: deployment_info.json not found!")
        print(f"{Fore.YELLOW}Please run 'python deploy_contract.py' first\n")
    except Exception as e:
        print(f"{Fore.RED}Error: {e}\n")

if __name__ == "__main__":
    main()
