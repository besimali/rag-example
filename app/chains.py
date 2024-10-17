from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain.schema.output_parser import StrOutputParser
from config import chat_model
from vector_store import retriever, get_vector_store
from config import MAX_DISTANCE_THRESHOLD, logger
from models import QuestionResponse

vector_store = get_vector_store()

def classify_question(question: str) -> str:
    classification_prompt = ChatPromptTemplate.from_template(
        """Determine if the following question is IT-related and within the scope of the system's designed topics.
        Respond with only 'IT' if it is IT-related and within scope, or 'Other' if it's not.

        Question: {question}

        Classification:"""
    )
    
    classification_chain = classification_prompt | chat_model | StrOutputParser()
    return classification_chain.invoke({"question": question})

prompt = ChatPromptTemplate.from_template("""Answer the following question based on the context provided:

Context: {context}

Question: {question}

Answer: """)

retrieval_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | chat_model
    | StrOutputParser()
)



def route_question(question: str) -> QuestionResponse:
    logger.info(f"Processing question: {question}")
    
    similar_questions = vector_store.similarity_search_with_score(question, k=1)
    
    if similar_questions and similar_questions[0][1] <= MAX_DISTANCE_THRESHOLD:
        logger.info("Question found in database")
        return QuestionResponse(
            source="database",
            matched_question=similar_questions[0][0].page_content,
            answer=similar_questions[0][0].metadata["answer"]
        )
    
    classification = classify_question(question)
    logger.info(f"Question classification: {classification}")
    
    if classification.strip().lower() == "it":
        logger.info("Generating answer using OpenAI")
        answer = retrieval_chain.invoke(question)
        return QuestionResponse(
            source="openai",
            matched_question="N/A",
            answer=answer
        )
    else:
        logger.info("Question not IT-related")
        return QuestionResponse(
            source="compliance",
            matched_question="N/A",
            answer="This is not really what I was trained for, therefore I cannot answer. Try again."
        )
    

full_chain = RunnablePassthrough() | RunnableLambda(route_question)


