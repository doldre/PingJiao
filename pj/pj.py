#coding:utf-8
import sys
import getpass
import requests
from bs4 import BeautifulSoup

def pj(params, cookies):
    jxpgurl = "http://zhjw.scu.edu.cn/jxpgXsAction.do"
    request_result = requests.post(jxpgurl, params, cookies = cookies)
    bsObj_in = BeautifulSoup(request_result.text, "html.parser")
    item_list = bsObj_in.findAll("input", {"type" : "radio"})

    params_post = dict()
    for item in item_list:
        radio_name = item.attrs["name"]
        if radio_name not in params_post.keys():
            params_post[radio_name] = item.attrs["value"]

    params_post["zgpj"] = "good"
    params_post["wjbm"] = params["wjbm"]
    params_post["bpr"] = params["bpr"]
    params_post["pgnr"] = params["pgnr"]
    requests.post(jxpgurl + "?oper=wjpg", params_post, cookies = cookies)

def get_class_list(cookies):
    jxpgurl = "http://zhjw.scu.edu.cn/jxpgXsAction.do"
    request_result = requests.get(jxpgurl + "?oper=listWj&pageSize=300", cookies = cookies)
    bsObj = BeautifulSoup(request_result.text, "html.parser")
    bs_class_list = bsObj.findAll("img", { "src" : "/img/icon/edit.gif" })

    result = []
    for item in bs_class_list:
        params = dict()
        str_list = item.attrs['name'].split("#@")
        params['wjbm']  = str_list[0]
        params['bpr']   = str_list[1]
        params['bprm']  = str_list[2]
        params['wjmc']  = str_list[3]
        params['pgnrm'] = str_list[4]
        params['pgnr']  = str_list[5]
        params["oper"]  = "wjShow"
        result.append(params)
    return result

def login(zjh, mm):
    login_url = "http://zhjw.scu.edu.cn/loginAction.do"
    return requests.post(login_url, { 'zjh' : zjh, 'mm' : mm })  

def teach_evaluate(zjh, mm):
    login_identify = login(zjh, mm)
    class_list = get_class_list(login_identify.cookies)

    msg = []
    for item in class_list:
        pj(item, login_identify.cookies)
        msg.append(item['bprm'] + "-" + item['pgnrm'] + ": 评教成功")
    if msg == []:
        msg.append("评教失败")
    return msg

if __name__ == "__main__":
    zjh = input("please input your username: ")
    mm = getpass.getpass("please input your password: ")
    msg = teach_evaluate(zjh, mm)
    tips = "Message: \n"
    for m in msg:
        tips = tips + m + '\n'
    print("%sPress any key to continue." % tips)
    input()
