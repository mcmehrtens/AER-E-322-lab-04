clear,clc,close all;
data = readmatrix('Lab 4 Tensile Data Yellow Box.csv');

% Multiply the data by (0.2605/1000)
data = data * (1000 / 0.2605) / 2;

% Plot the data
plot(data)
xlabel('Data Point')
ylabel('Strain')
title('Strain Data')