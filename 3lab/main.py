

if __name__ == "__main__":
    pass 
    class SimpleExpressionCalculator:
    def __init__(self):
        self.journal = []
        self.call_count = 0
    
    def calculate(self, expression):
        self.journal = []
        self.call_count = 0
        expr = expression.replace(" ", "")
        result = self._eval_expr(expr)
        
        print(f"Выражение: {expression}")
        print(f"Результат: {result}")
        print("\nЖурнал рекурсивных вызовов:")
        for entry in self.journal:
            print(entry)
        return result
    
    def _eval_expr(self, expr):
        """Вычисление выражения с операциями + и -"""
        self.call_count += 1
        call_id = self.call_count
        self.journal.append(f"{call_id}: eval_expr('{expr}')")
        
        result = self._eval_term(expr, 0)[0]
        
        self.journal.append(f"{call_id}: результат = {result}")
        return result
    
    def _eval_term(self, expr, start):
        """Вычисление выражения с операциями * и /"""
        self.call_count += 1
        call_id = self.call_count
        self.journal.append(f"{call_id}: eval_term('{expr[start:]}')")
        
        result, pos = self._eval_factor(expr, start)
        
        while pos < len(expr):
            if expr[pos] == '*':
                right, next_pos = self._eval_factor(expr, pos + 1)
                self.journal.append(f"{call_id}: {result} * {right} = {result * right}")
                result *= right
                pos = next_pos
            elif expr[pos] == '/':
                right, next_pos = self._eval_factor(expr, pos + 1)
                self.journal.append(f"{call_id}: {result} / {right} = {result / right}")
                result /= right
                pos = next_pos
            else:
                break
        
        self.journal.append(f"{call_id}: результат = {result}")
        return result, pos
    
    def _eval_factor(self, expr, start):
        """Обработка чисел и скобочных выражений"""
        self.call_count += 1
        call_id = self.call_count
        self.journal.append(f"{call_id}: eval_factor('{expr[start:]}')")
        
        pos = start
        
        if expr[pos] == '(':
            balance = 1
            end = pos + 1
            while end < len(expr) and balance > 0:
                if expr[end] == '(':
                    balance += 1
                elif expr[end] == ')':
                    balance -= 1
                end += 1
            
            inner_expr = expr[pos + 1:end - 1]
            result = self._eval_expr(inner_expr)
            self.journal.append(f"{call_id}: выражение в скобках = {result}")
            return result, end
        
        num_str = ""
        while pos < len(expr) and expr[pos].isdigit():
            num_str += expr[pos]
            pos += 1
        
        result = int(num_str)
        self.journal.append(f"{call_id}: число = {result}")
        return result, pos

if __name__ == "__main__":
    calc = SimpleExpressionCalculator()
    
    test_expr = "(2 + (3 * (4 - 1)))"
    print("=" * 50)
    calc.calculate(test_expr)
