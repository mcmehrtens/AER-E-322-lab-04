% Lab 4 G2S4 Raw Data; Peter Mikolitis, Matthew Mehrtens, Natuski Oda
% Load the data from the Excel file
data = readmatrix('Lab 4 Specimen Raw Data.csv');

original_length = 8;
cross_sectional_area = 0.05;

% Calculate the strain values
extension = data(:, 2);
strain = extension / original_length;

% Calculate the stress values
load = data(:, 3);
stress = load / cross_sectional_area;

% Create the stress-strain graph
plot(strain, stress);
xlabel('Strain');
ylabel('Stress');
title('Stress-Strain Graph');


