import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


def plot_line_graph(x, y, xlabel, ylabel, title, labels):
    """ Funtion to Create plot_line_graph. Arguments:
        list of values for xaxis
        list of values for yaxis
        xlabel, ylabel and titel value
        color name
        label value
    """
    plt.figure(figsize=(7, 5))
    for index in range(len(y)):
        plt.plot(x, y[index], label=labels[index], linestyle='-.', marker='s')
    plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=6))
    plt.xticks(rotation=90)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.show()
    return


def plot_bar_graph(dataframe, xlabel, ylabel, title):
    dataframe.plot(kind='bar', figsize=(10, 6))
    # Set plot labels and title
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()
    return


def draw_scatter_plot(
        x,
        y,
        title='Scatter Plot',
        xlabel='X-Axis',
        ylabel='Y-Axis',
        color='blue',
        marker='o',
        label=None):
    """
    Draw a scatter plot using Matplotlib.

    Parameters:
        x (list): X-axis data points.
        y (list): Y-axis data points.
        title (str): Title of the scatter plot.
        xlabel (str): Label for the X-axis.
        ylabel (str): Label for the Y-axis.
        color (str): Color of the markers.
        marker (str): Marker style.
        label (str): Label for the legend.
    """
    plt.scatter(x, y, color=color, marker=marker, label=label)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    if label is not None:
        plt.legend()
    plt.show()


def heat_map_fun(df, title, cmap='viridis'):
    correlation_matrix = df.corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    heatmap = ax.pcolormesh(correlation_matrix, cmap=cmap)
    cbar = plt.colorbar(heatmap)
    for i in range(len(correlation_matrix.columns)):
        for j in range(len(correlation_matrix.columns)):
            ax.text(j + 0.5, i + 0.5, f'{correlation_matrix.iloc[i, j]:.2f}',
                    ha='center', va='center', color='white')
    ax.set_xticks(range(len(correlation_matrix.columns)))
    ax.set_yticks(range(len(correlation_matrix.columns)))
    ax.set_xticklabels(correlation_matrix.columns, rotation=90)
    ax.set_yticklabels(correlation_matrix.columns)
    plt.title(title)
    plt.show()


def extract_data(df, countries, start_year, up_to_year):
    df = df.T
    df = df.drop(['Country Code', 'Indicator Name', 'Indicator Code'])
    df.columns = df.iloc[0]
    df = df.drop(['Country Name'])
    df = df.reset_index()
    df['Years'] = df['index']
    df = df.drop('index', axis=1)
    df = df[(df['Years'] >= start_year) & (df['Years'] <= up_to_year)]
    selected_data = df[countries]
    selected_data = selected_data.fillna(selected_data.iloc[:, :-1].mean())
    return selected_data


def data_for_countries(
        data_frame_list,
        n_countries,
        names,
        start_year,
        end_year):
    country_data = []
    for i, data in enumerate(data_frame_list):
        data = extract_data(data, n_countries, start_year, end_year)
        data = data.rename(columns={n_countries[0]: names[i]})
        country_data.append(data)
    country_data = pd.concat(country_data, axis=1)
    country_data = country_data.T.drop_duplicates().T
    country_data = country_data.drop('Years', axis=1)
    return country_data


def get_data_description(
        data_frame_list,
        n_countries,
        names,
        start_year,
        end_year):
    country_data = []
    for i, data in enumerate(data_frame_list):
        data = extract_data(data, n_countries, start_year, end_year)
        data = data.rename(columns={n_countries[0]: names[i]})
        country_data.append(data)
    country_data = pd.concat(country_data, axis=1)
    country_data = country_data.T.drop_duplicates().T
    country_data = country_data.set_index('Years')
    return country_data


def data_to_lists(df, cols):
    column_lists = [df[col].tolist() for col in cols[:-1]]
    return column_lists


def data_to_draw_bar(df, years):
    df = df[df['Years'].isin(years)]
    df = df.set_index('Years')
    return df


Urban_population = pd.read_csv('Urban_population.csv', skiprows=4)
Forest_area = pd.read_csv('Forest_area.csv', skiprows=4)
Arable_land = pd.read_csv('Arable_land.csv', skiprows=4)
Manufacturing_value_added_USD = pd.read_csv(
    'Manufacturing_value_added_USD.csv', skiprows=4)
cols = [
    'Austria',
    'Belgium',
    'Bulgaria',
    'Croatia',
    'Denmark',
    'Finland',
    'Malta',
    'Years']
start_year = '2000'
end_year = '2021'
plot_line_graph(list(extract_data(Forest_area,
                                  cols,
                                  start_year,
                                  end_year)['Years']),
                data_to_lists(extract_data(Forest_area,
                                           cols,
                                           start_year,
                                           end_year),
                              cols),
                'Years',
                'Sq m',
                'Forest Area (Countries in Europena Union)',
                cols[:-1])
plot_line_graph(list(extract_data(Arable_land,
                                  cols,
                                  start_year,
                                  end_year)['Years']),
                data_to_lists(extract_data(Arable_land,
                                           cols,
                                           start_year,
                                           end_year),
                              cols),
                'Years',
                "Sq m",
                'Arable Land (Countries in Europena Union)',
                cols[:-1])
Manufacturing_value_added_USD = pd.read_csv(
    'Manufacturing_value_added_USD.csv', skiprows=4)
CO2_emissions = pd.read_csv('CO2_emissions.csv', skiprows=4)
years = ['1995', '2000', '2005', '2010', '2015', '2020']
plot_bar_graph(
    data_to_draw_bar(
        extract_data(
            Manufacturing_value_added_USD,
            cols,
            start_year,
            end_year),
        years),
    'Years',
    'USD',
    'Manufacturing value added USD(Countries in Europena Union)')
plot_bar_graph(
    data_to_draw_bar(
        extract_data(
            CO2_emissions,
            cols,
            start_year,
            end_year),
        years),
    'Years',
    "CO2 Emissions",
    "CO2 Emissions (kt) (Countries in Europena Union)")
Energy_use = pd.read_csv('Energy_use.csv', skiprows=4)
Electric_power_consumption = pd.read_csv(
    'Electric_power_consumption.csv', skiprows=4)
Agricultural_land = pd.read_csv('Agricultural_land.csv', skiprows=4)
names = [
    'Forest_area',
    'Urban_population',
    'Manufacturing_GDP',
    'CO2_emissions',
    'Arable_land',
    'Electric_power_consumption',
    'Energy_use']
data_frames = [
    Forest_area,
    Urban_population,
    Manufacturing_value_added_USD,
    CO2_emissions,
    Arable_land,
    Electric_power_consumption,
    Energy_use]
n_countries = ['Austria', 'Years']
heat_map_fun(
    data_for_countries(
        data_frames,
        n_countries,
        names,
        '1990',
        '2020'),
    'Austria',
    'twilight_shifted')
n_countries = ['Croatia', 'Years']
heat_map_fun(
    data_for_countries(
        data_frames,
        n_countries,
        names,
        '1990',
        '2020'),
    'Croatia',
    'Dark2')
n_countries = ['Belgium', 'Years']
heat_map_fun(
    data_for_countries(
        data_frames,
        n_countries,
        names,
        '1990',
        '2020'),
    'Belgium',
    'brg')
get_data_description(data_frames, n_countries, names, '1990', '2020').head()
