import unittest

import pytest

from langchain_community.document_loaders.parsers.language.swift import SwiftSegmenter

@pytest.mark.requires("tree_sitter", "tree_sitter_languages")
class TestSwiftSegmenter(unittest.TestCase):
    def setUp(self) -> None:
        self.example_code = """
        func sayHello(name: String) -> String {
            return "Hello, \\(name)!"
        }

        class Person {
            var name: String
            init(name: String) {
                self.name = name
            }
        }

        struct Rectangle {
            var width: Double
            var height: Double
            func area() -> Double {
                return width * height
            }
        }

        enum Direction {
            case north, south, east, west
        }
        """

        self.expected_simplified_code = """// Code for: func sayHello(name: String) -> String
// Code for: class Person
// Code for: struct Rectangle
// Code for: enum Direction"""

        self.expected_extracted_code = [
            'func sayHello(name: String) -> String {\n    return "Hello, \\(name)!"\n}',
            "class Person {\n    var name: String\n    init(name: String) {\n        self.name = name\n    }\n}",
            "struct Rectangle {\n    var width: Double\n    var height: Double\n    func area() -> Double {\n        return width * height\n    }\n}",
            "enum Direction {\n    case north, south, east, west\n}",
        ]

    def test_is_valid(self) -> None:
        self.assertTrue(SwiftSegmenter("let greeting = \"Hi\"").is_valid())
        self.assertFalse(SwiftSegmenter("random text").is_valid())

    def test_extract_functions_classes(self) -> None:
        segmenter = SwiftSegmenter(self.example_code)
        extracted_code = segmenter.extract_functions_classes()
        self.assertEqual(extracted_code, self.expected_extracted_code)

    def test_simplify_code(self) -> None:
        segmenter = SwiftSegmenter(self.example_code)
        simplified_code = segmenter.simplify_code()
        self.assertEqual(simplified_code, self.expected_simplified_code)