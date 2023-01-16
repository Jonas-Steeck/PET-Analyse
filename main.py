import pprint
import time
from datasets import load_dataset

# Downloads the PET-dataset on first run, later loads PET-dataset from cache
pet = load_dataset("patriziobellan/PET", name='relations-extraction').get('test')
# Time buffer for download
time.sleep(3)

# Asks wich dataset to analyse (Can also be changed in the script)
set_id = int(input("Type the ID of the dataset/sentence u want to use: "))

# Tokens are a list of all the words in the process description
tokens = pet['tokens'][set_id]

components = []
component = []
tags = pet['ner_tags'][set_id]
sentence_ids = pet['sentence-IDs'][set_id]
token_ids = pet['tokens-IDs'][set_id]

for i, tag in enumerate(tags):
    if tag == 'O':
        continue
    identifier, name = tag.split('-')
    if identifier == 'B':
        if component:
            components.append(component)
        comp_id = [sentence_ids[i], token_ids[i]]
        component = name, comp_id, [tokens[i]]

    if identifier == 'I':
        component[-1].append(tokens[i])

if component:
    components.append(component)

print()
print("COMPONENTS:")
for i, comp in enumerate(components):
    print(f"[{i}] {comp[0]}: {' '.join([word for word in comp[-1]])}")

print()

relations = pet['relations'][set_id]
source_sentence = relations['source-head-sentence-ID']
source_word = relations['source-head-word-ID']
r_type = relations['relation-type']
target_sentence = relations['target-head-sentence-ID']
target_word = relations['target-head-word-ID']

print("RELATIONS:")

for i, rel in enumerate(r_type):
    source = None
    target = None
    for j, comp in enumerate(components):
        if [source_sentence[i], source_word[i]] == comp[1]:
            source = j, comp
        if [target_sentence[i], target_word[i]] == comp[1]:
            target = j, comp
        if source and target:
            src_str = f"[{source[0]}] ({source[1][0]}) {' '.join([word for word in source[1][-1]])}".ljust(40)
            tgt_str = f"[{target[0]}] ({target[1][0]}) {' '.join([word for word in target[1][-1]])}"
            rel_str = f"{rel}".ljust(15)
            print(src_str + " - " + rel_str + " - " + tgt_str)
            source, target = None, None
            break
    else:
        if not source:
            print(f"Couldn't find the source for", end=" ")
        if not target:
            print(f"Couldn't find the target for", end=" ")

        print(f"SOURCE: word: {source_sentence[i]} {source_word[i]}, relation: {rel}, TARGET: word: {target_sentence[i]} {target_word[i]}")

print()
print("FULL TEXT:")
for token in tokens:
    if token == ".":
        print(".")
        continue
    print(f"{token}", end=" ")
