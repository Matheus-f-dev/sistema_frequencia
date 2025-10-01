import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8001/api/v1"

def popular_dados_demo():
    print("🎓 Populando Sistema com Dados de Demonstração")
    print("=" * 50)
    
    try:
        # 1. Criar turmas
        print("\n1. Criando turmas...")
        turmas_data = [
            {"nome": "3º Ano A", "ano": 2024},
            {"nome": "2º Ano B", "ano": 2024},
            {"nome": "1º Ano C", "ano": 2024}
        ]
        
        turmas_ids = []
        for turma_data in turmas_data:
            response = requests.post(f"{BASE_URL}/turmas/", json=turma_data)
            turma = response.json()
            turmas_ids.append(turma["id"])
            print(f"✅ Turma criada: {turma['nome']} (ID: {turma['id']})")
        
        # 2. Cadastrar alunos para primeira turma
        print(f"\n2. Cadastrando alunos na turma {turmas_ids[0]}...")
        alunos_data = [
            {"nome": "Ana Silva", "matricula": "2024001", "turma_id": turmas_ids[0]},
            {"nome": "Bruno Santos", "matricula": "2024002", "turma_id": turmas_ids[0]},
            {"nome": "Carlos Oliveira", "matricula": "2024003", "turma_id": turmas_ids[0]},
            {"nome": "Diana Costa", "matricula": "2024004", "turma_id": turmas_ids[0]},
            {"nome": "Eduardo Lima", "matricula": "2024005", "turma_id": turmas_ids[0]}
        ]
        
        alunos_ids = []
        for aluno_data in alunos_data:
            response = requests.post(f"{BASE_URL}/alunos/", json=aluno_data)
            aluno = response.json()
            alunos_ids.append(aluno["id"])
            print(f"✅ Aluno cadastrado: {aluno['nome']} (ID: {aluno['id']})")
        
        # 3. Criar sessões de aula
        print(f"\n3. Criando sessões para turma {turmas_ids[0]}...")
        disciplinas = ["Matemática", "Português", "História", "Geografia", "Ciências"]
        sessoes_ids = []
        
        for disciplina in disciplinas:
            sessao_data = {"disciplina": disciplina, "turma_id": turmas_ids[0]}
            response = requests.post(f"{BASE_URL}/sessoes/", json=sessao_data)
            sessao = response.json()
            sessoes_ids.append(sessao["id"])
            print(f"✅ Sessão criada: {sessao['disciplina']} (ID: {sessao['id']})")
        
        # 4. Marcar frequências variadas
        print("\n4. Marcando frequências...")
        import random
        
        for i, sessao_id in enumerate(sessoes_ids):
            frequencias = []
            for j, aluno_id in enumerate(alunos_ids):
                # Simular diferentes padrões de frequência
                if j == 0:  # Ana - excelente frequência
                    presente = True
                    justificado = False
                elif j == 1:  # Bruno - boa frequência com algumas faltas justificadas
                    presente = random.choice([True, True, True, False])
                    justificado = not presente and random.choice([True, False])
                elif j == 2:  # Carlos - frequência regular
                    presente = random.choice([True, True, False])
                    justificado = not presente and random.choice([True, False])
                else:  # Outros - frequência variada
                    presente = random.choice([True, False])
                    justificado = not presente and random.choice([True, False])
                
                frequencias.append({
                    "aluno_id": aluno_id,
                    "presente": presente,
                    "justificado": justificado,
                    "observacao": "Atestado médico" if justificado else None
                })
            
            response = requests.post(f"{BASE_URL}/frequencias/lote/", json={
                "sessao_id": sessao_id,
                "frequencias": frequencias
            })
            print(f"✅ Frequências marcadas para {disciplinas[i]}")
        
        print("\n🎉 Dados de demonstração criados com sucesso!")
        print(f"🌐 Acesse: http://127.0.0.1:8000")
        print(f"📊 Selecione a turma '{turmas_data[0]['nome']}' para ver os dados")
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Servidor não está rodando!")
        print("Execute: python main.py")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    popular_dados_demo()