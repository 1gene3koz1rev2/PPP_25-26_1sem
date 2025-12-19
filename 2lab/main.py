from collections import defaultdict
from typing import Dict, List, Tuple, Optional


def convert_currency(
    rates_input: List[str], 
    conversion_path: str
) -> Tuple[Optional[float], List[str]]:

 
    rates: Dict[str, Dict[str, float]] = defaultdict(dict)
    
    for rate_str in rates_input:
        parts = rate_str.strip().split()
        if len(parts) != 3:
            return None, [f"Некорректный формат курса: {rate_str}"]
        
        currency_from, currency_to, rate_value = parts
        try:
            rate = float(rate_value)
            if rate <= 0:
                return None, [f"Курс должен быть положительным: {rate_str}"]
        except ValueError:
            return None, [f"Некорректный курс: {rate_str}"]
        
    
        rates[currency_from][currency_to] = rate
        rates[currency_to][currency_from] = 1.0 / rate
    
  
    path_parts = conversion_path.strip().split()
    if len(path_parts) < 3:
        return None, ["Путь конверсии должен содержать минимум: сумма, из_валюты, в_валюту"]
    
    try:
        amount = float(path_parts[0])
        if amount <= 0:
            return None, ["Сумма должна быть положительной"]
    except ValueError:
        return None, [f"Некорректная сумма: {path_parts[0]}"]
    
    currencies_path = path_parts[1:]
    
  
    for currency in currencies_path:
        if currency not in rates:
            return None, [f"Валюта '{currency}' отсутствует в курсах"]
    
  
    current_amount = amount
    steps = []
    
    for i in range(len(currencies_path) - 1):
        from_curr = currencies_path[i]
        to_curr = currencies_path[i + 1]
        
        if to_curr not in rates[from_curr]:
            return None, [f"Нет курса конверсии из '{from_curr}' в '{to_curr}'"]
        
        rate = rates[from_curr][to_curr]
        new_amount = current_amount * rate
        
        # Форматирование для вывода
        if rate < 0.001 or rate > 1000:
            rate_str = f"{rate:.6f}"
        else:
            rate_str = f"{rate:.4f}"
        
        step_str = f"{current_amount:.4f} {from_curr} -> {new_amount:.4f} {to_curr} (курс: {rate_str})"
        steps.append(step_str)
        
        current_amount = new_amount

    steps.append(f"{current_amount:.4f} {currencies_path[-1]}")
    
    return current_amount, steps


def main():
  
    print("Пример 1:")
    rates = ["r d 0.01", "d e 1", "e f 0.98"]
    path = "1000 r d e"
    
    result, steps = convert_currency(rates, path)
    
    if result is not None:
        print(f"Финальная сумма: {result:.4f}")
        print("Шаги конверсии:")
        for step in steps:
            print(f"  {step}")
    else:
        print(f"Ошибка: {steps[0]}")
    
    print("\n" + "="*50 + "\n")
    
   
    print("Пример 2 (с большим количеством шагов):")
    rates2 = [
        "rub usd 0.011",
        "usd eur 0.92", 
        "eur gbp 0.85",
        "gbp jpy 180.5"
    ]
    path2 = "5000 rub usd eur gbp jpy"
    
    result2, steps2 = convert_currency(rates2, path2)
    
    if result2 is not None:
        print(f"Финальная сумма: {result2:.4f}")
        print("Шаги конверсии:")
        for step in steps2:
            print(f"  {step}")
    else:
        print(f"Ошибка: {steps2[0]}")
    
    print("\n" + "="*50 + "\n")
    
  
    print("Пример 3 (с ошибкой):")
    rates3 = ["a b 1.5", "b c 2.0"]
    path3 = "100 a b d"
    
    result3, steps3 = convert_currency(rates3, path3)
    
    if result3 is not None:
        print(f"Финальная сумма: {result3:.4f}")
        print("Шаги конверсии:")
        for step in steps3:
            print(f"  {step}")
    else:
        print(f"Ошибка: {steps3[0]}")


if __name__ == "__main__":
    main()
