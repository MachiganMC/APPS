import unittest
from package.functional.data import Data
from package.functional.profil import Profil
from package.functional.question import Question


class TestData(unittest.TestCase):
    def test_init(self):
        with self.assertRaises(ValueError):
            Data("", "mdp", "google")
        with self.assertRaises(ValueError):
            Data("", "mdp", "google", "commentaire")
        with self.assertRaises(ValueError):
            Data("", "mdp", "google", None)

        with self.assertRaises(ValueError):
            Data("name", "", "google")
        with self.assertRaises(ValueError):
            Data("name", "", "google", "commentaire")
        with self.assertRaises(ValueError):
            Data("name", "", "google", None)

        with self.assertRaises(ValueError):
            Data("name", "mdp", "")
        with self.assertRaises(ValueError):
            Data("name", "mdp", "", "commentaire")
        with self.assertRaises(ValueError):
            Data("name", "mdp", "", None)

        raised: bool
        try:
            Data("name", "mdp", "service")
            raised = False
        except ValueError:
            raised = True
        self.assertFalse(raised)

        raised: bool
        try:
            Data("name", "mdp", "service", "comment")
            raised = False
        except ValueError:
            raised = True
        self.assertFalse(raised)

    def test_to_dict(self):
        data: Data = Data("name", "mdp", "service")
        data_dict: dict = data.to_dict()
        self.assertTrue("username" in data_dict)
        self.assertTrue("password" in data_dict)
        self.assertTrue("service" in data_dict)
        self.assertTrue("comment" in data_dict)

    def test_from_dict(self):
        data_dict: dict[str: str] = {
            "username": "name",
            "password": "pw",
            "service": "service",
            "comment": "comment"
        }
        data: Data = Data.from_dict(data_dict)
        self.assertEqual(data_dict["username"], data.username)
        self.assertEqual(data_dict["password"], data.password)
        self.assertEqual(data_dict["service"], data.service)
        self.assertEqual(data_dict["comment"], data.comment)

        with self.assertRaises(KeyError):
            data_dict.pop("username")
            Data.from_dict(data_dict)
        with self.assertRaises(KeyError):
            data_dict.pop("password")
            data_dict["username"] = "name"
            Data.from_dict(data_dict)
        with self.assertRaises(KeyError):
            data_dict.pop("service")
            data_dict["password"] = "pw"
            Data.from_dict(data_dict)
        with self.assertRaises(KeyError):
            data_dict.pop("comment")
            data_dict["service"] = "service"
            Data.from_dict(data_dict)

    def test_setter(self):
        data: Data = Data("name", "pw", "service", "comment")

        data.username = "new name"
        self.assertEqual(data.username, "new name")
        with self.assertRaises(ValueError):
            data.username = ""

        data.password = "new password"
        self.assertEqual(data.password, "new password")
        with self.assertRaises(ValueError):
            data.password = ""

        data.service = "new service"
        self.assertEqual(data.service, "new service")
        with self.assertRaises(ValueError):
            data.service = ""


class TestProfil(unittest.TestCase):
    # utilisée pour les tests
    __question: Question = Question(0, "answer")

    def test_new_profil(self):
        try:
            # on crée un profil et on l'enregistre, pour tester si 2 profils avec 2 mêmes noms peuvent coexister
            profil: Profil = Profil.new_profil("name", TestProfil.__question)
            profil.save("mdp", "answer")
        except ValueError:
            pass
        with self.assertRaises(ValueError):
            Profil.new_profil("", TestProfil.__question)
        with self.assertRaises(ValueError):
            Profil.new_profil("name", TestProfil.__question)
        
        raised: bool
        try:
            Profil.new_profil("test", TestProfil.__question)
            raised = False
        except ValueError:
            raised = True
        self.assertFalse(raised)

    def test_get_from_dict(self):
        profil_dict: dict = {
            "name": "name",
            "question_index": 0,
            "data": [{"username": "name", "password": "pw", "service": "service", "comment": ""}]
        }
        raised: bool
        try:
            Profil.get_from_dict(profil_dict)
            raised = False
        except KeyError:
            raised = True
        self.assertFalse(raised)

        with self.assertRaises(KeyError):
            profil_dict.pop("name")
            Profil.get_from_dict(profil_dict)

        with self.assertRaises(KeyError):
            profil_dict["name"] = "name"
            profil_dict.pop("question_index")
            Profil.get_from_dict(profil_dict)

        with self.assertRaises(KeyError):
            profil_dict["question_index"] = 0
            profil_dict = {
                "name": "name",
                "question_index": 0
            }
            Profil.get_from_dict(profil_dict)

    def test_encrypt(self):
        import cryptocode
        profil: Profil = Profil.new_profil("test", TestProfil.__question)
        profil.entries.append(Data("name", "pw", "service"))
        with self.assertRaises(ValueError):
            profil.encrypt("", "")
        with self.assertRaises(ValueError):
            profil.encrypt("", "test")
        with self.assertRaises(ValueError):
            profil.encrypt("test", "")

        encrypted: tuple[str, str] = profil.encrypt("pw", "answer")
        self.assertTrue(cryptocode.decrypt(encrypted[0], "pw"))
        self.assertTrue(cryptocode.decrypt(encrypted[1], "answer"))

    def test_save(self):
        import os
        try:
            # suppression du fichier pour pouvoir tester plusieurs fois
            os.remove("data/test_profil.alz")
        except FileNotFoundError:
            pass
        Profil.new_profil("test_profil", TestProfil.__question).save("pw", "answer")
        raised: bool
        try:
            open("data/test_profil.alz", "r")
            raised = False
        except FileNotFoundError:
            raised = True
        self.assertFalse(raised)

    def test_get_from_password(self):
        import os
        from package.functional.profil import hash_str
        try:
            # suppression du fichier pour pouvoir tester plusieurs fois
            os.remove("data/test_profil.alz")
        except FileNotFoundError:
            pass
        with self.assertRaises(ValueError):
            Profil.get_from_password("test_profil", "pw")

        profil: Profil = Profil.new_profil("test_profil", TestProfil.__question)
        profil.save(hash_str("pw"), hash_str("answer"))

        with self.assertRaises(ValueError):
            Profil.get_from_password("test_profil", "mauvais_pw")

        profil_copy: Profil = Profil.get_from_password("test_profil", "pw")
        self.assertEqual(profil.name, profil_copy.name)

    def test_all_profil_str(self):
        import os
        try:
            for file in os.listdir("data"):
                os.remove("data/" + file)
            os.removedirs("data")
        except NameError:
            pass

        raised: bool
        try:
            Profil.all_profil_str()
            raised = False
        except FileNotFoundError:
            raised = True
        self.assertFalse(raised)

        # un dossier a été créé entre temps, on teste maintenant une autre partie de la fonction
        raised: bool
        try:
            Profil.all_profil_str()
            raised = False
        except FileNotFoundError:
            raised = True
        self.assertFalse(raised)

        try:
            for file in os.listdir("data"):
                os.remove(file)
            os.removedirs("data")
        except FileNotFoundError:
            pass
        raised: bool
        try:
            Profil.all_profil_str()
            raised = False
        except FileNotFoundError:
            raised = True
        self.assertFalse(raised)

    def test_get_from_question(self):
        import os
        from package.functional.profil import hash_str
        try:
            # suppression pour pouvoir tester plusieurs fois
            os.remove("data/test_profil.alz")
        except FileNotFoundError:
            pass
        with self.assertRaises(ValueError):
            Profil.get_from_question("test_profil", "answer")

        profil: Profil = Profil.new_profil("test_profil", TestProfil.__question)
        profil.save(hash_str("pw"), hash_str("answer"))

        with self.assertRaises(ValueError):
            Profil.get_from_question("test_profil", "mauvaise_answer")

        profil_copy: Profil = Profil.get_from_question("test_profil", "answer")
        self.assertEqual(profil.name, profil_copy.name)

    def test_get_question_from_str(self):
        import os
        try:
            os.remove("data/test_profil.alz")
        except FileNotFoundError:
            pass

        with self.assertRaises(ValueError):
            Profil.get_question_from_str("test_profil")

        Profil.new_profil("test_profil", TestProfil.__question).save("pw", "answer")
        question: str = Profil.get_question_from_str("test_profil")
        self.assertEqual(TestProfil.__question.question, question)

    def test_getter(self):
        profil: Profil = Profil.new_profil("test", TestProfil.__question)
        self.assertEqual(profil.name, "test")
        self.assertEqual(profil.entries, [])
        self.assertEqual(profil.question_index, TestProfil.__question.index)


class TestQuestion(unittest.TestCase):
    def test_init(self):
        with self.assertRaises(ValueError):
            Question(0, "")

        with self.assertRaises(ValueError):
            '''
            Pour une raison que j'ignore, ce test n'ai pas pris en compte dans
            le coverage. Il permet de tester si l'index de la liste des questions
            est valide ou pas (ici non).
            '''
            Question(-1, "")

        raised: bool
        try:
            Question(0, "answer")
            raised = False
        except ValueError:
            raised = True
        self.assertFalse(raised)

    def test_getter(self):
        question: Question = Question(0, "answer")
        self.assertEqual(question.question, Question.all_questions[0])
        self.assertEqual(question.index, 0)
        self.assertEqual(question.answer, "answer")

    def test_setter(self):
        question: Question = Question(0, "answer")
        question.answer = "new_answer"
        self.assertEqual(question.answer, "new_answer")
        with self.assertRaises(ValueError):
            question.answer = ""


if __name__ == '__main__':
    import os

    try:
        os.makedirs("data")
    except FileExistsError:
        pass
    unittest.main()
