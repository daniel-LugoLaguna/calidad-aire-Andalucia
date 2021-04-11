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

URL_main = 'http://www.juntadeandalucia.es/medioambiente/site/portalweb/menuitem.7e1cf46ddf59bb227a9ebe205510e1ca/?vgnextoid=7e612e07c3dc4010VgnVCM1000000624e50aRCRD&vgnextchannel=910f230af77e4310VgnVCM1000001325e50aRCRD#apartadoce217adf12be4010VgnVCM1000000624e50a____'

#Función creada para reorganizar la lista de medidas dividiéndola en bloques en función de la longitud de su cabecera
def grouper(n, it_list, padValue=None):
    """ n -> nºcolumnas por fila
        it_list -> lista sobre la que iterar
        padValue -> valor por defecto
    """
    return zip_longest(*[iter(it_list)]*n, fillvalue=padValue)

# Opciones de navegación
options =  webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')

# Al descargarnos dicho ejecutable, debemos añadir la ruta del directorio webdrivers a nuestra variable de entorno del sistema PATH
driver_path = 'C:/Users/Pablo/Documents/webdrivers/chromedriver.exe'

driver = webdriver.Chrome(driver_path, options=options)

# Inicializamos el navegador
driver.get(URL_main)

# Para obtener el código de estado de la URL usamos un javascript y un objeto XMLHttpRequest
js_status = '''
let callback = arguments[0];
let xhr = new XMLHttpRequest();
xhr.open('GET', 'http://www.juntadeandalucia.es/medioambiente/site/portalweb/menuitem.7e1cf46ddf59bb227a9ebe205510e1ca/?vgnextoid=7e612e07c3dc4010VgnVCM1000000624e50aRCRD&vgnextchannel=910f230af77e4310VgnVCM1000001325e50aRCRD#apartadoce217adf12be4010VgnVCM1000000624e50a____', true);
xhr.onload = function () {
    if (this.readyState === 4) {
        callback(this.status);
    }
};
xhr.onerror = function () {
    callback('error');
};
xhr.send(null);
'''

# LLamamos al siguiente método de la clase WebDriver para ejecutar el código javascript anterior dentro del navegador
status_code = driver.execute_async_script(js_status)

# Comprobamos que la petición nos devuelve un Status Code = 200
if status_code == 200:
    #Inicialización del esquema del dataframe final
    df_final = pd.DataFrame({ 'FECHA-HORA': [],'SO2': [],'PART': [], 'NO2': [], 'CO': [], 'O3': [], 'SH2': [],
                            'Provincia': [], 'Municipio': [], 'Estacion': [], 'Direccion': []})

    # Obtenemos los 365 días del año 2020 en una lista para su uso posterior
    ini_2020 = datetime(2020,1,1)
    fin_2020 = datetime(2020,12,31)
    l_fechas_2020 = [(ini_2020 + timedelta(days=d)).strftime("%Y-%m-%d")
                        for d in range((fin_2020 - ini_2020).days + 1)]

    # Debido al límite de tamaño permitido por GitHub NO ES POSIBLE subir el dataset completo de las 8 provincias andaluzas (tamaño 413.37MB). Por ello limitamos las provincias a Sevilla solo,
    # dejando constancia de la intención de sacar un conjunto de datos completo de Andalucía con más de 4 millones de registros lo que posibilitaría un gran y óptimo estudio/análisis al tener
    # tantos datos comparables.
    #l_prov_id = ['al', 'ca', 'co', 'gr', 'hu', 'ja', 'ma', 'se']
    l_prov_id = ['se']
    for prov_id in l_prov_id:
        # Seleccionamos la provincia correspondiente
        WebDriverWait(driver, 5)\
            .until(EC.element_to_be_clickable((By.XPATH, "//option[@value='{}']".format(prov_id))))\
            .click()

        # Seleccionamos siempre el tipo "Cuantitativo" para los informes
        WebDriverWait(driver, 5)\
            .until(EC.element_to_be_clickable((By.XPATH, "//input[@value='n' and @name='TIPO']")))\
            .click()

        # Recorremos dicha lista para ir insertando los valores en los campos DIA/MES/AÑO y poder realizar todas las consultas
        for dia in l_fechas_2020:
            # Borramos los valores por defecto dados a Fecha(dd/mm/aa)
            driver.find_element_by_name("DIA").clear()
            driver.find_element_by_name("MES").clear()
            driver.find_element_by_name("ANO").clear()

            aa = dia.split('-')[0][-2:]
            mm = dia.split('-')[1]
            dd = dia.split('-')[2]

            # Asignamos a DIA/MES/AÑO sus valores correspondientes en cada iteración
            WebDriverWait(driver, 5)\
                .until(EC.element_to_be_clickable((By.NAME,"DIA")))\
                .send_keys(dd)

            WebDriverWait(driver, 5)\
                .until(EC.element_to_be_clickable((By.NAME,"MES")))\
                .send_keys(mm)

            WebDriverWait(driver, 5)\
                .until(EC.element_to_be_clickable((By.NAME,"ANO")))\
                .send_keys(aa)

            # Accedemos a la página con los informes de la provincia, fecha y tipo correspondiente
            WebDriverWait(driver, 5)\
                .until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[6]/div[2]/div/div/div[3]/div[2]/form/table/tbody/tr[3]/td/input[1]")))\
                .send_keys(Keys.CONTROL + Keys.RETURN)

            # Actuamos en PÁGINA de INFORMES
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            tables = soup.findAll("table")
            l_province = list()
            l_municipio = list()
            l_station = list()
            l_dir = list()
            #Iteramos por todas las tablas:
            #Índice para iterar por las filas del dataframe de localización
            j = 0
            for table in tables:
                tabla_measures = list()
                #Se ha utilizado la palabra clave provincia para filtrar
                if table.text.startswith('Provincia'):
                    indice_prov = table.text.index('Provincia')
                    indice_mun = table.text.index('Municipio')
                    indice_est = table.text.index('Estacion')
                    indice_dir = table.text.index('Direccion')
                    l_province.append(table.text[indice_prov+9:indice_mun])
                    l_municipio.append(table.text[indice_mun+9:indice_est])
                    l_station.append(table.text[indice_est+8:indice_dir])
                    l_dir.append(table.text[indice_dir+9:])

                    #Variable de control que indica que tabla se está recorriendo en dicha iteración, de localización (1) o de mediciones (0)
                    #Esto permite ir incrementando el índice para la tabla paramétrica de provincias
                    ind_tabla_prov = 1

                elif not table.text.startswith('RED DE VIGILANCIA'):
                    l_cab = list()
                    table_Cabecera = table.find_all('td', {'class': 'CabTabla'})
                    for cab in table_Cabecera:
                        l_cab.append(cab.text)

                    measures_tr = table.find_all('tr')
                    measures = list()
                    for tr in measures_tr:
                        measures_td = tr.find_all('td')
                        for td in measures_td:
                            if td.text not in ('FECHA-HORA', 'SO2', 'PART', 'NO2', 'CO', 'O3', 'SH2') and not td.text.startswith('\nNota:'):
                                measures.append(td.text)

                    if len(l_cab) != 0:
                        tabla_measures = list([l_cab])
                        tabla_measures+=list(grouper(len(l_cab), measures, math.ceil(len(measures)/len(l_cab))))
                        df_measures = pd.DataFrame(tabla_measures[1:],columns=tabla_measures[0])

                    df_loc = pd.DataFrame({'Provincia': l_province, 'Municipio': l_municipio, 'Estacion': l_station, 'Direccion': l_dir})

                    # Recuperamos todos los elementos cuya clase se denomine 'CabTabla', ya que estos representan las cabeceras de las tablas de medidas.
                    # (en cada tabla de medida hay tantos 'CabTabla' como columnas haya). Los almacenamos en una lista que recorremos y cuando se detecte
                    # el inicio de una cabecera (es decir, el texto "FECHA-HORA" es el primero que aparece) incrementamos el contador num_tablas_medidas en uno.
                    # Con esto obtenemos el número total de tablas de medidas que hay en cada página de informes.
                    lista_tablas_medidas = driver.find_elements_by_class_name('CabTabla')
                    num_tablas_medidas = 0
                    for indice in lista_tablas_medidas:
                        if indice.text == "FECHA-HORA":
                            num_tablas_medidas = num_tablas_medidas + 1

                    # Si el índice de la lista no ha llegado al nº máximo de tablas de medidas o no es la primera tabla de provincia, se crea un
                    # dataframe intermedio con la posición de la paramétrica correspondiente. A continuación, se replica la fila recogida tantas
                    # veces como filas tenga el dataframe de medidas intermedio del paso anterior.
                    if l_province and j < num_tablas_medidas:
                        df_loc_iter = pd.DataFrame(np.repeat(pd.DataFrame({'Provincia': l_province[j],
                                                'Municipio': l_municipio[j],
                                                'Estacion': l_station[j],
                                                'Direccion': l_dir[j]},index=[0]).values,len(df_measures),axis=0),columns = ['Provincia','Municipio',
                                                                                                                'Estacion','Direccion'])
                        # Se concatenan los dos df intermedios de medidas y localizaciones para la presente iteración
                        # Se añaden las filas al dataframe final con toda la información
                        df_iter = pd.concat((df_measures,df_loc_iter), axis = 1)
                        df_final = df_final.append(df_iter,sort=True)
                        # Si se ha recorrido tabla de provincia en el paso anterior, se incrementa +1 el indicador
                        if ind_tabla_prov == 1:
                            j = j + 1
                        # Variable de control de tabla de provincia. Dado que se ha recorrido una tabla de medidas, se pasa el indicador a 0
                        ind_tabla_prov = 0

            # Retrocedemos a la página principal
            driver.back()

    # Reordenamos columnas y quitamos indice
    df_final = df_final[['Provincia', 'Municipio','Direccion', 'Estacion','FECHA-HORA','CO','NO2','O3','PART','SO2','SH2']].reset_index(drop=True)
    # Añadimos nuevo índice
    df_final = df_final.reset_index()

    # Generamos fichero AirQualityAndalusia2020_Sevilla.csv
    df_final.to_csv('AirQualityAndalusia2020_Sevilla.csv', index = False, header=True,encoding='utf-8-sig',sep=',')
    driver.close()
else:
    print("Status code %d" % status_code)
