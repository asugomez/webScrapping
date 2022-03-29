"""
Web scraping is an automated process of gathering public data. 
A webpage scraper automatically extracts large amounts of public data from target websites in seconds.
More info:
https://oxylabs.io/blog/python-web-scraping
https://www.freecodecamp.org/news/web-scraping-python-tutorial-how-to-scrape-data-from-a-website/
https://towardsdatascience.com/web-scraping-basics-82f8b5acd45c

Beautiful documentation:
https://www.crummy.com/software/BeautifulSoup/bs3/documentation.html

"""
from connexion import *

BASE_URL = "https://chilepropiedades.cl"
URL = BASE_URL + "/propiedades/venta/casa/region-metropolitana-de-santiago-rm/"

# get the number of pages we have to scrap
soup = requestURL(URL)
divNumberPages = soup.select_one("div.clp-results-text-container span.light-bold")
nPages = divNumberPages.text #  Total de páginas: 418
nPages = int(nPages.replace("Total de páginas: ",'')) #418
print(nPages)

# help soup:
# soup.select('a.gamers') # select an `a` tag with the class gamers
# soup.select('a#gamer') # select an `a` tag with the id gamer

# SCRAPPING

# create empty lists with the info I want to save
# Comuna, Link, Tipo_Vivienda, N_Habitaciones, N_Baños, N_Estacionamientos, Total_Superficie_M2, Superficie_Construida_M2, Valor_UF, Valor_CLP, Dirección, Quién_Vende, Corredor
for i in range(1):    
    # Houses list
    page = requestURL(URL, str(i))
    housesList = soup.select("div.clp-publication-element")
    print(housesList)
    nHouses = len(housesList)
    print(nHouses)
    for j in range(nHouses):
        # each house
        # append the info to the lists 
        titleHouse = housesList[j].select_one("h2.publication-title-list")
        #print(title_house)
        address = titleHouse.text
        link = titleHouse.find('a')['href']
        finalLink = BASE_URL + link
        print(finalLink)
        # get the info from this link

    # save data into an output with panda
    # output=pd.DataFrame({'brandName':brand_name,'price':price,'location':location,'description':description,'rating score':rating_score})

    #print(nHouses)



# # Create top_items as empty list
# all_products = []

# # Extract and store in top_items according to instructions on the left
# products = soup.select('div.thumbnail')
# for product in products:
#     name = product.select('h4 > a')[0].text.strip()
#     description = product.select('p.description')[0].text.strip()
#     price = product.select('h4.price')[0].text.strip()
#     reviews = product.select('div.ratings')[0].text.strip()
#     image = product.select('img')[0].get('src')

#     all_products.append({
#         "name": name,
#         "description": description,
#         "price": price,
#         "reviews": reviews,
#         "image": image
#     })


# keys = all_products[0].keys()

# with open('products.csv', 'w', newline='') as output_file:
#     dict_writer = csv.DictWriter(output_file, keys)
#     dict_writer.writeheader()
#     dict_writer.writerows(all_products)