from check import check_nmea_sum, check_type
from parse import gga, rmc

class NmeaSentence:
    """
    A parser for NMEA sentences. Extracts, validates, and standardizes GPS data (NMEA sentences) into a dictionary format (see https://docs.google.com/document/d/1_Ciie3Mi22pj19iQkCL2BRS0iGqD6XTnKa7XMGRJgXI/edit?usp=sharing)

    :param raw_sentence: The raw NMEA sentence to be parsed
    :type raw_sentence: str | list | dict
    :ivar sentence: The standardized NMEA sentence
    :type sentence: dict
    """

    def __init__(self, raw_sentence):

        def parse(raw):
            """
            Internal parser for extracting and validating data from supported NMEA sentences schemes (e.g., GGA, RMC) then standardizing it into a dictionary with documented keys.

            :param raw: The raw NMEA sentence to be parsed
            :type raw: str
            :rtype: dict
            """

            check_type(raw, str) # Checks if the raw sentence is str
            check_nmea_sum(raw) # Checksum
            raw = raw.split('*')[0].split(',') # Removes the checksum part and splits the sentence into a list

            parsed = None

            match raw[0][3:]: # Routes the sentence to the right parser depending on its scheme or raises an error if the scheme is not supported
                case 'RMC':parsed = rmc(raw)
                case 'GGA':parsed = gga(raw)
                case _:raise ValueError(f"Sentence schema type not covered or non-existent (schema : {raw[0][3:]}).")

            parsed['VLDT'] = True # Marks the sentence as valid (for future re-imports if the sentence is exported to a file)

            return parsed

        match raw_sentence: # Uses the right importation method depending on sentence type

            case str(): # str -> Raw sentence -> Parses the sentence with parse
                self.sentence = parse(raw_sentence)

            case list(): # list -> Sentence as a list -> Reassembles the raw sentence then parses it with parse
                self.sentence = parse(','.join(raw_sentence))

            case dict(): # dict -> Maybe a sentence that has already been parsed and that is being re-imported -> Imports the sentence directly if the validity mark is detected
                if raw_sentence['VLDT']:self.sentence = raw_sentence
                else:raise ValueError(f"The sentence couldn't be verified as valid. Sentence : {raw_sentence}")

    def __str__(self) -> str:
        return str(self.sentence)

    def __repr__(self) -> str:
        return str(self.sentence)

    def __len__(self) -> int:
        return len(self.sentence)

    def __getitem__(self, key: str):
        return self.sentence.get(key)

    def coordinates(self, schema):

        for check in (
                (schema, tuple),
                (schema[0], float),
                (schema[1], float)
        ):
            check_type(check[0], check[1])

        latd = self['LATD']
        lond = self['LOND']

        for c in (latd,lond):
            if c is None:
                raise ValueError(f'Coordinate(s) missing : LAT:{latd},LON:{lond}')

        match schema:
            case dict():return {'LATD':latd, 'LOND':lond}
            case list():return [latd, lond]
            case tuple():return latd, lond
            case str():return f'{latd},{lond}'
            case _:raise ValueError(f'NMEA sentence format not supported.')