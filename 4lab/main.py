

if __name__ == "__main__":
    pass from abc import ABC, abstractmethod
from typing import List

class TimeInterval(ABC):
    @abstractmethod
    def to_seconds(self) -> float:
        pass
    
    @abstractmethod
    def to_human_readable(self) -> str:
        pass

class HMSInterval(TimeInterval):
    def __init__(self, h: int, m: int, s: int):
        self.h = h
        self.m = m
        self.s = s
    
    def to_seconds(self) -> float:
        return self.h * 3600 + self.m * 60 + self.s
    
    def to_human_readable(self) -> str:
        return f"{self.h} h {self.m} min {self.s} s"

class MillisecondsInterval(TimeInterval):
    def __init__(self, ms: int):
        self.ms = ms
    
    def to_seconds(self) -> float:
        return self.ms / 1000
    
    def to_human_readable(self) -> str:
        seconds = self.to_seconds()
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        return f"{h} h {m} min {s} s"

class MinutesSecondsInterval(TimeInterval):
    def __init__(self, m: int, s: int):
        self.m = m
        self.s = s
    
    def to_seconds(self) -> float:
        return self.m * 60 + self.s
    
    def to_human_readable(self) -> str:
        return f"0 h {self.m} min {self.s} s"

class HoursInterval(TimeInterval):
    def __init__(self, hours: float):
        self.hours = hours
    
    def to_seconds(self) -> float:
        return self.hours * 3600
    
    def to_human_readable(self) -> str:
        h = int(self.hours)
        m = int((self.hours - h) * 60)
        s = int(((self.hours - h) * 60 - m) * 60)
        return f"{h} h {m} min {s} s"

class TimeIntervalCalculator:
    def __init__(self, intervals: List[TimeInterval]):
        self.intervals = intervals
    
    def calculate(self, operation: str) -> str:
        if not self.intervals:
            return "Нет интервалов для вычисления"
        
        if operation == "sum":
            total = sum(i.to_seconds() for i in self.intervals)
            result = self._seconds_to_interval(total)
            return f"Total: {result.to_human_readable()}"
        elif operation == "avg":
            avg = sum(i.to_seconds() for i in self.intervals) / len(self.intervals)
            result = self._seconds_to_interval(avg)
            return f"Average: {result.to_human_readable()}"
        elif operation == "max":
            max_interval = max(self.intervals, key=lambda x: x.to_seconds())
            return f"Max: {max_interval.to_human_readable()}"
        elif operation == "min":
            min_interval = min(self.intervals, key=lambda x: x.to_seconds())
            return f"Min: {min_interval.to_human_readable()}"
        else:
            return f"Неизвестная операция: {operation}"
    
    def _seconds_to_interval(self, seconds: float) -> TimeInterval:
        """Вспомогательный метод для создания интервала из секунд"""
        class ResultInterval(TimeInterval):
            def __init__(self, sec):
                self.seconds = sec
            
            def to_seconds(self):
                return self.seconds
            
            def to_human_readable(self):
                h = int(self.seconds // 3600)
                m = int((self.seconds % 3600) // 60)
                s = int(self.seconds % 60)
                return f"{h} h {m} min {s} s"
        
        return ResultInterval(seconds)

# Пример использования
def main():
    # Создаем интервалы разных типов
    intervals = [
        HMSInterval(1, 30, 0),          # 1:30:00
        MillisecondsInterval(90000),     # 90000 мс = 90 сек
        MinutesSecondsInterval(3, 45),   # 3 мин 45 сек
        HoursInterval(2.5),              # 2.5 часа
    ]
    
    # Выводим информацию о каждом интервале
    print("Исходные интервалы:")
    for i, interval in enumerate(intervals, 1):
        print(f"{i}. {interval.to_human_readable():20} = {interval.to_seconds():.1f} сек")
    
    print("\n" + "="*50)
    
    # Создаем калькулятор
    calculator = TimeIntervalCalculator(intervals)
    
    # Выполняем операции
    operations = ["sum", "avg", "max", "min"]
    
    for op in operations:
        result = calculator.calculate(op)
        print(result)

if __name__ == "__main__":
    main()
