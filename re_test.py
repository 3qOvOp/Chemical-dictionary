import re
def deleKuo(word):

    l = word.find("(")
    r = word.find(")")
    ll = word.find("[")
    rr = word.find("]")
    n = 0
    while ll > -1 and rr > -1 and rr > ll:
        a = [word[0:ll], word[rr + 1:]]
        word = "".join(a)
        ll = word.find("[")
        rr = word.find("]")
        n += 1
        if n==2:
            break
    n = 0
    while l > -1 and r > -1 and r > l:
        a = [word[0:l], word[r + 1:]]
        word = "".join(a)
        l = word.find("(")
        r = word.find(")")
        n += 1
        if n==2:
            break
    word.replace("--","-")
    if len(word) == 0:
        return word
    if word[0] == "-":
        word = word[1:]
    return word
a = "丁腈/聚氯乙烯共混胶NBR/PVC blende以丁腈橡胶为主，加"
b = "丁腈橡胶改性酚醛模(压)塑粉NBR modified phenolic"
c = "丁腈/聚氯乙烯共混胶NBR/PVC blende以丁腈橡"
word = deleKuo(b)#此处去括号
print(word)
word = word.replace(" ",'')
print(word)
p111 = re.search("^(([\w，]{1,8}-){0,2}[\u4E00-\u9FA5/]{1,20}-{0,1}){1,4}"
                   "(([\w，]{1,8}-){0,2}[A-Za-z][A-Za-z\d；/]{4,40}-{0,1}){1,4}"
                   , word)
# ps = re.search("^(([\s\w，]{1,8}-){0,1}[\u4E00-\u9FA5·\s]{2,20}-{0,1}){1,4}[ⅠⅡⅢⅣⅤA-Z\d\s]{0,6}"
#                    "(([\s\w，]{1,8}-){0,1}[A-Za-z]{1}[A-Za-z\s\d；]{4,40}-{0,1}){1,4}[ⅠⅡⅢⅣⅤA-Z\d\s]{0,6}"
#                    , word)
if p111:
    print(p111)
