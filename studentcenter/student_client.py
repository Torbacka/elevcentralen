import json
import os

import requests
from bs4 import BeautifulSoup

base_url = 'https://elevcentralen.se/'
sessions = []
default_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'
}


def authenticate(username, password):
    """
    Authenticate the user against all schools.
    return boolean if users successful authenticated against elevcentralen.
    """
    sessions.clear()
    form = {
        '__RequestVerificationToken': 'ReJ0QP3-X_b_VV4wdw3_bEPUowzLB5up31e2KNB7b7ES2GRVgUWb83piECkKq8-6FDGBdz_6fq7meRvLzjNvLnGtVXs1',
        'Username': username,
        'Password': password
    }
    extra_headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': '__RequestVerificationToken=Snv90NLwWnHNVKSk2tNHSi43jK4zAjKW9tSyCdCATrE1Jou8VZ8bSO6ttaazW4-HJIra2T8HYlaCSacO87zynVr6wHY1'
    }
    headers = {**default_headers, **extra_headers}
    response = requests.post(url=f"{base_url}/sv/Login/Authenticate", data=form, headers=headers)
    parser = BeautifulSoup(response.content, 'html.parser')
    buttons = parser.findAll('button')
    for button in buttons:
        session = requests.Session()
        form['CustomerNumber'] = button['data-customer-number']
        session.post(url=f"{base_url}/sv/Login/Authenticate", data=form, headers=headers, )
        if '.SCFORMSAUTH' in session.cookies:
            sessions.append({
                'id': button['data-customer-number'],
                'name': button.text.strip(),
                'session': session
            })
    return len(sessions) != 0


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


def get_available_bookings():
    """
    Get all available bookings from all active schools.
    :return: all available bookings
    """

    for session in sessions:
        teacher_response = session['session'].get("https://elevcentralen.se/en/Booking")
        parser = BeautifulSoup(teacher_response.content, 'html.parser')
        teachers_div = parser.find("div", {"class": "list-group teachers"})
        teachers_labels = teachers_div.findAll("label")
        for label in teachers_labels:
            data = {
                "Source": "StudentCentral",
                "Person": {
                    "id": 8160381
                },
                "EducationTypeId": 3,
                "Start": "2019-09-15T22:00:00.000Z",
                "End": "2019-10-20T22:00:00.000Z",
                "SelectedView": "Free",
                "ShowInListView": False,
                "TeacherIDs": [
                    label['data-id']
                ]
            }
            booking_response = session['session'].post(url="https://elevcentralen.se/Booking/Home/Data", data=data, headers=default_headers)
            print(booking_response)


password = os.environ['PASSWORD']
username = os.environ['USERNAME']

if __name__ == '__main__':
    authenticate(username, password)
    get_available_bookings()
