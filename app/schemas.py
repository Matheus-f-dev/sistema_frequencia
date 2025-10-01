from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class TurmaBase(BaseModel):
    nome: str
    ano: int
    periodo: str

class TurmaCreate(TurmaBase):
    pass

class Turma(TurmaBase):
    id: int
    class Config:
        from_attributes = True

class DisciplinaBase(BaseModel):
    nome: str
    codigo: str
    carga_horaria: int
    professor: str

class DisciplinaCreate(DisciplinaBase):
    pass

class Disciplina(DisciplinaBase):
    id: int
    class Config:
        from_attributes = True

class AlunoBase(BaseModel):
    nome: str
    matricula: str
    email: Optional[str] = None

class AlunoCreate(AlunoBase):
    turma_id: int
    disciplina_ids: List[int] = []

class Aluno(AlunoBase):
    id: int
    turma_id: int
    class Config:
        from_attributes = True

class SessaoBase(BaseModel):
    turma_id: int
    disciplina_id: int
    descricao: Optional[str] = None

class SessaoCreate(SessaoBase):
    data: Optional[datetime] = None

class Sessao(SessaoBase):
    id: int
    data: datetime
    class Config:
        from_attributes = True

class FrequenciaBase(BaseModel):
    presente: bool = True
    justificado: bool = False
    observacao: Optional[str] = None

class FrequenciaCreate(FrequenciaBase):
    aluno_id: int
    sessao_id: int

class FrequenciaIndividual(BaseModel):
    aluno_id: int
    disciplina_id: int
    presente: bool = True
    justificado: bool = False
    observacao: Optional[str] = None

class FrequenciaLote(BaseModel):
    sessao_id: int
    frequencias: List[dict]

class Frequencia(FrequenciaBase):
    id: int
    aluno_id: int
    sessao_id: int
    data_registro: datetime
    class Config:
        from_attributes = True

class MatricularAluno(BaseModel):
    aluno_id: int
    disciplina_id: int