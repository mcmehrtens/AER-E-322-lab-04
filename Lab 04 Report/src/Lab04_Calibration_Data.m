% Lab 4 G2S4 Calibration Data; Peter Mikolitis, Matthew Mehrtens, Natuski Oda
% Load the data from the Excel file
clear,clc
data = readmatrix('Lab 4 Calibration Data.csv');

Elongation = data(:, 3);

Load = data(:, 1);


plot(Load, Elongation);
xlabel('Load (lbf)');
ylabel('Elongation (in)');
title('Elongation vs Load');

p = polyfit(Load, Elongation, 1);

hold on
plot(Load, polyval(p, Load), 'r--');
legend('Data', 'Line of Best Fit', 'Location', 'northwest');
fprintf('Equation of line of best fit: y = %.2f x + %.2f\n', p(1), p(2));