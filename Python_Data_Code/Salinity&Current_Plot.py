
# Plot the scatter plot for coordinates
ax = df.plot(x="longitude", y="latitude", kind="scatter", color="blue", alpha=1, label="Coordinate")

# Plot the first point separately
first_longitude = df['longitude'].iloc[0]
first_latitude = df['latitude'].iloc[0]
plt.plot(first_longitude, first_latitude, marker='*', color='red', markersize=10, label='Starting Point')

# Initialize prev variable
prev = None

# Iterate through the dataframe and add arrows
for row in df[::-1].itertuples():
    if prev:
        ax.annotate('', xy=(prev.longitude, prev.latitude), xytext=(row.longitude, row.latitude),
                    arrowprops=dict(arrowstyle="->", linewidth=1), color='b')
    prev = row

# Set plot title and labels
ax.set_title('Russian River Estuary with Salinity', fontweight='bold')
ax.set_xlabel('Longitude', fontweight='bold')
ax.set_ylabel('Latitude', fontweight='bold')

# Add north arrow
x, y, arrow_length = 0.10, 0.15, 0.085
ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
            arrowprops=dict(facecolor='black', width=2, headwidth=8),
            ha='center', va='center', fontsize=15,
            xycoords=ax.transAxes)

# Add northeast arrows
arrow_length = 0.07  # Adjust the length of the arrow
arrows = [(0.1, 0.9), (0.1, 0.7)]#, (0.9, 0.75)]  # Define the coordinates for each arrow

#for x_ne, y_ne in arrows:
    #ax.annotate('', xy=(x_ne, y_ne), xytext=(x_ne + arrow_length, y_ne - arrow_length),
                #arrowprops=dict(facecolor='blue', width=2, headwidth=8),
                #ha='center', va='center', fontsize=15,
                #xycoords=ax.transAxes)

# Show the legend
plt.legend()

# Plot the current readings
scatter = plt.scatter(df['longitude'], df['latitude'], c=df['salinity'], cmap='viridis', label='Salinity Reading')

# Find and annotate peak current readings
#peak_indices = df['salinity'].nlargest(3).index
#for idx in peak_indices:
   # plt.annotate(f'Peak: {df["salinity"][idx]} mA', (df['longitude'][idx], df['latitude'][idx]), textcoords="offset points", xytext=(0,10), ha='center')

# Show the colorbar
plt.colorbar(label='Salinity (ppt)')

# Create a new figure for the line graph for current readings
plt.figure()

# Plot the line graph for current readings
line_plot_salinity = plt.plot(df.index, df['salinity'], color='red', marker='')
plt.xlabel('Data Points', fontweight='bold')
plt.ylabel('Salinity Readings (ppt)', fontweight='bold')
plt.grid(True)

# Calculate average current
average_salinity = df['salinity'].mean()

# Plot average current as a horizontal line
plt.axhline(y=average_salinity, color='blue', linestyle='--', label=f'Average Salinity: {average_salinity:.2f} (ppt)')

# Show interactive tooltips with data point index and current reading on line graph
mplcursors.cursor(line_plot_salinity, hover=True).connect(
    "add", lambda sel: sel.annotation.set_text(f'Index: {round(sel.index)}\nSalinity Reading: {df["salinity"][int(sel.index)]} (ppt)')
)

# Show the plots
plt.tight_layout()
plt.legend()

# Print total charge (mAh) based on 15 minutes
#print(f"Total charge (mAh) based on 15 minutes: {current_reading_mAh:.2f} mAh")
plt.show()

# Create a new figure for the line graph for voltage readings
plt.figure()

# Plot the line graph for voltage readings
line_plot_voltage = plt.plot(df.index, df['voltage'], color='red', marker='o')
plt.xlabel('Data Point', fontweight='bold')
plt.ylabel('Voltage (V)', fontweight='bold')
plt.grid(True)

# Show the plots
plt.tight_layout()
plt.legend()
plt.show()

#Code for Current Section:
# Plot the current readings
scatter = plt.scatter(df['longitude'], df['latitude'], c=df['current'], cmap='viridis', label='Current Reading')

# Show the colorbar
plt.colorbar(label='Current (mA)')

# Create a new figure for the line graph for current readings
plt.figure()

# Plot the line graph for current readings
line_plot_current = plt.plot(df.index, df['current'], color='red', marker='')
plt.xlabel('Data Points', fontweight='bold')
plt.ylabel('Current Readings (mA)', fontweight='bold')
plt.grid(True)

# Calculate average current
average_current = df['current'].mean()

# Plot average current as a horizontal line
plt.axhline(y=average_current, color='blue', linestyle='--', label=f'Average Current: {average_current:.2f} (mA)')

# Show interactive tooltips with data point index and current reading on line graph
mplcursors.cursor(line_plot_current, hover=True).connect(
    "add", lambda sel: sel.annotation.set_text(f'Index: {round(sel.index)}\nCurrent Reading: {df["current"][int(sel.index)]} (mA)')
)

# Show the plots
plt.tight_layout()
plt.legend()

# Print total charge (mAh) based on 15 minutes
#print(f"Total charge (mAh) based on 15 minutes: {current_reading_mAh:.2f} mAh")
plt.show()



