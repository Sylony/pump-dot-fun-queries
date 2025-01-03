#!/usr/bin/env python3

import requests

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
        return request.json()
    else:
        raise Exception('Query failed\n\treturn code: {}\n\tmessage: {}\n'.format(request.status_code, request.text))

if __name__ == "__main__":
    query = """
   {
  EVM(network: eth) {
    Blocks(limit: { count: 10 }) {
      Block {
        Number
        Time
      }
    }
  }
}
    """
    query2 = """
{
  Solana {
    TokenSupplyUpdates(
      limit:{count:1}
      orderBy:{descending:Block_Time}
      where: {TokenSupplyUpdate: {Currency: {MintAddress: {is: "6D7NaB2xsLd7cauWu1wKk6KBsJohJmP2qZH9GEfVi5Ui"}}}}
    ) {
      TokenSupplyUpdate {
        Amount
        Currency {
          MintAddress
          Name
        }
        PreBalance
        PostBalance
      }
    }
  }
}
    """

    ### Not used?
    # variables = {
    #     "network": "solana",
    #     "xxx": "xxx"
    # }
    variables = {}

    ### Grab our API key.
    api_key = ''
    with open('API.key', 'r') as file:
        api_key = file.read().strip()

    output = run_query(query2, variables, api_key)

    print(output)
