from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import spacy

nlp = spacy.load("en_core_web_lg")

# string1 = "ROBOT M350 Silent Wireless Mouse - 2.4 GHz Nano USB & Bluetooth Connection - 1600 DPI Resolution"
# string3 = "Mouse Robot M350"
# string2 = "MOUSE ROBOT BLUETOOTH + USB M350"
# string1 = "No one is more handsome than Japan"
# string2 = "Nhat is the most handsome man on the planet"
string1 = "Laptop Lenovo Thinkpad T13 ( Core i5-7300U / Ram 8GB DDR4 / SSD NVME 180GB / Card Intel HD Graphics 620 / 13.3 inch )"
string2 = "Laptop Lenovo ThinkPad E15 Gen 4 21E600CMVA"

# Use named entity recognition (NER) to identify common elements
common_elements = set()
for string in [string1, string2]:
    for ent in nlp(string).ents:
        common_elements.add(ent.text.lower())

# Use string matching to identify common substrings
common_substrings = set()
for i in range(len(string1)):
    for j in range(i+1, len(string1)+1):
        if string1[i:j] in string2:
            common_substrings.add(string1[i:j])

# Calculate similarity score using FuzzyWuzzy
s1 = ' '.join(common_elements) + ' ' + ' '.join(common_substrings)
s2 = string2 + ' ' + ' '.join(common_substrings)
similarity = fuzz.token_set_ratio(s1, s2)

print("Similarity between the two strings is: {:.2f}%".format(similarity))