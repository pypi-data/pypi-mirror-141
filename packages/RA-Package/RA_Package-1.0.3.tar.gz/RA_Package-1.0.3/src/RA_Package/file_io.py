import main

print_mode = False

def read(filename):
    data = []
    with open(filename, "r+") as f:
        for line in f:
            if line:
                data.append(line.strip())
            if main.debugMode:
                if print_mode:
                    print("File" + filename + ", read line: " + str(data))
    return data

def write(filename, data):
    with open(filename, "w+") as f:
        f.truncate()
        for line in data:
            f.write(line)
            if main.debugMode:
                if print_mode:
                    print("File" + filename + ", write line: " + str(line))

def append(filename, data):
    with open(filename, "a") as f:
        for line in data:
            f.write(line)
            if main.debugMode:
                if print_mode:
                    print("File: " + filename + ", append line: " + str(line))
