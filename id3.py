import pandas as pd
from math import log2
df = pd.read_csv('play_tennis.csv')

Final_ans=[]

def find_entropy(List):
  countYes=0
  countNo=0
  for i in List:
    if(i=='Yes'):
      countYes +=1
    elif(i=='No'):
      countNo +=1
  
  if countNo==0:
    return 0
  elif countYes==0:
    return 0
  
  return -((countYes/len(List) * (log2(countYes/len(List))) + (countNo/len(List) * (log2(countNo/len(List))))))


def yesOrNo(List):
  return List[0]


def find_highest_info_gain(inputDict,outputDict,total_entropy):
  #all attributes
  returnList=[]
  List2=outputDict['play']
  max=0
  max_attribute='dummy'
  max_list_values=[]
  for key in inputDict.keys():
    List1=inputDict[key]
    list_set = set(List1)
    unique_list = (list(list_set))
    #all values of attribute
    #print(key,end=" ")
    entropy=0
    for i in unique_list:
      tempdict={}
      sublist=[]
      for a in range(0,len(List1)):
        if i == List1[a]:
          sublist.append(List2[a])
      tempdict[i]=sublist
      individual_entropy= (len(sublist)/len(List2))*find_entropy(sublist)
      entropy += individual_entropy
    Info_gain = total_entropy-entropy
    #print(Info_gain)
    if(max<Info_gain):
      max_attribute=key
      max=Info_gain
      max_list_values=unique_list    
  #returnList.append(max)
  returnList.append(max_attribute)
  returnList.append(max_list_values)
  if max>0:
    returnList.append('None')
  elif max==0:
    returnList.append(yesOrNo(sublist))
  
  return returnList



def helper(df):
  attributes=df.columns.tolist()
  attributes.remove('day')
  attributes.remove('play')
  #print(attributes)
  input={}
  output={}

  for j in range(1,len(attributes)+1):
    List=[]
    for i in range(0,len(df)):
      ele=df.iloc[i,j]
      List.append(ele)
    input[attributes[j-1]]=List

  List=[]
  for i in range(0,len(df)):
    List.append(df.iloc[i,len(attributes)+1])

  output['play']=List
  #print(input)
  #print(output)
  total_entropy=find_entropy(output['play'])
  #print(total_entropy)
  returnList=find_highest_info_gain(input,output,total_entropy)
  return returnList



def filterData(df,value,attribute):
  #print(df)
  index=[]
  total_index=[]
  delete_index=[]
  for i in range(0,len(df)):
    total_index.append(i)
    for j in range(0,len(df.columns)):
      if(df.iloc[i,j]==value):
        index.append(i)
  
  #print(index)
  #print(total_index)
  for i in total_index:
    if not i in index:
      delete_index.append(i)
  #print(delete_index)
  new_df=df.drop(delete_index)
  new_df.set_axis(range(len(new_df)), inplace=True)
  lisCol=[]
  lisCol.append(attribute)
  new_df_1=new_df.drop(attribute,axis=1)
  #print(new_df_1)
  return new_df_1



import copy


def recur(df,path):
  List=helper(df)
  #print(List)
  if not (List[2] =='None'):
    #print(path)
    li=copy.deepcopy(path)
    li.append(List[2])
    Final_ans.append(li)

  else:
    path.append(List[0])
    for i in List[1]:
      new_df=filterData(df,i,List[0])
      path.append(i)
      recur(new_df,path)
      path.pop()
    path.pop()



Final_ans.clear()
recur(df,[])
length=len(Final_ans)
for i in range(0,length):
  print(Final_ans[i])



