import pytest 
from pydantic import ValidationError
from src.routes.complex.domain.models.complex_operation_response import ComplexOperationResponse

def test_complex_operation_response_valid():
    # Test valid instantiation
    response = ComplexOperationResponse(
        z1="1.0 + 1.0 i",
        z2="1.0 + 1.0 i",
        polarZ1 =  "1.4142135623731 e^{\\frac{i \\pi}{4}}",
        polarZ2 = "1.4142135623731 e^{\\frac{i \\pi}{4}}",
        algebraicResult =  "2.0 + 2.0 i",
        polarResult = "2.82842712474619 e^{\\frac{i \\pi}{4}}"
    )
    assert response.z1 == "1.0 + 1.0 i"
    assert response.z2 == "1.0 + 1.0 i"
    assert response.polarZ1 == "1.4142135623731 e^{\\frac{i \\pi}{4}}"
    assert response.polarZ2 == "1.4142135623731 e^{\\frac{i \\pi}{4}}"
    assert response.algebraicResult == "2.0 + 2.0 i"
    assert response.polarResult == "2.82842712474619 e^{\\frac{i \\pi}{4}}"


def test_complex_operation_response_invalid() :
    # Test instantiation with invalid data types (e.g., passing a string instead of a float)
    with pytest.raises(ValidationError):
        ComplexOperationResponse(
            z1=1.0,
            z2=1.0,
            polarZ1 = 1.4142135623731,
            polarZ2 = 1.4142135623731,
            algebraicResult = 2.0,
            polarResult = 2.82842712474619
        )

def test_complex_operation_response_missing_field():
    # Test instantiation with missing fields
    with pytest.raises(ValidationError):
        ComplexOperationResponse(
            z1="1.0 + 1.0 i",
            z2="1.0 + 1.0 i",
            polarZ1 =  "1.4142135623731 e^{\\frac{i \\pi}{4}}",
            polarZ2 = "1.4142135623731 e^{\\frac{i \\pi}{4}}",
            algebraicResult =  "2.0 + 2.0 i",
            # Missing polarResult
        )
