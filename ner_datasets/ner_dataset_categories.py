NAVER_CATEGORY = [
    'PER_B', 'PER_I', # PERSON : 실존, 가상 등 인물명에 해당 하는 것
    'FLD_B', 'FLD_I', # FIELD : 학문 분야 및 이론, 법칙, 기술 등
    'AFW_B', 'AFW_I', # ARTIFACTS_WORKS : 인공물로 사람에 의해 창조된 대상물
    'ORG_B', 'ORG_I', # ORGANIZATION : 기관 및 단체와 회의/회담을 모두 포함
    'LOC_B', 'LOC_I', # LOCATION : 지역명칭과 행정구역 명칭 등
    'CVL_B', 'CVL_I', # CIVILIZATION : 문명 및 문화에 관련된 용어
    'DAT_B', 'DAT_I', # DATE : 날짜
    'TIM_B', 'TIM_I', # TIME : 시간
    'NUM_B', 'NUM_I', # NUMBER : 숫자
    'EVT_B', 'EVT_I', # EVENT : 특정 사건 및 사고 명칭과 행사 등
    'ANM_B', 'ANM_I', # ANIMAL : 동물
    'PLT_B', 'PLT_I', # PLANT : 식물
    'MAT_B', 'MAT_I', # MATERIAL : 금속, 암석, 화학물질 등
    'TRM_B', 'TRM_I', # TERM : 의학 용어, IT곤련 용어 등 일반 용어를 총칭
    '-',              # OUTSIDE
]

KLUE_CATEGORY = [
    'B-DT', 'I-DT', # DATE
    'B-LC', 'I-LC', # LOCATION
    'B-OG', 'I-OG', # ORGANIZATION
    'B-PS', 'I-PS', # PERSON
    'B-QT', 'I-QT', # QUANTITY
    'B-TI', 'I-TI', # TIME
    'O',            # OUTSIDE
]

KMOU_CATEGORY = [
    'PER', # PERSON : 인명
    'ORG', # ORGANIZATION : 조직
    'LOC', # LOCATION : 장소/위치
    'POH', # 기타 고유명사(제품/약품명, 경기/행사/사건, 영화/노래/드라마 제목, TV채널/잡지, 이메일/전화번호)
    'DAT', # DATE : 날짜
    'TIM', # TIME : 시간
    'DUR', # DURATION : 기간
    'MNY', # MONEY : 금액
    'PNT', # RATE : 비율
    'NOH', # 기타 숫자표현(단위 + 나이/면적/거리/속도/온도/부피/무게/에너지 등의 양/정도)
]