clc;clear all;close all;

%% Distancias Eslbones
l1 = 0.470;
l2 = 0.375;
l3 = 0.387;

x = 0;
y = 0;
z = 0;
%% Condiciones Iniciales
q1(1) = angulo(15*pi/180);    
q2(1) = angulo(45*pi/180);     
q3(1) = angulo(15*pi/180);   
q4(1) = angulo(60*pi/180);
q = [q1 q2 q3]';

%% Valores para Metodo 
epsilon = 1e-3;    % Error aceptable
max_int = 5000;   

%% Valor deseado
hxd=[0.4 -0.2 0.3  0.5 0.6] + x;
hyd=[0.4  0.4 0.1 -0.2 0.4] + y;
hzd=[0.9  0.7 0.9  0.8 0.3] + z;

%%
b=1;
for k = 1:max_int
    cpui = cputime;
    tStart = tic;  
    
    hx(k) = +0   +l2*sin(q2(k))*cos(q1(k))  +l3*sin(q2(k)+q3(k))*cos(q1(k)) + x;
    hy(k) = +0   +l2*sin(q2(k))*sin(q1(k))  +l3*sin(q2(k)+q3(k))*sin(q1(k)) + y; 
    hz(k) = +l1  +l2*cos(q2(k))             +l3*cos(q2(k)+q3(k))            + z; 
    h = [hx(k) ; hy(k) ; hz(k) ];
    
    j11 = -l2*sin(q2(k))*sin(q1(k))-l3*sin(q2(k)+q3(k))*sin(q1(k));
    j12 = +l2*cos(q2(k))*cos(q1(k))+l3*cos(q2(k)+q3(k))*cos(q1(k));
    j13 = +l3*cos(q2(k)+q3(k))*cos(q1(k));

    j21 = +l2*sin(q2(k))*cos(q1(k))+l3*sin(q2(k)+q3(k))*cos(q1(k));
    j22 = +l2*cos(q2(k))*sin(q1(k))+l3*cos(q2(k)+q3(k))*sin(q1(k));
    j23 = +l3*cos(q2(k)+q3(k))*sin(q1(k));

    j31 = +0;
    j32 = -l2*sin(q2(k))-l3*sin(q2(k)+q3(k));
    j33 = -l3*sin(q2(k)+q3(k));
    
    J = [j11 j12 j13;
         j21 j22 j23;
         j31 j32 j33];
    
  %% Ecuacion Metodo de Gradiente y Newton
    hd=[hxd(b) hyd(b) hzd(b)]';
    he = hd - h;
 
    alpha = 0.8;
    if norm(he)> epsilon * 30
        q = q + alpha*(J')*(he);
    else
        q = q + pinv(J)*(he);        
    end
    
    q1(k+1) = angulo(q(1));
    q2(k+1) = angulo(q(2));
    q3(k+1) = angulo(q(3)); 
    
  % Error del extremo operativo
    if norm(he)< epsilon
        b=b+1;
        dt(k)=toc(tStart);
        cpu(k)=cputime-cpui;
        if b >= length(hxd)+1
            break;
        end
    end
    
    MD(k)=b; 
    hxdv(k) = hxd(b);
    hydv(k) = hyd(b);
    hzdv(k) = hzd(b);
end

%% Grafico
axis vis3d;
fig=figure(1);
set(fig,'position',[200 200 1000 500]);
axis equal; 
axis([min(hxd)-0.5 max(hxd)+0.5 min(hyd)-0.5 max(hyd)+0.5 0 max(hzd)+0.5]);
view(20,25);
camlight('right');
camlight('headlight');
grid on, hold on

D1=Brazo_3DOF(q(1),q(2),q(3),q4(1),x,y,z);hold on; grid on;
plot3(hxd(1),hyd(1),hzd(1),'*r','linewidth',8);
title('Cinematica Inversa Brazo 3DOF');

paso=10;
c=1;
for j=1:paso:length(q1)
    delete(D1);
    D1=Brazo_3DOF(q1(j),q2(j),q3(j),q4(1),x,y,z);
    plot3(hx(1:j),hy(1:j),hz(1:j),'-k','linewidth',2);
    
    if MD(j)>=c
        c=c+1;
        if c <= max(MD)
            D2=plot3(hxd(c),hyd(c),hzd(c),'*r','linewidth',8);
        end
    end
     
    drawnow;
    pause(0.05);
end
%% Comprobacion
vf = length(q1);
q = [q1(vf) q2(vf) q3(vf)]'; 
disp('Articulaciones Calculadas'); 
disp(q)
disp('Posiciones Deseadas'); 
disp(hd)
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

figure(3)
subplot(3,1,1)
plot(hxdv,'r','LineWidth',2);hold on;grid on;
plot(hx,'b','LineWidth',2);
legend('hxd','hx');
xlim([0 length(hx)])

subplot(3,1,2)
plot(hydv,'r','LineWidth',2);hold on;grid on;
plot(hy,'g','LineWidth',2);
legend('hyd','hy');
xlim([0 length(hy)])

subplot(3,1,3)
plot(hzdv,'r','LineWidth',2);hold on;grid on;
plot(hz,'k','LineWidth',2);
legend('hzd','hz');
xlim([0 length(hz)])

figure(4)
plot(cpu,'b','LineWidth',2);hold on;grid on;
plot(dt,'r','LineWidth',2);
legend('CPU','Muestreo');
title('Tiempos');
xlim([0 length(cpu)])