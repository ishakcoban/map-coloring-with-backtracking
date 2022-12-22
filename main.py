import networkx as nx
import plotly.express as px
from matplotlib import pyplot as plt
from infos import countries
from infos import colors
from infos import neighbour_info


def drawConstraintGraph(colorMap):
    # Create an empty graph
    G = nx.Graph()

    # Add nodes to the graph
    for node in neighbour_info.keys():
        G.add_node(node)

    # Add edges to the graph
    for node, neighbors in neighbour_info.items():
        if len(neighbors) != 0:
            for neighbor in neighbors:
                G.add_edge(node, neighbor)

    # Set node colors
    node_colors = []
    for node in neighbour_info.keys():
        if colorMap[node] is not None:
            node_colors.append(colorMap[node])
        else:
            node_colors.append('grey')

    # Set edge colors
    edge_colors = ['black' for _ in range(G.number_of_edges())]

    pos = {
        'Argentina': (1, 0),
        'Bolivia': (5.6, 0.47),
        'Brazil': (5.1, 8.20),
        'Chile': (5, -7),
        'Colombia': (9, 6),
        'Ecuador': (9, 1),
        'Guyana': (4.8, 15.24),
        'Paraguay': (4.2, 3.19),
        'Peru': (8, 3),
        'Suriname': (3.3, 13.3),
        'Uruguay': (1.8, 9.8),
        'Venezuela': (8, 14),
        'Falkland Islands': (7.8, -5.6)
    }

    # Plot the graph
    nx.draw(G, node_color=node_colors, pos=pos, edge_color=edge_colors, with_labels=True, node_size=3500, font_size=9)

    plt.show()


def isValid(coloredMap):
    # control neighbours of country
    for country in neighbour_info:
        neighbours = (neighbour_info[country])
        colorOfCountry = coloredMap[country]

        for country in neighbours:
            colorOfNeighbour = coloredMap[country]
            # must not be same two adjacent of country
            if colorOfCountry == colorOfNeighbour:
                return False

    return True


def colorizeCountries():
    color_index = 0
    country_index = 0
    counter = 0
    result = True
    while True:

        if country_index >= len(countries):
            break

        if counter == len(colors):
            result = False
            break
        before = country_index
        colorMap.update({countries[country_index]: colors[color_index]})
        if not isValid(colorMap):
            country_index -= 1
        if color_index < 3:
            color_index += 1
        else:
            color_index = 0
        country_index += 1
        if before == country_index:
            counter += 1
        else:
            counter = 0

    return result


# Do not modify this method, only call it with an appropriate argument.
# colormap should be a dictionary having countries as keys and colors as values.


def plot_choropleth(colormap):
    fig = px.choropleth(locationmode="country names",
                        locations=countries,
                        color=countries,
                        color_discrete_sequence=[colormap[c] for c in countries],
                        scope="south america")
    fig.show()


# Implement main to call necessary functions
if __name__ == "__main__":

    temp = dict()
    # sort country according to neighbours number
    for country in countries:
        temp.update({country: len(neighbour_info[country])})
    temp = list(sorted(temp.items(), key=lambda kv: kv[1]))
    countries.clear()

    i = len(temp) - 1

    while i > -1:
        countries.append(temp[i][0])
        i -= 1

    colorMap = dict()

    # initially fill the map color by none
    for i in range(len(countries)):
        colorMap.update({countries[i]: F"NONE{i}"})

    # check optimum solution
    if colorizeCountries():
        plot_choropleth(colormap=colorMap)
        drawConstraintGraph(colorMap)
