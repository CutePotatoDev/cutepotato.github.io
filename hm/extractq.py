import pdfplumber
import re
import json


rline = re.compile(r"\d+\. .*[\.?:“…]", re.IGNORECASE)      # Question and answer format.
rqnr = re.compile(r"(\d+)\. ")      # Question number extract.
rpic = re.compile(r".* ([\w]{2,})[ ]+paveiksle.*")      # Picture name extract.

qbuffer = []    # List of raw questions text.


with pdfplumber.open("RM_egzaminu_klausimai_patvirtinti-20200211_1V-181.pdf") as pdf:
    tmp = ""
    for nr in range(32, 56):
        page = pdf.pages[nr]

        content = page.extract_text()
        # print(content)

        for line in content.splitlines():
            if rline.match(line):
                qbuffer.append(line.strip())
                tmp = ""    # New full question found. Tmp already out of date. Probably full of trash data.
            else:
                tmp += line
                # print(tmp)

                if rline.match(tmp):
                    qbuffer.append(tmp.strip())
                    tmp = ""
                elif "Kilometrinių" in tmp:     # Some mistakes in formatting.
                    qbuffer.append(tmp.strip())
                    tmp = ""

i = 0
qidx = 0
aidx = 1

questions = []
question = {}


for q in qbuffer:
    i += 1
    # print(q)

    if i == 1:
        qmatch = rqnr.match(q)

        if qmatch and (qidx + 1) == int(qmatch.group(1)):
            qidx += 1
        else:
            print("Questions sequence is not good.")
            break

        pmatch = rpic.match(q)
        if pmatch:
            picname = pmatch.group(1)
            question["p"] = picname[0:2] if len(picname) > 2 else picname
        else:
            question["p"] = None

        question["q"] = re.sub(r"\d+\. ", "", q)

    elif i == 2 or i == 3 or i == 4:
        qmatch = rqnr.match(q)

        if qmatch and aidx == int(qmatch.group(1)):
            aidx += 1
        else:
            print("Q `%s` Nok." % qidx)
            print(q)
            print("Answers sequence is not good.")
            break

        if "a" not in question:
            question["a"] = []

        question["a"].append({"key": q[3:]})

    if i == 4:
        print("Q `%s` Ok." % qidx)
        i = 0
        aidx = 1
        questions.append(question)
        question = {}


with open("questions.json", encoding="utf=8") as fd:
    questionsdata = json.load(fd)

questionsdata["questions"] = questions

with open("questions.json", "w", encoding="utf=8") as fd:
    json.dump(questionsdata, fd, indent=4, ensure_ascii=False)


# Little beautify answers arrays.
with open("questions.json", encoding="utf=8") as fd:
    content = fd.read()

content = re.sub(r"{\n[ ]{20}(\"key\")", "{ \\1", content, flags=re.S)
content = re.sub(r"\n[ ]{16}}", " }", content, flags=re.S)

with open("questions.json", "w", encoding="utf=8") as fd:
    fd.write(content)
