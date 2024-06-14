import pytest
from pydantic import ValidationError
from src.routes.complex.domain.models.complex_operation_request import ComplexOperationRequest
def test_complex_operation_request_valid():
    # Test valid instantiation
    request = ComplexOperationRequest(
        real1=1.0,
        imaginary1=2.0,
        real2=3.0,
        imaginary2=4.0
    )
    assert request.real1 == 1.0
    assert request.imaginary1 == 2.0
    assert request.real2 == 3.0
    assert request.imaginary2 == 4.0

def test_complex_operation_request_invalid_type():
    # Test instantiation with invalid data types (e.g., passing a string instead of a float)
    with pytest.raises(ValidationError):
        ComplexOperationRequest(
            real1="not a float",
            imaginary1=2.0,
            real2=3.0,
            imaginary2=4.0
        )

def test_complex_operation_request_missing_field():
    # Test instantiation with missing fields
    with pytest.raises(ValidationError):
        ComplexOperationRequest(
            real1=1.0,
            imaginary1=2.0,
            # Missing real2 and imaginary2
        )