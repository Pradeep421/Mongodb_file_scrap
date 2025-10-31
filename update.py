import retrival as gu
import pymongo
import mail
from pymongo import MongoClient, UpdateOne, UpdateMany
import pandas as pd
# import Consonants as cs
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb2 = myclient["master"]
mycol2 = mydb2["master_collection"]
mydb = myclient["employee_db"]
mycol = mydb["old_data"]
mycol1=mydb["present_data"]
cur=mycol1.find()
list_cur=list(cur)
# print("dataagsgsg",list_cur)

#Writing the file in json after unmerge operation
df=pd.DataFrame(list_cur)
print(df)
def getfilepathfrwrite():
    a=mycol2.find({},{'domain_id':1,'WBUCKETPATH':1})
    ## domain_id which will be obtained
    path=[]
    for data in a:
        c=((data['WBUCKETPATH']))
        path.append(str(c))
        print(type(path))
        path1=' '.join(map(str, path))
        print(type(path1))
        return path1
writebucketpath= getfilepathfrwrite()

def writejson(writebucketpath):
    df = pd.DataFrame(list_cur)
    df.to_json(writebucketpath,default_handler=str, orient = 'records')
    print('files written')
    return df
#Calling the function
writejson(writebucketpath)

# Function for removing the UnMerged records in the Golden Repository
class remove_unmerge:
    def __init__(self,id):
        self.id=id
        
        #self.file=file
    def unmerge_delete_guid(self):
        mail.update_report(self.id)
        for item in self.id:
          query = {"OLDGUID": item}
          
          result = mycol1.delete_many(query)
          print("records {} deleted".format(item))
          print("docs deleted:", result.deleted_count)
          #print("Removed the UNMERGED GUID {}  in GOLDEN REPO COLLECTION".format(item))
        

def unmerge_delete_guids():
    
    b =remove_unmerge(gu.matched)
    b.unmerge_delete_guid()

unmerge_delete_guids()