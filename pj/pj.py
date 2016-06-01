import sys
import getpass
import requests
from bs4 import BeautifulSoup

def teach_evaluate(zjh,mm):
    params_login = dict()
    #zjh = input("please input your username:")
    #mm = getpass.getpass("please input your password:")
    zjh = str(zjh)
    mm = str(mm)
    params_login["zjh"] = zjh
    params_login["mm"] = mm
    r = requests.post("http://zhjw.scu.edu.cn/loginAction.do",params_login)
    #print("Cookie is set to:")
    #print(r.cookies.get_dict())
    #print("-----")
    cook = r.cookies
    jxpgurl = "http://zhjw.scu.edu.cn/jxpgXsAction.do"
    r = requests.get(jxpgurl + "?oper=listWj&pageSize=300",cookies = cook)
    bsObj = BeautifulSoup(r.text,"html.parser")
    msg = []
    for item in bsObj.findAll("img",{"src":"/img/icon/edit.gif"}):
        params_in = dict()
        tmpstr = item.attrs["name"].split("#@")
        teacher_name = tmpstr[2]
        class_name = tmpstr[4]
        params_in["wjbm"] = tmpstr[0]
        params_in["bpr"] = tmpstr[1]
        params_in["pgnr"] = tmpstr[5]
        params_in["oper"] = "wjShow"
        r_in = requests.post(jxpgurl,params_in,cookies = cook)
        bsObj_in = BeautifulSoup(r_in.text,"html.parser")
        params_post = dict()
        params_post["wjbm"] = params_in["wjbm"]
        params_post["bpr"] = params_in["bpr"]
        params_post["pgnr"] = params_in["pgnr"]
        for item_in in bsObj_in.findAll("input",{"type":"radio"}):
            tmpstr_in = item_in.attrs["name"]
            if tmpstr_in not in params_post.keys():
                params_post[tmpstr_in] = item_in.attrs["value"]
        params_post["zgpj"] = "good"
        #print(params_post)
        requests.post(jxpgurl+"?oper=wjpg",params_post,cookies = cook)
        msg.append(teacher_name + " " + class_name + "评教成功")
        #for ss in tmpstr:
        #    print(ss)
        #print(item.attrs["name"])

    if msg == []:
        msg.append("评教失败")
    return msg

if __name__ == "__main__":
    zjh = input("please input your username:")
    mm = getpass.getpass("please input your password:")
    teach_evaluate(zjh,mm)
    input()