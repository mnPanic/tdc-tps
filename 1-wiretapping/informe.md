# Informe

## Integrantes

| LU     | Nombre            | Mail                      |
| ------ | ----------------- | ------------------------- |
| 72/18  | Manuel Panichelli | panicmanu@gmail.com       |
| 76/16  | Luciano Strika    | lucianostrika44@gmail.com |
| 692/12 | Elías Cerdeira    | eliascerdeira@gmail.com   |

## Introducción

<!-- 200 -->

En este trabajo se elabora un programa que modela el tráfico de una red con dos fuentes de memoria nula distintas. Por un lado, analizaremos todos los paquetes que circulan por la red, que serán distinguidos por el tipo de protocolo y la dirección destino (*UNICAST* o *BROADCAST*). Por el otro, analizamos limitándonos a los paquetes ARP distinguiéndolos por direccion de destino y fuente para enumerar, finalmente, a todos los hosts de una red.

## Métodos y condiciones de los experimentos

<!-- 400 -->

Para la ejecución de los experimentos se partió del código provisto por la cátedra, extendiendo el método `mostrar_fuente`, agregándole el cálculo de la información de cada símbolo y la entropía de la fuente para 15000 tramas.

Se ejecutó el programa en tres redes distintas el 1/05/2021 aproximadamente a las 20:00 (GMT-3).

- Red 1 (Manuel): Consta de una computadora de escritorio conectada por UTP, un celular y una tele.
- Red 2 (Luciano): Solo consta de una Notebook, el router y un celular conectados por Wi-Fi.
- Red 3 (Elías): Consta de 11 dispositivos. 2 Notebooks, 3 televisores, 2 decodificadores, 1 impresora y 3 celulares.

### Fuente de memoria nula para distinguir hosts de la red

Para hallar los hosts conectados a una red determinada, bastará con hallar todas las IPs que participan de la comunicación en el medio compartido. Esto es: todas las que envían o reciben paquetes ARP.

Para esto, se eligió modelar una fuente de memoria nula S2, en la que tratamos como símbolo distinguido a cada IP de fuente en un paquete ARP. También se eligió modelar otra fuente, en la que los símbolos son las IP de destino, y se observó las distribuciones de ambas, y cuántos nodos aparecían.

## Resultados de los experimentos

<!-- 600 -->

Resultado de análisis de protocolos, para cada red

1. (Manuel)

  | Tipo de mensaje | Protocolo            | Probabilidad | Información |
  | --------------- | -------------------- | ------------ | ----------- |
  | UNICAST         | 2048 (IPv4)          | 0.99640      | 0.00520     |
  | BROADCAST       | 2054 (ARP)           | 0.00220      | 8.82828     |
  | BROADCAST       | 2048 (IPv4)          | 0.00073      | 10.41324    |
  | UNICAST         | 35130 (IEEE 1905.1a) | 0.00027      | 11.87267    |
  | UNICAST         | 35020 (LLDP)         | 0.00027      | 11.87267    |
  | UNICAST         | 2054 (ARP)           | 0.00013      | 12.87267    |

  Entropía: 0.0403

2. (Luciano)

  | Tipo de mensaje | Protocolo | Probabilidad | Información |
  | --------------- | --------- | ------------ | ----------- |
  | UNICAST         | 2048      | 0.99920      | 0.00115     |
  | UNICAST         | 2054      | 0.00080      | 10.28771    |

  Entropía: 0.0093

3. (Elías)

  | Tipo de mensaje | Protocolo                | Probabilidad | Información |
  | --------------- | ------------------------ | ------------ | ----------- |
  | UNICAST         | 2048 (IPv4)              | 0.96774      | 0.047       |
  | UNICAST         | 34525 (IPv6)             | 0.01453      | 14.1        |
  | BROADCAST       | 33024 (IEEE 802.1Q VLAN) | 0.00640      | 16.83       |
  | BROADCAST       | 2054 (ARP)               | 0.00507      | 17.6        |
  | UNICAST         | 33024 (IEEE 802.1Q VLAN) | 0.00380      | 18.56       |
  | UNICAST         | 2054 (ARP)               | 0.00120      | 22.4        |
  | BROADCAST       | 2048 (IPv4)              | 0.00113      | 22.6        |
  | BROADCAST       | 34999 (OUI EE)           | 0.00013      | 29.73       |

  Entropía: 2.111

Viendo estos datos, podemos responder algunas incógnitas sobre los mismos.

- **¿Considera que las muestras obtenidas analizadas son representativas del comportamiento general de la red?**

  Se considera que la muestra tomada es representativa de las tres redes estudiadas, ya que predominan los paquetes IP y ARP.

- **¿Hay alguna relación entre la entropía de las redes y alguna característica de las mismas (ej.: tamaño, tecnología, etc)?**

  A mayor tamaño y diversidad tecnológica de la red (e.g. usar IPv6), mayor la entropía.
  
- **¿En alguna red la entropía de la fuente alcanza la entropía máxima teórica?**
  
  El máximo teórico se daría si cada paquete presentara un símbolo nuevo. En ese caso, la entropía divergería. Evidentemente, hay un límite en la cantidad de protocolos observables, y estuvimos lejos del límite habiendo en total menos 10 protocolos distintos observados que pueden ser fácilmente representarse en 3 bits.

- **¿Considera significativa la cantidad de tráfico broadcast sobre el tráfico total?**
  
  La cantidad de tráfico broadcast es despreciable en comparación al unicast.

- **¿Cuál es la función de cada uno de los protocolos encontrados? ¿Cuáles son protocolos de control y cuáles transportan datos de usuario? ¿Ha encontrado protocolos no esperados? ¿Puede describirlos?**

  Se encontraron los siguientes protocolos (Buscados en [IANA IEEE 802 Numbers](https://www.iana.org/assignments/ieee-802-numbers/ieee-802-numbers.xhtml) y Wireshark)

  Los protocolos esperados encontrados fueron IPv4, IPv6 (Transportan datos de usuario) y ARP (Protocolo de control). Luego se encontraron estos protocolos que no se esperaba observar

  - `35020` (LLDP) Link Layer Discovery Protocol, usado por dispositivos para darse a conocer en la LAN.
  - `35130` (IEEE 1905.1a) Protocolo usado para redes domésticas (con soporte para wireless).
  - `33024` (IEEE 802.1Q VLAN) Estándar de redes para VLAN en Ethernet.
  - `34999` (OUI EE)
  - `35020` (LLDP): IEEE Std 802.1AB - Link Layer Discovery Protocol

Preguntas agregadas:

- **¿Se mantiene esta distribución estable en el tiempo?**

  Sí. Se replicaron los experimentos para las mismas redes 5 veces y no se observaron diferencias significativas en los resultados.

### Resultados de experimentos con IP distinguidas

Al sniffear los paquetes de ARP de nuestras redes, conservando las IP como símbolos distinguidos, presentan el siguiente comportamiento:

1. (Manuel)
  
  Source:

  | IP          | Probabilidad | Información |
  | ----------- | ------------ | ----------- |
  | 192.168.0.4 | 0.95000      | 0.07400     |
  | 192.168.0.8 | 0.02000      | 5.64386     |
  | 192.168.0.6 | 0.02000      | 5.64386     |
  | 192.168.0.1 | 0.01000      | 6.64386     |

  Entropía: 0.3625

  Destination:

  | IP           | Probabilidad | Información |
  | ------------ | ------------ | ----------- |
  | 192.168.0.1  | 0.95000      | 0.07400     |
  | 192.168.0.10 | 0.02000      | 5.64386     |
  | 192.168.0.6  | 0.02000      | 5.64386     |
  | 192.168.0.4  | 0.01000      | 6.64386     |

  Entropía: 0.3625

2. (Luciano)

  Source:

  | IP            | Probabilidad | Información |
  | ------------- | ------------ | ----------- |
  | 192.168.0.1   | 0.50000      | 1.00000     |
  | 192.168.0.181 | 0.50000      | 1.00000     |

  Entropía: 1.0

  Destination:

  | IP            | Probabilidad | Información |
  | ------------- | ------------ | ----------- |
  | 192.168.0.1   | 0.50000      | 1.00000     |
  | 192.168.0.181 | 0.50000      | 1.00000     |

  Entropía: 1.0

3. (Elías)

  Source:

  | IP            | Probabilidad | Información |
  | ------------- | ------------ | ----------- |
  | 192.168.1.54  | 0.63000      | 0.46204     |
  | 192.168.1.1   | 0.26000      | 1.34707     |
  | 192.168.1.51  | 0.08000      | 2.52573     |
  | 192.168.1.201 | 0.01000      | 4.60517     |
  | 192.168.1.200 | 0.01000      | 4.60517     |
  | 192.168.1.39  | 0.01000      | 4.60517     |

  Entropía: 0.9815

  Destination:

  | IP            | Probabilidad | Información |
  | ------------- | ------------ | ----------- |
  | 192.168.1.1   | 0.66000      | 0.41552     |
  | 192.168.1.51  | 0.10000      | 2.30259     |
  | 192.168.1.54  | 0.03000      | 3.50656     |
  | 192.168.1.200 | 0.03000      | 3.50656     |
  | 192.168.1.41  | 0.02000      | 3.91202     |
  | 192.168.1.58  | 0.02000      | 3.91202     |
  | 192.168.1.65  | 0.02000      | 3.91202     |
  | 192.168.1.33  | 0.02000      | 3.91202     |
  | 192.168.1.52  | 0.02000      | 3.91202     |
  | 192.168.1.64  | 0.02000      | 3.91202     |
  | 192.168.1.201 | 0.02000      | 3.91202     |
  | 192.168.1.39  | 0.02000      | 3.91202     |
  | 192.168.1.63  | 0.01000      | 4.60517     |
  | 192.168.1.36  | 0.01000      | 4.60517     |

  Entropía: 1.4330

- **¿La entropía de la fuente es máxima? ¿Qué sugiere esto acerca de la red?**
  Si fuera máxima la entropía, la distribución de los símbolos sería uniforme, por lo que todos los dispositivos tendrían que estar enviándose o recibiendo paquetes entre sí con una porción del tráfico.

  Esto no se da en ninguna de las redes observadas, ya que en todas algún nodo -teorizamos que es el del router- domina por sobre el resto.

- **¿Se pueden distinguir nodos? ¿Se les puede adjudicar alguna función específica?**
  Sí, en todos existe un nodo con mayor participación del tráfico, y un segundo nodo distinguible, mientras que el resto, si existen, envían una fracción despreciable de los paquetes ARP. Creemos que el de mayor tráfico es el nodo del Router, y el segundo el de la PC con la que hacemos este trabajo.

- **¿Hay evidencia parcial que sugiera que algún nodo funciona de forma anómala y/o no esperada?**
  No, aunque hubiera sido interesante descubrir más dispositivos de los esperados, o uno desconocido enviando gran parte del tráfico, sugiriendo un posible actor malicioso.

- **¿Existe una correspondencia entre lo que se conoce de la red y los nodos distinguidos detectados por la herramienta?**
  Sí, de hecho detectamos casi exactamente lo que esperábamos, dado nuestro conocimiento de la topología de las redes.

- **¿Ha encontrado paquetes ARP no esperados? ¿Se puede determinar para que sirven?**
  No, los paquetes ARP que encontramos tienen operaciones 1 y 2, que se corresponden a request y responses. En la red 2 hay igual cantidad de tipo 1 y 2, pero en las redes 1 y 3 esto se vuelve muy asimétrico: hay muchos mas paquetes request que response. No supimos explicar este fenómeno.

## Conclusiones

<!-- 200 -->

El trabajo no presentó dificultades significativas, aunque generó dudas respecto de la falta de paquetes ARP en broadcast para la red número 2, que aún no se pudieron resolver.

Además, se vuelve evidente que la mayor parte del tráfico termina siendo IPv4 unicast, lo cual se condice con lo esperado.

Al observar a través de Wireshark el tráfico de paquetes de las redes, nos llamó la atención la cantidad elevada de paquetes UDP con respecto a la de TCP que, creemos, se debe a la transferencia de datos multimedia ya que estábamos compartiendo audio y video a través de Discord.

Finalmente, nos resultó sumamente interesante que mediante un análisis tan simple de los paquetes ARP se pueda conocer la topología de una red. Probablemente sea fructífero realizarlo en una red pública de tamaño mayor y ver cómo se comporta.
