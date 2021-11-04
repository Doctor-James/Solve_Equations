import re


# 乘除法
def mul_div(s):
    if '*' in s:
        s = s.split('*')
        return float(s[0]) * float(s[1])
    elif '/' in s:
        s = s.split('/')
        return float(s[0]) / float(s[1])

# 加减法
def add_sub(s):
    if '+' in s:
        s = s.split('+')
        return float(s[0]) + float(s[1])
    else:
        if s[0] == '-':
            s = s[1::].split('-', 1)
            s[0] = '-' + s[0]
            return float(s[0]) - float(s[1])
        else:
            s = s.split('-', 1)
            return float(s[0]) - float(s[1])


# 替换字符串
def str_replace(lst1,lst2,str1):
    for i in range(len(lst1)):
        if (lst2[i] != '!'):            
            str1 = str1.replace(lst1[i], lst2[i])

#修正一些符号
def correct_symbol(str1):
    str1 = str1.replace('++','+')
    str1 = str1.replace('--','+')
    str1 = str1.replace('+-','-')
    str1 = str1.replace('-+','-')
    str1 = str1.replace('*-','-')
    str1 = str1.replace('-*','-')
    return str1

#计算纯加减算式（不含x）
def calculate(str1):
    while True:
        if '(' not in str1 and ')' not in str1:
            break
        pattern1 = re.compile(r'\([^(^)]*?\)')
        ret1 = pattern1.findall(str1)
        #匹配括号内的内容
        ret2 = []
        pattern2 = re.compile(r'\((?P<tag>.*?)\)')
        for i in range(len(ret1)):
            ret = pattern2.search(ret1[i])
            ret2.append(ret.group('tag'))
            # 计算乘除法
            while True:
                pattern3 = re.compile(r'[-+*/]?(?P<tag>-?\d+(\.\d+)?[*/]-?\d+(\.\d+)?)')
                ret3 = pattern3.search(ret2[i])
                try:
                    ret4 = ret3.group('tag')
                except Exception as e:
                    pass
                if '*' not in ret2[i] and '/' not in ret2[i]:
                    break
                else:
                    ret2[i] = ret2[i].replace(ret4, str(mul_div(ret4)))
        # 计算加法
            while True:
                pattern3 = re.compile(r'-?\d+(\.\d+)?[-+]-?\d+(\.\d+)?')
                ret3 = pattern3.search(ret2[i])
                try:
                    ret4 = ret3.group()
                except Exception as e:
                    pass
                if '+' not in ret2[i] and '-' not in ret2[i][1::]:
                    break
                else:
                    ret2[i] = ret2[i].replace(ret4, str(add_sub(ret4)))
        
        for j in range(len(ret1)):
                str1 = str1.replace(ret1[j], ret2[j]) 
    return str1


#化简（打开括号）
def simplify(str1):
    cnt=0
    while True:
        str1[0] = correct_symbol('+'+str1[0])
        str1[1] = correct_symbol('+'+str1[1])
        if '(' not in str1[0] and ')' not in str1[0]:
            if '(' not in str1[1] and ')' not in str1[1]:
                break
        cnt = cnt +1
        for k in range(len(str1)):
            
            # 匹配最内层括号
            pattern1 = re.compile(r'\([^(^)]*?\)')
            ret1 = pattern1.findall(str1[k])
            # 匹配括号内的内容
            ret2 = []
            pattern2 = re.compile(r'\((?P<tag>.*?)\)')
            for i in range(len(ret1)):
                if (ret1[i].find('x') != -1):
                    begin = str1[k].find(str(ret1[i]))
                    finish = begin + len(str(ret1[i]))
                    if (str1[k][begin-1] =='*'): #括号前为乘号需考虑分配率
                        ret1[i] = ret1[i][1:-1]
                        smallpart=re.split(r'[\+-]', ret1[i]) #把括号内内容根据加减号分隔
                        yunsuanfu=re.findall(r'[\+-]', ret1[i])+[''] #搜出所有加减号；由于加减号比数字少一项，用空字符补齐
                        findthenumber=str1[k][:begin]  #开始搜括号前分配率的那个数
                        prenumbers=re.findall(r'[\d\*/\.]+$',findthenumber) 
                        prenumber=prenumbers[0][:-1]
                        begin=begin-len(prenumber)  #更新起始位置，因为下面要切片更新字符串
                        newi=''
                        for m in range(len(smallpart)):
                            smallpart[m]=prenumber+'*'+smallpart[m]
                            newi=newi+smallpart[m]+yunsuanfu[m]   #开始分配
                        ret1[i]='('+newi+')' #括号还回去，因为可能还要继续分配率
                        str1[k]=str1[k][:begin-1]+ret1[i]+str1[k][finish:] #拼接字符串
                        finish=begin+len(ret1[i])  #该括号结束位置变了
                    elif (str1[k][begin-1] =='+'): #括号前为加号
                        if ret1[i][1]=='-':  #括号内的第一个数
                            ret1[i] = ret1[i][1:-1]
                            str1[k]=str1[k][:begin-1]+ret1[i]+str1[k][finish:] #拼接字符串
                        else:
                            ret1[i] = ret1[i][1:-1]
                            str1[k]=str1[k][:begin]+ret1[i]+str1[k][finish:] #拼接字符串
                    elif (str1[k][begin-1] =='-'): #括号前为减号
                        if ret1[i][1]=='-':  #括号内的第一个数
                            ret1[i]=re.sub(r'\+(?=\w)','?',ret1[i])  #无法同时互换加减，只能先把加号替换成另一个无关符号
                            ret1[i]=re.sub(r'(?<=\w)\-(?=\w)','+',ret1[i])
                            ret1[i]=ret1[i].replace('?','-')
                            ret1[i] = ret1[i][1:-1]
                            str1[k]=str1[k][:begin-1]+ret1[i]+str1[k][finish:] #拼接字符串
                        else:
                            ret1[i]=re.sub(r'\+(?=\w)','?',ret1[i])  #无法同时互换加减，只能先把加号替换成另一个无关符号
                            ret1[i]=re.sub(r'(?<=\w)\-(?=\w)','+',ret1[i])
                            ret1[i]=ret1[i].replace('?','-')
                            ret1[i] = ret1[i][1:-1]
                            str1[k]=str1[k][:begin]+ret1[i]+str1[k][finish:] #拼接字符串s
                    ret2.append('!')
                    continue
                
                else:
                    ret = pattern2.search(ret1[i])
                    ret2.append(ret.group('tag'))
                    # 计算乘除法
                    while True:
                        pattern3 = re.compile(r'[-+*/]?(?P<tag>-?\d+(\.\d+)?[*/]-?\d+(\.\d+)?)')
                        ret3 = pattern3.search(ret2[i])
                        try:
                            ret4 = ret3.group('tag')
                        except Exception as e:
                            pass
                        if '*' not in ret2[i] and '/' not in ret2[i]:
                            break
                        else:
                            ret2[i] = ret2[i].replace(ret4, str(mul_div(ret4)))
                # 计算加法
                    while True:
                        pattern3 = re.compile(r'-?\d+(\.\d+)?[-+]-?\d+(\.\d+)?')
                        ret3 = pattern3.search(ret2[i])
                        try:
                            ret4 = ret3.group()
                        except Exception as e:
                            pass
                        if '+' not in ret2[i] and '-' not in ret2[i][1::]:
                            break
                        else:
                            ret2[i] = ret2[i].replace(ret4, str(add_sub(ret4)))
            for j in range(len(ret1)):
                if (ret2[j] != '!'):            
                    str1[k] = str1[k].replace(ret1[j], ret2[j])
        equation = str1[0]+"="+str1[1]
        print(equation)
    if cnt == 0:
        return str1[0]+"="+str1[1]
    else:
        return equation
        
    
error = ["++","-+","+-","**","*/","/*","//","+*","*+","-*","*-","--"]
while True:
    status = 13
    str1 = input('请输入算式：')
    if '=' not in str1:
        print("式子错误，请重输：")
        continue
    else :
        status = status -1
    for i in range(len(error)):            
        if error[i] in str1:
            print("式子错误，请重输：")
            break
        else:
            status = status -1
    if status == 0:
        break
print("计算过程以及结果为：")

#分为左式和右式
lst1 = str1.split('=')
#分左式右式别化简
equation = simplify(lst1)
equation = equation.split('=')
left = equation[0]
right = equation[1]

#在开头加一个正号，方便移项
left = "+"+left
right = "+"+right
left = correct_symbol(left)
right = correct_symbol(right)

#将左边式子分为带x的left_x和不带x的left_number
left_list = [i.start() for i in re.finditer('x', left)] 
left_x=[]
for j in range(len(left_list)):
    if left[left_list[j]-1] == "*":
        p = left_list[j]
        for p in range(left_list[j]-1,-1,-1):
            if left[p] in{'+','-'}:
                left_x.append(left[p:(left_list[j]+1)])
                break
                
    else:
        p = left_list[j]
        for p in range(left_list[j]-1,-1,-1):
            if left[p] in{'+','-'}:
                left_x.append(left[p:(left_list[j]+1)])
                break
                
        
left_number = left
if len(left_list) == 1:
    left_x = ''.join(left_x)
    left_number = left_number.replace(left_x,'')
else:    
    for k in range(len(left_list)):
        left_number = left_number.replace(left_x[k],'')
left_number = left_number.replace('-','?')
left_number = left_number.replace('+','-')
left_number = left_number.replace('?','+')

#将右边式子分为带x的right_x和不带x的right_number
right_list = [i.start() for i in re.finditer('x', right)] 
right_x=[]
for j in range(len(right_list)):
    if right[right_list[j]-1] == "*":
        p = right_list[j]
        for p in range(right_list[j]-1,-1,-1):
            if right[p] in{'+','-'}:
                right_x.append(right[p:(right_list[j]+1)])
                break
right_number = right
if len(right_list) == 1:
    if right_x[0] == '+':
        right_number = right_number.replace(right_x,'')
        right_x=right_x.replace('+','-')
    elif right_x[0] == '-':
        right_number = right_number.replace(right_x,'')
        right_x=right_x.replace('-','+')
elif len(right_list) > 1:    
    for k in range(len(right_list)):
        if right_x[k][0] == '+':
            right_number = right_number.replace(right_x[k],'')
            right_x[k]=right_x[k].replace('+','-')
            continue
        elif right_x[k][0] == '-':
            right_number = right_number.replace(right_x[k],'')
            right_x[k]=right_x[k].replace('-','+')
            continue
            

#移项，带x的移到左边，不带x的移到右边
right_x=''.join(right_x)
left_x=''.join(left_x)
#equation = str1[0]+"="+str1[1]
if (left_x[0] == '-'):
    left = left_x+right_x
else:
    left = left_x[1:]+right_x
    
if (right_number[0] == '-'):
    right = right_number+left_number
else:
    right = right_number[1:]+left_number

equation = left +'='+right
print(equation)

#右式直接计算，左式将x变为1，算出系数
left = '('+left+')'
right='('+right+')'
left = left.replace('x','1')
right=calculate(right)
left=calculate(left)
#输出最后结果
print(left+'*x='+right)
print('x=',float(right)/float(left))
