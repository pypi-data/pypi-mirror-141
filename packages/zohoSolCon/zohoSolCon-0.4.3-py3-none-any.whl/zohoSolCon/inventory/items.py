import requests
import json


def make_header(token):
    return {
        "Authorization": f"Zoho-oauthtoken {token.access}"
    }


def create_item(token, org_id, data_object):
    url = 'https://inventory.zoho.com/api/v1/items'
    headers = make_header(token)
    params = {'organization_id': org_id}

    data = json.dumps(data_object).encode('utf-8')

    response = requests.post(url=url, headers=headers, params=params, data=data)

    if response.status_code == 401:
        token.generate()
        return create_item(token, org_id, data_object)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content.get("message"), content.get("item")


def get_items(token, org_id):
    url = 'https://inventory.zoho.com/api/v1/items'
    headers = make_header(token)
    params = {'organization_id': org_id}

    response = requests.get(url=url, headers=headers, params=params)

    if response.status_code == 401:
        token.generate()
        return get_items(token, org_id)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content.get("items")


def update_item(token, org_id, item_id, data_object):
    url = f'https://inventory.zoho.com/api/v1/items/{item_id}'
    headers = make_header(token)
    params = {'organization_id': org_id}

    data = json.dumps(data_object).encode('utf-8')

    response = requests.put(url=url, headers=headers, params=params, data=data)

    if response.status_code == 401:
        token.generate()
        return update_item(token, org_id, item_id, data_object)

    else:
        content = json.loads(repsonse.content.decode('utf-8'))
        return token, content.get('message'), content.get("item")


def get_item(token, org_id, item_id):
    url = f'https://inventory.zoho.com/api/v1/items/{item_id}'
    headers = make_header(token)
    params = {'organization_id': org_id}

    response = requests.get(url=url, headers=headers, params=params)

    if response.status_code == 401:
        token.generate()
        return get_item(token, org_id, item_id)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content.get('item')


def delete_item(token, org_id, item_id):
    url = f'https://inventory.zoho.com/api/v1/items/{item_id}'
    headers = make_header(token)
    params = {'organization_id': org_id}

    response = requests.delete(url=url, headers=headers, params=params)

    if response.status_code == 401:
        token.generate()
        return delete_item(token, org_id, item_id)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content.get('message')


    

    
