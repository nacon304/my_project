import spacy

nlp = spacy.load("en_core_web_lg")

s1 = "Laptop Lenovo Thinkpad T14 GEN 3 21AHS0GM00 (Core i7 1255U/ 16GB/ 512GB SSD/ Intel UHD Graphics/ 14.0inch WUXGA/ DOS/ Black/ Carbon Fiber/3Y)"
s2 = "Laptop Lenovo ThinkPad T14 Gen 3 (21AHS0GM00) Intel Core i7-1255U (upto 4.7Ghz, 12MB) RAM 16GB 512GB SSD Intel UHD Graphics 14in"
s3 = "Laptop Lenovo ThinkPad E15 Gen 4 21E600CMVA"
s4 = "Laptop Lenovo Thinkpad T13 ( Core i5-7300U / Ram 8GB DDR4 / SSD NVME 180GB / Card Intel HD Graphics 620 / 13.3 inch )"

s1_nlp = nlp(s1)
s2_nlp = nlp(s2)
s3_nlp = nlp(s3)
s4_nlp = nlp(s4)

s5 = "ROBOT M350 Silent Wireless Mouse - 2.4 GHz Nano USB & Bluetooth Connection - 1600 DPI Resolution"
s6 = "Mouse Robot M350"
s7 = "MOUSE ROBOT BLUETOOTH + USB M350"

s5_nlp = nlp(s5)
s6_nlp = nlp(s6)
s7_nlp = nlp(s7)

s5_nouns = " ".join([token.lemma_ for token in s5_nlp if token.pos == "NOUN"])

print(s1_nlp.similarity(s2_nlp))
print(s5_nlp.similarity(s7_nlp))
print(s6_nlp.similarity(s7_nlp))
