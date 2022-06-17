# Importar modulo
import arcpy

# Acceder al objeto describe
desc = arcpy.Describe(r'C:\Student\PYTS\Datos\Surquillo.gdb\ParcelasPts')
# Variable para propiedades
dPath = desc.path
print(dPath)
dName = desc.baseName
dGeometry = desc.shapeType
dCoord = desc.spatialReference
# Modificar el nombre del feature class de salida
newName = "{}_Nuevo".format(dName)
print(newName)
# Crear un nuevo feature class
arcpy.CreateFeatureclass_management(dPath, newName, dGeometry, None, "", "", dCoord)
print("Script completado")

hasattr(r'C:\Student\PYTS\Datos\Surquillo.gdb\ParcelasPts')