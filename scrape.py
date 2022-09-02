"""
data-hook="cr-filter-info-review-rating-count" "12,620 total ratings, 1,893 with reviews"


"""
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
import time
import datetime

from db import *

asin = "B09G77DR7C"
link = "https://www.amazon.co.uk/product-reviews/{}/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber={}"


def get_soup_ret(url: str):
    ua = UserAgent()
    uag_random = ua.random

    header = {
        'User-Agent': uag_random,
        'Accept-Language': 'en-US,en;q=0.9'
    }
    isCaptcha = True
    while isCaptcha:
        page = requests.get(url, headers=header)
        assert page.status_code == 200
        soup = BeautifulSoup(page.content, 'lxml')
        if 'captcha' in str(soup):
            uag_random = ua.random
            # print(f'\rBot has been detected... retrying ... use new identity: {uag_random} ', end='', flush=True)
            logger.info(f'\rBot has been detected... retrying ... use new identity: {uag_random} ')
            continue
        else:
            logger.info('Bot bypassed')
            return soup

def get_soup(url: str, header_alt: dict = None):
    # print(url)
    # logger.info(url)
    ua = UserAgent()
    uag_random = ua.random

    HEADERS = {
        'User-Agent': uag_random,
        'Accept-Language': 'en-US,en;q=0.9'
    }

    if header_alt:
        HEADERS.update(header_alt)
    # with requests.Session as s:
    s = requests.Session()
    try:
        # r = s.get(url, headers=HEADERS)
        # s.close()
        # return BeautifulSoup(r.text, 'html.parser')

        isCaptcha = True
        while isCaptcha:
            page = s.get(url, headers=HEADERS)
            assert page.status_code == 200
            soup = BeautifulSoup(page.content, 'html.parser')

            review_name = soup.find('a', {'data-hook': 'product-link'})
            if review_name == None:
                print("bot review detected")
                HEADERS.update({'User-Agent':ua.random})
                continue
            elif 'captcha' in str(soup):
                HEADERS.update({'User-Agent':ua.random})
                print(f'\rBot has been detected... retrying ... use new identity: {uag_random} ', end='', flush=True)
                continue
            else:
                print(review_name)
                return soup
            #
            # else:
            #     print('Bot bypassed')
            #     return soup

    except:
        s.close()
        return None


"""
{
    "overall": 2.0,
    "verified": false,
    "reviewTime": "12 5, 2015",
    "reviewerID": "A3KUPJ396OQF78",
    "asin": "B017O9P72A",
    "reviewerName": "Larry Russlin",
    "reviewText": "Can only control one of two bulbs from one of two echos",
    "summary": "Buggy",
    "unixReviewTime": 1449273600
}
"""

def check_soup(soup):
    if not soup:
        print("soup was not seen")
        return None
    # print(soup)
    review_name = soup.find('a', {'data-hook': 'product-link'})
    if review_name == None:
        print(soup)
        return None
    else:
        print(review_name)
        return True

def total_num_of_reviews(soup: BeautifulSoup):

    if not soup:
        print("soup was not seen")
        return None
    print()
    review_num = soup.find('div', {'data-hook': 'cr-filter-info-review-rating-count'})
    print(review_num)
    if not review_num:
        return None
    rev_str = review_num.text.replace("\n", "").split()
    # print("hello this is review:",review_num.text.replace("\n","").split())
    num = 0
    num_of_review = ""
    for i in rev_str:
        j = i.replace(",", "").isnumeric()
        # print(j)
        if j:
            num += 1
            if num == 2:
                num_of_review = int(i.replace(",", ""))
                break
        else:
            continue
    return num_of_review
    # print(num_of_review)


def get_name_rating(index1: str) -> tuple[str, float]:
    name = ""
    rating = 0.0
    splited_index = index1.split(".")
    # print(index1)
    # this is for getting rating
    j = 1
    r = ""
    for i in reversed(str(index1)):
        if i.isnumeric():
            # print(i)
            if j < 3:
                j += 1
            elif j == 3:
                r = i

    if len(splited_index) > 2:
        first_index = splited_index[0] + splited_index[1]

        # rating = first_index[-1] + ".0"
        name = "".join(first_index[0: -1])
    else:
        name = "".join(splited_index[0][0: -1])
        # rating = splited_index[0][-1] + ".0"

    rating = r + ".0"
    return (name, float(rating))


def get_date(date_str: str) -> tuple[str, int]:
    date = ""
    v = 0
    month_dict = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12,
    }
    for i in date_str:
        if v == 0 and i.isnumeric():
            date += i
            v = 1
        elif v == 1 and i == "2":
            date += i
            v += 1
        elif v == 2:
            date += i
            v += 1
        elif v == 3:
            date += i
            v += 1
        elif v == 4:
            date += i
            break
        elif v == 1:
            date += i
    # print(date)
    # logger.info(date)
    splited_date = date.split()
    if len(splited_date) < 3:
        return (None, 0)
    # print(splited_date)
    day = int(splited_date[0])

    month = month_dict.get(str(splited_date[1]), 0)
    year = int(splited_date[2])

    date_in_str = str(month) if len(str(month)) == 2 else "0" + str(month)
    date_in_str += " " + str(day) + ", "
    date_in_str += str(year)
    # print(date_in_str)

    s = "01/12/2011"
    format_change = str(day) + "/" + str(month) + "/" + str(year)
    date_in_unix = time.mktime(datetime.datetime.strptime(s, "%d/%m/%Y").timetuple())

    return (date_in_str, int(date_in_unix))


def get_reviews(soup: BeautifulSoup, asin: str, index_start: int):
    prod_update = []

    if soup == None:
        return []

    reviews = soup.find_all('div', {'data-hook': 'review'})
    if reviews == []:
        print("soup was none")
        # logger.info("soup was none")
        return []
    schema = {
        "overall": 0.0,
        "reviewTime": "1 1, 2000",
        "vote": "0",
        "verified": False,
        "reviewerID": "",
        "asin": "",
        "reviewerName": "",
        "reviewText": "",
        "summary": "",
        "unixReviewTime": 0
    }

    j = 0
    for i in reviews:
        # print(i)
        if index_start == 0:
            pass
        elif j < index_start:
            j += 1
            continue
        dic = schema.copy()

        list_review_str = i.text.split("\n")
        # print(list_review_str)
        date_func = get_date(list_review_str[2])

        # print(i.find_all('span', {'data-hook': 'avp-badge'})[0].text)
        v = i.find('span', {'data-hook': 'avp-badge'})
        if v:
            dic["verified"] = True if v.text == "Verified Purchase" else False
        else:
            dic["verified"] = False

        more_info = i.find('a', {'data-hook': 'format-strip'})
        if more_info:
            # print(str(more_info))

            key = ""
            value = ""
            num1 = 0
            for j in str(more_info):
                # print(j)
                if j == ">" and num1 < 1:
                    num1 = 1
                    # print("i entered1")
                elif j == ":" and num1 == 1:
                    num1 = 2
                    # print("i entered3")
                elif j == "<" and num1 == 2:
                    # print("i entered5")
                    dic[key.strip("</i>")] = value
                    # print(key.strip("</i>"), ":",value)
                    key = ""
                    value = ""
                    num1 = 0
                elif num1 == 1:
                    key += j
                    # print(key)
                elif num1 == 2:
                    value += j
                    # print(value)
                    # print("i entered4")

        vote = i.find('span', {'data-hook': 'helpful-vote-statement'})
        if vote:
            if len(vote.text) > 1:
                vo = vote.text.split()
                # print(vote.text)
                try:
                    dic["vote"] = int(vo[0])
                except:
                    pass

        dic["image"] = i.img["src"] if i.img["src"] else ""
        dic["reviewerID"] = i.div["id"].split("-")[0]
        dic["summary"] = list_review_str[1]
        dic["reviewText"] = list_review_str[3]
        nr = get_name_rating(list_review_str[0])
        dic["reviewerName"] = nr[0]
        dic["overall"] = nr[1]
        dic["asin"] = asin
        dic["reviewTime"] = date_func[0]
        dic["unixReviewTime"] = date_func[1]

        print("\n\n\n", dic, "\n\n\n")
        # logger.info("\n\n\n", str(dic), "\n\n\n")
        prod_update.append(dic)
    # if prod_update != []:
    review_col.insert_many(prod_update)

    return prod_update


def scrape_master(asin, page, index):
    scrape_state = 0
    while True:
        #print(scrape_state)
        if scrape_state == 0:
            get_reviews(get_soup(link.format(asin, page)), asin, index)
        else:

            page += 1
            g = get_reviews(get_soup(link.format(asin, page)), asin, 0)
            # g = get_reviews(get_soup(link.format(asin, page)), asin, 0)
            if g == [] or g is None:
                break

        scrape_state = 1


def entry():
    try:
        stat = status_col.find_one({"_id": 1})
        stat.update({"active": 1})
        status_col.replace_one({"_id": 1}, stat)
        asin_list = stat["asin_list"]
        # logger.info(asin_list)

        stat_counter = 0
        for i in asin_list:
            if stat_counter > 50:
                stat = status_col.find_one({"_id": 1})
                if stat:
                    if stat["active"] == 0:
                        break

            stat_counter += 1
            # logger.info(a_counter)
            total = total_num_of_reviews(get_soup(link.format(i, 1)))
            # logger.info(i)
            # print(i)
            if not total:
                continue
            asin_info = status_col.find_one({"asin": i})
            if not asin_info:
                break
            diff = total - asin_info["total"]
            if diff < 1 or asin_info.get("active") == False:
                continue
            elif diff > 0:
                #print("i happen1")
                off = int(total / 10)
                #print("i happen2")
                # logger.info(str(i) + str(off))
                # print(str(i) + str(off))
                # try:
                page_num = off
                #print("i happen2.5")
                index_start = int(str(asin_info["total"])[-1])
                #print("i happen3")
                scrape_master(i, page_num, index_start)
                #print("i happen4")
                status_col.replace_one({"asin": i}, {"total": total, "active": True, "asin": i})

        #print("i happen5")
        stat.update({"active": 0})
        status_col.replace_one({"_id": 1}, stat)

    except:
        reset_status()

# if __name__ == '__main__':
#     scrape_master("B08C1RR8JM", 1, 0)

