from fastapi import FastAPI
from app.api.routes import router as doc_router
from app.api.routes import router as search_router
from app.api.routes import router as qa_router
# from app.services.reindex import rebuild_index
from app.api.routes import router
from app.api.admin import router as admin_router
from app.api.transcription import router as transcription_router
app = FastAPI(
    title="AI-Powered Document Intelligence Hub",
    version="1.0.0"
)

app.include_router(doc_router)
app.include_router(search_router)
app.include_router(qa_router)
app.include_router(router, prefix="/rag")
app.include_router(admin_router)
app.include_router(transcription_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

# @app.on_event("startup")
# def startup_event():
#     rebuild_index()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
