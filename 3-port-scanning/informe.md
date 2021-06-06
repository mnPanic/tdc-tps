# Taller 3 - Port Scanning y DNS

IPs:

- MIT: 23.37.251.54
- Osaka University: 133.1.138.1
- Delhi University: 14.139.45.149


## Introducción

## Métodos y condiciones de los experimentos

## Resultados de los experimentos


- osaka
tcp
 filtrado     1022
abiertoSA       2

80/ TCP abierto SA / UDP abierto|filtrado
443/ TCP abierto SA / UDP abierto|filtrado

udp
 abierto|filtrado    1024

- delhi
tcp
 filtrado     1022
abiertoSA       2

udp
 abierto|filtrado    1024

80/ TCP abiertoSA / UDP abierto|filtrado
443/ TCP abiertoSA / UDP abierto|filtrado

- MIT
tcp
 filtrado     1022
abiertoSA       2

udp
 abierto|filtrado    1024

80/ TCP abiertoSA / UDP abierto|filtrado
443/ TCP abiertoSA / UDP abierto|filtrado

- **¿Cuántos puertos abiertos aparecen? ¿A que servicios/protocolos (nivel de aplicación) corresponden?**

  En todas aparecen los mismos dos puertos abiertos: 80 (HTTP) y 443 (HTTPS), solo para TCP.

- **¿Cuántos puertos filtrados tenían los sitios web que se probaron?**

  En todas para TCP había 1022 puertos filtrados (todos menos el 80 y 443) y todos los de UDP `abierto|filtrado`.

- **¿Es posible darse cuenta si los hosts que se probaron están protegidos por un firewall?**

  Creemos que para los `filtered` hay un firewall y los `closed` no.

  ?? Verificar cuando veamos firewall

- **¿Existen otros puertos bien conocidos que puedan estar abiertos en los hosts que se probaron?**

  Si, hay [una lista](https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers) de puertos bien conocidos.

  ?? que quieren que digamos

## Conclusiones
