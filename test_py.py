import pymongo, certifi
print('Testing...')
c = pymongo.MongoClient('mongodb+srv://babanp513:1Sufyan786*@cluster0.cug3gqr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0', tlsCAFile=certifi.where())
print(c.admin.command('ping'))