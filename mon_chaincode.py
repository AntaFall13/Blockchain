from hfc.fabric import Client
from hfc.fabric.contract import Contract
from hfc.fabric.user import create_user
from hfc.fabric.orderer import Orderer
from hfc.fabric.peer import Peer
from hfc.fabric.ca import CAClient
from hfc.util.keyvaluestore import FileKeyValueStore

import asyncio
import json

class MonChaincode(Contract):
    async def stockerDocument(self, key, hash):
        client = self.client
        channel = client.get_channel('mychannel')
        proposal_request = {
            'fcn': 'invoke',
            'args': ['stockerDocument', key, hash],
            'chaincode_id': 'mon_chaincode'
        }
        responses = await channel.send_transaction_proposal(request=proposal_request)
        response = responses[0]
        if response.response.status != 200:
            raise Exception(f"Erreur lors de l'invocation: {response.response.message}")
        await channel.send_transaction(responses)
        return "Document stocké avec succès"

    async def recupererDocument(self, key):
        client = self.client
        channel = client.get_channel('mychannel')
        proposal_request = {
            'fcn': 'invoke',
            'args': ['recupererDocument', key],
            'chaincode_id': 'mon_chaincode'
        }
        responses = await channel.send_transaction_proposal(request=proposal_request)
        response = responses[0]
        if response.response.status != 200:
            raise Exception(f"Erreur lors de l'invocation: {response.response.message}")
        return response.response.payload.decode('utf-8')


async def main():
    # Configuration du client Hyperledger Fabric
    client = Client(net_profile="network.json")

    # Chargement de l'utilisateur
    admin = create_user(name='Admin', org='org1.example.com', state_store=FileKeyValueStore('/tmp/hfc-key-store'))

    client.set_user_context(admin)

    # Ajout de l'orderer
    orderer = Orderer('orderer.example.com', 'orderer.pem')
    client.add_orderer(orderer)

    # Ajout du peer
    peer = Peer('peer0.org1.example.com', 'peer.pem')
    client.add_peer(peer)

    # Ajout de la CA
    ca = CAClient('ca.org1.example.com')
    client.add_ca(ca)

    # Créer une instance du chaincode
    contract = MonChaincode(client, 'mychannel', 'mon_chaincode')

    # Stocker un document
    await contract.stockerDocument('doc1', 'hash1')

    # Récupérer un document
    document = await contract.recupererDocument('doc1')
    print(document)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
