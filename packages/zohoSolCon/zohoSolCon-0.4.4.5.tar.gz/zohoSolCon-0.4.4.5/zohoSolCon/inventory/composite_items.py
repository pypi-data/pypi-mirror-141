import requests
import json


def make_header(token):
    return {
        'Authorization': f'Zoho-oauthtoken {token.access}'
    }



def create_composite_item(token, org_id, name, mapped_items, **kwargs):
    url = 'https://inventory.zoho.com/api/v1/compositeitems'
    headers = make_header(token)
    params = {'organization_id': org_id}

    data_object = kwargs

    data_object['mapped_items'] = mapped_items
    data_object['name'] = name

    data = json.dumps(data_object).encode('utf-8')

    response = requests.post(url=url, headers=headers, params=params, data=data)

    if response.status_code == 401:
        token.generate()
        return create_composite_item(token, org_id, name, mapped_items, **kwargs)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content.get('message'), content.get("composite_item")


def get_composite_items(token, org_id, **kwargs):
    url = 'https://inventory.zoho.com/api/v1/compositeitems'
    headers = make_header(token)
    params = kwargs
    params['organization_id'] = org_id

    response = requests.get(url=url, headers=headers, params=params)

    if response.status_code == 401:
        token.generate()
        return get_composite_items(token, org_id, **kwargs)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content.get("composite_items")



def update_composite_item(token, org_id, item_id, data_object):
    url = f'https://inventory.zoho.com/api/v1/compositeitems/{item_id}'
    headers = make_header(token)
    params = {'organization_id': org_id}
    data = json.dumps(data_object).encode('utf-8')

    response = requests.put(url=url, headers=headers, params=params, data=data)

    if response.status_code == 401:
        token.generate()
        return update_composite_item(token, org_id, item_id, data_object)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content.get('message'), content.get("composite_item")


def get_composite_item(token, org_id, item_id):
    url = f'https://inventory.zoho.com/api/v1/compositeitems/{item_id}'
    headers = make_header(token)
    params = {'organization_id': org_id}
    response = requests.get(url=url, headers=headers, params=params)

    if response.status_code == 401:
        token.generate()
        return get_composite_item(token, org_id, item_id)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content.get("composite_item")


def delete_composite_item(token, org_id, item_id):
    url = f'https://inventory.zoho.com/api/v1/compositeitems/{item_id}'
    headers = make_header(token)
    params = {'organization_id': org_id}
    response = requests.delete(url=url, headers=headers, params=params)

    if response.status_code == 401:
        token.generate()
        return delete_composite_item(token, org_id, item_id)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content.get("message")


def toggle_status(token, org_id, item_id, status="active"):
    url = f'https://inventory.zoho.com/api/v1/compositeitems/{item_id}/{status.lower()}'
    headers = make_header(token)
    params = {'organization_id': org_id}

    response = requests.post(url=url, headers=headers, params=params)

    if response.status_code == 401:
        token.generate()
        return toggle_status(token, org_id, item_id, status=status)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content.get("message")


def create_bundle(token, org_id, reference_number, date, composite_item_id, quantity, line_items, is_completed=True, **kwargs):
    url = 'https://inventory.zoho.com/api/v1/bundles'
    headers = make_header(token)
    params = {'organization_id': org_id}

    data_object = {
        'reference_number': reference_number,
        'date': date,
        'composite_item_id': composite_item_id,
        'quantity_to_bundle': quantity,
        'line_items': line_items,
        'is_completed': is_completed,
        'description': kwargs.get('description'),
        'composite_item_name': kwargs.get("composite_item_name"),
        'composite_item_sku': kwargs.get("composite_item_sku")
    }
    data = json.dumps(data_object).encode('utf-8')

    response = requests.post(url=url, headers=headers, params=params, data=data)
    if response.status_code == 401:
        token.generate()
        return create_bundle(token, org_id, reference_number, date, composite_item_id, quantity, line_items, is_completed=is_completed, **kwargs)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content.get("message"), content.get("bundle_id")


def bundle_history(token, org_id, composite_item_id):
    url = 'https://inventory.zoho.com/api/v1/bundles'
    headers = make_header(token)
    params = {
        'organization_id': org_id,
        'composite_item_id': composite_item_id
    }
    response = requests.get(url=url, headers=headers, params=params)

    if response.status_code == 401:
        token.generate()
        return bundle_history(token, org_id, composite_item_id)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content.get("bundles")



def get_bundle(token, org_id, bundle_id):
    url = f'https://inventory.zoho.com/api/v1/bundles/{bundle_id}'
    headers = make_header(token)
    params = {'organization_id': org_id}
    response = requests.get(url=url, headers=headers, params=params)

    if response.status_code == 401:
        token.generate()
        return get_bundle(token, org_id, bundle_id)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content.get('bundle')


def delete_bundle(token, org_id, bundle_id):
    url = f'https://inventory.zoho.com/api/v1/bundles/{bundle_id}'
    headers = make_header(token)
    params = {'organization_id': org_id}
    response = requests.delete(url=url, headers=headers, params=params)

    if response.status_code == 401:
        token.generate()
        return delete_bundle(token, org_id, bundle_id)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content.get('messsage')
    
