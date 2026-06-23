import unittest

import services


class ServicesTests(unittest.TestCase):
    def test_get_contact_returns_known_contact(self):
        contact = services.get_contact(3)

        self.assertIsNotNone(contact)
        self.assertEqual("Obi-Wan Kenobi", contact.name)

    def test_list_contacts_in_group_returns_group_members(self):
        contacts = services.list_contacts_in_group("Jedi")
        names = {contact.name for contact in contacts}

        self.assertIn("Obi-Wan Kenobi", names)
        self.assertIn("Yoda", names)

    def test_list_contacts_filters_case_insensitively(self):
        name_matches = services.list_contacts(name_contains="solo")
        organization_matches = services.list_contacts(organization="rebel alliance")
        species_matches = services.list_contacts(species="droid")

        self.assertIn("Han Solo", {contact.name for contact in name_matches})
        self.assertIn("Leia Organa", {contact.name for contact in organization_matches})
        self.assertIn("R2-D2", {contact.name for contact in species_matches})

    def test_list_contacts_supports_q_filter(self):
        matches = services.list_contacts(q="tatooine")

        self.assertIn("Owen Lars", {contact.name for contact in matches})

    def test_list_contacts_supports_id_filter(self):
        matches = services.list_contacts(contact_id=6)

        self.assertEqual(["Han Solo"], [contact.name for contact in matches])


if __name__ == "__main__":
    unittest.main()