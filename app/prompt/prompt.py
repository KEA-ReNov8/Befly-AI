from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_google_genai import GoogleGenerativeAI

from app.core.config import settings
from app.database.CustomMongo import CustomMongoDBChatMessageHistory

# LLM 설정
llm = GoogleGenerativeAI(
    model="gemini-1.5-pro",
    google_api_key=settings.GOOGLE_API_KEY
)

# 프롬프트 템플릿 설정
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 전문 심리상담 챗봇입니다. "
              "사용자의 감정, 인지, 행동을 인지행동치료(CBT) 기법에 따라 분석하고 "
              "적절한 질문을 통해 스스로를 돌아보게 유도합니다. "
              "직접적인 판단 없이 공감하며, 문제 해결보다 감정 인식에 집중하세요."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# 체인 설정
chain = prompt | llm

# MongoDB 연결된 체인 설정
chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: CustomMongoDBChatMessageHistory(
        session_id=session_id,
        connection_string=settings.MONGODB_URL,
        database_name=settings.MONGODB_DB_NAME,
        collection_name=settings.MONGODB_COLLECTION,
    ),
    input_messages_key="input",
    history_messages_key="history",
)