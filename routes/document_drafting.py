from fastapi import APIRouter, Form

router = APIRouter()

def generate_moa(company_name, directors):
    return f"Memorandum of Association\nCompany Name: {company_name}\nDirectors: {', '.join(directors)}\n\n[Sample MOA content here]"

@router.post("/draft-moa/")
def draft_moa(company_name: str = Form(...), directors: str = Form(...)):
    directors_list = [d.strip() for d in directors.split(',')]
    moa = generate_moa(company_name, directors_list)
    return {"document": moa}
