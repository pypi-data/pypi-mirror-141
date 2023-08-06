import datetime as t
import RA_Package.file_io as file_io

session = ""

def last_res(data):
    global session
    if session:
        file_io.append(session, data)
        file_io.append(session, "\n")
    else:
        now = t.datetime.now()
        dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
        dt_string = dt_string.strip()
        session = "results/" + str(dt_string) + "_last_results.txt"
        file_io.write(session, data)
        file_io.write(session, "\n")

def get_res():
    data = file_io.read(session)
    return data

