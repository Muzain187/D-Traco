from fastapi import APIRouter, HTTPException
import whois

router = APIRouter()

@router.get('/domain-check', response_model=dict)
async def domain_check(domain_name: str):
    """
    A function that returns a boolean indicating 
    whether a `domain_name` is registered
    """
    try:
        w = whois.whois(domain_name)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to check domain")
    
    is_available = not bool(w.domain_name)
    
    return {"is_available": is_available, "status_code": 200 if is_available else 409}
