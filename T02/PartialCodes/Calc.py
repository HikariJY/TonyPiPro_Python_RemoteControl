a1, b1, c1, d1, e1 = 1, 2, 5, 4, 3
a2, b2, c2, d2, e2 = 4, 3, 0, 1, 2

t1 = a1+b1+c1+d1+e1
t2 = a2+b2+c2+d2+e2
print(t1)
print(t2)

f1 = t1*5/25
f2 = t2*5/25
print(f1)
print(f2)

x = 0
x = x + (a1-f1)*(a1-f1)/f1
x = x + (a2-f2)*(a2-f2)/f2
x = x + (b1-f1)*(b1-f1)/f1
x = x + (b2-f2)*(b2-f2)/f2
x = x + (c1-f1)*(c1-f1)/f1
x = x + (c2-f2)*(c2-f2)/f2
x = x + (d1-f1)*(d1-f1)/f1
x = x + (d2-f2)*(d2-f2)/f2
x = x + (e1-f1)*(e1-f1)/f1
x = x + (e2-f2)*(e2-f2)/f2
print(x)