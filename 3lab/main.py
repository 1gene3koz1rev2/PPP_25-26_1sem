class ExpressionEvaluator:
    def __init__(self):
        self.journal = []
        self.pos = 0
        self.expression = ""
    
    def evaluate(self, expression):
        """Основной метод для вычисления выражения"""
        self.journal = []
        self.pos = 0
        self.expression = expression.replace(" ", "") 
        
        result = self._parse_expression()
        
        
        if self.pos < len(self.expression):
            raise ValueError(f"Нераспознанные символы: {self.expression[self.pos:]}")
        
        return result
    
    def _log_call(self, level, operation, result, details=""):
        """Добавляет запись в журнал"""
        indent = "  " * level
        log_entry = f"{indent}Уровень {level}: {operation} -> {result}"
        if details:
            log_entry += f" ({details})"
        self.journal.append(log_entry)
    
    def _parse_expression(self, level=0):
        """Парсит выражение: сложение и вычитание"""
        self._log_call(level, "Начало разбора выражения", "в процессе", 
                      f"позиция {self.pos}, символы: {self.expression[self.pos:min(self.pos+10, len(self.expression))]}")
        
        
        left = self._parse_term(level + 1)
        
        while self.pos < len(self.expression):
            if self.expression[self.pos] == '+':
                self.pos += 1
                right = self._parse_term(level + 1)
                self._log_call(level, "Сложение", f"{left} + {right}", "до вычисления")
                left += right
                self._log_call(level, "Сложение", left, "после вычисления")
            elif self.expression[self.pos] == '-':
                self.pos += 1
                right = self._parse_term(level + 1)
                self._log_call(level, "Вычитание", f"{left} - {right}", "до вычисления")
                left -= right
                self._log_call(level, "Вычитание", left, "после вычисления")
            else:
                break
        
        self._log_call(level, "Конец разбора выражения", left)
        return left
    
    def _parse_term(self, level=0):
        """Парсит терм: умножение и деление"""
        self._log_call(level, "Начало разбора терма", "в процессе")
        
        
        left = self._parse_factor(level + 1)
        
        while self.pos < len(self.expression):
            if self.expression[self.pos] == '*':
                self.pos += 1
                right = self._parse_factor(level + 1)
                self._log_call(level, "Умножение", f"{left} * {right}", "до вычисления")
                left *= right
                self._log_call(level, "Умножение", left, "после вычисления")
            elif self.expression[self.pos] == '/':
                self.pos += 1
                right = self._parse_factor(level + 1)
                self._log_call(level, "Деление", f"{left} / {right}", "до вычисления")
                if right == 0:
                    raise ZeroDivisionError("Деление на ноль")
                left /= right
                self._log_call(level, "Деление", left, "после вычисления")
            else:
                break
        
        self._log_call(level, "Конец разбора терма", left)
        return left
    
    def _parse_factor(self, level=0):
        """Парсит фактор: числа или выражения в скобках"""
        self._log_call(level, "Начало разбора фактора", "в процессе", 
                      f"текущий символ: '{self.expression[self.pos] if self.pos < len(self.expression) else 'EOF'}'")
        
       
        if self.pos < len(self.expression) and self.expression[self.pos].isdigit():
            start = self.pos
            while self.pos < len(self.expression) and (self.expression[self.pos].isdigit() or self.expression[self.pos] == '.'):
                self.pos += 1
            number = float(self.expression[start:self.pos])
            self._log_call(level, "Число", number)
            return number
        
        
        elif self.pos < len(self.expression) and self.expression[self.pos] == '(':
            self.pos += 1  # Пропускаем '('
            self._log_call(level, "Открывающая скобка", "найдена")
            
           
            result = self._parse_expression(level + 1)
            
            if self.pos >= len(self.expression) or self.expression[self.pos] != ')':
                raise ValueError(f"Ожидается закрывающая скобка на позиции {self.pos}")
            
            self.pos += 1  # Пропускаем ')'
            self._log_call(level, "Закрывающая скобка", "обработана", f"результат: {result}")
            return result
        
        
        else:
            raise ValueError(f"Ожидается число или скобка на позиции {self.pos}")
    
    def print_journal(self):
        """Выводит журнал вызовов"""
        print("=== ЖУРНАЛ РЕКУРСИВНЫХ ВЫЗОВОВ ===")
        for entry in self.journal:
            print(entry)
        print("=================================")



if __name__ == "__main__":
    evaluator = ExpressionEvaluator()
    
   
    expressions = [
        "(2 + (3 * (4 - 1)))",
        "3 + 4 * 2",
        "(1 + 2) * (3 + 4)",
        "10 / 2 + 3 * 4",
        "((2 + 3) * (6 - 4)) / 2"
    ]
    
    for expr in expressions:
        print(f"\nВычисление выражения: {expr}")
        try:
            result = evaluator.evaluate(expr)
            print(f"Результат: {result}")
            evaluator.print_journal()
        except Exception as e:
            print(f"Ошибка: {e}")
    
  
    print("\n" + "="*60)
    print("Демонстрация для выражения из задания: (2 + (3 * (4 - 1)))")
    print("="*60)
    
    expr = "(2 + (3 * (4 - 1)))"
    evaluator = ExpressionEvaluator()
    result = evaluator.evaluate(expr)
    print(f"Выражение: {expr}")
    print(f"Результат: {result}")
    evaluator.print_journal()
