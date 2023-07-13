from utilities.helper import LLMHelper
import numpy as np
import pandas as pd
import datetime
import hashlib
import ast

def _sell_date(dates):
    from dateutil.parser import parse

    start = parse(dates[0]).strftime("%Y년 %m월 %d일")

def _candidate_date(dates):
    from dateutil.parser import parse
    
    ret = []
    for sd, ed in dates:
        sd = parse(sd).strftime("%Y년 %m월 %d일")
        if ed.isdigit():
            ed = parse(ed).strftime("%Y년 %m월 %d일")
        ret.append(sd + " ~ " + ed)

    return ", ".join(ret)

def _candidate_insurance(insurances):
    return ", ".join(insurances)

def get_hashkey_insurance_date(insurance_name, insurance_date):

    def get_tags(name):
        cond_tag = ['단체','변액','보장','실손','암','연금']
        ret = []
        for tag in cond_tag:
            if tag in name:
                ret.append(tag)
        return ret
            
    search_tags = get_tags(insurance_name)
    similar_insurance = llm_helper.vector_store.similarity_search_with_score_insurance(insurance_name, "*", search_tags=search_tags, index_name="insurance-index", k=4)
    # print("QQ",similar_insurance)
    best_insurance = similar_insurance.docs[0]
    
    date_list = ast.literal_eval(best_insurance.date)
    
    candidate_date = []
    for date in date_list:
        sd, ed = date.split("-")
        if ed == "99991231":
            ed = "현재"
        candidate_date.append((sd,ed))

    insurance_key = best_insurance.insurance
    date_key = None
    for start, end in candidate_date:
        if start <= insurance_date < end:
            date_key = start
            sell_date = (start, end)
    
    if date_key is None:
        date_key = candidate_date[-1][0]
        sell_date = candidate_date[-1]

    print("TTT")
    print(candidate_date)
    candidate_date.remove(sell_date)
    print(candidate_date)

    search_key = insurance_key + ":" + date_key
    hash_key = hashlib.sha1(search_key.encode('utf-8')).hexdigest()    

    candidate_insurance = [ins.insurance for ins in similar_insurance.docs[1:]]        

    candidate_date = _candidate_date(candidate_date)
    candidate_insurance = _candidate_insurance(candidate_insurance)


    return hash_key, insurance_key, sell_date, candidate_date, candidate_insurance


llm_helper = LLMHelper()

# 100개 뽑아놓은 데이터 넣어서 테스트 해보기.
# form recognizer 되는지 >> 코드.
# 변환 규칙 만들기 (100개 보면서 생각.)
# 1. 보험 떼기
# 2. III > 3 (보험 뒤에 있는 숫자만.)
# 3. 단체는 무조건 단체만 찾게.

# '교보장'이 아닌 '보장'만 

# 22222222222222222 데이터 찾기
insurance_name = "개인 연금보험"
dday = "19970201"
insurance_name = insurance_name.replace("보험", "")

print(insurance_name)

hash_key, insurance_key, sell_date, candidate_date, candidate_insurance = get_hashkey_insurance_date(insurance_name, dday)

print("입력 ins :",insurance_name) 
print("입력 date :", dday) 
print("매칭 ins :", insurance_key)
print("매칭 date :", sell_date)
print("후보 ins :",candidate_insurance)
print("후보 date :",candidate_date)
exit()


# FT.SEARCH idx:schools "@type:{forest} @type:{montessori}"
# FT.SEARCH idx:schools "@type:{forest|democratic}"

# 1111111111111 데이터 넣기

data = pd.read_excel("보험정보_검색태그.xlsx", sheet_name='Sheet1')

# 실제 데이터
insurances = data['보험상품명'].tolist()
tags = data['검색태그'].tolist()

start_dates = data['적용시작일자'].tolist()
end_dates = data['적용종료일자'].tolist()

start_dates = [str(sd) for sd in start_dates]
end_dates = [str(ed) for ed in end_dates]
dates = [sd+"-"+ed for sd, ed in zip(start_dates, end_dates)]

## test용
# insurances = list(set(data['보험상품명'].tolist()))
# dates = ['20230601'] * len(insurances)

# exit()
# print(len(dates))

for i, d, t in zip(insurances, dates, tags):
    t = eval(t)
    d = str(d)
    # tag = ";".join(t)
    tag = ", ".join(t) 
    print(tag)
    print(d)
    llm_helper.vector_store.add_insurance_info(i, d, tag)



