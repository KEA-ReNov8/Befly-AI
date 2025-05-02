from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

evaluation_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """당신은 심리상담 전문가이며, 다음은 사용자의 대화 기록을 바탕으로 한 심리 평가 과제입니다.

아래에는 평가 기준이 JSON 형식으로 주어집니다. 각 항목은 다음 정보를 포함합니다:
- keyword: 평가 항목 이름
- questions: 사용자가 실제로 받았던 질문들
- evaluation_hints: 사용자의 응답에서 관찰해야 할 평가 포인트

--- 평가 기준 JSON ---
1. 각 항목에 대해 **0 ~ 3점 중 하나의 점수**를 부여하세요.
2. 각 점수에 대해 **간단한 이유(코멘트)**를 작성하세요.
3. 결과는 **JSON 형식**으로 출력하세요.

다음 지시사항에 따라 평가를 수행하세요:



--- 출력 예시 형식 ---
{{
  "emotional_stability": {{
    "score": 2,
    "comment": "감정 표현이 일정하지만 고립감을 언급함"
  }},
  "stress_management": {{
    "score": 3,
    "comment": "스트레스와 무기력함을 지속적으로 표현함"
  }}
}}

"""
    ),
    MessagesPlaceholder(variable_name="History"),
    ("human", "위 사용자 대화를 평가해 주세요.")
])