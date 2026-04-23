from ..rmc import parse as rmc
from ..rmcf import parse as rmcf

def parse(raw):
    if len(raw[3].split('.')[0]) < 4 or len(raw[5].split('.')[0]) < 5:
        return rmcf(raw)
    return rmc(raw)
