import json
import regex
import requests
from enum import Enum
from fastapi import APIRouter, HTTPException
from typing import Union
from pydantic import BaseModel
from . import MessageResponse


class MethodName(str, Enum):
    meaning = "meaning"
    example = "example"
    synonyms = "synonyms"
    antonyms = "antonyms"


class explainRespone(BaseModel):
    meaning: str
    example: list
    synonyms: list
    antonyms: list


class AnswerResponse(BaseModel):
    answer: Union[str, list]


router = APIRouter(prefix="/gpt",
                   tags=["gpt"],
                   responses={404: {"model": MessageResponse}})


def prompt_explain_word(word: str, method_name: str):
    """
    Prompt the user to explain the meaning of the word.
    :param word: The word to be explained.
    :param method_name: The method name (all, meaning, example, synonyms, antonyms).
    """
    if method_name == "all":
        return f"""Explain the meaning of the word '{word}'.
                Give me 3 example sentences.
                Give me some synonyms and antonyms.
                Answer in json form.
                {{"meaning": content, "example": [content], "synonyms": [content], "antonyms": [content]}}
                """
    elif method_name == "meaning":
        return f"""Explain the meaning of the word '{word}'.
                 Answer in json form.
                 {{"answer": content}}"""

    if method_name == "example":
        prompt = f"Give me 3 example sentences of the word '{word}'."
    elif method_name == "synonyms":
        prompt = f"Give me some synonyms of the word '{word}'."
    elif method_name == "antonyms":
        prompt = f"Give me some antonyms of the word '{word}'."

    prompt += """
    Answer in json form.
    {{"answer": [content]}}
    """

    return prompt


def find_json(text: str) -> Union[dict, None]:
    """
    Find json data in the text.
    """
    pattern = r'\{(?:[^{}]|(?R))*\}'
    matches = regex.findall(pattern, text)

    for match in matches:
        try:
            json_data = json.loads(match)
            return json_data
        except json.JSONDecodeError:
            continue


def request_to_gpt(prompt: str) -> dict:
    """
    Request to GPT-3.
    """
    r = requests.get(f"http://127.0.0.1:3000/ask?prompt={prompt}")
    if r.status_code == 200:
        found_data = find_json(r.json()["content"])
    else:
        raise HTTPException(status_code=500, detail="Internal server error")

    if found_data is None:
        raise HTTPException(status_code=404, detail="Not found")
    return found_data


@router.get("/explain/all/{word}", description="Explain the meaning of the word.")
async def explain_all(word: str) -> explainRespone:
    prompt = prompt_explain_word(word, "all")
    return request_to_gpt(prompt)


@router.get("/explain/{word}", description="With query, explain partially.")
async def explain_partially(method: MethodName, word: str) -> AnswerResponse:
    prompt = prompt_explain_word(word, method.value)
    return request_to_gpt(prompt)


@router.get("/news/{topic}", description="Create a simulated news.")
async def create_news(topic: str) -> AnswerResponse:
    prompt = f"Give me a simulated news of the topic '{topic}'."
    prompt += """
    Answer in json form.
    {{"answer": [content]}}
    """
    return request_to_gpt(prompt)


@router.get("/", description="Answer the question.")
async def answer_question(question: str):
    r = requests.get(f"http://127.0.0.1:3000/ask?prompt={question}")
    if r.status_code == 200:
        return r.json()
    else:
        raise HTTPException(status_code=500, detail="Internal server error")
