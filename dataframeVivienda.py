from connexion import *
from saveData import *
from funAppend import *
import multiprocessing as mp

class DataframeVivienda:

    def __init__( self, Comuna = [], Link = [], Tipo_Vivienda = [], N_Habitaciones  = [], N_Baños = [], N_Estacionamientos = [], Amoblado = [], Total_Superficie_M2 = [], Superficie_Construida_M2 = [], anoConstruccion = [], Valor_UF = [], Valor_CLP = [], Dirección = [], tipoPublicacion = [], Quién_Vende = [], Corredor = [], fechaPublicacion = []):
        self.Comuna                = Comuna
        self.Link                  = Link
        self.Tipo_Vivienda           = Tipo_Vivienda
        self.N_Habitaciones           = N_Habitaciones
        self.N_Baños                  = N_Baños
        self.N_Estacionamientos       = N_Estacionamientos
        self.Amoblado               = Amoblado
        self.Total_Superficie_M2        = Total_Superficie_M2
        self.Superficie_Construida_M2   = Superficie_Construida_M2
        self.anoConstruccion        = anoConstruccion
        self.Valor_UF              = Valor_UF
        self.Valor_CLP               = Valor_CLP
        #self.Valor_USD               = Valor_USD Valor_USD = [], 
        self.Dirección              = Dirección
        self.tipoPublicacion        = tipoPublicacion
        self.Quién_Vende             = Quién_Vende
        self.Corredor               = Corredor
        self.fechaPublicacion       = fechaPublicacion
    
     
    def getNPagesToScrap(self):
        soup = requestURL(URL)
        divNumberPages = soup.select_one("div.clp-results-text-container span.light-bold")
        nPages = divNumberPages.text #  Total de páginas: 418
        nPages = int(nPages.replace("Total de páginas: ",'')) #418
        return nPages

    def getInfoUrl(self, newURL):
        BASE_URL = "https://chilepropiedades.cl"
        page = requestURL(newURL)
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
            self.Link.append(finalLink)
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
                self.Valor_CLP.append(valPrecio)
            elif(divisa == "UF"):
                self.Valor_UF.append(valPrecio)
            #elif(divisa == "USD"):
                #self.Valor_USD.append(valPrecio)
            else:
                print("WARNING: precio is not in CLP, UF or USD!")
                print(valPrecio)
                self.Valor_CLP.append(None)
            ### precio 2
            precio2 = main.select_one("div:-soup-contains('Valor (') ~ div.clp-description-value > span")
            valPrecio, divisa = appendPrice(precio2)
            if(divisa == "CLP"):
                self.Valor_CLP.append(valPrecio)
            elif(divisa == "UF"):
                self.Valor_UF.append(valPrecio)
            #elif(divisa == "USD"):
            #    self.Valor_USD.append(valPrecio)
            else:
                print("WARNING: precio is not in CLP, UF or USD!")
                print(valPrecio)
                self.Valor_CLP.append(None)

            ### habitaciones
            nHab = main.select_one("div:-soup-contains('Habitaciones') ~ div.clp-description-value")
            appendElementToList(nHab, self.N_Habitaciones, replaceEnter = True, replaceSpace = True, typeElement = "int" )
                
            ### baño 
            nBano = main.select_one("div:-soup-contains('Baño') ~ div.clp-description-value")
            appendElementToList(nBano, self.N_Baños, replaceEnter = True, replaceSpace = True, typeElement = "int" )

            ### estacionamiento 
            nEstacionamientos = main.select_one("div:-soup-contains('Estacionamiento') ~ div.clp-description-value")
            appendElementToList(nEstacionamientos, self.N_Estacionamientos, replaceEnter = True, replaceSpace = True, typeElement = "int" )

            ### amoblado
            muebles = main.select_one("div:-soup-contains('Amoblado') ~ div.clp-description-value")
            appendElementToList(muebles, self.Amoblado, replaceEnter = True, replaceSpace = True, typeElement = "str" )

            ### superficie total
            supTotal = main.select_one("div:-soup-contains('Superficie Total') ~ div.clp-description-value")
            appendElementToList(supTotal, self.Total_Superficie_M2, replaceEnter = True, replaceSpace = True, typeElement = "float", otherCharToDelete = ["m²"])
        
            ### superficie construida
            supConstruida = main.select_one("div:-soup-contains('Superficie Construida') ~ div.clp-description-value")
            appendElementToList(supConstruida, self.Superficie_Construida_M2, replaceEnter = True, replaceSpace = True, typeElement = "float", otherCharToDelete = ["m²"])
        
            ### año construccion
            añoCons = main.select_one("div:-soup-contains('Año') ~ div.clp-description-value")
            appendElementToList(añoCons, self.anoConstruccion, replaceEnter = True, replaceSpace = True, typeElement = "int")

            ### direccion
            direccionCasa = main.select_one("div:-soup-contains('Dirección') ~ div.clp-description-value")
            appendElementToList(direccionCasa, self.Dirección, replaceEnter = True, replaceSpace = False, typeElement = "str")
            
            ### comuna
            comuna = main.select_one("div:-soup-contains('Dirección') ~ div.clp-description-value")
            if(comuna != None):
                comuna = comuna.text.replace("\n","")
                comuna = comuna.partition(",")[0]
            appendElementToList(comuna, self.Comuna, replaceEnter = True, replaceSpace = False, typeElement = "str")

            ### codigo aviso 

            ### codigo externo

            ### tipo publicacion (venta usada por ej.) 
            tipoPub = main.select_one("div:-soup-contains('Tipo de publicación') ~ div.clp-description-value")
            appendElementToList(tipoPub, self.tipoPublicacion, replaceEnter = True, replaceSpace = False, typeElement = "str")
        
            ### tipo propiedad (casa) 
            tipoProp = main.select_one("div:-soup-contains('Tipo de propiedad') ~ div.clp-description-value")
            appendElementToList(tipoProp, self.Tipo_Vivienda, replaceEnter = True, replaceSpace = True, typeElement = "str")

            ### fecha publicacion 
            fecha = main.select_one("div:-soup-contains('Fecha Publicación') ~ div.clp-description-value")
            appendElementToList(fecha, self.fechaPublicacion, replaceEnter = True, replaceSpace = True, typeElement = "str")

            ### corredora
            corredora = footmain.select_one("h2:-soup-contains('Corredora') ~ div > div.clp-user-contact-details-table > table > tr > th:-soup-contains('Nombre') ~ td")
            appendElementToList(corredora, self.Corredor, replaceEnter = True, replaceSpace = False, typeElement = "str")
    
            ### quien vende
            propietario = footmain.select_one("div.clp-user-contact-details-table > h2:-soup-contains('Información de Contacto') ~ table > tr > th:-soup-contains('Nombre') ~ td")
            appendElementToList(propietario, self.Quién_Vende, replaceEnter = True, replaceSpace = False, typeElement = "str")


    def saveDataInCsvFile(self):
        d = self.__dict__
        print(d)
        print(len(self.Comuna))
        print(len(self.Link))
        print(len(self.Quién_Vende))
        print(len(self.Corredor))
        print(len(self.anoConstruccion))
        print(len(self.Dirección))
        print(len(self.N_Baños))
        print(len(self.N_Estacionamientos))
        print(len(self.N_Habitaciones))
        print(len(self.Tipo_Vivienda))
        print(len(self.tipoPublicacion))
        print(len(self.Valor_CLP))
        print(len(self.Valor_UF))
        #print(len(self.Valor_USD))
        print(len(self.Amoblado))
        print(len(self.fechaPublicacion))
        print(len(self.Total_Superficie_M2))
        print(len(self.Superficie_Construida_M2))
        createOuputCsv(d)

if __name__ == '__main__':
    # get the number of pages we have to scrap

    # url to test: https://chilepropiedades.cl/ver-publicacion/venta-usada/santiago/casa/camino-a-zapallar-parcelacion-los-cristales-lote-20-curico/6692328
    BASE_URL = "https://chilepropiedades.cl"
    URL = BASE_URL + "/propiedades/venta/casa/region-metropolitana-de-santiago-rm/"
    #urltest = "https://chilepropiedades.cl/ver-publicacion/venta-usada/santiago/casa/camino-a-zapallar-parcelacion-los-cristales-lote-20-curico/6692328"
    dataframeVivienda = DataframeVivienda()
    
    urls = [URL + f"{i}" for i in range(1)] # first 5 pages of houses (= 50 houses)
    #dataframeVivienda.getInfoUrl(urltest)

    with mp.Pool(mp.cpu_count()) as pool:
        print("im here")
        pool.map(dataframeVivienda.getInfoUrl, urls) # TRY with nro mas grande (repetidS) and without closing, run it without main 
        # test timing 
        pool.close()

    dataframeVivienda.saveDataInCsvFile()
