# OpenStreetMap Data Wrangling - Mumbai, India

## The general process

The general process was for me to experiment with the data in Jupyter Notebooks, and then consolidate the results in a proper set of python files.

## Cleaning data

I decided to clean the `addr:street` field. This field is supposed to contain the street name.

### Process used for cleaning data

I used the following process to clean the `addr:street` field.

**1. Establish assumptions about data**

First, I eyeballed random data and made a conscious assumption about the pattern that they follow. This started with assuming that the streets end with specific suffixes.

Refer `2. Define structure for street names` in `Transform Street Names.ipynb`.

**2. Transform street names**

I then printed out all the street names that didn't match my expected pattern. This allowed me to observe newer patterns and potential opportunities for standardization. Standardization involved turning "Rd." to "Road", etc.

Refer `3. Transform street names` in `Transform Street Names.ipynb`.

**3. Validate transformations**

After the initial set of transformations, the validations were run again against all the street names. This reduced their number each time I validated a certain pattern. This was incorporated in STEP 1 in form of a validating function.

Refer `4. Check transformations` in `Transform Street Names.ipynb`.

## Problems encountered

### Suffixes not standardized

The main problem was having "Road" represented as "rd", "rd.", "raod", "road.", "marg", etc. A few of them are abbreviations, one is a misspelling. "Marg" stands for "Road" in local tongue, so can be standardized.

### Road numbers not standardized

A lot of roads have a name and a corresponding number. This is the reason the word "road" does not necessarily appear as a suffix. For example, look at this example from the dataset:

|Before|After|
|------|-----|
|D.P. road No. 2|D.P. road No. 2|
|D.P. road No.2|D.P. road No. 2|
|D.P. road no2|D.P. road No. 2|
|D.P. road number 2|D.P. road No. 2|

### Full addresses instead of street names

In a lot of cases, we have full addresses instead of just the street name, delimited by commas. So, I had to split the address on commas and find out which one represented a street name the best. This was done in the same way as validating street names. The "segment" that matched a street name well was chosen.

|Before|After|
|------|-----|
|Gokhale Road North, Amarhind Mandal|Gokhale Road North|
|Additional Kalyan Bhiwandi MIDC Industrial Area, Plot No. 1, Village Kone,|Plot No. 1|
|9 A nerul, Uran Road, Sector 19A, Nerul, Navi Mumbai,|Uran Road|
|Erangal Beach, Madh Island, Marve Road, Malad East,|Marve Road|
|5th Floor, Chakala Pragati CHS, J B Nagar, Andheri East|J B Nagar|
|Vengaon Road,Dahivali, Karjat, Dist Raigad ,Raigad|Vengaon Road|
|, Rizvi Park, S V Road, Santacruz West|S V Road|

## Verifying solutions to problems encountered

In the codebase, if a specific transformation (like standardizing suffix, standardizing numeric suffix, extraction street segments) is applied to a street name, then the original and the transformed street name is indexed. This allowed me to quickly check the transformations to see if they are doing something that they're not supposed to.

## Overview of the data

### File sizes:

1. mumbai_india.osm: 409M
1. nodes.csv: 163M
1. nodes_tags.csv: 2.1M
1. ways.csv: 17M
1. ways_nodes.csv: 54M
1. ways_tags.csv: 10M
1. Total MySQL db size: 366MB

### No. of nodes:

```sql
select count(*) from nodes;
```

2055448

### No. of ways:

```sql
select count(*) from ways;
```

284435

### No. of unique users

```sql
select count(distinct(combined.uid)) from
    (select uid from nodes union all select uid from ways) combined;
```

1781

### No. of distinct node_tag types with counts

```sql
select `type`, count(*) c from nodes_tags group by `type` order by c desc;
```

```
Type            Count
regular         56359
addr            3961
name            1510
brand           186
seamark         57
building        50
fuel            31
shop            20
toilets         15
diet            13
service         11
currency        8
payment         8
tower           6
crossing        5
internet_access 5
gns             4
contact         4
motorcycle      3
fire_hydrant    3
old_name        2
public_transport 2
is_in           1
place           1
population      1
disused         1
historic        1
communication   1
social_facility 1
IR              1
health_facility 1
note            1
source          1
```

### Keys that appear in nodes_tags

```sql
select `key`, count(*) c from nodes_tags group by `key` order by c desc;
```

```
Key        Count
source     18416
power      8970
name       6336
created_by 4497
amenity    3130
natural    2645
highway    1496
street     1308
en         1286
postcode   1065
place      1052
operator   930
shop       796
city       746
... (truncated)
```

### Types of amenities

```sql
select `value`, count(*) c from nodes_tags where `key` = 'amenity' group by `value` order by c desc;
```

```
Type of amenity   Count
restaurant        430
place_of_worship  362
bank              329
cafe              148
school            143
atm               143
hospital          142
toilets           136
fast_food         131
police            124
fuel              117
waste_basket      115
bus_station       89
pharmacy          74
bench             65
parking           56
cinema            45
clinic            42
```

### Top 10 nodes with a name and ordered by the no. of ways associated with them

```sql
select tbl.nid, nodes_tags.value, tbl.c from (select nodes.id nid, count(*) c from nodes
    left join ways_nodes on nodes.id = ways_nodes.node_id
    group by nodes.id) tbl
    inner join nodes_tags on tbl.nid = nodes_tags.id and nodes_tags.key = 'name'
    order by tbl.c desc limit 10;
```

```
Node id     Node name                   No. of ways
631537705   Ram Ganesh Gadkari Chowk    5
2178293603  Nana Chowk                  5
2236680951  bombay bakery               5
2236680954  Govind Nagar                5
245660578   Albela Hanuman Mandir Chowk 4
245661918   Raja Badhe Chowk            4
245670700   Saki Naka                   4
317914112   Dr. Ambedkar Chauk          4
870449150   Gateway of India - Mandwa Rewas Ferry Terminal  4
1366900900  Amrut Nagar Circle          4
```

### No. of nodes without a name

```sql
select count(*) from nodes
    left join nodes_tags on nodes_tags.id = nodes.id and nodes_tags.key = 'name'
    where nodes_tags.key is null;
```

2049113

## Additional ideas for improvements

Nodes are supposed to have names. However, for `2049113` nodes, the "name" tag is missing. It becomes difficult to work with such data because we can't readily give a human-readable name to them. Data collection has to be improved so that the nodes have identifiable names. All the other parameters can be considered optional and can be handled accordingly, but name is mandatory.

The major problem could be in how data is collected. People should be able to "vote" on standardized names for "keys" in nodes and ways. This way, we can ensure that values for the "name" field are collected, and is not accidentally entered in some new field that got created by the user making the update.
