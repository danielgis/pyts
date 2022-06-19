import arcpy
# Establecer los espacios de trabajo
arcpy.env.workspace = r"C:\Student\PYTS\Datos\Surquillo.gdb"
outWorkspace = r"C:\Student\PYTS\Default.gdb"
fcList = arcpy.ListFeatureClasses("", "Point")
for fc in fcList:
    outputFC= "{}\\{}_copy".format(outWorkspace,fc)
    arcpy.CopyFeatures_management(fc, outputFC)
    print("{} copiado".format(fc))