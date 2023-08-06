import re

data = '''2021-01-01 10:00:05 - Surname1 Name1 (Comment)
Blablabla
Blabla
2021-01-01 23:00:05 - Surname2 SurnameBis Name2 (WorkNotes)
What?
I don't know?
2021-01-02 03:00:05 - Surname1 Name1 (Comment)
Blablabla!'''.splitlines()

first_line_patt = re.compile(r'^(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) - (.*)(?= \() \((.*)\)$')


def parse(lines, idx):
    # parse the meta line
    res = first_line_patt.findall(lines[idx])

    # get the message
    message = []
    while idx < len(lines)-1:
        line = lines[idx + 1]
        idx += 1

        # check if next line is a meta line
        if first_line_patt.match(line):
            break

        # if not, it is a message line
        message.append(line)

    res.append('\n'.join(message))
    return res, idx


idx = 0
while True:
    res, idx = parse(data, idx)
    if not res[0]:
        break
    print(res)


