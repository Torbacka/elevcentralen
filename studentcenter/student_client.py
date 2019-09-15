import json

import requests
from bs4 import BeautifulSoup

base_url = 'https://elevcentralen.se/'
sessions = []


def authenticate(username, password):
    """
    Authenticate the user against all schools.
    return boolean if users successful authenticated against elevcentralen.
    """
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
    parser = BeautifulSoup(response.content, 'html.parser')
    buttons = parser.findAll('button')
    for button in buttons:
        session = requests.Session()
        form['CustomerNumber'] = button['data-customer-number']
        session.post(url=f"{base_url}/sv/Login/Authenticate", headers=headers, data=form)
        if '.SCFORMSAUTH' in session.cookies:
            sessions.append({
                'id': button['data-customer-number'],
                'name': button.text.strip(),
                'session': session
            })


def get_all_bookings():
    """
    Get all bookings for all active schools.
    :return: all bookings.
    """
    bookings = []
    for session in sessions:
        response = session['session'].get(f"{base_url}/Booking/Home/CurrentBookings")
        bookings_data = json.loads(response.text)
        for item in bookings_data['items']:
            bookings.append({
                'title': item['title'],
                'length': item['length'],
                'employees': item['employees'],
                'start': item['start'],
                'end': item['end'],
                'cancellationTime': item['lateCancellationTime'],
                'log': item['log']
            })
    return bookings


if __name__ == '__main__':
    bookings_test = get_all_bookings()
    print(bookings_test)
