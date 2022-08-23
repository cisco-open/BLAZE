import requests 

"""

This is a script use to test the requests methods. 

"""

def test_requests(app): 

    response = requests.get('http://localhost:3000/')
    print(response)