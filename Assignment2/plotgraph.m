clc;
clear all;
close all;

figure;
x = [2,5,10,15,20];
y1 = [0.6,1.1,2.3,3.1,3.3];
y2 = [0.3,1,2.1,2.9,3];
plot(x,y1);
hold on;
plot(x,y2);
title('Number of Variables vs Running Time (3-5 constraints)');
xlabel('Number of Variables');
ylabel('Running Time');
legend('Designed Solver','Existing Solver');

figure;
x = [5,10,15,20,25];
y1 = [0.5,1,1.2,2.8,3.1];
y2 = [0.4,1,1.7,2.6,3];
plot(x,y1);
hold on;
plot(x,y2);
title('Number of Constraints vs Running Time (3-5 variables)');
xlabel('Number of Constraints');
ylabel('Running Time');
legend('Designed Solver','Existing Solver');