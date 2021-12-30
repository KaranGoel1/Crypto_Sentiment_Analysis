# query: (#btc OR #bitcoin OR bitcoin OR btc) is:verified

import requests
import os
import json

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")

search_url = "https://api.twitter.com/2/tweets/search/recent"

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
def create_url(pagination_token = None):

    query_params = {'query': 'is:verified (#btc OR #bitcoin OR bitcoin OR btc) lang:en -"Paxful"',
                    'tweet.fields': 'author_id,public_metrics,created_at',
                    'expansions': 'author_id', 
                    'user.fields': 'name,public_metrics,created_at',
                    'max_results': 100,
                    'next_token': pagination_token
                    }
    return query_params

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def main():
    json_data = []
    query = create_url()
    json_response = connect_to_endpoint(search_url, query)
    token = json_response['meta']['next_token']
    json_data.append(json_response)
    counter = 1
    while token:
        query = create_url(token)
        json_response = connect_to_endpoint(search_url, query)
        json_data.append(json_response)
        try:
            token = json_response['meta']['next_token']
        except KeyError:
            token = None
        counter += 1
        print('page' + str(counter) + 'downloaded')
    file_name = 'twitter_data.json'
    with open(file_name, 'w', encoding='ascii') as f:
        f.write(json.dumps(json_data, indent=4, sort_keys=True))
    #print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()
    