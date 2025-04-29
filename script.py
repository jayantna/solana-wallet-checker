from solana.keypair import Keypair
from solana.rpc.api import Client
from solana.rpc.async_api import AsyncClient
from solana.publickey import PublicKey
from solana.rpc.types import TokenAccountOpts
import asyncio

# Define the Solana RPC endpoint (you can use https://api.mainnet-beta.solana.com or a testnet URL)
RPC_URL = "https://api.devnet.solana.com"  # Change to "https://api.mainnet-beta.solana.com" for mainnet

# Function to derive multiple addresses from a base keypair
def derive_addresses(base_keypair: Keypair, count: int):
    derived_addresses = []
    for i in range(count):
        # Derive a new keypair using a seed based on the base public key and an index
        seed = f"{base_keypair.public_key}{i}".encode("utf-8")
        derived_keypair = Keypair.from_seed(seed[:32])  # Ensure the seed is 32 bytes
        derived_addresses.append(derived_keypair.public_key)
    return derived_addresses

# Function to check balances of multiple addresses
async def check_balances(addresses):
    client = AsyncClient(RPC_URL)
    balances = {}
    for address in addresses:
        try:
            response = await client.get_balance(PublicKey(address))
            balances[address] = response['result']['value'] / 1e9  # Convert lamports to SOL
        except Exception as e:
            balances[address] = f"Error: {e}"
    await client.close()
    return balances

async def main():
    # Step 1: Generate a base wallet
    base_wallet = Keypair.generate()
    print(f"Base Wallet Address: {base_wallet.public_key}")

    # Step 2: Derive multiple addresses from the base wallet
    num_addresses = 5  # Number of derived addresses
    derived_addresses = derive_addresses(base_wallet, num_addresses)
    print(f"Derived Addresses: {[str(addr) for addr in derived_addresses]}")

    # Step 3: Check balances of the derived addresses
    balances = await check_balances(derived_addresses)
    for addr, balance in balances.items():
        print(f"Address: {addr}, Balance: {balance} SOL")

# Run the script
if __name__ == "__main__":
    asyncio.run(main())
