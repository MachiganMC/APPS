class Question:
    all_questions: list[str] = [
        "Quelle est votre couleur préférée ?",
        "Quel est le nom de votre premier animal de compagnie ?",
        "Quelle est votre ville de naissance ?"
    ]

    __question: str
    __answer: str
    ___index: int

    def __init__(self, index: int, answer: str):
        try:
            self.__question = Question.all_questions[index]
            self.___index = index
        except IndexError:
            raise ValueError("L'index ne correspond à aucune question")

        self.__answer = answer

    @property
    def question(self) -> str:
        return self.__question

    @property
    def answer(self) -> str:
        return self.__answer

    @property
    def index(self) -> int:
        return self.___index

    @question.setter
    def question(self, question: str) -> None:
        self.__question = question

    @answer.setter
    def answer(self, answer: str) -> None:
        self.__answer = answer



