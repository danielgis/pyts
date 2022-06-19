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
ListaPuntos = []
#--Recorremos la lista de Coordenadas de corte
for itemCoordenadas in corteCoords:
    #--creamos un objeto Punto en base a las coordenadas XY
    oPunto = arcpy.Point(itemCoordenadas [1], itemCoordenadas[2])
    #--Agregamos el Punto a la colección de objetos Puntos
    ListaPuntos.append(oPunto)
#--Creamos un Arreglo de Puntos en base a lista de Puntos
ArrayPuntos = arcpy.Array(ListaPuntos)
#--Creamos una geometría de tipo Multipunto
cortePuntos = arcpy.Multipoint(ArrayPuntos)
#--Imprimimos el mensaje en consola
print("Se creo el objeto de geometría.")
# Crear límite de interrupción utilizando convexHull (casco convexo)
convexHull = cortePuntos.convexHull()
#--Copiamos los nuevos Features y lo almacenamos en una variable
arcpy.CopyFeatures_management(convexHull, outConvexHull)
#--Imprimimos el mensaje en consola
print("Limite de interrupción creado.")# Crear límite de interrupción utilizando convexHull (casco convexo)

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