from .check import check_type, check_both
from .nmea_sentence import NmeaSentence

class NmeaDataset:
    """
    Handles NMEA files in various formats importing and exporting.

    :param datatype: The type of loaded data ('file' is currently the only supported type)
    :type datatype: str
    :param data: The data that is loaded
    :ivar sentences: The list of sentences that has been loaded
    :type sentences: list
    """

    def __init__(self, data, datatype: str = 'file'):
        self.sentences = []

        check_both(datatype, str, 'file')
        check_type(data, str)

        match datatype:
            case 'file':
                from os.path import exists
                if not exists(data):
                    raise FileNotFoundError(f"{data} doesn't exist.")
                if data.endswith(('.nmea','.txt')):
                    try:
                        with open(data,'r',encoding='utf-8-sig') as fi:
                            for line in fi:
                                line = line.strip()
                                if not line:
                                    continue
                                try:self.sentences.append(NmeaSentence(line))
                                except Exception:pass
                    except Exception:pass
                elif data.endswith('.nmeasz'):
                    try:
                        with open(data,'r',encoding='utf-8') as fi:
                            try:self.sentences = eval(fi.read())
                            except Exception:pass
                    except Exception:pass
                else:
                    raise ValueError('File type not supported. Supported file types are : .nmea, .txt and .nmeasz')

    def __str__(self) -> str:
        return str(self.sentences)

    def __repr__(self) -> str:
        return str(self.sentences)

    def __len__(self) -> int:
        return len(self.sentences)

    def __list__(self) -> list:
        return self.sentences

    def __getitem__(self, index: int):
        check_type(index, int)
        return self.sentences[index]

    def export(self, file_name):
        with open(f'{file_name}.nmeasz', 'w', encoding='utf-8') as fi:
            fi.write(str(self.sentences))

    def coordinates(self, schema = tuple) -> list:
        return [sentence.coordinates(schema) for sentence in self.sentences]

    def framing(self) -> dict:
        if not self.sentences or len(self.sentences) <= 1:
            raise ValueError("Not enough NMEA sentences loaded.")
        return {
            'MAX': {
                'LATD':max([sentence['LATD'] for sentence in self.sentences]),
                'LOND':max([sentence['LOND'] for sentence in self.sentences])
            },
            'MIN':{
                'LATD':min([sentence['LATD'] for sentence in self.sentences]),
                'LOND':min([sentence['LOND'] for sentence in self.sentences])
            }
        }