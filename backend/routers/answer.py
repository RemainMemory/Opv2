from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.query_answer import query_answer_for_question  # 确保路径正确

router = APIRouter()

class QuestionRequest(BaseModel):
    query_text: str

@router.post("/ask")
def ask_question(request: QuestionRequest):
    query_text = request.query_text.strip()
    if not query_text:
        raise HTTPException(status_code=400, detail="问题不能为空")

    answer = query_answer_for_question(query_text)
    if not answer:
        raise HTTPException(status_code=500, detail="生成回答失败")
    
    return {"answer": answer}
