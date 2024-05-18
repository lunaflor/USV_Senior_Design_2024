clear vars;

% Read the CSV file
D = readtable('python_estuary - Sheet1.csv');
lat = D(:,1).Variables; %column 1 of CSV file
lon = D(:,2).Variables; %column 2 of CSV file
dep = D(:,3).Variables; %column 3 of CSV file
dep = (-1* dep)*0.00328084; % Invert depth to make deeper parts downward

% Define grid for interpolation
latlin = linspace(min(lat), max(lat), 100);
lonlin = linspace(min(lon), max(lon), 100);
[LAT,LON] = meshgrid(latlin, lonlin);

% Interpolate data - biharmonic spline interpolation - 'v4'
DEP = griddata(lat,lon,dep, LAT, LON, 'v4');

% Plotting
surf(LON,LAT,DEP, 'EdgeColor', 'none'); % Create the surface plot without edge color
hold on; % Hold on to plot additional data
plot3(lon,lat,dep,'.','MarkerSize',5, 'Color', [0 0 0]); % Plot the original data points

% Set the z-limits to remove spikes
zlim([min(dep) max(dep)]);

% Tighten the axis around the plot and set labels and title
axis tight;
title('Depth Plot');
xlabel('Longitude');
ylabel('Latitude');
zlabel('Depth(ft)');

 % makes sure the tick labels on the z-axis are positive since depth is neg
zticks = get(gca, 'ZTick');
set(gca, 'ZTickLabel', abs(zticks));

%set color scheme for colorbar + map
colormap("jet"); 
colorbar;
h = colorbar;

% Set color axis limits to match depth data
caxis([min(dep) max(dep)]);

% Set colorbar ticks at intervals based on data range
h.Ticks = linspace(min(dep), max(dep), 9); %evenly spaces ticks within the range
% Set rounded and positive tick labels
h.TickLabels = arrayfun(@(x) sprintf('%.f', abs(x)), h.Ticks, 'UniformOutput', false);

% Plot the surface again making sure its on top
surf(LON, LAT, DEP);
hold on;

