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

    if len(s[3].split('.')[0] != 4):
        raise ValueError(f"Invalid latitude format (correct format : ddmm.mm ; given value : {s[3]}).")
    if len(s[5].split('.')[0] != 5):
        raise ValueError(f"Invalid longitude format (correct format : dddmm.mm ; given value : {s[5]}).")

    # Parses the sentence's data and puts it in the dict
    dc = {
        'LATD': (float(s[3][:2]) + (float(s[3][2:]) / 60)) * ((-1) if s[4] == "S" else 1 if s[4] == "N" else 0),
        'LOND': (float(s[5][:3]) + (float(s[5][3:]) / 60)) * ((-1) if s[6] == "W" else 1 if s[6] == "E" else 0),
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