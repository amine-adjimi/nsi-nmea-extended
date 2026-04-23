import os
import datetime
import traceback

def log(error, sentence=None):
    """
    Logs an error to nsi-nmea.log if a 'dev' file exists in the current directory.
    
    :param error: The exception to log
    :param sentence: An optional sentence to include in the log
    :rtype: None
    """
    if not os.path.exists('dev'):return

    timestamp = datetime.datetime.now().strftime("%Y:%m:%d %H:%M:%S.%f")[:-2] # YYYY:MM:DD HH:MM:SS.SSSS

    tb = traceback.extract_tb(error.__traceback__)
    if tb:
        filename, line, location, text = tb[-1]
    else:
        location = "Unknown"

    error_type = type(error).__name__
    error_message = str(error)

    log_entry = f"{timestamp} -> [{location}] -> [{error_type}] -> [{error_message}]"
    if sentence:
        log_entry += f" : {sentence}"
    
    log_entry += "\n"

    with open('nsi-nmea.log', 'a', encoding='utf-8') as f:
        f.write(log_entry)
