import geopandas as gpd
import matplotlib.pyplot as plt

# Replace with the path to the downloaded 'naturalearth_lowres.shp' file
shapefile_path = 'D:/path/to/naturalearth_lowres.shp'

# Load the shapefile from the downloaded data
world = gpd.read_file(shapefile_path)

# Define the countries to highlight
highlight_countries = ['United States', 'China', 'India', 'Brazil']

# Create a column for coloring the countries
world['highlight'] = world['name'].apply(lambda x: 'highlight' if x in highlight_countries else 'other')

# Plot the map
fig, ax = plt.subplots(figsize=(10, 6))
world[world['highlight'] == 'highlight'].plot(ax=ax, color='green')
world[world['highlight'] == 'other'].plot(ax=ax, color='lightgrey')

# Set the title and display the map
ax.set_title('World Map with Highlighted Countries')
plt.show()
