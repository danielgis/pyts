####################################################################################
# Name: CorteEnergia.py
# Descripcion: Script de corte de energía para usarlo con la herramienta de script
# Autor: TELEMATICA
# Curso: PYTS
####################################################################################

# importar modulos
import arcpy
import csv
import sys

# Crea clases de excepción personalizadas para la gestion de errores


class phoneEmptyRows(Exception):
    pass


class xyEmptyRows(Exception):
    pass


# Configurar el entorno
arcpy.env.workspace = r"C:\Student\PYTS\Datos"
arcpy.env.overwriteOutput = True

# Establecer parámetros para archivos de entrada/salida
# Archivos de corte de entrada
repTelFile = r"C:\Student\PYTS\Datos\ReporteTelefonico.csv"
xyFile = r"C:\Student\PYTS\Datos\ReporteRedesSociales.xlsx\RedesSocialesXY$"
ptFile = r"C:\Student\PYTS\Datos\ReporteApp.shp"
parcelPoints = r"C:\Student\PYTS\Datos\Surquillo.gdb\ParcelasPts"
serviceAreas = r"C:\Student\PYTS\Datos\Surquillo.gdb\AreaServicio"
outputGDB = r"C:\Student\PYTS\Datos\Cortes.gdb"


# Derivado de parámetros de entrada
serviceAreasJoin = "in_memory\\join"
# outages = "{0}\Outages".format(outputGDB)
# outageDensity = "{0}\OutageDensity".format(outputGDB)
# outConvexHull = "{0}\OutageArea".format(outputGDB)
Cortes = outputGDB + "\\Cortes"
outageDensity = outputGDB + "\\DensidadDeCorte"
outConvexHull = outputGDB + "\\AreaDeCorte"

# Gestion del error
try:
    # Importar el shapefile de puntos de la App en la geodatabase
    # print ("Importar puntos de la App al FC Cortes")
    arcpy.AddMessage("Importando puntos de la App en el FC Cortes")
    arcpy.FeatureClassToFeatureClass_conversion(ptFile, outputGDB, 'Cortes')
    # crear un archivo de puntos del Excel de redes sociales y agregarlo al FC Cortes
    # print("Creando FC de puntos desde la tabla redes sociales")
    arcpy.AddMessage("Creando FC de puntos desde la tabla redes sociales")

    # Obtener el recuento de filas en el archivo XY para la gestion de errores
    xyCount = arcpy.GetCount_management(xyFile)
    if int(xyCount[0]) > 0:
        xyEvent = "XY_Event_Layer"
        spatialRef = arcpy.SpatialReference(32718)
        arcpy.MakeXYEventLayer_management(xyFile, "Point_X", "Point_Y", xyEvent, spatialRef)
        arcpy.Append_management(xyEvent, Cortes, "NO_TEST")
    else:
        # Excepcion Raise
        raise phoneEmptyRows(xyCount)

    # Desde el csv de reporte teléfonico buscara numeros en el FC ParcelasPts usando el cursor Search.
    # Obten la geometria de shapeXY y agregalo a una lista
    print("Buscando numeros de telefono")
    arcpy.AddMessage("Buscando numeros de telefono")
    # Obten el recuento de filas en CSV para la gestion de errores
    pNumCount = arcpy.GetCount_management(repTelFile)
    arcpy.AddMessage("{} numeros de telefono".format(pNumCount))
    if int(pNumCount[0]) > 0:
        pList = []
        csvFile = open(repTelFile)
        csvReader = csv.reader(csvFile)
        for row in csvReader:
            with arcpy.da.SearchCursor(parcelPoints, ['NUMTELEF', 'SHAPE@XY']) as sCursor:
                for sRow in sCursor:
                    if row[0] == sRow[0]:
                        pList.append(sRow[1])
            del sCursor
    else:
        # Excepcion Raise
        raise xyEmptyRows(pNumCount)

    # Insertar la geometria de shapexy desde la lista hacia el FC Cortes 'PhoneNum_1'
    print("Insertando los numeros de telefono de los puntos en el FC Cortes")
    arcpy.AddMessage("Insertando los numeros de telefono de los puntos en el FC Cortes")
    iCursor = arcpy.da.InsertCursor(Cortes, ['SHAPE@X', 'SHAPE@Y'])
    for pRow in pList:
        iCursor.insertRow(pRow)
    del iCursor

    # Crear un mapa de kernel density

    print("Creando Kernel density")
    arcpy.AddMessage("Creando Kernel density")
    #arcpy.env.extent = arcpy.Extent(2053764.41650888, 507185.366399556, 2115439.05332997, 551798.058013887)
    populationField = "NONE"
    cellSize = ""
    searchRadius = ""
    outKernelDensity = arcpy.sa.KernelDensity(Cortes, populationField, cellSize, searchRadius, "SQUARE_METERS")
    outKernelDensity.save(outageDensity)

    # Crear convex hull
    # Crear FC multipunto desde puntos
    print("Creando convex hull")
    arcpy.AddMessage("Creando convex hull")
    multipoints = arcpy.Dissolve_management(in_features=Cortes,
                                            out_feature_class=r"in_memory\multi",
                                            dissolve_field=None,
                                            multi_part=True)
    points = [f[0].convexHull() for f in arcpy.da.SearchCursor(multipoints, "SHAPE@")]
    arcpy.CopyFeatures_management(points, outConvexHull)

    # Determine qué areas de servicio necesitan enviarse
    print("Uniendo los puntos de Corte con Area de Servicio")
    arcpy.AddMessage("Uniendo los puntos de Corte con Area de Servicio")
    arcpy.SpatialJoin_analysis(serviceAreas, Cortes, serviceAreasJoin, "JOIN_ONE_TO_ONE", "KEEP_ALL", "", "INTERSECT")

    # print("Obtener cortes ordenados por area de servicio")
    # arcpy.AddMessage("Obtener cortes ordenados por area de servicio")
    # jCursor = sorted(arcpy.da.SearchCursor(serviceAreasJoin, ["ServArNu","Join_Count"]))
    # for jRow in jCursor:
    #     print("Area de Servicio {}: {} cortes".format(str(jRow[0]), str(jRow[1])))
    #     arcpy.AddMessage("Area de Servicio {}: {} cortes".format(str(jRow[0]), str(jRow[1])))
    # del jCursor

    # print("Obtener cortes ordenados por el numero total de cortes")
    arcpy.AddMessage("Obtener cortes ordenados por el numero total de cortes")
    jCursor = sorted(arcpy.da.SearchCursor(serviceAreasJoin, ["Join_Count", "NumArServ"]), reverse=True)
    for jRow in jCursor:
        # print("Area de Servicio {}: {} cortes".format(str(jRow[1]), str(jRow[0])))
        arcpy.AddMessage("Area de Servicio {}: {} cortes".format(str(jRow[1]), str(jRow[0])))
    del jCursor
    # print("Script completado")

except phoneEmptyRows:
    # Mensaje de que el archivo CSV no tiene valores de fila
    # print("Error: El archivo {} no tiene valores de fila".format(xyFile))
    arcpy.AddError("Error: El archivo {} no tiene valores de fila".format(xyFile))

except xyEmptyRows:
    # Mensaje de que el archivo CSV no tiene valores de fila
    # print("Error: El archivo {} no tiene valores de fila".format(pNumFile))
    arcpy.AddError("Error: El archivo {} no tiene valores de fila".format(repTelFile))

except arcpy.ExecuteError:
    arcpy.AddError(arcpy.GetMessages(2))

except Exception:
    e = sys.exc_info()[1]
    # print(e.args[0])
    arcpy.AddError(e.args[0])

# Agregar la salida al mapa
aprx = arcpy.mp.ArcGISProject(r"C:\Student\PYTS\Proyectos\DensidadPoblacional\DensidadPoblacional.aprx")
m = aprx.listMaps("HerramientaScript")[0]

m.addDataFromPath(outConvexHull)
m.addDataFromPath(Cortes)
densityLyr = arcpy.mp.LayerFile(r"C:\Student\PYTS\Datos\CorteDensity.lyrx")
m.addLayer(densityLyr)
del aprx