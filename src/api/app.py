import os
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from pathlib import Path
from helpers.form_processor import validate_form
import pandas as pd
import joblib
import traceback

## Defined here for global access, will be instantiated during startup
trained_model = None
model_columns = None

parent = Path(__file__).parent.absolute()
data_folder = f"{parent}/data"

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/query', methods=['POST'])
@cross_origin()
def query_model():
    try:
        json_data = request.json
        validate_form(json_data)
        data_frame = pd.DataFrame(json_data)
        dummied_data = pd.get_dummies(data_frame)

        cleansed_query = dummied_data.reindex(columns=model_columns, fill_value=0)
        prediction = trained_model.predict(cleansed_query)

        return jsonify({'result': list(map(int, prediction))})
    
    except Exception as e:
        print(e)
        return jsonify({'error': str(e), 'trace': traceback.format_exc()})

@app.route('/health', methods=['GET'])
@cross_origin()
def get_status():
    try:
        model_loaded = False
        if trained_model is not None:
            model_loaded = True
        result = {'modelLoaded': model_loaded, 'apiStatus': 'Healthy'}
        
        return jsonify(result)
    
    except Exception as e:
        print(e)
        result = {'modelLoaded': model_loaded, 'apiStatus': 'Down'}
        return jsonify(result)


if __name__ == '__main__':
    trained_model = joblib.load(f"{data_folder}/model.pkl")
    model_columns = joblib.load(f"{data_folder}/model_columns.pkl")

    app.run(host='0.0.0.0', port=os.getenv('PORT'))
