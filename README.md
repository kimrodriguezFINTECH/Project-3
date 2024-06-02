<img width="1291" alt="Screenshot 2024-06-01 at 7 45 44 PM" src="https://github.com/kimrodriguezFINTECH/Project-3/assets/152752672/2734ebc0-3abb-4581-b2bf-c014b492f0d5">

# Self Generate Event NFT for Sale
## Background
Event management has always been a complex and multi-faceted industry, involving numerous stakeholders, significant logistical challenges, and various layers of security and verification. Traditional methods of ticketing often face problems such as fraud, counterfeiting, and unauthorized reselling, which can significantly impact the experience of event organizers and attendees alike. For example, The Department of Justice has filed an antitrust lawsuit against Live Nation, aiming to break up the entertainment giant, Ticketmaster. The lawsuit, supported by 29 states and the District of Columbia, accuses Live Nation of monopolistic practices that undermine competition in the live events industry. The DOJ claims that Live Nation (Ticketmaster) forces consumers to pay higher prices and manipulates ticketing technology. Additionally, the company allegedly uses its market power to impose barriers that prevent competitors from entering or expanding within the industry​. The lawsuit seeks structural changes to break up the company's monopoly and restore competition to benefit fans, artists, and smaller promoters​. Hence, the structure of our application aims to completely stop or discourage these types of practices that Live Nation has displayed within this lawsuit. 

## Objective
Create a Streamlit-based web application that allows users to generate AI images or upload their own images to create NFTs (Non-Fungible Tokens). These NFTs serve as digital tickets that users can sell, and others can purchase. The app will also display the transaction history for each NFT.

Throughout our application we aim to: 

1. Eliminate Fraud and Counterfeiting: Traditional paper or digital tickets are susceptible to fraud and counterfeiting. NFTs, being unique and verifiable on the blockchain, can ensure that each ticket is authentic and tamper-proof. According to Forbes, blockchain's immutability and transparency significantly reduce fraud in ticketing [3].
2. Prevent Unauthorized Reselling: NFT-based tickets can include smart contract rules that restrict or control the resale of tickets. This can prevent scalping and ensure tickets are sold at fair prices. TechCrunch discusses how smart contracts can enforce resale rules automatically, making them ideal for this purpose [4].
3. Enhance Attendee Experience: NFT tickets can offer a richer experience by including additional digital content, such as event memorabilia, exclusive access, or future benefits, all embedded within the NFT. CoinDesk highlights various case studies where NFTs have enhanced fan engagement in sports and entertainment [5].
4. Empower Event Organizers: By decentralizing the ticketing process, event organizers have greater control over the distribution and pricing of tickets, reducing dependency on third-party vendors and increasing their revenue potential.

## Files
* app.py
* NFT_Ticket_Transferrable.sol
* contract_abi.json
* env.txt 

## Install Packages/Imports 
* `os` for interacting with the operating system
* `streamlit` to create the web app interface
* `json` for transmitting data in web applications 
* `requests` for interacting with web APIs
* `pandas` for data manipulation
* `python-dotenv` for environment-specific variables:
* `OpenAI` API for generating images based on user prompts
* `Pinata` for images on IPFS and retrieves IPFS hashes
* `Solidity` for Smart contract language used to create and manage NFTs
* `Remix` for Online IDE for writing and deploying Solidity contracts
* `Web3.py` Python library for interacting with Ethereum
* `Ganache` Personal Ethereum wallet, used to simulate transactions
* `Metaask` Browser extension wallet for managing Ethereum accounts and transactions
* "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol"

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
### Connecting to Ganache & Metamask
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

### Streamlit UI
We then connected to streamlit in order to store data related to our NFTs, such as the list of NFTs, images, number of copies, price per ticket, and Ethereum address for the trasaction history. This ensures that the variables are available and have default values throughout the app's session, allowing the creator to manage and retain user inputs or manage the NFTs in session.
  
`if 'nfts' not in st.session_state:
    st.session_state['nfts'] = []`
   
`if 'image_url' not in st.session_state:
    st.session_state['image_url'] = None`
    
`if 'num_copies' not in st.session_state:
    st.session_state['num_copies'] = 1`
    
`if 'price_per_ticket' not in st.session_state:
    st.session_state['price_per_ticket'] = 0.01`
    
`if 'eth_address' not in st.session_state:
    st.session_state['eth_address'] = ""`

### Sidebar Navigation
A dropdown menu in the sidebar allows the creator and customer to choose between three options: 'Create NFT', 'Marketplace', and 'Resell NFT'.
For example when the creator selects 'Create NFT', the main area of the app displays a header with the text "Create NFT Ticket". This indicates that the app will present the user with tools or forms to create an NFT ticket in this section.

`st.sidebar.title("Navigation")`
option = st.sidebar.selectbox('Select an option', ('Create NFT', 'Marketplace', 'Resell NFT'))`

The Sidebar Navigation also gives the creator the option to generate an AI image flyer of the event that will inlude the following:

* name of the event
* date of the event
* time of the event
* name of the location
* address of the location
* description of the image to be generated for the event
  
`if st.button("Generate Image"):`
            `prompt = f"Create a flyer of {descriptionevent} for an event with title {eventname}, on {eventdate}, at {eventtime} hrs at {eventloc} {eventaddress}"`

* Note: The creator can also upload their own personal flyer if they do not want to use the AI generator for the event

`elif image_option == 'Upload Image':`
        `uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png"])`


## BACK END OF CODE  
Our Solidity code defines a smart contract for an NFT-based ticketing system using the ERC721 standard, extended with additional functionalities. 

The provided Solidity code defines a smart contract for an NFT-based ticketing system using the ERC721 standard, extended with additional functionalities. Here is a step-by-step explanation of what each part of the code does:

1. The ERC721 Contract imports the ERC721Full contract from OpenZeppelin, a library of secure smart contract components. ERC721Full is a complete implementation of the ERC721 standard for non-fungible tokens (NFTs).
   
"import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";"

2. We then declare a new contract named `NFTTicket` which inherits from ERC721Full, gaining all the functionalities of the ERC721 standard. A struct named Ticket is defined to hold information about each ticket, including its `tokenId`, `price`, and the `number of copies available`

`contract NFTTicket is ERC721Full {struct Ticket { uint256 tokenId; uint256 price; uint256 copies;}`

3. Stating the Variables 
* `tickets` holds all the tickets that will be available to buy
* `ownershipHistory` will track the ownership history of each ticket by the `tokenId`
* `priceHistory` records the price history of each ticket by the `tokenId` for later use if the customer want to resell the ticket later 

`Ticket[] public tickets;`
`mapping(uint256 => address[]) public ownershipHistory;`
`mapping(uint256 => uint256[]) public priceHistory;`

4. Event
The `TicketCreated` and `TicketTransferred` are events when a ticket is created or transferred. These events are indexed for easier querying in the event logs or transaction history.

`event TicketCreated(uint256 indexed tokenId, address indexed owner, uint256 price, uint256 copies);`
`event TicketTransferred(uint256 indexed tokenId, address indexed from, address indexed to, uint256 price);`

5. Regsitering a New Ticket
This is when a new tokenId is generated based on the current quantity of tokens available. The new token is then assigned to the owner and price histories are initialized at this point and time.

`function registerTicket(address owner, string memory tokenURI, uint256 price, uint256 copies) public returns (uint256) {`
        `uint256 tokenId = totalSupply();`
        `_mint(owner, tokenId);`
        `_setTokenURI(tokenId, tokenURI);`
        `tickets.push(Ticket(tokenId, price, copies));`
        `ownershipHistory[tokenId].push(owner);`
        `priceHistory[tokenId].push(price);`
        `emit TicketCreated(tokenId, owner, price, copies);`
        `return tokenId;}`
	
6. Buying the Ticket 
The buyTicket allows users to purchase a ticket by retrieving the ticket by tokenId. It then checks if the payment is sufficient and if there are copies available. This allows the transfers of the token from the previous owner to the new owner. Additionally, it updates the ownership and price histories when the payment is recieved by the previous owner.

`function buyTicket(uint256 tokenId) public payable {`

        `Ticket storage ticket = tickets[tokenId];`
	
        `require(msg.value >= ticket.price, "Insufficient funds");`
	
        `require(ticket.copies > 0, "No more copies available");`

        `address previousOwner = ownerOf(tokenId);`
	
        `address newOwner = msg.sender;`

        `_transferFrom(previousOwner, newOwner, tokenId);`

        `ownershipHistory[tokenId].push(newOwner);`
	
        `priceHistory[tokenId].push(msg.value);`

        `ticket.copies--;`

        `address(uint160(previousOwner)).transfer(msg.value);`

        `emit TicketTransferred(tokenId, previousOwner, newOwner, msg.value);}`

7. Ownership and Price History
* The `getOwnershipHistory` returns the ownership history of a ticket given its `tokenId`

`function getOwnershipHistory(uint256 tokenId) public view returns (address[] memory) {return ownershipHistory[tokenId];}`

* The `getPriceHistory` returns the price history of a ticket given its `tokenId`

`function getPriceHistory(uint256 tokenId) public view returns (uint256[] memory) {return priceHistory[tokenId];}`

8. Copies
The `getCopies` returns the number of remaining copies for a given ticket by `tokenId`

`function getCopies(uint256 tokenId) public view returns (uint256) {return tickets[tokenId].copies;}`

## Technical Explanation Demo 
Step 1: Generating an Image

• User Input for Image Generation:

	◦ The user enters a prompt for the image they want to generate.
 
	◦ The user clicks the "Generate Image" button.
 
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


## Conclusion
In conclusion, our application leverages the power of NFTs and blockchain technology to address and resolve the prevalent issues in traditional ticketing systems. Additionally, our applicaiton aligns with recent developments and industry demands for a more secure, transparent, and user-centric solutions in event management. This ensures a fairer and more enjoyable experience for all stakeholders involved.

## References
* https://www.cnn.com/2024/05/23/tech/live-nation-antitrust-violations-doj-lawsuit/index.html

* https://www.theguardian.com/business/article/2024/may/23/live-nation-ticketmaster-lawsuit

* Verified.org: "How to Avoid Fake Tickets to Events, Flights, and More". Available at: https://www.verified.org/articles/scams/fake-ticket-scams
  
* IdentityIQ: "How to not Get Scammed Buying Tickets". Available at: https://www.identityiq.com/scams-and-fraud/how-to-not-get-scammed-buying tickets/#:~:text=Avoid%20offers%20that%20seem%20%E2%80%9Ctoo,don't%20take%20the%20bait.
  
* Forbes: "How Mobile Blockchain Ticketing Is Changing The Events Industry”. Available at: https://www.forbes.com/sites/forbesbusinesscouncil/2022/03/18/how-mobile-blockchain-ticketing-is-changing-the-events-industry/?sh=52c7926d683e
  
* TechCrunch: "How NFT Ticketing is Reshaping Traditional Ticketing Systems?” Available at: https://www.mxicoders.com/how-nft-ticketing-is-reshaping-traditional-ticketing-systems/
  
* CoinDesk: "Why We Need NFT Ticketing for Sports Events.” Available at: https://www.coindesk.com/layer2/2022/07/29/why-we-need-nft-ticketing-for-sports-events/#:~:text=Offering%20the%20potential%20for%20change,adding%20value%20for%20loyal%20fans

