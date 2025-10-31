from ..db.managementDB import getDataForML


# sobreescribir predictSales.pkl
def generateML():

    # fetch BD
    dataFrame = getDataForML()
    print(dataFrame)


    # modifica DF
    # exporta modelo