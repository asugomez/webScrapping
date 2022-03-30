import requests
from bs4 import BeautifulSoup

#url = "https://chilepropiedades.cl/propiedades/venta/casa/region-metropolitana-de-santiago-rm/"
def requestURL(URL, attr = ""):
    ''' 
    Make a request to the URL
    Store the result in 'res' variable
    URL the website we want to scrap
    attr might be some additional information to the URL (to add at the end)
    '''
    try:
        # send the request, with a randome user agent 
        finalURL = URL + attr
        # Store the result in 'res' variable
        res = requests.get(finalURL, headers={
        "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
        })
        txt = res.text
        status = res.status_code
        # print the result
        #print(txt, status)

        # beautiful soup to get the information in str
        soup = BeautifulSoup(res.content, 'html.parser')
        return soup
    except requests.exceptions.ConnectionError:
        print("Site not rechable", url)
