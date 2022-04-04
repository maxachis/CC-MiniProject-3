from web3 import Web3
from solcx import compile_source
import merkletools
import hashlib

def build_merkle_tree(data):
    """ Build Merkle Tree over your data"""
    mt = merkletools.MerkleTools(hash_type="md5")
    for k, v in data.items():
        mt.add_leaf(v, True)
    mt.make_tree()
    return mt

def get_merkle_index_by_key(key, key_index):
    """ Get merkle tree leaf index associated with a key"""
    index=key_index.get(key)
    return index

def get_merkle_proof_by_index(merkle_tree, index):
    """ Get merkle proof associated with an index"""
    merkle_proof=merkle_tree.get_proof(index)
    return merkle_proof

def query_data_by_key(key,data):
    """ Query data by a given key"""
    value=data.get(key)
    return value

def get_value_hash(value):
    """ Calculate hash value"""
    target_hash=hashlib.md5(value.encode('utf-8')).hexdigest()
    return target_hash

if __name__ == '__main__':
    #Replace your own data here
    ori_data = {
        'A': '1',
        'B': '2',
        'C': '3',
        'D': '4',
        'E': '5',
        'F': '6'
    }
    #Replace your own modified data here
    modified_data={
        'A': '1',
        'B': '3',#Modified Pair
        'C': '3',
        'D': '4',
        'E': '5',
        'F': '6'
    }
    #Replace your own key merkle leaf index here
    key_index = {
        'A': 0,
        'B': 1,
        'C': 2,
        'D': 3,
        'E': 4,
        'F': 5
    }
    #build merkle tree
    merkle_tree=build_merkle_tree(ori_data)
    #get merkle root
    merkle_root=merkle_tree.get_merkle_root()
    ## Ethereum Blockchain Part Start ##
    compiled_sol = compile_source(
        '''
        pragma solidity >0.5.0;
        contract Verify{
            string merkleRoot;

            function setMerkleRoot(string memory _merkleRoot) public {
                merkleRoot=_merkleRoot;
            }

            function getMerkleRoot()view public returns (string memory){
                return merkleRoot;
            }
        }
        ''',
        output_values=['abi', 'bin']
    )

    contract_id, contract_interface = compiled_sol.popitem()

    bytecode = contract_interface['bin']
    abi = contract_interface['abi']

    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

    w3.eth.default_account = w3.eth.accounts[0]

    Verify = w3.eth.contract(abi=abi, bytecode=bytecode)

    deploy_tx_hash = Verify.constructor().transact()
    deploy_tx_receipt = w3.eth.wait_for_transaction_receipt(deploy_tx_hash)

    verify = w3.eth.contract(
        address=deploy_tx_receipt.contractAddress,
        abi=abi
    )
    # data owner set merkle root
    set_tx_hash = verify.functions.setMerkleRoot(merkle_root).transact()
    set_tx_recipient = w3.eth.wait_for_transaction_receipt(set_tx_hash)
    ## Ethereum Blockchain End ##

    ##Query Client start querying, this part is for original data query, no malicious event##
    query_result=query_data_by_key('B',ori_data)
    merkle_proof_index_ori=get_merkle_index_by_key('B', key_index)
    merkle_proof_ori=get_merkle_proof_by_index(merkle_tree,merkle_proof_index_ori)

    #get original merkle root from Ethereum
    root_from_chain = verify.functions.getMerkleRoot().call()
    #get the hash of query result
    query_result_hash=get_value_hash(query_result)
    #verification
    print("no malicious operations")
    is_valid_ori = merkle_tree.validate_proof(merkle_proof_ori, query_result_hash, root_from_chain)
    print(is_valid_ori)

    ##Query Client start querying, this part is for modified data,malicious event occured##
    query_result_mali = query_data_by_key('B', modified_data)
    merkle_proof_index_mali = get_merkle_index_by_key('B',key_index)
    merkle_proof_mali = get_merkle_proof_by_index(merkle_tree, merkle_proof_index_mali)

    query_result_hash_mali = get_value_hash(query_result_mali)
    #verification
    print("malicious operations")
    is_valid_mali = merkle_tree.validate_proof(merkle_proof_mali, query_result_hash_mali, root_from_chain)
    print(is_valid_mali)

