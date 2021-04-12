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
import math, time
from itertools import zip_longest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
```

En esta proyecto, se proporciona un dataset para todas las mediciones de calidad del aire en Andalucía durante el año 2020, proporcionadas por la Junta de Andalucía. Se proporciona una función adicional para la obtención de datos para un intervalo y provincia personalizable por el usuario. El dataset está disponible en: https://zenodo.org/record/4681703#.YHSYxOj7SUk
