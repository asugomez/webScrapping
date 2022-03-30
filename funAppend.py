
def appendElementToList(element, listOfElements, replaceEnter = True, replaceSpace = True, typeElement = "int", otherCharToDelete = []):
    """
    Si el type es float --> reemplazar replace(".","").replace(",",".")
    """
    try:
        if(element != None):
            if(type(element) != str): element = element.text
            if(replaceEnter): element = element.replace("\n","")
            if(replaceSpace): element = element.replace(" ", "")
            if(len(otherCharToDelete) != 0):
                for i in range(len(otherCharToDelete)):
                    element = element.replace(otherCharToDelete[i], "")
            if(typeElement == "int"): element = int(element)
            if(typeElement == "float"): element = float(element.replace(".","").replace(",","."))
        #print("the element: ", element) 
        listOfElements.append(element)
    except Exception as e:
        listOfElements.append(None)
        print("Error: ", e)

def appendPrice(element):
    try:
        valDvs = ""
        if(element != None):
            if(type(element) != str): element = element.text
            element = element.replace("\n","").replace(" ", "")
            if(element.find("$") != -1): # valor CLP
                element = element.replace("$","")
                valDvs = "CLP"
                element = float(element.replace(".","").replace(",","."))
            elif(element.find("UF") != -1): # valor UF
                element = element.replace("UF","")
                valDvs = "UF"
                element = float(element.replace(".","").replace(",","."))
            elif(element.find("USD") != -1):
                element = element.replace("USD","")
                valDvs = "USD"
                element = float(element.replace(".","").replace(",","."))
            else:
                print("WARNING: precio is not in CLP, UF or USD!")
                print(element)
                valDvs = "N/A"
        return (element, valDvs)
    except Exception as e:
        return (None, "N/")
        print("Error: ", e)

        