from presidio_governance.anonymizer import presidio_anonymizer_service
from presidio_governance.rehydrator import presidio_rehydrator_service


def test_pan_anonymization():

    text = (
        "My PAN is ABCDE1234F"
    )

    anonymized, token_map = (
        presidio_anonymizer_service
        .anonymize_and_map(text)
    )

    assert (
        "ABCDE1234F"
        not in anonymized
    )

    assert len(token_map) > 0


def test_phone_anonymization():

    text = (
        "My mobile number is 9876543210"
    )

    anonymized, token_map = (
        presidio_anonymizer_service
        .anonymize_and_map(text)
    )

    assert (
        "9876543210"
        not in anonymized
    )

    assert len(token_map) > 0

def test_ifsc_anonymization():

    text = (
        "My IFSC code is HDFC0001234"
    )

    anonymized, token_map = (
        presidio_anonymizer_service
        .anonymize_and_map(text)
    )

    assert (
        "HDFC0001234"
        not in anonymized
    )

    assert len(token_map) > 0

def test_bank_account_anonymization():

    text = (
        "My bank account number is 1234567890123456"
    )

    anonymized, token_map = (
        presidio_anonymizer_service
        .anonymize_and_map(text)
    )

    assert (
        "1234567890123456"
        not in anonymized
    )

    assert len(token_map) > 0

def test_aadhaar_anonymization():

    text = (
        "My Aadhaar number is 1234-5678-9012"
    )

    anonymized, token_map = (
        presidio_anonymizer_service
        .anonymize_and_map(text)
    )

    assert (
        "1234-5678-9012"
        not in anonymized
    )

    assert len(token_map) > 0

def test_bank_account_with_spaces_anonymization():

    text = (
        "My bank account number is 9876 5431 23456"
    )

    anonymized, token_map = (
        presidio_anonymizer_service
        .anonymize_and_map(text)
    )

    assert (
        "9876 5431 23456"
        not in anonymized
    )

    assert len(token_map) > 0

def test_aadhaar_not_detected_as_bank_account():

    text = (
        "Aadhaar : 1234 5678 4321"
    )

    _, token_map = (
        presidio_anonymizer_service
        .anonymize_and_map(text)
    )

    assert any(
        "AADHAAR_NUMBER" in key
        for key in token_map
    )

    assert not any(
        "BANK_ACCOUNT" in key
        for key in token_map
    )

def test_rehydration():

    text = (
        "My PAN is ABCDE1234F"
    )

    anonymized, token_map = (
        presidio_anonymizer_service
        .anonymize_and_map(text)
    )

    restored = (
        presidio_rehydrator_service
        .rehydrate_text(
            anonymized,
            token_map
        )
    )

    assert restored == text