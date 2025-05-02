from langchain_core.runnables import RunnableWithMessageHistory
from langchain_google_genai import GoogleGenerativeAI

from app.core.config import settings
from app.database.CustomMongo import CustomMongoDBChatMessageHistory
from app.prompt.counselorAI import counselor_prompt
from app.prompt.evaulatorAI import evaluation_prompt

# LLM 설정
llm = GoogleGenerativeAI(
    model="gemini-1.5-pro",
    google_api_key=settings.GOOGLE_API_KEY
)
evaluation_chain = evaluation_prompt | llm

# 기본 평가 체인
evaluation_with_history = RunnableWithMessageHistory(
    evaluation_chain,
    lambda sessionId: CustomMongoDBChatMessageHistory(
        session_id=sessionId,
        connection_string=settings.MONGODB_URL,
        database_name=settings.MONGODB_DB_NAME,
        collection_name=settings.MONGODB_COLLECTION,
    ),
    input_messages_key="input",
    history_messages_key="History",
)

# 기본 상담 체인 설정
counselor_chain = counselor_prompt | llm

# MongoDB 연결된 체인 설정
chain_with_history = RunnableWithMessageHistory(
    counselor_chain,
    lambda sessionId: CustomMongoDBChatMessageHistory(
        session_id=sessionId,
        connection_string=settings.MONGODB_URL,
        database_name=settings.MONGODB_DB_NAME,
        collection_name=settings.MONGODB_COLLECTION,
    ),
    input_messages_key="input",
    history_messages_key="History",
)