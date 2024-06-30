import pytest
import requests

import pteredactyl as pt

# Sample text for testing
sample_text = """
NHS Confidential Clinical Information Summary Patient: JellyKins, Mr Simon Jumbo
Date of Birth: 12/12/1956 UBRN: 0004 0123 4567 Age: 25 years NHS: 420 568 7899
Gender: Male UBRN Information Appointment Date/Time: - Referral Created Date:
05-Feb-2021 12:44 Priority: Urgent Clinical Information First 15-Mar-2021 12:44
Submitted: Referred By: MUNGO, Tricksy (Dr) Clinical Information Last - Referring
Organisation: BLOCKSWOOD SURGERY Updated: Address: MIDDLE WAY Named Clinician: -
BLOCKS HEATH DORSET Allocated Clinician: - DORSET Clinical Context: GI and Liver
(Medicine and SO80 10DX Surgery)/Upper GI incl Telephone: 01489 123123 Dyspepsia
Location: - Clinical Term: - Patient Information Patient Address: 100 Blankswood
Drive Registered Practice: BLOCKSWOOD SURGERY Toffs Heath Address: MIDDLE WAY,
TOFFS HEATH Hants, DORSET Telephone (Primary Home): 01489123123 Telephone (Mobile):
07775015050 More contact details available when reviewing online Attachments File
Name File 500
"""

expected_output = """
<LOCATION> Confidential Clinical Information Summary Patient: <PERSON> Date of Birth:
<DATE_TIME> UBRN: <ID> Age: 25 years <LOCATION>: <ID> Gender: Male UBRN Information
Appointment Date/Time: - Referral Created Date: <DATE_TIME> 12:44 Priority: Urgent
Clinical Information First <DATE_TIME> 12:44 Submitted: Referred By: <PERSON>) Clinical
Information Last - Referring Organisation: <LOCATION> Updated: Address: <LOCATION> Named
Clinician: - <PERSON> Allocated Clinician: <PERSON> Clinical Context: GI and Liver
(Medicine and SO80 10DX Surgery)/Upper GI incl Telephone: <NUMBER> Dyspepsia Location: -
Clinical Term: - Patient Information Patient Address: 100 <LOCATION> Drive Registered
Practice: <LOCATION> SURGERY <LOCATION> Address: <LOCATION> <PERSON> Telephone (Primary
Home): <NUMBER> Telephone (Mobile): <NUMBER> More contact details available when reviewing
online Attachments File Name File 500
"""


@pytest.fixture
def sample_data():
    return sample_text, expected_output


def test_redact(sample_data):
    test_text, expected_output = sample_data
    actual_output = pt.anonymise(test_text)
    actual_output = actual_output.replace("<", "[").replace(">", "]")
    assert actual_output == expected_output


def test_server_running():
    try:
        response = requests.get("http://localhost:7860")
        response.raise_for_status()
    except requests.exceptions.HTTPError as errH:
        pytest.fail(f"HTTP Error: {errH}")
    except requests.exceptions.ConnectionError as errC:
        pytest.fail(f"Error Connecting: {errC}")
    except requests.exceptions.Timeout as errT:
        pytest.fail(f"Timeout Error: {errT}")
    except requests.exceptions.RequestException as err:
        pytest.fail(f"Request Exception: {err}")
