import nltk
import re
from datasets import Dataset, concatenate_datasets

# sentence 단위로 잘라줌
def sentence_parser(text:str):
    seps = nltk.tokenize.sent_tokenize(text)
    return seps

# label_names는 same with KLUE/NER : dataset['train'].features['ner_tags'].feature.names
LABEL_NAMES = [
    'B-DT', 'I-DT',     # 0, 1 : Date(DT)
    'B-LC', 'I-LC',     # 2, 3 : Location(LC)
    'B-OG', 'I-OG',     # 4, 5 : Organization(OG)
    'B-PS', 'I-PS',     # 6, 7 : Person(PS)
    'B-QT', 'I-QT',     # 8, 9 : Quantity(QT)
    'B-TI', 'I-TI',     # 10, 11 : Time(TI)
    'O', 'O',           # 12, 13 : Outside(O)
    'B-CR', 'I-CR'      # 14, 15 : Crime(CR) **
] 
# type_names는 KLUE에서 BIO 구분 없이 (same with : label2type(label_names))
TYPE_NAMES = [
    'DT',               # 0 : Date(DT)
    'LC',               # 1 : Location(LC)
    'OG',               # 2 : Organization(OG)
    'PS',               # 3 : Person(PS)
    'QT',               # 4 : Quantity(QT)
    'TI',               # 5 : Time(TI)
    'O',                # 6 : Outside(O)
    'CR',               # 7 : Crime(CR) **
]

def label2type(label_names):
    type_names = []
    for i in range(0, len(label_names), 2):
        if '-' in label_names[i]:
            type_names.append(label_names[i].split('-')[-1])
        else:
            type_names.append(label_names[i])
            
    return type_names

def type2label(type_, type_names):
    if type_ == 'O': 
        return type_names.index(type_)*2, type_names.index(type_)*2

    begin_id = type_names.index(type_)*2
    inside_id = type_names.index(type_)*2 + 1
    
    return begin_id, inside_id

# 꺾쇠 <, >로 감싸진 NER 태그를 찾아 해석, tokens와 ner_tags 리스트를 만들어주는 과정
# ex: "안녕 <길동:PS>!" -> "길동:PS" -> "길동", "PS"
def ne_tag_finder(sent:str):
    c = re.compile("\<([^>]+)")
    nes = re.findall(c, sent)

    return nes

def ne_tokenizer(sent:str):
    global TYPE_NAMES

    nes = ne_tag_finder(sent)

    ne_tokens = []
    ne_ner_tags = []
    for tagged in nes:
        try:
            ne_, type_ = tagged.split(':')
        except: 
            # 태깅이 아닌 단순 꾸밈 <, > 면 Outside로 돌려서 넘겨
            ne_ = '<' + tagged + '>'
            type_ = 'O'

        B, I = type2label(type_, TYPE_NAMES)
        
        tokens = list(ne_)
        ner_tags = [B] + [I] * (len(ne_)-1)
        
        ne_tokens.append(tokens)
        ne_ner_tags.append(ner_tags)
        
    # ne_tokens: 한글자씩 파싱된 NE 토큰 list들의 list
    # ne_ner_tags : ne_tokens 각 토큰에 대응하는 LABEL ID (LABEL_NAMES[ID]가 해당 태그를 의미)    
    return ne_tokens, ne_ner_tags

# <, > 태그 안된 일반 문자열(Outside) 처리
def o_tokenizer(sent:str):
    c = re.compile("\<([^>]+)")
    seps = re.split(c, sent)[::2]

    o_tokens = []
    o_ner_tags = []
    for sep in seps:
        if sep.startswith('>'):
            tokens = list(sep[1:])
        else:
            tokens = list(sep)
            
        ner_tags = [12] * len(tokens)
        
        o_tokens.append(tokens)
        o_ner_tags.append(ner_tags)
        
    # o_tokens: 한글자씩 파싱된 O 토큰 list들의 list
    # o_ner_tags : o_tokens 각 토큰에 대응하는 LABEL ID (12 : Outside(O))
    return o_tokens, o_ner_tags

# 두 리스트를 합쳐서 전체 tokens, ner_tags를 만듬.
def ner_tokenizer(sent:str):
    ne_tokens, ne_ner_tags = ne_tokenizer(sent)
    o_tokens, o_ner_tags = o_tokenizer(sent)

    tokens = []
    ner_tags = []
    for i in range(len(ne_tokens)):
        tokens += o_tokens[i] + ne_tokens[i]
        ner_tags += o_ner_tags[i] + ne_ner_tags[i]
    tokens += o_tokens[-1]
    ner_tags += o_ner_tags[-1]

    # tokens: 한글자씩 파싱된 전체 토큰 리스트
    # ner_tags: tokens에 해당하는 LABEL ID 리스트
    return tokens, ner_tags


# yielder가 실질적으로 위 함수들을 이용해 sentence, tokens, ner_tags 순차적으로 쏴주고
# 외부 노출 함수 ner_dataset_generator는 huggingface Dataset으로 만들어줌
def yielder(text:str):
    seps = sentence_parser(text)
    for sent in seps:
        tokens, ner_tags = ner_tokenizer(sent)
        yield {'sentence': sent, 'tokens': tokens, 'ner_tags': ner_tags}

# 외부 노출 함수 1: NER Tagging된 text를 입력하면 KLUE/NER 타입의 Dataset 생성
def ner_dataset_generator(text:str):
    gen = yielder(text)
    sentence, tokens, ner_tags = [], [], []
    for ge in gen:
        sentence.append(ge['sentence'])
        tokens.append(ge['tokens'])
        ner_tags.append(ge['ner_tags'])
    dataset = Dataset.from_dict({
        'sentence': sentence, 
        'tokens': tokens,
        'ner_tags': ner_tags,
    })
    return dataset

# sentence list input을 위한 yielder, ner_dataset_generator도 만들자
def yielder(seps:list):
    for sent in seps:
        tokens, ner_tags = ner_tokenizer(sent)
        yield {'sentence': sent, 'tokens': tokens, 'ner_tags': ner_tags}

# 외부 노출 함수 1: NER Tagging된 text를 입력하면 KLUE/NER 타입의 Dataset 생성
def ner_dataset_generator(seps:list):
    gen = yielder(seps)
    sentence, tokens, ner_tags = [], [], []
    for ge in gen:
        sentence.append(ge['sentence'])
        tokens.append(ge['tokens'])
        ner_tags.append(ge['ner_tags'])
    dataset = Dataset.from_dict({
        'sentence': sentence, 
        'tokens': tokens,
        'ner_tags': ner_tags,
    })
    return dataset

# 외부 노출 함수 2: NER Tagging된 text를 처리해 이미 생성된 Dataset에 덧붙여 생성
def ner_dataset_extender(ds1:Dataset, text:str):
    ds2 = ner_dataset_generator(text)
    merged_ds = concatenate_datasets([ds1, ds2])
    return merged_ds

# 외부 노출 함수 3: DS 두개 합치기
def ner_dataset_merger(ds1:Dataset, ds2:Dataset):
    merged_ds = concatenate_datasets([ds1, ds2])
    return merged_ds


# tester
if __name__ == "__main__":
    test_sentence1 = "<여덟 살 때:DT> 8086 PC에서 베이직(Basic)으로 <첫 번:QT>째 프로그램을 만들었는데, 이때 이미 기본 방정식의 2D 플로팅 방법을 구현할 수 있었다. IP 주소는 <192.168.0.1:LC>이였다."
    test_sentence2 = "<2005년:DT>에는 OpenCV(<v0.96:QT>)를 이용해 컴퓨터 비전이 지원하는 인간-컴퓨터 상호 작용 방법을 사용해 <발렌시아 폴리테크닉 대학:OG>(<Universitat Politecnica de Valencia:OG>)의 IT 연구를 진행했으며, 이 주제를 바탕으로 최종 프로젝트를 진행했고 그 결과를 <HCI 스페인 학회:OG>에 발표했다. 오픈소스 3D 소프트웨어 프로젝트인 블렌더(Blender)에 참여했고, 컴퓨터 그래픽 소프트웨어 개발자로서 첫 상업 영화인 프리버즈: <밍쿠:PS>와 <찌아:PS>의 도시 대탈출(<2010:DT>)의 제작 과정에도 기여했다. 컴퓨터 비전, 컴퓨터 그래픽, 패턴 인식의 경험과 다양한 프로젝트 및 스타트업 작업, 컴퓨터 비전, 광학 문자 인식, 증강현실에 관한 지식을 적용함으로써 IT 분야에서 <10년:QT> 이상의 경력을 쌓았다. ‘DamilesBlog’ 블로그의 저자이며 OpenCV, 일반적인 컴퓨터 비전, 광학 문자 인식 알고리즘의 연구 기사와 자습서를 블로그에 게시하고 있다."
    test_sentence3 = ""
    res1 = ner_dataset_generator(test_sentence1)
    print(res1)
    res2 = ner_dataset_generator(test_sentence2)
    print(res2)
    res3 = ner_dataset_generator(test_sentence3)
    print(res3)
    # for con in conc:
    #     print(con)

    res4 = ner_dataset_extender(res1, test_sentence2)
    res5 = ner_dataset_extender(res4, test_sentence3)
    print(res5)
    print(res5[0])
