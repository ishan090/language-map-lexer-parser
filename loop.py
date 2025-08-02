
from sys import argv
import os
import json


c = {         # colours
    "b": "\033[94m",
    "reset": '\033[0m',
    "y": "\033[33m",
    "g": "\033[32m",
    "r": "\033[31m"
    }

def gettoken(line, index):
    word = ""
    types = {
        "=": 1,
        "/": 2,
        "\n": 3,
        "~": 4,
        "#": 5,
        ",": 2
        }
    t = 10

    # get to something that's not a white space
    while index < len(line) and line[index] == " ":
        index += 1
    if index >= len(line):
        return None
    else:
        word += line[index]
        t = types.get(line[index], 0)
        if t == types["#"]:
            return None
        index += 1
        if t == types["~"]:
            return None, index, t
    carry = ""
    while index < len(line) and (types.get(line[index], 0) == t or line[index] == " "):
        word += carry + line[index]
        carry = ""
        index += 1
        if index < len(line) and line[index] == " ":
            carry += " "
        while index < len(line) and line[index] == " ":
            index += 1

    return word, index, t


def parse(data, langs, output):
    """Given the output of file.readlines() returns the tokens as a tuple"""
    lines = []
    comments = {}
    lines.append(langs)
    for line in data:
        words = []
        part = []
        word = gettoken(line, 0)
        while word is not None:
            # print("this is our word:", word)
            w, i, t = word
            if t == 1:
                # print("is a separator")
                words.append(part)
                # print("current line:", words)
                part = []
            elif t == 4:  # then it's a soft comment
                if len(words) and len(part):  # attach to the same line
                    comments[len(lines)] = line[i:]
                else: # attach to the previous line
                    comments[len(lines)-1] = line[i:]
                break
            if t == 0:
                part.append(w)
            word = gettoken(line, i)
        if part:
            words.append(part)
        if words:
            lines.append(words)
    return lines, comments



if __name__ == "__main__":

    if len(argv) >= 1 and argv[1] == "-h":
        with open("help_msg.txt") as f:
            help_msg = f.read()
        print(help_msg)
        exit()

    # print("sys argv", argv)
    if len(argv) <= 1:
        print("Error: require a file to read from (-h for help)")
        exit()
    elif not os.path.isfile(argv[1]):
        print(f"Error: file {argv[1]} doesn't exist (-h for help)")
        exit()

    output = None
    if len(argv) == 4:
        # Then the languages are given and output file isn't
        langs = [[argv[2]], [argv[3]]]
    elif len(argv) == 3 or len(argv) <= 2:  # output given but no langs
        if len(argv) != 2:
            output = argv[2]
        while True:
            langs = [[i] for i in input("Any idea what the languages are? (write both of them out separated by a space)\n--> ").split()]
            if len(langs) <= 1:
                print("Sorry, try again. E.g., \"español english\"")
                continue
            break
    else:  # both lang and output with some possible extra stuff
        output = argv[2]
        langs = [[argv[3]], [argv[4]]]

    filename = argv[1]

    if output is None:
        output = filename.split(".")[0] + ".json"
        print(f"{c['y']}Warning: output files wasn't given; using", output, f"as write file{c['reset']}")
    comm_out = filename.split(".")[0] + "_comm.json"

    print(f"{c['b']}Info: Reading file{c['reset']}", filename)
    with open(filename) as f:  # Read the stuff
        data = f.readlines()
    print(f"{c['g']}Succes: Read file{c['reset']}", filename)

    print(f"{c['b']}Info: parsing the data{c['reset']}")
    parsed, comms = parse(data, langs, output)  # Parse it
    print(f"{c['g']}Succes: parsed{c['reset']}")

    print(f"{c['b']}writing to", output, f"and comments{c['reset']}")
    with open(output, "w") as out:
        json.dump(parsed, out)
    with open(comm_out, "w") as c_out:
        json.dump(comms, c_out)
    print(f"{c['g']}Succes: writing complete{c['reset']}")


