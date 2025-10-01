class FrequenciaApp {
    constructor() {
        this.baseURL = window.location.origin + '/api/v1';
        this.currentAluno = null;
        this.currentDisciplina = null;
        this.init();
    }

    init() {
        this.loadTurmas();
        this.loadDisciplinas();
        this.loadAlunos();
        this.setupEventListeners();
        // Carregar relatório inicial após um pequeno delay
        setTimeout(() => this.atualizarRelatorio(), 1000);
    }

    setupEventListeners() {
        document.getElementById('turmaForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.criarTurma();
        });

        document.getElementById('disciplinaForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.criarDisciplina();
        });

        document.getElementById('alunoForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.criarAluno();
        });

        document.getElementById('frequenciaDisciplina').addEventListener('change', (e) => {
            this.currentDisciplina = e.target.value;
            this.loadAlunosDisciplina();
        });

        document.getElementById('frequenciaAluno').addEventListener('change', (e) => {
            this.currentAluno = e.target.value;
            this.showFrequenciaCard();
        });
    }

    async request(url, options = {}) {
        try {
            const response = await fetch(`${this.baseURL}${url}`, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            this.showAlert(`Erro: ${error.message}`, 'error');
            throw error;
        }
    }

    async criarTurma() {
        const nome = document.getElementById('turmaNome').value;
        const ano = parseInt(document.getElementById('turmaAno').value);
        const periodo = document.getElementById('turmaPeriodo').value;

        try {
            await this.request('/turmas/', {
                method: 'POST',
                body: JSON.stringify({ nome, ano, periodo })
            });

            this.showAlert('Turma criada com sucesso!', 'success');
            document.getElementById('turmaForm').reset();
            this.loadTurmas();
            setTimeout(() => this.atualizarRelatorio(), 500);
        } catch (error) {
            console.error('Erro ao criar turma:', error);
        }
    }

    async criarDisciplina() {
        const nome = document.getElementById('disciplinaNome').value;
        const codigo = document.getElementById('disciplinaCodigo').value;
        const carga_horaria = parseInt(document.getElementById('disciplinaCarga').value);
        const professor = document.getElementById('disciplinaProfessor').value;

        try {
            await this.request('/disciplinas/', {
                method: 'POST',
                body: JSON.stringify({ nome, codigo, carga_horaria, professor })
            });

            this.showAlert('Disciplina cadastrada com sucesso!', 'success');
            document.getElementById('disciplinaForm').reset();
            this.loadDisciplinas();
            setTimeout(() => this.atualizarRelatorio(), 500);
        } catch (error) {
            console.error('Erro ao criar disciplina:', error);
        }
    }

    async criarAluno() {
        const nome = document.getElementById('alunoNome').value;
        const matricula = document.getElementById('alunoMatricula').value;
        const email = document.getElementById('alunoEmail').value;
        const turma_id = parseInt(document.getElementById('alunoTurma').value);

        if (!turma_id) {
            this.showAlert('Selecione uma turma!', 'error');
            return;
        }

        try {
            await this.request('/alunos/', {
                method: 'POST',
                body: JSON.stringify({ nome, matricula, email, turma_id })
            });

            this.showAlert('Aluno cadastrado com sucesso!', 'success');
            document.getElementById('alunoForm').reset();
            this.loadAlunos();
            setTimeout(() => this.atualizarRelatorio(), 500);
        } catch (error) {
            console.error('Erro ao criar aluno:', error);
        }
    }

    async matricularAluno() {
        const aluno_id = parseInt(document.getElementById('matriculaAluno').value);
        const disciplina_id = parseInt(document.getElementById('matriculaDisciplina').value);

        if (!aluno_id || !disciplina_id) {
            this.showAlert('Selecione aluno e disciplina!', 'error');
            return;
        }

        try {
            const result = await this.request('/matricular/', {
                method: 'POST',
                body: JSON.stringify({ aluno_id, disciplina_id })
            });

            this.showAlert(result.message || 'Aluno matriculado com sucesso!', 'success');
            document.getElementById('matriculaAluno').value = '';
            document.getElementById('matriculaDisciplina').value = '';
            setTimeout(() => this.atualizarRelatorio(), 500);
        } catch (error) {
            console.error('Erro ao matricular aluno:', error);
        }
    }

    async loadTurmas() {
        try {
            const turmas = await this.request('/turmas/');
            const select = document.getElementById('alunoTurma');
            
            select.innerHTML = '<option value="">Selecione uma turma</option>';
            turmas.forEach(turma => {
                select.innerHTML += `<option value="${turma.id}">${turma.nome} - ${turma.ano} (${turma.periodo})</option>`;
            });
        } catch (error) {
            console.error('Erro ao carregar turmas:', error);
        }
    }

    async loadDisciplinas() {
        try {
            const disciplinas = await this.request('/disciplinas/');
            
            // Atualizar select de matrícula
            const selectMatricula = document.getElementById('matriculaDisciplina');
            selectMatricula.innerHTML = '<option value="">Selecione uma disciplina</option>';
            
            // Atualizar select de frequência
            const selectFrequencia = document.getElementById('frequenciaDisciplina');
            selectFrequencia.innerHTML = '<option value="">Selecione uma disciplina</option>';
            
            disciplinas.forEach(disciplina => {
                const option = `<option value="${disciplina.id}">${disciplina.nome} (${disciplina.codigo}) - Prof. ${disciplina.professor}</option>`;
                selectMatricula.innerHTML += option;
                selectFrequencia.innerHTML += option;
            });
        } catch (error) {
            console.error('Erro ao carregar disciplinas:', error);
        }
    }

    async loadAlunos() {
        try {
            const turmas = await this.request('/turmas/');
            const select = document.getElementById('matriculaAluno');
            
            select.innerHTML = '<option value="">Selecione um aluno</option>';
            
            for (const turma of turmas) {
                const alunos = await this.request(`/turmas/${turma.id}/alunos/`);
                if (alunos.length > 0) {
                    const optgroup = document.createElement('optgroup');
                    optgroup.label = `${turma.nome} - ${turma.ano}`;
                    
                    alunos.forEach(aluno => {
                        const option = document.createElement('option');
                        option.value = aluno.id;
                        option.textContent = `${aluno.nome} (${aluno.matricula})`;
                        optgroup.appendChild(option);
                    });
                    
                    select.appendChild(optgroup);
                }
            }
        } catch (error) {
            console.error('Erro ao carregar alunos:', error);
        }
    }

    async loadAlunosDisciplina() {
        if (!this.currentDisciplina) return;

        try {
            const alunos = await this.request(`/disciplinas/${this.currentDisciplina}/alunos/`);
            const select = document.getElementById('frequenciaAluno');
            
            select.innerHTML = '<option value="">Selecione um aluno</option>';
            alunos.forEach(aluno => {
                select.innerHTML += `<option value="${aluno.id}">${aluno.nome} (${aluno.matricula})</option>`;
            });

            if (alunos.length === 0) {
                select.innerHTML = '<option value="">Nenhum aluno matriculado nesta disciplina</option>';
            }
        } catch (error) {
            console.error('Erro ao carregar alunos da disciplina:', error);
        }
    }

    async showFrequenciaCard() {
        if (!this.currentAluno || !this.currentDisciplina) return;

        try {
            // Buscar informações do aluno
            const alunos = await this.request(`/disciplinas/${this.currentDisciplina}/alunos/`);
            const aluno = alunos.find(a => a.id == this.currentAluno);
            
            if (!aluno) return;

            // Buscar informações da disciplina
            const disciplina = await this.request(`/disciplinas/${this.currentDisciplina}`);

            // Mostrar card de frequência
            const card = document.getElementById('frequenciaCard');
            const alunoInfo = document.getElementById('alunoInfo');
            
            alunoInfo.innerHTML = `
                <div class="student-info">
                    <div class="student-name">${aluno.nome}</div>
                    <div class="student-details">
                        Matrícula: ${aluno.matricula} | 
                        Disciplina: ${disciplina.nome} | 
                        Professor: ${disciplina.professor}
                    </div>
                </div>
            `;
            
            card.style.display = 'block';
        } catch (error) {
            console.error('Erro ao mostrar card de frequência:', error);
        }
    }

    async marcarFrequencia(presente, justificado) {
        if (!this.currentAluno || !this.currentDisciplina) {
            this.showAlert('Selecione aluno e disciplina!', 'error');
            return;
        }

        const observacao = document.getElementById('observacao').value;

        try {
            await this.request('/frequencias/individual/', {
                method: 'POST',
                body: JSON.stringify({
                    aluno_id: parseInt(this.currentAluno),
                    disciplina_id: parseInt(this.currentDisciplina),
                    presente: presente,
                    justificado: justificado,
                    observacao: observacao || null
                })
            });

            const status = presente ? 'Presente' : (justificado ? 'Falta Justificada' : 'Falta');
            this.showAlert(`Frequência registrada: ${status}`, 'success');
            
            // Limpar observação
            document.getElementById('observacao').value = '';
            
            // Resetar seleções
            document.getElementById('frequenciaAluno').value = '';
            document.getElementById('frequenciaCard').style.display = 'none';
            this.currentAluno = null;
            
        } catch (error) {
            console.error('Erro ao marcar frequência:', error);
        }
    }

    showAlert(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type}`;
        alertDiv.innerHTML = `
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    ${type === 'success' ? 
                        '<path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>' : 
                        '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>'}
                </svg>
                ${message}
            </div>
        `;
        
        document.body.insertBefore(alertDiv, document.body.firstChild);
        
        setTimeout(() => {
            alertDiv.style.opacity = '0';
            alertDiv.style.transform = 'translateY(-20px)';
            setTimeout(() => alertDiv.remove(), 300);
        }, 3000);
    }

    async atualizarRelatorio() {
        try {
            const turmas = await this.request('/turmas/');
            const disciplinas = await this.request('/disciplinas/');
            
            if (turmas.length === 0 || disciplinas.length === 0) {
                document.getElementById('relatorioContainer').innerHTML = `
                    <div class="empty-state">
                        <div class="empty-state-icon">📊</div>
                        <div class="empty-state-title">Configure o sistema primeiro</div>
                        <div class="empty-state-description">Cadastre turmas, disciplinas e alunos para visualizar relatórios</div>
                    </div>
                `;
                return;
            }
            
            await this.gerarRelatorioGeral();
            this.showAlert('Relatório atualizado!', 'success');
        } catch (error) {
            console.error('Erro ao atualizar relatório:', error);
        }
    }
    
    async gerarRelatorioGeral() {
        try {
            const turmas = await this.request('/turmas/');
            const disciplinas = await this.request('/disciplinas/');
            
            // Calcular estatísticas gerais
            let totalAlunos = 0;
            let totalPresencas = 0;
            let totalFaltas = 0;
            let totalJustificadas = 0;
            
            for (const turma of turmas) {
                const alunos = await this.request(`/turmas/${turma.id}/alunos/`);
                totalAlunos += alunos.length;
                
                for (const aluno of alunos) {
                    try {
                        const relatorioAluno = await this.request(`/relatorio/aluno/${aluno.id}`);
                        totalPresencas += relatorioAluno.presencas || 0;
                        totalFaltas += relatorioAluno.faltas || 0;
                        totalJustificadas += relatorioAluno.faltas_justificadas || 0;
                    } catch (e) {
                        // Ignorar se não houver dados de frequência
                    }
                }
            }
            
            let relatorioHTML = `
                <div class="stats">
                    <div class="stat-card primary">
                        <div class="stat-number">${turmas.length}</div>
                        <div class="stat-label">Turmas</div>
                    </div>
                    <div class="stat-card success">
                        <div class="stat-number">${disciplinas.length}</div>
                        <div class="stat-label">Disciplinas</div>
                    </div>
                    <div class="stat-card success">
                        <div class="stat-number">${totalAlunos}</div>
                        <div class="stat-label">Alunos</div>
                    </div>
                    <div class="stat-card ${totalPresencas > 0 ? 'success' : 'warning'}">
                        <div class="stat-number">${totalPresencas}</div>
                        <div class="stat-label">Presenças</div>
                    </div>
                    <div class="stat-card ${totalFaltas > 0 ? 'warning' : 'success'}">
                        <div class="stat-number">${totalFaltas}</div>
                        <div class="stat-label">Faltas</div>
                    </div>
                    <div class="stat-card ${totalJustificadas > 0 ? 'warning' : 'success'}">
                        <div class="stat-number">${totalJustificadas}</div>
                        <div class="stat-label">Justificadas</div>
                    </div>
                </div>
                
                <h4 style="margin: 2rem 0 1rem 0;">Relatório Detalhado de Frequência</h4>
            `;
            
            for (const turma of turmas) {
                const alunos = await this.request(`/turmas/${turma.id}/alunos/`);
                
                if (alunos.length > 0) {
                    relatorioHTML += `
                        <div class="card" style="margin-bottom: 1.5rem;">
                            <h3>${turma.nome} - ${turma.ano} (${turma.periodo})</h3>
                            <p style="color: #64748b; margin-bottom: 1rem;">${alunos.length} alunos matriculados</p>
                            
                            <table class="data-table">
                                <thead>
                                    <tr>
                                        <th>Aluno</th>
                                        <th>Matrícula</th>
                                        <th>Presenças</th>
                                        <th>Faltas</th>
                                        <th>Justificadas</th>
                                        <th>Total Sessões</th>
                                        <th>Frequência</th>
                                        <th>Status</th>
                                    </tr>
                                </thead>
                                <tbody>
                    `;
                    
                    for (const aluno of alunos) {
                        try {
                            const relatorioAluno = await this.request(`/relatorio/aluno/${aluno.id}`);
                            const percentual = relatorioAluno.percentual_presenca || 0;
                            const status = percentual >= 75 ? 'Aprovado' : percentual >= 50 ? 'Atenção' : 'Reprovado';
                            const statusClass = percentual >= 75 ? 'success' : percentual >= 50 ? 'warning' : 'danger';
                            const progressClass = percentual >= 75 ? 'success' : percentual >= 50 ? 'warning' : 'danger';
                            
                            relatorioHTML += `
                                <tr>
                                    <td><strong>${aluno.nome}</strong></td>
                                    <td><span class="badge badge-success">${aluno.matricula}</span></td>
                                    <td><span class="badge badge-success">${relatorioAluno.presencas || 0}</span></td>
                                    <td><span class="badge badge-danger">${relatorioAluno.faltas || 0}</span></td>
                                    <td><span class="badge badge-warning">${relatorioAluno.faltas_justificadas || 0}</span></td>
                                    <td>${relatorioAluno.total_sessoes || 0}</td>
                                    <td>
                                        <div class="progress-bar">
                                            <div class="progress-fill ${progressClass}" style="width: ${percentual}%"></div>
                                        </div>
                                        <small>${percentual}%</small>
                                    </td>
                                    <td><span class="badge badge-${statusClass}">${status}</span></td>
                                </tr>
                            `;
                        } catch (e) {
                            // Se não houver dados de frequência, mostrar zeros
                            relatorioHTML += `
                                <tr>
                                    <td><strong>${aluno.nome}</strong></td>
                                    <td><span class="badge badge-success">${aluno.matricula}</span></td>
                                    <td><span class="badge badge-success">0</span></td>
                                    <td><span class="badge badge-danger">0</span></td>
                                    <td><span class="badge badge-warning">0</span></td>
                                    <td>0</td>
                                    <td>
                                        <div class="progress-bar">
                                            <div class="progress-fill" style="width: 0%"></div>
                                        </div>
                                        <small>0%</small>
                                    </td>
                                    <td><span class="badge badge-warning">Sem dados</span></td>
                                </tr>
                            `;
                        }
                    }
                    
                    relatorioHTML += `
                                </tbody>
                            </table>
                        </div>
                    `;
                }
            }
            
            // Relatório por disciplina
            if (disciplinas.length > 0) {
                relatorioHTML += `
                    <div class="card">
                        <h3>Relatório por Disciplina</h3>
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>Disciplina</th>
                                    <th>Professor</th>
                                    <th>Alunos</th>
                                    <th>Sessões</th>
                                    <th>Presenças</th>
                                    <th>Faltas</th>
                                    <th>Média Frequência</th>
                                </tr>
                            </thead>
                            <tbody>
                `;
                
                for (const disciplina of disciplinas) {
                    try {
                        const alunosDisciplina = await this.request(`/disciplinas/${disciplina.id}/alunos/`);
                        let totalPresencasDisciplina = 0;
                        let totalFaltasDisciplina = 0;
                        let totalSessoesDisciplina = 0;
                        let alunosComDados = 0;
                        
                        for (const aluno of alunosDisciplina) {
                            try {
                                const relatorioAlunoDisciplina = await this.request(`/relatorio/aluno/${aluno.id}/disciplina/${disciplina.id}`);
                                totalPresencasDisciplina += relatorioAlunoDisciplina.presencas || 0;
                                totalFaltasDisciplina += relatorioAlunoDisciplina.faltas || 0;
                                totalSessoesDisciplina += relatorioAlunoDisciplina.total_sessoes || 0;
                                if (relatorioAlunoDisciplina.total_sessoes > 0) alunosComDados++;
                            } catch (e) {
                                // Ignorar alunos sem dados
                            }
                        }
                        
                        const mediaFrequencia = totalSessoesDisciplina > 0 ? 
                            Math.round((totalPresencasDisciplina / totalSessoesDisciplina) * 100) : 0;
                        const statusFrequencia = mediaFrequencia >= 75 ? 'success' : mediaFrequencia >= 50 ? 'warning' : 'danger';
                        
                        relatorioHTML += `
                            <tr>
                                <td><strong>${disciplina.nome}</strong><br><small>${disciplina.codigo}</small></td>
                                <td>${disciplina.professor}</td>
                                <td><span class="badge badge-success">${alunosDisciplina.length}</span></td>
                                <td><span class="badge badge-primary">${Math.floor(totalSessoesDisciplina / Math.max(alunosComDados, 1))}</span></td>
                                <td><span class="badge badge-success">${totalPresencasDisciplina}</span></td>
                                <td><span class="badge badge-danger">${totalFaltasDisciplina}</span></td>
                                <td>
                                    <div class="progress-bar">
                                        <div class="progress-fill ${statusFrequencia}" style="width: ${mediaFrequencia}%"></div>
                                    </div>
                                    <small>${mediaFrequencia}%</small>
                                </td>
                            </tr>
                        `;
                    } catch (e) {
                        relatorioHTML += `
                            <tr>
                                <td><strong>${disciplina.nome}</strong><br><small>${disciplina.codigo}</small></td>
                                <td>${disciplina.professor}</td>
                                <td><span class="badge badge-warning">0</span></td>
                                <td><span class="badge badge-warning">0</span></td>
                                <td><span class="badge badge-success">0</span></td>
                                <td><span class="badge badge-danger">0</span></td>
                                <td>
                                    <div class="progress-bar">
                                        <div class="progress-fill" style="width: 0%"></div>
                                    </div>
                                    <small>0%</small>
                                </td>
                            </tr>
                        `;
                    }
                }
            
                relatorioHTML += `
                            </tbody>
                        </table>
                    </div>
                `;
            }
            
            relatorioHTML += `
                <div style="margin-top: 1.5rem; display: flex; gap: 0.75rem; justify-content: center;">
                    <button class="btn btn-outline" onclick="app.atualizarRelatorio()">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M17.65,6.35C16.2,4.9 14.21,4 12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20C15.73,20 18.84,17.45 19.73,14H17.65C16.83,16.33 14.61,18 12,18A6,6 0 0,1 6,12A6,6 0 0,1 12,6C13.66,6 15.14,6.69 16.22,7.78L13,11H20V4L17.65,6.35Z"/>
                        </svg>
                        Atualizar Dados
                    </button>
                </div>
            `;
            
            document.getElementById('relatorioContainer').innerHTML = relatorioHTML;
            
        } catch (error) {
            console.error('Erro ao gerar relatório:', error);
            document.getElementById('relatorioContainer').innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">❌</div>
                    <div class="empty-state-title">Erro ao carregar relatório</div>
                    <div class="empty-state-description">Verifique se há dados cadastrados no sistema</div>
                </div>
            `;
        }
    }
    

}

// Inicializar app quando a página carregar
let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new FrequenciaApp();
});