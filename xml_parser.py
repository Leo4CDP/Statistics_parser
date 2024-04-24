import csv
from lxml import etree

# Function to extract the necessary information from the XML file
def extract_data(file_path):
    tree = etree.parse(file_path)
    root = tree.getroot()

    analysed_xml_filename = file_path.split('/')[-1]
    extracted = root.find(".//m:Extracted", namespaces=root.nsmap).text
    structure_ref = root.find(".//m:Structure", namespaces=root.nsmap).get("structureID")


    version_data = [analysed_xml_filename, extracted, structure_ref]

    data_rows = []
    for series in root.findall(".//Series", namespaces=root.nsmap):
        freq = series.get("freq")
        geo = series.get("geo")
        hhtyp = series.get("hhtyp")
        indic_is = series.get("indic_is")
        unit = series.get("unit")

        for obs in series.findall("Obs", namespaces=root.nsmap):
            time_period = obs.get("TIME_PERIOD")
            obs_value = obs.get("OBS_VALUE")

            data_rows.append([freq, geo, hhtyp, indic_is, unit, time_period, obs_value])

    return version_data, data_rows

# Function to save the data to CSV files
def save_to_csv(file_path, version_data, data_rows):
    with open(f"{file_path}_version.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["analysed_xml_filename", "extracted", "structure_ref"])
        writer.writerow(version_data)

    with open(f"{file_path}_output.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["freq", "geo", "hhtyp", "indic_is", "unit", "time_period", "obs_value"])
        writer.writerows(data_rows)

# Sript
file_path = "download/"
version_data, data_rows = extract_data(file_path)
save_to_csv(file_path, version_data, data_rows)
