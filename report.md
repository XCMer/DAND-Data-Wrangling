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




