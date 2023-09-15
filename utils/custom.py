
# estandarizar fecha 
from datetime import datetime
from sklearn.preprocessing import PowerTransformer, QuantileTransformer
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def datetime_convert(date_str,output_format = '%Y-%m-%d %H:%M:%S'):
    """
    Intenta estandarizar una cadena de fecha y hora en el formato 'YYYY-MM-DD HH:MM:SS'.

    Esta función intenta convertir una cadena de fecha y hora en uno de los formatos admitidos:
    - 'YYYY-MM-DDTHH:MM:SS'
    - 'YYYY-MM-DD HH:MM:SS'
    - 'MM/DD/YYYYTHH:MM:SS'
    - 'MM/DD/YYYY HH:MM:SS'

    Si el formato de entrada no coincide con ninguno de los formatos admitidos,
    devuelve un objeto datetime en el formato 'YYYY-MM-DD HH:MM:SS' si es posible.

    Parámetros:
    date_str (str): La cadena de fecha y hora en uno de los formatos admitidos.

    Devuelve:
    datetime: Un objeto datetime en el formato 'YYYY-MM-DD HH:MM:SS'.

    Ejemplos:
    is_date_matching('2023-08-24T15:30:00') devuelve un objeto datetime en formato 'YYYY-MM-DD HH:MM:SS'
    is_date_matching('08/24/2023 15:30:00') devuelve un objeto datetime en formato 'YYYY-MM-DD HH:MM:SS'
    """
    try:
        # Intenta convertir la cadena en el primer formato
        d = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
        return d.strftime(output_format)
    except:
        try:
            # Intenta convertir la cadena en el segundo formato
            d = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            return d.strftime(output_format)
        except:
            try:
                # Intenta convertir la cadena en el tercer formato
                d = datetime.strptime(date_str, '%m/%d/%YT%H:%M:%S')
                return d.strftime(output_format)
            except:
                # Si no coincide con ninguno de los formatos anteriores, intenta el cuarto formato
                d = datetime.strptime(date_str, '%m/%d/%Y %H:%M:%S')
                return d.strftime(output_format)


def anomaly_delete(x, mn, mx):
    """
    Esta función se utiliza para tratar valores atípicos (anomalías) en una variable.
    
    Parameters:
        x (float): El valor a ser evaluado y ajustado si es una anomalía.
        mn (float): El límite inferior para considerar valores como anomalías.
        mx (float): El límite superior para considerar valores como anomalías.
    
    Returns:
        x (float): El valor ajustado si es una anomalía, de lo contrario, se mantiene igual.
    """
    # Comprobar si x es mayor que el límite superior (mx)
    if x > mx:
        x = mx
    # Comprobar si x es menor que el límite inferior (mn)
    if x < mn:
        x = mn
    return x



def handle_outliers(df, variable, distance=1.5, num_sigma = 3, flag_quantil = True):
    """
    Esta función identifica y trata los valores atípicos en una variable de un DataFrame.

    Parameters:
        df (DataFrame): El DataFrame que contiene los datos.
        variable (str): El nombre de la variable para la que se tratarán los valores atípicos.
        distance (float): La distancia multiplicativa para calcular los límites de valores atípicos. Por defecto, es 1.5.

    Returns:
        df_cleaned (DataFrame): El DataFrame con los valores atípicos tratados en la variable especificada.
    """
    

    if flag_quantil:
        # Calcular los límites superior e inferior utilizando find_boundaries
        upper_boundary, lower_boundary = find_boundaries_quuantil(df, variable, distance)

    else :
        upper_boundary, lower_boundary = find_boundaries_sigma(df, variable, num_sigma)
    
    # Tratar los valores atípicos en la variable
    df_cleaned = df.copy()
    df_cleaned.loc[df_cleaned[variable] > upper_boundary, variable] = upper_boundary
    df_cleaned.loc[df_cleaned[variable] < lower_boundary, variable] = lower_boundary
    
    return df_cleaned


def find_boundaries_sigma(df, variable,num_sigma=2):
    """
    Calcula los límites inferior y superior para detectar valores atípicos utilizando el método de los sigma.

    Parameters:
    data (array-like): La serie de datos en la que deseas calcular los límites.
    num_sigma (int): El número de desviaciones estándar para considerar un valor como atípico. Por defecto, se establece en 2.

    Returns:
    lower_bound (float): El límite inferior para detectar valores atípicos.
    upper_bound (float): El límite superior para detectar valores atípicos.
    """
    mean = np.mean(df[variable].values)
    std_dev = np.std(df[variable].values)
    lower_bound = mean - (num_sigma * std_dev)
    upper_bound = mean + (num_sigma * std_dev)
    
    return upper_bound,lower_bound



def find_boundaries_quuantil(df, variable, distance=1.5):
    """
    Esta función calcula los límites superior e inferior para identificar valores atípicos en una variable dada.

    Parameters:
        df (DataFrame): El DataFrame que contiene los datos.
        variable (str): El nombre de la variable para la que se calcularán los límites.
        distance (float): La distancia multiplicativa para ajustar los límites. Un valor típico es 1.5.

    Returns:
        upper_boundary (float): El límite superior para identificar valores atípicos.
        lower_boundary (float): El límite inferior para identificar valores atípicos.
    """

    # Calcular el rango intercuartílico (IQR)
    IQR = df[variable].quantile(0.75) - df[variable].quantile(0.25)

    # Calcular los límites
    lower_boundary = df[variable].quantile(0.25) - (IQR * distance)
    upper_boundary = df[variable].quantile(0.75) + (IQR * distance)

    return upper_boundary, lower_boundary


import numpy as np

def encode(df, col, max_val):
    """
    Aplicar la transformación seno y coseno a un vector.

    Parámetros:
    -----------
    df : DataFrame
        El DataFrame que contiene los datos.
    col : str
        El nombre de la columna que se va a transformar.
    max_val : float
        El valor máximo para normalizar la columna.

    Retorna:
    --------
    df : DataFrame
        El DataFrame con las columnas transformadas agregadas.
    """
    # Aplicar la transformación seno y coseno a la columna
    df[col + '_sin'] = np.sin(2 * np.pi * df[col] / max_val)
    df[col + '_cos'] = np.cos(2 * np.pi * df[col] / max_val)
    
    return df


def test_transformers(columns):
    """
    Esta función aplicar la trasformación PowerTransformer y QuantileTransformer a una matriz de datos 
    y muestra los resultados en forma gráfica
    
    input 
            columns : lista con el nombre de las columnas a las que se le aplicarán las transformaciones a dataframe 'df'
            
    output  
        Visualizació de los resultados
    
    """
    
    pt = PowerTransformer()
    qt = QuantileTransformer(n_quantiles=5000, output_distribution='normal')
    fig = plt.figure(figsize=(20,30))
    j = 1
    for i in columns:
        array = np.array(df[i]).reshape(-1, 1)
        y = pt.fit_transform(array)
        x = qt.fit_transform(array)
        plt.subplot(3,3,j)
        sns.histplot(array, bins = 50, kde = True)
        plt.title(f"Original {i}")
        plt.subplot(3,3,j+1)
        sns.histplot(x, bins = 50, kde = True)
        plt.title(f" Transformación Quantile{i}")
        plt.subplot(3,3,j+2)
        sns.histplot(y, bins = 50, kde = True)
        plt.title(f"Transformación Power {i}")
        j += 3

