from pychartdir import *
from random import shuffle


def next_color():
    color_counter = 0
    colors_set = [0xf0f8ff, 0x8b8378, 0x7fffd4, 0x458b74, 0x838b8b, 0x0000ff, 0x00008b, 0x8a2be2, 0x8b2323, 0x7fff00, 0x458b00, 0xff7f24, 0xcd661d, 0x6495ed, 0x006400, 0x556b2f, 0xcaff70, 0x9932cc, 0x68228b, 0xff1493, 0xffd700, 0xadff2f, 0xff0000, 0x8b0000]
    shuffle(colors_set)
    color_counter += 1
    return colors_set[color_counter - 1]


def create(scheme):

    way_list = list()
    trains_list = list()
    for way in scheme.ways:
        way_list.append(way)
    for train in scheme.trains:
        trains_list.append(train)

    way_labels = list()
    for way in way_list:
        way_labels.append(str(way.stations_on_ends))

    way_indexes = list()
    start_dates = list()
    end_dates = list()
    colors_list = list()
    trains_colors_list = list()
    for train in trains_list:
        train_color = next_color()
        trains_colors_list.append(train_color)
        schedule = train.schedule
        for position in schedule:
            if position.way() in way_list:
                if position.time_in_way != 0:
                    index = way_list.index(position.way())
                    way_indexes.append(index)
                    start_dates.append(position.time - 1)
                    end_dates.append(position.time)
                    colors_list.append(train_color)



    # # The tasks for the gantt chart
    # way_labels = ["1", "2", "3"]
    #
    # # The task index, start date, end date and color for each bar
    # way_indexes = [0, 0, 1]
    # start_dates = [0, 5, 10]
    # end_dates = [5, 10, 15]
    # colors_list = [0x00cc00, 0x00cc00, 0x00cc00]

    # Create a XYChart object of size 620 x 325 pixels. Set background color to light red (0xffcccc),
    # with 1 pixel 3D border effect.
    c = XYChart(620, 325, 0xffcccc, 0x000000, 1)

    # Add a title to the chart using 15 points Times Bold Itatic font, with white (ffffff) text on a
    # dark red (800000) background
    c.addTitle("Mutli-Color Gantt Chart Demo", "timesbi.ttf", 15, 0xffffff).setBackground(0x800000)

    # Set the plotarea at (140, 55) and of size 460 x 200 pixels. Use alternative white/grey background.
    # Enable both horizontal and vertical grids by setting their colors to grey (c0c0c0). Set vertical
    # major grid (represents month boundaries) 2 pixels in width
    c.setPlotArea(140, 55, 460, 200, 0xffffff, 0xeeeeee, LineColor, 0xc0c0c0, 0xc0c0c0).setGridWidth(2,
        1, 1, 1)

    # swap the x and y axes to create a horziontal box-whisker chart
    c.swapXY()

    # Set the y-axis to shown on the top (right + swapXY = top)
    c.setYAxisOnRight()

    # Set the labels on the x axis
    c.xAxis().setLabels(way_labels)

    # Reverse the x-axis scale so that it points downwards.
    c.xAxis().setReverse()

    # Set the horizontal ticks and grid lines to be between the bars
    c.xAxis().setTickOffset(0.5)

    # Add a multi-color box-whisker layer to represent the gantt bars
    layer = c.addBoxWhiskerLayer2(start_dates, end_dates, None, None, None, colors_list)
    layer.setXData(way_indexes)
    layer.setBorderColor(SameAsMainColor)

    # Divide the plot area height ( = 200 in this chart) by the number of tasks to get the height of
    # each slot. Use 80% of that as the bar height.
    layer.setDataWidth(int(200 * 4 / 5 / len(way_labels)))

    # Add a legend box at (140, 265) - bottom of the plot area. Use 8pt Arial Bold as the font with
    # auto-grid layout. Set the width to the same width as the plot area. Set the backgorund to grey
    # (dddddd).
    legendBox = c.addLegend2(140, 265, AutoGrid, "arialbd.ttf", 8)
    legendBox.setWidth(461)
    legendBox.setBackground(0xdddddd)

    # The keys for the scatter layers (milestone symbols) will automatically be added to the legend box.
    # We just need to add keys to show the meanings of the bar colors.

    for train, train_color in zip(trains_list, trains_colors_list):
        legendBox.addKey(train.name, train_color)

    # Output the chart
    c.makeChart("colorgantt.png")