import requests
import json


def make_header(token):
    return {
        'Authorization': f'Zoho-oauthtoken {token.access}'
    }


def create_invoice(token, org_id, customer_id, data_object):
    url = 'https://books.zoho.com/api/v3/invoices'
    headers = make_header(token)
    params = {'organization_id': org_id}

    data_object['customer_id'] = customer_id
    data = json.dumps(data_object).encode('utf-8')

    response = requests.post(url=url, headers=headers, params=params, data=data)

    if response.status_code == 401:
        token.generate()
        return create_invoice(token, org_id, customer_id, data_object)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content.get("invoice")
    

def get_invoices(token, org_id, **kwargs):
    url = 'https://books.zoho.com/api/v3/invoices'
    headers = make_header(token)
    params = kwargs
    params['organization_id'] = org_id

    response = requests.get(url=url, headers=headers, params=params)

    if response.status_code == 401:
        token.generate()
        return get_invoices(token, org_id, **kwargs)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content.get("invoices")



def update_invoice(token, org_id, invoice_id, customer_id, data_object):
    url = f'https://books.zoho.com/apiv/3/invoices/{invoice_id}'
    headers = make_header(token)
    params = {'organization_id': org_id}

    data_object['customer_id'] = customer_id
    data = json.dumps(data_object).encode('utf-8')

    response = requests.put(url=url, headers=headers, params=params, data=data)

    if response.status_code == 401:
        token.generate()
        return update_invoice(token, org_id, invoice_id, customer_id, data_object)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content.get("message"), content.get("invoice")


def get_invoice(token, org_id, invoice_id, **kwargs):
    url = f'https://books.zoho.com/api/v3/invoices/{invoice_id}'
    headers = make_header(token)
    params = {
        'organization_id': org_id,
        'print': kwargs.get("print"),
        "accept": kwargs.get("accept")
    }
    response = requests.get(url=url, headers=headers, params=params)

    if response.status_code == 401:
        token.generate()
        return get_invoice(token, org_id, invoice_id, **kwargs)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content.get('invoice')

def delete_invoice(token, org_id, invoice_id):
    url = f'https://books.zoho.com/api/v3/invoices/{invoice_id}'
    headers = make_header(token)
    params = {
        'organization_id': org_id
    }
    response = requests.delete(url=url, headers=headers, params=params)

    if response.status_code == 401:
        token.generate()
        return delete_invoice(token, org_id, invoice_id, **kwargs)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content.get('message')



def mark_status(token, org_id, invoice_id, status):
    url = f'https://books.zoho.com/api/v3/invoices/{invoice_id}/status/{status}'
    headers = make_header(token)
    params = {'organization_id': org_id}

    response = requests.post(url=url, headers=headers, params=params)

    if response.status_code == 401:
        token.generate()
        return mark_status(token, org_id, invoice_id, status)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content.get("message")


def email_invoice(token, org_id, invoice_id, to_mail_ids, **kwargs):
    url = f'https://books.zoho.com/api/v3/invoices/{invoice_id}/email'
    headers = make_header(token)
    params = {'organization_id': org_id}

    data_object = kwargs
    data_object['to_mail_ids'] = to_mail_ids
    data = json.dumps(data_object).encode('utf-8')

    response = requests.post(url=url, headers=headers, params=params, data=data)

    if response.status_code == 401:
        token.generate()
        return email_invoice(token, org_id, invoice_id, to_mail_ids, **kwargs)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content.get("message")

    d
    



