import unittest
from unittest.mock import MagicMock, patch
from human_agi_interface.intent_interpreter import IntentInterpreter

class TestIntentInterpreter(unittest.TestCase):
    def setUp(self):
        self.interpreter = IntentInterpreter()

    @patch('spacy.load')
    def test_initialization(self, mock_spacy_load):
        mock_spacy_load.return_value = MagicMock()
        interpreter = IntentInterpreter()
        self.assertIsNotNone(interpreter.nlp)

    @patch('spacy.load')
    def test_interpret(self, mock_spacy_load):
        mock_nlp = MagicMock()
        mock_doc = MagicMock()
        mock_token = MagicMock()
        mock_token.pos_ = "VERB"
        mock_token.lemma_ = "test"
        mock_doc.__iter__.return_value = [mock_token]
        mock_doc.ents = []
        mock_doc.sentiment = 0.5
        mock_nlp.return_value = mock_doc
        mock_spacy_load.return_value = mock_nlp

        interpreter = IntentInterpreter()
        result = interpreter.interpret({"data": "Test input"})

        self.assertIsNotNone(result)
        self.assertEqual(result['action'], "test")
        self.assertIsNone(result['subject'])
        self.assertIsNone(result['object'])
        self.assertEqual(result['entities'], [])
        self.assertEqual(result['sentiment'], 0.5)

    def test_interpret_no_nlp(self):
        self.interpreter.nlp = None
        result = self.interpreter.interpret({"data": "Test input"})
        self.assertIsNone(result)

    @patch('spacy.load')
    def test_extract_subject_and_object(self, mock_spacy_load):
        mock_nlp = MagicMock()
        mock_doc = MagicMock()
        mock_subj = MagicMock(dep_="nsubj", text="user")
        mock_obj = MagicMock(dep_="dobj", text="file")
        mock_doc.__iter__.return_value = [mock_subj, mock_obj]
        mock_doc.ents = []
        mock_doc.sentiment = 0
        mock_nlp.return_value = mock_doc
        mock_spacy_load.return_value = mock_nlp

        interpreter = IntentInterpreter()
        result = interpreter.interpret({"data": "User opens file"})

        self.assertEqual(result['subject'], "user")
        self.assertEqual(result['object'], "file")

    @patch('spacy.load')
    def test_extract_entities(self, mock_spacy_load):
        mock_nlp = MagicMock()
        mock_doc = MagicMock()
        mock_ent = MagicMock(text="John", label_="PERSON")
        mock_doc.ents = [mock_ent]
        mock_doc.__iter__.return_value = []
        mock_doc.sentiment = 0
        mock_nlp.return_value = mock_doc
        mock_spacy_load.return_value = mock_nlp

        interpreter = IntentInterpreter()
        result = interpreter.interpret({"data": "John is a person"})

        self.assertEqual(result['entities'], [("John", "PERSON")])

if __name__ == '__main__':
    unittest.main()