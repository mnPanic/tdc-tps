# Informe

## Introducción

<!-- 200 -->

## Métodos y condiciones de los experimentos

<!-- 400 -->

Para la ejecución de los experimentos se partió del código provisto por la cátedra, extendiendo el método `mostrar_fuente`, agregándole el cálculo de la información de cada símbolo y la entropía de la fuente para 15000 tramas.

Se ejecutó el programa en tres redes distintas el 1/05/2021 aproximadamente a las 20:00 (GMT-3).

- red 1
- red 2
- red 2

{justificar eleccion de s2 cuando lo hagamos}

## Resultados de los experimentos

<!-- 600 -->

Resultado para cada red

- 1. (manu)

  | Tipo de mensaje | Protocolo            | Probabilidad | Información |
  | --------------- | -------------------- | ------------ | ----------- |
  | UNICAST         | 2048 (IPv4)          | 0.99713      | 0.00287     |
  | BROADCAST       | 2054 (ARP)           | 0.00153      | 6.48031     |
  | BROADCAST       | 2048 (IPv4)          | 0.00067      | 7.31322     |
  | UNICAST         | 35130 (IEEE 1905.1a) | 0.00027      | 8.22951     |
  | UNICAST         | 35020 (LLDP)         | 0.00027      | 8.22951     |
  | UNICAST         | 2054 (ARP)           | 0.00013      | 8.92266     |

  Entropía: 0.0233

- 2. (lu)

  | Tipo de mensaje | Protocolo   | Probabilidad | Información |
  | --------------- | ----------- | ------------ | ----------- |
  | UNICAST         | 2048 (IPv4) | 0.99920      | 0.00080     |
  | UNICAST         | 2054 (ARP)  | 0.00080      | 7.13097     |

  Entropía: 0.0065

- 3. (elias)

  | Tipo de mensaje | Protocolo                | Probabilidad | Información |
  | --------------- | ------------------------ | ------------ | ----------- |
  | UNICAST         | 2048 (IPv4)              | 0.96774      | 0.03280     |
  | UNICAST         | 34525 (IPv6)             | 0.01453      | 4.23138     |
  | BROADCAST       | 33024 (IEEE 802.1Q VLAN) | 0.00640      | 5.05152     |
  | BROADCAST       | 2054 (ARP)               | 0.00507      | 5.28514     |
  | UNICAST         | 33024 (IEEE 802.1Q VLAN) | 0.00380      | 5.57282     |
  | UNICAST         | 2054 (ARP)               | 0.00120      | 6.72550     |
  | BROADCAST       | 2048 (IPv4)              | 0.00113      | 6.78266     |
  | BROADCAST       | 34999 (OUI EE)           | 0.00013      | 8.92272     |

  Entropía: 0.1905

{algo}

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

  {explicar funcionalidades}
  - 35020 (LLDP)
  - 35130 (IEEE 1905.1a)
  - 33024 (IEEE 802.1Q VLAN)
  - 34999 (OUI EE)
  - LLDP: IEEE Std 802.1AB - Link Layer Discovery Protocol

    Enviado por el router

  - Type: 1905.1a Convergent Digital Home Network for Heterogenous Technologies (0x893a)

Preguntas agregadas:

- **¿Se mantiene esta distribución estable en el tiempo?**

  Sí. Se replicaron los experimentos para las mismas redes 5 veces y no se observaron diferencias significativas en los resultados.

## Conclusiones

<!-- 200 -->

El trabajo no presentó dificultades significativas, aunque generó dudas respecto de la falta de paquetes ARP en broadcast para la red número 2, que aún no se pudieron resolver.

Además, se vuelve evidente que la mayor parte del tráfico termina siendo IPv4 unicast, lo cual se condice con lo esperado.

Al observar a través de Wireshark el tráfico de paquetes de las redes, nos llamó la atención la cantidad elevada de paquetes UDP con respecto a la de TCP que, creemos, se debe a la transferencia de datos multimedia ya que estábamos compartiendo audio y video a través de Discord.
