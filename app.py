from flask import Flask, render_template, request, redirect, url_for
import csv
from datetime import datetime
import os

app = Flask(__name__)
global_name = None
global_file_name = None

# Load questions from CSV
def load_questions(question_file):
    questions = []
    with open(question_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            questions.append(row)
    return questions

# Save the rating to a CSV file with a timestamp in the name
def save_rating(preference, question_id):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"ratings/ratings_{global_name}_{global_file_name}.csv"
    file_exists = os.path.isfile(filename)

    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['question_id', 'preference']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()
        
        writer.writerow({'question_id': question_id, 'preference': preference})


@app.route('/', methods=['GET', 'POST'])
def get_name():
    if request.method == 'POST':
        global global_name
        global global_file_name
        global_name = request.form.get('name')
        global_file_name = request.form.get('file_name')
        return redirect(url_for('index'))
    return render_template('name.html')

def get_next_question_id():
    # Track the question ID within the session
    if 'current_question_id' not in get_next_question_id.__dict__:
        get_next_question_id.current_question_id = 0  # Initialize the question ID
    return get_next_question_id.current_question_id

@app.route('/rate', methods=['GET', 'POST'])
def index():
    if not global_name or not global_file_name:
        return redirect('/')  # Redirect to form page if name is not provided
    
    questions = load_questions("questions/"+global_file_name+"_questions.csv")
    question_id = get_next_question_id()

    if request.method == 'POST':
        preference = request.form.get('preference')
        if not preference:
            return "No preference selected", 400

        current_question = questions[question_id]
        save_rating(preference, current_question['question_id'])
        question_id += 1
        get_next_question_id.current_question_id = question_id

        if question_id >= len(questions):
            return "Thank you for completing the ratings...!"

    current_question = questions[question_id]
    return render_template('index.html', question=current_question, name=global_name)

if __name__ == '__main__':

    app.run(debug=True)
