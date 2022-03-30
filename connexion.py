import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

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
        #  "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
        ua = UserAgent()
        proxies = { "http": None,"https": None }
        # Store the result in 'res' variable
        # todo look why session 
        session = requests.Session()
        session.trust_env = False
        res = session.get(finalURL, headers={"User-Agent": ua.random}, proxies = proxies)
        txt = res.text
        status = res.status_code
        
        # print the result
        print(status, res.reason, finalURL)

        # beautiful soup to get the information in str
        soup = BeautifulSoup(res.content, 'html.parser')
        return soup
    except requests.exceptions.ConnectionError:
        print("attr: ", attr)
        print("Site not rechable", URL)

        # from getpass import getpass
#>>> requests.get('https://api.github.com/user', auth=('username', getpass()))
#<Response [200]>
