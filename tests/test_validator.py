def test_validator_registration(validator, mock_valid_source):
    result = validator.verify(mock_valid_source)

    assert result is True
    assert len(validator.validated_sources) == 1
    assert mock_valid_source in validator.validated_sources


def test_validator_rejection(validator, mock_invalid_source):
    result = validator.verify(mock_invalid_source)

    assert result is False
    assert len(validator.validated_sources) == 0