import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api/v1"

def exemplo_completo():
    print("🎓 Sistema de Frequência Escolar - Exemplo de Uso")
    print("=" * 50)
    
    # 1. Criar turma
    print("\n1. Criando turma...")
    turma_data = {"nome": "3º Ano A", "ano": 2024}
    response = requests.post(f"{BASE_URL}/turmas/", json=turma_data)
    turma = response.json()
    turma_id = turma["id"]
    print(f"✅ Turma criada: {turma['nome']} (ID: {turma_id})")
    
    # 2. Cadastrar alunos
    print("\n2. Cadastrando alunos...")
    alunos = [
        {"nome": "João Silva", "matricula": "2024001", "turma_id": turma_id},
        {"nome": "Maria Santos", "matricula": "2024002", "turma_id": turma_id},
        {"nome": "Pedro Costa", "matricula": "2024003", "turma_id": turma_id}
    ]
    
    alunos_ids = []
    for aluno_data in alunos:
        response = requests.post(f"{BASE_URL}/alunos/", json=aluno_data)
        aluno = response.json()
        alunos_ids.append(aluno["id"])
        print(f"✅ Aluno cadastrado: {aluno['nome']} (ID: {aluno['id']})")
    
    # 3. Criar sessão de aula
    print("\n3. Criando sessão de aula...")
    sessao_data = {"disciplina": "Matemática", "turma_id": turma_id}
    response = requests.post(f"{BASE_URL}/sessoes/", json=sessao_data)
    sessao = response.json()
    sessao_id = sessao["id"]
    print(f"✅ Sessão criada: {sessao['disciplina']} (ID: {sessao_id})")
    
    # 4. Marcar frequências em lote
    print("\n4. Marcando frequências...")
    frequencias_data = {
        "sessao_id": sessao_id,
        "frequencias": [
            {"aluno_id": alunos_ids[0], "presente": True},
            {"aluno_id": alunos_ids[1], "presente": False, "justificado": True, "observacao": "Atestado médico"},
            {"aluno_id": alunos_ids[2], "presente": False, "justificado": False}
        ]
    }
    response = requests.post(f"{BASE_URL}/frequencias/lote/", json=frequencias_data)
    print(f"✅ {response.json()['message']}")
    
    # 5. Gerar relatório da turma
    print("\n5. Relatório da turma:")
    response = requests.get(f"{BASE_URL}/relatorio/turma/{turma_id}")
    relatorio = response.json()
    
    for aluno in relatorio:
        status = "🟢" if aluno["percentual_presenca"] >= 75 else "🔴"
        print(f"{status} {aluno['nome']}: {aluno['percentual_presenca']}% presença")
    
    # 6. Exportar CSV
    print("\n6. Exportando relatório CSV...")
    response = requests.get(f"{BASE_URL}/exportar/turma/{turma_id}")
    if response.status_code == 200:
        print("✅ Arquivo CSV exportado com sucesso!")
    
    print("\n🎉 Exemplo concluído! Sistema funcionando perfeitamente.")

if __name__ == "__main__":
    try:
        exemplo_completo()
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Servidor não está rodando!")
        print("Execute: python main.py")