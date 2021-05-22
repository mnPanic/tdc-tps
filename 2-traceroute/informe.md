# Taller 2 - Traceroute

## Integrantes

| LU     | Nombre            | Mail                      |
| ------ | ----------------- | ------------------------- |
| 72/18  | Manuel Panichelli | panicmanu@gmail.com       |
| 76/16  | Luciano Strika    | lucianostrika44@gmail.com |
| 692/12 | Elías Cerdeira    | eliascerdeira@gmail.com   |

- https://www.cmu.edu/: 128.2.42.52
- https://www.u-tokyo.ac.jp/: 210.152.243.234
- dc.uba.ar: 157.92.27.128
- http://www.du.ac.in/: 14.139.45.149
- https://www.osaka-u.ac.jp/

## Introducción

<!-- 200 palabras -->
<!-- Breve explicación de los experimentos que se van a realizar. -->

## Métodos y condiciones de los experimentos

<!-- 400 palabras -->
<!-- Explicación del código implementado y descripciones de las rutas. Se debe detallar la localización geográfica de cada universidad y
las características de las pruebas -horario, día de la semana, etc.- -->

## Resultados de los experimentos

<!-- 600 palabras -->
<!-- En esta sección deben presentarse figuras
y/o tablas que muestren de manera integral los resultados observados. A modo de sugerencia, se puede
mostrar un gráfico de RTT entre saltos que se deduce de restar los valores promediados a cada salto y/o
RTT total a cada salto. -->

| Hop | IP             | RTT       | SD       | dRTT      | Interoceánico | Location |
|:---:|:--------------:|:---------:|:--------:|:---------:|:-------------:|:--------:|
|  1  | 192.168.1.1    | 17.17 ms  | 7.37 ms  | 155.38 ms | No            |                                                                                                             |
|  2  | 200.51.241.181 | 14.76 ms  | 13.55 ms | 0.50 ms   | No            | (Buenos Aires - Argentina, AS10834 Telefonica de Argentina)                                                 |
|  3  | * * *          |     N/A   |   N/A    | N/A       | N/A           |                                                                                                             |
|  4  | 10.192.19.58   | 15.26 ms  | 1.57 ms  | 0.82 ms   | No            |                                                                                                             |
|  5  | 10.192.19.52   | 16.08 ms  | 1.15 ms  | 0.12 ms   | No            |                                                                                                             |
|  6  | 10.192.18.12   | 16.20 ms  | 2.08 ms  | 156.34 ms | No            |                                                                                                             |
|  7  | 94.142.98.192  | 172.55 ms | 5.33 ms  | 1.86 ms   | No            | (São Paulo - Brazil, AS12956 TELEFONICA GLOBAL SOLUTIONS SL)                                                |
|  8  | 213.140.39.116 | 25.51 ms  | 40.84 ms | 18.26 ms  | No            | (Madrid - Spain, AS12956 TELEFONICA GLOBAL SOLUTIONS SL)                                                    |
|  9  | 176.52.249.39  | 43.76 ms  | 3.28 ms  | 114.61 ms | Sí            | (Madrid - Spain, AS12956 TELEFONICA GLOBAL SOLUTIONS SL)                                                    |
| 10  | 94.142.98.123  | 158.37 ms | 0.00 ms  | 16.03 ms  | No            | (São Paulo - Brazil, AS12956 TELEFONICA GLOBAL SOLUTIONS SL)                                                |
| 11  | 94.142.98.192  | 174.40 ms | 13.18 ms | 51.71 ms  | No            | (São Paulo - Brazil, AS12956 TELEFONICA GLOBAL SOLUTIONS SL)                                                |
| 12  | 129.250.8.117  | 171.71 ms | 4.10 ms  | 54.39 ms  | No            | (Ashburn - United States, AS2914 NTT America, Inc.)                                                         |
| 13  | 129.250.2.144  | 159.62 ms | 4.54 ms  | 66.49 ms  | Sí            | (Ashburn - United States, AS2914 NTT America, Inc.)                                                         |
| 14  | 129.250.6.237  | 226.11 ms | 2.69 ms  | 101.67 ms | Sí            | (San Jose - United States, AS2914 NTT America, Inc.)                                                        |
| 15  | 129.250.2.119  | 327.77 ms | 8.30 ms  | 1.11 ms   | No            | (Osaka - Japan, AS2914 NTT America, Inc.)                                                                   |
| 16  | 129.250.3.232  | 320.50 ms | 9.22 ms  | 1.33 ms   | No            | (Osaka - Japan, AS2914 NTT America, Inc.)                                                                   |
| 17  | 61.200.91.154  | 321.82 ms | 1.94 ms  | 1.51 ms   | No            | (Osaka - Japan, AS2914 NTT America, Inc.)                                                                   |
| 18  | 150.99.64.58   | 316.43 ms | 11.36 ms | 6.91 ms   | No            | (Osaka - Japan, AS2907 Research Organization of Information and Systems, National Institute of Informatics) |
| 19  | 150.99.188.62  | 323.33 ms | 2.37 ms  | 5.55 ms   | No            | (Kobe - Japan, AS2907 Research Organization of Information and Systems, National Institute of Informatics)  |
| 20  | 133.1.0.10     | 328.88 ms | 12.04 ms | 2.31 ms   | No            | (Suita - Japan, AS4730 Osaka University)                                                                    |
| 21  | 133.1.14.33    | 324.41 ms | 5.82 ms  | 6.77 ms   | No            | (Suita - Japan, AS4730 Osaka University)                                                                    |
| 22  | 133.1.14.46    | 331.18 ms | 17.49 ms | 0.00 ms   | No            | (Suita - Japan, AS4730 Osaka University)                                                                    |
| 23  | * * *          |     N/A   |    N/A   |   N/A     | N/A           |                                                                                                             |
| 24  | * * *          |     N/A   |    N/A   |   N/A     | N/A           |                                                                                                             |
| 25  | * * *          |     N/A   |    N/A   |   N/A     | N/A           |                                                                                                             |
| 26  | * * *          |     N/A   |    N/A   |   N/A     | N/A           |                                                                                                             |
| 27  | * * *          |     N/A   |    N/A   |   N/A     | N/A           |                                                                                                             |
| 28  | * * *          |     N/A   |    N/A   |   N/A     | N/A           |                                                                                                             |
| 29  | * * *          |     N/A   |    N/A   |   N/A     | N/A           |                                                                                                             |
| 30  | * * *          |     N/A   |    N/A   |   N/A     | N/A           |                                                                                                             |

**NOTA:** Para el caso del hop 7 notamos un incremento local y anómalo en el RTT. Creemos que esto puede deberse a que  
el host puede asignar distintos grados de prioridad a los diferentes protocolos de mensajería. Esto resultaría en que la 
respuesta de ICMP se aplace en el tiempo.

- ¿Qué porcentaje de saltos no responden los Time exceeded? ¿Cuál es el largo de la ruta en terminos de
los saltos que si responden?

  
    
- ¿La ruta tiene enlaces intercontinentales? ¿Cuántos?

  

- ¿Se observaron comportamientos anómalos del tipo descripto en la bibliografía sugerida?

  

- ¿Se observaron otros comportamientos anómalos? Proponga hipótesis que permitan explicarlos.

  

## Conclusiones

<!-- 200 palabras -->
<!-- Breve reseña que sintetize las principales dificultades y des-
cubrimientos. -->