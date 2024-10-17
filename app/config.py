from dotenv import load_dotenv
import logging
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

load_dotenv()

# Maximum distance threshold (lower is better)
MAX_DISTANCE_THRESHOLD = 0.4

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
chat_model = ChatOpenAI(model="gpt-4o-mini")
