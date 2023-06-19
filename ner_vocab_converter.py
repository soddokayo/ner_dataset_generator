CRIME_VOCAB_PATH = "crime_vocab.txt"

from ner_dataset_generator import ner_dataset_generator, ner_dataset_extender
from datasets import DatasetDict



# 수집한 범죄 용어 사전을 단어 단위로 모델에 추가 학습

def get_sents(lines):
    sentences_list = []
    for line in lines:
        if line.startswith('$'): sentences_list.append(line[1:-1])

    return sentences_list

fin_crime = open(CRIME_VOCAB_PATH, "r", encoding='utf-8')
lines_crime = fin_crime.readlines()
fin_crime.close()

sents_crime = []
for line in lines_crime:
    word, ner_tag, _ = line.split('\t')
    sent = "<"+word+":"+ner_tag+">"
    sents_crime.append(sent)

print(len(sents_crime), "records collected from", CRIME_VOCAB_PATH)

ds_ = ner_dataset_generator(sents_crime)
print(ds_)

ds_dict = {'train': ds_}

ds_crime = DatasetDict(ds_dict)
print(ds_crime)
for rec in ds_crime['train']:
    print(rec)

print("uploading ds to huggingface hub ...")
ds_crime.push_to_hub("soddokayo/crime-1")
print("done")