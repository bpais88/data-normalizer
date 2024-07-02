from flask import Flask, request, jsonify
import pandas as pd
import openai
import os

app = Flask(__name__)

# Configure OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    df = pd.read_csv(file)
    return df.to_json()

@app.route('/transform', methods=['POST'])
def transform_data():
    data = request.json
    source_df = pd.read_json(data['source'])
    target_schema = data['target_schema']
    mappings = data['mappings']
    transformations = data['transformations']
    
    # Apply field mappings
    for target_field, source_field in mappings.items():
        source_df[target_field] = source_df[source_field]
    
    # Apply transformations
    for field, transformation in transformations.items():
        # Example: concatenating first_name and last_name
        if transformation['type'] == 'concatenate':
            source_df[field] = source_df[transformation['fields']].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
    
    # Reorder columns to match target schema
    transformed_df = source_df[target_schema]
    
    return transformed_df.to_csv(index=False)

@app.route('/suggest_mappings', methods=['POST'])
def suggest_mappings():
    source_fields = request.json['source_fields']
    target_fields = request.json['target_fields']
    
    prompt = f"Suggest mappings from source fields {source_fields} to target fields {target_fields}"
    
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=100
    )
    
    suggestions = response.choices[0].text.strip().split('\n')
    mappings = {target: source for source, target in (suggestion.split('->') for suggestion in suggestions)}
    
    return jsonify(mappings)

if __name__ == '__main__':
    app.run(debug=True)
