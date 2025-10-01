from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import TurmaCreate, AlunoCreate, SessaoCreate, FrequenciaLote, DisciplinaCreate, MatricularAluno, FrequenciaIndividual
from app.services.frequencia_service import FrequenciaService
from fastapi.responses import FileResponse
from typing import List
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/turmas/")
def criar_turma(turma: TurmaCreate, db: Session = Depends(get_db)):
    return FrequenciaService.criar_turma(db, turma)

@router.get("/turmas/")
def listar_turmas(db: Session = Depends(get_db)):
    return FrequenciaService.listar_turmas(db)

@router.post("/disciplinas/")
def criar_disciplina(disciplina: DisciplinaCreate, db: Session = Depends(get_db)):
    return FrequenciaService.criar_disciplina(db, disciplina)

@router.get("/disciplinas/")
def listar_disciplinas(db: Session = Depends(get_db)):
    return FrequenciaService.listar_disciplinas(db)

@router.get("/disciplinas/{disciplina_id}")
def get_disciplina(disciplina_id: int, db: Session = Depends(get_db)):
    disciplina = FrequenciaService.get_disciplina(db, disciplina_id)
    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    return disciplina

@router.post("/alunos/")
def criar_aluno(aluno: AlunoCreate, db: Session = Depends(get_db)):
    return FrequenciaService.criar_aluno(db, aluno)

@router.get("/turmas/{turma_id}/alunos/")
def listar_alunos_turma(turma_id: int, db: Session = Depends(get_db)):
    return FrequenciaService.listar_alunos_turma(db, turma_id)

@router.get("/disciplinas/{disciplina_id}/alunos/")
def listar_alunos_disciplina(disciplina_id: int, db: Session = Depends(get_db)):
    return FrequenciaService.listar_alunos_disciplina(db, disciplina_id)

@router.post("/matricular/")
def matricular_aluno_disciplina(matricula: MatricularAluno, db: Session = Depends(get_db)):
    return FrequenciaService.matricular_aluno_disciplina(db, matricula)

@router.post("/sessoes/")
def criar_sessao(sessao: SessaoCreate, db: Session = Depends(get_db)):
    return FrequenciaService.criar_sessao(db, sessao)

@router.post("/frequencias/individual/")
def marcar_frequencia_individual(frequencia: FrequenciaIndividual, db: Session = Depends(get_db)):
    try:
        return FrequenciaService.marcar_frequencia_individual(db, frequencia)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/frequencias/lote/")
def marcar_frequencia_lote(frequencia_lote: FrequenciaLote, db: Session = Depends(get_db)):
    return FrequenciaService.marcar_frequencia_lote(
        db, 
        frequencia_lote.sessao_id, 
        frequencia_lote.frequencias
    )

@router.get("/relatorio/aluno/{aluno_id}")
def relatorio_aluno(aluno_id: int, db: Session = Depends(get_db)):
    return FrequenciaService.relatorio_aluno(db, aluno_id)

@router.get("/relatorio/aluno/{aluno_id}/disciplina/{disciplina_id}")
def relatorio_aluno_disciplina(aluno_id: int, disciplina_id: int, db: Session = Depends(get_db)):
    return FrequenciaService.relatorio_aluno_disciplina(db, aluno_id, disciplina_id)

@router.get("/relatorio/turma/{turma_id}")
def relatorio_turma(turma_id: int, db: Session = Depends(get_db)):
    return FrequenciaService.relatorio_turma(db, turma_id)

@router.get("/exportar/turma/{turma_id}")
def exportar_csv_turma(turma_id: int, db: Session = Depends(get_db)):
    try:
        import os
        filename = f"relatorio_turma_{turma_id}.csv"
        filepath = FrequenciaService.exportar_csv(db, turma_id, filename)
        
        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail="Arquivo não encontrado")
        
        return FileResponse(
            path=filepath,
            filename=filename,
            media_type='text/csv'
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar arquivo: {str(e)}")