%depth plot with krig interpolation 
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

% prepare data for krig interpolation
X = [lat lon];
y = dep;

%Fit Gaussian process regression
gprMdl = fitrgp(X, y, 'Basis', 'constant', 'FitMethod', 'exact', 'PredictMethod', 'exact');

%Predict values for interpolation
DEP_kriging = predict(gprMdl, [LAT(:) LON(:)]);
DEP_kriging = reshape(DEP_kriging, size(LAT));

% Create a binary mask based on the convex hull of the data points
k = convhull(lat, lon);
mask = inpolygon(LAT, LON, lat(k), lon(k));

% Apply the mask to the DEP matrix
DEP_kriging(~mask) = NaN; % Set points outside the convex hull to NaN


%apply mask for kriging output
%DEP_kriging(~mask) = NaN; % Set points outside the convex hull to NaN

%figure;
figure('Units','normalized','OuterPosition',[0 0 1 1]); % Maximize the figure window
mesh(LON, LAT, DEP_kriging);
hold on;
plot3(lon,lat,dep,'.','MarkerSize',10, 'Color', [0 0 0]); % Plot the original data points
set(gca, 'CLim', [min(dep) max(dep)]); % Match the color limits to the data range
set(findobj(gca, 'Type', 'Surface'), 'FaceColor', 'interp'); % Fill the curtains

colormap jet; 
colorbar;
h= colorbar;
% Set colorbar ticks at intervals based on data range
h.Ticks = linspace(min(dep), max(dep), 9); %evenly spaces ticks within the range
% Set rounded and positive tick labels
h.TickLabels = arrayfun(@(x) sprintf('%.f', abs(x)), h.Ticks, 'UniformOutput', false);

% Tighten the axis around the plot and set labels and title
axis tight;
title('Depth Plot');
xlabel('Longitude');
ylabel('Latitude');
zlabel('Depth(ft)');

 % makes sure the tick labels on the z-axis are positive since depth is neg
zticks = get(gca, 'ZTick');
set(gca, 'ZTickLabel', abs(zticks));

% Plot the surface again making sure its on top
%mesh(LON, LAT, DEP);
%hold on;
