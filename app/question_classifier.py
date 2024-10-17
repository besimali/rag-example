from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from config import chat_model

def classify_question(question):
    classification_prompt = ChatPromptTemplate.from_template(
        """Determine if the following question is IT-related and within the scope of the system's designed topics.
        Respond with only 'IT' if it is IT-related and within scope, or 'Other' if it's not.

        Question: {question}

        Classification:"""
    )
    
    classification_chain = classification_prompt | chat_model | StrOutputParser()
    return classification_chain.invoke({"question": question})