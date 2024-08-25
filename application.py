from flask import Flask, request, render_template, jsonify
from pymongo import MongoClient
from src.pipelines.prediction_pipeline import CustomData, PredictPipeline
import datetime

application = Flask(__name__)
app = application


uri = "mongodb+srv://palkii:dogbarks@cluster0.6vihjoo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri)


DATABASE_NAME="Diamond_Price"
COLLECTION_NAME="Diamonds"

@app.route('/predict', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('form.html')
    else:
        # Get data from the form
        data = CustomData(
            carat=float(request.form.get('carat')),
            depth=float(request.form.get('depth')),
            table=float(request.form.get('table')),
            x=float(request.form.get('x')),
            y=float(request.form.get('y')),
            z=float(request.form.get('z')),
            cut=request.form.get('cut'),
            color=request.form.get('color'),
            clarity=request.form.get('clarity')
        )
        
        # Convert the data to a dataframe
        final_new_data = data.get_data_as_dataframe()
        
        # Prediction
        predict_pipeline = PredictPipeline()
        pred = predict_pipeline.predict(final_new_data)
        results = round(pred[0], 2)
        
        # Store the data and prediction result in MongoDB
        record = {
            "carat": data.carat,
            "depth": data.depth,
            "table": data.table,
            "x": data.x,
            "y": data.y,
            "z": data.z,
            "cut": data.cut,
            "color": data.color,
            "clarity": data.clarity,
            "prediction": results,
            "timestamp": datetime.datetime.utcnow()
        }
        
        client[DATABASE_NAME][COLLECTION_NAME].insert_one(record)
        
        return render_template('form.html', final_result=results)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)


















#**************old*****************************************

# from flask import Flask,request,render_template,jsonify
# from src.pipelines.prediction_pipeline import CustomData,PredictPipeline


# application=Flask(__name__)

# app=application



# @app.route('/predict',methods=['GET','POST'])

# def predict_datapoint():
#     if request.method=='GET':
#         return render_template('form.html')
    
#     else:
#         data=CustomData(
#             carat=float(request.form.get('carat')),
#             depth = float(request.form.get('depth')),
#             table = float(request.form.get('table')),
#             x = float(request.form.get('x')),
#             y = float(request.form.get('y')),
#             z = float(request.form.get('z')),
#             cut = request.form.get('cut'),
#             color= request.form.get('color'),
#             clarity = request.form.get('clarity')
#         )
#         final_new_data=data.get_data_as_dataframe()
#         predict_pipeline=PredictPipeline()
#         pred=predict_pipeline.predict(final_new_data)

#         results=round(pred[0],2)

#         return render_template('form.html',final_result=results)
    

# if __name__=="__main__":
#     app.run(host='0.0.0.0',debug=True)