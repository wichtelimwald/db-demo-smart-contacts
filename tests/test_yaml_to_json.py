import json
import tempfile
import textwrap
import unittest
from pathlib import Path

from yaml_to_json import main


class YamlToJsonTests(unittest.TestCase):
    def run_conversion(self, yaml_content: str) -> dict:
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "contacts.yaml"
            output_path = Path(temp_dir) / "contacts.json"
            input_path.write_text(textwrap.dedent(yaml_content).strip() + "\n", encoding="utf-8")

            main(input_path, output_path)

            return json.loads(output_path.read_text(encoding="utf-8"))

    def assert_conversion_fails(self, yaml_content: str, expected_message: str) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "contacts.yaml"
            output_path = Path(temp_dir) / "contacts.json"
            input_path.write_text(textwrap.dedent(yaml_content).strip() + "\n", encoding="utf-8")

            with self.assertRaises(SystemExit) as context:
                main(input_path, output_path)

        self.assertIn(expected_message, str(context.exception))

    def test_happy_path_converts_contacts_groups_and_related_ids(self):
        result = self.run_conversion(
            """
            contacts:
              - id: 1
                name: Leia Organa
                groups:
                  - Rebel Alliance
                related_to:
                  - id: 2
                    relation: Bruder
              - id: 2
                name: Luke Skywalker
                groups:
                  - Rebel Alliance
                  - Jedi
            """
        )

        self.assertEqual(2, len(result["contacts"]))
        self.assertEqual([2], result["contacts"][0]["relatedTo"])
        self.assertEqual(
            {"id": 2, "name": "Luke Skywalker", "knownPreferences": [], "relatedTo": []},
            result["contacts"][1],
        )
        self.assertEqual(
            [
                {"id": 1, "name": "Rebel Alliance"},
                {"id": 2, "name": "Jedi"},
            ],
            result["groups"],
        )
        self.assertEqual(
            [
                {"id": 1, "contact_id": 1, "group_id": 1},
                {"id": 2, "contact_id": 2, "group_id": 1},
                {"id": 3, "contact_id": 2, "group_id": 2},
            ],
            result["contactGroups"],
        )

    def test_duplicate_contact_ids_fail_with_german_message(self):
        self.assert_conversion_fails(
            """
            contacts:
              - id: 1
                name: Leia Organa
              - id: 1
                name: Luke Skywalker
            """,
            "Doppelte Kontakt-IDs gefunden: 1",
        )

    def test_missing_required_fields_fail_with_german_message(self):
        self.assert_conversion_fails(
            """
            contacts:
              - id: 1
              - name: Luke Skywalker
            """,
            "Pflichtfeld 'name' fehlt",
        )

    def test_invalid_related_to_reference_fails_with_german_message(self):
        self.assert_conversion_fails(
            """
            contacts:
              - id: 1
                name: Leia Organa
                related_to:
                  - id: 99
                    relation: Verweisfehler
            """,
            "related_to verweist auf nicht existente ID 99",
        )


if __name__ == "__main__":
    unittest.main()