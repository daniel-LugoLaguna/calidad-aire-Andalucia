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

En esta entrega parcial del código del proyecto, se extraen los datos para el día 15/03/2021 y la provincia de Sevilla. En la entrega final, se pretende ampliar el alcance de datos históricos a una franja temporal más amplia, así como a todas las provincias andaluzas.
