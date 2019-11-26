import re

import nltk
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import json

from nltk.corpus import stopwords
from nltk.tokenize import WordPunctTokenizer


fname = 'News_list.json'


data = []
with open(fname, 'r') as f:
    data = json.load(f)

for i in range(len(data)):
    index = i
    url = data[i]['link']

    #request를 통해 파싱한 html 문서를 beautifulsoup 객체로 데이터 추출
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = requests.get(url, headers = headers)
    soup = bs(req.content, 'html.parser')

    news_data = []

    for link in soup.find_all('p'):
        news_data.append(link.text.strip())

    #print(news_data)

    news_description = ", ".join(news_data)


    news_description = news_description.lower()
    news_description = news_description.replace(",", "")


    # 불용어, 특수문자 제거
    shortword = re.compile(r'\W*\b\w{1,2}\b')
    news_description = shortword.sub('', news_description)
    news_description = re.sub('[!@#$%^&*,('')"/<>?.=]', '', news_description)
    news_description = news_description.replace("]", "")
    news_description = news_description.replace("[", "")
    news_description = news_description.replace("-", "")
    news_description = news_description.replace("_", "")
    stop = stopwords.words('english')

    news_token = nltk.wordpunct_tokenize(news_description)
    news_token = [word for word in news_token if not word in stop]

    # 동사의 원형복원(lemmatizing)
    lm = nltk.WordNetLemmatizer()
    lm_tokens = [lm.lemmatize(w, pos="v") for w in news_token]

    # 품사 구분하여 고유명사, 명사, 동사 출력
    tagged_list = nltk.pos_tag(lm_tokens)
    pnouns_tokens = [t[0] for t in tagged_list if t[1] == "NNP"]
    nouns_tokens = [t[0] for t in tagged_list if t[1] == "NN"]
    verb_tokens = [t[0] for t in tagged_list if t[1] == "VB"]

    # 분류된 단어들을 합치기
    news_token_list = pnouns_tokens + nouns_tokens + verb_tokens

    print(news_token_list)









