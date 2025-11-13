

if __name__ == "__main__":
    pass 
import random
from statistics import mean

# data
students = [f"Студент_{i+1}" for i in range(10)]
grades = [[random.randint(2, 5) for _ in range(5)] for _ in range(10)]

#Сред оценка
averages = [mean(student_grades) for student_grades in grades]
print("Средние оценки:")
for i, student in enumerate(students):
    print(f"{student}: {averages[i]:.2f}")

# 2. выс и низк оценк
print("\nОценки по предметам:")
for subject in range(5):
    subject_grades = [student_grades[subject] for student_grades in grades]
    print(f"Предмет {subject+1}: макс={max(subject_grades)}, мин={min(subject_grades)}")

# 3. best/worst оценк
best_idx = averages.index(max(averages))
worst_idx = averages.index(min(averages))
print(f"\nЛучший: {students[best_idx]} ({averages[best_idx]:.2f})")
print(f"Худший: {students[worst_idx]} ({averages[worst_idx]:.2f})")




