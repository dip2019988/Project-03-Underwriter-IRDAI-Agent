from presidio_governance.anonymizer import (
    presidio_anonymizer_service
)


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