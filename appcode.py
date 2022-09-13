from dotenv import dotenv_values
import argparse
import requests
import json

parser = argparse.ArgumentParser()

parser.add_argument("-n", "--number", help="Number of Entries", type=int)
parser.add_argument("-p", "--page", help="Page Number", type=int)
parser.add_argument("-ts", "--tech-stack", help="Tech Stack to search")

args = parser.parse_args()

config = dotenv_values('.env')

headers = {'Referer':'https://app.microacquire.com/'}

login_url = 'https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=AIzaSyDUxAmTGc7LhbduowuDOJF0YZl5xXrmJaI'
login_input = {'email':config.get('email'),'password':config.get('password'),'returnSecureToken':True}

login_response = requests.post(login_url, json=login_input, headers=headers)
login_data = login_response.json()

# =============================================================================
# account_url = 'https://www.googleapis.com/identitytoolkit/v3/relyingparty/getaccountInfo?key=AIzaSyDUxAmTGc7LhbduowuDOJF0YZl5xXrmJaI'
# account_input = {'idToken':login_data.get('idToken')}
# account_response = requests.post(account_url, json=account_input, headers=headers)
# account_data = account_response.json()
# =============================================================================

number = 10 if args.number == None else args.number
page = ((1 if args.page == None else args.page) - 1) * number

headers['Authorization'] = 'Bearer ' + login_data.get('idToken')
search_url = 'https://us-central1-microacquire.cloudfunctions.net/v1-search'
search_input = {'data':{'marketplace':{'query':{'ids':{'exclude':[],'only':None}},'skip':page,'take':number,'order':[{'by':'date','order':'desc'}]}}}
search_response = requests.post(search_url, json=search_input, headers=headers)
search_data = search_response.json()

results = search_data.get('result').get('marketplace').get('results')

techStack = args.tech_stack
if techStack != None:
    filtered = filter(lambda company: company.get('techStack').find(techStack) > -1, results)
    results = list(filtered)

print(json.dumps(results))