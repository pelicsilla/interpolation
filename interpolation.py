import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.colors import BoundaryNorm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from metpy.interpolate import interpolate_to_grid, remove_nan_observations
from metpy.plots import add_metpy_logo


def load_data(filepath):
    """Load data from a CSV file."""
    return pd.read_csv(filepath, delimiter=",")

def transform_coordinates(lon, lat, projection):
    """Transform geographic coordinates to a specified projection."""
    return projection.transform_points(ccrs.Geodetic(), lon, lat).T


def interpolate_temperature(x, y, temp, resolution=5000):
    """
    Interpolate temperature data to a grid.

    Parameters:
    - x, y: Coordinates
    - temp: Temperature values
    - resolution: Horizontal resolution of the grid
    """
    x_masked, y_masked, temp_masked = remove_nan_observations(x, y, temp)
    grid_x, grid_y, grid_temp = interpolate_to_grid(
        x_masked, y_masked, temp_masked,
        interp_type="natural_neighbor",
        minimum_neighbors=3,
        search_radius=400000,
        hres=resolution,
    )
    grid_temp = np.ma.masked_where(np.isnan(grid_temp), grid_temp)
    return grid_x, grid_y, grid_temp

def setup_map(projection, extent):
    """Set up a Cartopy map with specific features."""
    fig = plt.figure(figsize=(14, 8))
    ax = fig.add_subplot(1, 1, 1, projection=projection)
    ax.set_extent(extent)

    features = [
        cfeature.STATES.with_scale("50m"),
        cfeature.OCEAN,
        cfeature.LAKES,
        cfeature.RIVERS,
        cfeature.COASTLINE.with_scale("50m"),
        cfeature.BORDERS,
    ]
    for feature in features:
        ax.add_feature(feature, linestyle=":" if feature == cfeature.BORDERS else "-")

    return fig, ax

def plot_temperature(ax, x, y, temp, levels, cmap):
    """Plot temperature data on the map."""
    norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

    # Contour lines
    cs = ax.contour(x, y, temp, colors="k", levels=levels[::2])
    ax.clabel(cs, inline=1, fontsize=12, fmt="%i")

    # Filled contours
    mmb = ax.pcolormesh(x, y, temp, cmap=cmap, norm=norm)
    return mmb

def main(filepath, output_filename):
    """Main function to process data and generate a temperature map."""
    # Projection settings
    to_proj = ccrs.AlbersEqualArea(central_longitude=19.0, central_latitude=45.0)
    extent = [15, 25, 44, 50]

    # Load and process data
    data = load_data(filepath)
    lon, lat = data["Lon"].values, data["Lat"].values
    temp = data["Temp"].values
    xp, yp, _ = transform_coordinates(lon, lat, to_proj)
    tempx, tempy, temp_grid = interpolate_temperature(xp, yp, temp)

    # Map setup
    fig, ax = setup_map(to_proj, extent)
    levels = list(range(-20, 40, 1))
    cmap = plt.get_cmap("coolwarm")

    # Plot temperature
    mmb = plot_temperature(ax, tempx, tempy, temp_grid, levels, cmap)
    cbar = fig.colorbar(mmb, shrink=0.6, pad=0.04, boundaries=levels)
    cbar.ax.tick_params(labelsize=14)
    cbar.set_label("Temperature (°C)", fontsize=18)
    ax.set_title("Surface Temperature - natural_neighbor", fontsize=22)

    plt.savefig(output_filename) #, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    main("adat.csv", "Temp_natural_neighbor.png")
