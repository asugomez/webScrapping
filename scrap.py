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
from connexion import *
from saveData import *

def appendElementToList(element, listOfElements, replaceEnter = True, replaceSpace = True, typeElement = "int"):
    """
    Si el type es float --> reemplazar replace(".","").replace(",",".")
    """
    if(element != None):
        element = element.text
        if(replaceEnter): element = element.replace("\n","")
        if(replaceSpace): element = element.replace(" ", "")
        if(typeElement == "int"): element = int(element)
        if(typeElement == "float"): element = float(element.replace(".","").replace(",","."))
    listOfElements.append(element)
        

BASE_URL = "https://chilepropiedades.cl"
URL = BASE_URL + "/propiedades/venta/casa/region-metropolitana-de-santiago-rm/"

# get the number of pages we have to scrap
soup = requestURL(URL)
divNumberPages = soup.select_one("div.clp-results-text-container span.light-bold")
nPages = divNumberPages.text #  Total de páginas: 418
nPages = int(nPages.replace("Total de páginas: ",'')) #418
#print(nPages)

# SCRAPPING
# create empty lists with the info I want to save
valorUF, valorCLP, valorUSD, habitaciones, banos, estacionamientos, amoblado, totalSuperficie, superficieConstruida, añoConstruccion = [], [], [], [], [], [], [], [], [], []
direccion, comunas, tipoPublicacion, tipoVivienda, fechaPublicacion = [], [], [], [], []
links, quienVende, corredor  = [], [], []
# npages

## try except, if excep columna vacia 
for i in range(1):   
    # Houses list
    page = requestURL(URL, str(i))
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
        #housePage = requestURL(finalLink)
        housePage = requestURL("https://chilepropiedades.cl/ver-publicacion/venta-usada/santiago/casa/camino-a-zapallar-parcelacion-los-cristales-lote-20-curico/6692328")
        if(housePage == None): print("The url is: ", finalLink)
        main = housePage.select_one("div.clp-administration-main-panel div.clp-details-table")
        footmain = housePage.select_one("div.clp-administration-main-panel div.clp-publication-contact-box")

    

        ## precios CLP y UF
        # los valores estan en CLP y UF, pero cambia el orden segun el anuncio
        # además se debe modificar el texto para que quede solo el string del numero y sea convertible en float
        # por eso se le saca " " y los puntos, y se modifican las comas por puntos
        precio1 = main.select_one("div:-soup-contains('Valor:') ~ div.clp-description-value")
        precio2 = main.select_one("div:-soup-contains('Valor (') ~ div.clp-description-value > span")
        #print(precio2)
        try:
            if(precio1 != None):
                precio1 = precio1.text
                precio1 = precio1.replace("\n","").replace(" ","").replace(".","").replace(",",".")
                if(precio1.find("$") != -1): # valor CLP
                    precio1 = precio1.replace("$","")
                    precio1 = float(precio1)
                    valorCLP.append(precio1)
                elif(precio1.find("UF") != -1): # valor UF
                    precio1 = precio1.replace("UF","")
                    precio1 = float(precio1)
                    valorUF.append(precio1)
                elif(precio1.find("USD") != -1):
                    precio1 = precio1.replace("USD","")
                    precio1 = float(precio1)
                    valorUSD.append(precio1)
                else:
                    print("WARNING: precio is not in CLP, UF or USD!")
                    print(precio1)
                    valorCLP.append(precio1)

            else:
                valorCLP.append(precio1)

            if(precio2 != None):
                precio2 = precio2.text
                precio2 = precio2.replace("\n","").replace(" ","").replace(".","").replace(",",".")
                if(precio2.find("$") != -1): # valor CLP
                    precio2 = precio2.replace("$","")
                    precio2 = float(precio2)
                    valorCLP.append(precio2)
                elif(precio2.find("UF") != -1): # valor UF
                    precio2 = precio2.replace("UF","")
                    precio2 = float(precio2)
                    valorUF.append(precio2)
                elif(precio2.find("USD") != -1):
                    precio2 = precio2.replace("USD","")
                    precio2 = float(precio2)
                    valorUSD.append(precio2)
                else:
                    print("WARNING: precio is not in CLP, UF or USD!")
                    print(precio2)
                    valorCLP.append(precio2)

            else:
                valorUF.append(precio2)

            ### habitaciones
            nHab = main.select_one("div:-soup-contains('Habitaciones') ~ div.clp-description-value")
            if(nHab != None):
                nHab = nHab.text.replace("\n","").replace(" ","")
                nHab = int(nHab)
            habitaciones.append(nHab)
                
            ### baño 
            nBano = main.select_one("div:-soup-contains('Baño') ~ div.clp-description-value")
            if(nBano != None):
                nBano = nBano.text.replace("\n","").replace(" ","")
                nBano = int(nBano)
            banos.append(nBano)
    
            ### estacionamiento 
            nEstacionamientos = main.select_one("div:-soup-contains('Estacionamiento') ~ div.clp-description-value")
            if(nEstacionamientos != None):
                nEstacionamientos = nEstacionamientos.text.replace("\n","").replace(" ","")
                nEstacionamientos = int(nEstacionamientos)
            estacionamientos.append(nEstacionamientos)

            ### amoblado
            muebles = main.select_one("div:-soup-contains('Amoblado') ~ div.clp-description-value")
            if(muebles != None):
                muebles = muebles.text.replace("\n","").replace(" ","")
            amoblado.append(muebles)

            ### superficie total
            supTotal = main.select_one("div:-soup-contains('Superficie Total') ~ div.clp-description-value")
            if(supTotal != None):
                supTotal = supTotal.text.replace("\n","").replace(" ","").replace("m²", "" ).replace(".","").replace(",",".")
                supTotal = float(supTotal)
            totalSuperficie.append(supTotal)
        
            ### superficie construida
            supConstruida = main.select_one("div:-soup-contains('Superficie Construida') ~ div.clp-description-value")
            if(supConstruida != None):
                supConstruida = supConstruida.text.replace("\n","").replace(" ","").replace("m²", "" ).replace(".","").replace(",",".")
                supConstruida = float(supConstruida)
            superficieConstruida.append(supConstruida)
        
            ### año construccion
            añoCons = main.select_one("div:-soup-contains('Año') ~ div.clp-description-value")
            if(añoCons != None):
                añoCons = añoCons.text.replace("\n","").replace(" ","")
                añoCons = int(añoCons)
            añoConstruccion.append(añoCons)

            ### direccion
            direccionCasa = main.select_one("div:-soup-contains('Dirección') ~ div.clp-description-value")
            comuna = main.select_one("div:-soup-contains('Dirección') ~ div.clp-description-value")
            if(direccion != None):
                direccionCasa = direccionCasa.text.replace("\n","")
                comuna = direccionCasa.partition(",")[0]
            direccion.append(direccionCasa)
            comunas.append(comuna)

            ### codigo aviso 

            ### codigo externo

            ### tipo publicacion (venta usada por ej.) 
            tipoPub = main.select_one("div:-soup-contains('Tipo de publicación') ~ div.clp-description-value")
            if(tipoPub != None):
                tipoPub = tipoPub.text.replace("\n","")
            tipoPublicacion.append(tipoPub)

            ### tipo propiedad (casa) 
            tipoProp = main.select_one("div:-soup-contains('Tipo de propiedad') ~ div.clp-description-value")
            if(tipoProp != None):
                tipoProp = tipoProp.text.replace("\n","").replace(" ","")
            tipoVivienda.append(tipoProp)

            ### fecha publicacion 
            fecha = main.select_one("div:-soup-contains('Fecha Publicación') ~ div.clp-description-value")
            if(fecha != None):
                fecha = fecha.text.replace("\n","").replace(" ","")
            fechaPublicacion.append(fecha)

            ### corredora
            corredora = corredora = footmain.select_one("h2:-soup-contains('Corredora') ~ div > div.clp-user-contact-details-table > table > tr > th:-soup-contains('Nombre') ~ td")
            if(corredora != None):
                corredora = corredora.text.replace("\n","")
            corredor.append(corredora)

            ### quien vende
            propietario = footmain.select_one("div.clp-user-contact-details-table > h2:-soup-contains('Información de Contacto') ~ table > tr > th:-soup-contains('Nombre') ~ td")
            if(propietario != None):
                propietario = propietario.text.replace("\n","")
            quienVende.append(propietario)
        except Exception as e:
            print("ERROR," , e)


### FINAL CREATE CSV FILE

columns = [comunas, links, tipoVivienda, habitaciones, banos, estacionamientos, amoblado, totalSuperficie, superficieConstruida, añoConstruccion, valorUF, valorCLP, valorUSD, direccion, tipoPublicacion, quienVende, corredor ]
names = ["Comuna", "Link", "Tipo_Vivienda", "N_Habitaciones", "N_Baños", "N_Estacionamientos", "Amoblado", "Total_Superficie_M2", "Superficie_Construida_M2", "Año_Construccion", "Valor_UF", "Valor_CLP", "Valor_USD", "Dirección", "Tipo_Publicacion", "Quién_Vende", "Corredor"]

createOuputCsv(names, columns)

# todo an assert between len(valorCLP) y len(valorUF)

