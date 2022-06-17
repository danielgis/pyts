# coding: utf-8
# Importar modulo
import arcpy

print("Modulo arcpy importado")
arcpy.env.overwriteOutput = True
# Establecer variables
output = r"C:\Student\PYTS\Default.gdb\CopiaDePoblacion"
rasterName = r"C:\student\PYTS\Default.gdb\KernelDensityPob"
shpInput = r"C:\Student\PYTS\Datos\Poblacion.shp"
print("Variables configuradas")
# Agregar shapefile a la geodatabase
# arcpy.management.CopyFeatures('Poblacion', output)
arcpy.management.CopyFeatures(shpInput, output)
print("Shapefile importado a la geodatabase")
# Calcular la densidad de población a partir de puntos
KernelDensityPob = arcpy.sa.KernelDensity(output, 'NONE')
KernelDensityPob.save(rasterName)
print("Kernel density calculado \nScript completado")