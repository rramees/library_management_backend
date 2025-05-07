from fastapi import APIRouter, HTTPException
from app.services.gemini_service import generate_sql_query

router = APIRouter()

@router.post("/generate-sql")
def generate_sql_endpoint(natural_language_query: str):
    """
    API endpoint to generate an SQL query from a natural language query.
    """
    try:
        # Use the gemini_service to generate the SQL query
        sql_query = generate_sql_query(natural_language_query)
        return {"natural_language_query": natural_language_query, "sql_query": sql_query}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating SQL query: {str(e)}")