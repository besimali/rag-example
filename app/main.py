from fastapi import FastAPI, HTTPException, Depends
from models import QuestionRequest, QuestionResponse
from config import logger
from chains import full_chain
from auth import get_token
from vector_store import init_db
from contextlib import asynccontextmanager
from typing import Dict, Any

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/ask-question", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest, token: str = Depends(get_token)):
    user_question = request.user_question
    logger.info(f"Received question: {user_question}")

    try:
        result = await full_chain.ainvoke(user_question)
        logger.info(f"Result content: {result}")
        
        return result
    except Exception as e:
        logger.exception(f"Error processing question: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
