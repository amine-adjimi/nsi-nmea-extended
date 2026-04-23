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
#### Extracted data
- Latitude and Longitude
- Time (HH:NN:SS) (NN stands for minutes)
- Altitude (Meters)
- Validation: Requires GPS Quality (1-5), at least 4 satellites, and HDOP ≤ 10.0.

#### Sentence schema

This is one of the sentences commonly emitted by GPS units.

Time, Position and fix related data for a GPS receiver.

```text
                                                      11
        1         2       3 4        5 6 7  8   9  10 |  12 13  14   15
        |         |       | |        | | |  |   |   | |   | |   |    |
 $--GGA,hhmmss.ss,ddmm.mm,a,ddmm.mm,a,x,xx,x.x,x.x,M,x.x,M,x.x,xxxx*hh<CR><LF>
```

Field Number:
1. UTC of this position report, hh is hours, mm is minutes, ss.ss is seconds.
2. Latitude, dd is degrees, mm.mm is minutes
3. N or S (North or South)
4. Longitude, dd is degrees, mm.mm is minutes
5. E or W (East or West)
6. GPS Quality Indicator (non null)
```text
0 - fix not available,
1 - GPS fix,
2 - Differential GPS fix (values above 2 are 2.3 features)
3 = PPS fix
4 = Real Time Kinematic
5 = Float RTK
6 = estimated (dead reckoning)
7 = Manual input mode
8 = Simulation mode
```
7. Number of satellites in use, 00 - 12
8. Horizontal Dilution of precision (meters)
9. Antenna Altitude above/below mean-sea-level (geoid) (in meters)
10. Units of antenna altitude, meters
11. Geoidal separation, the difference between the WGS-84 earth ellipsoid and mean-sea-level (geoid), "-" means mean-sea-level below ellipsoid
12. Units of geoidal separation, meters
13. Age of differential GPS data, time in seconds since last SC104 type 1 or 9 update, null field when DGPS is not used
14. Differential reference station ID, 0000-1023
15. Checksum

The number of digits past the decimal point for Time, Latitude and Longitude is model dependent.

Example:
`$GNGGA,001043.00,4404.14036,N,12118.85961,W,1,12,0.98,1113.0,M,-21.3,M*47`

### RMC (Recommended Minimum Specific GNSS Data)
#### Extracted data
- Latitude and Longitude
- Date (DD,MM,YY) and time (HH,NN,SS) (NN stands for minutes)
- Speed (km/h)
- Track Angle (Degrees)
- Validation: Requires sentence to be marked as valid ('A') by the satellite and checks FAA modes for newer versions.

#### Sentence schema

This is one of the sentences commonly emitted by GPS units.

```text
        1         2 3       4 5        6  7   8   9    10 11
        |         | |       | |        |  |   |   |    |  |
 $--RMC,hhmmss.ss,A,ddmm.mm,a,dddmm.mm,a,x.x,x.x,xxxx,x.x,a*hh<CR><LF>
NMEA 2.3:
 $--RMC,hhmmss.ss,A,ddmm.mm,a,dddmm.mm,a,x.x,x.x,xxxx,x.x,a,m*hh<CR><LF>
NMEA 4.1:
 $--RMC,hhmmss.ss,A,ddmm.mm,a,dddmm.mm,a,x.x,x.x,xxxx,x.x,a,m,s*hh<CR><LF>
```

Field Number:
1. UTC of position fix, `hh` is hours, `mm` is minutes, `ss.ss` is seconds.
2. Status, `A` = Valid, `V` = Warning
3. Latitude, `dd` is degrees. `mm.mm` is minutes.
4. `N` or `S`
5. Longitude, `ddd` is degrees. `mm.mm` is minutes.
6. `E` or `W`
7. Speed over ground, knots
8. Track made good, degrees true
9. Date, `ddmmyy`
10. Magnetic Variation, degrees
11. `E` or `W`
12. FAA mode indicator (NMEA 2.3 and later)
13. Nav Status (NMEA 4.1 and later) `A`=autonomous, `D`=differential, `E`=Estimated, `M`=Manual input mode `N`=not valid, `S`=Simulator, `V` = Valid
14. Checksum

A status of V means the GPS has a valid fix that is below an internal quality threshold, e.g. because the dilution of precision is too high or an elevation mask test failed.
The number of digits past the decimal point for Time, Latitude and Longitude is model dependent.

Example: `$GNRMC,001031.00,A,4404.13993,N,12118.86023,W,0.146,,100117,,,A*7B`

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