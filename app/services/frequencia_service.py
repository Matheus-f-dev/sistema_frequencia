from sqlalchemy.orm import Session
from app.database import Turma, Aluno, Sessao, Frequencia, Disciplina, aluno_disciplina
from app.schemas import TurmaCreate, AlunoCreate, SessaoCreate, FrequenciaCreate, DisciplinaCreate, MatricularAluno, FrequenciaIndividual
from datetime import datetime, timedelta
import csv
import json
from typing import List, Dict

class FrequenciaService:
    
    @staticmethod
    def criar_turma(db: Session, turma: TurmaCreate):
        db_turma = Turma(**turma.dict())
        db.add(db_turma)
        db.commit()
        db.refresh(db_turma)
        return db_turma
    
    @staticmethod
    def listar_turmas(db: Session):
        return db.query(Turma).all()
    
    @staticmethod
    def criar_disciplina(db: Session, disciplina: DisciplinaCreate):
        db_disciplina = Disciplina(**disciplina.dict())
        db.add(db_disciplina)
        db.commit()
        db.refresh(db_disciplina)
        return db_disciplina
    
    @staticmethod
    def listar_disciplinas(db: Session):
        return db.query(Disciplina).all()
    
    @staticmethod
    def get_disciplina(db: Session, disciplina_id: int):
        return db.query(Disciplina).filter(Disciplina.id == disciplina_id).first()
    
    @staticmethod
    def criar_aluno(db: Session, aluno: AlunoCreate):
        aluno_data = aluno.dict()
        disciplina_ids = aluno_data.pop('disciplina_ids', [])
        
        db_aluno = Aluno(**aluno_data)
        db.add(db_aluno)
        db.commit()
        db.refresh(db_aluno)
        
        # Matricular aluno nas disciplinas
        for disciplina_id in disciplina_ids:
            disciplina = db.query(Disciplina).filter(Disciplina.id == disciplina_id).first()
            if disciplina:
                db_aluno.disciplinas.append(disciplina)
        
        db.commit()
        return db_aluno
    
    @staticmethod
    def matricular_aluno_disciplina(db: Session, matricula: MatricularAluno):
        aluno = db.query(Aluno).filter(Aluno.id == matricula.aluno_id).first()
        disciplina = db.query(Disciplina).filter(Disciplina.id == matricula.disciplina_id).first()
        
        if aluno and disciplina and disciplina not in aluno.disciplinas:
            aluno.disciplinas.append(disciplina)
            db.commit()
            return {"message": f"Aluno {aluno.nome} matriculado em {disciplina.nome}"}
        return {"error": "Matrícula não realizada"}
    
    @staticmethod
    def listar_alunos_turma(db: Session, turma_id: int):
        return db.query(Aluno).filter(Aluno.turma_id == turma_id).all()
    
    @staticmethod
    def listar_alunos_disciplina(db: Session, disciplina_id: int):
        disciplina = db.query(Disciplina).filter(Disciplina.id == disciplina_id).first()
        return disciplina.alunos if disciplina else []
    
    @staticmethod
    def criar_sessao(db: Session, sessao: SessaoCreate):
        data_sessao = sessao.data or datetime.now()
        db_sessao = Sessao(
            turma_id=sessao.turma_id,
            disciplina_id=sessao.disciplina_id,
            descricao=sessao.descricao,
            data=data_sessao
        )
        db.add(db_sessao)
        db.commit()
        db.refresh(db_sessao)
        return db_sessao
    
    @staticmethod
    def marcar_frequencia_individual(db: Session, frequencia: FrequenciaIndividual):
        # Verificar se aluno está matriculado na disciplina
        aluno = db.query(Aluno).filter(Aluno.id == frequencia.aluno_id).first()
        disciplina = db.query(Disciplina).filter(Disciplina.id == frequencia.disciplina_id).first()
        
        if not aluno or not disciplina:
            raise ValueError("Aluno ou disciplina não encontrados")
        
        if disciplina not in aluno.disciplinas:
            raise ValueError("Aluno não está matriculado nesta disciplina")
        
        # Criar sessão se não existir uma para hoje
        hoje = datetime.now().date()
        sessao = db.query(Sessao).filter(
            Sessao.disciplina_id == frequencia.disciplina_id,
            Sessao.turma_id == aluno.turma_id,
            Sessao.data >= hoje,
            Sessao.data < hoje + timedelta(days=1)
        ).first()
        
        if not sessao:
            sessao = Sessao(
                turma_id=aluno.turma_id,
                disciplina_id=frequencia.disciplina_id,
                data=datetime.now()
            )
            db.add(sessao)
            db.commit()
            db.refresh(sessao)
        
        # Verificar se já existe frequência para hoje
        freq_existente = db.query(Frequencia).filter(
            Frequencia.aluno_id == frequencia.aluno_id,
            Frequencia.sessao_id == sessao.id
        ).first()
        
        if freq_existente:
            # Atualizar frequência existente
            freq_existente.presente = frequencia.presente
            freq_existente.justificado = frequencia.justificado
            freq_existente.observacao = frequencia.observacao
            freq_existente.data_registro = datetime.now()
        else:
            # Criar nova frequência
            db_freq = Frequencia(
                aluno_id=frequencia.aluno_id,
                sessao_id=sessao.id,
                presente=frequencia.presente,
                justificado=frequencia.justificado,
                observacao=frequencia.observacao
            )
            db.add(db_freq)
        
        db.commit()
        return {"message": "Frequência registrada com sucesso"}
    
    @staticmethod
    def marcar_frequencia_lote(db: Session, sessao_id: int, frequencias: List[Dict]):
        for freq_data in frequencias:
            # Verificar se já existe frequência
            freq_existente = db.query(Frequencia).filter(
                Frequencia.aluno_id == freq_data['aluno_id'],
                Frequencia.sessao_id == sessao_id
            ).first()
            
            if freq_existente:
                freq_existente.presente = freq_data.get('presente', True)
                freq_existente.justificado = freq_data.get('justificado', False)
                freq_existente.observacao = freq_data.get('observacao')
                freq_existente.data_registro = datetime.now()
            else:
                db_freq = Frequencia(
                    aluno_id=freq_data['aluno_id'],
                    sessao_id=sessao_id,
                    presente=freq_data.get('presente', True),
                    justificado=freq_data.get('justificado', False),
                    observacao=freq_data.get('observacao')
                )
                db.add(db_freq)
        db.commit()
        return {"message": f"{len(frequencias)} frequências registradas"}
    
    @staticmethod
    def relatorio_aluno_disciplina(db: Session, aluno_id: int, disciplina_id: int):
        # Buscar frequências do aluno na disciplina
        frequencias = db.query(Frequencia).join(Sessao).filter(
            Frequencia.aluno_id == aluno_id,
            Sessao.disciplina_id == disciplina_id
        ).all()
        
        total = len(frequencias)
        presencas = sum(1 for f in frequencias if f.presente)
        faltas = total - presencas
        justificadas = sum(1 for f in frequencias if not f.presente and f.justificado)
        
        return {
            "aluno_id": aluno_id,
            "disciplina_id": disciplina_id,
            "total_sessoes": total,
            "presencas": presencas,
            "faltas": faltas,
            "faltas_justificadas": justificadas,
            "percentual_presenca": round((presencas / total * 100) if total > 0 else 0, 2)
        }
    
    @staticmethod
    def relatorio_aluno(db: Session, aluno_id: int):
        frequencias = db.query(Frequencia).filter(Frequencia.aluno_id == aluno_id).all()
        total = len(frequencias)
        presencas = sum(1 for f in frequencias if f.presente)
        faltas = total - presencas
        justificadas = sum(1 for f in frequencias if not f.presente and f.justificado)
        
        return {
            "aluno_id": aluno_id,
            "total_sessoes": total,
            "presencas": presencas,
            "faltas": faltas,
            "faltas_justificadas": justificadas,
            "percentual_presenca": round((presencas / total * 100) if total > 0 else 0, 2)
        }
    
    @staticmethod
    def relatorio_turma(db: Session, turma_id: int):
        try:
            alunos = db.query(Aluno).filter(Aluno.turma_id == turma_id).all()
            relatorio = []
            
            for aluno in alunos:
                freq_aluno = FrequenciaService.relatorio_aluno(db, aluno.id)
                freq_aluno['nome'] = aluno.nome
                freq_aluno['matricula'] = aluno.matricula
                relatorio.append(freq_aluno)
            
            return relatorio
        except Exception as e:
            print(f"Erro ao gerar relatório: {e}")
            return []
    
    @staticmethod
    def exportar_csv(db: Session, turma_id: int, filename: str):
        try:
            import os
            relatorio = FrequenciaService.relatorio_turma(db, turma_id)
            
            if not relatorio:
                raise ValueError("Nenhum dado encontrado para exportação")
            
            # Criar diretório data se não existir
            os.makedirs("data", exist_ok=True)
            filepath = os.path.abspath(f"data/{filename}")
            
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['nome', 'matricula', 'total_sessoes', 'presencas', 'faltas', 'faltas_justificadas', 'percentual_presenca']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(relatorio)
            
            return filepath
        except Exception as e:
            raise Exception(f"Erro ao exportar CSV: {str(e)}")