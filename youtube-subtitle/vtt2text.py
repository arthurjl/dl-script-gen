import webvtt
import os
import sys


def main(file_loc):
    transcript = ""
    lines = []
    files = [os.path.join(file_loc, f) for f in os.listdir(file_loc) if f.endswith(".vtt")]

    for f in files:
        vtt = webvtt.read(f)
        for line in vtt:
            # Strip the newlines from the end of the text.
            # Split the string if it has a newline in the middle
            # Add the lines to an array
            lines.extend(line.text.strip().splitlines())

    # Remove repeated lines
    previous = None
    for line in lines:
        line = line.replace("&amp;", "&")
        if line == previous:
            continue
        if transcript == "":
            transcript = line
        else:
            transcript += "\n" + line
        previous = line
    previous = previous.strip()

    filename = os.path.basename(os.path.normpath(file_loc))
    with open(f"cleaned_{filename}.txt", "w", encoding='utf8', errors="ignore") as f:
        f.write(transcript)
        print(f"Saved to cleaned_{filename}.txt")

if __name__=="__main__":
    if len(sys.argv) != 2:
        print("Pass in folder name as param")
    main(sys.argv[1])