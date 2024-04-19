function [q] = angulo(ang)

% if ang>=180*pi/180
%     while ang>=180*pi/180
%     ang=ang-360*pi/180;
%     end
%     q=ang;
%     return
% end
% 
% if ang<-180*pi/180
%     while ang<-180*pi/180
%     ang=ang+360*pi/180;
%     end
%     q=ang;
%     return
% end

if  ang>=+180*(pi/180)
    ang =+180*(pi/180);
end
if  ang<=-180*(pi/180)
    ang =-180*(pi/180);
end

q=ang;
return