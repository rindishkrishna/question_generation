from flask import Flask,render_template, request
# import pickle
app = Flask(__name__)

@app.route("/")
def main():
  return render_template('index.html')

@app.route('/questions-generated', methods=['POST'])
def home():
    if request.method == 'POST':
      if request.form['generate']:
        data = request.form['a']
        # model = pickle.load(open('model.pkl','rb'))
        # l=model(data)
        list=[{'answer': 'Python',
  'question': 'What is an interpreted, high-level, general-purpose programming language?'},
 {'answer': 'Guido van Rossum', 'question': 'Who created Python?'}]
        return render_template('answer.html', data=list)
    else:
      return    

if __name__ == "__main__":
  app.run(debug=True) 