# Importar modulo
import arcpy
# Configurar variable
fc = r"C:\Student\PYTS\Datos\Surquillo.gdb\ParcelasPts"
# Actualizar el valor por metro cuadrado con el cursor Update
uFields = ['MetroCdo', 'TaxValue', 'PrecioMtrCdo']
with arcpy.da.UpdateCursor(fc, uFields) as uCursor:
      for row in uCursor:
           row[2] = row[1] / row[0]
           uCursor.updateRow(row)

# Establecer variables para el cursor de búsqueda
sFields = ["PARCELCODE","PROPIETARIO","NUMTELEF","PrecioMtrCdo"]
exp = '"PrecioMtrCdo" <= 90'
# Rellenar los nombres de campo para el archivo CSV desde el cursor de búsqueda
parcelList = ["PARCELCODE,PROPIETARIO,NUMTELEF,PrecioMtrCdo"]
with arcpy.da.SearchCursor(fc, sFields, exp) as sCursor:
    for row in sCursor:
        rowText = "{},{},{},{}".format(row[0],row[1],row[2],row[3])
        parcelList.append(rowText)

# Escribir mensajes en un archivo CSV
textBody = '\n'.join(parcelList)
csvFile = open(r"C:\Student\PYTS\ValoracionDeParcelas.csv", "w")
csvFile.write(textBody)
csvFile.close()
print("Script Completado")