def createTable(inputDict,outputList):
  #Final_ans={}
  TableDict={}
  for key in inputDict.keys():
    #TableDict={}
    lista=inputDict[key]
    setA=set(lista)
    for i in setA:
      countYes=0
      countNo=0
      ans=[]
      for j in range(0,len(lista)):
        if i==lista[j]:
          if outputList[j]=='Yes':
            countYes=countYes+1
          elif outputList[j]=='No':
            countNo=countNo+1
      ans.append(countYes)
      ans.append(countNo)
      TableDict[i]=ans
    #Final_ans[key]=TableDict
  #return Final_ans
  return TableDict


def intial(df):
  inputDict={}
  attributes=[]
  for col in df.columns:
    if not (col=='day' or col=='play'):
      attributes.append(col)
  for j in range(1,len(df.columns)-1):
    list1=[]
    for i in range(0,len(df)):
      list1.append(df.iloc[i,j])
    inputDict[attributes[j-1]]=list1

  list2=[]
  for i in range(0,len(df)):
    list2.append(df.iloc[i,len(df.columns)-1])
  return createTable(inputDict,list2)



def total_yes_no(df):
  countYes=0
  countNo=0
  for i in range(0,len(df)):
    if df.iloc[i,len(df.columns)-1] == 'Yes':
      countYes=countYes+1
    elif df.iloc[i,len(df.columns)-1] == 'No':
      countNo=countNo+1
  count=[]
  count.append(countYes)
  count.append(countNo)
  return count



def classify(Table,Count,Total_data_points,q1):
  prob_yes=1
  prob_no=1
  for i in q1:
    prob_yes = prob_yes * Table[i][0]/Count[0]
    prob_no = prob_no * Table[i][1]/Count[1]

  prob_yes = prob_yes * Count[0]/Total_data_points
  prob_no = prob_no * Count[1]/Total_data_points

  Denominator = prob_yes + prob_no

  print(prob_yes)
  prob_yes = prob_yes/Denominator
  print(prob_no)
  prob_no = prob_no/Denominator

  print("Probablity of playing is ",prob_yes)
  print("Probablity of not playing is ",prob_no)

  if prob_yes > prob_no:
    print(q1," given these conditions play = yes")
  elif prob_yes < prob_no:
    print(q1," given these conditions play = no")



def main():
  df=pd.read_csv('play_tennis.csv')
  print(df)
  print()
  Table=intial(df)
  print(Table)
  Count=total_yes_no(df)
  Total_data_points=len(df)
  q1=['Rain','Hot','Normal','Weak']
  classify(Table,Count,Total_data_points,q1)



import pandas as pd

main()