import geopy.distance
import requests

# Clave API de OpenCage
API_KEY = '4f5dc70dd1f2497aade8783ec5ad81b8'

def obtener_coordenadas(ciudad, pais):
    try:
        response = requests.get(f'https://api.opencagedata.com/geocode/v1/json?q={ciudad},{pais}&key={API_KEY}')
        response.raise_for_status()
        data = response.json()
        if data['results']:
            return (data['results'][0]['geometry']['lat'], data['results'][0]['geometry']['lng'])
        else:
            print(f"No se encontraron coordenadas para {ciudad}, {pais}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener coordenadas: {e}")
        return None

def calcular_distancia(coord1, coord2):
    return geopy.distance.distance(coord1, coord2).km

def obtener_duracion_viaje(ciudad_origen, ciudad_destino, transporte):
    try:
        # Cambiar transporte de español a inglés
        if transporte.lower() == 'manejando':
            transporte = 'driving'
        elif transporte.lower() == 'caminando':
            transporte = 'walking'
        elif transporte.lower() == 'bicicleta':
            transporte = 'cycling'

        url = f"http://router.project-osrm.org/route/v1/{transporte}/{ciudad_origen[1]},{ciudad_origen[0]};{ciudad_destino[1]},{ciudad_destino[0]}?overview=false"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data['routes']:
            duracion_segundos = data['routes'][0]['duration']
            return duracion_segundos / 3600  # convertir a horas
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener la duración del viaje: {e}")
    return None

def main():
    while True:
        ciudad_origen = input("Ingrese Ciudad de Origen (o 's' para salir): ")
        if ciudad_origen.lower() == 's':
            break
        ciudad_destino = input("Ingrese Ciudad de Destino (o 's' para salir): ")
        if ciudad_destino.lower() == 's':
            break
        transporte = input("Ingrese el medio de transporte (manejando, caminando, bicicleta) (o 's' para salir): ")
        if transporte.lower() == 's':
            break

        coordenadas_origen = obtener_coordenadas(ciudad_origen, "Chile")
        coordenadas_destino = obtener_coordenadas(ciudad_destino, "Argentina")

        if coordenadas_origen and coordenadas_destino:
            distancia_km = calcular_distancia(coordenadas_origen, coordenadas_destino)
            distancia_millas = distancia_km * 0.621371

            duracion_horas = obtener_duracion_viaje(coordenadas_origen, coordenadas_destino, transporte)

            print(f"\nNarrativa del Viaje:")
            print(f"De {ciudad_origen} a {ciudad_destino}:")
            print(f"Distancia: {distancia_km:.2f} km ({distancia_millas:.2f} millas)")
            if duracion_horas:
                print(f"Duración del viaje: {duracion_horas:.2f} horas\n")
            else:
                print("No se pudo calcular la duración del viaje.\n")
        else:
            print("No se pudieron obtener las coordenadas de las ciudades ingresadas.\n")

if __name__ == "__main__":
    main()