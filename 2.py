#This for  analyzing and visualizing environmental data from the Tobol River

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MaxNLocator
import matplotlib.gridspec as gridspec

# Set the style for all visualizations
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("colorblind")

# Create the water quality data along river stations
stations = ['Headwaters', 'Station 2', 'Station 3', 'Station 4', 'Station 5', 'Station 6', 'Station 7', 'River Mouth']
distances = [0, 200, 400, 600, 800, 1000, 1200, 1400]
do_values = [9.2, 8.9, 8.6, 8.3, 8.0, 7.8, 7.7, 7.6]
bod_values = [2.1, 2.5, 3.1, 3.5, 3.9, 4.2, 4.4, 4.5]
tn_values = [0.84, 1.15, 1.56, 1.92, 2.21, 2.45, 2.58, 2.63]
tp_values = [0.06, 0.09, 0.14, 0.17, 0.20, 0.22, 0.23, 0.24]
ph_values = [7.3, 7.4, 7.6, 7.7, 7.8, 7.9, 8.0, 8.0]

water_quality_df = pd.DataFrame({
    'station': stations,
    'distance': distances,
    'DO': do_values,
    'BOD': bod_values,
    'TN': tn_values,
    'TP': tp_values,
    'pH': ph_values
})

# Create seasonal variation data
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
do_seasonal = [7.1, 6.8, 7.4, 8.6, 9.1, 8.4, 7.8, 7.2, 7.9, 8.3, 8.5, 7.8]
temp_seasonal = [0.5, 0.2, 1.8, 5.6, 12.4, 17.5, 22.3, 21.8, 16.2, 9.4, 3.1, 0.9]
flow_seasonal = [105, 90, 250, 1200, 2800, 1600, 850, 620, 480, 310, 190, 145]

seasonal_df = pd.DataFrame({
    'month': months,
    'DO': do_seasonal,
    'temp': temp_seasonal,
    'flow': flow_seasonal
})

# Create pollution source data
pollution_sources = ['Municipal Wastewater', 'Industrial Discharges', 'Agricultural Runoff', 'Urban Runoff', 'Atmospheric Deposition']
pollution_values = [32, 24, 28, 10, 6]

pollution_df = pd.DataFrame({
    'source': pollution_sources,
    'percentage': pollution_values
})

# Create ecological status data
reaches = ['Upper Reach', 'Upper-Middle Reach', 'Middle Reach', 'Lower-Middle Reach', 'Lower Reach']
benthos_values = [3.2, 2.9, 2.6, 2.3, 2.1]
fish_values = [3.4, 3.1, 2.8, 2.5, 2.2]
macrophytes_values = [3.0, 2.7, 2.5, 2.2, 2.0]
overall_values = [3.2, 2.9, 2.6, 2.3, 2.1]

ecological_df = pd.DataFrame({
    'reach': reaches,
    'benthos': benthos_values,
    'fish': fish_values,
    'macrophytes': macrophytes_values,
    'overall': overall_values
})

# Create historical trend data
years = list(range(2015, 2025))
do_trend = [7.2, 7.3, 7.3, 7.4, 7.4, 7.5, 7.5, 7.6, 7.6, 7.6]
bod_trend = [5.1, 5.0, 4.9, 4.8, 4.7, 4.7, 4.6, 4.6, 4.5, 4.5]
tn_trend = [2.95, 2.90, 2.85, 2.83, 2.80, 2.76, 2.72, 2.68, 2.65, 2.63]
tp_trend = [0.28, 0.27, 0.26, 0.26, 0.25, 0.25, 0.25, 0.24, 0.24, 0.24]

historical_df = pd.DataFrame({
    'year': years,
    'DO': do_trend,
    'BOD': bod_trend,
    'TN': tn_trend,
    'TP': tp_trend
})

# Function to save figures with higher resolution
def save_figure(fig, filename, dpi=300):
    fig.savefig(filename, dpi=dpi, bbox_inches='tight')
    plt.close(fig)

# 1. Water Quality Parameters Along the Tobol River
def plot_water_quality():
    fig, ax1 = plt.subplots(figsize=(12, 8))
    
    # Plot DO line
    color = 'tab:blue'
    ax1.set_xlabel('Distance from source (km)')
    ax1.set_ylabel('Dissolved Oxygen (mg/L)', color=color)
    ax1.plot(water_quality_df['distance'], water_quality_df['DO'], color=color, linewidth=2, marker='o', label='DO (mg/L)')
    ax1.tick_params(axis='y', labelcolor=color)
    
    # Create a second y-axis for BOD
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('BOD (mg/L)', color=color)
    ax2.plot(water_quality_df['distance'], water_quality_df['BOD'], color=color, linewidth=2, marker='s', label='BOD (mg/L)')
    ax2.tick_params(axis='y', labelcolor=color)
    
    # Create a third y-axis for TN
    ax3 = ax1.twinx()
    # Offset the right spine of ax3
    ax3.spines['right'].set_position(('outward', 60))
    color = 'tab:green'
    ax3.set_ylabel('Total Nitrogen (mg/L)', color=color)
    ax3.plot(water_quality_df['distance'], water_quality_df['TN'], color=color, linewidth=2, marker='^', label='TN (mg/L)')
    ax3.tick_params(axis='y', labelcolor=color)
    
    # Create a fourth y-axis for TP
    ax4 = ax1.twinx()
    # Offset the right spine of ax4
    ax4.spines['right'].set_position(('outward', 120))
    color = 'tab:purple'
    ax4.set_ylabel('Total Phosphorus (mg/L)', color=color)
    ax4.plot(water_quality_df['distance'], water_quality_df['TP'], color=color, linewidth=2, marker='d', label='TP (mg/L)')
    ax4.tick_params(axis='y', labelcolor=color)
    
    # Add custom legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    lines3, labels3 = ax3.get_legend_handles_labels()
    lines4, labels4 = ax4.get_legend_handles_labels()
    
    lines = lines1 + lines2 + lines3 + lines4
    labels = labels1 + labels2 + labels3 + labels4
    
    ax1.legend(lines, labels, loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=4)
    
    plt.title('Water Quality Parameters Along the Tobol River', fontsize=16, fontweight='bold')
    plt.grid(True)
    fig.tight_layout()
    
    # Show station names at the bottom
    station_positions = water_quality_df['distance']
    station_names = water_quality_df['station']
    plt.xticks(station_positions, [])
    
    # Add secondary x-axis for station names
    ax5 = ax1.twiny()
    ax5.set_xlim(ax1.get_xlim())
    ax5.set_xticks(station_positions)
    ax5.set_xticklabels(station_names, rotation=45, ha='right')
    ax5.grid(False)
    
    save_figure(fig, 'tobol_water_quality.png')

# 2. Seasonal Variations in Dissolved Oxygen, Temperature, and Flow
def plot_seasonal_variations():
    fig, ax1 = plt.subplots(figsize=(12, 8))
    
    # Plot temperature
    color = 'tab:red'
    ax1.set_xlabel('Month')
    ax1.set_ylabel('Temperature (°C)', color=color)
    ax1.plot(range(len(months)), seasonal_df['temp'], color=color, linewidth=2, marker='o', label='Temperature (°C)')
    ax1.tick_params(axis='y', labelcolor=color)
    
    # Create a second y-axis for DO
    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Dissolved Oxygen (mg/L)', color=color)
    ax2.plot(range(len(months)), seasonal_df['DO'], color=color, linewidth=2, marker='s', label='DO (mg/L)')
    ax2.tick_params(axis='y', labelcolor=color)
    
    # Create a third y-axis for flow
    ax3 = ax1.twinx()
    # Offset the right spine of ax3
    ax3.spines['right'].set_position(('outward', 60))
    color = 'tab:green'
    ax3.set_ylabel('Flow (m³/s)', color=color)
    ax3.plot(range(len(months)), seasonal_df['flow'], color=color, linewidth=2, marker='^', label='Flow (m³/s)')
    ax3.tick_params(axis='y', labelcolor=color)
    
    # Add custom legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    lines3, labels3 = ax3.get_legend_handles_labels()
    
    lines = lines1 + lines2 + lines3
    labels = labels1 + labels2 + labels3
    
    ax1.legend(lines, labels, loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=3)
    
    plt.title('Seasonal Variations in Temperature, Dissolved Oxygen, and Flow', fontsize=16, fontweight='bold')
    plt.grid(True)
    plt.xticks(range(len(months)), months)
    fig.tight_layout()
    
    save_figure(fig, 'tobol_seasonal_variations.png')

# 3. Contribution of Different Pollution Sources
def plot_pollution_sources():
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create pie chart with percentages
    wedges, texts, autotexts = ax.pie(
        pollution_df['percentage'], 
        labels=pollution_df['source'],
        autopct='%1.1f%%',
        startangle=90,
        shadow=True,
        explode=[0.05, 0, 0, 0, 0],
        colors=sns.color_palette("Set3", len(pollution_df))
    )
    
    # Style the pie chart text
    plt.setp(autotexts, size=10, weight='bold')
    plt.setp(texts, size=12)
    
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    plt.title('Contribution of Different Pollution Sources to the Tobol River', fontsize=16, fontweight='bold')
    
    save_figure(fig, 'tobol_pollution_sources.png')

# 4. Ecological Status Assessment
def plot_ecological_status():
    fig, ax = plt.subplots(figsize=(12, 8))
    
    bar_width = 0.2
    x = np.arange(len(reaches))
    
    # Plot bars for each ecological component
    ax.bar(x - bar_width*1.5, ecological_df['benthos'], bar_width, label='Benthic Macroinvertebrates', color='tab:blue')
    ax.bar(x - bar_width/2, ecological_df['fish'], bar_width, label='Fish', color='tab:orange')
    ax.bar(x + bar_width/2, ecological_df['macrophytes'], bar_width, label='Aquatic Plants', color='tab:green')
    ax.bar(x + bar_width*1.5, ecological_df['overall'], bar_width, label='Overall Assessment', color='tab:red')
    
    # Add labels, title and custom x-axis tick labels
    ax.set_xlabel('River Reach')
    ax.set_ylabel('Ecological Quality Index (0-5)')
    ax.set_title('Ecological Status Assessment Along the Tobol River', fontsize=16, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(reaches)
    ax.legend()
    
    # Set y-axis limits
    ax.set_ylim(0, 5)
    
    # Add reference lines for quality classes
    ax.axhline(y=4, color='green', linestyle='--', alpha=0.7, label='High Status')
    ax.axhline(y=3, color='lightgreen', linestyle='--', alpha=0.7, label='Good Status')
    ax.axhline(y=2, color='orange', linestyle='--', alpha=0.7, label='Moderate Status')
    ax.axhline(y=1, color='red', linestyle='--', alpha=0.7, label='Poor Status')
    
    # Add text labels to indicate quality classes
    plt.text(len(reaches)-1, 4.5, 'High Status', ha='right', va='center', color='green')
    plt.text(len(reaches)-1, 3.5, 'Good Status', ha='right', va='center', color='green')
    plt.text(len(reaches)-1, 2.5, 'Moderate Status', ha='right', va='center', color='orange')
    plt.text(len(reaches)-1, 1.5, 'Poor Status', ha='right', va='center', color='red')
    plt.text(len(reaches)-1, 0.5, 'Bad Status', ha='right', va='center', color='darkred')
    
    plt.grid(True, axis='y')
    fig.tight_layout()
    
    save_figure(fig, 'tobol_ecological_status.png')

# 5. Long-term Trends in Key Water Quality Parameters
def plot_historical_trends():
    fig, ax1 = plt.subplots(figsize=(12, 8))
    
    # Plot DO trend
    color = 'tab:blue'
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Dissolved Oxygen (mg/L)', color=color)
    ax1.plot(historical_df['year'], historical_df['DO'], color=color, linewidth=2, marker='o', label='DO (mg/L)')
    ax1.tick_params(axis='y', labelcolor=color)
    
    # Create a second y-axis for BOD
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('BOD (mg/L)', color=color)
    ax2.plot(historical_df['year'], historical_df['BOD'], color=color, linewidth=2, marker='s', label='BOD (mg/L)')
    ax2.tick_params(axis='y', labelcolor=color)
    
    # Create a third y-axis for TN
    ax3 = ax1.twinx()
    # Offset the right spine of ax3
    ax3.spines['right'].set_position(('outward', 60))
    color = 'tab:green'
    ax3.set_ylabel('Total Nitrogen (mg/L)', color=color)
    ax3.plot(historical_df['year'], historical_df['TN'], color=color, linewidth=2, marker='^', label='TN (mg/L)')
    ax3.tick_params(axis='y', labelcolor=color)
    
    # Create a fourth y-axis for TP
    ax4 = ax1.twinx()
    # Offset the right spine of ax4
    ax4.spines['right'].set_position(('outward', 120))
    color = 'tab:purple'
    ax4.set_ylabel('Total Phosphorus (mg/L)', color=color)
    ax4.plot(historical_df['year'], historical_df['TP'], color=color, linewidth=2, marker='d', label='TP (mg/L)')
    ax4.tick_params(axis='y', labelcolor=color)
    
    # Add custom legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    lines3, labels3 = ax3.get_legend_handles_labels()
    lines4, labels4 = ax4.get_legend_handles_labels()
    
    lines = lines1 + lines2 + lines3 + lines4
    labels = labels1 + labels2 + labels3 + labels4
    
    ax1.legend(lines, labels, loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=4)
    
    plt.title('Long-term Trends in Key Water Quality Parameters (2015-2024)', fontsize=16, fontweight='bold')
    plt.grid(True)
    ax1.set_xticks(historical_df['year'])
    ax1.set_xticklabels(historical_df['year'], rotation=45)
    fig.tight_layout()
    
    save_figure(fig, 'tobol_historical_trends.png')

# Create a comprehensive dashboard with all plots
def create_dashboard():
    fig = plt.figure(figsize=(16, 20))
    
    # Create grid layout
    gs = gridspec.GridSpec(8, 4)
    
    # Title area
    title_ax = plt.subplot(gs[0, :])
    title_ax.text(0.5, 0.5, 'TOBOL RIVER ENVIRONMENTAL ANALYSIS DASHBOARD', 
                 horizontalalignment='center', verticalalignment='center', 
                 fontsize=20, fontweight='bold')
    title_ax.axis('off')
    
    # Date and author area
    date_ax = plt.subplot(gs[1, :])
    date_ax.text(0.5, 0.5, 'Analysis Period: 2015-2024 | Generated: April 17, 2025', 
                horizontalalignment='center', verticalalignment='center')
    date_ax.axis('off')
    
    # Water Quality Parameters Plot
    wq_ax = plt.subplot(gs[2:4, :])
    
    # Plot DO line
    color = 'tab:blue'
    wq_ax.set_xlabel('Distance from source (km)')
    wq_ax.set_ylabel('Concentration (mg/L)')
    wq_ax.plot(water_quality_df['distance'], water_quality_df['DO'], color='tab:blue', linewidth=2, marker='o', label='DO (mg/L)')
    wq_ax.plot(water_quality_df['distance'], water_quality_df['BOD'], color='tab:red', linewidth=2, marker='s', label='BOD (mg/L)')
    wq_ax.plot(water_quality_df['distance'], water_quality_df['TN'], color='tab:green', linewidth=2, marker='^', label='TN (mg/L)')
    
    # Plot TP on secondary y-axis due to scale difference
    wq_ax2 = wq_ax.twinx()
    wq_ax2.plot(water_quality_df['distance'], water_quality_df['TP'], color='tab:purple', linewidth=2, marker='d', label='TP (mg/L)')
    wq_ax2.set_ylabel('TP (mg/L)')
    
    # Add custom legend
    lines1, labels1 = wq_ax.get_legend_handles_labels()
    lines2, labels2 = wq_ax2.get_legend_handles_labels()
    lines = lines1 + lines2
    labels = labels1 + labels2
    wq_ax.legend(lines, labels, loc='upper right')
    
    wq_ax.set_title('Water Quality Parameters Along the Tobol River', fontsize=14, fontweight='bold')
    wq_ax.grid(True)
    
    # Plot station names at the bottom
    station_positions = water_quality_df['distance']
    station_names = water_quality_df['station']
    wq_ax.set_xticks(station_positions)
    wq_ax.set_xticklabels(station_names, rotation=45, ha='right')
    
    # Seasonal Variations Plot
    seasonal_ax = plt.subplot(gs[4:6, :2])
    
    seasonal_ax.plot(range(len(months)), seasonal_df['temp'], color='tab:red', linewidth=2, marker='o', label='Temperature (°C)')
    seasonal_ax.plot(range(len(months)), seasonal_df['DO'], color='tab:blue', linewidth=2, marker='s', label='DO (mg/L)')
    seasonal_ax.set_ylabel('Temperature (°C) / DO (mg/L)')
    seasonal_ax.set_xticks(range(len(months)))
    seasonal_ax.set_xticklabels(months)
    
    # Plot flow on secondary y-axis due to scale difference
    seasonal_ax2 = seasonal_ax.twinx()
    seasonal_ax2.plot(range(len(months)), seasonal_df['flow'], color='tab:green', linewidth=2, marker='^', label='Flow (m³/s)')
    seasonal_ax2.set_ylabel('Flow (m³/s)')
    
    lines1, labels1 = seasonal_ax.get_legend_handles_labels()
    lines2, labels2 = seasonal_ax2.get_legend_handles_labels()
    lines = lines1 + lines2
    labels = labels1 + labels2
    seasonal_ax.legend(lines, labels, loc='upper right')
    
    seasonal_ax.set_title('Seasonal Variations', fontsize=14, fontweight='bold')
    seasonal_ax.grid(True)
    
    # Pollution Sources Plot
    pollution_ax = plt.subplot(gs[4:6, 2:], aspect='equal')
    
    # Create pie chart with percentages
    wedges, texts, autotexts = pollution_ax.pie(
        pollution_df['percentage'], 
        labels=pollution_df['source'],
        autopct='%1.1f%%',
        startangle=90,
        shadow=True,
        explode=[0.05, 0, 0, 0, 0],
        colors=sns.color_palette("Set3", len(pollution_df))
    )
    
    # Style the pie chart text
    plt.setp(autotexts, size=8, weight='bold')
    plt.setp(texts, size=9)
    
    pollution_ax.set_title('Pollution Sources', fontsize=14, fontweight='bold')
    
    # Ecological Status Plot
    eco_ax = plt.subplot(gs[6:, :2])
    
    bar_width = 0.2
    x = np.arange(len(reaches))
    
    # Plot bars for each ecological component
    eco_ax.bar(x - bar_width*1.5, ecological_df['benthos'], bar_width, label='Benthos', color='tab:blue')
    eco_ax.bar(x - bar_width/2, ecological_df['fish'], bar_width, label='Fish', color='tab:orange')
    eco_ax.bar(x + bar_width/2, ecological_df['macrophytes'], bar_width, label='Plants', color='tab:green')
    eco_ax.bar(x + bar_width*1.5, ecological_df['overall'], bar_width, label='Overall', color='tab:red')
    
    # Add labels and custom x-axis tick labels
    eco_ax.set_xlabel('River Reach')
    eco_ax.set_ylabel('Ecological Quality Index (0-5)')
    eco_ax.set_xticks(x)
    eco_ax.set_xticklabels([r.replace(' Reach', '') for r in reaches], rotation=45, ha='right')
    eco_ax.legend(loc='upper right', fontsize=8)
    
    # Set y-axis limits
    eco_ax.set_ylim(0, 5)
    eco_ax.grid(True, axis='y')
    
    eco_ax.set_title('Ecological Status Assessment', fontsize=14, fontweight='bold')
    
    # Historical Trend Plot
    hist_ax = plt.subplot(gs[6:, 2:])
    
    hist_ax.plot(historical_df['year'], historical_df['DO'], color='tab:blue', linewidth=2, marker='o', label='DO')
    hist_ax.plot(historical_df['year'], historical_df['BOD'], color='tab:red', linewidth=2, marker='s', label='BOD')
    hist_ax.plot(historical_df['year'], historical_df['TN'], color='tab:green', linewidth=2, marker='^', label='TN')
    hist_ax.plot(historical_df['year'], historical_df['TP'], color='tab:purple', linewidth=2, marker='d', label='TP')
    
    hist_ax.set_xlabel('Year')
    hist_ax.set_ylabel('Concentration (mg/L)')
    hist_ax.set_xticks(historical_df['year'][::2])  # Show every other year for clarity
    hist_ax.set_xticklabels(historical_df['year'][::2], rotation=45)
    hist_ax.legend(loc='upper right', fontsize=8)
    hist_ax.grid(True)
    
    hist_ax.set_title('Historical Water Quality Trends', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    save_figure(fig, 'tobol_river_dashboard.png', dpi=300)
    
if __name__ == "__main__":
    print("Generating plots for Tobol River environmental analysis...")
    plot_water_quality()
    plot_seasonal_variations()
    plot_pollution_sources()
    plot_ecological_status()
    plot_historical_trends()
    create_dashboard()
    print("All plots have been generated successfully!")