import os
import json
from difflib import get_close_matches


with open(os.path.join("dictionary", "data", "data.json"), 'r') as jsonfile:
    data = json.load(jsonfile)


def translate(word_to_translate):
    word_to_translate = word_to_translate.lower()
    matches = get_close_matches(word_to_translate, data.keys())
    if word_to_translate in data:
        return data[word_to_translate]
    elif word_to_translate.capitalize() in data:
        return data[word_to_translate.capitalize()]
    elif word_to_translate.title() in data:
        return data[word_to_translate.title()]
    elif word_to_translate.upper() in data:
        return data[word_to_translate.upper()]
    elif len(matches) > 0:
        return data[matches[0]]
    else:
        return "The word %s doesn't exist or not found!" % word_to_translate.upper()


if __name__ == '__main__':
    while True:
        word = input("Enter a word to search for <>: ")
        if word == "\\end":
            break
        else:
            responses = translate(word)
            if type(responses) == list:
                for response in responses:
                    print(response)
            else:
                print(responses)