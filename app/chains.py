from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain.schema.output_parser import StrOutputParser
from config import chat_model
from vector_store import retriever
from config import MAX_DISTANCE_THRESHOLD, logger
from vector_store import vector_store
from question_classifier import classify_question

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



def route_question(question: str):
    logger.info(f"Processing question: {question}")
    
    similar_questions = vector_store.similarity_search_with_score(question, k=1)
    
    if similar_questions and similar_questions[0][1] <= MAX_DISTANCE_THRESHOLD:
        logger.info("Question found in database")
        return similar_questions[0][0].metadata["answer"]
    
    classification = classify_question(question)
    logger.info(f"Question classification: {classification}")
    
    if classification.strip().lower() == "it":
        logger.info("Generating answer using OpenAI")
        return retrieval_chain.invoke(question)
    else:
        logger.info("Question not IT-related")
        return "This is not really what I was trained for, therefore I cannot answer. Try again."
    

full_chain = RunnablePassthrough() | RunnableLambda(route_question)