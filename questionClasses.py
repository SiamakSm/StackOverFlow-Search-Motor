# questionClasses.py :::: Définit les classes RawQuestionC (questions brutes) et CleanedQuestionC (questions nettoyées).


class RawQuestionC:
    def __init__(self, data):
        # print("📌 Création d'une instance de RawQuestion")
        self.data = data

    def to_dict(self):
        return self.data


class CleanedQuestionC:
    def __init__(self, index, question_id, title, body, tags):
        # print(f"📌 Création de CleanedQuestion pour ID {question_id}")
        self.index = index
        self.question_id = question_id
        self.title = title
        self.body = body
        self.tags = tags

    def to_dict(self):
        return {
            "index": self.index,
            "question_id": self.question_id,
            "title": self.title,
            "body": self.body,
            "tags": self.tags,
        }
