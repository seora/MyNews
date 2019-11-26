import json

fname = 'News_Category_Dataset_v2.json'

data = []
with open(fname) as st_json:
    for line in st_json:
        data.append(json.loads(line))

# 카테고리 리스트
category_list = []
for i in range(len(data)):
    category_list.append(data[i]['category'])
    category_list = list(set(category_list))

news_list = []
for category in category_list:
    con_cg_list = []
    con_data_list = []

    for con_data in data:
        con_data_list.append(con_data)

    news_generator = (item for item in con_data_list if item['category'] == category)

    num = 0;
    for news_item in news_generator:
        con_cg_list.append(news_item)
        num += 1

        news_list.append(news_item)
        if (num == 500): break
    # print(category, " done")
# print(news_list)

with open('News_list.json', 'w') as fout:
    json.dump(news_list, fout, indent="\t")

