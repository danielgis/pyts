#Asignar variables a los shapefiles
localidad = "localidad_surco.shp"
manzanas = "mz_surco.shp"
calles = "street_surco.shp"


# Crear y abrir un nuevo archivo de texto para un shapefile actualizado
ruta = r"C:\Student\PYTS\SantiagoSurcoActualizado.txt"
file = open(ruta, 'w')

# Crear ua lista de variables de shapefile
shapeList = [localidad, manzanas, calles]

# Actualizar los nombres de los shapefiles de la lista

for shp in shapeList:
    print (shp)
    shp = shp.replace("surco", "SURCO")
    print (shp)
    file.write(shp + "\n")

file.close()
