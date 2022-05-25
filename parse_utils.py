import re

# 提取介绍、描述describe 输入段落文字，中文名和英文名字
def extract_describe(paragraph_text,term_and_ename):
    #替换段落paragraph_text中的term_and_ename词语为空格，去调首位空格并返回
    describe = paragraph_text.replace(term_and_ename, '')
    #describe = describe.strip()
    return describe

# 在介绍中提取同意词synonym，输入段落文字，中文名和英文名字
def another_name(para,term_tem):
    des = extract_describe(para,term_tem)
    #又称硫Na Oz SCH， NH--SO2---NH CH， SO2Na·2Hzo福宋钠。
    #another_p = re.search("(又称|实质上是|又名|也称|简称|即|俗称)([\u4E00-\u9FA5，\s\dA-Za-z()·-]+。)?", des)
    another_p = re.search("^[^。]*(又称|实质上是|又名|别名|也称|简称|即|俗称|学名|历史名称， 是|历史名称)([^。]+。)?", des)
    synonym = ""
    if another_p:
        print(another_p)
        synonym = another_p.group(2)
    if synonym!= "" and synonym!= None :
        synonym = synonym.replace("。","").replace(".","").replace(" ", "")
        synonym = re.split("[，或]",synonym)
    else:
        synonym = None
    return synonym

# 去掉括号的word，输入段落文字
def deleKuo(word):
    #print("word:",word)
    l = word.find("(")
    r = word.find(")")
    ll = word.find("[")
    rr = word.find("]")
    n = 0
    dw = {}
    # 去掉 [] 括号部分
    while ll > -1 and rr > -1 and rr > ll:
        dw[ll] = word[ll:rr+1]
        a = [word[0:ll]+(r-l+1)*" ", word[rr + 1:]]
        word = "".join(a)
        ll = word.find("[")
        rr = word.find("]")
        n += 1
        if n==2:
            break
    # 去掉（）括号部分
    n = 0
    while l > -1 and r > -1 and r > l:
        dw[l] =  word[l:r + 1]
        a = [word[0:l]+(r-l+1)*" ", word[r + 1:]]
        word = "".join(a)
        l = word.find("(")
        r = word.find(")")
        n += 1
        if n==4:
            break
    # 去括号后有两种情况修正 --  ^-
    word.replace("--","- ")
    if word[0] == "-":
        word = "".join([" ",word[1:]])
    #print("word:",word,"dw",dw)
    return word,dw

# 本函数的功能是找到最后一个中文字位置index，输入中英文名字，和初始化索引index
def find_index(term_tem,index):
    # 找到最后一个中文的位置
    for i in range(len(term_tem)):
        if '\u4e00' <= term_tem[i] <= '\u9fff':
            index = i
    index += 1  # 那么英文第一个字母的位置就要加一
    return index

# 解决(一)(二)问题,输出修正的英文名字term_en
def en2(term_en,word,dw):#key == 左括号的索引
    # 解决括号一问题 如：2，6-本分(一)sadasda苯酚(二)sdasdasd本
    # 去括号的方案会忽略(二)后的英文sdasdasd，这里把它加载英文名字后面
    for key in dw.keys():
        if dw[key] =='(二)':
            # print("para:",word,"key:",key)
            find_en = word[key+3:]
            re_en = re.search("^[^\u4E00-\u9FA5]+",find_en)
            if re_en:
                term_en2 = re_en.group()
                # print("aaaaaaaa",term_en2)
                return  term_en[3:] + "；"+term_en2
            else:
                return ""
    return ""

# 解决英文名字部分的头部出现中文名字的英文,输出修正的英文名字term_en
def en3(term_en,index):
    # 解决英文名字部分的头部出现中文名字的英文
    # 7-氨(基)喹[c]哪啶H37-amino quin aldineH3 中的H3是中文名字
    # 拿到第一个英文名字
    en = term_en.split("；")
    en = en[0]
    # 比较这时英文第一个名字的首尾，若相同取最长部分给中文部分（通过改变index）
    for i in range(int(len(en) / 2)):
        i = i + 1
        # print(en[0:i],en[-i:])
        if en[0:i] == en[-i:] and (en[0:i] < "a" or en[0:i] > "z"):
            index += i
    return index

# 第一种情况，如下：
# para1 = "7-氨(基)喹[c]哪啶H3 7-amino quin aldineH3； 7-amino-2-me thy!-H2NCH3quinoline   又称7-氨基-2-甲基喹啉，sdasd。针，"
def r1(para):
    # 去括号
    word,dw = deleKuo(para)
    term_tem = re.search("(^\d{1,5}_)([^a-z]+"
                         "[^\u4E00-\u9FA5]+([ⅠⅡA-Za-z]{0,4}|[\d]{5}))"
                         , word)
    if term_tem:# 若检测出名字和英文名字
        # 提取页码部分长度 和 名字、英文名字
        lpage = len(term_tem.group(1))
        # term_tem 去除段首数字的中文名字和英文名字，如：
        # 7-氨(基)喹[c]哪啶H3 7-amino quin aldineH3； 7-amino-2-me thy!-H2NCH3quinoline
        term_tem = term_tem.group(2)
        #print("lpage",lpage,"term_tem",term_tem)
    else:# 若提取不出来，直接返回空
        return None,None,None,None
    # 初始化中文名字末尾和总名字末尾的索引
    index = 0                   # index 为第一个英文别称字母的位置
    index2 = len(term_tem)      # index2为名字的总长度
    # 以最为一个中文字为中文的末尾
    index = find_index(term_tem,index)
    # 原始的段落
    para = para[lpage:]         # 要去掉段首页码 26_
    # 拿到同义词synonym
    synonym = another_name(para, para[0:index2])

    # ll 是原始段落的长度，在本函数之外用
    ll = index2 + lpage

    # 第一次拿到英文名字，此时不是正确的，下面的H3是中文名字，此刻index应在7的位置
    # 7-氨(基)喹[c]哪啶H37-amino quin aldineH3
    term_en = para[index:index2]
    # 解决英文名字部分的头部出现中文名字的英文
    index = en3(term_en,index)
    # 赋值中文名字term，和英文名字term_en
    term = para[0:index].replace(" ", "")

    # 解决英文名字部分的头部出现中文名字的英文
    term_en = para[index:index2].replace(" ", "")
    term_en = en2(term_en,word,dw)

    return term,term_en,synonym,ll

# 解决第二种情况:苯酚见苯酚酸1860。
def r2(para):
    term_tem = re.search("(^\d{1,5}_)((([\s\w，]{1,8}-){0,1}[\u4E00-\u9FA5·\s]{1,20}-{0,1}){1,4}[A-Z\d\s]{0,6}"
                   "见[\u4E00-\u9FA5]{0,20}([(][\u4E00-\u9FA5][)]){0,1}[\u4E00-\u9FA5]+\d{1,5})"
                   , para)
    if term_tem:
        lpage = term_tem.group(1)
        term_tem = term_tem.group(2)
        #print(term_tem)
        ll = len(term_tem) + len(lpage) + 1
        #print("ll",ll)
        term_tem.replace(" ", "")
        index1 = term_tem.index("见")
        p = re.search("\d{1,5}$",term_tem)
        if p:
            p = p.group()
        index2 = len(term_tem)-len(p) # 第一个数字的位置
    else:
        return None,None,None,None
    term = term_tem[0:index1]
    synonym = term_tem[index1+1:index2]
    if synonym != "" and synonym != None:
        synonym = synonym.replace("。", "").replace(".", "").replace(" ", "").split("，")
    else:
        synonym = None
    return term, "", synonym, ll

# 124_Kinyon泵Kinyon pump
# Worthington泵   Worthington pump
#para3 = "Worthington泵Worthington pump"
def r3(para):
    term_tem = re.search("^(\d{1,5}_)((([A-Z][a-z\s]{3,40})|([A-Z]{2,10}))[\u4E00-\u9FA5]{1,20}\s?[A-Z][a-z\s]{3,40})",para)
    if term_tem:
        # print(term_tem)
        lpage = len(term_tem.group(1))
        term_tem = term_tem.group(2)
        ll = len(term_tem) + lpage
    else:
        return None,None,None,None
    index = 0
    for i in range(len(term_tem)):
        if '\u4e00' <= term_tem[i] <= '\u9fff':
            index = i
    index2 = index+1
    term = term_tem[0:index2].replace(" ", "")
    term_en = term_tem[index2:].replace(" ", "")
    synonym = another_name(para, term_tem)
    if synonym != "" and synonym != None:
        synonym = synonym.replace("。", "").replace(".", "").replace(" ", "").split("，")
    else:
        synonym = None
    # print(term)
    # print(term_en)
    # print(term, term_en, synonym)
    return term, term_en, synonym, ll

if __name__ == '__main__':
    # para2 = "1_氨基酸见氨基酸算1840"
    a = "1_2-(c)-吖啶(一)H3CaaaeH3C又称氮(杂) 蒽。(二)sdasd本"
    #dw = {}
    print(r1(a))
    #print(another_name("", ""))



# term_tem = re.search("^(([\s\w，]{1,8}-){0,1}[\u4E00-\u9FA5·\s]{2,20}-{0,1}){1,4}[A-Z\d\s]{0,6}"
#                          "(([\s\w，]{1,8}-){0,1}[A-Za-z]{1}[a-z\s\d；]{4,40}-{0,1}){1,4}[A-Z\d\s]{0,6}"
#                          , word)
# term_tem = re.search("(^\d{1,5}_)([\u4E00-\u9FA5A-Z·\s\d，/ⅠⅡαβγy-]+[ⅠⅡ]?"
#                      "[\da-zA-Z；，/\s'-αβy]+[A-Za-z]{0,4}([ⅠⅡA-Za-z]|[\d]{5}))"
#                      , word)