import requests
from bs4 import BeautifulSoup
import random

BASE_URL = "https://handbook.unimelb.edu.au/search?query="
OUTPUT_FILE = "output.txt"

class Subject():
    def __init__(self, code, name):
        self.code = code
        self.name = name
    
    def __str__(self) -> str:
        return f"{self.code}: {self.name}"

    def __repr__(self) -> str:
        return f"{self.code}: {self.name}"

    def __lt__(self, other):
        return self.code < other.code

def main():
    query = input("Search subjects: ")
    subjects = getSubjects(query)
    random.shuffle(subjects)
    for subject in subjects:
        ans = input(f"What is the code for {subject.name}? ")
        if ans.lower() == subject.code.lower():
            print("Correct!")
        else:
            print(f"Incorrect! It is {subject.code}.")
    

def getSubjects(query):
    soup = BeautifulSoup(requests.get(f"{BASE_URL}{query}").text, "html.parser")
    results = soup.find("ul", {"class":"search-results__list"})
    subjects = []
    for item in results.find_all("li", {"class": "search-result-item"}):
        flags =  item.find("div", {"class":"search-result-item__flags"})
        is_subject = False
        for flag in flags.find_all("span"):
            if str(flag.text) == "Subject":
                is_subject = True
                break
        if not is_subject:
            continue
        subject = item.find("div", {"class":"search-result-item__name"})
        subjects.append(Subject(subject.span.text, subject.h3.text))
    
    subjects.sort()
    f = open(OUTPUT_FILE, "w")
    f.writelines(map(lambda x: f"{str(x)}\n", subjects))
    f.close()
    return subjects
    
if __name__ == "__main__":
    main()