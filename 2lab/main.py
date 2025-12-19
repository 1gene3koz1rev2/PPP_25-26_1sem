def convert_currency(rates, amount, path):

    currency_rates = {}
    for rate in rates.split(', '):
        from_curr, to_curr, value = rate.strip().split()
        currency_rates[(from_curr, to_curr)] = float(value)
    
 
    result_path = []
    current_amount = float(amount)
    try:
        for i in range(len(path)):
            if i + 1 >= len(path): break
            
            curr_from = path[i]
            curr_to = path[i+1]
            
        
            conversion_rate = currency_rates.get((curr_from, curr_to))
            if not conversion_rate:
                raise ValueError(f'Нет курса для {curr_from}->{curr_to}')
                
            new_amount = round(current_amount * conversion_rate, 2)
            result_path.append(f'{current_amount:.2f} {curr_from} -> {new_amount:.2f} {curr_to}')
            current_amount = new_amount
        
        return ', '.join(result_path)
    except Exception as e:
        return str(e)
        
rates = 'r d 0.01, d e 1, e f 0.98'
amount = '1000'
path = ['r', 'd', 'e']
print(convert_currency(rates, amount, path))
