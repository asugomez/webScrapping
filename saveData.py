
import pandas as pd 

def createOuputCsv(nameCols, columnsList, nameFileCsv = "output.csv"):
    """
    columns list a list of lists 
    """
    # todo asser len namelist == len columnsList
    d = dict(zip(nameCols, columnsList))
    createOuputCsv(dictionary, nameFileCsv)

def createOuputCsv(dictionary, nameFileCsv = "output.csv"):
    #print("dict: ", dictionary)
    print(dictionary.keys())
    dataframe = pd.DataFrame.from_dict(dictionary)
    nameFileCsv = "./" + nameFileCsv
    dataframe.to_csv(nameFileCsv)

