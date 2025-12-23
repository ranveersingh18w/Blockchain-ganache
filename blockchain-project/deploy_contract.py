import json
import os
from web3 import Web3
from solcx import compile_standard, install_solc
from colorama import Fore, Style, init

init(autoreset=True)

class ContractDeployer:
    def __init__(self, config_path="config.json"):
        print(f"{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}Blockchain Contract Deployment System")
        print(f"{Fore.CYAN}{'='*60}\n")
        
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.ganache_url = self.config['ganache_url']
        self.account_address = self.config['account_address']
        self.private_key = self.config['private_key']
        self.solc_version = self.config['solc_version']
        
        self.validate_config()
        
        self.w3 = Web3(Web3.HTTPProvider(self.ganache_url))
        if not self.w3.is_connected():
            raise Exception(f"{Fore.RED}Failed to connect to Ganache at {self.ganache_url}")
        
        print(f"{Fore.GREEN}✓ Connected to Ganache")
        print(f"{Fore.YELLOW}Chain ID: {self.w3.eth.chain_id}")
        print(f"{Fore.YELLOW}Account: {self.account_address}\n")
    
    def validate_config(self):
        if "REPLACE" in self.account_address or "REPLACE" in self.private_key:
            print(f"{Fore.RED}ERROR: Please update config.json with your Ganache credentials")
            print(f"{Fore.YELLOW}\nSteps to configure:")
            print("1. Open Ganache")
            print("2. Copy an account address")
            print("3. Click the key icon to get the private key")
            print("4. Update config.json with these values")
            raise SystemExit(1)
    
    def compile_contract(self, contract_path):
        print(f"{Fore.CYAN}Compiling contract: {contract_path}")
        
        install_solc(self.solc_version)
        
        with open(contract_path, 'r') as f:
            contract_source = f.read()
        
        compiled = compile_standard(
            {
                "language": "Solidity",
                "sources": {os.path.basename(contract_path): {"content": contract_source}},
                "settings": {
                    "optimizer": {"enabled": True, "runs": 200},
                    "evmVersion": "london",
                    "outputSelection": {"*": {"*": ["abi", "evm.bytecode", "evm.deployedBytecode"]}}
                }
            },
            solc_version=self.solc_version
        )
        
        contract_filename = os.path.basename(contract_path)
        contract_name = list(compiled["contracts"][contract_filename].keys())[0]
        
        abi = compiled["contracts"][contract_filename][contract_name]["abi"]
        bytecode = compiled["contracts"][contract_filename][contract_name]["evm"]["bytecode"]["object"]
        
        print(f"{Fore.GREEN}✓ Contract compiled successfully: {contract_name}\n")
        return contract_name, abi, bytecode
    
    def deploy_contract(self, abi, bytecode):
        print(f"{Fore.CYAN}Deploying contract to blockchain...")
        
        Contract = self.w3.eth.contract(abi=abi, bytecode=bytecode)
        nonce = self.w3.eth.get_transaction_count(self.account_address)
        
        try:
            estimated_gas = Contract.constructor().estimate_gas({"from": self.account_address})
            print(f"{Fore.YELLOW}Gas Estimate: {estimated_gas}")
        except Exception as e:
            print(f"{Fore.RED}Gas estimation failed: {e}")
            estimated_gas = 3000000
        
        transaction = Contract.constructor().build_transaction({
            "from": self.account_address,
            "nonce": nonce,
            "gas": int(estimated_gas * 1.2),
            "gasPrice": self.w3.eth.gas_price
        })
        
        signed_txn = self.w3.eth.account.sign_transaction(transaction, self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        
        print(f"{Fore.YELLOW}Transaction Hash: {tx_hash.hex()}")
        print(f"{Fore.CYAN}Waiting for transaction confirmation...")
        
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        print(f"\n{Fore.GREEN}{'='*60}")
        print(f"{Fore.GREEN}✓ Contract Deployed Successfully!")
        print(f"{Fore.GREEN}{'='*60}")
        print(f"{Fore.YELLOW}Contract Address: {tx_receipt.contractAddress}")
        print(f"{Fore.YELLOW}Gas Used: {tx_receipt.gasUsed}")
        print(f"{Fore.YELLOW}Block Number: {tx_receipt.blockNumber}")
        print(f"{Fore.GREEN}{'='*60}\n")
        
        return tx_receipt.contractAddress
    
    def save_deployment_info(self, contract_name, contract_address, abi):
        deployment_info = {
            "contract_name": contract_name,
            "contract_address": contract_address,
            "abi": abi,
            "network": "Ganache Local",
            "deployer": self.account_address
        }
        
        with open("deployment_info.json", "w") as f:
            json.dump(deployment_info, f, indent=4)
        
        print(f"{Fore.GREEN}✓ Deployment info saved to deployment_info.json")

def main():
    try:
        deployer = ContractDeployer()
        
        contract_path = os.path.join("contracts", "DataStorage.sol")
        if not os.path.exists(contract_path):
            print(f"{Fore.RED}Error: Contract file not found at {contract_path}")
            return
        
        contract_name, abi, bytecode = deployer.compile_contract(contract_path)
        contract_address = deployer.deploy_contract(abi, bytecode)
        deployer.save_deployment_info(contract_name, contract_address, abi)
        
        print(f"\n{Fore.CYAN}Next Steps:")
        print(f"{Fore.YELLOW}1. Run 'python main.py' to start using the blockchain system")
        print(f"{Fore.YELLOW}2. The contract is ready to store and manage data")
        
    except Exception as e:
        print(f"{Fore.RED}Error: {e}")
        raise

if __name__ == "__main__":
    main()
