from pymongo import MongoClient
from flask import Flask , request,jsonify



app = Flask(__name__)



client = MongoClient("mongodb://localhost:27017/")



db = client["sih2k24"]
print("DB connected");
domains_collection =db["Classify"]



@app.route('/add-context'  , methods=['POST'])
def add_Context_db():
    
    data = request.json
    
    domain = data.get('domain','').lower()
    
    difficulty = data.get('difficulty','').lower()
    
    context = data.get('context','')
    
    domain_data = domains_collection.find_one({"name":domain})
    
    if domain_data:
        if difficulty in domain_data['Difficulty']:
            domains_collection.update_one(
                {"name":domain},
                {"$push" :{f"Difficulty.{difficulty}":context} }
            )
            return jsonify({"message": f"Inserted {difficulty} context."}), 200
        else:
             return jsonify({"error": f"Invalid difficulty level: {difficulty}."}), 400
            
    else:
        
        new_domain={
            "name":domain,
            "Difficulty":{
                "easy":[],
                "medium":[],
                "hard":[]
            }
        }
        
        new_domain['Difficulty'][difficulty].append(context)
        domains_collection.insert_one(new_domain)
        
        return jsonify({"message": "Newly inserted domain."}), 201
        

@app.route('/get-context/<domain>', methods=['GET'])  
def get_context(domain):
    print(domain)
    print(f"Received domain: {domain.lower()}")
    domain_data = domains_collection.find_one({"name": domain.strip()})

    print(domain_data)

    if domain_data:
        return jsonify({"name": domain_data['name'], "difficulty": domain_data['Difficulty']}), 200
    else:
        return jsonify({"error": "Domain not found."}), 404


    
if __name__=="__main__":
    app.run(debug=True , port=6000)
            