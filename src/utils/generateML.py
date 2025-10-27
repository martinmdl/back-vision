from ..db.managementDB import getDataForML


# sobreescribir predictSales.pkl
def generateML():

    # fetch BD
    dataFrame = getDataForML()
    

    # modifica DF
    # exporta modelo