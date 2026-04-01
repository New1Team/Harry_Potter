# 폴더 생성 후 파일 업로드
import os
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

def setFolder():
  folder_path = r"C:\Users\hi\Desktop\Sooah\Team\Harry_Potter\data"
  if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print("폴더를 생성했습니다.")
  else:
    print("폴더가 이미 존재합니다.")
  # return folder_path

  base_path = setFolder()
  file_path = os.path.join(base_path, 'Book1.txt')
  try:
      if folder_path:
        with open('data\Book1.txt', 'r', encoding='UTF-8') as file:
            text = file.read()
        tokens = word_tokenize(text)
        tagged = pos_tag(tokens)
        output_path = os.path.join(base_path, 'Analysis_Result.txt')
        with open(output_path, 'w', encoding='UTF-8') as out_file:
            out_file.write(str(tagged))
        print(f"💾 분석 결과가 저장되었습니다: {output_path}")
  except FileNotFoundError:
    print("파일 찾기 실패")