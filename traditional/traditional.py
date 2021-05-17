import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from typing import List
from itertools import permutations
data = pd.read_excel("../data/1.xlsx")

class member:
    def __init__(self, 
                mid, total_day, past_day, driver, accident_times, 
                A_times, B_times, C_times, D_times):
        self.mid = mid
        self.total_day = total_day
        self.past_day = past_day
        self.driver = driver
        self.accident_times = accident_times
        self.A_times = A_times
        self.B_times = B_times
        self.C_times = C_times
        self.D_times = D_times
        self.fair_ratio = 0
        self.exprience = (A_times or B_times or C_times or D_times)
    
    # calculate fair_ratio
    def cal_fair_ratio(self):
        self.fair_ratio = (self.A_times + self.B_times + self.C_times + self.D_times) / self.past_day
        if(self.past_day < 0):
            self.fair_ratio += 2
    # override < operator to sort 
    def __lt__(self, other):
        return self.fair_ratio < other.fair_ratio



member_list = []

for i in range(data.shape[0]):
    new_member = member(
        data.loc[:,"编号"][i], 
        data.loc[:,"工作天数"][i],
        data.loc[:,"已工作天数"][i],
        data.loc[:,"驾驶资格"][i],
        data.loc[:,"历史事故"][i],
        data.loc[:,"已安排A"][i],
        data.loc[:,"已安排B"][i],
        data.loc[:,"已安排C"][i],
        data.loc[:,"已安排D"][i]
    )
    new_member.cal_fair_ratio()
    member_list.append(new_member)

member_list = sorted(member_list)

# caculate amount of member who is in the company already
active_member_num = len([each.past_day for each in member_list if each.past_day >= 0])

# caculate the work number base on the amount of active member x
def calculate_work_num(x):
    if(x <= 7 ):
        return 1
    elif(x <= 10):
        return 2
    elif(x<= 12):
        return 3
    elif(x <= 15):
        return 4
# caculate the amount of work 
work_num = calculate_work_num(active_member_num)

alternative_list = []

# get all alternative member as list from all memeber list arr and work number total_num
def get_alternative(arr:List[member], total_num:int):
    cur_driver = 0
    cur_total = 0
    max_fair_ratio = 0.0
    res_list = []
    for each in arr:
        if(each.driver):
            cur_driver += 1
        cur_total += 1
        res_list.append(each)
        if(cur_driver >= total_num and cur_total >= 2*total_num):
            max_fair_ratio = each.fair_ratio
            break
    # get all alternative which meet the hard condition
        
    if(cur_driver < total_num or cur_total < 2*total_num):
        return []
    # cannot satisfy the hard condition

    for each in arr:
        if(each not in res_list):
            if(each.fair_ratio <= max_fair_ratio + 0.1):
                res_list.append(each)
    return res_list

alternative_list = get_alternative(member_list, work_num)

# arr is a possible_solution a total_num is work number
def cal_optimize_ratio(arr:List[member], total_num:int):
    opt_ratio = 0.3
    # soft condition 1
    for i in range(total_num):
        if(not arr[i*2].exprience and not arr[i*2+1].exprience):
            opt_ratio -= 0.3
            break
    
    # soft condition 3
    opt_ratio += 0.1
    for i in range(total_num):
        if(max(arr[i*2].accident_times, arr[i*2+1].accident_times) > 3):
            if(min(arr[i*2].accident_times, arr[i*2+1].accident_times) > 1 ):
                opt_ratio -= 0.1
                break
    
    # soft condition 2
    def cal_member_work_avg(mem:member, type:int):
        A_times = mem.A_times + (type == 1)
        B_times = mem.B_times + (type == 1)
        C_times = mem.C_times + (type == 1)
        D_times = mem.D_times + (type == 1)

        _tmp_list = []
        _tmp_list.append(A_times)
        if(B_times):
            _tmp_list.append(B_times)
        if(C_times):
            _tmp_list.append(C_times)
        if(D_times):
            _tmp_list.append(D_times)

        return np.std(_tmp_list)

    _condition2_list = []
    for i in range(total_num):
        _condition2_list.append(cal_member_work_avg(arr[i], i))
    opt_ratio += np.mean(_condition2_list)
    # print(opt_ratio)
    return opt_ratio


ans = []
max_ratio = 0.0

for possible_solution in list(permutations(alternative_list, work_num * 2)):
    validator = True
    for i in range(work_num):
        if((not alternative_list[i*2].driver)and (not alternative_list[i*2+1].driver)):
            validator = False
            break
    if(not validator):
        continue
    
    _tmp_ratio = cal_optimize_ratio(possible_solution, work_num)
    if(_tmp_ratio > max_ratio):
        max_ratio = _tmp_ratio
        ans = possible_solution

[print(i.__dict__) for i in ans]
# print(ans)

