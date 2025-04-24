import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set the style for visualizations
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("colorblind")

# Parameters for the Tobol River system (using data from the original code)
# Spatial domain
river_length = 1400  # river length in km
nx = 100  # number of spatial points
dx = river_length / (nx - 1)  # spatial step size
x = np.linspace(0, river_length, nx)  # spatial grid

# Time domain
days = 60  # simulation days
nt = 120  # number of time steps
dt = days / nt  # time step in days
t = np.linspace(0, days, nt)  # time grid

# Model parameters
D = 15.0  # diffusion coefficient (km²/day)
v = 20.0  # advection velocity (km/day)
k = 0.1   # first-order decay rate (1/day)

# Pollution input parameters
input_location = int(0.2 * nx)  # location of pollution input (20% of the way downstream)
input_rate = 2.0  # pollution input rate (mass/day)
input_duration = int(0.1 * nt)  # duration of input (10% of total simulation time)

def solve_1d_dar(D, v, k, x, t, dx, dt, input_location, input_rate, input_duration):
    """
    Solves the 1D Diffusion-Advection-Reaction equation using explicit finite differences.
    """
    # Initialize concentration array
    c = np.zeros((nt, nx))
    
    # Initial condition - clean river (zero concentration everywhere)
    c[0, :] = 0.0
    
    # Compute stability condition number for finite difference method
    alpha = D * dt / (dx**2)
    beta = v * dt / dx
    
    if alpha > 0.5 or abs(beta) > 1:
        print(f"Warning: Numerical instability possible! alpha={alpha}, beta={beta}")
        print("Try decreasing dt or increasing dx.")
    
    # Solve using explicit finite difference method
    for n in range(0, nt-1):
        # Source term - constant input at a specific location for a set duration
        source = np.zeros(nx)
        if n < input_duration:
            source[input_location] = input_rate * dt / dx
        
        # Update concentration using finite differences
        for i in range(1, nx-1):
            # Diffusion term: D * (c[i+1] - 2*c[i] + c[i-1]) / dx²
            diffusion = D * (c[n, i+1] - 2*c[n, i] + c[n, i-1]) / (dx**2)
            
            # Advection term: -v * (c[i] - c[i-1]) / dx (upwind scheme)
            advection = -v * (c[n, i] - c[n, i-1]) / dx
            
            # Reaction term: -k * c[i]
            reaction = -k * c[n, i]
            
            # Update concentration
            c[n+1, i] = c[n, i] + dt * (diffusion + advection + reaction) + source[i]
        
        # Boundary conditions
        # Upstream: fixed concentration (clean water entering)
        c[n+1, 0] = 0.0
        
        # Downstream: zero gradient (concentration doesn't change at outlet)
        c[n+1, -1] = c[n+1, -2]
    
    return c

# Solve the DAR equation
concentration = solve_1d_dar(D, v, k, x, t, dx, dt, input_location, input_rate, input_duration)

# Plot selected time snapshots
def plot_concentration_snapshots():
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Select time points to plot
    time_indices = [0, int(nt/6), int(nt/3), int(2*nt/3), nt-1]
    colors = ['blue', 'green', 'orange', 'red', 'purple']
    
    for i, time_idx in enumerate(time_indices):
        day = t[time_idx]
        ax.plot(x, concentration[time_idx, :], color=colors[i], linewidth=2, 
                label=f'Day {day:.1f}')
    
    # Mark the pollution input location
    ax.axvline(x=x[input_location], color='black', linestyle='--', alpha=0.5, 
               label='Pollution input site')
    
    # Add station markers from the original dataset
    stations = ['Headwaters', 'Station 2', 'Station 3', 'Station 4', 'Station 5', 'Station 6', 'Station 7', 'River Mouth']
    distances = [0, 200, 400, 600, 800, 1000, 1200, 1400]
    
    for station, distance in zip(stations, distances):
        ax.axvline(x=distance, color='gray', linestyle=':', alpha=0.3)
        ax.text(distance, ax.get_ylim()[1]*0.95, station, rotation=90, 
                verticalalignment='top', fontsize=8)
    
    ax.set_xlabel('Distance along river (km)')
    ax.set_ylabel('Pollutant concentration (mass/volume)')
    ax.set_title('Pollutant concentration along the Tobol River at different times', 
                fontsize=16, fontweight='bold')
    ax.legend(loc='upper right')
    ax.grid(True)
    
    plt.tight_layout()
    plt.savefig('tobol_pollution_transport.png', dpi=300)
    plt.close(fig)

# Plot concentration evolution at specific locations
def plot_concentration_evolution():
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Select locations to monitor
    locations = [0, input_location, int(nx/4), int(nx/2), int(3*nx/4), nx-1]
    distances = [x[loc] for loc in locations]
    labels = [f'{dist} km' for dist in distances]
    colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown']
    
    for i, loc in enumerate(locations):
        ax.plot(t, concentration[:, loc], color=colors[i], linewidth=2, label=labels[i])
    
    ax.set_xlabel('Time (days)')
    ax.set_ylabel('Pollutant concentration (mass/volume)')
    ax.set_title('Pollutant concentration over time at different locations', 
                fontsize=16, fontweight='bold')
    ax.legend(loc='upper right')
    ax.grid(True)
    
    plt.tight_layout()
    plt.savefig('tobol_pollution_time_series.png', dpi=300)
    plt.close(fig)

# Create a 2D heatmap of concentration over space and time
def plot_concentration_heatmap():
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create meshgrid for plotting
    X, T = np.meshgrid(x, t)
    
    # Plot concentration heatmap
    im = ax.pcolormesh(X, T, concentration, cmap='viridis', shading='auto')
    
    # Add colorbar
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label('Pollutant concentration (mass/volume)')
    
    # Mark the pollution input
    ax.axhline(y=input_duration*dt, color='red', linestyle='--', alpha=0.7, 
               label='End of pollution input')
    ax.axvline(x=x[input_location], color='red', linestyle='--', alpha=0.7)
    
    ax.set_xlabel('Distance along river (km)')
    ax.set_ylabel('Time (days)')
    ax.set_title('Spatiotemporal evolution of pollutant concentration', 
                fontsize=16, fontweight='bold')
    
    # Mark station locations on x-axis
    stations = ['Headwaters', 'Station 2', 'Station 3', 'Station 4', 'Station 5', 'Station 6', 'Station 7', 'River Mouth']
    distances = [0, 200, 400, 600, 800, 1000, 1200, 1400]
    
    ax.set_xticks(distances)
    ax.set_xticklabels([s.split(' ')[0] for s in stations], rotation=45)
    
    plt.tight_layout()
    plt.savefig('tobol_pollution_heatmap.png', dpi=300)
    plt.close(fig)

# Create an integrated model dashboard
def create_model_dashboard():
    fig = plt.figure(figsize=(16, 20))
    
    # Add title
    plt.suptitle('TOBOL RIVER POLLUTANT TRANSPORT MODEL', fontsize=20, fontweight='bold', y=0.995)
    plt.figtext(0.5, 0.965, f'Simulation Parameters: D={D} km²/day, v={v} km/day, k={k} day⁻¹, Duration={days} days', 
                ha='center', fontsize=12)
    
    # Top plot: concentration snapshots
    ax1 = plt.subplot(3, 1, 1)
    time_indices = [0, int(nt/6), int(nt/3), int(2*nt/3), nt-1]
    colors = ['blue', 'green', 'orange', 'red', 'purple']
    
    for i, time_idx in enumerate(time_indices):
        day = t[time_idx]
        ax1.plot(x, concentration[time_idx, :], color=colors[i], linewidth=2, 
                label=f'Day {day:.1f}')
    
    ax1.axvline(x=x[input_location], color='black', linestyle='--', alpha=0.5, 
               label='Pollution input site')
    
    stations = ['Headwaters', 'Station 2', 'Station 3', 'Station 4', 'Station 5', 'Station 6', 'Station 7', 'River Mouth']
    distances = [0, 200, 400, 600, 800, 1000, 1200, 1400]
    
    for station, distance in zip(stations, distances):
        ax1.axvline(x=distance, color='gray', linestyle=':', alpha=0.3)
        ax1.text(distance, ax1.get_ylim()[1]*0.95, station, rotation=90, 
                verticalalignment='top', fontsize=8)
    
    ax1.set_xlabel('Distance along river (km)')
    ax1.set_ylabel('Pollutant concentration')
    ax1.set_title('A) Pollutant concentration snapshots at different times', fontsize=14)
    ax1.legend(loc='upper right')
    ax1.grid(True)
    
    # Middle plot: concentration time series
    ax2 = plt.subplot(3, 1, 2)
    locations = [0, input_location, int(nx/4), int(nx/2), int(3*nx/4), nx-1]
    distances = [x[loc] for loc in locations]
    labels = [f'{int(dist)} km' for dist in distances]
    colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown']
    
    for i, loc in enumerate(locations):
        ax2.plot(t, concentration[:, loc], color=colors[i], linewidth=2, label=labels[i])
    
    ax2.set_xlabel('Time (days)')
    ax2.set_ylabel('Pollutant concentration')
    ax2.set_title('B) Pollutant concentration over time at different locations', fontsize=14)
    ax2.legend(loc='upper right')
    ax2.grid(True)
    
    # Bottom plot: concentration heatmap
    ax3 = plt.subplot(3, 1, 3)
    X, T = np.meshgrid(x, t)
    im = ax3.pcolormesh(X, T, concentration, cmap='viridis', shading='auto')
    cbar = fig.colorbar(im, ax=ax3)
    cbar.set_label('Pollutant concentration')
    
    ax3.axhline(y=input_duration*dt, color='red', linestyle='--', alpha=0.7, 
               label='End of pollution input')
    ax3.axvline(x=x[input_location], color='red', linestyle='--', alpha=0.7)
    
    ax3.set_xlabel('Distance along river (km)')
    ax3.set_ylabel('Time (days)')
    ax3.set_title('C) Spatiotemporal evolution of pollutant concentration', fontsize=14)
    
    ax3.set_xticks(distances)
    ax3.set_xticklabels([s.split(' ')[0] for s in stations], rotation=45)
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('tobol_pollution_model_dashboard.png', dpi=300)
    plt.close(fig)

if __name__ == "__main__":
    print("Solving 1D diffusion-advection-reaction equation for the Tobol River...")
    plot_concentration_snapshots()
    plot_concentration_evolution()
    plot_concentration_heatmap()
    create_model_dashboard()
    print("Model simulation completed successfully!")