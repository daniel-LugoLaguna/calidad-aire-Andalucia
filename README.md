# calidad-aire-Andalucia

## Autores

Daniel Lugo Laguna

Pablo Mora Galindo

## Descripción

Web Scraper para la generación de un dataset histórico de calidad del aire en Andalucía. Los datos han sido tomados de la página Web oficial de la Junta de Andalucía, en el apartado de informes SIVA y mediciones de tipo cuantitativo.

Para poder ejecutar el código del presente proyecto es necesario instalar las siguientes librerías:

```
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import math
from itertools import zip_longest
```

En esta proyecto, se proporciona un dataset para todas las mediciones de calidad del aire en Andalucía durante el año 2020, proporcionadas por la Junta de Andalucía. Se proporciona una función adicional para la obtención de datos para un intervalo y provincia personalizable por el usuario.
