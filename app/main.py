from fastapi import FastAPI, Depends
from langchain.chat_models import AzureChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate

from .config import settings
from .models import ChatMessage, ChatResponse
import json
from pydantic import BaseModel

app = FastAPI(title=settings.APP_NAME)

# LangChain 설정
llm = AzureChatOpenAI(
    openai_api_key=settings.AZURE_OPENAI_API_KEY,
    azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
    deployment_name=settings.AZURE_DEPLOYMENT_NAME
)

memory = ConversationBufferMemory(return_messages=True)

def load_prompts():
    with open(settings.PROMPT_FILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

@app.post("/chat")
async def chat(message: ChatMessage):
    chat_chain = LLMChain(
        llm=llm,
        prompt=ChatPromptTemplate.from_messages([
            ("system", "당신은 전문 심리 상담가입니다."),
            ("human", "{input}")
        ]),
        memory=memory
    )
    response = await chat_chain.arun(message.content)
    return ChatResponse(message=response)

class EvaluationResult(BaseModel):
    keyword: str
    score: float
    details: dict

@app.post("/evaluate")
async def evaluate():
    prompts = load_prompts()
    results = []
    
    for keyword, data in prompts.items():
        total_score = 0
        question_scores = {}
        
        for question in data["questions"]:
            evaluate_chain = LLMChain(
                llm=llm,
                prompt=ChatPromptTemplate.from_messages([
                    ("system", "사용자의 대화 내용을 바탕으로 0-3점으로 평가해주세요."),
                    ("human", f"질문: {question}\n대화내용: {memory.chat_memory}")
                ])
            )
            score = int(await evaluate_chain.arun({}))
            question_scores[question] = score
            total_score += score
            
        avg_score = total_score / len(data["questions"])
        results.append(
            EvaluationResult(
                keyword=keyword,
                score=avg_score,
                details=question_scores
            )
        )
    
    return sorted(results, key=lambda x: x.score, reverse=True)[:3]