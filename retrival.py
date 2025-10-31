import pymongo
import pandas
import mail


# connecting to mongo
mongodb=pymongo.MongoClient("mongodb://localhost:27017/")

db=mongodb["employee_db"]
collection1=db["present_data"]
collection2=db["old_data"]
master=mongodb["master"]
master_collection=master["master_collection"]

# print(master_collection)


#retrivinga the data from the ibucket
def get_path():
    data=master_collection.find({},{"domain_id","IBUCKETPATH"})
    let=[]
    for i in data:
        return (i["IBUCKETPATH"])
     
   
file_path=get_path()

def read_file(file_path):
    data=pandas.read_csv(file_path)
    file_data= data["GUID"].tolist()    
    old_data=collection2.find({},{"GUID"})
    old_df=pandas.DataFrame(old_data)
    b=old_df["GUID"].tolist()
    # let =[i["GUID"]  for i in old_data if int(i["GUID"]) in file_data]
    matched=[]
    unmatched=[]
    for i in file_data :
        if str(i) in b:
            matched.append(str(i))
        else:
            unmatched.append(i)

    return(matched,unmatched)
    # return let

class update_old:

    def __init__(self,matched):
        self.id=matched
    
    def update_old_data(self):
        for i in self.id:
            old_data=collection2.update_many({"GUID":i},{"$set":{"umerge":"true"}})     
        
    
# Function for removing  the  indicator fields and updating them with respect to the unmergedGUID
    def unmerge_remove_ind_guid(self):
        print(self.id)
        # col_name = 'Consolidation_Ind'
        for item in self.id:
            filter, update = {"GUID": item}, {'$unset': {'Consolidation_Ind': " "}}
            # db.testcollection.update_many({}, {"$unset": {f"{col_name}": 1}})
            collection1.update_many(filter, update)
            # { $unset: {name: "", weight: ""}}
            print("Removed the consolidationindicatorof {} and Updated in Mongodb".format(item))

# Function for adding the OLD GUID fields and updating unmerged GUIDS
    def unmerge_guidrepo_update_oldguid(self):
        for item in self.id:
            filter, update = {"GUID": item}, {"$set": {"OLDGUID": item}}
            collection1.update_many(filter, update)
            print("Updated oldguid {} in Mongodb".format(item))
# Function for emptying the  GUID fields and updating them with respect to the unmergedGUID
    def unmerge_empty_guid(self):
        for item in self.id:
            filter, update = {"GUID": item}, {"$set": {"GUID": " "}}
            collection1.update_many(filter, update)
            print("Removed the oldguid {} and Updated in Mongodb".format(item))




matched,unmatched=read_file(file_path)
a=update_old(matched)
a.update_old_data()
a.unmerge_guidrepo_update_oldguid()
a.unmerge_remove_ind_guid()
a.unmerge_empty_guid()

mail.send_report(matched,unmatched)
