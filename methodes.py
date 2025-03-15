from collections import Counter , defaultdict
from corpus import *
import json
from questionClasses import CleanedQuestionC, RawQuestionC
import re
import nltk
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from tqdm import tqdm
import time

# Télécharger les ressources nécessaires pour NLTK
nltk.download("stopwords")
nltk.download("wordnet")

# Initialiser les stopwords 
stop_words = set(stopwords.words("english"))

# Liste des termes spécifiques à ne pas modifier
special_terms = [
    "C++",
    "C#",
    "JavaScript",
    "Python",
    "Ruby",
    "Java",
    "R",
    "Go",
    "Swift",
    "Kotlin",
    "Rust",
    "PHP",
    "TypeScript",
    "Perl",
    "Haskell",
    "Lua",
    "Scala",
    "Objective-C",
    "F#",
    "MATLAB",
    "TensorFlow.js",
    "Node.js",
    "p5.js",
    "React.js",
    "react",
    "React-Native",
    "Angular",
    "Vue.js",
    "Django",
    "Flask",
    "Ruby on Rails",
    "Laravel",
    "Spring Framework",
    ".NET",
    "Express.js",
    "Svelte",
    "Bootstrap",
    "jQuery",
    "Foundation",
    "H2O",
    "Scikit-learn",
    "PyTorch",
    "Theano",
    "XGBoost",
    "LightGBM",
    "Pandas",
    "NumPy",
    "Matplotlib",
    "Seaborn",
    "Keras",
    "OpenCV",
    "Scipy",
    "NLTK",
    "SpaCy",
    "Gensim",
    "HTML",
    "CSS",
    "SQL",
    "XML",
    "JSON",
    "YAML",
    "CSV",
    "REST",
    "GraphQL",
    "OAuth",
    "JWT",
    "Docker",
    "Kubernetes",
    "CI/CD",
    "Git",
    "Azure",
    "AWS",
    "GCP",
    "Terraform",
    "Blockchain",
    "Bootstrap",
    "Tailwind CSS",
    "Bulma",
    "Foundation",
    "Materialize",
    "Tailwind",
    "SQLAlchemy",
    "GitHub",
    "Jupyter",
    "TensorFlow",
    "ChatGPT",
    "Vercel",
    "Sass",
    "Figma",
    "PostgreSQL",
    "MongoDB",
    "Firebase",
    "AWS Lambda",
    "Google Cloud",
    "Heroku",
    "Kali Linux",
    "RedHat",
    "Ubuntu",
    "Fedora",
    "Debian",
    "CentOS",
    "Anaconda",
    "PyInstaller",
    "Flask-RESTful",
    "Django REST Framework",
    "NUM",
    "LINK",
    "CODEBLOCK",
]


def find_question_by_id(self, id):
    n = 0
    indices_list = []
    print("📂 Recherche une question par ID ...")
    searchIds = self.load_cleaned_questions()
    if searchIds is not None:
        for question in searchIds:
            if id == question.question_id:
                indices_list.append(question.index)
                n += 1
            else:
                continue
        return f"📊 {n} Questions trouvée par ID in : {indices_list}"
    else:
        return "🚫 Aucune donnée disponible."


def find_question_by_tags(self, tag):
    n = 0
    tags_list = []
    print("📂 Recherche une question par tag ...")
    searchTags = self.load_cleaned_questions()
    if searchTags is not None:
        for question in searchTags:
            if tag.lower() in question.tags:
                tags_list.append(question.index)
                n += 1
            else:
                continue
        return f"📊 {n} Questions trouvée par tags in : {tags_list}"
    else:
        return "🚫 Aucune donnée disponible."


def most_common_tags(self, top_n):
    print("📂 Recherche des tags les plus fréquents...")
    common_tags = self.load_cleaned_questions()
    if common_tags is not None:
        all_tags = []
        for question in common_tags:
            all_tags.extend(question.tags)
        counter = Counter(all_tags)
        return ("📊 Tags les plus fréquents :", str(counter.most_common(top_n)))
    else:
        return "🚫 Aucune donnée disponible."


def clean_TitleBody_ToText(self, keep_code):
    newlist = []
    data = self.load_questions("clean_indexed.json")
    
    for q in data:
        toBeCleaned_text = (q["title"] + " " + q["body"]) 
        toBeCleaned_text = tokenizer(toBeCleaned_text, keep_code)
        one = {  # Utiliser un dictionnaire pour `one`
            "index": q["index"],
            "question_id": q["question_id"],
            "text": toBeCleaned_text,
            "tags": q["tags"],
        }
        newlist.append(one)
    
    self.save_questions("tokenized.json", newlist)      


def tokenizer(text, keep_code):

    ## 1. Remplacer les balises <pre>, <pre><code>, <pre class=...>, <code> par "CODEBLOCK"
    if keep_code:
        text = re.sub(r"<pre.*?>.*?</pre>", " CODEBLOCK ", text, flags=re.DOTALL)  # Remplacer tout <pre> (toutes les variantes)
        text = re.sub(r"<code.*?>.*?</code>", " CODEBLOCK ", text, flags=re.DOTALL)  # Remplacer tout <code> par CODEBLOCK
    else:
        text = re.sub(r"<pre.*?>.*?</pre>", " ", text, flags=re.DOTALL)
        text = re.sub(r"<code.*?>.*?</code>", " ", text, flags=re.DOTALL) 

    ## 2. Remplacer les liens <a> par LINK + texte du lien
    soup = BeautifulSoup(text, "html.parser")
    
    for a in soup.find_all("a"):
        if a.get("href", "").startswith("http"):  # Vérifie si le lien commence par "http"
            a.replace_with(" LINK ")  # Remplace par "LINK" sans garder le texte
        elif a.string:  # Vérifie qu'il y a du texte dans le lien
            link_text = a.get_text()
            a.replace_with(f" LINK {link_text} ")  # Remplace par "LINK" + texte du lien
        else:
            a.replace_with(" LINK ")  # Si le lien n'a pas de texte visible
    
    ## Convertir de nouveau en texte
    text = str(soup)
    
    ## 3. Supprimer toutes les balises HTML restantes
    text = BeautifulSoup(text, "html.parser").get_text(separator=" ")
    
    ## 4. Remplacer les nombres par 'NUM'
    text = re.sub(r"\d+", " NUM ", text) 
    
    ## 5. Supprimer les espaces supplémentaires
    text = re.sub(r'\s+', ' ', text)
    
    ## 6. Convertir tout en minuscule sauf les Termes spéciaux
    text = text.split()
    text = [word.lower() if word not in special_terms else word for word in text]
    
    ## 7. Nettoyer normalement
    text = [re.sub(r"[^a-zA-Z0-9]", " ", word) if word not in special_terms else word for word in text]
    
    ## 8. Supprimer les stopwords sauf si le mot est dans les Termes spéciaux
    text = [word for word in text if word.lower() in special_terms or word not in stop_words]
    
    ## 9. Suppression des tokens d’un seul caractère sauf ceux dans les Termes spéciaux
    text = [word for word in text if len(word) > 2 or word in special_terms]
    
    ## Recomposer le texte
    text = " ".join(text)
     
    ## 10. Les étaps 7 et 8 et 9 sont répétées pour s'assurer     
    text = text.split()    
    text = [word for word in text if len(word) > 2 or word in special_terms]
    text = [word for word in text if word.lower() in special_terms or word not in stop_words]
    text = [re.sub(r"[^a-zA-Z0-9]", " ", word) if word not in special_terms else word for word in text]
    
    ## Recomposer le texte
    text = " ".join(text)
    
    return text

    
def wordFrec(self):
    data = self.load_questions("tokenized.json")
    wordFrec = {}
    for q in tqdm(data, desc="Traitement des éléments"):
        words = q["text"].split()
        for word in words:
            if word in wordFrec:
                wordFrec[word] += 1
            else:
                wordFrec[word] = 1
        time.sleep(0.05) 

    self.save_questions("wordFrec.json", dict(wordFrec))
