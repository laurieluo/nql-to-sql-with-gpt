import openai
import json
from sqlquerylib import *
from flask import Flask, render_template, request

openai.api_key = open('key.txt', 'r').read().strip()
def get_completion(prompt, model):
    messages = [{'role': 'user', 'content': prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.5,
    )
    return response.choices[0].message['content']

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

# Conduct NQL
@app.route('/execute_text', methods=['POST'])
def execute_text():
    content = request.get_json()
    text = content['text']
    model = 'gpt-4'
    prompt = open('prompt_nql.txt').read()
    result = get_completion(prompt%text, model=model)
    result = json.loads(result)

    # Create the table header
    html_table = '<table>\n'
    html_table += '<tr>'
    for column_name in result[0].keys():
        html_table += '<th>{}</th>'.format(column_name)
    html_table += '</tr>\n'

    # Create the table rows
    for row in result:
        html_table += '<tr>'
        for (key, value) in row.items():
            html_table += '<td>{}</td>'.format(value)
        html_table += '</tr>\n'

    # End of the table header
    html_table += '</table>'
    data = {'table': html_table}
    return json.dumps(data)

# Generate SQL with chatGPT prompt engineering
@app.route('/text_to_sql', methods=['POST'])
def text_to_sql():
    content = request.get_json()
    text = content['text']
    model = content['model']
    prompt = open('prompt_sql.txt').read()
    result = get_completion(prompt%text, model=model)
    return {'result': result}

# Execute the SQL query and return the table or error information
@app.route('/execute_code', methods=['POST'])
def execute_code():
    content = request.get_json()
    query = content['query']

    try:
        result = executeSQL(query)
    except Exception as exception:
        result = f'<p style="color: red;"> Query is failed! </p><{exception}>'

    data = {'table': result}
    return json.dumps(data)

if __name__ == '__main__':
    app.run(debug=True)
