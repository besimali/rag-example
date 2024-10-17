
## Getting Started


2. Create a `.env` file in the project root and add the following environment variables:
   ```
   OPENAI_API_KEY=your_api_key_here
   API_SECRET_TOKEN=secret-token
   DATABASE_URL=postgresql://user:password@db:5432/vectordb
   ```

3. Build and run the Docker containers using Docker Compose:
   ```
   docker-compose up --build
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

