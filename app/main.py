from fastapi import FastAPI, HTTPException, Depends
from models import QuestionRequest, QuestionResponse
from config import logger
from chains import full_chain
from auth import get_token

app = FastAPI()

@app.post("/ask-question", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest, token: str = Depends(get_token)):
    user_question = request.user_question
    logger.info(f"Received question: {user_question}")

    try:
        result = full_chain.invoke(user_question)
        logger.info(f"Result type: {type(result)}")
        logger.info(f"Result content: {result}")
        
        if isinstance(result, str):
            if result.startswith("This is not really what I was trained for"):
                return QuestionResponse(
                    source="compliance",
                    matched_question="N/A",
                    answer=result
                )
            else:
                return QuestionResponse(
                    source="database",
                    matched_question=user_question,
                    answer=result
                )
        elif isinstance(result, dict):
            return QuestionResponse(
                source="openai",
                matched_question="N/A",
                answer=str(result)
            )
        else:
            return QuestionResponse(
                source="openai",
                matched_question="N/A",
                answer=str(result)
            )
    except Exception as e:
        logger.exception(f"Error processing question: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
