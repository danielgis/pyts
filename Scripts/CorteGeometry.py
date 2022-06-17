# import modules
import arcpy
import csv

arcpy.env.overwriteOutput = True
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(32718)
print("Modulos importados y entornos configurados.")

# variables
corteXY = r"C:\Student\PYTS\Datos\CorteXY.csv"
outConvexHull = r"C:\Student\PYTS\Datos\Cortes.gdb\AreaAfectadaActual"
outputJoin = r"in_memory\outputJoin"
areaServicio = r"C:\Student\PYTS\Datos\Surquillo.gdb\AreaServicio"
print("Se establecieron las variables.")

# Agregar las coordenadas del csv en una lista
corteCoords = []
csvFile = open(corteXY)
csvReader = csv.reader(csvFile)
next(csvReader)
for row in csvReader:
    corteCoords.append(row)

# Crear un objeto de geometría multipunto a partir de la lista de coordenadas

# Crear límite de interrupción utilizando convexHull (casco convexo)

# Use Spatial Join (unión espacial) para identificar las areas afectadas
arcpy.SpatialJoin_analysis(areaServicio, cortePuntos, outputJoin)
print("Unión espacial terminada.")

# Buscar la salida del join (union)
sFields = ['Join_Count', 'NumArServ']
exp = '"Join_Count" = 1'
print("Areas de servicios afectadas")
with arcpy.da.SearchCursor(outputJoin, sFields, exp) as sCursor:
    for row in sCursor:
        print("Area de servicio: {}".format(row[1]))
del sCursor
print("Analisis completo.")