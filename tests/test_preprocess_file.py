# tests/test_preprocess_file.py

import unittest
from utils.preprocess import preprocess_file_content

class TestPreprocessFileContent(unittest.TestCase):
    def test_preprocess_file_content_basic(self):
        input_text = "I absolutely love this! It's fantastic and works great."
        expected_output = "absolutely love fantastic works great"
        self.assertEqual(preprocess_file_content(input_text, apply_stemming=False), expected_output)

    def test_preprocess_file_content_with_stemming(self):
        input_text = "Running runs ran runner easily"
        expected_output = "run run ran runner easili"  # Assuming PorterStemmer
        self.assertEqual(preprocess_file_content(input_text, apply_stemming=True), expected_output)

    def test_preprocess_file_content_empty(self):
        input_text = "   "
        with self.assertRaises(ValueError):
            preprocess_file_content(input_text)

    def test_preprocess_file_content_non_string(self):
        input_text = None
        with self.assertRaises(TypeError):
            preprocess_file_content(input_text)

    def test_preprocess_file_content_full_content(self):
        input_text = """Technology has transformed the way we live, work, and communicate.
Over the past few decades, advancements in science and technology have revolutionized industries,
reshaped economies, and fundamentally altered daily life."""
        expected_output = "technolog transform way live work communic past decad advanc scienc technolog revolution industri reshap economi fundament alter daili life"
        self.assertEqual(preprocess_file_content(input_text, apply_stemming=True), expected_output)

if __name__ == '__main__':
    unittest.main()
