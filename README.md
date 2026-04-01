# Harry_Potter

## 텍스트 전처리를 통한 소설 분석

1) 단어 빈도분석
- 주요단어 > 저빈도단어 > 일회성단어 구분
- 단어 별 카테고리 매칭
    * 카테고리: 등장인물 / 장소 / 마법구문 

## 진행 순서
1. 문장 토큰화
2. 단어 토큰화
2-1. 예외 규칙 수립
    - 호칭/직업 등(Mr, Dr..) 뒤 명사와 한 덩어리로 인식하여 추출하도록 규칙 생성
    - 소유격(Harry's legacy) 뒤 명사와 한 덩어리로 인식하여 추출하도록 규칙 생성


- 가족 대명사(Potters)를 단순 인물 Potter와 구분하도록 규칙 생성
- 단수 / 복수형 구분
해답 :  **복수형 일반 명사 처리 규칙과 고유명사 예외 규칙 분리** -->
분리 방법: 

A1. 사전 기반 예외 규칙

명사별로 명사 사전 만들기
```bash
FAMILY_NAME_EXCEPTIONS = {
    "Potters": "Potter_Family",
    "Weasleys": "Weasley_Family",
    "Dursleys": "Dursley_Family",
    "Malfoys": "Malfoy_Family"
}
```


    - 대명사는 한 덩어리로 인식하도록 규칙 추가(ex) Harry / Potter => Harry Potter)

3. 불용어 및 특수문자 제거


