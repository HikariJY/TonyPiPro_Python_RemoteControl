clear all
Base=stlread('Base_.stl');
BaseS=stlread('BaseS_.stl');
Link1=stlread('Link1_.stl');
Link1S=stlread('Link1S_.stl');
Link2=stlread('Link2v_.stl');
Link3=stlread('Link3v_.stl');
LinkG=stlread('LinkG_.stl');
save('Arm.mat','Base','BaseS','Link1','Link1S','Link2','Link3','LinkG');