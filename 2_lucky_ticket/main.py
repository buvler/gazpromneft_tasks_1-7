import itertools

def is_possible_lucky_ticket(digits: tuple) -> bool:
    """
    Проверяет, можно ли из кортежа 6 цифр собрать счастливый билет.
    """
    total_sum = sum(digits)
    
    if total_sum % 2 != 0:
        return False
        
    target_sum = total_sum // 2
    for combo in itertools.combinations(digits, 3):
        if sum(combo) == target_sum:
            return True
            
    return False

ticket_1 = (1, 2, 3, 0, 1, 5)
print(f"Кортеж {ticket_1}: {is_possible_lucky_ticket(ticket_1)}")  # Вывод: True

ticket_2 = (4, 5, 6, 1, 2, 3) 
print(f"Кортеж {ticket_2}: {is_possible_lucky_ticket(ticket_2)}")  # Вывод: False

ticket_3 = (0, 0, 0, 0, 2, 10) 
print(f"Кортеж {ticket_3}: {is_possible_lucky_ticket(ticket_3)}")  # Вывод: False