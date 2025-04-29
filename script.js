const {
  Connection,
  Keypair,
  PublicKey,
  clusterApiUrl,
} = require('@solana/web3.js');

// Define the Solana RPC endpoint
const RPC_URL = clusterApiUrl('mainnet-beta'); // Use 'mainnet-beta' for mainnet

// Function to derive multiple addresses from a base Keypair
const deriveAddresses = (baseKeypair, count) => {
  const derivedAddresses = [];
  for (let i = 0; i < count; i++) {
    // Create a deterministic seed based on the base public key and an index
    const seed = Buffer.from(baseKeypair.publicKey.toString() + i).slice(0, 32);
    const derivedKeypair = Keypair.fromSeed(seed);
    derivedAddresses.push(derivedKeypair.publicKey);
  }
  return derivedAddresses;
};

// Function to check balances of multiple addresses
const checkBalances = async (connection, addresses) => {
  const balances = {};
  for (const address of addresses) {
    try {
      const balance = await connection.getBalance(new PublicKey(address));
      balances[address.toString()] = balance / 1e9; // Convert lamports to SOL
    } catch (err) {
      balances[address.toString()] = `Error: ${err.message}`;
    }
  }
  return balances;
};

const main = async () => {
  // Create a connection to the Solana network
  const connection = new Connection(RPC_URL, 'confirmed');

  // Step 1: Generate a base wallet
  const baseWallet = Keypair.generate();
  console.log(`Base Wallet Address: ${baseWallet.publicKey.toString()}`);

  // Step 2: Derive multiple addresses from the base wallet
  const numAddresses = 5; // Number of derived addresses
  const derivedAddresses = deriveAddresses(baseWallet, numAddresses);
  console.log(`Derived Addresses: ${derivedAddresses.map((addr) => addr.toString())}`);

  // Step 3: Check balances of the derived addresses
  const balances = await checkBalances(connection, derivedAddresses);
  console.log('Balances:', balances);
};

main().catch((err) => console.error(err));
