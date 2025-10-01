from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Boolean, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

SQLITE_DATABASE_URL = "sqlite:///./data/frequencia.db"

engine = create_engine(SQLITE_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Tabela de associação para alunos e disciplinas
aluno_disciplina = Table(
    'aluno_disciplina',
    Base.metadata,
    Column('aluno_id', Integer, ForeignKey('alunos.id'), primary_key=True),
    Column('disciplina_id', Integer, ForeignKey('disciplinas.id'), primary_key=True)
)

class Turma(Base):
    __tablename__ = "turmas"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True)
    ano = Column(Integer)
    periodo = Column(String)  # Manhã, Tarde, Noite
    
    alunos = relationship("Aluno", back_populates="turma")
    sessoes = relationship("Sessao", back_populates="turma")

class Disciplina(Base):
    __tablename__ = "disciplinas"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True)
    codigo = Column(String, unique=True, index=True)
    carga_horaria = Column(Integer)
    professor = Column(String)
    
    alunos = relationship("Aluno", secondary=aluno_disciplina, back_populates="disciplinas")
    sessoes = relationship("Sessao", back_populates="disciplina")

class Aluno(Base):
    __tablename__ = "alunos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    matricula = Column(String, unique=True, index=True)
    email = Column(String, nullable=True)
    turma_id = Column(Integer, ForeignKey("turmas.id"))
    
    turma = relationship("Turma", back_populates="alunos")
    disciplinas = relationship("Disciplina", secondary=aluno_disciplina, back_populates="alunos")
    frequencias = relationship("Frequencia", back_populates="aluno")

class Sessao(Base):
    __tablename__ = "sessoes"
    id = Column(Integer, primary_key=True, index=True)
    data = Column(DateTime, default=datetime.utcnow)
    turma_id = Column(Integer, ForeignKey("turmas.id"))
    disciplina_id = Column(Integer, ForeignKey("disciplinas.id"))
    descricao = Column(String, nullable=True)  # Tópico da aula
    
    turma = relationship("Turma", back_populates="sessoes")
    disciplina = relationship("Disciplina", back_populates="sessoes")
    frequencias = relationship("Frequencia", back_populates="sessao")

class Frequencia(Base):
    __tablename__ = "frequencias"
    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id"))
    sessao_id = Column(Integer, ForeignKey("sessoes.id"))
    presente = Column(Boolean, default=True)
    justificado = Column(Boolean, default=False)
    observacao = Column(String, nullable=True)
    data_registro = Column(DateTime, default=datetime.utcnow)
    
    aluno = relationship("Aluno", back_populates="frequencias")
    sessao = relationship("Sessao", back_populates="frequencias")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)