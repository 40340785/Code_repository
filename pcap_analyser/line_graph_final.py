import matplotlib.pyplot as plt
from datetime import datetime, timedelta


def timestamp_round(timestamp, delta):
    """Rounds timestamps to set value"""
    return timestamp + (datetime.min - timestamp) % delta
    # This functions rounds timestamps to nearest second.


def plot_me(timestamp_dict):
    """Creates the line graph"""
    list1 = sorted(timestamp_dict.items())
    # Sorts the timestamp_dictionary.
    x, y = zip(*list1)
    # Zips the dictionary into tuples.
    plt.figure(figsize=(10, 10))
    plt.plot(x, y, 'r')
    plt.ylabel('Packets')
    plt.xlabel('Time')
    plt.show()



timestamp_list = []
timestamp_dict = {}
basic_list = []


def line_graph_main(received_timestamp_list):
    """Sets parameters for the line graph"""
    for x in received_timestamp_list:

        timestamp_list.append(timestamp_round(datetime.fromtimestamp(x), timedelta(seconds=1)))
        # New list created to store the returned value from timestamp_round, modify seconds to what you want.
        basic_list.append(str(datetime.fromtimestamp(x).strftime('%H:%M:%S')))
        # This formats the timestamps into human readable and stores in another list.

    for x in timestamp_list:
        # This takes all the rounded timestamps, and iterates through.
        timestamp_dict[x] = timestamp_list.count(x)
        # Takes each rounded timestamp as the key, the value is the count of how many there are.


    plot_me(timestamp_dict)
    # Passes the timestamp dictionary to function plot_me.











