# corpus.py ::::: Contient la classe CorpusC, qui gère la récupération des questions via l’API, le stockage et le nettoyage.

from datetime import datetime, timedelta
import requests
import json
import time
from questionClasses import RawQuestionC, CleanedQuestionC
from methodes import *
from collections import Counter
import numpy as np

today = datetime.today()
last_month = today - timedelta(days=3)
from_date = int(last_month.timestamp())
IGNORED_TOKENS = {"NUM", "LINK", "CODEBLOCK"}


class CorpusC:
    def __init__(self, name):
        print(f"📌 Initialisation du corpus '{name}'")
        self.name = name
        self.raw_questions = []
        self.cleaned_questions = []
        self.existing_ids = set()

    def func(self):
        print("📌 Création d'une instance de RawQuestion")

    def fetch_questions(self, access_token, api_key, pages=2):
        print("🚀 Début de la récupération des questions...")

        url = "https://api.stackexchange.com/2.3/questions"
        params = {
            "order": "desc",
            "sort": "votes",
            "fromdate": from_date,
            "filter": "withbody",
            "site": "stackoverflow",
            "pagesize": 50,
            "access_token": access_token,
            "key": api_key,
        }
        page = 1
        nouvelles_questions_ajoutées = 0
        Question_déjà_récupérée = 0
        while page <= pages:
            params["page"] = page
            print(f"📄 Récupération de la page {page}...")
            try:
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()
                rawData = response.json()
                print(f"🔍 Analyse des données de la page {page}...")
                if "items" in rawData:
                    for item in rawData["items"]:
                        question_id = item["question_id"]
                        if question_id not in self.existing_ids:
                            self.raw_questions.append(RawQuestionC(item))
                            self.existing_ids.add(question_id)
                            nouvelles_questions_ajoutées += 1
                        else:
                            Question_déjà_récupérée += 1
                if not rawData.get("has_more", False):
                    print("🚫 Plus de questions disponibles.")
                    break
            except requests.exceptions.RequestException as e:
                print(f"❌ Erreur réseau : {e}")
                break
            print(f"✅ Page {page} traitée.")
            print(f"📈 {nouvelles_questions_ajoutées} nouvelles questions ajoutées depuis le debout.")
            page += 1
            print("⏳ Pause de 15 secondes avant la prochaine page...")
            time.sleep(15)
        print(f"🎯 Fin de récupération : {nouvelles_questions_ajoutées} nouvelles questions ajoutées et ")
        print(f"🎯 Fin de récupération : {Question_déjà_récupérée} Questions déjà récupérées.")

    def save_raw_questions(self, filename="stackoverflow_questions.json"):
        print(f"💾 Sauvegarde des questions brutes dans {filename}...")
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(
                [q.to_dict() for q in self.raw_questions],
                file,
                ensure_ascii=False,
                indent=4,
            )
        print("✅ Sauvegarde terminée.")

    def load_raw_questions(self, filename="stackoverflow_questions.json"):
        print(f"📂 Chargement des questions brutes depuis {filename}...")
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.raw_questions = [RawQuestionC(q) for q in data]
                self.existing_ids = {q["question_id"] for q in data}
            print(f"✅ {len(self.raw_questions)} questions brutes chargées.")
        except FileNotFoundError:
            print("🚫 Aucune donnée brute trouvée.")

    def clean_questions(self):
        print("🛠 Nettoyage et indexation des questions...")
        index = len(self.cleaned_questions) + 1
        for raw in self.raw_questions:
            data = raw.to_dict()
            cleaned = CleanedQuestionC(
                index=index,
                question_id=data["question_id"],
                title=data["title"],
                body=data["body"],
                tags=data["tags"],
            )
            self.cleaned_questions.append(cleaned)
            index += 1
        print(f"✅ {len(self.cleaned_questions)} questions nettoyées et indexées.")

    def save_cleaned_questions(self, filename="clean_indexed.json"):
        print(f"💾 Sauvegarde des questions nettoyées dans {filename}...")
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(
                [q.to_dict() for q in self.cleaned_questions],
                file,
                ensure_ascii=False,
                indent=4,
            )
        print("✅ Sauvegarde terminée.")

    def load_cleaned_questions(self, filename="clean_indexed.json"):
        print(f"📂 Chargement des questions nettoyées depuis {filename}...")
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.cleaned_questions = [CleanedQuestionC(**q) for q in data]
            print(f"✅ {len(self.cleaned_questions)} questions nettoyées chargées.")
            return self.cleaned_questions
        except FileNotFoundError:
            print("🚫 Aucune donnée nettoyée trouvée.")
            return None

    def load_questions(self, filename):
        print(f"📂 Chargement des questions souhaité {filename}...")
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            print("🚫 Aucune donnée nettoyée trouvée.")
            return None
                      
    def save_questions(self, filename, data):  
        print(f"💾 Sauvegarde des questions souhaité {filename}...")
        with open (filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
                      
    def get_question_by_id(self, question_id):
        print(find_question_by_id(self, question_id))

    def get_question_by_tags(self, tag):
        print(find_question_by_tags(self, tag))

    def get_top_tags(self, top_n):
        print(most_common_tags(self, top_n))

    def deep_clean(self, keep_code):
        clean_TitleBody_ToText(self, keep_code)
         
    def wordsFrequency(self):
        print("📂 Calculate des frecuancy des mots")
        wordFrec(self)
    
      
         
class SearchEngine:
    def __init__(self, json_path='tokenized.json'):
        self.data = self._load_json(json_path)
        self.doc_ids = [q["question_id"] for q in self.data]
        self.docs = [self._build_full_text(q) for q in self.data]
        
        self.docs = [doc.split() for doc in self.docs]
        self.vocab = self._build_vocab()
        #print(self.vocab)
        self.tf = self._TF_Matrix()
        self.idf = self._IDF_Matrix()
        self.tfidf = self.tf * self.idf
        self.doc_norms = self._norms(self.tfidf)      
  

    def _load_json(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def _build_full_text(self, question):
        return question["text"] + " " + " ".join(question["tags"] * 2)
    
    def _build_vocab(self):
        vocab = {}
        index = 0
        for doc in self.docs :
            for word in doc :
                if word not in IGNORED_TOKENS :
                    word = word.lower()
                    if word not in vocab :
                        vocab[word] = index
                        index += 1
        return vocab
                
    def _TF_Matrix(self):
        tf = np.zeros((len(self.docs), len(self.vocab)))
        for i , doc in enumerate(self.docs):
            for word in doc :
                if word in self.vocab:
                    tf[i , self.vocab[word]] += 1
        return tf          
       
    def _IDF_Matrix(self):
        N = len(self.docs)
        df = np.zeros(len(self.vocab))
        for word , idx in self.vocab.items():
            for doc in self.docs:
                if word in doc:
                    df[idx] += 1 
        return np.log((N+1)/(df+1)) +1

    def _norms(self, matrix):
        return np.linalg.norm(matrix,axis=1)
        
    def _vectorise_query(self,query):
        tokens = query.lower().split()
        vec = np.zeros(len(self.vocab))
        for token in tokens :
            if token in self.vocab :
                vec[self.vocab[token]] += 1
        return vec * self.idf
    
    def _search(self, query):
        query_vec = self._vectorise_query(query)
        query_norm = np.linalg.norm(query_vec)
        similarities = []
        for i, doc_vec in enumerate(self.tfidf):
            dot_product = np.dot(query_vec, doc_vec)
            denom = query_norm * self.doc_norms[i]
            score = dot_product / denom if denom != 0 else 0.0
            similarities.append((self.doc_ids[i], score))
        similarities.sort(key=lambda x: x[1], reverse=True)
        return [(doc_id, score) for doc_id, score in similarities if score > 0]