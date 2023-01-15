import json
import re
import csv

FILE = 'dubai_data.json'
FILE_EXT = 'dubai_data_extended.json'


def extract_square_meters(string):

    # Use a regular expression to match the pattern of digits after "sqm"
    match = re.search(r"\d+sqm", string)

    if match:
        # Extract the digits
        digits = match.group(0).replace("sqm", "")
        return digits
    else:
        print("No match found")
        return -1


def clean_facts(facts):
    try:
        age = [item for item in facts if "Years" in item][0].replace(" Years", '')
    except:
        age = None
    bedrooms = facts[-2].replace('+Maid', '')
    if bedrooms == 'studio':
        bedrooms = 0
    return {"apartment type": facts[0], "size(sqm)": extract_square_meters(facts[1]), "bedrooms": bedrooms, "age": age}


def clean_data(file):
    with open(file, 'r') as f:
        # Load the JSON data
        data = json.load(f)
        cleaned_data = []
        for apartment in data:
            if 'url' in apartment.keys():
                if apartment['price'] != 'Ask' and apartment['price'] != '\n':
                    apartment['area'] = apartment['area'].strip()
                    cleaned_facts = clean_facts(apartment["facts"])
                    apartment.update(cleaned_facts)
                    apartment.pop('facts')
                    apartment.pop('input')
                    try:
                        apartment['price(USD/month)'] = float(apartment['price'].replace(",", "")) * 0.27 / 12
                        apartment.pop('price')
                    except:
                        print(apartment['price'])
                    try:
                        apartment['amenities'][0] = apartment['amenities'][0].replace(" ", "")
                    except:
                        pass
                    cleaned_data.append(apartment)
    return cleaned_data


def get_all_amenities(data):
    amenities = set()
    for item in data:
        for amenity in item['amenities']:
            if amenity == 'Unfurnished':
                continue
            amenities.add(amenity)
    return amenities


def clean_amenities(amenities, all_amenities):
    new_amenities = {}
    for amenity in all_amenities:
        new_amenities[amenity] = 1 if amenity in amenities else 0
    return new_amenities


def load_to_csv():
    cleaned_data = clean_data(FILE)
    cleaned_data_ext = clean_data(FILE_EXT)
    all_amenities = get_all_amenities(cleaned_data)
    for item in cleaned_data:
        item.update(clean_amenities(item['amenities'], all_amenities))
        item.pop('amenities')
    for item in cleaned_data_ext:
        item.update(clean_amenities(item['amenities'], all_amenities))
        item.pop('amenities')
    with open('dubai_data.csv', 'w') as csv_file:
        # Create a CSV writer
        writer = csv.writer(csv_file)

        # Add the header row
        keys = list(cleaned_data[0].keys())
        print(list(keys))
        writer.writerow(keys)

        # Add the data rows
        for row in cleaned_data:
            writer.writerow(row.values())
        for row in cleaned_data_ext:
            writer.writerow(row.values())


# load_to_csv()

cleaned_data_ext = clean_data(FILE_EXT)
print(get_all_amenities(cleaned_data_ext))