import requests
import json


def make_header(token):
    return {
        'Authorization': f'Zoho-oauthtoken {token.access}'
    }


def create_contact(token, org_id, data_object):
    url = f'https://inventory.zoho.com/api/v1/contacts?organization_id={org_id}'
    headers = make_header(token)

    data = json.dumps(data_object).encode('utf-8')

    response = requests.post(url=url, headers=headers, data=data)

    if response.status_code == 401:
        token.generate()
        return create_contact(token, org_id, data_object)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content.get("message"), content.get("contact")


def get_contacts(token, org_id, **kwargs):
    url = f'https://inventory.zoho.com/api/v1/contacts?organization_id={org_id}'
    headers = make_header(token)

    response = requests.get(url=url, headers=headers, params=kwargs)

    if response.status_code == 401:
        token.generate()
        return get_contacts(token, org_id, **kwargs)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content.get('contacts')


    
def update_contact(token, org_id, contact_id, data_object):
    url = f'https://inventory.zoho.com/api/v1/contacts/{contact_id}?organization_id={org_id}'
    headers = make_header(token)

    data = json.dumps(data_object).encode('utf-8')

    response = requests.put(url=url, headers=headers, data=data)

    if response.status_code == 401:
        token.generate()
        return update_contact(token, org_id, contact_id, data_object)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content.get("message"), content.get("contact")


def get_contact(token, org_id, contact_id):
    url = f'https://inventory.zoho.com/api/v1/contacts/{contact_id}'
    headers = make_header(token)
    params = {'organization_id': org_id}

    response = requests.get(url=url, headers=headers, params=params)
    if response.status_code == 401:
        token.generate()
        return get_contact(token, org_id, contact_id)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content.get('contact')


def delete_contact(token, org_id, contact_id):
    url = f'https://inventory.zoho.com/api/v1/contacts/{contact_id}'
    headers = make_header(token)
    params = {'organization_id': org_id}

    response = requests.delete(url=url, headers=headers, params=params)

    if response.status_code == 401:
        token.generate()
        return delete_contact(token, org_id, contact_id)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content.get("message")


def toggle_status(token, org_id, contact_id, status="active"):
    url = f'https://inventory.zoho.com/api/v1/contacts/{contact_id}/{status}'
    headers = make_header(token)
    params = {'organization_id': org_id}

    response = requests.post(url=url, headers=headers, params=params)

    if response.status_code == 401:
        token.generate()
        return toggle_status(token, org_id, contact_id, status=status)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content.get('message')


def email_statement(token, org_id, contact_id, subject, body, **kwargs):
    url = f'https://inventory.zoho.com/api/v1/contacts/{contact_id}/statements/email'
    headers = make_header(token)
    params = {'organization_id': org_id}

    data_object = {
        'send_from_org_email_id': kwargs.get('send_from_org_email_id'),
        'to_mail_ids': kwargs.get('to_mail_ids'),
        'cc_mail_ids': kwargs.get("cc_mail_ids"),
        "subject": subject,
        "body": body
    }
    data = json.dumps(data_object).encode('utf-8')

    response = requests.post(url=url, headers=headers, params=params, data=data)

    if response.status_code == 401:
        token.generate()
        return email_statement(token, org_id, contact_id, subject, body, **kwargs)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content.get("message")



    
