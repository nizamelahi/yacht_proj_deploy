import json

with open("data/listing_data.json", "rb") as f:
    data_listings = json.load(f)


def lower(item):
    if item != None:
        item.lower()
    else:
        item = ""
    return item


def extract_engine_data(pwr):
    engines = []
    for key in pwr:
        en_make = pwr[key].get("Engine_Make")
        en_model = pwr[key].get("Engine_Model")
        en_fuel = pwr[key].get("Fuel_Type")
        en_pwr = pwr[key].get("Total_Power")
        en_type = pwr[key].get("Engine_Type")
        en_fuel = lower(en_fuel)
        en_pwr = lower(en_pwr)
        en_type = lower(en_type)
        en_model = lower(en_model)
        en_make = lower(en_make)

        if en_model:
            en_str = f"{en_type} {en_make} {en_model} {en_fuel} {en_pwr}"
            if en_str.replace(' ','') not in [x.replace(' ','') for x in engines]:
                engines.append(en_str.strip())
    return engines


def add_to_cleaned(cleaned_data, listing_key, key):
    if listing_key[key].lower() not in cleaned_data.get(key):
        cleaned_data[key].append(listing_key[key].lower())


cleaned_data = {}
for i in data_listings:
    if i["basics"].get("Year") and i["basics"].get("Make") and i["basics"].get("Model"):
        entry = f'{i["basics"]["Year"].lower()} {i["basics"]["Make"].lower()} {i["basics"]["Model"].lower()}'

        if not cleaned_data.get(entry):
            cleaned_data[entry] = {
                "Length": [i["basics"]["Length"].lower()],
                "Hull_Material": [i["basics"]["Hull_Material"].lower()],
                "Class": [i["basics"]["Class"].lower()],
            }
            pwr = i["propulsion"]
            en_data = extract_engine_data(pwr)
            if len(en_data) != 0:
                cleaned_data[entry]["engine_types"] = en_data
                cleaned_data[entry]["num_of_engines"] = [f"{len(pwr)}"]

            specs = i["specifications"]
            for key in specs:
                if specs[key] not in ["", "()"]:
                    cleaned_data[entry][key] = [specs[key].lower()]

        else:
            add_to_cleaned(cleaned_data[entry], i["basics"], "Length")
            add_to_cleaned(cleaned_data[entry], i["basics"], "Hull_Material")
            add_to_cleaned(cleaned_data[entry], i["basics"], "Class")

            specs = i["specifications"]
            for key in specs:
                if specs[key] not in ["", "()"]:
                    if cleaned_data.get(key):
                        if specs[key].lower() not in cleaned_data[entry][key]:
                            cleaned_data[entry][key].append(specs[key].lower())
                    else:
                        cleaned_data[entry][key] = [specs[key].lower()]

            pwr = i["propulsion"]
            if len(pwr) != 0:
                engine_data = extract_engine_data(pwr)
                for item in engine_data:
                    if cleaned_data[entry].get("engine_types"):
                        if item.replace(' ','') not in [x.replace(' ','') for x in cleaned_data[entry]["engine_types"]]:
                            cleaned_data[entry]["engine_types"].append(item)
                    else:
                        cleaned_data[entry]["engine_types"] = [item]

                if cleaned_data[entry].get("num_of_engines"):
                    if f"{len(pwr)}" not in cleaned_data[entry]["num_of_engines"]:
                        cleaned_data[entry]["num_of_engines"].append(f"{len(pwr)}")
                else:
                    cleaned_data[entry]["num_of_engines"] = [f"{len(pwr)}"]

print(len(cleaned_data))
with open("data/listings_cleaned.json", "w") as w:
    json.dump(cleaned_data, w)
