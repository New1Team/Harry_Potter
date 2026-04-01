# 폴더 생성 후 파일 업로드
import os
import nltk  
from nltk.tokenize import word_tokenize 
from nltk import ne_chunk
from nltk.tag import pos_tag
from nltk.tree import Tree
import csv 

required = [
    'maxent_ne_chunker_tab',
    'maxent_ne_chunker',
    'words',
    'punkt',
    'punkt_tab',
    'averaged_perceptron_tagger',
    'averaged_perceptron_tagger_eng'
]

for resource in required:
    nltk.download(resource, quiet=True)

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



def setFolder():
  folder_path = r"C:\Users\hi\Desktop\Sooah\Team\Harry_Potter\data"
  if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print("폴더를 생성했습니다.")
  else:
    print("폴더가 이미 존재합니다.")
  return folder_path

base_path = setFolder()
file_path = os.path.join(base_path, 'Book1.txt')
try:
    with open('data\Book1.txt', 'r', encoding='UTF-8') as file:
        text = file.read()
    tokens = word_tokenize(text)
    tagged = pos_tag(tokens)
    chunked = ne_chunk(tagged)
    result = []
    for subtree in chunked:
       if isinstance(subtree, Tree):
          # 묶인 개체명 (Harry Potter 등)
          entity = " ".join(word for word, tag in subtree)
          label = NE_KOREAN.get(subtree.label(), subtree.label())
          result.append((entity, label))
       else:
         word, tag = subtree
         # ✅ 명사 태그만 + 알파벳으로만 이루어진 단어만 (a, the, "" 제거)
         if tag in ['NN','NNS','NNP','NNPS'] and word.isalpha() and len(word) > 1 :
          result.append((word,'일반명사'))
    # NN(명사), NNS(복수명사), NNP(고유명사), NNPS(복수고유명사) 만 추출
    nouns = [word for word, tag in tagged if tag in ['NN', 'NNS', 'NNP', 'NNPS']]

    print(nouns)
    # ['Harry', 'Potter', 'student', 'Hogwarts', 'School', 'Witchcraft']
    print(chunked)
    

    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(current_dir, 'Analysis_Result_Hayoung.csv')
    with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['명사', '분류'])   # 헤더
        writer.writerows(result)

    with open('토큰.csv', 'w', encoding='utf-8-sig', newline='') as f:
     writer = csv.writer(f)
     writer.writerow(['token'])        # 헤더
     for token in tokens:
        writer.writerow([token])

except FileNotFoundError:
   print("파일 찾기 실패")