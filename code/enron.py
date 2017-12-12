import os
import re
import time

header_elements = ["Date: ", "From: ", "To: ", "Subject: "]

def main(i_path, o_path = "", b_path = "broken.txt", search = False, phrase = "", limit = 517401):
    def look_for(path, phrase, o_path = ""):
        nonlocal counter
        nonlocal limit
        if counter > limit:
            return
        else:
            if os.path.isdir(path):
                for folder in os.listdir(path):
                    look_for(os.path.join(path, folder), phrase, o_path)
            else:
                email = open(path, 'r')
                for line in email:
                    if o_path != "":
                            print(counter, "/", limit, "|\t", path)
                    if phrase in line:
                        counter += 1
                        if o_path == "":
                            print(counter, "/", limit, ":\t", path, "\n", line, "\n\n")
                        else:
                            output.append(path + "\n" + line)

    def make_vec(path):
        nonlocal counter
        nonlocal limit
        if counter > limit:
            return
        else:
            if os.path.isdir(path):
                for folder in os.listdir(path):
                    make_vec(os.path.join(path, folder))
            else:
                email = open(path, 'r')
                body = []
                header = []
                element_len = [6, 6, 4, 9]
                body_start = False
                mult = -1
                for line in email:
                    if body_start:
                            body.append(line)
                            continue
                    if line.find("X-FileName: ") != -1:
                        if (len(header) != 4):
                            broken.append(path)
                            return
                        else:
                            body_start = True
                            continue
                    else: # e = [0,3] --> looking for Date, From, To, Subject
                        for e in range(len(header), 4):
                            n = line.find(header_elements[e])
                            if n != -1:
                                if e == 2 and mult == -1: # special case for "To: "
                                    mult = line.find(",")
                                    if mult != -1:
                                        header.append(line[n+element_len[e]:mult])
                                    else:
                                        header.append(line[n+element_len[e]:])
                                else: 
                                    header.append(line[n+element_len[e]:])
                # email parsed succesfully
                print(counter, "/", limit, ":\t", path)
                header = "º".join(header)
                body = "".join(body)
                output.append(path)
                output.append(header)
                output.append(body)
                counter+=1

    start = time.time()
    counter = 1
    output = []
    broken = []
    if search: 
        look_for(i_path, phrase, o_path)
        if o_path != "":
            outFile = open(o_path, 'w')
            outFile.write("\n\n".join(output))
            outFile.close()
    else:
        make_vec(i_path)
        a = [s.replace('\n', '').replace('\r', '') for s in output]
        outFile = open(o_path, 'w')
        outFile.write("º".join(a) + "º")
        outFile.close()
        outFile = open(b_path, 'w')
        outFile.write("\n".join(broken))
        outFile.close()
    print("[", limit, " files took ", time.time() - start, " seconds ]")

# prints the first valid 20,000 files located to a text file
#main("maildir", o_path = "enron_short.txt", limit = 20000)
# prints the first 1000 hits to the phrase, "corporate losses" to console
main("maildir", search = True, phrase = "pete.davis", limit = 20)

def count(i_path):
    files = 0
    def look(path):
        nonlocal files
        if os.path.isdir(path):
            for folder in os.listdir(path):
                    look(os.path.join(path, folder))
        else:
            files+=1
            print("File ", files, ":\t", path)
    look(i_path)
    print("TOTAL:\t", files)