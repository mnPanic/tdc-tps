# Taller 3 - Port Scanning y DNS

## Implementaciones

No es necesario nada en particular para correrlos a parte de la biblioteca
scapy.

- *Port scanning* está en [`taller3.py`](taller3.py) (outputs en [`out/`](out/))

  Para correrlo,

  ```bash
  $ sudo python3 taller3.py <host>
  ```

  Por ejemplo

  ```bash
  $ sudo python3 taller.py mx.msu.ru
  ```

- Resolución de nombres en [`dns.py`](dns.py) (outputs en
  [`dns-out/`](dns-out/)).

  Para correrlo,

  ```bash
  $ sudo python3 dns.py <host> <record_type>
  ```

  Por ejemplo

  ```bash
  $ sudo python3 dns.py msu.ru MX
  # o también
  $ sudo python3 dns.py mx.msu.ru A
  ```

## Informe

El informe está en [`informe.md`](informe.md)
