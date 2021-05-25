# Taller 2 - Traceroute

El código principal del taller está en [`taller2.py`](taller2.py), y para
correrlo es necesario descargar las dependencias

```bash
pip3 install requirements.txt
```

Para correrlo,

```bash
sudo IPINFO_ACCESS_TOKEN=<access_token> python3 taller2.py <ip>
```

Consideraciones:

- Como el taller debe ser corrido con `sudo`, puede haber problemas con
  los virtual environments. Nosotros lo solucionamos instalando todo en el
  python del sistema y listo.

- Para obtener la información geográfica de forma programática usamos
  [`ipinfo`](ipinfo.io), que requiere de un *access token* para hacer los
  requests. El programa lo toma de la variable de entorno `IPINFO_ACCESS_TOKEN`,
  y si quieren correrlo de 0 pueden usar el que usamos nosotros, que les pasamos
  por mail.

## Estructura

- En la carpeta `out` se disponen las salidas de cada corrida.
- En `img` se encuentran las imágenes generadas en los *jupyter notebooks*.
- En `graficos.ipynb` se encuentra el análisis de los resultados.
- Finalmente, en `cimbala.pynb` y `thomson.py` se encuentra el código adicional para la realización del apartado opcional.
