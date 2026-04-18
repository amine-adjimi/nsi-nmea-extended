from ..check import check_value

def parse(s):
    check_value(int(s[6]), (1, 2, 3, 4, 5)) # Only accepts precise GPS Quality
    if int(s[7]) < 4:
        raise ValueError(f"Not enough satellites in use to consider the position as precise ({int(s[7])} satellites in use).") # Rejects the sentence when there isn't enough satellites in use to consider the position as precise
    if float(s[8]) > 10:
        raise ValueError(f"HDOP too high (>10.0). HDOP : {s[8]}", ) # Rejects the sentence when the horizontal dilution of the measure is too high
    check_value(s[10], 'M') # Checks if there isn't any anomaly in the antenna altitude measure unit

    # Parses the sentence's data and puts it in the dict
    dc = {
        'LATD': (float(s[2][:2]) + (float(s[2][2:]) / 60)) * ((-1) if s[3] == "S" else 1 if s[3] == "N" else 0),
        'LOND': (float(s[4][:3]) + (float(s[4][3:]) / 60)) * ((-1) if s[5] == "W" else 1 if s[5] == "E" else 0),
        'DATE': {
            'HH': int(s[1][0:2]),
            'NN': int(s[1][2:4]),
            'SS': float(s[1][4:])
        },
        'ALTM': float(s[9])
    }

    return dc