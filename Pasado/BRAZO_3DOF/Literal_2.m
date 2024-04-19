clc;clear all;close all;

%% Distancias Eslbones
l1 = 0.470;
l2 = 0.375;
l3 = 0.387;

x = 0;
y = 0;
z = 0;

t=[0:0.1:200];
q1=0*(pi/180)+45*(pi/180)*(cos(0.04*t));
% q2=+0*(pi/180)*ones(1,length(t));
q2=+0*(pi/180)+15*(pi/180)*(sin(0.02*t));
q3=45*(pi/180)-45*(pi/180)*(sin(0.03*t));
q4=45*(pi/180)+45*(pi/180)*(cos(0.04*t));


for k = 1:length(q1)
    %% Cinematica Directa 
    hx(k) = +0   +l2*sin(q2(k))*cos(q1(k))  +l3*sin(q2(k)+q3(k))*cos(q1(k)) + x;
    hy(k) = +0   +l2*sin(q2(k))*sin(q1(k))  +l3*sin(q2(k)+q3(k))*sin(q1(k)) + y; 
    hz(k) = +l1  +l2*cos(q2(k))             +l3*cos(q2(k)+q3(k))            + z; 
    h = [hx(k) ; hy(k) ; hz(k) ];
    
    q = [q1(k) q2(k) q3(k)]';
end

%% Grafico
axis vis3d;
fig=figure(1);
set(fig,'position',[200 200 1000 500]);
axis equal; 
axis([min(hx)-0.7 max(hx)+0.7 min(hy)-0.7 max(hy)+0.7 0 max(hz)+0.5]);
view(20,25);
camlight('right');
camlight('headlight');
grid on, hold on

D1=Brazo_3DOF(q1(1),q2(1),q3(1),q4(1),x,y,z);hold on; grid on;
title('Cinematica Directa Brazo 3DOF');

paso=50;
for j=1:paso:length(q1)
    delete(D1);
    D1=Brazo_3DOF(q1(j),q2(j),q3(j),q4(1),x,y,z);
    plot3(hx(1:j),hy(1:j),hz(1:j),'-r','linewidth',2);
    
    drawnow;
    pause(0.05);
end

disp('Cinematica Directa Brazo 3DOF');
disp('Articulaciones'); 
disp(q)
disp('Posiciones Calculadas'); 
disp(h)

%% Grafica
figure(2)
plot(q1,'b','LineWidth',2);hold on;grid on;
plot(q2,'r','LineWidth',2);
plot(q3,'k','LineWidth',2);
legend('q1','q2','q3');
title('Articulaciones');
xlim([0 length(q1)])
