import requests
import json


def make_header(token):
    return {
        'Authorization': 'Zoho-oauthtoken {token.access}'
    }


def create_organization(token, org_id, data_object):
    url = f'https://inventory.zoho.com/api/v1/organizations?organization_id={org_id}'
    headers = make_header(token)
    data = json.dumps(data_object).encode('utf-8')

    response = requests.post(url=url, headers=headers, data=data)

    if response.status_code == 401:
        token.generate()
        return create_organization(token, org_id, data_object)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content.get("message"), content.get("organization")


def get_organizations(token, org_id):
    url = f'https://inventory.zoho.com/api/v1/organizations?organization_id={org_id}'
    headers = make_header(token)

    response = requests.get(url=url, headers=headers)

    if response.status_code == 401:
        token.generate()
        return get_organizations(token, org_id)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content.get("organizations")


