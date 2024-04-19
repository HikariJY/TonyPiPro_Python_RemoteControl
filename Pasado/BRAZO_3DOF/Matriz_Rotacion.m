clc;clear all;

syms q1 q2 q3
Rz1=[cos(q1) -sin(q1)    0;
     sin(q1)  cos(q1)    0;
          0         0    1];  
      
Ry2=[cos(q2)    0  sin(q2);
           0    1        0;
    -sin(q2)    0  cos(q2)];

Ry3=[ cos(q3)   0   sin(q3);
            0   1         0;
     -sin(q3)   0   cos(q3)];
 
h3=Rz1*Ry2*Ry3
h3=simplify(h3)