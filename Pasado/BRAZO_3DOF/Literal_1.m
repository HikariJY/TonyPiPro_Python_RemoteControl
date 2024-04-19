clc;clear all;close all;

axis vis3d;
fig=figure(1);
set(fig,'position',[200 200 1000 500]);
axis equal; 
axis([-1 1 -1 1 0 2]);
view(20,25);
camlight('right');
camlight('headlight');
grid on, hold on

%% Condiciones Iniciales
q1(1) = 0*pi/180;    
q2(1) = 0*pi/180;     
q3(1) = 0*pi/180;   
q4(1) = 0*pi/180;

x = 0.2;
y = 0.1;
z = 0;
R1=Brazo_3DOF(q1(1),q2(1),q3(1),q4(1),x,y,z);hold on

%%  Movimiento Robot
t=[0:0.1:100];
q1=0*(pi/180)+45*(pi/180)*(cos(0.01*t));
% q2=+0*(pi/180)*ones(1,length(t));
q2=+0*(pi/180)+15*(pi/180)*(sin(0.02*t));
q3=45*(pi/180)-45*(pi/180)*(sin(0.03*t));
q4=45*(pi/180)+45*(pi/180)*(cos(0.04*t));

for n = 1:100:length(t)
 drawnow
 delete(R1)

 q1v = angulo(q1(n));
 q2v = angulo(q2(n));
 q3v = angulo(q3(n));
 q4v = angulo(q4(n));
 
 R1 = Brazo_3DOF(q1v,q2v,q3v,q4v,x,y,z); hold on

 pause(0.01)
end

%% Grafica
figure(2)
plot(q1,'b','LineWidth',2);hold on;grid on;
plot(q2,'r','LineWidth',2);
plot(q3,'k','LineWidth',2);
legend('q1','q2','q3');
title('Articulaciones');
xlim([0 length(q1)])
