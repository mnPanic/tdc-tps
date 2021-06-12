# Taller 3 - Port Scanning y DNS

IPs:

## Introducción

En este trabajo se desarrolla una herramienta para detectar al estado de los puertos en un sistema operativo, implementando un subconjunto de las funcionalidades de [nmap](https://nmap.org/).

En concreto, la herramienta efectuará un *port scan* sobre una cierta IP enviando paquetes TCP y UDP a cada puerto y analizando las respuestas para determinar su estado.

En particular, en este trabajo solo se evalúan los *well-known ports* (1 a 1024) las páginas web de 3 universidades diferentes: Osaka, MIT y Moscow. A partir de los resultados obtenidos se pretende descubrir qué servicios están disponibles en cada host y si están protegidos por un *firewall*.

## Métodos y condiciones de los experimentos

La herramienta implementada envía paquetes TCP y UDP a la IP especificada utilizando la biblioteca `scapy`[citation needed]. Analiza las respuestas y las clasifica en tres grandes categorías: `filtrado`, `abierto`, `cerrado`.

- Para TCP, se inicia una conexión mediante un paquete TCP con flag SYN sobre IP al socket elegido y se analiza la respuesta:
  - Si no hubo respuesta, se devuelve `filtrado`.
  - Si hubo respuesta del tipo TCP,
    - Si los flags de la respuesta fueron SYNC ACK (SA), se devuelve `abierto`.
    - Si los flags fueron RESET ACK (RA), se devuelve `cerrado`.
  - Si hubo respuesta del tipo ICMP
    - Se retorna `filtrado (icmp t: <type> c: <code>)`.

- Para UDP, se envía un paquete UDP vacío sobre IP al socket elegido y se analiza la respuesta siguiendo la guía de interpretación especificada por [`nmap`](https://nmap.org/book/scan-methods-udp-scan.html)
  - Si no hubo respuesta, se devuelve `abierto|filtrado`
  - Si hubo respuesta UDP, `abierto`.
  - Si hubo respuesta ICMP de tipo 3 (Destination Unreachable)
    - Si tiene code 3 (Port Unreachable) se devuelve `cerrado`
    - Sino, se devuelve `filtrado (icmp t: 3 c: <code>)`

Se ejecutó la herramienta sobre los sitios web de tres universidades, a las 19:00 del sábado 06/06/2021.

- [MIT](https://www.mit.edu/): `23.37.251.54`
- [Osaka University](https://www.osaka-u.ac.jp/ja): `133.1.138.1`
- [Moscow](https://www.google.com/search?q=russian+vodka&tbm=isch&ved=2ahUKEwiT0svG6JLxAhVos5UCHShjD6EQ2-cCegQIABAA&oq=russian+vodka&gs_lcp=CgNpbWcQAzICCAAyAggAMgIIADICCAAyBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB46BAgAEBM6CAgAEAcQHhATULETWKcgYK4haANwAHgAgAFYiAGqBpIBAjExmAEAoAEBqgELZ3dzLXdpei1pbWfAAQE&sclient=img&ei=RwnFYNOSDejm1sQPqMa9iAo&bih=902&biw=1920#imgrc=OAqVtyW0tV48VM) [University](https://www.msu.ru/en/): `188.44.51.94`
- [Tokyo Univesity](u-tokyo.ac.jp): Solo DNS.

Se ejecutó también para otros sitios, pero los resultados no variaron significativamente.

## Resultados de los experimentos

A continuación presentamos los resultados obtenidos para cada universidad, enumerando primero las respuestas TCP y luego las UDP.

- **Osaka** (Elías)

  | Protocolo | Respuesta         | Cantidad |
  | --------- | ----------------- | -------- |
  | tcp       | filtrado          | 1022     |
  | tcp       | abierto (SA)      | 2        |
  | udp       | abierto\|filtrado | 1024     |

  Puertos abiertos:

  - `80/tcp` abierto (SA)
  - `443/tcp` abierto (SA)

- **Moscu** (Manuel)

  | Protocolo | Respuesta                | Cantidad |
  | --------- | ------------------------ | -------- |
  | tcp       | filtrado                 | 962      |
  | tcp       | filtrado (icmp t:3 c:10) | 59       |
  | tcp       | abierto (SA)             | 3        |
  | udp       | abierto\|filtrado        | 989      |
  | udp       | filtrado (icmp t:3 c:10) | 35       |

  Puertos abiertos:

  - `22/tcp` (SSH) abierto (SA)
  - `80/tcp` (HTTP) abierto (SA)
  - `443/tcp` (HTTPS) abierto (SA)

- **MIT** (Luciano)

  | Protocolo | Respuesta         | Cantidad |
  | --------- | ----------------- | -------- |
  | tcp       | filtrado          | 1022     |
  | tcp       | abierto (SA)      | 2        |
  | udp       | abierto\|filtrado | 1024     |

  Puertos abiertos:

  - `80/tcp` abierto (SA)
  - `443/tcp` abierto (SA)

Viendo estos datos, podemos responder algunas de las incógnitas planteadas.

- **¿Cuántos puertos abiertos aparecen? ¿A que servicios/protocolos (nivel de aplicación) corresponden?**

  En todas aparecen los mismos dos puertos abiertos: 80/tcp (HTTP) y 443/tcp (HTTPS), y además en Moscú aparece el 22/tcp (SSH/scp/sftp).

- **¿Cuántos puertos filtrados tenían los sitios web que se probaron?**

  En Osaka y MIT para TCP había 1022 puertos filtrados (todos menos el 80 y 443)
  y todos los de UDP fueron abierto\|filtrado.

  Para Moscú para tcp hubieron 962 filtrados por falta de respuesta y 59 por ICMP *Destination Unreachable (type 3) / Host administratively prohibited (code 10)*. Para UDP, 989 udp abierto\|filtrado por falta de respuesta y 35 por ICMP 3/10.

  En la documentación de nmap se menciona el uso de payloads específicos para intentar escanear los puertos UDP, ya que las aplicaciones que reciben paquetes vacíos suelen descartarlos. Suponemos que esta es la razón por la cual no obtuvimos ninguna respuesta UDP para estas universidades. Comprobamos que nuestra herramienta no detecta algunos puertos UDP que nmap sí, como por ejemplo el 53 (DNS) para la IP `8.8.8.8` (DNS de Google).

- **¿Es posible darse cuenta si los hosts que se probaron están protegidos por un firewall?**

  Con la herramienta implementada no es posible determinar la presencia de un firewall. Esto es porque si un puerto está filtrado es imposible distinguir si no hubo respuesta del host o el paquete fue descartado (*drop*) por un firewall. Además, tampoco se puede en caso de recibir una respuesta, ya que ese puerto podría estar habilitado para ciertos protocolos por una regla. Por ejemplo, sería razonable que un servidor HTTP que aloja una página tenga habilitados solamente los puertos 80 (http) y 443 (https)

- **¿Existen otros puertos bien conocidos que puedan estar abiertos en los hosts que se probaron?**

  El programa itera todos los puertos [*well-known* (de 0 a 1024)](https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers) y reporta el estado de todos ellos, pero podría suceder que un puerto esté abierto y que no sea detectado (como en el caso descrito arriba de UDP). Además existen los *registered ports* (de 1024 a 49151), que son de uso frecuente y en caso de estar abiertos nuestro programa no los detectaría.

## Conclusiones

- hablar de **firewall**
- los puertos que estan abiertos son los usuales y esperados para una pagina web
- no suelen responder probablemente por razones de seguridad o porque no son necesarias.
  - estaria piola saber por qué tendrías mas
- trabajo futuro
  - queda como trabajo futuro implementar payloads especificos de UDP para cada puerto, como se cuenta en la sección resultados.
  - pegarle a otras urls y descubrir más puertos, y que casos de uso reales hay
    - mail SMTP, POP, IMAP
    - dns server DNS y TLS DNS
    - ...
