clear,clc
data = xlsread('your_filename.xlsx');

% Multiply the data by (0.2605/1000)
data = data * (0.2605/1000);

% Plot the data
plot(data)
xlabel('Data Point')
ylabel('Strain')
title('Strain Data')