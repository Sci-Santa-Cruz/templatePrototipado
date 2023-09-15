from string import punctuation
from re import sub, compile,split,findall,IGNORECASE
# from klp_commons.datefinder.constants import DELIMITERS_PATTERN, MONTHS_PATTERN ,YYYY_PATTERN, DD_PATTERN
from unicodedata import normalize
from re import search
from urlextract import URLExtract
from collections import OrderedDict
#from klp_commons.datefinder import find_dates
extractor = URLExtract()



def count_words(text):
    return len(findall(r'\w+', text))

def removeDupWithOrder(list_word):
    return " ".join(OrderedDict.fromkeys(list_word))

def removeDupWithOrder_2(list_word):
    return list(OrderedDict.fromkeys(list_word))

def get_max_str(lst, fallback=''):
    return max(lst, key=len) if lst else fallback

def rm_tildes(text: str = None) -> str:
    '''
    Eliminar tildes
    '''
    trans_tab = dict.fromkeys(map(ord, '\u0301\u0308'), None)
    return normalize('NFKC', normalize('NFKD', text).translate(trans_tab))

def lower(text: str = None) -> str:
    return text.lower()

def only_text(text):
    return sub(r'[^A-Za-z0-9]+', ' ', text)

def remove_num(text):
    return sub(r'[\d]{5,20}', ' ', text)

def only_capital_letter(text):
    return ' '.join(sub(r'[^A-Z]', r'', ch) for ch in text.split(' '))

def rm_duplicates(text):
    '''
    Input a string and split them
    '''
    return ''.join(list(dict.fromkeys(text)))

def white_space_fix(text: str = None) -> None:
    '''
    Eliminar espacios en blanco innecesarios

    '''
    return ' '.join(text.split())
    

def extract_rfc(text: str = None) -> str:
    '''
    Extraer RFCs de cadenas de texto
    '''
    def pattern_one(text):
        pattern = compile(r'(((al\s)?(rfc|rfc/curp)(:|:\s|\s)?[A-Za-zñÑ]{3,4}\s?\d{6}(\s)?\w{2})+(\s)?(\w)?\b)')

        return pattern.findall(text)

    def pattern_two(text):
        pattern = compile(r'((al\s)?((r\.f\.c\.)(:|:\s|\s)?[A-Za-zñÑ]{3,4}\d{6}\w{2,3})+)')

        return pattern.findall(text)

    def pattern_three(text):
        pattern = compile(r'(((al\s)?(rfc)+(:|:\s|\s)?)(\w{2,3})+(:\w{2,3})?\b)')

        return pattern.findall(text)

    def pattern_four(text):
        pattern = compile(r'(al\s)?rfc:?|r\.f\.c\.:?')

        return pattern.findall(text)

    def pattern_five(text):
        pattern = compile(r'((al\s)?rfc\s\d\.\d\s\d{7,9})')

        return pattern.findall(text)

    def pattern_six(text):
        pattern = compile(r'(\b([A-Za-zñÑ&]{3,4}\s?\d{6}(\s)?\w{2})+(\s)?(\w)?(mx)?\b|\b([A-Za-zñÑ&]{3,4}\s?\d{6}(\s)?\w{2,3}(mx)?\b))')

        return pattern.findall(text)

    def pattern_seven(text):
        pattern = compile(r'((al\s)?(r\.f\.c\.)+(:|:\s|\s)?\w{2,10}\b)')
        return pattern.findall(text)
    
    def pattern_pb(text):
        pattern = compile(r'(rfc: p&?b 0108104k7\b)')
        return pattern.findall(text)


    if None is text:
        return 'None_remove_RFC'

    list_patters = []
    
    list_patters.append(pattern_one(text))
    list_patters.append(pattern_two(text))
    list_patters.append(pattern_three(text))
    list_patters.append(pattern_four(text))
    list_patters.append(pattern_five(text))
    list_patters.append(pattern_six(text))
    list_patters.append(pattern_seven(text))
    list_patters.append(pattern_pb(text))
    
    r = list(set().union(*list_patters))
    r = list(set().union(*r))

  
    if len(r) == 0:
        return []
    else :
        r = list(filter(lambda x: len(x) >= 4 , r))
        r = sorted(r, key=len, reverse=True)
        
        return r





    """
    def filter_datetime(text):
        regexp_moths = compile(MONTHS_PATTERN)
        regexp_delimiters = compile(DELIMITERS_PATTERN)
        regexp_days = compile(DAYS_PATTERN)


        if regexp_moths.search(text):
            time_str = filter_str_month(text)

        elif regexp_delimiters.search(regexp_delimiters,text):

        elif regexp_days.search(regexp_delimiters,text):

    """
    
def filter_datetime(text, dict_datetime):
    datetime_list = []
    count = 0
    for key in dict_datetime['date']:
        for key_nested in dict_datetime['date'][key]:
                if key_nested != 'index':
                    
                    # es una cifra numérica?
                    if not str(key_nested).isnumeric():
                        
                        result = findall(r'[a-z]', key_nested)
                        # contiene letras ?
                        if result != []:
                            if len(result) >=3 :
                                datetime_list.append(dict_datetime['date'][key])
                        else : 
                            # split
                            result = split(DELIMITERS_PATTERN, key_nested ,flags=IGNORECASE)
                            # tiene al menos tres elementos
                            if len(result) >= 3:
                                    datetime_list.append(dict_datetime['date'][key])
                    
    if len(datetime_list) == 1:
        return list(datetime_list[0].keys())[0]
    if len(datetime_list) == 2:
        start = datetime_list[0]['index'][0]
        end = datetime_list[1]['index'][1]
        return text[start:end]
    else : return ''

def filter_str_month(text):
    
    result = split(DELIMITERS_PATTERN, text ,flags=IGNORECASE)

    pattern = ''
    if len(result) > 1 and  (len(result[0].replace('/','').replace('\-','').replace('\.','').strip()) == 2 or  len(result[0].strip()) == 0):
        pattern = text

    elif len(result) > 1 and ( len(result[0].strip()) != 2 or  len(result[0].strip()) != 0):
        pattern = text.replace(result[0],'')

    else : 
        pattern = text



    if ':' in pattern:
        result_2 = split(r'\d{2}\:\d{2}', pattern ,flags=IGNORECASE)
        if len(result_2) > 1 and  len(result_2[0].strip()) > 3:
            pass
        else :
            pattern = ''
    
    return pattern 

def extract_datetime(text: str = None) -> list:
    
    if None is text:
        return []

    matches = find_dates(text, source=True, index=True, strict=True, base_date=None, first="month")
    dict_datetime= dict()
    dict_datetime['date'] = dict()

    for count, match in enumerate(matches):
        dict_datetime['date'][count] = dict()
        dict_datetime['date'][count] [match[1]] = match[0].strftime("%d-%b-%Y")
        dict_datetime['date'][count] ['index'] = match[2]

    return dict_datetime

def extract_lowers(text):
    
    pattern = compile(r'(([\d]+(\s?))?([A-Z]{1}?[a-z,.]*)((\s)?[\d]+)?|([\d\s]+)?[a-z,.]+([\s\d]+)?)')
    result = pattern.findall(text)
    result_list = list()
          
    for tupla in result:
        tupla = list(tupla)
        result = [item for item in tupla if item != '']
        result_list.extend(result)
        
    result =  [ item for item in result_list if not item.isupper() and len(item) > 1]
    
    return [ item for item in result if not item.strip().isdigit() ]

def regex_dates(text):
    regex_pattern = r'(\b({day})?({delimiter})?({months})({delimiter})?({year})?\b)|(\b({year})?({delimiter})?({months})({delimiter})?({day})?\b)'.format(delimiter = DELIMITERS_PATTERN ,year = YYYY_PATTERN, day = DD_PATTERN, months = MONTHS_PATTERN)
    pattern = compile(regex_pattern, IGNORECASE)
    result = pattern.findall(text)

    result = [item[0] for item in result ]

    return sorted(result, key=len, reverse=True)
 
def extract_codes(text: str = None) -> list:
    """"
        extraer de cadenas de texto los patrones :

        NUM-TEXT-NUM
        TEXT-NUM
        TEXT-NUM-TEXT

        Ej:

        8767GHAGAT89
    
    """

    if None is text:
        return []

    
    regex = r'(([a-z]+[0-9]+[a-z]+)([a-z]|[0-9])*|([0-9]+[a-z]+[0-9])([a-z]|[0-9])*|[a-z]+[0-9]+|[0-9]+[a-z]+)'

    
    pattern = compile(regex)
    result = pattern.findall(text)
    result = set().union(*result)
    result = list(filter(lambda x: len(x.strip()) != 0, result))
    return sorted(result, key=len, reverse=True)

def extract_codes_mix(text: str = None) -> list:
    """"

    
    """

    if None is text:
        return []

    
    regex = r'(([\d\-]+/[\d]+/[\d]+/[\d]+\-)(([a-z]+[0-9]+[a-z]+)|([0-9]+[a-z]+[0-9]+)|([a-z]+[0-9]+|[0-9]+[a-z]+))+)'

    pattern = compile(regex)
    result = pattern.findall(text)

    result = set().union(*result)
    result = list(filter(lambda x: len(x) >= 2, result))
    return sorted(result, key=len, reverse=True)

def extract_num_sec(text: str = None) -> list:

    if None is text:
        return []

    
    regex = r'(^[\d]{1,}$)'
    pattern = compile(regex)
    result = pattern.findall(text)
    
    result = set().union(*result)
    result = [ item.strip() for item in result if item.strip() != '']
    return sorted(result, key=len, reverse=True)

def extract_num(text: str = None) -> list:

    if None is text:
        return []

    
    regex = r'((^[\d]{4}\b)|([\d]{5,30}(\s|$)))'
    pattern = compile(regex)
    result = pattern.findall(text.strip())
    
    result = set().union(*result)
    result = [ item.strip() for item in result if item.strip() != '']
    return sorted(result, key=len, reverse=True)

def change_mixed_wordNumber (text):
    
    if None is text:
        return 'None'

    pattern = compile(r'(^|\s)([a-z]{3,20})([0-9]{3,20})($|\s)|(^|\s)([0-9]{3,20c})([a-z]{3,20})($|\s)')
    r = pattern.findall(text)
    result = []
    for tupla in r:
        result.append(list(filter(lambda x: len(x.strip()) != 0, tupla))[0])
    return result

def extract_periodo_consumo(text: str = None) -> list:
    '''

    '''

    if text is None:
        return []  
    pattern = compile(regex_perio_consumo)
    result = pattern.findall(text)
    result = [item.strip() for item in result]
    return sorted(result, key=len, reverse=True)

def extract_num_pago(text):

    
    if None is text:
        return []

    
    result = search(regex_num_pago,text)
    if result:
        return result.groups()
    else :
        return []
