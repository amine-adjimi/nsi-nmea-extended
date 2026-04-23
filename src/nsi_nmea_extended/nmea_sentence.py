from .check import check_type, check_nmea_sum
import importlib

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

            try:
                parsed = importlib.import_module(f".parse.{raw[0][3:].lower()}", package="nsi_nmea_extended").parse(raw)
            except (ModuleNotFoundError, AttributeError):
                raise ValueError(f"Sentence schema type not covered or non-existent (schema : {raw[0][3:].upper()}).")

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
        latd = self['LATD']
        lond = self['LOND']

        for c in (latd,lond):
            if c is None:
                raise ValueError(f'Coordinate(s) missing : LAT:{latd},LON:{lond}')

        if schema is dict:return {'LATD': latd, 'LOND': lond}
        elif schema is list:return [latd, lond]
        elif schema is tuple:return latd, lond
        elif schema is str:return f'{latd},{lond}'
        else:raise ValueError('NMEA sentence format not supported.')