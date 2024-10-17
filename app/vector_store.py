from langchain_community.vectorstores import FAISS
from config import embeddings, MAX_DISTANCE_THRESHOLD
from db import faq_database

texts = [item["question"] for item in faq_database]
metadatas = [{"answer": item["answer"]} for item in faq_database]
vector_store = FAISS.from_texts(texts, embeddings, metadatas=metadatas)

retriever = vector_store.as_retriever(search_type="similarity_score_threshold",
                search_kwargs={'score_threshold': MAX_DISTANCE_THRESHOLD, 'k': 1})