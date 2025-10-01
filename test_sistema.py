import requests
import time

def test_sistema():
    base_url = "http://127.0.0.1:8001"
    api_url = f"{base_url}/api/v1"
    
    print("Testando Sistema de Frequência...")
    
    try:
        # Teste 1: Verificar se servidor está rodando
        response = requests.get(base_url, timeout=5)
        print("✅ Servidor está rodando")
        
        # Teste 2: Criar turma
        turma_data = {"nome": "Teste Turma", "ano": 2024}
        response = requests.post(f"{api_url}/turmas/", json=turma_data)
        if response.status_code == 200:
            turma = response.json()
            print(f"✅ Turma criada: {turma['nome']}")
            
            # Teste 3: Criar aluno
            aluno_data = {"nome": "Aluno Teste", "matricula": "TEST001", "turma_id": turma["id"]}
            response = requests.post(f"{api_url}/alunos/", json=aluno_data)
            if response.status_code == 200:
                aluno = response.json()
                print(f"✅ Aluno criado: {aluno['nome']}")
                
                # Teste 4: Criar sessão
                sessao_data = {"disciplina": "Teste", "turma_id": turma["id"]}
                response = requests.post(f"{api_url}/sessoes/", json=sessao_data)
                if response.status_code == 200:
                    sessao = response.json()
                    print(f"✅ Sessão criada: {sessao['disciplina']}")
                    
                    # Teste 5: Marcar frequência
                    freq_data = {
                        "sessao_id": sessao["id"],
                        "frequencias": [{"aluno_id": aluno["id"], "presente": True}]
                    }
                    response = requests.post(f"{api_url}/frequencias/lote/", json=freq_data)
                    if response.status_code == 200:
                        print("✅ Frequência marcada")
                        
                        # Teste 6: Gerar relatório
                        response = requests.get(f"{api_url}/relatorio/turma/{turma['id']}")
                        if response.status_code == 200:
                            relatorio = response.json()
                            print(f"✅ Relatório gerado: {len(relatorio)} alunos")
                            
                            print("\n🎉 Todos os testes passaram!")
                            print(f"🌐 Acesse: {base_url}")
                            return True
        
        print("❌ Algum teste falhou")
        return False
        
    except requests.exceptions.ConnectionError:
        print("❌ Servidor não está rodando!")
        print("Execute: python main.py")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    test_sistema()