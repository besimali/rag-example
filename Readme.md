# AI-Powered Question Answering System

This project is an AI-powered question answering system built with FastAPI, LangChain, and OpenAI. It uses Docker for easy deployment and management.


## Getting Started


2. Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

3. Build and run the Docker container:
   ```
   docker build -t ai-qa-system .
   docker run -p 8000:8000 --env-file .env ai-qa-system
   ```


4. The API will be available at `http://localhost:8000`

## Usage

To ask a question, send a POST request to the `/ask-question` endpoint:

```
curl -X POST "http://localhost:8000/ask-question" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer secret-token" \
-d '{"user_question": "How do I change to dark theme?"}'
```

