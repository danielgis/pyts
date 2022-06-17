# importar modulos
import arcpy
import csv
import sys

print("Modulos importados.")

# Crear una clase de excepcion personalizada
class EmptyRows(Exception):
    pass

# variables
CorteXY = r"C:\Student\PYTS\Datos\CorteXY3.csv"
print("Variables configuradas.")


try:
    #Obtener el recuento de filas del CSV
    csvCount = arcpy.GetCount_management(CorteXY)
    if int(csvCount[0]) > 0:
        # Append coordinates from csv in a list and print the first row
        # Agrega coordenadas de un csv a una lista e imprime la primera fila
        corteCoords = []
        csvFile = open(CorteXY)
        csvReader = csv.reader(csvFile)
        next(csvReader)
        for row in csvReader:
            corteCoords.append(row)
        print(corteCoords[0])
    
    else:
        # Excepcion Raise
        raise EmptyRows(csvCount)
except EmptyRows:
    # Mensaje de que el archivo CSV no tiene valores de fila
    print("Error: El archivo {} no tiene valores de fila.".format(CorteXY))
except arcpy.ExecuteError:
    print(arcpy.AddError(arcpy.GetMessages(2)))
except Exception:
    e = sys.exc_info()[1]
    print(e.args[0])


print("Analisis completo.")