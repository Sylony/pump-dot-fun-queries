#!/usr/bin/env python3

import requests
import argparse
import json

def run_query(query, variables, api_key):

    # endpoint = 'https://streaming.bitquery.io/graphql'
    endpoint = 'https://streaming.bitquery.io/eap'
    headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {api_key}'}

    request = requests.post(endpoint,
                            json={'query': query.strip(),
                                  'variables': variables},
                            headers=headers)
    
    if request.status_code == 200:
        return request.text
    else:
        raise Exception('Query failed\n\treturn code: {}\n\tmessage: {}\n'.format(request.status_code, request.text))

if __name__ == "__main__":
    ### Parse our args
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--api_key', required=True,
                        type=str, help='File that contains our API key.')
    parser.add_argument('-q', '--query', required=True,
                        type=str, help='File that contains our query')
    args = parser.parse_args()
    api_key_file = args.api_key
    query_file = args.query

    
    ### We'll probably need variables later.
    variables = {}

    ### Grab our API key.
    api_key = ''
    with open(api_key_file, 'r') as file:
        api_key = file.read().strip()

    ### Grab our query.
    query = ''
    with open(query_file, 'r') as file:
        query = file.read().strip()

    ### Run our query
    output = run_query(query, variables, api_key)
    data = json.loads(output)

    query2 = ''
    with open('queries/pf.creation_time.query', 'r') as file:
        query2 = file.read().strip()
        

    for trade in data['data']['Solana']['DEXTrades']:
        print(trade['Trade']['Buy']['Currency']['Name'])
        # print(trade['Trade']['Buy']['Currency']['MintAddress'])
        mint_address = trade['Trade']['Buy']['Currency']['MintAddress']
        final_query = query2.replace('$ADDRESS', '"' + mint_address + '"')
        print(run_query(final_query, variables, api_key))
        print('========================')
        
    # print(output)
