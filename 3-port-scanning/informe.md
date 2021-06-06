# Taller 3 - Port Scanning y DNS

IPs:

## Introducción

- se desarrolla nmap
- se prueba para los well known ports (hasta 1024) para 3 universidades
- se analiza el estado de los puertos tratando de determinar si hay un firewall

## Métodos y condiciones de los experimentos

- mandamos pkt TCP SYN o UDP vacio sobre IP,
  - tcp
    - si no hay respuesta, `filtrado`
    - si hay respuesta tcp
      - SA `abierto`
      - RA `cerrado`
    - si hay respuesta icmp
      - `filtrado icmp ...`
  - udp
    - si no hay respuesta `abierto|filtrado`, justificar con https://nmap.org/book/scan-methods-udp-scan.html
    - si hay respuesta udp `abierto`
    - si hay respuesta icmp de tipo 3 (destination unreachable)
      - si tiene codigo 3 (destination port unreachable): `cerrado`
      - sino, `filtrado c: <codigo>`

le pegamos a 3 universidades a las 19:00 de un sabado 06/06/21

- MIT: 23.37.251.54
- Osaka University: 133.1.138.1
- Moscow University: 188.44.51.94

## Resultados de los experimentos

- **Osaka** (Elías)

  | Protocolo | Respuesta         | Cantidad |
  | --------- | ----------------- | -------- |
  | tcp       | filtrado          | 1022     |
  | tcp       | abiertoSA         | 2        |
  | udp       | abierto\|filtrado | 1024     |

  Abiertos:

  - 80/tcp abierto (SA)
  - 443/tcp abierto (SA)

- **Moscu** (Manuel)

  | Protocolo | Respuesta                | Cantidad |
  | --------- | ------------------------ | -------- |
  | tcp       | filtrado                 | 962      |
  | tcp       | filtrado (icmp t:3 c:10) | 59       |
  | tcp       | abierto (SA)             | 3        |
  | udp       | abierto\|filtrado        | 989      |
  | udp       | filtrado (icmp c: 10)    | 35       |

  Abiertos:

  - 22/tcp (SSH) abierto (SA)
  - 80/tcp (HTTP) abierto (SA)
  - 443/tcp (HTTPS) abierto (SA)

- **MIT** (Luciano)

  | Protocolo | Respuesta         | Cantidad |
  | --------- | ----------------- | -------- |
  | tcp       | filtrado          | 1022     |
  | tcp       | abierto (SA)      | 2        |
  | udp       | abierto\|filtrado | 1024     |

  Abiertos:

  - 80/tcp abierto (SA)
  - 443/tcp abierto (SA)

Probamos con otras y todas daban mas o menos lo mismo (80 y 443).

Preguntas:

- **¿Cuántos puertos abiertos aparecen? ¿A que servicios/protocolos (nivel de aplicación) corresponden?**

  En todas aparecen los mismos dos puertos abiertos: 80/tcp (HTTP) y 443/tcp (HTTPS), y además en Moscú aparece el 22/tcp (SSH/scp/sftp).

- **¿Cuántos puertos filtrados tenían los sitios web que se probaron?**

  En Osaka y MIT para TCP había 1022 puertos filtrados (todos menos el 80 y 443)
  y todos los de UDP fueron abierto\|filtrado.

  Para Moscú para tcp hubieron 962 filtrados por falta de respuesta y 59 por ICMP *Destination Unreachable (type 3) / Host administratively prohibited (code 10)*. Para UDP, 989 udp abierto\|filtrado por falta de respuesta y 35 por ICMP 3/10.

  revisando la docu de nmap, vimos que tiene paylods específicos para cada port UDP, porque sino no te responden. Esto lo comprobamos ya que algunas universidades respondían al port 53 (DNS) con nmap pero no con nuestro programa.

- **¿Es posible darse cuenta si los hosts que se probaron están protegidos por un firewall?**

  Creemos que para los `filtered` hay un firewall y los `closed` no.

  **?? Verificar cuando veamos firewall**

- **¿Existen otros puertos bien conocidos que puedan estar abiertos en los hosts que se probaron?**

  Si, hay [una lista](https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers) de puertos bien conocidos.

  **?? que quieren que digamos**

## Conclusiones

**?? firewall**

queda como trabajo futuro implementar payloads especificos de UDP para cada puerto, como se cuenta en resultados.