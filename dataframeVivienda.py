from connexion import *
from saveData import *
from funAppend import *
import multiprocessing as mp

class DataframeVivienda:

    def __init__( self, Codigo_Aviso = [], Comuna = [], Link = [], Tipo_Vivienda = [], N_Habitaciones  = [], N_Baños = [], N_Estacionamientos = [], Amoblado = [], Total_Superficie_M2 = [], Superficie_Construida_M2 = [], anoConstruccion = [], Valor_UF = [], Valor_CLP = [], Dirección = [], tipoPublicacion = [], Quién_Vende = [], Corredor = [], fechaPublicacion = []):
        self.Codigo_Aviso           = Codigo_Aviso
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
        self.Dirección              = Dirección
        self.tipoPublicacion        = tipoPublicacion
        self.Quién_Vende             = Quién_Vende
        self.Corredor               = Corredor
        self.fechaPublicacion       = fechaPublicacion
    
     
    def getNPagesToScrap(URL):
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
            
            # get the info from this link
            housePage = requestURL(finalLink)
            #if(housePage == None): print("The url is: ", finalLink)
            if(housePage != None):
                # append link to list
                self.Link.append(finalLink)
                main = housePage.select_one("div.clp-administration-main-panel div.clp-details-table")
                footmain = housePage.select_one("div.clp-administration-main-panel div.clp-publication-contact-box")

                ### codigo aviso 
                codigoAviso = main.select_one("div:-soup-contains('Código aviso') ~ div.clp-description-value")
                appendElementToList(codigoAviso, self.Codigo_Aviso, replaceEnter = True, replaceSpace = False, typeElement = "str")

                ## precios CLP y UF
                # los valores estan en CLP y UF, pero cambia el orden segun el anuncio
                # además se debe modificar el texto para que quede solo el string del numero y sea convertible en float
                # por eso se le saca " " y los puntos, y se modifican las comas por puntos
                # cread dictionary para guardar en clp y uf los precios, si ambos estan bien se agregan, sino, se pone None
                dict_price = dict()
                ### precio 1
                precio1 = main.select_one("div:-soup-contains('Valor:') ~ div.clp-description-value")
                valPrecio1, divisa = appendPrice(precio1)
                dict_price[divisa] = valPrecio1
                ### precio 2
                precio2 = main.select_one("div:-soup-contains('Valor (') ~ div.clp-description-value > span")
                valPrecio2, divisa = appendPrice(precio2)
                dict_price[divisa] = valPrecio2

                if "CLP" in dict_price.keys():
                    self.Valor_CLP.append(dict_price["CLP"])
                    # caso: CLP y UF
                    if "UF" in dict_price.keys():
                        self.Valor_UF.append(dict_price["UF"])
                    # caso: CLP y N/A
                    else:
                        # agrego none a ambas divisas
                        print("WARNING: UF NONE")
                        self.Valor_UF.append(None)
                elif "UF" in dict_price.keys():
                    print("WARNING: CLP NONE")
                    self.Valor_UF.append(dict_price["UF"])
                    self.Valor_CLP.append(None)
                else:
                    print("WARNING NONE IN UF AND CLP")
                    self.Valor_CLP.append(None)
                    self.Valor_UF.append(None)

                


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
            else:
                print("WATNING: housepage null: ", finalLink)    
        


    def saveDataInCsvFile(self):
        d = self.__dict__
        dict_gral = dict()
        # dict_keys(['Comuna', 'Link', 'Tipo_Vivienda', 'N_Habitaciones', 'N_Baños', 'N_Estacionamientos', 'Amoblado', 'Total_Superficie_M2', 'Superficie_Construida_M2', 'anoConstruccion', 'Valor_UF', 'Valor_CLP', 'Dirección', 'tipoPublicacion', 'Quién_Vende', 'Corredor', 'fechaPublicacion', 'Codigo_Aviso'])
        for key, val in d.items():
            dict_gral[key] = val[:]

        # print(len(self.Comuna))
        # print(len(self.Link))
        # print(len(self.Tipo_Vivienda))
        # print(len(self.N_Habitaciones))
        # print(len(self.N_Baños))
        # print(len(self.N_Estacionamientos))
        # print(len(self.Amoblado))
        # print(len(self.Total_Superficie_M2))
        # print(len(self.Superficie_Construida_M2))
        # print(len(self.anoConstruccion))
        # print(len(self.Valor_UF))
        # print(len(self.Valor_CLP))
        # print(len(self.Dirección))
        # print(len(self.tipoPublicacion))
        # print(len(self.Quién_Vende))
        # print(len(self.Corredor))
        # print(len(self.fechaPublicacion))
        # print(len(self.Codigo_Aviso))

        createOuputCsv(dict_gral, "dtgeneral.csv")

if __name__ == '__main__':
    # get the number of pages we have to scrap

    # url to test: https://chilepropiedades.cl/ver-publicacion/venta-usada/santiago/casa/camino-a-zapallar-parcelacion-los-cristales-lote-20-curico/6692328
    BASE_URL = "https://chilepropiedades.cl"
    URL = BASE_URL + "/propiedades/venta/casa/region-metropolitana-de-santiago-rm/"
    #urltest = "https://chilepropiedades.cl/ver-publicacion/venta-usada/santiago/casa/camino-a-zapallar-parcelacion-los-cristales-lote-20-curico/6692328"
    manager = mp.Manager()
    dataframeVivienda = DataframeVivienda(Codigo_Aviso=manager.list(), Comuna= manager.list(), Link= manager.list(), Tipo_Vivienda= manager.list(), N_Habitaciones= manager.list(), N_Baños= manager.list(), N_Estacionamientos=manager.list(), Amoblado=manager.list(), Total_Superficie_M2=manager.list(), Superficie_Construida_M2=manager.list(), anoConstruccion=manager.list(), Valor_UF=manager.list(),Valor_CLP=manager.list(), Dirección=manager.list(), tipoPublicacion=manager.list(), Quién_Vende=manager.list(), Corredor=manager.list(), fechaPublicacion=manager.list())

    npages = DataframeVivienda.getNPagesToScrap(URL)
    print(npages)

    urls = [URL + f"{i}" for i in range(npages)] # first 5 pages of houses (= 50 houses)

    pool = mp.Pool(mp.cpu_count())
    results = pool.map(dataframeVivienda.getInfoUrl, urls)

    dataframeVivienda.saveDataInCsvFile()

