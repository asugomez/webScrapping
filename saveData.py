
import pandas as pd 

def createOuputCsv(nameList, columnsList, nameFileCsv = "output.csv"):
    """
    columns list a list of lists 
    """
    # todo asser len namelist == len columnsList
    d = dict(zip(nameList, columnsList))
    dataFrame = pd.DataFrame(d)
    nameFileCsv = "./" + nameFileCsv
    dataFrame.to_csv(nameFileCsv)
