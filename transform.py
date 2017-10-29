import re


def standardize_suffixes(street_name):
    mapping = {
        'rd.': 'Road',
        'rd': 'Road',
        'raod': 'Road',
        'road.': 'Road',
        'marg': 'Road',
        'mg.': 'Road',
        'mg': 'Road',
        'gali': 'galli',
        'gully': 'galli',
        'stn': 'station',
        'sec': 'Sector',
        'chauk': 'Chowk',
        'st': 'Street',
        'bunglow': 'Bungalow',
        'J.v.link.rod': 'J.V Link Road'
    }
    
    for k, v in mapping.iteritems():
        street_name = re.sub(r'\b' + re.escape(k) + r'\b', v, street_name, flags=re.I)

    return street_name


# Convert no.4, no. 5, no 6 etc. to No. 4, No. 5, and No. 6
# at the end of the string
numeric_suffixes_regex = re.compile(r'(no|number)\.?\s?(?P<digit>\d+)$', flags=re.I)
def standardize_numeric_suffixes(street_name):
    return numeric_suffixes_regex.sub("No. \g<digit>", street_name)


def extract_street_segment(street_name, default_first_segment=False):
    splits = street_name.split(',')
    
    # The order here is important
    search_words = ['road', 'lane', 'street', 'avenue', 'plot', 'sector', '-sector',
                    'nagar', 'area', 'bungalow', 'bungalows', 'mahal', 'estate', 'wadi',
                    'circle', 'centre', 'towers', 'garden', 'village', 'society',
                    'multiplex']
    for search_word in search_words:
        for split in splits:
            if search_word in split.lower():
                return split.strip()

    if default_first_segment:
        return street_name.split(',')[0].strip()
    else:
        # Just return the street name if we don't get a valid
        # transformation
        # This is useful during the wrangling phase
        return street_name

def transform_street_name(street_name):
    std_street_name = standardize_suffixes(street_name)

    # Default_first_segment should be False for most of the wrangling phase
    # Once we're down to a handful street names with commas, and only intend to
    # get the first segment as a fallback, we should pass True
    segment_street_name = extract_street_segment(std_street_name, default_first_segment=True)
    num_street_name = standardize_numeric_suffixes(segment_street_name)
    
    return num_street_name
