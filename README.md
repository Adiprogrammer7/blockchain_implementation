# blockchain_implementation

Simple blockchain implemetation with python! Though it won't transfer anything actual to a given address but it implements all the basic concepts of blockchain like 
proof of work, mining, consensus, generating and validating signature on transaction etc. The best way of understanding the blockchain is by building one!

## Instructions to run: 
First download the repo on your local machine using git clone:
```
git clone https://github.com/Adiprogrammer7/blockchain_implementation.git
```
Then navigate to repo and install dependencies:
```
pip install -r requirements.txt
```
In the ```config_peers.py``` add the peers you wish to have while running the network. By default we have some peers added to file like:
```
# store all url's running on the network here in string format, so that they can communicate
# for example: 'http://127.0.0.1:5000/'
peers = {'http://127.0.0.1:5000/', 'http://127.0.0.1:5001/'}
```
We will need a valid private key and public key pair to be able to sign the transaction and make a valid transaction. For that you can run ```generate_wallet.py``` file 
which will give you a valid private key and public key pair.  

Now to run, open two terminals and navigate both to repo. Use following commands to run instances of our application:   
For the first instance on port 5000:
```
set FLASK_APP=main.py
flask run --port 5000 --debugger --reload
```   
For the second instance on port 5001:   
```
set FLASK_APP=main.py
flask run --port 5001 --debugger --reload
```
Now we will have two instances running on http://localhost:5000 and http://localhost:5001.   
![index](https://user-images.githubusercontent.com/30752980/110203144-67feaa00-7e92-11eb-90f5-3a81a91153af.png)


## How it works:
You can find private key and public key pair in ```wallet.txt```, which we generated earlier by running ```generate_wallet.py```. Using that you can make a valid transaction:  
![image](https://user-images.githubusercontent.com/30752980/110203408-12c39800-7e94-11eb-8689-76829381c3d4.png)

That transaction now can be mined by ```/mine```. For example, http://localhost:5001/mine:
![image](https://user-images.githubusercontent.com/30752980/110203573-e8bea580-7e94-11eb-996b-dc8235725581.png)

Just like this you can make multiple transactions and mining will put them in a block which will be added to blockchain of each peer.
You can view the entire blockchain on ```/chain``` view. For example, http://localhost:5000/chain:
![image](https://user-images.githubusercontent.com/30752980/110203709-ab0e4c80-7e95-11eb-9640-e9dc48462eb6.png)

Also there are other views like ```/peers```, ```/consensus```, ```/unconfirmed_transactions```, etc.

### Open to any useful contribution :)