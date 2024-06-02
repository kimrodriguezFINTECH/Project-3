import os
from dotenv import load_dotenv
import streamlit as st
from web3 import Web3
import json
import requests
import openai
from streamlit_lottie import st_lottie
import pandas as pd
# Load environment variables
load_dotenv()

# Pinata Configuration
pinata_api_key = os.getenv('PINATA_API_KEY')
pinata_secret_api_key = os.getenv('PINATA_SECRET_API_KEY')
pinata_base_url = "https://api.pinata.cloud/"
ipfs_gateway_url = "https://gateway.pinata.cloud/ipfs/"

def pin_file_to_ipfs(file):
    url = pinata_base_url + "pinning/pinFileToIPFS"
    headers = {
        "pinata_api_key": pinata_api_key,
        "pinata_secret_api_key": pinata_secret_api_key
    }
    files = {'file': file}
    response = requests.post(url, files=files, headers=headers)
    return response.json()

def pin_json_to_ipfs(json_data):
    url = pinata_base_url + "pinning/pinJSONToIPFS"
    headers = {
        "Content-Type": "application/json",
        "pinata_api_key": pinata_api_key,
        "pinata_secret_api_key": pinata_secret_api_key
    }
    response = requests.post(url, json=json_data, headers=headers)
    return response.json()

def generate_image(prompt):
    api_key = os.getenv('OPENAI_API_KEY')
    url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024"
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        response_data = response.json()
        return response_data['data'][0]['url']
    else:
        error_response = response.json()
        if error_response.get('error', {}).get('code') == 'billing_hard_limit_reached':
            st.error("Error: Billing limit reached. Please check your OpenAI account billing settings.")
        else:
            st.error(f"Error: {response.status_code}")
            st.error(error_response)
        return None

# Web3 Configuration
ganache_url = os.getenv('GANACHE_URL')
st.write(f"Connecting to Ganache at {ganache_url}")  # Debugging line to check GANACHE_URL
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Ensure Web3 is connected
if not web3.is_connected():
    st.error("Web3 is not connected. Please ensure Ganache is running and the URL is correct.")
else:
    st.write("Web3 is connected.")

web3.eth.default_account = web3.eth.accounts[0]

# Convert contract address to checksum format
contract_address = Web3.to_checksum_address(os.getenv('CONTRACT_ADDRESS'))
with open('contract_abi.json') as f:
    contract_abi = json.load(f)
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Streamlit UI
st.title("NFT Ticketing System")

# Initialize session state for storing NFTs and form inputs
if 'nfts' not in st.session_state:
    st.session_state['nfts'] = []
if 'image_url' not in st.session_state:
    st.session_state['image_url'] = None
if 'num_copies' not in st.session_state:
    st.session_state['num_copies'] = 1
if 'price_per_ticket' not in st.session_state:
    st.session_state['price_per_ticket'] = 0.01
if 'eth_address' not in st.session_state:
    st.session_state['eth_address'] = ""

# Sidebar for navigation
st.sidebar.title("Navigation")
option = st.sidebar.selectbox('Select an option', ('Create NFT', 'Marketplace', 'Resell NFT'))

if option == 'Create NFT':
    st.header("Create NFT Ticket")
    
    # Inputs for number of copies and price before image generation
    st.session_state['num_copies'] = st.number_input("Number of Copies", min_value=1, value=st.session_state['num_copies'])
    st.session_state['price_per_ticket'] = st.number_input("Price per Ticket (in Ether)", min_value=0.01, value=st.session_state['price_per_ticket'])
    url = "https://www.coinbase.com/converter/eth/usd"
    st.markdown(f"For the USD Equivalent you may visit: {url}")
    st.session_state['eth_address'] = st.text_input("Your Ethereum Address", value=st.session_state['eth_address'])

    # Sidebar options for image generation or upload
    image_option = st.sidebar.radio('Select Image Option', ('Generate via AI', 'Upload Image'))

    if image_option == 'Generate via AI':
        eventname = st.text_input("Please enter the name of the event")
        eventdate = st.date_input("Please enter the date of the event")
        st.write("Your event is:", eventdate)
        eventtime = st.time_input("Time of the event")
        st.write("Your event is set for", eventtime)
        eventloc = st.text_input("Please enter the name of the location")
        eventaddress = st.text_input("Please enter the address of the location")
        descriptionevent = st.text_input("Please enter a description of the image to be generated for the event. e.g. Orpheus playing guitar with the Golden Gate bridge at night as background")
        
        if st.button("Generate Image"):
            prompt = f"Create a flyer of {descriptionevent} for an event with title {eventname}, on {eventdate}, at {eventtime} hrs at {eventloc} {eventaddress}"
            st.write("Generating image with prompt:", prompt)
            image_url = generate_image(prompt)
            if image_url:
                st.image(image_url)
                st.session_state['image_url'] = image_url
                st.write(f"Generated image URL: {image_url}")
            else:
                st.error("Failed to generate image.")

    elif image_option == 'Upload Image':
        uploaded_file = st.sidebar.file_uploader("Choose an image...", type=["jpg", "png"])
        if uploaded_file is not None:
            response = pin_file_to_ipfs(uploaded_file)
            if 'IpfsHash' in response:
                ipfs_hash = response['IpfsHash']
                st.session_state['image_url'] = ipfs_gateway_url + ipfs_hash
                st.image(st.session_state['image_url'])
                st.write(f"Uploaded image IPFS hash: {ipfs_hash}")
            else:
                st.error("Failed to upload image to IPFS.")

    if st.session_state['image_url']:
        st.image(st.session_state['image_url'])
        
    if st.button("Create NFT"):
        if st.session_state['image_url']:
            image_url = st.session_state['image_url']
            response = pin_json_to_ipfs({'image': image_url})
            if 'IpfsHash' in response:
                token_uri = response['IpfsHash']
                price_in_wei = web3.to_wei(st.session_state['price_per_ticket'], 'ether')
                num_copies = st.session_state['num_copies']
                tx_hash = contract.functions.registerTicket(Web3.to_checksum_address(st.session_state['eth_address']), token_uri, price_in_wei, num_copies).transact({'from': web3.eth.default_account, 'gas': 1000000})
                receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
                st.write(f"Transaction successful with hash: {receipt.transactionHash.hex()}")

                # Store NFT details in session state
                nft = {
                    'token_id': len(st.session_state['nfts']),
                    'image_url': image_url,
                    'price': st.session_state['price_per_ticket'],
                    'owner': web3.eth.default_account,
                    'copies': num_copies,
                    'transaction_history': [{'owner': web3.eth.default_account, 'price': st.session_state['price_per_ticket']}]
                }
                st.session_state['nfts'].append(nft)
                st.write("NFT created and added to marketplace.")
            else:
                st.error("Failed to pin JSON to IPFS.")
        else:
            st.error("No image URL found. Please generate or upload an image first.")

elif option == 'Marketplace':
    st.header("NFT Marketplace")
    if not st.session_state['nfts']:
        st.write("No NFTs available in the marketplace.")
    else:
        cols = st.columns(3)  # Adjust the number of columns as needed
        for i, nft in enumerate(st.session_state['nfts']):
            with cols[i % 3]:
                st.image(nft['image_url'], width=200)
                st.write(f"**Token ID:** {nft['token_id']}")
                st.write(f"**Price:** {nft['price']} Ether")
                st.write(f"**Owner:** {nft['owner']}")
                try:
                    copies_available = contract.functions.getCopies(nft['token_id']).call()
                    st.write(f"**Copies Available:** {copies_available}")
                except Exception as e:
                    st.error(f"Failed to fetch copies: {e}")
                st.write("**Transaction History:**")
                for transaction in nft['transaction_history']:
                    #st.write(f" - Owner: {transaction['owner']}, Price: {transaction['price']} Ether")
                    dictionary=[[transaction["owner"],transaction['price']]]
                    df=pd.DataFrame(dictionary,columns=["Owner", "Price"])
                    st.write(df) 
                buyer_eth_address = st.text_input(f"Your Ethereum Address for NFT {nft['token_id']}", key=f"buyer_{nft['token_id']}")
                if st.button(f"Buy NFT {nft['token_id']}", key=f"buy_{nft['token_id']}"):
                    if buyer_eth_address:
                        try:
                            st.write(f"Buying NFT {nft['token_id']} for {nft['price']} Ether from {buyer_eth_address}")
                            price_in_wei = web3.to_wei(nft['price'], 'ether')
                            tx_hash = contract.functions.buyTicket(nft['token_id']).transact({'from': Web3.to_checksum_address(buyer_eth_address), 'value': price_in_wei, 'gas': 1000000})
                            receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
                            st.write(f"Transaction successful with hash: {receipt.transactionHash.hex()}")
                            # Update NFT ownership and copies
                            nft['owner'] = Web3.to_checksum_address(buyer_eth_address)
                            nft['copies'] -= 1
                            nft['transaction_history'].append({'owner': Web3.to_checksum_address(buyer_eth_address), 'price': nft['price']})
                        except Exception as e:
                            st.error(f"Transaction failed: {e}")

elif option == 'Resell NFT':
    st.header("Resell Your NFT")
    st.session_state['eth_address'] = st.text_input("Enter your Ethereum Address", value=st.session_state['eth_address'])

    if st.session_state['eth_address']:
        web3.eth.default_account = Web3.to_checksum_address(st.session_state['eth_address'])
    
    owned_nfts = [nft for nft in st.session_state['nfts'] if nft['owner'] == web3.eth.default_account]
    if not owned_nfts:
        st.write("You don't own any NFTs.")
    else:
        for nft in owned_nfts:
            st.image(nft['image_url'], width=200)
            st.write(f"**Token ID:** {nft['token_id']}")
            try:
                copies_available = contract.functions.getCopies(nft['token_id']).call()
                st.write(f"**Copies Available:** {copies_available}")
            except Exception as e:
                st.error(f"Failed to fetch copies: {e}")
            new_price = st.number_input(f"New Price for NFT {nft['token_id']} (in Ether)", min_value=0.01, value=nft['price'])
            if st.button(f"Resell NFT {nft['token_id']}"):
                try:
                    new_price_in_wei = web3.to_wei(new_price, 'ether')
                    tx_hash = contract.functions.updateTicketPrice(nft['token_id'], new_price_in_wei).transact({'from': web3.eth.default_account, 'gas': 1000000})
                    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
                    st.write(f"NFT {nft['token_id']} is now listed for {new_price} Ether.")
                    nft['price'] = new_price
                except Exception as e:
                    st.error(f"Failed to resell NFT: {e}")
