clear vars;

% Read the CSV file into a table
T = readtable('voltage_current_cals.csv', 'Format', '%T%f%f', 'Delimiter', ',');

% Extract time and convert to datetime
time = T.Var1;
startTime = time(1);
timeInSeconds = seconds(time - startTime); % Time in seconds from the start

% current an voltage data
Imot = T.Var2 / 1000; 
vbat = T.Var3 / 1000;

%power consumption in watts
power = Imot .* vbat; 

% Calculate average, idle, and peak power
averagePower = mean(power);
idlePower = min(power); % Assuming the minimum power is the idle power
peakPower = max(power);

% Plotting the data
figure;
tiledlayout(3,1);  

% Current draw plot
nexttile
plot(timeInSeconds, Imot, 'Color', [0 0.4470 0.7410]);
title('Current Draw vs Time');
xlabel('Time (seconds)');
ylabel('Current (A)');

% Battery voltage plot
nexttile
plot(timeInSeconds, vbat, 'Color', [0 0 0]);
title('Battery Voltage vs Time');
xlabel('Time (seconds)');
ylabel('Battery Voltage (V)');

% Power consumption plot
nexttile
plot(timeInSeconds, power, 'Color', [1 0 0]);  % Red color for power curve
title('Power Consumption vs Time');
xlabel('Time (seconds)');
ylabel('Power (W)');

% Calculating the energy consumed in watt-hours
energyConsumed = trapz(timeInSeconds, power) / 3600; % Convert seconds to hours for watt-hours

% Battery capacity and duration
batteryCapacityWh = 11.1 * 5;  % 11.1V, 5000mAh (or 5Ah) battery
possibleDurationHoursAVG = batteryCapacityWh / averagePower;  % Total duration at average power usage
possibleDurationHoursPEAK = batteryCapacityWh / peakPower;  % Total duration at average power usage
possibleDurationHoursIDLE = batteryCapacityWh / idlePower;  % Total duration at average power usage
% Display results
disp(['Average Power: ', num2str(averagePower), ' W']);
disp(['Energy Consumed: ', num2str(energyConsumed), ' Wh']);
disp(['Idle Power: ', num2str(idlePower), ' W']);
disp(['Peak Power: ', num2str(peakPower), ' W']);
disp(['Possible Duration at Average Power: ', num2str(possibleDurationHoursAVG), ' hours']);
disp(['Possible Duration at Peak Power: ', num2str(possibleDurationHoursPEAK), ' hours']);
disp(['Possible Duration at idle Power: ', num2str(possibleDurationHoursIDLE), ' hours']);
