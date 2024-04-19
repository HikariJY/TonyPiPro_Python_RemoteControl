clc;
clear all;

syms q1 q2 q3 l1 l2 l3

hx = +0   +l2*sin(q2)*cos(q1)  +l3*sin(q2+q3)*cos(q1);
hy = +0   +l2*sin(q2)*sin(q1)  +l3*sin(q2+q3)*sin(q1); 
hz = +l1  +l2*cos(q2)          +l3*cos(q2+q3); 
jacobian([hx,hy,hz], [q1, q2, q3]) 