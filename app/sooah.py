from tensorflow.keras.preprocessing.text import text_to_word_sequence
from nltk.tokenize import word_tokenize, RegexpTokenizer, sent_tokenize
from nltk.tag import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import kss
from konlpy.tag import Okt
from konlpy.tag import Kkma
import argparse
import os
import spacy
import re

# with open('../data/Book1.txt', 'r', encoding='UTF-8') as file:
#   text = file.read()
with open('../results/Book1.txt', 'r', encoding='UTF-8') as file:
  text = file.read()

# 추출물 저장 폴더 생성
def setFolder():
  folder_path = "C:/Users/hi/Desktop/Sooah/Team/Harry_Potter/results"
  if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print("폴더를 생성했습니다.")
  return folder_path

# 추출 후 파일 저장
def saveFile(data_list, folder_path, file_name):
  """
  data_list: 저장할 내용
  folder_path: 폴더 경로
  file_name: 저장할 파일명
  """
  path = os.path.join(folder_path, file_name)
  with open(path, 'w', encoding='UTF-8') as f:
    for i, item in enumerate(data_list, 1):
      f.write(f"{i}: {item}\n")
  print(f"파일 저장 성공: {path}")

# 호칭/직업 구분 및 일반 단어 추출
def Word_Tokenization(text, folder_path):
  """
  영어 단어 토큰화(Word Tokenization) 비교
  규칙 추가
  1) 호칭/직업 + 이름은 한 덩어리로 인식할 것
  2) 그 외의 일반 단어도 함께 추출할 것
  """
  titles = r'(?:Mr\.|Mrs\.|Ms\.|Dr\.|Prof\.|Rev\.|Atty\.|Capt\.|Sir|Lord|Miss)'
  pattern = rf'{titles}\s?[A-Z][a-z]+|\w+'
  # +부분이 일반단어 함께 추출
  tokenizer = RegexpTokenizer(pattern)
  tokens = tokenizer.tokenize(text)
  saveFile(tokens, folder_path, "단어_토큰화.txt")

# Only 호칭/직업 및 대명사 또는 소유격 추출
nlp = spacy.load("en_core_web_sm")

def Upper_Word_Tokenization(text, folder_path):
  """
  영어 단어 토큰화(Upper_Word_Tokenization)
  규칙 추가
  1) 호칭/직업 + 이름은 한 덩어리로 인식할 것: {titles}\s?[A-Z][a-z]
  2) 대문자로 시작하는 단어만 추출할 것: [A-Z][a-z]+
  3) Mr and Mrs. 이름은 한 단어로 묶을 것: {titles}\s?and\s?{titles}\s?[A-Z][a-z]
  4) 소유격을 한 단어로 묶을 것: [A-Z][a-z]+'s\s[a-z]+|[A-Z][a-z]+'s\s[A-Z] (대문자 / 소문자)
  """
  titles = r'(?:Mr\.|Mrs\.|Ms\.|Dr\.|Prof\.|Rev\.|Atty\.|Capt\.|Sir|Lord|Miss)'
  pattern = rf"{titles}\s?and\s?{titles}\s?[A-Z][a-z]+|{titles}\s?[A-Z][a-z]+|[A-Z][a-z]+|[A-Z][a-z]+'s\s[a-z]+|[A-Z][a-z]+'s\s[A-Z]+"
  # +부분이 일반단어 함께 추출
  tokenizer = RegexpTokenizer(pattern)
  tokens = tokenizer.tokenize(text)
  stop_words = set(stopwords.words('english')) 
  result = []
  for word in tokens: 
    if word.lower() not in stop_words: 
      # 표제어 추출 및 불용어 제거
      doc = nlp(word)
      lemma = [token.lemma_ for token in doc]
      final_word = " ".join(lemma).title()
    #   if "And" in final_word:
      final_word = final_word.replace(" .",'.').replace("And",'and')
      if word == 'Rowling':
        final_word = 'Rowling'
      result.append(final_word)
  saveFile(result, folder_path, "복수형제거_규칙_단어_토큰화.txt")
  return result

'''
모델 설치 명령어
uv add spacy
uv add "https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl"
'''


# 규칙_단어_토큰화에서 불용어 삭제
def Stop_Word_Tokenization(token2, folder_path):
  """
  불용어 제거
  규칙 추가 !
  """
  stop_words = set(stopwords.words('english')) 
  result = []
  for word in token2: 
    if word.lower() not in stop_words: 
      result.append(word)
  saveFile(result, folder_path, "규칙_단어_불용어삭제.txt")



# 문장토큰화 불필요한 부분 날림
def Sentence_Tokenization(text, folder_path):
  """
  영어 문장 토큰화(Sentence Tokenization)
  규칙 추가
  1) 줄바꿈 공백은 제거할 것
  2) Page 로 시작하여 J.K. Rowling 로 끝나는 구문 제거하기
  """
  # 2)
  patterns = r"Page\s?\|\s?\d+.*?Rowling"
  text = re.sub(patterns, "", text, flags=re.IGNORECASE | re.DOTALL)
  # 1)
  text = text.replace("\n"," ").replace("\r", " ")
  text = re.sub(r"\s+", " ", text).strip()
  tokens = sent_tokenize(text)
  saveFile(tokens, folder_path, "Book1.txt")

def Speech_Tagging():
  """
  영어 품사 태깅(Part-of-Speech Tagging)
  - 단어의 역할(명사, 동사, 형용사 등)을 정의된 태그로 표시
  """  
  # 먼저 단어 토큰화를 수행
  tokenized_sentence = word_tokenize(text)
  print('단어 토큰화 :', tokenized_sentence)

  # pos_tag: NLTK 제공. PRP(인칭 대명사), VBP(동사), RB(부사) 등의 태그를 붙임
  print('품사 태깅 :', pos_tag(tokenized_sentence))

if __name__ == '__main__':
  # 터미널(CLI)에서 -s 인자를 받아 실행할 단계를 결정
  parser = argparse.ArgumentParser()
  parser.add_argument('-s', type=int, help="실행할 단계 선택 (step1~step5, 미입력 시 step0)")
  

  ## 다 완성시킨 후에는 각각의 savefile 무시하고 한번에 실행시키는 코드로 만들면 될 듯
  try:
    args = parser.parse_args()
    result_dir = setFolder()
    
    # 입력된 step 값에 따라 해당 함수 실행
    if args.s == 1:
      Upper_Word_Tokenization(text, result_dir)
    #   Word_Tokenization(text, result_dir)
    elif args.s == 2:
      Sentence_Tokenization(text, result_dir)
    # elif args.s == 3:
    #   Speech_Tagging()
    # elif args.s == 4:
    #   token2 = Upper_Word_Tokenization(text, result_dir)
    #   Stop_Word_Tokenization(token2,result_dir) 
    # elif args.s == 5:
      
    # else:
      # 기본값 또는 step0 입력 시 실행
      # step0(text, result_dir)
  except SystemExit:
    # argparse 오류 시(잘못된 인자 입력 등) 프로그램 종료 처리
    print("잘못된 인자 입력이 발생했습니다.")
    exit()
