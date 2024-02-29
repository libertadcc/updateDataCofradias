from arcgis.gis import GIS

gis = GIS("https://www.arcgis.com", "liber.preventas", "******")

import requests

url = "https://dtd008cofradiasapi.azurewebsites.net/api/Localizacion/UltimasTiempo?ultimosMinutos=100000000"
payload = {}

response = requests.request("GET", url, data=payload)

data = response.json()

features = []

for dato in data['Resul']:
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [
                float(dato["Longitud"]),
                float(dato["Latitud"])
            ]
        },
        "properties": {
            "IdLocalizacion": dato['IdLocalizacion'],
            "IdProcesion": dato['IdProcesion'],
            "IdPaso": dato["IdPaso"],
            "IdTipoPosicion": dato["IdTipoPosicion"],
            "Fecha": dato["Fecha"],
            "Paso": dato["Paso"],
            "ProcesionNombre": dato['Procesion']['ProcesionNombre'],
            "ProcesionDescription": dato['Procesion']['ProcesionDescripcion'],
            "ProcesionImagen": dato['Procesion']['ProcesionImagen'],
            "IdAsociacionPrincipal": dato['Procesion']['IdAsociacionPrincipal'],
            "MusicaDescripcion": dato['Procesion']['MusicaDescripcion'],
            "CruzGuiaDescripcion": dato['Procesion']['CruzGuiaDescripcion'],
            "CruzGuiaImagen": dato['Procesion']['CruzGuiaImagen'],
            "PrevistoFechaInicio": dato['Procesion']['PrevistoFechaInicio'],
            "PrevistoFechaFin": dato['Procesion']['PrevistoFechaFin'],
            "NumeroPasos": dato['Procesion']['NumeroPasos'],
            "Color": dato['Procesion']['Color'],
            "Asociacion": dato['Procesion']['Asociacion'],
            "ConfDispositivos": dato['Procesion']['ConfDispositivos']
            }
        }
    features.append(feature)

geojson_data = {
    "type": "FeatureCollection",
    "features": features
}


import tempfile
import json

# Crear un archivo temporal y escribir los datos GeoJSON en él
with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as temp_file:
    temp_file.write(json.dumps(geojson_data).encode('utf-8'))

# Definir las propiedades del item
item_properties = {
    "type": "GeoJson",  # Especificamos el tipo de contenido como 'GeoJson'
    "title": "cofradias1"
}

# Publicar el archivo GeoJSON como un Feature Layer alojado
item = gis.content.add(item_properties, temp_file.name)
feature_layer_item = item.publish()

print("Feature Layer publicado:", feature_layer_item)
