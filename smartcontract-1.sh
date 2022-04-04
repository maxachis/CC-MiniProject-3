# Install python3 for this project
sudo apt-get install python3
# Install pip3 for package management
sudo apt install python3-pip

# Create a file to store nvm commands
touch ~/.bashrc

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.37.2/install.sh | bash

# Activate the commands
source ~/.bashrc

# install node 16.14.2 (which are supported by ganache)
nvm install --lts
node -v

# Install the Solidity Compiler
sudo add-apt-repository ppa:ethereum/ethereum
sudo apt-get update
sudo apt-get install solc
# Install ganache command line tool
npm install -g ganache-cli

# Create py file to run the codes
mkdir project3
cd project3
touch demo.py
nano demo.py # copy the codes into this file

# Install related packages
pip3 install web3 merkletools py-solc-x

# Start ganache service
ganache-cli -p 7545

# run the demo in another terminal
python3 demo.py