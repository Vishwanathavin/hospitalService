import pymongo

try:
    conn = pymongo.MongoClient()
    print("Connected successfully!!!")
except pymongo.errors.ConnectionFailure as e:
    print("Could not connect to MongoDB: %s" % e)
hospDatabase = conn['hospitalDB']

val = hospDatabase.hospInfo.distinct('specializations')
print(val)
# hospList = hospDatabase.hospInfo.find({"$and":[{"specializations":{"$in":["Gynaecology"]}},{"city":"Chennai"},{"services_":{"$in":["Ambulance"]}}]})
#
# for hosp in hospList:
#     print (hosp)
# for comp in connection.YNOSdatabase.startupInfo.aggregate([{"$match": {"$and": [{"groupClassification":{"$in": [client['groupClassification']]}}, {"foundedDate": {"$type": "date"}}]}},
# 								{"$group": {"_id": {"$year": "$foundedDate"}, "count": {"$sum": 1}}}])['result']: