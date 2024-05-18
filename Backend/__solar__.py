import warnings
import os
import requests
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_upstage import ChatUpstage
from langchain_community.retrievers import BM25Retriever
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter
from youtube_transcript_api import YouTubeTranscriptApi
import json
import copy 

warnings.filterwarnings("ignore")

# .env 파일 불러오기
load_dotenv()

# api키 불러오기
UPSTAGE_API_KEY = os.getenv("UPSTAGE_API_KEY")
if not UPSTAGE_API_KEY:
    raise ValueError("UPSTAGE_API_KEY is not set in the environment variables")

# 유튜브 영상에서 자막 데이터 가져오기
def getCaptions(vid: str):
    captions = YouTubeTranscriptApi.get_transcript(vid, languages=['en'])
    context = "" #시간 및 재생 시간을 제외한 텍스트 데이터
    for caption in captions:
        temp = caption["text"].replace("\n", " ")
        context += temp
    return {"context" : context, "captions": captions}

# 동영상 요약 및 문제 생성
def generate(vid: str):
    # 결과 반환 객체
    result = {}
    # api 요청 엔드포인트
    url = "https://api.upstage.ai/v1/document-ai/layout-analysis"
    # api 요청 헤드
    headers = {"Authorization": f"Bearer {UPSTAGE_API_KEY}"}

    # 유튜브 영상에서 자막 데이터 가져오기
    captions = getCaptions(vid)
    # 자막 데이터만 가져오기
    context = captions["context"]
    if not context:
        raise ValueError("No context found in the result")

    # Upstage Chat LLM 모델 불러오기
    llm = ChatUpstage()
    # 프롬프트 템플릿 설정(요약)
    prompt_template = PromptTemplate.from_template(
        """
        Give the Summary
        If the answer is not present in the context, please write "The information is not present in the context."
        ---
        Context: {Context}
        """
    )
    chain = prompt_template | llm | StrOutputParser()
    summary = chain.invoke({"Context": context})
    result["summary"] = summary
    
    # 프롬프트 템플릿 설정(키워드)
    prompt_template = PromptTemplate.from_template(
        """
        Give the keywords from context
        If the answer is not present in the context, please write "The information is not present in the context."
        ---
        Context: {Context}
        """
    )
    chain = prompt_template | llm | StrOutputParser()
    keyword = chain.invoke({"Context": context})
    # 키워드 파싱
    keyword_arr = keyword.split(":")[1]
    keyword_temp = []
    if "," in keyword_arr:
        keyword_arr = keyword_arr.split(", ")
    elif "\n\n*" in keyword_arr:
        keyword_arr = keyword_arr.split("\n\n* ")
    else:
        keyword_arr = keyword_arr.split("\n* ")
    for key in keyword_arr:
        keyword_temp.append(key.strip())
    result["keyword"] = keyword_temp

    # 프롬프트 템플릿 설정(퀴즈)
    prompt_template = PromptTemplate.from_template(
        """
        Give the 10 questions for 4 multiple choices from context.
        And Give the correct answer bottom of each questions

        If the answer is not present in the context, please write "The information is not present in the context."
        ---
        Context: {Context}
        """
    )
    result["quiz"] = []
    # 퀴즈 파싱
    chain = prompt_template | llm | StrOutputParser()
    quizForm = {"question": "", "options": [], "answer": 1}
    quiz = chain.invoke({"Context": context})
    quiz = quiz.split("\n")
    temp = copy.deepcopy(quizForm)
    for idx in range(len(quiz)):
        if idx % 8 == 0:
            result["quiz"].append(temp)
            temp = copy.deepcopy(quizForm)
            temp["question"] = quiz[idx]
        elif idx % 8 == 6:
            temp["answer"] = quiz[idx]
        else:
            if quiz[idx] != "":
                temp["options"].append(quiz[idx])
    result["quiz"] = result["quiz"][1:]
    return result


if __name__ == '__main__':
    result = getData("VJ78D7Yyep0")
    print(result["quiz"])