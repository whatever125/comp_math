# Лабораторная работа №3. Решение нелинейных уравнений
### Метод Ньютона

- [Отчет](./report.pdf)
- [Решение](./main.py)

#### Текст задания
Дана система нелинейных уравнений. По заданному начальному приближению необходимо найти решение системы с точностью до 5 верного знака после запятой при помощи метода Ньютона.

##### Формат входных данных
```
k
n
x0
y0
...
```

где k - номер системы, n - количество уравнений и количество неизвестных, а остальные значения - начальные приближения для соответствующих неизвестных.

##### Формат выходных значений

Cписок такого же типа данных, как списки входных данных, содержащие значения корня для каждой из неизвестных с точностью до 5 верного знака.