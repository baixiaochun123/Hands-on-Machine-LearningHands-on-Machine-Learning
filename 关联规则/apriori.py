import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.pylab import style  # 自定义图表风格

style.use('ggplot')
from IPython.core.interactiveshell import InteractiveShell
# IPython：Python中用于交互式和并行计算的工具。
# 用于Python的增强的交互式shell。
InteractiveShell.ast_node_interactivity = "all"

pd.set_option('display.float_format', lambda x: '%.2f' % x)  # 取消科学计数法

plt.rcParams['font.sans-serif'] = ['Simhei']  # 解决中文乱码问题

# pip install mlxtend
from mlxtend.preprocessing import TransactionEncoder  # 编码
from mlxtend.frequent_patterns import apriori  # 挖掘频繁项集
from mlxtend.frequent_patterns import association_rules  # 挖掘关联规则

# pip install wordcloud
from wordcloud import WordCloud, ImageColorGenerator
from collections import Counter

import os
import openpyxl  # 结果保存到同一个工作簿的不同工作表

def loadDataSet():
    """加载数据集"""
    return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]

def createC1(dataSet):
    """创建候选项集C1"""
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    return list(map(frozenset, C1))

def aprioriGen(Lk, k):
    """生成Ck"""
    retlist = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i + 1, lenLk):
            L1 = list(Lk[i])[:k - 2]
            L2 = list(Lk[j])[:k - 2]
            if L1 == L2:
                retlist.append(Lk[i] | Lk[j])
    return retlist

def scanD(D, CK, minSupport):
    """扫描数据集D，获取项集CK的支持度，并返回频繁项集和支持度数据"""
    ssCnt = {}
    for tid in D:
        for can in CK:
            if can.issubset(tid):
                if not can in ssCnt:
                    ssCnt[can] = 1
                else:
                    ssCnt[can] += 1
    numItems = float(len(list(D)))
    retlist = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key] / numItems
        if support >= minSupport:
            retlist.insert(0, key)
        supportData[key] = support
    return retlist, supportData

def apriori(dataSet, minSupport=0.5):
    """Apriori算法主体"""
    C1 = createC1(dataSet)
    L1, supportData = scanD(dataSet, C1, minSupport)
    L = [L1]
    k = 2
    while len(L[k-2]) > 0:
        CK = aprioriGen(L[k-2], k)
        LK, supk = scanD(dataSet, CK, minSupport)
        supportData.update(supk)
        L.append(LK)
        k += 1
    return L, supportData

def generateRules(L, supportData, minConf=0.6):
    """从频繁项集中生成关联规则"""
    rulelist = []
    for i in range(1, len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            rulesFromConseq(freqSet, H1, supportData, rulelist, minConf)
    return rulelist

def rulesFromConseq(freqSet, H, supportData, rulelist, minConf=0.6):
    """从频繁项集中生成规则"""
    m = len(H[0])
    while len(freqSet) > m:
        H = calConf(freqSet, H, supportData, rulelist, minConf)
        if len(H) > 1:
            H = aprioriGen(H, m + 1)
            m += 1
        else:
            break

def calConf(freqSet, H, supportData, rulelist, minConf=0.6):
    """计算置信度并筛选规则"""
    prunedh = []
    for conseq in H:
        conf = supportData[freqSet] / supportData[freqSet - conseq]
        if conf >= minConf:
            print(freqSet - conseq, '-->', conseq, 'conf:', conf)
            rulelist.append((freqSet - conseq, conseq, conf))
            prunedh.append(conseq)
    return prunedh

if __name__ == '__main__':
    """主程序入口"""
    dataSet = loadDataSet()
    L, support = apriori(dataSet)
    i = 0
    for freq in L:
        print('项数', i + 1, ':', freq)
        i += 1
    rules = generateRules(L, support, minConf=0.5)