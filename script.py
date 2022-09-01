import json

from db import *
from scrape import total_num_of_reviews, link, get_reviews, get_soup, check_soup
from env import *

link = "https://www.amazon.co.uk/product-reviews/{}/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber={}"

if not data_set:
    js = open("All_Beauty.json", "r")
elif data_set:
    js = open(data_set, "r")

# The code below pushes the dataset to the database

a = 0
j_list = []
for i in js.readlines():

    if a == 200:
        review_col.insert_many(j_list)
        a = 0
        j_list = []

    else:

        res = json.loads(i)
        j_list.append(res)
        a += 1
        # print(a,".", res)

js.close()

# this initiates the flaggin process

a = {
    "_id": 1,
    "active": 0,
    "asin_list": [],
    # "asin_eg": {
    #     "total": 0,
    #     "active": True
    # }
}

d = review_col.distinct("asin")
# print(d)
a["active"] = 0
a["asin_list"] = d
status_col.insert_one(a)
for i in d:

    t = review_col.find({"asin": i})

    print(t.count())
    act = check_soup(get_soup(link.format(i, 1)))
    if act == None:
        act = False
    else:
        act = True


    # a.update({i: })
    status_col.insert_one({"total": t.count(), "active": act, "asin": i})
    # print(a)

# status_col.insert_one(a)


