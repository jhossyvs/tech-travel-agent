import requests

def obtener_clima_real(ciudad: str) -> str:
    try:
        geo = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={
                "name": ciudad,
                "count": 1,
                "language": "es",
            },
            timeout=10,
        )
        geo.raise_for_status()

        datos = geo.json()

        if not datos.get("results"):
            return f"No encontré la ciudad '{ciudad}'."

        lugar = datos["results"][0]

        clima = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lugar["latitude"],
                "longitude": lugar["longitude"],
                "current": "temperature_2m,wind_speed_10m",
            },
            timeout=10,
        )
        clima.raise_for_status()

        actual = clima.json()["current"]

        return (
            f"{lugar['name']}: "
            f"{actual['temperature_2m']} °C, "
            f"viento de {actual['wind_speed_10m']} km/h"
        )

    except requests.exceptions.Timeout:
        return "No pude consultar el clima porque el servicio tardó demasiado en responder."

    except requests.exceptions.RequestException:
        return "No pude consultar el clima porque el servicio meteorológico no está disponible."

    except (KeyError, ValueError):
        return "Recibí una respuesta inesperada del servicio meteorológico."