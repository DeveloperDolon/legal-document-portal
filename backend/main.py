from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uvicorn

app = FastAPI(title="Legal Document Search API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://0.0.0.0:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LEGAL_DOCUMENTS = [
    {
        "id": "doc_001",
        "title": "Contract Law Fundamentals",
        "content": """A contract is a legally binding agreement between two or more parties. 
        For a contract to be valid, it must contain several essential elements: offer, 
        acceptance, consideration, capacity, and lawful purpose. The offer must be clear 
        and definite, stating the terms of the agreement. Acceptance must be unconditional 
        and communicated to the offeror. Consideration refers to something of value 
        exchanged between the parties. Both parties must have the legal capacity to enter 
        into a contract, meaning they are of sound mind and legal age. Finally, the 
        contract's purpose must be lawful and not against public policy."""
    },
    {
        "id": "doc_002",
        "title": "Employment Law Guidelines",
        "content": """Employment law governs the relationship between employers and employees. 
        Key aspects include wage and hour laws, workplace safety regulations, and 
        anti-discrimination protections. The Fair Labor Standards Act (FLSA) establishes 
        minimum wage, overtime pay, and child labor standards. Employers must provide a 
        safe working environment under OSHA regulations. Discrimination based on race, 
        color, religion, sex, national origin, age, or disability is prohibited under 
        federal law. Employees have the right to organize and engage in collective 
        bargaining. Wrongful termination occurs when an employee is fired in violation 
        of legal protections or employment contracts."""
    },
    {
        "id": "doc_003",
        "title": "Intellectual Property Rights",
        "content": """Intellectual property (IP) refers to creations of the mind, including 
        inventions, literary and artistic works, designs, and symbols. There are four 
        main types of IP protection: patents, trademarks, copyrights, and trade secrets. 
        Patents protect inventions and grant exclusive rights for a limited period, 
        typically 20 years. Trademarks protect brand names, logos, and slogans that 
        distinguish goods or services. Copyrights protect original works of authorship, 
        including literature, music, and software, typically for the life of the author 
        plus 70 years. Trade secrets protect confidential business information that 
        provides a competitive advantage. IP infringement occurs when these rights are 
        violated without authorization."""
    }
]


class QueryRequest(BaseModel):
    query: str


class RelevantDocument(BaseModel):
    doc_id: str
    title: str
    excerpt: str
    relevance_score: float


class SearchResponse(BaseModel):
    summary: str
    relevant_docs: List[RelevantDocument]


class DocumentInfo(BaseModel):
    id: str
    title: str
    content_length: int


class DocsResponse(BaseModel):
    api_name: str
    version: str
    description: str
    total_documents: int
    documents: List[DocumentInfo]
    endpoints: List[dict]


def search_documents(query: str) -> SearchResponse:
    """
    Mock search function that finds relevant documents based on query keywords.
    In a real application, this would use vector embeddings or full-text search.
    """
    query_lower = query.lower()
    results = []

    keywords_map = {
        "contract": ["doc_001"],
        "employment": ["doc_002"],
        "patent": ["doc_003"],
        "trademark": ["doc_003"],
        "copyright": ["doc_003"],
        "wage": ["doc_002"],
        "discrimination": ["doc_002"],
        "agreement": ["doc_001"],
        "intellectual property": ["doc_003"],
        "ip": ["doc_003"]
    }
    
    matched_docs = set()
    for keyword, doc_ids in keywords_map.items():
        if keyword in query_lower:
            matched_docs.update(doc_ids)
    
    if not matched_docs:
        matched_docs = {doc["id"] for doc in LEGAL_DOCUMENTS}
    
    for doc in LEGAL_DOCUMENTS:
        if doc["id"] in matched_docs:
            score = 0.9 if any(kw in query_lower for kw, ids in keywords_map.items() if doc["id"] in ids) else 0.5
            
            excerpt = doc["content"].strip()[:200] + "..."
            
            results.append(RelevantDocument(
                doc_id=doc["id"],
                title=doc["title"],
                excerpt=excerpt,
                relevance_score=score
            ))
    
    results.sort(key=lambda x: x.relevance_score, reverse=True)
    
    summary = generate_summary(query, results)
    
    return SearchResponse(summary=summary, relevant_docs=results)


def generate_summary(query: str, relevant_docs: List[RelevantDocument]) -> str:
    """
    Generate a mock summary based on the query and relevant documents.
    """
    if not relevant_docs:
        return "No relevant documents found for your query."
    
    query_lower = query.lower()
    
    if "contract" in query_lower:
        return ("Based on the legal documents, a valid contract requires several essential "
                "elements including offer, acceptance, consideration, capacity, and lawful purpose. "
                "All parties must have legal capacity and the contract's purpose must be lawful.")
    elif "employment" in query_lower or "employee" in query_lower:
        return ("Employment law covers various aspects of the employer-employee relationship, "
                "including wage and hour regulations, workplace safety, and anti-discrimination "
                "protections. Employers must comply with federal standards and provide safe "
                "working conditions.")
    elif any(word in query_lower for word in ["patent", "trademark", "copyright", "intellectual property", "ip"]):
        return ("Intellectual property rights protect creations of the mind through patents, "
                "trademarks, copyrights, and trade secrets. Each type of protection serves "
                "different purposes and has specific duration and requirements.")
    else:
        return (f"Found {len(relevant_docs)} relevant legal document(s) related to your query. "
                "The documents provide information on various aspects of law including contracts, "
                "employment regulations, and intellectual property rights.")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "Legal Document Search API is running"}


@app.get("/docs", response_model=DocsResponse)
async def get_docs():
    """
    Custom documentation endpoint that provides information about available documents and API endpoints.
    Note: FastAPI also provides interactive documentation at /docs (Swagger UI) and /redoc (ReDoc)
    """
    documents_info = [
        DocumentInfo(
            id=doc["id"],
            title=doc["title"],
            content_length=len(doc["content"])
        )
        for doc in LEGAL_DOCUMENTS
    ]
    
    endpoints = [
        {
            "path": "/",
            "method": "GET",
            "description": "Health check endpoint"
        },
        {
            "path": "/docs",
            "method": "GET",
            "description": "Get API documentation and available legal documents"
        },
        {
            "path": "/generate",
            "method": "POST",
            "description": "Search legal documents and generate summary",
            "request_body": {
                "query": "string (required)"
            },
            "response": {
                "summary": "string",
                "relevant_docs": "array of documents with relevance scores"
            }
        }
    ]
    
    return DocsResponse(
        api_name="Legal Document Search API",
        version="1.0.0",
        description="API for searching and summarizing legal documents. Contains 3 hardcoded legal documents covering Contract Law, Employment Law, and Intellectual Property Rights.",
        total_documents=len(LEGAL_DOCUMENTS),
        documents=documents_info,
        endpoints=endpoints
    )


@app.post("/generate", response_model=SearchResponse)
async def generate_response(request: QueryRequest):
    """
    Main endpoint that processes queries and returns relevant legal documents with summary.
    """
    try:
        if not request.query or not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        response = search_documents(request.query)
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)