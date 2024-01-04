import xml.etree.ElementTree as ET

def calculate_elevation(tcx_file_path, elevation_per_km):
    # Load tcx file
    tree = ET.parse(tcx_file_path)
    root = tree.getroot()

    # Find all "Lap" elements
    lap_elements = root.findall(".//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Lap")

    elevation_gain_per_lap = 0

    for lap in lap_elements:
        # Check distance for particular "Lap"
        distance_element = lap.find(".//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}DistanceMeters")
        if distance_element is not None:
            distance = float(distance_element.text)
            if distance > 200:
                # Found all "Trackpoint" elements in a current "Lap"
                trackpoint_elements = lap.findall(".//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Trackpoint")
                
                elevation_per_lap = elevation_per_km * (distance / 1000)
                elevation_per_point = elevation_per_lap / len(trackpoint_elements)

                for trackpoint in trackpoint_elements:
                    # Found or add filed "AltitudeMeters" for particular point
                    altitude_element = trackpoint.find(".//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}AltitudeMeters")
                    if altitude_element is None:
                        altitude_element = ET.SubElement(trackpoint, "{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}AltitudeMeters")

                    elevation_gain_per_lap += elevation_per_point
                    altitude_element.text = str(elevation_gain_per_lap)
            else:
                # Found all "Trackpoint" elements in a current "Lap"
                trackpoint_elements = lap.findall(".//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Trackpoint")
                for trackpoint in trackpoint_elements:
                    # Found or add filed "AltitudeMeters" for particular point
                    altitude_element = trackpoint.find(".//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}AltitudeMeters")
                    if altitude_element is None:
                        altitude_element = ET.SubElement(trackpoint, "{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}AltitudeMeters")

                    altitude_element.text = str(elevation_gain_per_lap)

    # Save changed file in tcx
    tree.write(tcx_file_path)

# Example usage
tcx_file_path = 'file_with_activity.tcx'
elevation_per_km = 67 # in meters

calculate_elevation(tcx_file_path, elevation_per_km)
