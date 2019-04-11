import json

from flask import Flask, jsonify
from flask import request
from flask import abort
from iroha import Iroha, IrohaGrpc
from iroha import IrohaCrypto
import binascii

admin_account = "admin@test"
admin_private_key = "f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70"
iroha = Iroha(admin_account)
net = IrohaGrpc()

app = Flask(__name__)

def send_transaction_and_print_status(transaction):
    hex_hash = binascii.hexlify(IrohaCrypto.hash(transaction))
    print('Transaction hash = {}, creator = {}'.format(
        hex_hash, transaction.payload.reduced_payload.creator_account_id))
    net.send_tx(transaction)
    for status in net.tx_status_stream(transaction):
        print(status)


@app.route('/iroha_rest/api/v1.0/items', methods=['POST'])
def put_item():
    item = request.args["address"]
    insured_total = request.args["insured_total"]
    query = iroha.query('GetAccountDetail', account_id=admin_account)
    IrohaCrypto.sign_query(query, admin_private_key)
    response = net.send_query(query)
    data = response.account_detail_response
    all_items = json.loads(str(data)[9:-2].replace("\\", ""))[admin_account]
    if item in all_items.keys():
        abort(409, 'Item is already insured')
    commands = [
        iroha.command('SetAccountDetail',
                      account_id=admin_account, key=item, value=insured_total),
    ]
    transaction = iroha.transaction(commands)
    IrohaCrypto.sign_transaction(transaction, admin_private_key)
    send_transaction_and_print_status(transaction)
    query = iroha.query('GetAccountDetail', account_id='admin@test')
    IrohaCrypto.sign_query(query, admin_private_key)
    response = net.send_query(query)
    data = response.account_detail_response
    result = item+":"+str(json.loads(str(data)[9:-2].replace("\\", ""))[admin_account][item])
    return result, 201


@app.route('/iroha_rest/api/v1.0/items', methods=['GET'])
def get_all_items():
    query = iroha.query('GetAccountDetail', account_id=admin_account)
    IrohaCrypto.sign_query(query, admin_private_key)
    response = net.send_query(query)
    data = response.account_detail_response
    return str(json.loads(str(data)[9:-2].replace("\\", ""))), 201


if __name__ == '__main__':
    app.run(debug=True)

# Result:
