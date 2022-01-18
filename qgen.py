import pickle
from pipelines import pipeline
nlp = pipeline("multitask-qa-qg", model="valhalla/t5-base-qa-qg-hl")
pickle.dump(nlp, open('model.pkl','wb'))