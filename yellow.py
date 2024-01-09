lines = 20
columns = 102


buffer1 = [" " * 50] * (lines - 2)
buffer2 = [" " * 50] * (lines - 2)


symbol_table = {}


editing_text = False
opened_file = ""
buffer = []
current_file_line = 0


current_directory = "/"
skip_event = False


folder = {"name": "", "root": "", "files": [], "folders": []}
file = {"name": "", "content": ""}
fs = {
    "/": {
        "name": "/",
        "root": "/",
        "files": [{"name": ".bash_history", "content": ""}],
        "folders": [],
    }
}


pending_commands = []


while True:
    print("\n" * 100)
    print("-" + "-" * (columns - 2) + "-")
    print("\n" * 100)
    print("-" + "-" * (columns - 2) + "-")
    for x in range(len(buffer1)):
        line0 = buffer1[x]
        line1 = buffer2[x]
        print("⎢" + line0 + "⎢" + line1 + "⎢")
    print("-" + "-" * (columns - 2) + "-")
    if skip_event:
        command_original = ""
    elif len(pending_commands) == 0:
        command_original = input(">> ")
    else:
        command_original = pending_commands[0]
        pending_commands = pending_commands[1:]
    fs["/"]["files"][0]["content"] += "\n" + command_original
    fs["/"]["files"][0]["content"] = fs["/"]["files"][0]["content"].strip()
    commands = command_original.split()
    command = ">> " + command_original
    buffer1.append(" " * 50)
    buffer1 = buffer1[1:]
    buffer1[-1] = command + " " * (50 - len(command))
    output = ""
    if len(commands) == 0:
        if skip_event:
            skip_event = False
            commands = [""]
        else:
            continue
    if editing_text == False:
        if commands[0] == "touch":
            if len(commands) < 2:
                continue
            for x in fs[current_directory]["files"]:
                if x["name"] == commands[1]:
                    continue
            fs[current_directory]["files"].append(
                {"name": commands[1][:14], "content": ""}
            )
        elif commands[0] == "ls":
            buffer2 = [" " * 50] * (lines - 2)
            file_listing = -1
            for x in fs[current_directory]["files"]:
                file_listing += 1
                current_output = str(file_listing) + ". " + x["name"]
                output += current_output
                output += " " * (21 - len(current_output)) + "  File  "
                output += "  " + str(len(x["content"])) + "\n"
            for x in fs[current_directory]["folders"]:
                file_listing += 1
                current_output = str(file_listing) + ". " + x["name"]
                output += current_output
                output += " " * (21 - len(current_output)) + "  Folder"
                output += "  " + "\n"
            output = output.strip("\n")
            output_lines = output.split("\n")
            mid = []
            if len(output_lines) > 0:
                mid = ["S. Name" + " " * 16 + "Type    " + "size"]
            output_lines = (
                ["Here's the directory listing for " + current_directory]
                + mid
                + output_lines
            )
            if len(output_lines) > 18:
                output_lines = output_lines[len(output_lines) - 18 :]
            output_lines_i = -1
            for x in output_lines:
                output_lines_i += 1
                buffer2[output_lines_i] = x + " " * (50 - len(x))
        elif commands[0] == "mkdir":
            fs[current_directory]["folders"].append(
                {
                    "name": commands[1][:14],
                    "root": current_directory,
                    "files": [],
                    "folders": [],
                }
            )
            fs[commands[1][:14]] = {
                "name": commands[1][:14],
                "root": current_directory,
                "files": [],
                "folders": [],
            }
        elif commands[0] == "cd":
            if len(commands) < 2:
                continue
            commands[1] = commands[1].strip()
            if commands[1] == "..":
                commands[1] = fs[current_directory]["root"]
            if commands[1] in fs:
                current_directory = commands[1]
        elif commands[0] == "cat":
            if len(commands) < 2:
                continue
            buffer2 = [" " * 50] * (lines - 2)
            commands[1] = commands[1].strip()
            file = {}
            for x in fs[current_directory]["files"]:
                if x["name"] == commands[1]:
                    file = x
                    break
            if file == {}:
                continue
            output_lines = file["content"].split("\n")
            if len(output_lines) > 18:
                output_lines = output_lines[len(output_lines) - 18 :]
            output_lines_i = -1
            for x in output_lines:
                output_lines_i += 1
                buffer2[output_lines_i] = x + " " * (50 - len(x))
        elif commands[0] == "clear":
            if len(commands) < 2:
                continue
            if commands[1] == "1":
                buffer1 = [" " * 50] * (lines - 2)
            if commands[1] == "2":
                buffer2 = [" " * 50] * (lines - 2)
        elif commands[0] == "edit":
            if len(commands) < 2:
                continue
            buffer2 = [" " * 50] * (lines - 2)
            commands[1] = commands[1].strip()
            file = {}
            for x in fs[current_directory]["files"]:
                if x["name"] == commands[1]:
                    file = x
                    break
            if file == {}:
                continue
            buffer = file["content"].split("\n")
            editing_text = True
            opened_file = x["name"]
            skip_event = True
        elif commands[0] == "rm":
            if len(commands) < 2:
                continue
            buffer2 = [" " * 50] * (lines - 2)
            commands[1] = commands[1].strip()
            file_index = -1
            for x in fs[current_directory]["files"]:
                file_index += 1
                if x["name"] == commands[1]:
                    fs[current_directory]["files"] = (
                        fs[current_directory]["files"][:file_index]
                        + fs[current_directory]["files"][file_index + 1 :]
                    )
                    break
        elif commands[0] == "mode" or commands[0] == "median" or commands[0] == "mean":
            if len(commands) < 2:
                continue
            buffer2 = [" " * 50] * (lines - 2)
            commands[1] = commands[1].strip()
            file = {}
            for x in fs[current_directory]["files"]:
                if x["name"] == commands[1]:
                    file = x
                    break
            if file == {}:
                continue
            content = file["content"].split(",")
            content_i = -1
            full_continue = False
            for x in content:
                content_i += 1
                content[content_i] = x.strip()
                if not str(content[content_i]).isdigit():
                    full_continue = True
                    break
                content[content_i] = int(content[content_i])
            if full_continue:
                continue
            import statistics


            if commands[0] == "mean":
                out = str(statistics.mean(content))
            elif commands[0] == "median":
                out = str(statistics.median(content))
            elif commands[0] == "mode":
                out = str(statistics.mode(content))
            buffer2 = [" " * 50] * (lines - 2)
            buffer2[0] = out + " " * (50 - len(out))
        elif commands[0] == "fate":
            import random


            jokes = [
                "Quantum physics is like a box of chocolates. You never know where the electron is.",
                "Why did the computer go to therapy? It had too many bytes of emotional baggage.",
                "Parallel lines have so much in common. It's a shame they'll never meet.",
                "How does a computer catch a virus? By using anti-virus software!",
                "I told my wife she should embrace her mistakes. She gave me a hug.",
                "Why don't scientists trust atoms? Because they make up everything!",
                "The early bird might get the worm, but the second mouse gets the cheese.",
                "I used to play piano by ear, but now I use my hands and fingers.",
                "Why do programmers prefer dark mode? Less light attracts fewer bugs.",
                "I asked the librarian if the library had any books on paranoia. She whispered, 'They're right behind you.'",
            ]
            buffer2 = [" " * 50] * (lines - 2)
            res = (
                jokes[random.randint(0, len(jokes) - 1)]
                .replace("!", ".")
                .replace("?", ".")
                .split(".")
            )
            joke_res_index = -1
            for x in res:
                if x == "\n" or x == "":
                    continue
                joke_res_index += 1
                x += "."
                x = x.strip()
                buffer2[joke_res_index] = x + " " * (50 - len(x))
    else:
        if command == "END":
            editing_text = False
            opened_file = ""
            current_file_line = 0
            buffer = []
        elif commands[0] == "TO":
            if len(commands) < 2:
                continue
            if not commands[1].isdigit():
                continue
            current_file_line = int(commands[1])
            if current_file_line > len(buffer):
                current_file_line = len(buffer) - 1
            else:
                current_file_line -= 1
            if current_file_line < 0:
                current_file_line = 0
        elif commands[0] == "INSERT":
            buffer2 = [" " * 50] * (lines - 2)
            content = command.partition("INSERT")[2].partition(" ")[2]
            buffer[current_file_line] = content
        elif commands[0] == "ADD_LINE":
            buffer2 = [" " * 50] * (lines - 2)
            buffer.append("")
            current_file_line += 1
        elif commands[0] == "CLEAR_LINE":
            buffer2 = [" " * 50] * (lines - 2)
            buffer[current_file_line] = ""
        elif commands[0] == "DELETE_LINE":
            buffer2 = [" " * 50] * (lines - 2)
            if len(buffer) > 0:
                if len(buffer) != 1:
                    buffer = (
                        buffer[:current_file_line] + buffer[current_file_line + 1 :]
                    )
                else:
                    buffer = [""]
                if current_file_line != 0:
                    current_file_line -= 1
        elif commands[0] == "SAVE":
            buffer2 = [" " * 50] * (lines - 2)
            opened_file_index = -1
            for x in fs[current_directory]["files"]:
                opened_file_index += 1
                if x["name"] == opened_file:
                    break
            fs[current_directory]["files"][opened_file_index]["content"] = "\n".join(
                buffer
            )
            editing_text = False
            opened_file = ""
            current_file_line = 0
            buffer = []
            continue
        top_limit = current_file_line - 8
        if (top_limit) < 0:
            top_limit = 0
        top_lines = buffer[top_limit:current_file_line]
        bottom_lines = buffer[
            current_file_line + 1 : current_file_line + 1 + (17 - len(top_lines))
        ]
        command = command_original
        output_lines_i = -1
        for x in top_lines:
            output_lines_i += 1
            extra = " "
            if output_lines_i == current_file_line:
                extra = "*"
            x = (extra + str(output_lines_i + 1) + ". " + x)[:50]
            buffer2[output_lines_i] = x + " " * (50 - len(x))
        output_lines_i += 1
        extra = " "
        if output_lines_i == current_file_line:
            extra = "*"
        x = (extra + str(output_lines_i + 1) + ". " + buffer[current_file_line])[:50]
        buffer2[output_lines_i] = x + " " * (50 - len(x))
        for x in bottom_lines:
            output_lines_i += 1
            extra = " "
            if output_lines_i == current_file_line:
                extra = "*"
            x = (extra + str(output_lines_i + 1) + ". " + x)[:50]
            buffer2[output_lines_i] = x + " " * (50 - len(x))