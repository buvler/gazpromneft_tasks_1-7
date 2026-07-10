from typing import Any, Optional

def get_nested_value(data: dict, path: str) -> Optional[Any]:
    """
    Возвращает значение из вложенного словаря по пути ключей, 
    разделенных точкой.
    """

    keys = path.split('.')
    current = data
    
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key] 
        else:
            return None 
            
    return current


data_obj = {
    'a': {
        'b': {
            'c': '+++'
        }
    }
}

print(get_nested_value(data_obj, 'a.b.c'))    # Вывод: '+++'
print(get_nested_value(data_obj, 'a.x.c'))    # Вывод: None