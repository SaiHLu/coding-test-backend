import pytest

from llm import generate_record, Waste, Company


@pytest.mark.asyncio
async def test_generate_record_for_waste() -> None:
    waste_record = await generate_record("waste")
    assert isinstance(waste_record, Waste)


@pytest.mark.asyncio
async def test_generate_record_for_company() -> None:
    company_record = await generate_record("company")
    assert isinstance(company_record, Company)


@pytest.mark.asyncio
async def test_generate_record_invalid_type() -> None:
    with pytest.raises(ValueError) as e:
        await generate_record("random")
    assert "Invalid input type:" in str(e.value)
