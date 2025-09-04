from langchain.prompts import ChatPromptTemplate
from langchain.schema import Document
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

from .ingestions import retriever

llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")


def format_docs(docs: list[Document]) -> str:
    template = """
      Provide a concise executive summary of the following text, highlighting only the most important insights in under 100 words:

      {context}
    """
    docs_string = "\n\n".join(doc.page_content for doc in docs)
    response = llm.invoke(template.format(context=docs_string))
    return str(response.content)


async def ai_answer(question: str):
    template = """
      Use the following pieces of context to answer the question at the end.
      If you don't know the answer, just say you don't know, don't try to make up an answer. Use three sentences maximum and keep the answer as concise as possible. Always say "Thanks for asking!" at the end of the answer.

      {context}

      Question: {question}

      Helpful Answer:
    """

    prompt = ChatPromptTemplate.from_template(template)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
    )

    return chain.invoke(question)


if __name__ == "__main__":
    documents = [
        Document(
            page_content="""The relatively high potassium content of milk has led to the suggestion that greater milk intake may reduce blood pressure. The Dietary Approaches to Stop Hypertension (DASH) diet, which includes low-fat dairy foods, reduces blood pressure, but the specific contribution of milk is unclear because the diet is low in sodium and high in fruits and vegetables. Randomized trials of low-fat milk have shown inconsistent results with respect to reduction of blood pressure.15,70,71 It is important to note that the effect of milk in such trials often depends on the comparison beverages or foods. If milk replaces sugar-sweetened beverages or other refined carbohydrates, outcomes will probably be beneficial,72,73 but results may differ if milk replaces nuts, legumes, or whole fruits"""
        ),
        Document(
            page_content="""
            In international comparisons, consumption of
            dairy products is strongly correlated with rates
            of breast cancer, prostate cancer, and other cancers.9,90 The effects of milk consumption on
            plasma IGF-I,20,91 which predicts increased risks
            of prostate and breast cancers,92 provides a plausible mechanism. In prospective cohort studies,
            milk consumption is most consistently associated with a greater risk of prostate cancer,23,93
            especially aggressive or fatal forms, but not with
            a greater risk of breast cancer.23 Total dairy intake has been associated with a greater risk of
            endometrial cancer, particularly among postmenopausal women who are not receiving hormone therapy, a finding possibly related to the
            sex-hormone content of dairy products.94 Consumption of dairy products or lactose has been
            hypothesized to increase the risk of ovarian
            cancer, but no relation was seen in a pooled
            analysis.95 In contrast, in meta-analyses and
            pooled analyses of primary data,96,97 milk consumption was inversely associated with the risk
            of colorectal cancer, potentially owing to its
            high calcium content.23 A major limitation of the
            existing literature is that almost all prospective
            studies have been initiated among persons in
            midlife or later, whereas many cancer risk factors operate in childhood or early adult life.98 In
            one study of diets in adolescents, milk intake
            was shown to be unrelated to a future risk of
            breast cancer.99"""
        ),
    ]
    print(format_docs(documents))
