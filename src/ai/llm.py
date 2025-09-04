from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from datetime import datetime
from typing import Union
from dotenv import load_dotenv

load_dotenv()


class Company(BaseModel):
    """Company data output format"""

    name: str = Field(description="name of the company")
    industry: str = Field(description="industry of the company")
    country: str = Field(description="country of the company")


class Waste(BaseModel):
    """Waste data output format"""

    date: datetime = Field(description="date of the waste record in YYYY-MM-DD format")
    type: str = Field(description="type of the waste")
    weight: float = Field(description="weight of the waste in tons")
    location: str = Field(description="location of the waste")


def get_llm_chain(input_type: str):
    """
    Create an LLM chain based on input type ('company' or 'waste')

    Args:
        input_type: Either 'company' or 'waste'

    Returns:
        A langchain chain configured for the specified input type
    """
    if input_type.lower() == "company":
        structured_llm = ChatOpenAI(
            model="gpt-4o-mini", temperature=1
        ).with_structured_output(Company)

        system_prompt = """
          You're a helpful assistant that can help to generate company information records.

          Generate realistic company data in the following JSON format:
          {{
              "name": "Company Name",
              "industry": "Industry Type", 
              "country": "Country Name"
          }}

          Make sure to provide realistic and diverse company information.
        """

    elif input_type.lower() == "waste":
        structured_llm = ChatOpenAI(
            model="gpt-4o-mini", temperature=1
        ).with_structured_output(Waste)

        system_prompt = """
          You're a helpful assistant that can help to generate waste management records.

          Generate realistic waste data in the following JSON format:
          {{
              "date": "YYYY-MM-DD",
              "type": "Waste Type",
              "weight": 0.0,
              "location": "Location Name"
          }}

          Make sure to provide realistic waste management data with proper date format (YYYY-MM-DD), 
          weight in tons (as float), and realistic waste types and locations.
        """

    else:
        raise ValueError(
            f"Invalid input type: {input_type}. Must be 'company' or 'waste'"
        )

    prompt = ChatPromptTemplate(
        [
            ("system", system_prompt),
        ]
    )

    return prompt | structured_llm


async def generate_record(input_type: str) -> Union[Company, Waste]:
    """
    Generate a record based on input type

    Args:
        input_type: Either 'company' or 'waste'

    Returns:
        Generated record (Company or Waste object)
    """
    chain = get_llm_chain(input_type)
    result = chain.invoke(input={})

    # Ensure we return the proper Pydantic model instance
    if input_type.lower() == "company":
        if isinstance(result, dict):
            return Company(**result)
        return result
    elif input_type.lower() == "waste":
        if isinstance(result, dict):
            return Waste(**result)
        return result
    else:
        raise ValueError(
            f"Invalid input type: {input_type}. Must be 'company' or 'waste'"
        )


if __name__ == "__main__":
    import asyncio

    async def main():
        company_record, waste_record = await asyncio.gather(
            generate_record("company"), generate_record("waste")
        )
        print("-- Company Record --")
        print(company_record.model_dump(mode="json"))
        print("-- Waste Record --")
        print(waste_record.model_dump(mode="json"))

    asyncio.run(main())
