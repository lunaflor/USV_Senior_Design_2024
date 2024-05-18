#load all the essential libraries/tools
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import mplcursors

#load your csv file of: lat, long, depth, current, voltage, salinity, temperature)
df = pd.read_csv('C:\\Users\\youruser\\Downloads\\python_estuary - Sheet1.csv')

#assuming 'depth' column is in millimeters and you want it in ft
df['depth'] = df['depth'].abs() / 304.8

#grid for number of points for resolution
num_points = 200
grid_long, grid_lat = np.mgrid[
    df['longitude'].min():df['longitude'].max():complex(0, num_points),
    df['latitude'].min():df['latitude'].max():complex(0, num_points)
]

#perform grid interpolation 
grid_depth = griddata(
    points=(df['latitude'], df['longitude']), 
    values=df['depth'],  
    xi=(grid_lat, grid_long), # The grid of points where you want to interpolate
    method='cubic'  # Cubic interpolation method; it creates a smooth surface
)
print("Min grid depth:", np.min(grid_depth))
print("Max grid depth:", np.max(grid_depth))

#define minimum and maximum values for the colorscale 
colorscale_min = df['depth'].min()  
colorscale_max = df['depth'].max()  

#2D Contour Map 
contour = go.Contour(
    z=grid_depth.T, #transpose to match the grid orientation
    x=np.linspace(df['longitude'].min(), df['longitude'].max(), num_points),
    y=np.linspace(df['latitude'].min(), df['latitude'].max(), num_points),
    colorscale='Jet_r', #use a reversed Jet color scale to show depth better
    zmin=colorscale_min,
    zmax=colorscale_max,
    contours=dict(
        coloring='heatmap',
        showlabels=True,
        labelfont=dict(size=12, color='white'),
    ),
    colorbar=dict(
        title='Depth (ft)', #add a title to the colorbar to serve as the label for the units
        title_font=dict(size=14, color='black', family='Arial'),  
        titleside='top' #position the title on the top of the colorbar
    )
)

#add scatter plot for original data points with markers and lines
scatter = go.Scatter(
    x=df['longitude'],  
    y=df['latitude'],  
    mode='markers+lines', #display both markers and lines
    marker=dict(color='black', size=5),  
    line=dict(color='black'),  
    name='Data Points', #name for legend
    showlegend=True #ensure the legend is shown
)

#creates 2D Contour Plot with markers
fig2D = go.Figure(data=[contour, scatter])

#creates 2D Contour Plot without markers
fig2D2= go.Figure(data=[contour])

#update the layout of the 2D figure to add titles with units
fig2D.update_layout(
    title="2D Contour Map for Russian River Estuary",
    xaxis_title='Longitude',  
    yaxis_title='Latitude',  
    font=dict(family="Arial", size=12, color="black"),  
    xaxis=dict(
        title_font=dict(size=14, color='black', family='Arial')  
    ),
    yaxis=dict(
        title_font=dict(size=14, color='black', family='Arial')  
    ),
    legend=dict(
        x=1, #hoorizontally align the legend to the right
        y=1, #vertically align the legend to the top
        xanchor='left', #anchor the legend's x-position to the left
        yanchor='bottom', #anchor the legend's y-position to the bottom
        bordercolor="Grey", #border color for the legend
        borderwidth=1 #border width for the legend
    )
)

#update the layout of the 2D figure w/o markers to add titles with units
fig2D2.update_layout(
    title="2D Contour Map for Russian River Estuary",
    xaxis_title='Longitude', 
    yaxis_title='Latitude',  
    font=dict(family="Arial", size=12, color="black"), 
    xaxis=dict(
        title_font=dict(size=14, color='black', family='Arial')  
    ),
    yaxis=dict(
        title_font=dict(size=14, color='black', family='Arial')  
    ),
    legend=dict(
        x=1,  
        y=1,  
        xanchor='left',  
        yanchor='bottom',  
        bordercolor="Grey",  
        borderwidth=1 
    )
)

#create a 3D surface plot using the interpolated grid data
surface = go.Surface(
    x=grid_long,
    y=grid_lat,
    z=grid_depth,  
    colorscale='Jet_r',
    cmin=colorscale_min, 
    cmax=colorscale_max,  
     colorbar=dict(
        title='Depth (ft)',  
        title_font=dict(size=14, color='black', family='Arial'),  
        titleside='top'  
    )
)

#create figure and add the surface plot to it
fig3D = go.Figure(data=[surface])

#update the layout of the figure to add titles and set aspect ratios
fig3D.update_layout(
    title="3D Map for Russian River Estuary",
    scene=dict(
        xaxis_title='Longitude',  
        yaxis_title='Latitude',  
        zaxis_title='Depth (ft)', 
        aspectratio=dict(x=1, y=1, z=0.7),  
        zaxis=dict(autorange="reversed"),  
    ),
    scene_camera=dict(
        eye=dict(x=1.87, y=0.88, z=-0.64)  # Camera position for the initial view of the plot
    ),
)

# Write HTML files for offline viewing
fig2D.write_html("C:\\Users\\youruser\\Downloads\\2D_contour_map_plot_with_markers.html")
fig2D2.write_html("C:\\Users\\youruser\\Downloads\\2D_contour_map_plot_without_markers.html")
fig3D.write_html("C:\\Users\\youruser\\Downloads\\3D_plot.html")

# Display the plots
fig2D.show()
fig2D2.show()
fig3D.show()
