import pandas as pd
from math import log2
from copy import deepcopy

def convertData(df):
  colList = df.columns.tolist()
  colList.remove('day')
  colList.remove('play')
  
  input = {}
  output = []

  for col in colList:
    for index,row in df.iterrows():
      key = str(col)
      val = df[key][index]
      if key in input:
        input[key].append(val)
      else:
        input[key] = [val]

  for index,row in df.iterrows():
    val = df['play'][index]
    output.append(val)

  return input, output



def entropy(values):
  countYes = 0
  countNo = 0
  size = len(values)

  for val in values:
    if val == 'Yes':
      countYes += 1
    else:
      countNo += 1
  
  if(countYes == 0 or countNo == 0):
    return 0
  
  return -((countYes/size * (log2(countYes/size))) + (countNo/size * (log2(countNo/size))))



def findHighestInfoGain(input, output, totalEntropy):
  size = len(output)
  infoGainList = []

  for attribute in input:
    infoGain = 0

    #finding unique elements
    tempDict = {}
    for val in input[attribute]:
      tempDict[val] = 1
    
    #find entropy for each value
    for key in tempDict:
      outputVal = []
      index = 0
      for val in input[attribute]:
        if val == key:
          outputVal.append(output[index])
        index += 1
      #finding infoGain
      #print(key, len(outputVal),size, entropy(outputVal))
      infoGain += ((len(outputVal)/size) * entropy(outputVal))
    
    infoGain = totalEntropy - infoGain
    infoGainList.append([infoGain, attribute])
  
  infoGainList.sort()
  infoGainList.reverse()
  
  return infoGainList[0][1]



def filterDataset(df,value,attribute):
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



def generateTree(df, input, output, totEntropy, answer, columns, index):
  if totEntropy == 0:
    if(len(output)):
      answer.append(output[0])
    decisionRules.append(deepcopy(answer))
    if(len(output)):
      answer.pop()
    return 

  attribute = columns[index]
  index += 1
  
  #finding unique elements
  tempDict = {}
  for val in input[attribute]:
    tempDict[val] = 1

  for key in tempDict:
    answer.append([attribute, key])
    newDf = filterDataset(df, key, attribute)
    newInput, newOutput = convertData(newDf)
    newTotEntropy = entropy(newOutput)
    generateTree(newDf, newInput, newOutput, newTotEntropy, answer, columns, index)
    answer.pop()


#modified ID3 Algo to Hunt's algo
answer = []

decisionRules = []

df = pd.read_csv('data.csv')

input, output = convertData(df)

index = 0
totEntropy = entropy(output)
columns = df.columns.tolist()

columns.remove('day')
columns.remove('play')
generateTree(df, input, output, totEntropy, answer, columns, index)

file = open('answer.txt','w')
file.write(str(decisionRules))
file.close()

print(decisionRules)