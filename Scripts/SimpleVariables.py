# coding: utf-8
output = r"C:\Student\PYTS\Default.gdb\CopiaDePoblacion"
rasterName = r"C:\Student\PYTS\Default.gdb\KernelDensityPob"
arcpy.management.CopyFeatures('Poblacion', output)
# <Result 'C:\\Student\\PYTS\\Default.gdb\\CopiaDePoblacion'>
KernelDensityPob = arcpy.sa.KernelDensity(output, 'NONE')
KernelDensityPob.save(rasterName)

