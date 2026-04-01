import os
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

def setFolder():
    folder_path = r"C:\Users\hi\Desktop\harry\Harry_Potter\data"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print("폴더를 생성했습니다.")
    else:
        print("폴더가 이미 존재합니다.")
    return folder_path


def apply_rules(prev_word, word, tag):
    # Potter Family
    if prev_word is not None and prev_word.lower() == "the" and word == "Potters":
        return "Potter_Family"

    # Gryffindor Group
    group_prev_words = {"the", "first-year", "other", "new"}

    if prev_word is not None and prev_word.lower() in group_prev_words and word == "Gryffindors":
        return "Gryffindor_Group"

    return None


base_path = setFolder()
file_path = os.path.join(base_path, "Book1.txt")

try:
    with open(file_path, "r", encoding="UTF-8") as file:
        text = file.read()

    tokens = word_tokenize(text)
    tagged = pos_tag(tokens)

    output_path = os.path.join(base_path, "rule_family_house_result.txt")

    with open(output_path, "w", encoding="UTF-8") as out_file:
        out_file.write("prev_word\toriginal\ttag\tdisplay\n")

        for i, (word, tag) in enumerate(tagged):
            prev_word = tagged[i - 1][0] if i > 0 else None

            converted_word = apply_rules(prev_word, word, tag)

            if converted_word is not None:
                display_word = f"{word} ({converted_word})"
            else:
                display_word = word

            out_file.write(f"{prev_word}\t{word}\t{tag}\t{display_word}\n")

    print(f"💾 분석 결과가 저장되었습니다: {output_path}")

except FileNotFoundError:
    print("파일 찾기 실패")