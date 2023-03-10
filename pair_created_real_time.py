import time
import json
import asyncio
import random
import requests
from web3 import Web3
import mysql.connector
from datetime import datetime

ETHERSCAN_API_KEY = 'B1V982TXGKY38KGM6E4WIHUFZU7DGXDWTP'
EHTERSCAN_API_KEY_LV = 'M1TVWJZKFJ9RIEJDE6C6DX35ZJ8IV8IEGH'

# add your blockchain connection information
infura_url_viti = "https://mainnet.infura.io/v3/a69b219fbd54407faa5af30d764526ef"
infura_url = 'https://mainnet.infura.io/v3/60588a2725ef46fcb8a5a10bbcf10362'
infura_fxindepth = 'https://mainnet.infura.io/v3/c1240437c0004bda83c8faa35d1755ff'
infura_url_97dm = 'https://mainnet.infura.io/v3/457fbd6509e5473fb8acc23193ae1633'
infura_dennis_matios = 'https://mainnet.infura.io/v3/d2f78ad6cdd04364a78505084a561142'
infura_funnygram = 'https://mainnet.infura.io/v3/9d9db586517d424ba8ebfd229ec88aca'
infura_infofunnygram = 'https://mainnet.infura.io/v3/72f66800c7c744009796d2ccbc53d7f4'
infura_igfuturemillionaires = 'https://mainnet.infura.io/v3/9d9db586517d424ba8ebfd229ec88aca'
infura_infohellraiser = 'https://mainnet.infura.io/v3/60588a2725ef46fcb8a5a10bbcf10362'

random_infura = [infura_url_viti, infura_url, infura_fxindepth, infura_url_97dm, infura_dennis_matios, infura_infofunnygram, infura_funnygram, infura_igfuturemillionaires, infura_infohellraiser]
random_ETHERSCAN_API = [ETHERSCAN_API_KEY, EHTERSCAN_API_KEY_LV]

# uniswap address and abi
uniswap_router = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D'
uniswap_factory = '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f'
uniswap_factory_abi = json.loads('[{"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"token0","type":"address"},{"indexed":true,"internalType":"address","name":"token1","type":"address"},{"indexed":false,"internalType":"address","name":"pair","type":"address"},{"indexed":false,"internalType":"uint256","name":"","type":"uint256"}],"name":"PairCreated","type":"event"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"allPairs","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"allPairsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"createPair","outputs":[{"internalType":"address","name":"pair","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"feeTo","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"feeToSetter","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"getPair","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeTo","type":"address"}],"name":"setFeeTo","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"name":"setFeeToSetter","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')

class InsertDbJson():
    def mysqlConnector(self, launch_date, token_address, pair_address, token_name, token_symbol,token_supply, creator_address, creator_eth_balance, token_url, dexcreener):
        # Connect to the database
        cnx = mysql.connector.connect(
            host='sql8.freesqldatabase.com',
            user='sql8593502',
            password='tuz9qrT3jT',
            database='sql8593502',
            port=3306
        )
        # Create a cursor object
        cursor = cnx.cursor()
        # Insert data into the "table_name" table
        
        query = "INSERT INTO pair_created_real_time (launch_date, token_address, pair_address, token_name, token_symbol,token_supply, creator_address, creator_eth_balance, token_url, dexcreener) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE token_address = %s"
        
        data = (launch_date, token_address, pair_address, token_name, token_symbol,token_supply, creator_address, creator_eth_balance, token_url, dexcreener, token_address)
        cursor.execute(query, data)
        # Commit the transaction
        cnx.commit()
        print(f'{token_name} | {token_address} was inserted into the DB')
        # Close the cursor and connection
        cursor.close()
        cnx.close()

class FindEtherscan():
    def build_url(self, TOKEN_ADDRESS):
        url = "https://api.etherscan.io/api"

        params = {
            "module": "token",
            "action": "tokeninfo",
            "contractaddress": TOKEN_ADDRESS,
            "apikey": "B1V982TXGKY38KGM6E4WIHUFZU7DGXDWTP",
        }

        response = requests.get(url, params=params)

        data = json.loads(response.text)
        token_name = data["result"][0]["tokenName"]
        token_symbol = data["result"][0]["symbol"]

        return token_name, token_symbol

    def creator_balance(self, TOKEN_ADDRESS):
        creator_address = self.get_token_creator(TOKEN_ADDRESS)
        random_ETHERSCAN_API = [ETHERSCAN_API_KEY, EHTERSCAN_API_KEY_LV]

        get_creator_balance = json.loads(requests.get(
            f"https://api.etherscan.io/api?module=account&action=balance&address={creator_address}&tag=latest&apikey={random.choice(random_ETHERSCAN_API)}"
        ).text)["result"]
        
        creator_balance = int(get_creator_balance)/10**18
        creator_balance_formated = "{:.8f}".format(float(creator_balance))

        return creator_balance_formated, creator_address

    def get_token_creator(self,TOKEN_ADDRESS):
        random_ETHERSCAN_API = [ETHERSCAN_API_KEY, EHTERSCAN_API_KEY_LV]

        get_contract_creator = json.loads(requests.get(
            f"https://api.etherscan.io/api?module=contract&action=getcontractcreation&contractaddresses={TOKEN_ADDRESS}&apikey={random.choice(random_ETHERSCAN_API)}"
        ).text)["result"]
        
        contract_creator = get_contract_creator[0]['contractCreator']
        return contract_creator
        

    def get_token_supply(self, TOKEN_ADDRESS):
        random_ETHERSCAN_API = [ETHERSCAN_API_KEY, EHTERSCAN_API_KEY_LV]

        get_supply = json.loads(requests.get(
            f"https://api.etherscan.io/api?module=stats&action=tokensupply&contractaddress={TOKEN_ADDRESS}&apikey={random.choice(random_ETHERSCAN_API)}"
        ).text)["result"]

        total_supply = str(get_supply)

        return total_supply

    def init_etherscan(self, TOKEN_ADDRESS, PAIR_ADDRESS):
        
            time.sleep(1)
            token_name, token_symbol = self.build_url(TOKEN_ADDRESS)
            time.sleep(7)
            try:
                creator_eth_balance, creator_address = self.creator_balance(TOKEN_ADDRESS)
                
                token_supply = self.get_token_supply(TOKEN_ADDRESS)
            except:
                creator_eth_balance, creator_address, token_supply = "", "", ""
            
            token_url = f"https://etherscan.io/address/{TOKEN_ADDRESS}"
            build_dexscreener = "https://dexscreener.com/ethereum/" + PAIR_ADDRESS
            now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            token_info = {
                    "launch_date": now,
                    "token_address": TOKEN_ADDRESS,
                    "pair_address": PAIR_ADDRESS,
                    "token_name": token_name,
                    "token_symbol": token_symbol,
                    "token_supply": token_supply,
                    "creator_address": creator_address,
                    "creator_eth_balance": creator_eth_balance,
                    "token_url": token_url,
                    "dexcreener": build_dexscreener
            }
            InsertDbJson().mysqlConnector(
                now,
                TOKEN_ADDRESS,
                PAIR_ADDRESS,
                token_name,
                token_symbol,
                token_supply,
                creator_address,
                creator_eth_balance,
                token_url,
                build_dexscreener
            )

            return token_info
        
class SyncToken():
    def handle_event(self, event):
        token_address_args = json.loads(Web3.toJSON(event))["args"]
        
        if token_address_args["token0"] != "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2" and token_address_args["token1"] == "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2":
            TOKEN_ADDRESS = token_address_args["token0"].replace(' ', '')
            PAIR_ADDRESS = token_address_args["pair"].replace(' ', '')

            print(json.loads(Web3.toJSON(event)))
            time.sleep(3)
            token_info = FindEtherscan().init_etherscan(TOKEN_ADDRESS, PAIR_ADDRESS)

            time.sleep(1)
            
            return token_info
            
        elif token_address_args["token1"] != "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2" and token_address_args["token0"] == "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2":
            TOKEN_ADDRESS = token_address_args["token1"].replace(' ', '')
            PAIR_ADDRESS = token_address_args["pair"].replace(' ', '')
            
            print(json.loads(Web3.toJSON(event)))
            time.sleep(3)
            token_info = FindEtherscan().init_etherscan(TOKEN_ADDRESS, PAIR_ADDRESS)

            time.sleep(1)

            return token_info

        else:
            pass
        

    async def log_loop(self, event_filter, poll_interval):
        while True:
            for PairCreated in event_filter.get_new_entries():
                
                self.handle_event(PairCreated)
                
                await asyncio.sleep(poll_interval)
            
    def main(self):
        loop = asyncio.get_event_loop()
        
        for url in random_infura:
            try:
                print(f"GOOD INFURA API - {url}")
                web3 = Web3(Web3.HTTPProvider(url))
                contract = web3.eth.contract(address=uniswap_factory, abi=uniswap_factory_abi)
                
                event_filter = contract.events.PairCreated.createFilter(fromBlock='latest')
                loop.run_until_complete(
                    asyncio.gather(
                        self.log_loop(event_filter, 2)))
                break
            except:
                print(f"ERROR - {url}")
                continue
                
        loop.close()     

if __name__ == '__main__':
    SyncToken().main()