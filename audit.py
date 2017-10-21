import xml.etree.ElementTree as ET
from tqdm import tqdm
from collections import defaultdict

tags = defaultdict(lambda: defaultdict(int))


i = 0
for event, elem in tqdm(ET.iterparse('mumbai_india.osm')):
    if elem.tag != 'way':
        continue

    for tag in elem.iter('tag'):
        tags[elem.tag][tag.attrib['k']] += 1

        i += 1

    if i > 1000:
        break

print(tags)
