from flask import Flask,render_template, request
from cleantext import clean
import pickle
app = Flask(__name__)

import torch


def summarizer1(text,model,tokenizer):
  text = text.strip().replace("\n"," ")
  text = "summarize: "+text

  max_len = 512
  encoding = tokenizer.encode_plus(text,max_length=max_len, pad_to_max_length=True,truncation=True, return_tensors="pt").to(device)

  input_ids, attention_mask = encoding["input_ids"], encoding["attention_mask"]

  outs = model.generate(input_ids=input_ids,
                                  attention_mask=attention_mask,
                                  early_stopping=True,
                                  num_beams=3,
                                  num_return_sequences=1,
                                  no_repeat_ngram_size=2,
                                  min_length = 75,
                                  max_length=300)


  dec = [tokenizer.decode(ids,skip_special_tokens=True) for ids in outs]
  summary = dec[0]
  summary = postprocesstext(summary)
  summary= summary.strip()

  return summary

def summarizer2(text,model,tokenizer):
  text = text.strip().replace("\n"," ")
  text = "summarize: "+text
  max_len = 512
  encoding = tokenizer.encode_plus(text,max_length=max_len, pad_to_max_length=True,truncation=True, return_tensors="pt").to(device)

  input_ids, attention_mask = encoding["input_ids"], encoding["attention_mask"]

  outs = model.generate(input_ids=input_ids,
                                  attention_mask=attention_mask,
                                  early_stopping=True,
                                  num_beams=3,
                                  num_return_sequences=2,
                                  no_repeat_ngram_size=1,
                                  min_length = 75,
                                  max_length=512)


  dec = [tokenizer.decode(ids,skip_special_tokens=True) for ids in outs]
  summary = dec[0]
  summary = postprocesstext(summary)
  summary= summary.strip()

  return summary

@app.route("/")
def main():
  return render_template('index.html')

# @app.route("/error")
# def hi():
#   data = request.form['a']
#   return render_template('error.html')

@app.route('/questions-generated', methods=['POST'])
def home():
    if request.method == 'POST':
      if request.form.get("generate"):
        data = request.form['a']
        model = pickle.load(open('model.pkl','rb'))
        # print("befor cleaning: "+data)
        quoted_text = '"""' + data + '"""'
        # print("quoted text: "+quoted_text)
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
        l=model(Ctext)
        return render_template('answer.html', data=l)
      elif request.form.get("try_again"):
        print("executed")
        data = request.form['a']
        model = pickle.load(open('model.pkl','rb')) 
        quoted_text = '"""' + data + '"""'
        Ctext = clean(quoted_text,
        fix_unicode=True,               # fix various unicode errors
        to_ascii=True,                  # transliterate to closest ASCII representation
        lower=False,                     # lowercase text
        no_line_breaks=False,           # fully strip line breaks as opposed to only normalizing them
        no_urls=True,                  # replace all URLs with a special token
        no_emails=False,                # replace all email addresses with a special token
        no_phone_numbers=False,         # replace all phone numbers with a special token
        no_numbers=True,               # replace all numbers with a special token
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
        l=model(Ctext)
        return render_template('answer.html', data=l)  
      elif request.form.get("summary"):
         data = request.form['a']
         model = pickle.load(open('abstraction-model.pkl','rb'))
         summarized_text1 = summarizer1(data,model,summary_tokenizer)
         summarized_text2 = summarizer2(data,model,summary_tokenizer)
         final_text=summarized_text1+summarized_text2  
         return render_template('summary.html', data=final_text)
    else:
      return "Please try uploading the picture with maximum contrast edit and/or edit the text so that there are no extra spaces/symbols"      
@app.errorhandler(500)
def internal_error(error):
    data = request.form['a']
    print("data"+data)
    return render_template('error.html', data=data)       
if __name__ == '__main__':
 app.run()