import pandas as pd
df=pd.read_csv('rules_1.csv')

def AprioriReturns(antecedents):
    consequents=[]
    for i in antecedents:
        for j in range(0,len(df)):
            if df.antecedents[j]=='frozenset({'+str(i)+'})':
                if int(df.consequents[j][11:-2]) not in antecedents:
                    if df.consequents[j][11:-2] not in consequents:
                        consequents.append(df.consequents[j][11:-2])
    return consequents

#a_list=[5,6]
#print(AprioriReturns(a_list))
