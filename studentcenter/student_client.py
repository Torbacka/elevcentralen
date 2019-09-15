import os

import requests

username = os.environ['USERNAME']
password = os.environ['PASSWORD']
base_url = 'https://elevcentralen.se/'
sessions = []


def authenticate():
    form = {
        '__RequestVerificationToken': 'ReJ0QP3-X_b_VV4wdw3_bEPUowzLB5up31e2KNB7b7ES2GRVgUWb83piECkKq8-6FDGBdz_6fq7meRvLzjNvLnGtVXs1',
        'Username': username,
        'Password': password
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': '__RequestVerificationToken=Snv90NLwWnHNVKSk2tNHSi43jK4zAjKW9tSyCdCATrE1Jou8VZ8bSO6ttaazW4-HJIra2T8HYlaCSacO87zynVr6wHY1'
    }
    response = requests.post(url=f"{base_url}/sv/Login/Authenticate", headers=headers, data=form)



if __name__ == '__main__':
    authenticate()
