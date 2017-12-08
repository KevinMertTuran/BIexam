import bs4
import requests
import csv
import os
import re
from tqdm import tqdm
#Not Working yet TOO MUCH TIME SPEND!!!!
def scrape(url):

    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.content.decode('utf-8'), "html5lib")

    table = soup.find('table')
    table_body = table.find('tbody')

    a_tags = table_body.find_all('a')
    del a_tags[:5]

    a_tags = [a.text for a in a_tags]

    return a_tags


# Scrapes all data single paged
def scrape_event_data(url):

    data =[int(x) for x in input().split(",")]
    max = min = data[0]

    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.content.decode('utf-8'), 'html5lib')

    table = soup.find('table')
    table_body = table.find('tbody')

    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')

        # Decode event address column
        a_tags = cols[0].find_all('a')
        line = re.sub(r'<br/>', '\n', str(a_tags[0]))
        _, line, _ = line.split('>')
        line, _ = line.split('<')
        # Split the two values
        street, town= line.split('\n')
        # Split the two values
        Where = town.split(' ', 1)
        str(Where)

        # Decode event prices
        How_Much_it_cost = cols[4].text.strip()
        # Exception handling
        try:
            How_Much = int(How_Much_it_cost)
        except:
            How_Much = None

        # Decode Band
        What_str = cols[6].text.strip()
        # Exception handling
        try:
            What = str(What_str)
        except:
            What = None

        #event date
        When_str = cols[2].text.strip()
        When = When_str[:10]

        decoded_row = (What, Where, When, How_Much)
        data.append(decoded_row)

    return data


def save_data(base_url, urls):
    response = []
    for url in urls:
        u = os.path.join(base_url, url)
        response += scrape_event_data(u)
    save_to_file = os.path.join(out_dir, os.path.basename(url).split('_')[0] + '.csv')
    save_to_csv(response, save_to_file)




# Saving scraped data into CSV
def save_to_csv(data, path='scraped_events.csv'):

    with open(path, 'w', encoding='utf-8') as output_file:
        output_writer = csv.writer(output_file)
        output_writer.writerow(['What', 'Where', 'When',
                                'How_Much'])

        for row in data:
            output_writer.writerow(row)

def run():

    base_url = 'http://46.101.108.154/page_0.html'
    urls = scrape(base_url)
    temp_list = []
    count = 0
   #Progress
    for i in tqdm(urls, desc='saving'):
        _, number = i.split('_')
        number, _ = number.split('.')
        num = int(number)
        temp_val = count + 1
        if num == temp_val:
            temp_list.append(i)
            count += 1
        else:
            save_data(base_url, temp_list)
            temp_list = []
            count = 1
            temp_list.append(i)

    save_data(base_url, temp_list)


out_dir = './data/out'
if not os.path.exists(out_dir):
    os.mkdir(out_dir)
run()            