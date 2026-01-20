"""
Main entry point for the FastAPI application.
Run with: uvicorn main:app --reload
"""
from ms_fa import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)

