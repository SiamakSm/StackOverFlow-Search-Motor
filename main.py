# main.py :::: Point d’entrée du programme. Il utilise CorpusC pour récupérer, nettoyer et sauvegarder les questions.

from corpus import *
from corpus import SearchEngine

def main():

    access_token = "THA20obO92R6Ypx4rvw18w))"
    api_key = "rl_7QCUyb7FnDge43E41ooisGKHf"
    
    corpusObjet = CorpusC("StackOverflow")
    motorObjet = SearchEngine()
    
    access_token = "THA20obO92R6Ypx4rvw18w))"
    api_key = "rl_7QCUyb7FnDge43E41ooisGKHf"
    #print("-------------------------------------------------------------")
    #print("-----------------    Class StackOverflow    -----------------\n")
    #corpusObjet = CorpusC("StackOverflow")
    #print("-------------------------------------------------------------")
    #print("-----------------    load_raw_questions    -----------------\n")
    #corpusObjet.load_raw_questions()
    #print("-------------------------------------------------------------")
    #print("-----------------    fetch_questions    -----------------\n")
    #corpusObjet.fetch_questions(access_token, api_key)
    #print("-------------------------------------------------------------")
    #print("-----------------    save_raw_questions    -----------------\n")
    #corpusObjet.save_raw_questions()
    #print("-------------------------------------------------------------")
    #print("-----------------    load_cleaned_questions    -----------------\n")
    #corpusObjet.load_cleaned_questions()
    #print("-------------------------------------------------------------")
    #print("-----------------    clean_questions    -----------------\n")
    #corpusObjet.clean_questions()
    #print("-------------------------------------------------------------")
    #print("-----------------    save_cleaned_questions    ----------------\n")
    #corpusObjet.save_cleaned_questions()   
    #print("-------------------------------------------------------------")
    #print("-----------------    get_question_by_id    -----------------\n")
    #corpusObjet.get_question_by_id(79455901)
    print("-------------------------------------------------------------")
    print("-----------------    get_question_by_tags    -----------------\n")
    corpusObjet.get_question_by_tags("c++")
    print("-------------------------------------------------------------")
    print("-----------------    get_top_tags    -----------------\n")
    corpusObjet.get_top_tags(5)
    #print("-------------------------------------------------------------")
    #print("-----------------    deep_clean    -----------------\n")
    #corpusObjet.deep_clean(True)
    print("-------------------------------------------------------------")
    print("-----------------    wordsFrequency    -----------------\n")
    corpusObjet.wordsFrequency()
    print("-------------------------------------------------------------")
    print("-----------------    SearchEngine    -----------------\n")
    results = motorObjet._search("library making list")
    for doc_id, score in results:
        print(f"Document ID: {doc_id} → Similarité : {score:.3f}")
    
    
    
    
if __name__ == "__main__":
    main()
