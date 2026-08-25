from fastapi import APIRouter, Form

router = APIRouter()

def generate_incorporation_doc(entity_type, company_name, directors):
    return f"Incorporation Document\nEntity Type: {entity_type}\nCompany Name: {company_name}\nDirectors: {', '.join(directors)}\n\n[Sample incorporation content here]"

@router.post("/register-company/")
def register_company(entity_type: str = Form(...), company_name: str = Form(...), directors: str = Form(...)):
    directors_list = [d.strip() for d in directors.split(',')]
    doc = generate_incorporation_doc(entity_type, company_name, directors_list)
    # For now, just return the generated document
    return {"status": "submitted", "document": doc}
