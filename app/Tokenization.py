import os
import nltk

# =========================================================
# [apps.py 에서 가져온 요소]
# - RegexpTokenizer: 규칙 기반 토큰화
# - 이 버전에서는 apps.py 규칙을 "최종 토큰 입력"으로 사용
# =========================================================
from nltk.tokenize import RegexpTokenizer
from nltk.tag import pos_tag

# =========================================================
# [appH.py 에서 가져온 요소]
# - ne_chunk: 개체명 인식
# - Tree: 개체명 chunk 판별
# =========================================================
from nltk import ne_chunk
from nltk.tree import Tree


# =========================================================
# [appj.py 에서 가져온 핵심 규칙]
# - 명사 태그 기준
# =========================================================
NOUN_TAGS = {"NN", "NNS", "NNP", "NNPS"}


# =========================================================
# [appH.py 에서 가져온 개체명 라벨 한글화]
# - PERSON / GPE / LOCATION 등을 사람이 보기 쉽게 변환
# =========================================================
NE_KOREAN = {
    'PERSON'       : '인물',
    'ORGANIZATION' : '기관/단체',
    'GPE'          : '지명(국가/도시)',
    'LOCATION'     : '장소',
    'FACILITY'     : '시설',
    'GSP'          : '지정학적 장소',
    'DATE'         : '날짜',
    'TIME'         : '시간',
    'MONEY'        : '금액',
    'PERCENT'      : '퍼센트',
    'CARDINAL'     : '숫자',
    'ORDINAL'      : '순서',
}


# =========================================================
# [apps.py / appH.py 에 흩어져 있던 nltk 다운로드 통합]
# =========================================================
REQUIRED_NLTK_RESOURCES = [
    "punkt",
    "punkt_tab",
    "averaged_perceptron_tagger",
    "averaged_perceptron_tagger_eng",
    "maxent_ne_chunker",
    "maxent_ne_chunker_tab",
    "words",
]


# =========================================================
# [공통 유틸] nltk 리소스 다운로드
# =========================================================
def download_nltk_resources():
    for resource in REQUIRED_NLTK_RESOURCES:
        nltk.download(resource, quiet=True)


# =========================================================
# [공통 유틸] 작업 폴더 생성
# - apps.py / appj.py / appH.py 중복 제거
# =========================================================
def set_folder():
    folder_path = r"C:\Users\hi\Desktop\harry\Harry_Potter\data"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print("폴더를 생성했습니다.")
    else:
        print("폴더가 이미 존재합니다.")

    return folder_path


# =========================================================
# [공통 유틸] 원문 파일 읽기
# =========================================================
def load_text(file_path):
    with open(file_path, "r", encoding="UTF-8") as file:
        return file.read()


# =========================================================
# [apps.py 규칙 토큰화]
#
# 목적:
# - 호칭 + 이름 묶기
# - 소유격 패턴 유지
# - 대문자 연속 이름 패턴 유지
#
# 주의:
# - 여기서 묶인 토큰은 "토큰화 품질 향상" 목적
# - 하지만 최종 출력은 단어 단위로 다시 풀어서 사용
#   (빈도 분석 / 인코딩을 위해 단어 단위가 더 적절하기 때문)
# =========================================================
def tokenize_with_rules(text):
    titles = r"(?:Mr\.|Mrs\.|Ms\.|Dr\.|Prof\.|Professor|Miss|Sir|Lord)"

    pattern = (
        rf"{titles}\s+and\s+{titles}\s+[A-Z][a-z]+"
        rf"|{titles}\s+[A-Z][a-z]+"
        rf"|[A-Z][a-z]+\'s\s+[a-z]+"
        rf"|[A-Z][a-z]+\s+[A-Z][a-z]+"
        rf"|[A-Z][a-z]+"
        rf"|[A-Za-z]+(?:-[A-Za-z]+)?"
    )

    tokenizer = RegexpTokenizer(pattern)
    return tokenizer.tokenize(text)


# =========================================================
# [통합 보정]
# - apps.py 규칙 토큰화 결과를 최종 분석용 "단어 단위"로 다시 분해
#
# 예:
# - "Harry Potter" -> ["Harry", "Potter"]
# - "Mr. Dursley" -> ["Mr.", "Dursley"]
# - "Harry's wand" -> ["Harry's", "wand"]
#
# 이유:
# - 최종 목표가 명사 단어 빈도 분석 + 인코딩이기 때문
# - 따라서 최종 저장 단위는 "구"가 아니라 "단어"여야 함
# =========================================================
def flatten_rule_tokens(rule_tokens):
    final_tokens = []

    for token in rule_tokens:
        parts = token.split()
        final_tokens.extend(parts)

    return final_tokens


# =========================================================
# [공통] 품사 태깅
# =========================================================
def tag_tokens(tokens):
    return pos_tag(tokens)


# =========================================================
# [appj.py 규칙]
# - 명사만 남기기 위한 기본 조건
# =========================================================
def is_valid_noun(word, tag):
    cleaned = word.replace(".", "").replace("'", "").replace("-", "")

    return (
        tag in NOUN_TAGS
        and len(cleaned) > 1
        and any(ch.isalpha() for ch in cleaned)
    )


# =========================================================
# [appj.py 규칙]
# - 복수형 대문자 명사 후보 표시
#
# 예:
# - Potters
# - Gryffindors
# - Dursleys
#
# 주의:
# - 하드코딩 family/group 분류는 하지 않음
# - Step 1에서는 후보 라벨만 붙임
# =========================================================
def is_plural_capitalized_noun(word, tag):
    cleaned = word.replace(".", "").replace("'", "").replace("-", "").replace(" ", "")

    return (
        tag in NOUN_TAGS
        and len(cleaned) > 1
        and cleaned[0].isupper()
        and cleaned.endswith("s")
        and cleaned.isalpha()
    )


# =========================================================
# [appH.py 규칙]
# - ne_chunk 결과를 "단어 -> 개체명 라벨" 형태로 변환
#
# 기존 문제:
# - 이전 버전은 "Harry Potter (인물)"처럼 구 단위로 묶여서
#   최종 토큰 단위가 흔들렸음
#
# 수정 방식:
# - 이제는 개체명 구를 최종 토큰으로 쓰지 않고
# - 구 안에 포함된 각 단어에 같은 라벨을 부여
#
# 예:
# "Harry Potter" -> {"Harry": "PERSON", "Potter": "PERSON"}
# =========================================================
def build_entity_token_map(tagged_tokens):
    chunked = ne_chunk(tagged_tokens)
    entity_token_map = {}

    for subtree in chunked:
        if isinstance(subtree, Tree):
            entity_label = NE_KOREAN.get(subtree.label(), subtree.label())

            for word, tag in subtree:
                if is_valid_noun(word, tag):
                    entity_token_map[word] = entity_label

    return entity_token_map


# =========================================================
# [통합 핵심]
#
# apps.py + appj.py + appH.py 규칙을 모두 적용해서
# "단어 단위 최종 결과"를 생성
#
# 최종 결과 구조:
# {
#   "token": "Harry",
#   "tag": "NNP",
#   "rule_label": "",
#   "entity_label": "PERSON"
# }
#
# 원칙:
# - token은 무조건 단어 단위
# - rule_label, entity_label은 부가 정보
# =========================================================
def build_final_tokenization_result(text):
    # -----------------------------------------------------
    # 1) apps.py 규칙 토큰화 적용
    # -----------------------------------------------------
    rule_tokens = tokenize_with_rules(text)

    # -----------------------------------------------------
    # 2) 최종 분석 단위는 단어여야 하므로 다시 단어 단위로 분해
    # -----------------------------------------------------
    final_tokens = flatten_rule_tokens(rule_tokens)

    # -----------------------------------------------------
    # 3) 품사 태깅
    # -----------------------------------------------------
    tagged_tokens = tag_tokens(final_tokens)

    # -----------------------------------------------------
    # 4) appH.py 개체명 규칙 적용
    # - 단어별 entity label 맵 생성
    # -----------------------------------------------------
    entity_token_map = build_entity_token_map(tagged_tokens)

    results = []

    # -----------------------------------------------------
    # 5) appj.py 명사 추출 규칙 적용
    # - 명사만 남김
    # - rule_label / entity_label 분리 저장
    # -----------------------------------------------------
    for word, tag in tagged_tokens:
        if not is_valid_noun(word, tag):
            continue

        rule_label = ""
        entity_label = ""

        # appj 규칙: 복수 대문자 명사 후보
        if is_plural_capitalized_noun(word, tag):
            rule_label = "PLURAL_ENTITY"

        # appH 규칙: 개체명 라벨
        if word in entity_token_map:
            entity_label = entity_token_map[word]

        results.append({
            "token": word,
            "tag": tag,
            "rule_label": rule_label,
            "entity_label": entity_label
        })

    return results


# =========================================================
# [최종 저장]
# - txt 하나로 저장
# - 최종 목적에 맞게 "단어 단위" 형식으로 출력
#
# 출력 형식:
# 1. token    tag    rule_label    entity_label
# =========================================================
def save_result_txt(output_path, results):
    with open(output_path, "w", encoding="UTF-8") as out_file:
        out_file.write("STEP 1. TOKENIZATION FINAL RESULT\n")
        out_file.write("=================================\n\n")
        out_file.write("index\ttoken\ttag\trule_label\tentity_label\n")

        for idx, item in enumerate(results, start=1):
            out_file.write(
                f"{idx}\t"
                f"{item['token']}\t"
                f"{item['tag']}\t"
                f"{item['rule_label']}\t"
                f"{item['entity_label']}\n"
            )


# =========================================================
# [main]
# - apps.py + appj.py + appH.py 규칙을 모두 적용
# - 결과는 txt 하나만 저장
# =========================================================
def main():
    download_nltk_resources()

    base_path = set_folder()
    file_path = os.path.join(base_path, "Book1.txt")
    output_path = os.path.join(base_path, "Tokenization_Result.txt")

    try:
        text = load_text(file_path)

        # 통합 규칙 적용 최종 결과
        final_results = build_final_tokenization_result(text)

        # txt 하나로 저장
        save_result_txt(output_path, final_results)

        print(f"최종 통합 토큰화 결과 저장 완료: {output_path}")

    except FileNotFoundError:
        print("파일 찾기 실패")


if __name__ == "__main__":
    main()