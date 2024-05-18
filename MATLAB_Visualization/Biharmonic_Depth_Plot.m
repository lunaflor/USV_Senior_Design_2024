% Read the CSV file
D = readtable('python_estuary - Sheet1.csv');
lat = D{:,1}; % Simplified syntax for extracting columns
lon = D{:,2};
dep = D{:,3};
dep = (-1 * dep) * 0.00328084; % Convert depth to feet and invert

% Define grid for interpolation
latlin = linspace(min(lat), max(lat), 100);
lonlin = linspace(min(lon), max(lon), 100);
[LAT, LON] = meshgrid(latlin, lonlin);

% Interpolate data - biharmonic spline interpolation - 'v4'
DEP = griddata(lat, lon, dep, LAT, LON, 'v4');

% Create a binary mask based on the convex hull of the data points
k = convhull(lat, lon);
mask = inpolygon(LAT, LON, lat(k), lon(k));

% Apply the mask to the DEP matrix
DEP(~mask) = NaN; % Set points outside the convex hull to NaN

% Plotting
figure('Units','normalized','OuterPosition',[0 0 1 1]); % Maximize the figure window
surf(LON, LAT, DEP, 'EdgeColor', 'none'); % Surface plot without edge color
hold on;
plot3(lon, lat, dep, '.', 'MarkerSize', 5, 'Color', 'k'); % Plot the original data points

% Set the z-limits to remove spikes
zlim([min(dep) max(dep)]);

% Tighten the axis around the plot and set labels and title
axis tight;
title('Depth Plot');
xlabel('Longitude');
ylabel('Latitude');
zlabel('Depth(ft)');

% Adjust the view angle to be wider
view(45, 30); % Adjust the viewing angle for better perspective

% Positive tick labels on the z-axis
zticks = get(gca, 'ZTick');
set(gca, 'ZTickLabel', abs(zticks));
colormap("jet"); % Apply the jet colormap
colorbar; % Display the colorbar

h = colorbar;

% Set color axis limits to match depth data
caxis([min(dep) max(dep)]);

% Set colorbar ticks at specific intervals - adjust based on your data range
h.Ticks = linspace(min(dep), max(dep), 9); % Creates evenly spaced ticks within the range
% Set rounded and positive tick labels
h.TickLabels = arrayfun(@(x) sprintf('%.f', abs(x)), h.Ticks, 'UniformOutput', false);

% Plot the surface again making sure it's on top
surf(LON, LAT, DEP, 'EdgeColor', 'none');
hold off;


