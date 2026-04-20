# NSI NMEA Extended

A Python library for parsing, validating, and managing NMEA (GPS) data sentences, datasets and files.

## Features

- **NMEA Parsing**: Extract and standardize data from NMEA sentences.
- **Validation**: Checks for checksum integrity and GPS data quality.
- **Conversion**: Automatically converts latitude and longitude from NMEA format to decimal degrees for simpler usage.
- **Dataset Management**: Load multiple sentences from files (.nmea, .txt, .nmeasz), iterate over them, and export them.
- **Metadata Extraction**: Easily get framing (bounding box) and lists of coordinates from datasets.

## Installation

```bash
pip install git+https://github.com/amine-adjimi/nsi-nmea-extended.git
```

## Supported Sentences

### GGA (Global Positioning System Fix Data)
Extracts:
- Latitude and Longitude
- Time (HH:NN:SS) (NN stands for minutes)
- Altitude (Meters)
- Validation: Requires GPS Quality (1-5), at least 4 satellites, and HDOP ≤ 10.0.

### RMC (Recommended Minimum Specific GNSS Data)
Extracts:
- Latitude and Longitude
- Date (DD,MM,YY) and time (HH,NN,SS) (NN stands for minutes)
- Speed (km/h)
- Track Angle (Degrees)
- Validation: Requires sentence to be marked as valid ('A') by the satellite and checks FAA modes for newer versions.

## Usage

### Parsing a single sentence

```python
from nsi_nmea_extended import NmeaSentence

# Example GGA sentence
raw_gga = "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47"
sentence = NmeaSentence(raw_gga)

# Accessing data
print(f"Latitude: {sentence['LATD']}")
print(f"Longitude: {sentence['LOND']}")
print(f"Altitude: {sentence['ALTM']}m")
print(f"Time: {sentence['DATE']['HH']}:{sentence['DATE']['NN']}:{sentence['DATE']['SS']}")

# Get coordinates in different formats
print(sentence.coordinates(tuple)) # (48.1173, 11.516666666666667)
print(sentence.coordinates(dict))  # {'LATD': 48.1173, 'LOND': 11.516666666666667}
```

### Managing a dataset

```python
from nsi_nmea_extended import NmeaDataset

# Load sentences from a file
dataset = NmeaDataset('path/to/your/data.nmea', datatype='file')

# Dataset properties
print(f"Number of sentences: {len(dataset)}")

# Get all coordinates
coords = dataset.coordinates(tuple) # Will return a list of tuples

# Get bounding box (Min/Max coordinates)
framing = dataset.framing()
print(f"Max Latitude: {framing['MAX']['LATD']}")
print(f"Min Longitude: {framing['MIN']['LOND']}")

# Export to .nmeasz format (serialized Python representation)
dataset.export('output_file')
```

## Data Structure

Standardized keys used in the output dictionary:
- `LATD`: Latitude in decimal degrees (float)
- `LOND`: Longitude in decimal degrees (float)
- `ALTM`: Altitude in meters (float)
- `SPEE`: Speed in km/h (float)
- `ANGL`: Listener movement angle from North [0°;360°[ (float)
- `DATE`: Date
  - `YYYY`: Year (int)
  - `YY`: Year (last two digits, int)
  - `MM`: Month (int)
  - `DD`: Day (int)
  - `HH`: Hour (UTC, int)
  - `NN`: Minute (int)
  - `SS`: Second (float)
- `VLDT`: Internal validity flag (bool)

## License

This project is licensed under the GNU GPL v3 License.