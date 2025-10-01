from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routes.api import router
from app.database import Base, engine

app = FastAPI(title="Sistema de Frequência Escolar", version="1.0.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

# Configurar arquivos estáticos e templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(router, prefix="/api/v1")

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api")
def api_info():
    return {"message": "Sistema de Frequência Escolar - API funcionando!", "docs": "/docs"}

@app.get("/favicon.ico")
def favicon():
    return FileResponse("static/favicon.ico")

if __name__ == "__main__":
    import uvicorn
    print("Sistema de Frequencia Escolar")
    print("Interface Web: http://127.0.0.1:8002")
    print("API Docs: http://127.0.0.1:8002/docs")
    print("Iniciando servidor...")
    uvicorn.run(app, host="127.0.0.1", port=8002)