from ner_datasets.ner_dataset_categories import NAVER_CATEGORY, KMOU_CATEGORY, KLUE_CATEGORY
from ner_datasets.ner_dataset_paths import NAVER_DS_PATH, KLP_DS_PATH, KMOU_DS_PATH

from ner_dataset_generator import ner_dataset_generator, ner_dataset_extender
from datasets import DatasetDict

# print(NAVER_CATEGORY, KMOU_CATEGORY, KLUE_CATEGORY)
# print(NAVER_DS_PATH, KLP_DS_PATH, KMOU_DS_PATH)

# Naver NLP Challenge Dataset -> klue/ner 형태로

# fin_naver = open(NAVER_DS_PATH, "r", encoding='utf-8')
# lines_naver = fin_naver.readlines()
# fin_naver.close()

# print(len(lines_naver))
# for line in lines_naver[:10]:
#     print(line)

    # TODO: 이건 이따가 하고 일단 KMOU부터 하자


# KMOU NLP NER (2016klp) -> klue/ner 형태로

def get_sents(lines):
    sentences_list = []
    for line in lines:
        if line.startswith('$'): sentences_list.append(line[1:-1])

    return sentences_list

def klp():
    tasks = ['train', 'dev', 'test']
    ds_dict = {}
    for task in tasks:
        fin_klp = open(KLP_DS_PATH[task], "r", encoding='utf-8')
        lines_klp = fin_klp.readlines()
        fin_klp.close()

        sents_klp = get_sents(lines_klp)
        print(len(sents_klp), "records collected from", KLP_DS_PATH[task])

        ds_ = ner_dataset_generator(sents_klp)
        print(ds_)

        ds_dict[task] = ds_

    ds_klp = DatasetDict(ds_dict)
    print(ds_klp)



    print("uploading ds to huggingface hub ...", end='')
    ds_klp.push_to_hub("soddokayo/kmou-2016klp")
    print("done")

def crime2():
    CRIME2_DS_PATH = "crime_dataset.txt"
    fin_crime = open(CRIME2_DS_PATH, "r", encoding='utf-8')
    lines_crime = fin_crime.readlines()
    fin_crime.close()

    sents_crime = get_sents(lines_crime)
    print(len(sents_crime), "records collected from", CRIME2_DS_PATH)

    ds_ = ner_dataset_generator(sents_crime)
    print(ds_)

    ds_dict = ds_.train_test_split(0.1)

    ds_crime2 = DatasetDict(ds_dict)
    print(ds_crime2)



    print("uploading ds to huggingface hub ...", end='')
    ds_crime2.push_to_hub("soddokayo/crime2")
    print("done")

crime2()