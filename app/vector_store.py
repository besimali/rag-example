from langchain_postgres import PGVector
from config import embeddings, MAX_DISTANCE_THRESHOLD, logger
from db import faq_database
import os
from typing import List, Dict
from langchain.schema.retriever import BaseRetriever

CONNECTION_STRING = os.environ.get("DATABASE_URL", "postgresql://user:password@db:5432/vectordb")

def get_vector_store(collection_name: str = "faq_vectors") -> PGVector:
    return PGVector(
        connection=CONNECTION_STRING,
        embeddings=embeddings,
        collection_name=collection_name
    )

def create_embeddings(texts: List[str], metadatas: List[Dict] = None, collection_name: str = "faq_vectors") -> None:
    vector_store = get_vector_store(collection_name)
    vector_store.add_texts(texts=texts, metadatas=metadatas)
    logger.info(f"Created embeddings for {len(texts)} texts in collection '{collection_name}'")

def update_embeddings(texts: List[str], metadatas: List[Dict] = None, collection_name: str = "faq_vectors") -> None:
    vector_store = get_vector_store(collection_name)
    existing_docs = vector_store.similarity_search_with_score(" ".join(texts), k=len(texts))
    
    to_update = []
    to_add = []
    
    for i, text in enumerate(texts):
        matching_doc = next((doc for doc, score in existing_docs if doc.page_content == text), None)
        if matching_doc:
            to_update.append((matching_doc.id, text, metadatas[i] if metadatas else None))
        else:
            to_add.append((text, metadatas[i] if metadatas else None))
    
    if to_update:
        vector_store.update(to_update)
        logger.info(f"Updated {len(to_update)} existing embeddings in collection '{collection_name}'")
    
    if to_add:
        vector_store.add_texts([t[0] for t in to_add], [t[1] for t in to_add])
        logger.info(f"Added {len(to_add)} new embeddings to collection '{collection_name}'")

def add_collection(collection_name: str) -> None:
    get_vector_store(collection_name)
    logger.info(f"Created new collection '{collection_name}'")

def get_retriever(collection_name: str = "faq_vectors") -> BaseRetriever:
    vector_store = get_vector_store(collection_name)
    return vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={'score_threshold': MAX_DISTANCE_THRESHOLD, 'k': 1}
    )

def init_db() -> None:
    logger.info("Initializing vector store")
    texts = [item["question"] for item in faq_database]
    metadatas = [{"answer": item["answer"]} for item in faq_database]
    create_embeddings(texts, metadatas)
    logger.info("Vector store initialized successfully.")

retriever = get_retriever()
