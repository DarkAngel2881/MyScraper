from bs4 import BeautifulSoup as bs
import requests
import re
import csv




def get_sostitutions(classe):
    URL = "https://sostituzionidocenti.com/fe/controllaCodice.php"
    payload = {"pass": "FE71199LC"}
    s = requests.session()
    response = s.post(URL, data=payload)
    soup = bs(response.content, "html.parser")

    sost = {}

    pattern = re.compile(f"{classe}.*")
    rows = soup.find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        if len(cells) > 0:
            classe = cells[1].get_text()
            if re.match(pattern, classe):
                columns = row.find_all("td")
                if len(columns) > 0:
                    hour = columns[0].text.strip()[0]
                    teacher = columns[2].text.strip()
                    repl_teach = columns[3].text.strip()
                    note = columns[6].text.strip()
                    
                    sost[len(sost)] = {
                        "hour": hour,
                        "teacher": teacher,
                        "replacement": repl_teach,
                        "note": note
                    }
                    
                    return sost
                    #print(f"Hour: {hour}, Teacher: {teacher},  Replacement: {repl_teach}, Notes: {note}")
                    
def build_csv():
    sosts = get_sostitutions("5AI")
    with open('substitutions.csv', mode='w', newline='', encoding='utf-8') as f:
    fieldnames = ['hour', 'teacher', 'replacement', 'note']
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    writer.writeheader()
    for i, sost in enumerate(sosts.values()):
        writer.writerow(sost)            



'''classe = input("Classe --> ")
if(classe == ""):
    classe = "5AI"
else:
    classe = classe.capitalize()'''






