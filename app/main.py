from fastapi import FastAPI, Depends
# from langchain.chat_models import AzureChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# 절대 경로로 바꿔 가져오기
from app.config import settings
from app.models import ChatMessage, ChatResponse
import json
from pydantic import BaseModel


app = FastAPI(title=settings.APP_NAME)

# Azure OpenAI
# llm = AzureChatOpenAI(
#     openai_api_key=settings.AZURE_OPENAI_API_KEY,
#     azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
#     deployment_name=settings.AZURE_DEPLOYMENT_NAME
# )

# Google Generative AI
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    max_output_tokens=200,
    google_api_key=settings.GOOGLE_API_KEY
)

memory = ConversationBufferMemory(return_messages=True)

def load_prompts():
    with open(settings.PROMPT_FILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@app.get("/test")
async def test():
    print("테스트 엔드포인트가 호출되었습니다.")
    return {"message": "test"}


@app.post("/chat")
async def chat(message: ChatMessage):
    print(f"message: {message.content}")
    chat_chain = LLMChain(
        llm=llm,
        prompt=ChatPromptTemplate.from_messages([
            ("system", "당신은 전문 심리상담 챗봇입니다."
                       "사용자의 감정, 인지, 행동을 인지행동치료(CBT) 기법에 따라분석하고"
                       "적절한 질문을 통해 스스로를 돌아보게 유도합니다."
                       "직접적인 판단 없이 공감하며, 문제 해결보다 감정 인식에 집중하세요."),
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
                    ("system", "당신은 전문 심리상담 챗봇입니다." #예시 프롬프트
                               "지금까지의 대화를 보고 질문에 대해 점수를 매겨주세요."),
                    ("human", f"질문: {question}\n대화내용: {memory.chat_memory}") #여기에 들어갈 것은 지금까지의 대화 내용이 입력된다.
                                                                                #전체 내용이 들어갈지, 요약본이 들어갈지는 추후 결정
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