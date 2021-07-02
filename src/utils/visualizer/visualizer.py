import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from utils.enums import Charts


def get_median(numbers: list) -> int:
    """
    Get the median from a list of numbers.
    :param numbers: The list containing the numbers.
    :return: The median.
    """
    numbers.sort()
    return numbers[len(numbers) // 2]


def get_exploding_values(list_of_values: list) -> tuple:
    """
    This function will determine which value is the largest in the list, and
    will return a tuple containing the information that will have the largest percentage
    within the pie chart pop off.
    :param list_of_values:
    :return: A tuple of 'exploding' values for a pie chart.
    """
    exploding_values = [0.0 for value in list_of_values]
    largest_value = list_of_values[0]
    pop_out_index = 0

    # iterate through the list of values and find the index that contains the largest value.
    for i, value in enumerate(list_of_values):
        if value > largest_value:
            largest_value = value
            pop_out_index = i

    # set the popout value
    exploding_values[pop_out_index] = 0.1

    return tuple(exploding_values)


def set_up_bar_chart(title: str, list_of_values: list, list_of_labels: list, currency_labels: list) -> None:
    """
    Configure the bar chart visualization.
    :param title: The title to be displayed on the visualization.
    :param list_of_values: The list containing the values to plot.
    :param list_of_labels: The list containing the labels that correspond to the values.
    :param currency_labels: The list containing the currency labels.
    """
    fig, ax1 = plt.subplots(figsize=(12, 7))  # Create the figure
    fig.subplots_adjust(left=0.115, right=0.88)

    pos = np.arange(len(list_of_labels))

    # plot the bars horizontally
    ax1.barh(pos, list_of_values, align='center', height=0.5, tick_label=list_of_labels)

    # display vertical grid lines
    ax1.xaxis.set_major_locator(MaxNLocator(11))
    ax1.xaxis.grid(True, linestyle='--', which='major', color='grey', alpha=.25)

    # Plot a solid vertical grid-line to highlight the median position
    ax1.axvline(get_median(list_of_values), color='red', alpha=0.25)

    ax2 = ax1.twinx()

    # Set the tick locations
    ax2.set_yticks(pos)

    # Set equal limits on both yaxis so that the ticks line up
    ax2.set_ylim(ax1.get_ylim())

    # title
    ax1.set_title(title)
    fig.canvas.manager.set_window_title(title)

    # labels
    ax1.set_xlabel("Dollar Range")
    ax1.set_ylabel("Date Range")

    # set the labels on the right side of the visualization
    ax2.set_yticklabels(currency_labels)
    ax2.set_ylabel("Total Spent", rotation=-90)


def set_up_pie_chart(title: str, list_of_values: list, list_of_labels: list) -> None:
    """
    Configure the pie chart visualization where the slices will be ordered and plotted counter-clockwise.
    :param title: The title to be displayed on the visualization.
    :param list_of_values: The list containing the values to plot.
    :param list_of_labels: The list containing the labels that correspond to the values.
    """
    explode = get_exploding_values(list_of_values)
    width = 12
    height = 9
    fig, ax = plt.subplots(figsize=(width, height))

    np_values = np.array(list_of_values)
    np_labels = np.char.array(list_of_labels)
    percentage = 100 * np_values / np_values.sum()

    patches, texts, dummy = ax.pie(np_values,
                                   explode=explode,
                                   autopct='%1.1f%%',
                                   shadow=True,
                                   startangle=90)

    labels_to_display = [f'{label} - {round(float(percent), 1)}%' for label, percent in zip(np_labels, percentage)]

    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # title
    ax.set_title(title)
    fig.canvas.manager.set_window_title(title)

    plt.legend(patches, labels_to_display, loc='lower left', fontsize=8)
    plt.tight_layout()


def display_visual(title: str, chart_type: Charts = Charts.BAR, list_of_values: list = None,
                   list_of_labels: list = None, currency_labels: list = None) -> None:
    """
    Display a visualization.
    :param title: The title to display at the top of the visualization.
    :param chart_type: The type of chart to display.
    :param list_of_values: List containing all of the necessary values to display information.
    :param list_of_labels: List containing all of the labels to display on the visualization.
    :param currency_labels: List containing labels of currency information to display.
    """
    if chart_type.name == Charts.BAR.name:
        set_up_bar_chart(title=title,
                         list_of_values=list_of_values,
                         list_of_labels=list_of_labels,
                         currency_labels=currency_labels)
    elif chart_type.name == Charts.HISTOGRAM.name:
        # TODO
        pass
    elif chart_type.name == Charts.PIE.name:
        set_up_pie_chart(title=title,
                         list_of_values=list_of_values,
                         list_of_labels=list_of_labels)

    plt.show()


def display_pie_chart(title: str, merchants: dict) -> None:
    """
    TODO: This has yet to be used within the application.
    Display a Pie Chart that contains information about where the most money was spent over a period of time.
    :param title: The title to display at the top of the visualization.
    :param merchants: Dictionary containing merchant information.
                      Note: The form of the dictionary is: { MerchantName : TotalSpent }.
    """
    list_of_values = []
    list_of_labels = []
    for key in merchants:
        list_of_labels.append(key)
        list_of_values.append(merchants[key])

    display_visual(title=title,
                   list_of_values=list_of_values,
                   list_of_labels=list_of_labels,
                   chart_type=Charts.PIE
                   )


def display_bar_chart(title: str, list_of_values: list, list_of_labels: list, currency_labels: list) -> None:
    """
    Display a Bar Chart that contains information about how much money was spent over a period of time.
    :param title: The title to display at the top of the visualization.
    :param list_of_values: List containing all of the necessary values to display information.
    :param list_of_labels: List containing all of the labels to display on the visualization.
    :param currency_labels: List containing labels of currency information to display.
    """
    display_visual(title=title,
                   list_of_values=list_of_values,
                   list_of_labels=list_of_labels,
                   currency_labels=currency_labels,
                   chart_type=Charts.BAR)
