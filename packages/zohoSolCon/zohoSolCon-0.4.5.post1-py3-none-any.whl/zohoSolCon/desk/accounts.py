import requests
import json
from datetime import datetime


def make_header(token, org_id):
    return {
        "orgId": org_id,
        "Authorization": f"Zoho-oauthtoken {token.access}"
    }

def get_account(token, org_id, account_id, **kwargs):
    url = f'https://desk.zoho.com/api/v1/accounts/{account_id}'
    headers = make_header(token, org_id)
    response = requests.get(url=url, headers=headers, params=kwargs)

    if response.status_code == 401:
        token.generate()
        return get_account(token, org_id, account_id, **kwargs)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content


def get_accounts(token, org_id, **kwargs):
    url = f'https://desk.zoho.com/v1/accounts'
    headers = make_header(token, org_id)
    
    response = requests.get(url=url, headers=headers, params=kwargs)

    if response.status_code == 401:
        token.generate()
        return get_accounts(token, org_id, **kwargs)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content.get('data')


def create_account(token, org_id, data_object):
    url = f'https://desk.zoho.com/v1/accounts'
    headers = make_header(token, org_id)
    data = json.dumps(data_object).encode('utf-8')

    response = requests.post(url=url, headers=headers, data=data)

    if response.status_code == 401:
        token.generate()
        return create_account(token, org_id, data_object)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, response.status_code, content

def update_account(token, org_id, data_object):
    url = f'https://desk.zoho.com/v1/accounts'
    headers = make_header(token, org_id)
    data = json.dumps(data_object).encode('utf-8')
    
    response = requests.patch(url=url, headers=headers, data=data)

    if response.status_code == 401:
        token.generate()
        return update_account(token, org_id, data_object)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, response.status_code, content


def account_contracts(token, org_id, account_id, **kwargs):
    url = f'https://desk.zoho.com/api/v1/accounts/{account_id}/contracts'
    headers = make_header(token, org_id)
    response = requests.get(url=url, headers=headers, params=kwargs)

    if response.status_code == 401:
        token.generate()
        return account_contracts(token, org_id, account_id, **kwargs)

    else:
        return token, json.loads(response.content.decode('utf-8')).get('data')


def accounts_count(token, org_id, view_id):
    url = 'https://desk.zoho.com/api/v1/accounts/count'
    headers = make_header(token, org_id)
    response = requests.get(url=url, headers=headers, params={'viewId': view_id})

    if response.status_code == 401:
        token.generate()
        return accounts_count(token, org_id, view_id)

    else:
        return token, int(json.loads(response.content.decode('utf-8')).get('count'))


def account_contacts(token, org_id, account_id, **kwargs):
    url = f'https://desk.zoho.com/api/v1/accounts/{account_id}/contacts'
    headers = make_header(token, org_id)
    response = requests.get(url=url, headers=headers, params=kwargs)

    if response.status_code == 401:
        token.generate()
        return account_contacts(token, org_id, account_id, **kwargs)

    else:
        return token, json.loads(response.content.decode('utf-8')).get('data')


def account_tickets(token, org_id, account_id, **kwargs):
    url = f'https://desk.zoho.com/api/v1/accounts/{account_id}/tickets'
    headers = {
        'orgId': org_id,
        'Authorization': f'Zoho-oauthtoken {token.access}'
    }
    response = requests.get(url=url, headers=headers, params=kwargs)

    if response.status_code == 401:
        token.generate()
        return account_tickets(token, org_id, account_id, **kwargs)

    else:
        return token, json.loads(response.content.decode('utf-8')).get('data')


def account_products(token, org_id, account_id, **kwargs):
    url = f'https://desk.zoho.com/api/v1/accounts/{account_id}/products'
    headers = make_header(token, org_id)
    response = requests.get(url=url, headers=headers, params=kwargs)

    if response.status_code == 401:
        token.generate()
        return account_products(token, org_id, account_id, **kwargs)

    else:
        return token, json.loads(response.content.decode('utf-8')).get('data')


def account_product_link(token, org_id, account_id, product_id_list, associate=True):
    url = f'https://desk.zoho.com/api/v1/accounts/{account_id}/associateProducts'
    headers = make_header(token, org_id)
    data_object = {'ids': product_id_list, 'associate': associate}

    data = json.dumps(data_object).encode('utf-8')
    response = requests.post(url=url, headers=headers, data=data)

    if response.status_code == 401:
        token.generate()
        
        return account_product_link(token, org_id, account_id, product_id_list, associate=associate)

    else:
        return token, response.status_code, json.loads(response.content.decode('utf-8')).get('results')


def mass_action(token, org_id, callback, **kwargs):
    url = 'https://desk.zoho.com/api/v1/tickets'
    headers = make_header(token, org_id)
    empty = False
    index = 0
    params = kwargs
    start_time = datetime.utcnow()

    while not empty:
        params['from'] = index
        params['limit'] = 100
        response = requests.get(url=url, headers=headers, params=params)
        if response.status_code == 401:
            token.generate()
            headers = make_header(token, org_id)
            continue
        content = json.loads(response.content.decode('utf-8'))
        data = content.get("data")
        if len(data) == 0:
            empty = True

        for record in data:
            token, callback_response = callback(token, org_id, record)
            print(callback_response)
            index += 1
            print(f'{index} Records iterated')
        if len(data) < 100:
            empty = True

    end_time = datetime.utcnow()
    time_diff = end_time - start_time
    return token, f'{index} Records iterated.\nStart Time: {start_time.isoformat()}\nEnd Time: {end_time.isoformat()}\nElapsed: {time_diff}'
    
    
