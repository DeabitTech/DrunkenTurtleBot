from _datetime import datetime
from time import time
from helpers import paths

tab = '    '
nl = '\n'


def raw_log_append(*stuff_to_print_in_a_line):
    lineToPrint = ''
    for s in stuff_to_print_in_a_line:
        lineToPrint += str(s)
    lineToPrint += '\n'
    with open(paths.rawLog, 'a') as f:
        f.writelines(lineToPrint)
    return True


def event_log_append(*stuff_to_print_in_a_line):
    lineToPrint = ''
    for s in stuff_to_print_in_a_line:
        lineToPrint += str(s)
    lineToPrint += '\n'
    with open(paths.eventLog, 'a') as f:
        f.writelines(lineToPrint)
    return True


def error_log_append(errorString, sessionID, statusID):
    localTimestamp = int(time())
    localDateTime = datetime.fromtimestamp(localTimestamp)
    with open(paths.errorLog, 'a') as f:
        f.writelines("Status crashed and the following exception or error was raised:")
        f.writelines('\n\t' + errorString)
        f.writelines('\n\tSession ID: ' + sessionID)
        f.writelines('\n\tCurrent or previous Status ID: ' + statusID)
        f.writelines('\n\t' + str(localTimestamp))
        f.writelines('\n\t' + str(localDateTime) + '\n')

def new_orders_log_csv_append(list_of_variables_to_print_as_csv_record_fields):
    recordToPrint = ''
    for v in list_of_variables_to_print_as_csv_record_fields:
        recordToPrint = recordToPrint + '"' + str(v) + '",'
    recordToPrint = recordToPrint[:-1] + '\n'
    with open(paths.newOrdersLog, 'a') as f:
        f.writelines(recordToPrint)
    return True


def session_log_append(session_id_str, *stuff_to_print_in_a_line):
    lineToPrint = ''
    for s in stuff_to_print_in_a_line:
        lineToPrint += str(s)
    lineToPrint += '\n'
    try:
        f = open(paths.session_logs/session_id_str, 'a')
        f.writelines(lineToPrint)
    except:
        with open(paths.session_logs/session_id_str, 'w') as f:
            f.writelines(lineToPrint)
    return True
