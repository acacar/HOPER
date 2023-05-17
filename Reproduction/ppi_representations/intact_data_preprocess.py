

#The zip file downloaded from the intact database was opened.
import pandas as pd
from zipfile import ZipFile
with ZipFile('/content/drive/MyDrive/intact.zip', 'r') as zipObj:
   # Extract all the contents of zip file in current directory
   zipObj.extractall()

#The intact.txt file was read
intact_df=pd.read_csv("/content/intact.txt", sep='\t')

#First two columns of interaction filtered
intact_df_filter=intact_df.filter(['#ID(s) interactor A' , 'ID(s) interactor B'])

#uniprotkb: containing words replaced with spaces
intact_drop_uniprotkb=intact_df_filter.replace(regex=r'uniprotkb:', value='')

#Lines where certain variables were found were filtered out.
drop_values = [':','_', '-',',']
intact_drop_values_filt_A_col=intact_drop_uniprotkb[~intact_drop_uniprotkb['#ID(s) interactor A'].str.contains('|'.join(drop_values))]
intact_drop_values_filt_B_col=intact_drop_values_filt_A_col[~intact_drop_values_filt_A_col['ID(s) interactor B'].str.contains('|'.join(drop_values))]
intact_df_dub=intact_drop_values_filt_B_col.drop_duplicates()
intact_df_reset_index=intact_df_dub.reset_index()
intact_df_raw_sorted=intact_df_reset_index.sort_values(by=['#ID(s) interactor A'])
intact_df_raw_sorted_reset=intact_df_raw_sorted.reset_index()
intact_df_raw_sorted_reset_filter=intact_df_raw_sorted_reset.filter(['#ID(s) interactor A' , 'ID(s) interactor B'])

intact_df_raw_sorted_reset_filter.to_excel("intact_raw_data_preprocessing_.xlsx")
protein_df=pd.read_excel("/content/drive/MyDrive/human_proteins.xlsx")
intact_data=pd.read_excel("/content/drive/MyDrive/intact_raw_data_preprocessing.xlsx")
intact_data_frame=intact_data.filter(['#ID(s) interactor A','ID(s) interactor B'])

#Data filtered to include human proteins()
human_protein=pd.DataFrame()
human_protein=protein_df.filter(items=['A'])
human_protein_df_A=pd.DataFrame()
lengthB=len(human_protein)
for i in range(lengthB):
 human_protein_df_A=human_protein_df_A.append(intact_data_frame[intact_data_frame["#ID(s) interactor A"] == human_protein["A"][i]])
human_protein_df_A=human_protein_df_A.reset_index()
intact_data_frame_A=human_protein_df_A.filter(['#ID(s) interactor A','ID(s) interactor B'])
human_protein_df_B=pd.DataFrame()
lengthB=len(human_protein)
for i in range(lengthB):
  human_protein_df_B=human_protein_df_B.append(intact_data_frame_A[intact_data_frame_A["ID(s) interactor B"] == human_protein["A"][i]])
human_protein_df_B=human_protein_df_B.reset_index()
intact_data_frame_B=human_protein_df_B.filter(['#ID(s) interactor A','ID(s) interactor B'])
intact_data_frame_filter_sorted=intact_data_frame_B.sort_values(by=['#ID(s) interactor A'])
intact_data_frame_filter_sorted=intact_data_frame_filter_sorted.reset_index()
intact_data_frame_filter_sorted=intact_data_frame_filter_sorted.filter(['#ID(s) interactor A','ID(s) interactor B'])
intact_data_frame_filter_sorted.to_excel("intact_data_frame_filter_sorted.xlsx")
intact_data_read=pd.read_excel("intact_data_frame_filter_sorted.xlsx")
intact_data_read_filt=intact_data_read.filter(['#ID(s) interactor A','ID(s) interactor B'])
#intactdata_dataframe=pd.read_excel("/content/intact_data_frame_filter_sorted.xlsx")
intactdata_dataframe=intact_data_read_filt
#
converted to edgelist format required for vector operation.
protein=[]
protein=intactdata_dataframe['#ID(s) interactor A']
interactionprotein=intactdata_dataframe['ID(s) interactor B']

list =[]
for col in intactdata_dataframe.columns:
    val = intactdata_dataframe[col]
    for v in val:
        list.append(v)

lengt=intactdata_dataframe.shape[0]
from collections import defaultdict
temp = defaultdict(lambda: len(temp))
res = [temp[ele] for ele in list]
P=res[0:lengt]
i=res[lengt:len(res)]
intactdata_dataframe= pd.DataFrame()
intactdata_dataframe['#ID(s) interactor A']=P
intactdata_dataframe['ID(s) interactor B']=i
print(intactdata_dataframe)
intactdata_dataframe.to_csv("intactdata_dataframe_filter_human_proteins.edgelist",header=False, sep=' ', index=False)

#The order of the proteins corresponding to the numbers in the edgelist was recorded.
newlist =[]
for i in temp.keys():
    newlist.append(i)

protein_id_df=pd.DataFrame(newlist)
protein_id_df.to_csv("proteins_id.csv")
protein_id=pd.read_csv("/content/drive/MyDrive/proteins_id.csv")
mylist=protein_id['0'].tolist()