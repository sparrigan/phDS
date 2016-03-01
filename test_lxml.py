from lxml import html
import requests

page = requests.get('http://www.indeed.com/viewjob?jk=c4848781fb5e0c73&qd=Q-9_DEivXuuvrIPGk6CzKjyvqzK5Hi6-yLCxDZTcfJc6J0xz_ZriJujSdXbfmH7cc9ajfFcDz9ck9lNpxl2RVTXlJOqjNW2rTxIszurrR83qhzefMEr7vs1aw5eF4c4w&indpubnum=9774998588751407&atk=19tgemjoibqid8kf')
tree = html.fromstring(page.text)

job_info = tree.xpath('//span[@class="summary"]/text()')

job_info_list = tree.xpath('//span[@class="summary"]/ul//li/text()')

print job_info

print ''

print job_info_list

