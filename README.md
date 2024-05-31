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

## Hypothesis 
We believe we can create our own application that can help event organizers create their own event flyer with the time date and location of the even with the help of AI technology. Our application will give the event creator full control of the number of tickets that will be sold including the option of buying and selling the ticket amongst other customers.

## Files
* app.py
* NFT_Ticket_Transferrable.sol
* contract_abi.json
* env.txt 

## Install Packages
* `os` for interacting with the operating system.
* `streamlit` for connecting to web applications
* `json` for transmitting data in web applications 
* `requests` for interacting with web APIs
* `openai` for accessing and integrating AI models into our applications.
* `pandas` for data manipulation
  
## Setting Up
Ganache and Metamask Set Up

We started off with the Pinata Configuration: `pinata_api_key = os.getenv('PINATA_API_KEY')`
* Our API key ensures our sensitive information is securely managed, enhances flexibility across different environments, and is used for best practices regarding application configuration.

Using Web3 Configuration provided us the flexibility to run the application in different environments without changing the codebase. 
* Hence, our same code can be used with different blockchain networks by simply changing the environment variable. For example we used ganache as a testing tool for Ethereum-based blockchain. 

`ganache_url = os.getenv('GANACHE_URL')`

`web3 = Web3(Web3.HTTPProvider(ganache_url))`

Connecting MetaMask to a smart contract involves several steps, from setting up MetaMask itself to interacting with the smart contract on the Ethereum blockchain. Below is a step-by-step guide:

1. Create a Wallet: Open MetaMask, and follow the instructions to create a new wallet. 
2. Fund Your Wallet: We used Ether (ETH) in our wallet to pay for gas fees which in our case we bought ETH directly from MetaMask.
3. Smart Contract: We ensured MetaMask is connected to the same network where our contract is deployed `contract_address = Web3.to_checksum_address(os.getenv('CONTRACT_ADDRESS'))`
4. Install Web3.js or Ethers.js: These libraries help you interact with the Ethereum blockchain from your frontend. `contract = web3.eth.contract(address=contract_address, abi=contract_abi)`

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

![sampleimagegenerated052824](https://github.com/kimrodriguezFINTECH/Project-3/assets/152752672/0a8c1824-7aaf-4787-a71f-85027daeaeff)



## References
Verified.org: "How to Avoid Fake Tickets to Events, Flights, and More". Available at: https://www.verified.org/articles/scams/fake-ticket-scams
IdentityIQ: "How to not Get Scammed Buying Tickets". Available at: https://www.identityiq.com/scams-and-fraud/how-to-not-get-scammed-buying-tickets/#:~:text=Avoid%20offers%20that%20seem%20%E2%80%9Ctoo,don't%20take%20the%20bait.
Forbes: "How Mobile Blockchain Ticketing Is Changing The Events Industry”. Available at: https://www.forbes.com/sites/forbesbusinesscouncil/2022/03/18/how-mobile-blockchain-ticketing-is-changing-the-events-industry/?sh=52c7926d683e
TechCrunch: "How NFT Ticketing is Reshaping Traditional Ticketing Systems?” Available at: https://www.mxicoders.com/how-nft-ticketing-is-reshaping-traditional-ticketing-systems/
CoinDesk: "Why We Need NFT Ticketing for Sports Events.” Available at: https://www.coindesk.com/layer2/2022/07/29/why-we-need-nft-ticketing-for-sports-events/#:~:text=Offering%20the%20potential%20for%20change,adding%20value%20for%20loyal%20fans
Harvard Business Review: "How Blockchain Is Changing Finance". Available at: https://hbr.org/2017/03/how-blockchain-is-changing-finance
