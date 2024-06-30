import unittest

import requests

import pteredactyl as pt


class TestRedact(unittest.TestCase):
    def setUp(self):
        # setUp is a method that is ran before each test.
        # You can use it to set up any state that is shared between tests.
        pass

    def test_redact(self):
        # Define your test case
        test_text = (
            "NHS Confidential Clinical Information Summary "
            "Patient: JellyKins, Mr Simon Jumbo Date of Birth: 12/12/1956 "
            "UBRN: 0004 0123 4567 Age: 25 years NHS: 420 568 7899 Gender: Male "
            "UBRN Information Appointment Date/Time: - Referral Created Date: "
            "05-Feb-2021 12:44 Priority: Urgent Clinical Information First "
            "15-Mar-2021 12:44 Submitted: Referred By: MUNGO, Tricksy (Dr) "
            "Clinical Information Last - Referring Organisation: BLOCKSWOOD SURGERY "
            "Updated: Address: MIDDLE WAY Named Clinician: - BLOCKS HEATH DORSET "
            "Allocated Clinician: - DORSET Clinical Context: GI and Liver "
            "(Medicine and SO80 10DX Surgery)/Upper GI incl Telephone: "
            "01489 123123 Dyspepsia Location: - Clinical Term: - "
            "Patient Information Patient Address: 100 Blankswood Drive "
            "Registered Practice: BLOCKSWOOD SURGERY Toffs Heath Address: "
            "MIDDLE WAY, TOFFS HEATH Hants, DORSET Telephone (Primary Home): "
            "01489123123 Telephone (Mobile): 07775015050 More contact details "
            "available when reviewing online Attachments File Name File 500"
        )

        expected_output = (
            "<LOCATION> Confidential Clinical Information Summary "
            "Patient: <PERSON> Date of Birth: <DATE_TIME> UBRN: <ID> Age: 25 years "
            "<LOCATION>: <ID> Gender: Male UBRN Information Appointment Date/Time: - "
            "Referral Created Date: <DATE_TIME> 12:44 Priority: Urgent "
            "Clinical Information First <DATE_TIME> 12:44 Submitted: "
            "Referred By: <PERSON>) Clinical Information Last - Referring Organisation: "
            "<LOCATION> Updated: Address: <LOCATION> Named Clinician: - <PERSON> "
            "Allocated Clinician: <PERSON> Clinical Context: GI and Liver "
            "(Medicine and SO80 10DX Surgery)/Upper GI incl Telephone: <NUMBER> "
            "Dyspepsia Location: - Clinical Term: - Patient Information "
            "Patient Address: 100 <LOCATION> Drive Registered Practice: <LOCATION> SURGERY "
            "<LOCATION> Address: <LOCATION> <PERSON> Telephone (Primary Home): <NUMBER> "
            "Telephone (Mobile): <NUMBER> More contact details available when "
            "reviewing online Attachments File Name File 500"
        )

        # Apply your function to the test case
        actual_output = pt.anonymise(test_text)

        # Check that the actual output matches the expected output
        self.assertEqual(actual_output, expected_output)

    def test_server_running(self):
        try:
            response = requests.get(
                "http://localhost:7860"
            )  # replace with your server's address
            response.raise_for_status()
        except requests.exceptions.HTTPError as errH:
            print("Http Error:", errH)
        except requests.exceptions.ConnectionError as errC:
            print("Error Connecting:", errC)
        except requests.exceptions.Timeout as errT:
            print("Timeout Error:", errT)
        except requests.exceptions.RequestException as err:
            print("Something went wrong with the server", err)

    def tearDown(self):
        # tearDown is a method that is ran after each test.
        # You can use it to clean up any state that may have been modified during tests.
        pass


# This statement allows the tests to be run if the file is ran directly, but not if it is imported as a module.
if __name__ == "__main__":
    unittest.main()
