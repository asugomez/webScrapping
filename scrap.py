"""
Web scraping is an automated process of gathering public data. 
A webpage scraper automatically extracts large amounts of public data from target websites in seconds.
More info:
https://oxylabs.io/blog/python-web-scraping
https://www.freecodecamp.org/news/web-scraping-python-tutorial-how-to-scrape-data-from-a-website/
https://towardsdatascience.com/web-scraping-basics-82f8b5acd45c

Beautiful documentation:
https://www.crummy.com/software/BeautifulSoup/bs3/documentation.html


CSS selector:
a.gamers: select an `a` tag with the class gamers
a#gamer: select an `a` tag with the id gamer
p ~ span will match all <span> elements that follow a <p>, immediately or not.
More: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Selectors 
"""
# from urlparse import urlparse
# from threading import Thread
# import httplib, sysa
# from Queue import Queue

from dataframeVivienda import *
import multiprocessing as mp



# SCRAPPING
# create empty lists with the info I want to save
# valorUF, valorCLP, valorUSD, habitaciones, banos, estacionamientos, amoblado, totalSuperficie, superficieConstruida, añoConstruccion# = [], [], [], [], [], [], [], [], [], []
# direccion, comunas, tipoPublicacion, tipoVivienda, fechaPublicacion# = [], [], [], [], []
# links, quienVende, corredor#  = [], [], []
# # npages
''' 
def getInfoUrl(URL):
    page = requestURL(URL)
    housesList = page.select("div.clp-publication-element")
    #print(housesList)
    nHouses = len(housesList)
    # each house
    for j in range(nHouses):
        # append the info to the lists 
        titleHouse = housesList[j].select_one("h2.publication-title-list")
        ### link
        link = titleHouse.find('a')['href']
        finalLink = BASE_URL + link
        # append link to list
        links.append(finalLink)
        # get the info from this link
        housePage = requestURL(finalLink)
        #if(housePage == None): print("The url is: ", finalLink)
        main = housePage.select_one("div.clp-administration-main-panel div.clp-details-table")
        footmain = housePage.select_one("div.clp-administration-main-panel div.clp-publication-contact-box")

        ## precios CLP y UF
        # los valores estan en CLP y UF, pero cambia el orden segun el anuncio
        # además se debe modificar el texto para que quede solo el string del numero y sea convertible en float
        # por eso se le saca " " y los puntos, y se modifican las comas por puntos
        ### precio 1
        precio1 = main.select_one("div:-soup-contains('Valor:') ~ div.clp-description-value")
        valPrecio, divisa = appendPrice(precio1)
        if(divisa == "CLP"):
            valorCLP.append(valPrecio)
        elif(divisa == "UF"):
            valorUF.append(valPrecio)
        elif(divisa == "USD"):
            valorUSD.append(valPrecio)
        else:
            print("WARNING: precio is not in CLP, UF or USD!")
            print(valPrecio)
            valorCLP.append(None)
        ### precio 2
        precio2 = main.select_one("div:-soup-contains('Valor (') ~ div.clp-description-value > span")
        valPrecio, divisa = appendPrice(precio2)
        if(divisa == "CLP"):
            valorCLP.append(valPrecio)
        elif(divisa == "UF"):
            valorUF.append(valPrecio)
        elif(divisa == "USD"):
            valorUSD.append(valPrecio)
        else:
            print("WARNING: precio is not in CLP, UF or USD!")
            print(valPrecio)
            valorCLP.append(None)

        ### habitaciones
        nHab = main.select_one("div:-soup-contains('Habitaciones') ~ div.clp-description-value")
        appendElementToList(nHab, habitaciones, replaceEnter = True, replaceSpace = True, typeElement = "int" )
            
        ### baño 
        nBano = main.select_one("div:-soup-contains('Baño') ~ div.clp-description-value")
        appendElementToList(nBano, banos, replaceEnter = True, replaceSpace = True, typeElement = "int" )

        ### estacionamiento 
        nEstacionamientos = main.select_one("div:-soup-contains('Estacionamiento') ~ div.clp-description-value")
        appendElementToList(nEstacionamientos, estacionamientos, replaceEnter = True, replaceSpace = True, typeElement = "int" )

        ### amoblado
        muebles = main.select_one("div:-soup-contains('Amoblado') ~ div.clp-description-value")
        appendElementToList(muebles, amoblado, replaceEnter = True, replaceSpace = True, typeElement = "str" )

        ### superficie total
        supTotal = main.select_one("div:-soup-contains('Superficie Total') ~ div.clp-description-value")
        appendElementToList(supTotal, totalSuperficie, replaceEnter = True, replaceSpace = True, typeElement = "float", otherCharToDelete = ["m²"])
    
        ### superficie construida
        supConstruida = main.select_one("div:-soup-contains('Superficie Construida') ~ div.clp-description-value")
        appendElementToList(supConstruida, superficieConstruida, replaceEnter = True, replaceSpace = True, typeElement = "float", otherCharToDelete = ["m²"])
    
        ### año construccion
        añoCons = main.select_one("div:-soup-contains('Año') ~ div.clp-description-value")
        appendElementToList(añoCons, añoConstruccion, replaceEnter = True, replaceSpace = True, typeElement = "int")

        ### direccion
        direccionCasa = main.select_one("div:-soup-contains('Dirección') ~ div.clp-description-value")
        appendElementToList(direccionCasa, direccion, replaceEnter = True, replaceSpace = False, typeElement = "str")
        
        ### comuna
        comuna = main.select_one("div:-soup-contains('Dirección') ~ div.clp-description-value")
        if(comuna != None):
            comuna = comuna.text.replace("\n","")
            comuna = comuna.partition(",")[0]
        appendElementToList(comuna, comunas, replaceEnter = True, replaceSpace = False, typeElement = "str")

        ### codigo aviso 

        ### codigo externo

        ### tipo publicacion (venta usada por ej.) 
        tipoPub = main.select_one("div:-soup-contains('Tipo de publicación') ~ div.clp-description-value")
        appendElementToList(tipoPub, tipoPublicacion, replaceEnter = True, replaceSpace = False, typeElement = "str")
      
        ### tipo propiedad (casa) 
        tipoProp = main.select_one("div:-soup-contains('Tipo de propiedad') ~ div.clp-description-value")
        appendElementToList(tipoProp, tipoVivienda, replaceEnter = True, replaceSpace = True, typeElement = "str")

        ### fecha publicacion 
        fecha = main.select_one("div:-soup-contains('Fecha Publicación') ~ div.clp-description-value")
        appendElementToList(fecha, fechaPublicacion, replaceEnter = True, replaceSpace = True, typeElement = "str")

        ### corredora
        corredora = footmain.select_one("h2:-soup-contains('Corredora') ~ div > div.clp-user-contact-details-table > table > tr > th:-soup-contains('Nombre') ~ td")
        appendElementToList(corredora, corredor, replaceEnter = True, replaceSpace = False, typeElement = "str")

        ### quien vende
        propietario = footmain.select_one("div.clp-user-contact-details-table > h2:-soup-contains('Información de Contacto') ~ table > tr > th:-soup-contains('Nombre') ~ td")
        appendElementToList(propietario, quienVende, replaceEnter = True, replaceSpace = False, typeElement = "str")
    
    #return valorUF, valorCLP, valorUSD, habitaciones, banos, estacionamientos, amoblado, totalSuperficie, superficieConstruida, añoConstruccion, direccion, comunas, tipoPublicacion, tipoVivienda, fechaPublicacion, links, quienVende, corredor
 '''

#pool.wait_completion()
''' 
for i in range(5):   
    # Houses list
    page = requestURL(URL, str(i))
    housesList = page.select("div.clp-publication-element")
    #print(housesList)
    nHouses = len(housesList)
    # each house
    # crear nHouses threads
    #q = Queue(concurrent * 2)
    for j in range(nHouses):
        # append the info to the lists 
        titleHouse = housesList[j].select_one("h2.publication-title-list")
        ### link
        link = titleHouse.find('a')['href']
        finalLink = BASE_URL + link
        # append link to list
        links.append(finalLink)
        # get the info from this link
        housePage = requestURL(finalLink)
        #if(housePage == None): print("The url is: ", finalLink)
        main = housePage.select_one("div.clp-administration-main-panel div.clp-details-table")
        footmain = housePage.select_one("div.clp-administration-main-panel div.clp-publication-contact-box")

        ## precios CLP y UF
        # los valores estan en CLP y UF, pero cambia el orden segun el anuncio
        # además se debe modificar el texto para que quede solo el string del numero y sea convertible en float
        # por eso se le saca " " y los puntos, y se modifican las comas por puntos
        ### precio 1
        precio1 = main.select_one("div:-soup-contains('Valor:') ~ div.clp-description-value")
        valPrecio, divisa = appendPrice(precio1)
        if(divisa == "CLP"):
            valorCLP.append(valPrecio)
        elif(divisa == "UF"):
            valorUF.append(valPrecio)
        elif(divisa == "USD"):
            valorUSD.append(valPrecio)
        else:
            print("WARNING: precio is not in CLP, UF or USD!")
            print(valPrecio)
            valorCLP.append(None)
        ### precio 2
        precio2 = main.select_one("div:-soup-contains('Valor (') ~ div.clp-description-value > span")
        valPrecio, divisa = appendPrice(precio2)
        if(divisa == "CLP"):
            valorCLP.append(valPrecio)
        elif(divisa == "UF"):
            valorUF.append(valPrecio)
        elif(divisa == "USD"):
            valorUSD.append(valPrecio)
        else:
            print("WARNING: precio is not in CLP, UF or USD!")
            print(valPrecio)
            valorCLP.append(None)

        ### habitaciones
        nHab = main.select_one("div:-soup-contains('Habitaciones') ~ div.clp-description-value")
        appendElementToList(nHab, habitaciones, replaceEnter = True, replaceSpace = True, typeElement = "int" )
            
        ### baño 
        nBano = main.select_one("div:-soup-contains('Baño') ~ div.clp-description-value")
        appendElementToList(nBano, banos, replaceEnter = True, replaceSpace = True, typeElement = "int" )

        ### estacionamiento 
        nEstacionamientos = main.select_one("div:-soup-contains('Estacionamiento') ~ div.clp-description-value")
        appendElementToList(nEstacionamientos, estacionamientos, replaceEnter = True, replaceSpace = True, typeElement = "int" )

        ### amoblado
        muebles = main.select_one("div:-soup-contains('Amoblado') ~ div.clp-description-value")
        appendElementToList(muebles, amoblado, replaceEnter = True, replaceSpace = True, typeElement = "str" )

        ### superficie total
        supTotal = main.select_one("div:-soup-contains('Superficie Total') ~ div.clp-description-value")
        appendElementToList(supTotal, totalSuperficie, replaceEnter = True, replaceSpace = True, typeElement = "float", otherCharToDelete = ["m²"])
    
        ### superficie construida
        supConstruida = main.select_one("div:-soup-contains('Superficie Construida') ~ div.clp-description-value")
        appendElementToList(supConstruida, superficieConstruida, replaceEnter = True, replaceSpace = True, typeElement = "float", otherCharToDelete = ["m²"])
    
        ### año construccion
        añoCons = main.select_one("div:-soup-contains('Año') ~ div.clp-description-value")
        appendElementToList(añoCons, añoConstruccion, replaceEnter = True, replaceSpace = True, typeElement = "int")

        ### direccion
        direccionCasa = main.select_one("div:-soup-contains('Dirección') ~ div.clp-description-value")
        appendElementToList(direccionCasa, direccion, replaceEnter = True, replaceSpace = False, typeElement = "str")
        
        ### comuna
        comuna = main.select_one("div:-soup-contains('Dirección') ~ div.clp-description-value")
        if(comuna != None):
            comuna = comuna.text.replace("\n","")
            comuna = comuna.partition(",")[0]
        appendElementToList(comuna, comunas, replaceEnter = True, replaceSpace = False, typeElement = "str")

        ### codigo aviso 

        ### codigo externo

        ### tipo publicacion (venta usada por ej.) 
        tipoPub = main.select_one("div:-soup-contains('Tipo de publicación') ~ div.clp-description-value")
        appendElementToList(tipoPub, tipoPublicacion, replaceEnter = True, replaceSpace = False, typeElement = "str")
      
        ### tipo propiedad (casa) 
        tipoProp = main.select_one("div:-soup-contains('Tipo de propiedad') ~ div.clp-description-value")
        appendElementToList(tipoProp, tipoVivienda, replaceEnter = True, replaceSpace = True, typeElement = "str")

        ### fecha publicacion 
        fecha = main.select_one("div:-soup-contains('Fecha Publicación') ~ div.clp-description-value")
        appendElementToList(fecha, fechaPublicacion, replaceEnter = True, replaceSpace = True, typeElement = "str")

        ### corredora
        corredora = footmain.select_one("h2:-soup-contains('Corredora') ~ div > div.clp-user-contact-details-table > table > tr > th:-soup-contains('Nombre') ~ td")
        appendElementToList(corredora, corredor, replaceEnter = True, replaceSpace = False, typeElement = "str")

        ### quien vende
        propietario = footmain.select_one("div.clp-user-contact-details-table > h2:-soup-contains('Información de Contacto') ~ table > tr > th:-soup-contains('Nombre') ~ td")
        appendElementToList(propietario, quienVende, replaceEnter = True, replaceSpace = False, typeElement = "str")


       '''  


if __name__ == '__main__':
    # valorUF, valorCLP, valorUSD, habitaciones, banos, estacionamientos, amoblado, totalSuperficie, superficieConstruida, añoConstruccion = [], [], [], [], [], [], [], [], [], []
    # direccion, comunas, tipoPublicacion, tipoVivienda, fechaPublicacion = [], [], [], [], []
    # links, quienVende, corredor = [], [], []
    # get the number of pages we have to scrap
    BASE_URL = "https://chilepropiedades.cl"
    URL = BASE_URL + "/propiedades/venta/casa/region-metropolitana-de-santiago-rm/"
    dataframeVivienda = DataframeVivienda(URL)
    
    urls = [URL + f"{i}" for i in range(1)] # first 5 pages of houses (= 50 houses)

    with mp.Pool(mp.cpu_count()) as pool:
        pool.map(dataframeVivienda.getInfoUrl, urls) # TRY with nro mas grande (repetidS) and without closing, run it without main 
        # test timing 
        pool.close()
    print("helo")

    dataframeVivienda.saveDataInCsvFile()
    #print(fechaPublicacion)
    #print()
    #columns = [comunas, links, tipoVivienda, habitaciones, banos, estacionamientos, amoblado, totalSuperficie, superficieConstruida, añoConstruccion, valorUF, valorCLP, valorUSD, direccion, tipoPublicacion, quienVende, corredor]
    #names = ["Comuna", "Link", "Tipo_Vivienda", "N_Habitaciones", "N_Baños", "N_Estacionamientos", "Amoblado", "Total_Superficie_M2", "Superficie_Construida_M2", "Año_Construccion", "Valor_UF", "Valor_CLP", "Valor_USD", "Dirección", "Tipo_Publicacion", "Quién_Vende", "Corredor"]
    #print(columns)
    #createOuputCsv(names, columns)

# todo an assert between len(valorCLP) y len(valorUF)

