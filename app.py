from flask import Flask,render_template, request
import pickle
app = Flask(__name__)

@app.route("/")
def main():
  return render_template('index.html')

@app.route('/result', methods=['POST'])
def home():
    if request.method == 'POST':
      if request.form.get("generate"):
        data = request.form['a']
        model = pickle.load(open('model-latest.pkl','rb'))
        print("befor cleaning: "+data)
        quoted_text = '"""' + data + '"""'
        print("quoted text: "+quoted_text)
        Ctext = clean(quoted_text,
        fix_unicode=True,               # fix various unicode errors
        to_ascii=True,                  # transliterate to closest ASCII representation
        lower=False,                     # lowercase text
        no_line_breaks=False,           # fully strip line breaks as opposed to only normalizing them
        no_urls=True,                  # replace all URLs with a special token
        no_emails=False,                # replace all email addresses with a special token
        no_phone_numbers=False,         # replace all phone numbers with a special token
        no_numbers=False,               # replace all numbers with a special token
        no_digits=False,                # replace all digits with a special token
        no_currency_symbols=False,      # replace all currency symbols with a special token
        no_punct=False,                 # remove punctuations
        replace_with_punct="",          # instead of removing punctuations you may replace them
        replace_with_url="<URL>",
        replace_with_email="<EMAIL>",
        replace_with_phone_number="<PHONE>",
        replace_with_number="<NUMBER>",
        replace_with_digit="0",
        replace_with_currency_symbol="<CUR>",
        lang="en"                       # set to 'de' for German special handling
        )
        print("after cleaning: "+Ctext)
        l=model(Ctext)
        return render_template('answer.html', data=l)
      elif request.form.get("summary"):
         data = request.form['a']
         model = pickle.load(open('abstraction-model.pkl','rb'))
         summarized_text1 = summarizer1(data,model,summary_tokenizer)
         summarized_text2 = summarizer2(data,model,summary_tokenizer)
         final_text=summarized_text1+summarized_text2  
         return render_template('summary.html', data=final_text)   
if __name__ == "__main__":
  app.run(debug=True) 