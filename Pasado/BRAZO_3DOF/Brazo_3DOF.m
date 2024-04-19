function grafico = Brazo_3DOF(q1,q2,q3,q4,x,y,z)
load 'Arm.mat' Base BaseS Link1 Link1S Link2 Link3 LinkG;  

BaseVertices=Base.vertices'; 
BaseFaces=Base.faces; 

BaseSVertices=BaseS.vertices'; 
BaseSFaces=BaseS.faces; 

Link1Vertices=Link1.vertices'; 
Link1Faces=Link1.faces; 

Link1SVertices=Link1S.vertices'; 
Link1SFaces=Link1S.faces; 

Link2Vertices=Link2.vertices'; 
Link2Faces=Link2.faces;

Link3Vertices=Link3.vertices'; 
Link3Faces=Link3.faces;

LinkGVertices=LinkG.vertices'; 
LinkGFaces=LinkG.faces;

colorBase=[33/255 33/255 254/255];
colorServo=[20/255 20/255 20/255];
colorLink=[209/255 209/255 216/255];
colorLink2=[116/255 116/255 180/255];
colorLink3=[101/255 151/255 80/255];
colorLinkG=[55/255 109/255 34/255];

scale = 0.1;
l1 = +0.470;
l2 = +0.375;
l3 = -0.387;

q2=-q2;
q3=-q3;
q1 = q1 +180*pi/180; 
q3 = q3 +90*pi/180; 
%% Base
armPatch = BaseVertices; % Aplicar la matriz de rotacion a los vertices del componente del robot
armPatch(1,:)=armPatch(1,:)*scale + x; %Escalar y dezplazar en el Eje x
armPatch(2,:)=armPatch(2,:)*scale + y; %Escalar y dezplazar en el Eje y
armPatch(3,:)=armPatch(3,:)*scale + z; %Escalar y dezplazar en el Eje z

grafico(1) = patch('Faces',BaseFaces,'Vertices',armPatch','FaceColor',colorBase,'EdgeColor','none');

armPatch = BaseSVertices; 
armPatch(1,:)=armPatch(1,:)*scale + x; 
armPatch(2,:)=armPatch(2,:)*scale + y; 
armPatch(3,:)=armPatch(3,:)*scale + z; 

grafico(2) = patch('Faces',BaseSFaces,'Vertices',armPatch','FaceColor',colorServo,'EdgeColor','none');

Rz1=[cos(q1) -sin(q1)    0;
     sin(q1)  cos(q1)    0;
          0         0    1];  
     
%% Eslabon 1
lb = 0;
armPatch = Rz1*Link1Vertices; 
armPatch(1,:)=armPatch(1,:)*scale +0  + x; 
armPatch(2,:)=armPatch(2,:)*scale +0  + y; 
armPatch(3,:)=armPatch(3,:)*scale +lb + z; 

grafico(3) = patch('Faces',Link1Faces,'Vertices',armPatch','FaceColor',colorLink,'EdgeColor','none'); 

armPatch = Rz1*Link1SVertices; 
armPatch(1,:)=armPatch(1,:)*scale + x; 
armPatch(2,:)=armPatch(2,:)*scale + y; 
armPatch(3,:)=armPatch(3,:)*scale + z; 

grafico(4) = patch('Faces',Link1SFaces,'Vertices',armPatch','FaceColor',colorServo,'EdgeColor','none'); 

Ry2=[cos(q2)    0  sin(q2);
           0    1        0;
    -sin(q2)    0  cos(q2)];

%% Eslabon 2
armPatch = Rz1*Ry2*Link2Vertices; 
armPatch(1,:)=armPatch(1,:)*scale + 0 + 0 + x; 
armPatch(2,:)=armPatch(2,:)*scale + 0 + 0 + y; 
armPatch(3,:)=armPatch(3,:)*scale +lb +l1 + z; 

grafico(5) = patch('Faces',Link2Faces,'Vertices',armPatch','FaceColor',colorLink2,'EdgeColor','none'); 

Ry3=[ cos(q3)   0   sin(q3);
            0   1         0;
     -sin(q3)   0   cos(q3)];

%% Eslabon 3
armPatch = Rz1*Ry2*Ry3*Link3Vertices; 
armPatch(1,:)=armPatch(1,:)*scale +0  +0   +l2*sin(q2)*cos(q1) + x;
armPatch(2,:)=armPatch(2,:)*scale +0  +0   +l2*sin(q2)*sin(q1) + y; 
armPatch(3,:)=armPatch(3,:)*scale +lb +l1  +l2*cos(q2)         + z; 

grafico(6) = patch('Faces',Link3Faces,'Vertices',armPatch','FaceColor',colorLink3,'EdgeColor','none'); 

Rz4=[cos(q4) -sin(q4)  0; 
     sin(q4)  cos(q4)  0; 
           0       0   1];
       
% Rx4=[1       0         0;
%      0  cos(q4) -sin(q4); 
%      0  sin(q4)  cos(q4)];

%% Gripper
lb = 0.008;
q3 = q3 +90*pi/180; 
armPatch = Rz1*Ry2*Ry3*Rz4*LinkGVertices; 
armPatch(1,:)=armPatch(1,:)*scale +0  +0   +l2*sin(q2)*cos(q1)  +l3*sin(q2+q3)*cos(q1) + x;
armPatch(2,:)=armPatch(2,:)*scale +0  +0   +l2*sin(q2)*sin(q1)  +l3*sin(q2+q3)*sin(q1) + y; 
armPatch(3,:)=armPatch(3,:)*scale +lb +l1  +l2*cos(q2)          +l3*cos(q2+q3)         + z; 

grafico(7) = patch('Faces',LinkGFaces,'Vertices',armPatch','FaceColor',colorLinkG,'EdgeColor','none'); 

xlabel('X (m)');
ylabel('Y (m)');
zlabel('Z (m)');