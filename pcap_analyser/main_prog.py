import socket
import dpkt
import re
from datetime import datetime
from operator import itemgetter
import json
import os
import networkx as nx
import matplotlib.pyplot as plt
from networkx_graph_final import network_graph_func
from collections import Counter
from line_graph_final import line_graph_main
import sys


counter_list = [0, 0, 0, 0]
#TCP[0], UDP[1], IGMP[2], ICMP[3]
timestamps = [[], [], [], []]
#TCP[0], UDP[1], IGMP[2], ICMP[3]
packet_sizes = [[], [], [], []]
url_list = [[], [], [], []]
#URL[0], URI[1], Filename[2]
email_list = []
ip_list = []
ip_counter_list = [[], []]
ip_packet_list = [[], []]
to_ip_dict = {}
from_ip_dict = {}
ip_destination_list = []
src_and_dest_ip_count_dict = {}
src_and_dest_ip_count_list = []

def graph_drawer(ipsrcnipdst, output_path):
    iplist = []
    for t,y in ipsrcnipdst:
        iplist.append((t, y))

    g = nx.DiGraph()
    edgeList = iplist
    plt.figure(1, figsize=(10, 10))
    g.add_edges_from(edgeList)

    # pos = nx.spring_layout(g,scale=2) #default to scale=1
    pos = nx.spring_layout(g, k=2, iterations=30, weight=10)
    nx.draw(g, pos, with_labels=True)
    plt.savefig(output_path + '/graph.png')
    #plt.show()


def packet_dictionary_builder():
    """This function builds the dictionary of IP:Packet count"""
    global ip_packet_list, ip_counter_list
    for x in ip_counter_list[0]: ip_packet_list[0].append(socket.inet_ntoa(x))
    #For each value in the first index of IP_COUNTER_LIST, this contains the ToIP's, this adds the decoded IP address
    #To IP_PACKET_LIST list index 0.
    for x in ip_packet_list[0]:
        if x in to_ip_dict:
            pass
            # Checks if value is in the to_ip_dcit if it is don't add it again

        else:
            to_ip_dict[x] = ip_packet_list[0].count(x)
            #If value isn't in the dict add it and add the count of its packets to the dictionary as the value.
        if x in ip_list or x == '0.0.0.0' or x == '255.255.255.255':
            pass
        else:
            ip_list.append(x)

    for x in ip_counter_list[1]: ip_packet_list[1].append((socket.inet_ntoa(x)))
    # For each value in the first index of IP_COUNTER_LIST, this contains the FromIP's, this adds the decoded IP address
    # To IP_PACKET_LIST list index 1.
    for x in ip_packet_list[1]:
        if x in from_ip_dict:
            pass
            # Checks if value is in the to_ip_dcit if it is don't add it again
        else:
            from_ip_dict[x] = ip_packet_list[1].count(x)
            # If value isn't in the dict add it and add the count of its packets to the dictionary as the value.
        if x in ip_list or x == '0.0.0.0' or x == '255.255.255.255':
            pass
        else:
            ip_list.append(x)


def packet_counter(ipsrc, ipdst):
    """This functions purpose is to receive the IP.SRC and IP.DST IPs and add them to the IP_COUNTER_LIST global list."""
    ip_counter_list[0].append(ipsrc)
    ip_counter_list[1].append(ipdst)
    src_and_dest_ip_count_list.append(socket.inet_ntoa(ipsrc) + ':' + socket.inet_ntoa(ipdst))

def tcp_analyser(ts, buf, tcp):
    """This function handles any TCP packets found in the PCAP file."""
    global counter_list, url_list
    counter_list[0] += 1
    #This counts each TCP packet and increments the counter lsit.
    timestamps[0].append(ts)
    #This adds the timestamp to the timestamp list.
    packet_sizes[0].append(len(buf))
    #Adds the size of the packet to the packet size list.
    try:
        if (tcp.dport == 80 and len(tcp.data) > 0):
            # If the TCP port is 80 it will be HTTP traffic and is treadted accoridingly.
            http = dpkt.http.Request(tcp.data)
            # Pulls the HTTP request part of the packet.
            just_url = re.search(r'\w+\.com|\w+\.co\.uk|\w+\..*\.html', str(http))
            # Pulls the URL part out of the HTTP request.
            pictures_urls = re.search(r'\w+\.gif|\w+\.jpg|\w+\.png|\w+\.co\.uk.*\w+\.gif|\w+\.jpg|\w+\.png',
                                       str(http))
            # Looks for any picture URL's
            if pictures_urls and just_url:
                # Checks if there is any picture in the url
                url_list[0].append(just_url.group())
                # Puts the URL part of URL into url_list index 0
                url_list[1].append(http.uri)
                # Puts the URI part of URL into url_list index 1
                url_list[2].append(pictures_urls.group())
                # Puts the filename part of URL into url_list into index 2
                print(just_url.group() + http.uri + pictures_urls.group())

        else:
        # Checks if the traffic is email traffic.

            emails = re.search('[a-zA-Z0-9._+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', str(tcp.data))
            # Regex to find email addresses

            if emails:
                if emails.group() in email_list: pass
                # If the email is already in the email_list list, skip it.
                else: email_list.append(emails.group())
                # if not in list add to list.
    except dpkt.UnpackError:
        # Exception for handling unpack errors.
        pass

def udp_analyser(ts, buf):
    """Function handles UDP packets, counts, gets timestamp and packets length"""
    counter_list[1] += 1
    timestamps[1].append(ts)
    packet_sizes[1].append(len(buf))
def igmp_analyser(ts, buf):
    """Function handles IGMP packets, counts, gets timestamp and packets length"""
    counter_list[2] += 1
    timestamps[2].append(ts)
    packet_sizes[2].append(len(buf))
def icmp_analyser(ts, buf):
    """Function handles ICMP packets, counts, gets timestamp and packets length"""
    counter_list[3] += 1
    timestamps[3].append(ts)
    packet_sizes[3].append(len(buf))

def create_directories(filename):
    """Function creates directories"""
    path = os.getcwd() + '/' + filename
    if (os.path.isdir(path)):
        # Checks if the path is a valid directory
        os.chdir(path)
        for file in os.listdir(path):
            # Checks if the directory exists already
            if (file.startswith('.' or '..')):
                continue
                # If the file is a hidden file it isn't removed, this is required for Unix based systems.
            else:
                os.remove(path + '/' + file)
                # This removes any other files in directory
        #os.chdir("../")
    else:
        os.mkdir(path)
        os.chdir(path)
        # If the directory does not exist, it's created and moved into the directory.

def write_results_to_json():
    """Writes the output from processing to a .json file"""
    packet_dictionary_builder()
    # temp_list = [[], [], [], [], [], []]
    x = 0
    packet_types = ['TCP', 'UDP', 'IGMP', 'ICMP']

    while x < len(counter_list) - 1:
        if (counter_list[x] > 0):

            print(f"{packet_types[x]} Total Packets: {counter_list[x]} \n"
                  f"{packet_types[x]} First timestamp: {datetime.fromtimestamp(timestamps[x][0]).strftime('%H:%M:%S %d-%m-%Y')} \n"
                  f"{packet_types[x]} Last timestamp: {datetime.fromtimestamp(timestamps[x][-1]).strftime('%H:%M:%S %d-%m-%Y')} \n"
                  f"{packet_types[x]} Average packet size: {int(sum(packet_sizes[x]) / int(len(packet_sizes[x])))}\n")
            # This handles the counting, first and last timestamp, and average packet size, and adds them to the packet_dict.
        x += 1

    index = 0
    uri_and_filename_dict = {}
    for x in url_list[0]:
        uri_and_filename_dict[url_list[1][index]] = url_list[2][index]
        index += 1
        # This takes all URLs and filenames and adds them to a dictionary for readabilty.
    for x in email_list: print(f"Unique emails: {x}")
    for x in ip_list: print(f"Unique IP: {x}")

    data = [sorted(to_ip_dict.items(), key=itemgetter(1), reverse=True),
            sorted(from_ip_dict.items(), key=itemgetter(1), reverse=True)]
    # This adds the sorted dictionary of IP's and packets to/from it to data.

    output_file = 'data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, separators=(',', ':'))
        # This dumps all data to one .json file.
    return os.getcwd()+ '/' + output_file, os.getcwd()
    # Returns the .json file location


def main():

    print("Collecting data.")
    pcap_file = os.getcwd() + '/' + "evidence-packet-analysis.pcap"
    #pcap_file = sys.argv[1]
    filename = 'dpkt_output'
    create_directories(filename)
    # Creates a new directory to store all exported values.

    ip_list2 = []
    ip_list = []
    timestamp_list = []

    with open(pcap_file, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)
        for ts,buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            tcp = ip.data

            timestamp_list.append(ts)
            # Appends timestamps to timestamp list
            ip_list2.append(str(socket.inet_ntoa(ip.src)) + ',' + str(socket.inet_ntoa(ip.dst)))
            # Appends source and destination IP's to ip_list2
            if (socket.inet_ntoa(ip.src) == '0.0.0.0' or socket.inet_ntoa(ip.src) == '255.255.255.255'):
                if (socket.inet_ntoa(ip.dst) == '0.0.0.0' or socket.inet_ntoa(ip.dst) == '255.255.255.255'):
                    # If the source or destination IP == all 0's or all 255's, skip it.
                    pass
                else:
                    ip_list.append((socket.inet_ntoa(ip.src), socket.inet_ntoa(ip.dst)))
                    if socket.inet_ntoa(ip.dst) in ip_destination_list:
                        None
                    else:
                        ip_destination_list.append(socket.inet_ntoa(ip.dst))

            packet_counter(ip.src, ip.dst)
            if (type(ip.data) == dpkt.igmp.IGMP):
                igmp_analyser(ts, buf)
            if (type(ip.data) == dpkt.udp.UDP):
                udp_analyser(ts, buf)
            if (type(ip.data) == dpkt.tcp.TCP):
                tcp_analyser(ts, buf, tcp)
            if (type(ip.data) == dpkt.icmp.ICMP):
                icmp_analyser(ts, buf)
            else:
                pass

    ip_src_dest_count = Counter(src_and_dest_ip_count_list)
    network_graph_func(ip_src_dest_count)
    output_file, output_path = write_results_to_json()
    print(f"Complete please see {output_file} file for results.")
    #graph_drawer(iplist, output_path)
    line_graph_main(timestamp_list)


if __name__=="__main__":
    main()