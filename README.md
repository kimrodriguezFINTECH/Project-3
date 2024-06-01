# Self Generate Event NFT for Sale 
## Background
Event management has always been a complex and multi-faceted industry, involving numerous stakeholders, significant logistical challenges, and various layers of security and verification. Traditional methods of ticketing often face problems such as fraud, counterfeiting, and unauthorized reselling, which can significantly impact the experience of event organizers and attendees alike.
* Fraud and Counterfeiting: Ticket fraud is a significant issue, with consumers losing millions of dollars annually to counterfeit tickets. A report from Verified.org explains how scammers often sell fake tickets to high-demand events, leaving buyers without access and out of pocket [1].
* Unauthorized Reselling: Unauthorized ticket reselling (scalping) leads to significant losses for both event organizers and consumers. This problem is highlighted by IdentityIQ, which notes that ticket scams are prevalent for sold-out events due to high demand [2].
With the advent of blockchain technology, there is a unique opportunity to revolutionize the event ticketing process. Non-Fungible Tokens (NFTs) provide a secure, transparent, and immutable way to represent ownership of digital assets. By leveraging NFTs for event tickets, we can address many of the longstanding issues in the ticketing industry.
## Objective
1. Eliminate Fraud and Counterfeiting: Traditional paper or digital tickets are susceptible to fraud and counterfeiting. NFTs, being unique and verifiable on the blockchain, can ensure that each ticket is authentic and tamper-proof. According to Forbes, blockchain's immutability and transparency significantly reduce fraud in ticketing [3].
2. Prevent Unauthorized Reselling: NFT-based tickets can include smart contract rules that restrict or control the resale of tickets. This can prevent scalping and ensure tickets are sold at fair prices. TechCrunch discusses how smart contracts can enforce resale rules automatically, making them ideal for this purpose [4].
3. Enhance Attendee Experience: NFT tickets can offer a richer experience by including additional digital content, such as event memorabilia, exclusive access, or future benefits, all embedded within the NFT. CoinDesk highlights various case studies where NFTs have enhanced fan engagement in sports and entertainment [5].
4. Empower Event Organizers: By decentralizing the ticketing process, event organizers have greater control over the distribution and pricing of tickets, reducing dependency on third-party vendors and increasing their revenue potential. Harvard Business Review elaborates on the benefits of decentralization in ticketing [6].Recently, current events have shown the importance of potential soutions to this issue. The follwing are some of the news relating to these issues:
   
   "Live Nation, Ticketmaster’s parent company, sued in groundbreaking monopoly lawsuit" | CNN Businesshu May 23, 2024
   "US sues Ticketmaster owner Live Nation and seeks break-up of alleged monopoly" |  The Guardian May 23, 2024

   "Mention the news"^

## Hypothesis 
Create a Streamlit-based web application that allows users to generate AI images or upload their own images to create NFTs (Non-Fungible Tokens). These NFTs serve as digital tickets that users can sell, and others can purchase. The app will also display the transaction history for each NFT.

## Files
* app.py
* NFT_Ticket_Transferrable.sol
* contract_abi.json
* env.txt 

## Install Packages
* `os` for interacting with the operating system.
* `streamlit` to create the web app interface.
* `json` for transmitting data in web applications 
* `requests` for interacting with web APIs
* `pandas` for data manipulation
* `OpenAI` API for generating images based on user prompts.
* `Pinata` for images on IPFS and retrieves IPFS hashes.
* `Solidity` for Smart contract language used to create and manage NFTs.
* `Remix` for Online IDE for writing and deploying Solidity contracts.
* `Web3.py` Python library for interacting with Ethereum.
* `Ganache` Personal Ethereum wallet, used to simulate transactions.
* `Metaask` Browser extension wallet for managing Ethereum accounts and transactions.

## Key Functionalities

1. NFT Creation:

User Inputs:

- Prompt for AI Image Generation: Users can enter a text prompt to generate an image using OpenAI's API.

- Image Upload: Users can upload their own images if they do not want to use the AI-generated ones.

- Number of Copies: Users specify how many copies/tickets of the NFT they want to create.

- Price per Ticket: Users set the price for each NFT/ticket.

- Ethereum Address: Users provide their Ethereum address to receive funds from sales.

- Image Generation: The app uses the OpenAI API to generate an image based on the user's prompt if they choose not to upload their own image.

- Image Storage: The generated or uploaded image is stored on IPFS via Pinata, and an IPFS hash is obtained.

- NFT Minting: A Solidity smart contract is used to mint NFTs with the IPFS hash as metadata. This contract is deployed on the Ethereum blockchain, and interactions are handled using Web3.py.

2. Marketplace:

- Listing NFTs: The app displays available NFTs with details such as cover art, number of copies, price, and transaction history.

- Purchasing NFTs: Users can input their Ethereum address to purchase NFTs. Transactions are processed using Web3.py, and ownership is transferred through the smart contract.

- Transaction History: The app shows the transaction history for each NFT, including previous sale prices.

  
## FRONT END OF CODE 

We started off with the Pinata Configuration: `pinata_api_key = os.getenv('PINATA_API_KEY')`
* Our API key ensures our sensitive information is securely managed, enhances flexibility across different environments, and is used for best practices regarding application configuration.

Using Web3 Configuration provided us the flexibility to run the application in different environments without changing the codebase. 
* Hence, our same code can be used with different blockchain networks by simply changing the environment variable. For example we used ganache as a testing tool for Ethereum-based blockchain. 

`ganache_url = os.getenv('GANACHE_URL')`

`web3 = Web3(Web3.HTTPProvider(ganache_url))`

In order for us to be able to sell and buy for this event we used Metamask as our source of currency exchange. Hence, connecting MetaMask to a smart contract involves several steps, from setting up MetaMask itself to interacting with the smart contract on the Ethereum blockchain. Below is a step-by-step guide:

1. Create a Wallet: Open MetaMask, and follow the instructions to create a new wallet. 
2. Fund Your Wallet: We used Ether (ETH) in our wallet to pay for gas fees which in our case we bought ETH directly from MetaMask.
3. Smart Contract: We ensured MetaMask is connected to the same network where our contract is deployed

`contract_address = Web3.to_checksum_address(os.getenv('CONTRACT_ADDRESS'))`

4. Install Web3.js or Ethers.js: These libraries help us interact with the Ethereum blockchain from our frontend.

`contract = web3.eth.contract(address=contract_address, abi=contract_abi)`

## BACK END OF CODE  


## NFT Ticket
For the Streamlit's session state is used to store variables that need to persist across reruns of the app. 

`nfts` : A list to store NFT data.

`image_url` : The URL of the image to be used for the NFT.

`num_copies` : The number of copies for each NFT ticket, defaulting to 1.

`price_per_ticket` : The price for each NFT ticket, defaulting to 0.01 ETH.

`eth_address` : The Ethereum address for the transaction, initialized as an empty string.


Create NFT Ticket:
When the "Create NFT Ticket" button is clicked, a new NFT dictionary is created with the input values and appended to the `st.session_state['nfts']` list.
A success message is displayed.

Display NFTs:

The created NFTs are displayed with their image, number of copies, price per ticket, and Ethereum address.
`image_option = st.sidebar.radio('Select Image Option', ('Generate via AI', 'Upload Image'))`

## Technical Explanation Demo 
Step 1: Generating an Image

• User Input for Image Generation:
	◦ The user enters a prompt for the image they want to generate.
	◦ The user clicks the "Generate Image" button.
 
![sampleimagegenerated052824](https://github.com/kimrodriguezFINTECH/Project-3/assets/152752672/0a8c1824-7aaf-4787-a71f-85027daeaeff)

• Calling OpenAI API:
	◦ The generate_image(prompt) function is called.
	◦ The function constructs a request to the OpenAI API to generate an image based on the provided prompt.
	◦ The API key is retrieved from the environment variables (OPENAI_API_KEY).
(Insert Image)

• Displaying Generated Image:
	◦ If the image generation is successful, the URL of the generated image is stored in st.session_state['image_url'].
	◦ The image is displayed on the Streamlit UI using st.image(image_url).
(Insert Image)

Step 2: Selecting Quantity, Price and Ethereum Address for Receiving
 
• The user selects the number of copies they want to create (num_copies).
• The user sets the price per ticket in Ether (price_per_ticket).
• The user provides their Ethereum address to receive funds from sales of ticket(NFT) (eth_address).
(Insert Image) 

Step 3: Creating the NFT

• Creating NFT Metadata:
	◦ The st.button("Create NFT") click triggers the process.
	◦ The metadata for the NFT, including the image URL, is prepared in JSON format.
(Insert Image) 

• Pinning Metadata to IPFS:
	◦ The pin_json_to_ipfs function is called to pin the NFT metadata to IPFS via Pinata.
	◦ The Pinata API key and secret key are retrieved from the .env.
	◦ The metadata is sent to Pinata, which returns an IPFS hash (IpfsHash).
(Insert Image)

• Minting the NFT:
	◦ The IPFS hash (token_uri) is used as the token URI for the NFT.
	◦ The smart contract's registerTicket function is called to mint the NFT on the blockchain.
	◦ The user's Ethereum address and token URI are passed as arguments to the registerTicket function.
(Insert Image)

• Storing NFT Details:
	◦ The NFT details (token ID, image URL, price, owner) are stored in st.session_state['nfts'] to be displayed in the marketplace.
	◦ The marketplace can then show all NFTs with their respective details.
(Insert Image) 

## References
Verified.org: "How to Avoid Fake Tickets to Events, Flights, and More". Available at: https://www.verified.org/articles/scams/fake-ticket-scams
IdentityIQ: "How to not Get Scammed Buying Tickets". Available at: https://www.identityiq.com/scams-and-fraud/how-to-not-get-scammed-buying-tickets/#:~:text=Avoid%20offers%20that%20seem%20%E2%80%9Ctoo,don't%20take%20the%20bait.
Forbes: "How Mobile Blockchain Ticketing Is Changing The Events Industry”. Available at: https://www.forbes.com/sites/forbesbusinesscouncil/2022/03/18/how-mobile-blockchain-ticketing-is-changing-the-events-industry/?sh=52c7926d683e
TechCrunch: "How NFT Ticketing is Reshaping Traditional Ticketing Systems?” Available at: https://www.mxicoders.com/how-nft-ticketing-is-reshaping-traditional-ticketing-systems/
CoinDesk: "Why We Need NFT Ticketing for Sports Events.” Available at: https://www.coindesk.com/layer2/2022/07/29/why-we-need-nft-ticketing-for-sports-events/#:~:text=Offering%20the%20potential%20for%20change,adding%20value%20for%20loyal%20fans
Harvard Business Review: "How Blockchain Is Changing Finance". Available at: https://hbr.org/2017/03/how-blockchain-is-changing-finance
