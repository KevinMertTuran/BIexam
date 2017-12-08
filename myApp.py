import csv
import os
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import math
import dateparser


scraped_events = pd.read_csv('scraped_events.csv')


def get_start_time(date_str):

    date_str = date_str.strip().strip('.')
    if '&' in date_str:
        date_str = date_str.split('&')[0]
    if '-' in date_str:
        date_str = date_str.split('-')[0].strip()
    if '.' in date_str:
        date_str = date_str.replace('.', ':')
    if date_str.startswith('Tues'):
        date_str = date_str.replace('Tues', 'Tue')
    if date_str.startswith('Thur'):
        date_str = date_str.replace('Thur', 'Thu')
    
    date = parse(date_str)
    return date


def start_time_to_float(b):
    try:
        return float("{}{:02d}".format(b.hour, b.minute))
    except:
        return math.nan


def get_price(price_str):
    price_regexp = r"(?P<price>/d+)"

    if 'Free admissions' in price_str:
        price = 0
    elif 'ratis' in price_str:
        price = 0
    else:
        m = re.search(price_regexp, price_str)
        try:
            price = int(m.group('price'))
        except:
            price = None

        return price

def decode_node_to_csv():
    # Dictionary with geo-locations of each address to use as strings
    for entry in parse_file('locs2.json'):
        if (isinstance(entry, Node) and 
            'addr:street' in entry.tags and 
            'addr:city' in entry.tags and 
            'addr:housenumber' in entry.tags):

            yield entry


def add_geolocations(decoded_node):
    
    progress_bar = tqdm()
    for file in os.listdir('scraped_events.csv'):
        for idx, decoded_node in enumerate(decode_node_to_csv()):
            try:                
                full_address = decoded_node.tags['addr:street'] + " " + decoded_node.tags['addr:housenumber'] + " " + decoded_node.tags['addr:postcode'] + " " + decoded_node.tags['addr:city']
                addr_with_geo = (decoded_node.locs2.longitude,decoded_node.locs2.latitude)
                
                with open('decoded_nodes.csv', 'a', encoding='utf-8') as f:
                    output_writer = csv.writer(f)
                    output_writer.writerow(addr_with_geo)
                
                progress_bar.update()

            except (KeyError, ValueError):
                pass




def scatter_plot_from_dataframe(dataframe):
    plot = dataframe.plot(kind='scatter', x='lon', y='lat')
    plot.get_figure().savefig('scatterplotImage.png')


def generate_scatter_plot(datetime_dataframe):
    scatter_plot_from_dataframe(datetime_dataframe)
      


def run():
    #add_geolocations(decode_node_to_csv())
    #Write DataFrame to csv
    #to_csv(path)
    datetime_dataframe = pd.read_csv('scraped_events.csv')
    generate_scatter_plot(datetime_dataframe)
    #generate_scatter_plot(datetime_dataframe)
    run()