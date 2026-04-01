import os
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

NOUN_TAGS = {"NN", "NNS", "NNP", "NNPS"}

def setFolder():
    folder_path = r"C:\Users\hi\Desktop\harry\Harry_Potter\data"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path

def is_plural_capitalized_noun(word, tag):
    if not word:
        return False
    if tag not in NOUN_TAGS:
        return False
    if not word[0].isupper():
        return False
    if not word.endswith("s"):
        return False
    if not word.replace("-", "").isalpha():
        return False
    return True

def apply_rules(prev_word, word, tag):
    # 복수 대문자 명사 후보만 추출
    if is_plural_capitalized_noun(word, tag):
        return "PLURAL_ENTITY"
    return None

base_path = setFolder()
file_path = os.path.join(base_path, "Book1.txt")
output_path = os.path.join(base_path, "noun_result.txt")

try:
    with open(file_path, "r", encoding="UTF-8") as file:
        text = file.read()

    tokens = word_tokenize(text)
    tagged = pos_tag(tokens)

    with open(output_path, "w", encoding="UTF-8") as out_file:
        idx = 1

        for i, (word, tag) in enumerate(tagged):
            if tag not in NOUN_TAGS:
                continue

            prev_word = tagged[i - 1][0] if i > 0 else None
            category = apply_rules(prev_word, word, tag)

            if category is not None:
                display_word = f"{word} ({category})"
            else:
                display_word = word

            out_file.write(f"{idx}. {display_word}\n")
            idx += 1

    print(f"저장 완료: {output_path}")

except FileNotFoundError:
    print("파일 찾기 실패")