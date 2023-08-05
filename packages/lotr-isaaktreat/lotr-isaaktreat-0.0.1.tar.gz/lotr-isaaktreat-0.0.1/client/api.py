import requests

baseUrl = "https://the-one-api.dev/v2/"

def connect(url):
    r = requests.get(url, headers={'Authorization': 'Bearer UFqJQJQzA0I28Tg9GfFs'})
    return r

def get_all_data(type, filter, limit): # Returns all data for certain parameter
    if filter and limit:
        url = baseUrl + type + "?" + filter + "=" + limit
        r = connect(url)
    else:
        r = connect(baseUrl + type)

    data_length = len(r.json()['docs'])
    
    out = []
    for i in range(data_length):
        out.append(r.json()['docs'][i]) 
    return out