from ..check import check_value

def parse(s):
    check_value(s[2], 'A')  # Checks if the sentence has marked as valid

    version = 0

    match len(s):  # Deduces the sentence's version (and checks the validity of sentence's length btw)
        case 12:
            version = 0
        case 13:
            version = 2.3
        case 14:
            version = 4.1
        case _:
            raise IndexError(f"RMC SS version not covered or schema non-existent (sentence length : {s}).")

    if version >= 2.3:
        check_value(s[12], ('A', 'D', 'R', 'P', 'F'))  # Only accepts precise FAA modes
    if version >= 4.1:
        check_value(s[13], ('A', 'D', 'V'))  # Only accepts precise Nav Statutes

    # For RMCF, we don't check for fixed length of 4 or 5 before the dot
    # We just ensure it's a valid coordinate format (at least 3 digits for lat, 4 for lon if we want to be strict,
    # but the issue description says "0 are removed", so we'll be flexible)
    
    lat_str = s[3]
    lon_str = s[5]
    
    # Standard RMC is DDMM.MMMM (4 digits before .)
    # Standard RMC is DDDMM.MMMM (5 digits before .)
    
    # We need to find the split point between degrees and minutes.
    # In RMC, minutes are always the last 2 digits before the decimal point plus the decimal part.
    
    lat_dot_idx = lat_str.find('.')
    if lat_dot_idx == -1:
        lat_before_dot = lat_str
    else:
        lat_before_dot = lat_str[:lat_dot_idx]
        
    lon_dot_idx = lon_str.find('.')
    if lon_dot_idx == -1:
        lon_before_dot = lon_str
    else:
        lon_before_dot = lon_str[:lon_dot_idx]

    if len(lat_before_dot) < 2:
         raise ValueError(f"Invalid latitude format for RMCF (given value : {s[3]}).")
    if len(lon_before_dot) < 2:
         raise ValueError(f"Invalid longitude format for RMCF (given value : {s[5]}).")

    # minutes are always the last 2 digits before the dot
    lat_mins = float(lat_str[len(lat_before_dot)-2:])
    lat_degs = float(lat_str[:len(lat_before_dot)-2]) if len(lat_before_dot) > 2 else 0.0
    
    lon_mins = float(lon_str[len(lon_before_dot)-2:])
    lon_degs = float(lon_str[:len(lon_before_dot)-2]) if len(lon_before_dot) > 2 else 0.0

    # Parses the sentence's data and puts it in the dict
    dc = {
        'LATD': (lat_degs + (lat_mins / 60)) * ((-1) if s[4] == "S" else 1 if s[4] == "N" else 0),
        'LOND': (lon_degs + (lon_mins / 60)) * ((-1) if s[6] == "W" else 1 if s[6] == "E" else 0),
        'DATE': {
            'YY': int(s[9][4:6]),
            'MM': int(s[9][2:4]),
            'DD': int(s[9][0:2]),
            'HH': int(s[1][0:2]),
            'NN': int(s[1][2:4]),
            'SS': float(s[1][4:])
        },
        'SPEE': float(s[7]) * 1.852,
        'ANGL': float(s[8])
    }

    return dc
