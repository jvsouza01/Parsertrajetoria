// Estado Global da Aplicação
let questoesData = [];
let currentIndex = 0;
let currentBanca = 'FCC';

// Inicialização de Elementos e Eventos
document.addEventListener('DOMContentLoaded', () => {
  setupTheme();
  setupDragAndDrop();
  setupInputs();
});

// Configuração do Tema Dark / Light
function setupTheme() {
  const btn = document.getElementById('btnThemeToggle');
  const icon = document.getElementById('themeIcon');
  const savedTheme = localStorage.getItem('studio_theme') || 'dark';
  
  document.documentElement.setAttribute('data-bs-theme', savedTheme);
  updateThemeIcon(savedTheme, icon);

  btn.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-bs-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-bs-theme', next);
    localStorage.setItem('studio_theme', next);
    updateThemeIcon(next, icon);
  });
}

function updateThemeIcon(theme, icon) {
  if (theme === 'dark') {
    icon.className = 'bi bi-moon-stars-fill text-warning';
  } else {
    icon.className = 'bi bi-sun-fill text-warning';
  }
}

// Drag and Drop e Seleção de Arquivos
function setupDragAndDrop() {
  const dropProva = document.getElementById('dropZoneProva');
  const fileProva = document.getElementById('fileProva');
  const dropGabarito = document.getElementById('dropZoneGabarito');
  const fileGabarito = document.getElementById('fileGabarito');

  // Prova Drop Zone
  dropProva.addEventListener('dragover', (e) => { e.preventDefault(); dropProva.classList.add('dragover'); });
  dropProva.addEventListener('dragleave', () => dropProva.classList.remove('dragover'));
  dropProva.addEventListener('drop', (e) => {
    e.preventDefault();
    dropProva.classList.remove('dragover');
    if (e.dataTransfer.files.length) {
      fileProva.files = e.dataTransfer.files;
      handleProvaFileSelected(fileProva.files[0]);
    }
  });
  fileProva.addEventListener('change', () => {
    if (fileProva.files.length) handleProvaFileSelected(fileProva.files[0]);
  });

  // Gabarito Drop Zone
  dropGabarito.addEventListener('dragover', (e) => { e.preventDefault(); dropGabarito.classList.add('dragover'); });
  dropGabarito.addEventListener('dragleave', () => dropGabarito.classList.remove('dragover'));
  dropGabarito.addEventListener('drop', (e) => {
    e.preventDefault();
    dropGabarito.classList.remove('dragover');
    if (e.dataTransfer.files.length) {
      fileGabarito.files = e.dataTransfer.files;
      handleGabaritoFileSelected(fileGabarito.files[0]);
    }
  });
  fileGabarito.addEventListener('change', () => {
    if (fileGabarito.files.length) handleGabaritoFileSelected(fileGabarito.files[0]);
  });
}

function handleProvaFileSelected(file) {
  const lbl = document.getElementById('selectedProvaName');
  const status = document.getElementById('lblProvaStatus');
  lbl.textContent = `✓ ${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)`;
  lbl.classList.remove('d-none');
  status.textContent = "Arquivo pronto";
  status.className = "text-success small fw-semibold";
}

function handleGabaritoFileSelected(file) {
  const lbl = document.getElementById('selectedGabaritoName');
  lbl.textContent = `✓ ${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)`;
  lbl.classList.remove('d-none');
}

function setupInputs() {
  const inputBanca = document.getElementById('inputBanca');
  inputBanca.addEventListener('input', (e) => {
    currentBanca = e.target.value;
  });
}

function setBanca(banca) {
  currentBanca = banca;
  document.getElementById('inputBanca').value = banca;
  document.querySelectorAll('.btn-preset').forEach(btn => {
    if (btn.textContent.trim().toUpperCase() === banca.toUpperCase()) {
      btn.classList.add('active');
    } else {
      btn.classList.remove('active');
    }
  });
}

// Processamento da Prova via API
async function processarProva() {
  const fileProvaInput = document.getElementById('fileProva');
  if (!fileProvaInput.files.length) {
    alert('Por favor, selecione ou arraste o arquivo PDF da Prova.');
    return;
  }

  const formData = new FormData();
  formData.append('prova_pdf', fileProvaInput.files[0]);

  const fileGabaritoInput = document.getElementById('fileGabarito');
  if (fileGabaritoInput.files.length) {
    formData.append('gabarito_pdf', fileGabaritoInput.files[0]);
  }

  const gabaritoText = document.getElementById('txtGabaritoDirect').value;
  if (gabaritoText) {
    formData.append('gabarito_text', gabaritoText);
  }

  formData.append('banca', document.getElementById('inputBanca').value || 'FCC');
  formData.append('orgao', document.getElementById('inputOrgao').value || '');
  formData.append('cargo', document.getElementById('inputCargo').value || '');
  formData.append('ano', document.getElementById('inputAno').value || '2025');
  formData.append('dificuldade', document.getElementById('selectDificuldade').value || 'FACIL');

  // Exibe Loading
  document.getElementById('stepUploadSection').classList.add('d-none');
  document.getElementById('loadingSection').classList.remove('d-none');

  try {
    const response = await fetch('/api/parse', {
      method: 'POST',
      body: formData
    });

    const data = await response.json();
    document.getElementById('loadingSection').classList.add('d-none');

    if (!data.success) {
      alert(`Erro ao processar: ${data.error}`);
      document.getElementById('stepUploadSection').classList.remove('d-none');
      return;
    }

    questoesData = data.questoes || [];
    if (questoesData.length === 0) {
      alert('Nenhuma questão foi detectada. Verifique se o PDF é legível ou tente selecionar outra banca.');
      document.getElementById('stepUploadSection').classList.remove('d-none');
      return;
    }

    // Atualiza estatísticas
    document.getElementById('statTotalQuestoes').textContent = questoesData.length;
    const gabCount = questoesData.filter(q => q.gabaritoOficial).length;
    document.getElementById('statGabaritosEncontrados').textContent = gabCount;
    
    // Atualiza modais
    document.getElementById('batchEndQ').value = questoesData.length;
    document.getElementById('sendModalTotalCount').textContent = questoesData.length;

    // Mostra tela de revisão
    document.getElementById('stepReviewSection').classList.remove('d-none');
    currentIndex = 0;
    renderQuestionNav();
    renderQuestionDetail(0);

  } catch (err) {
    document.getElementById('loadingSection').classList.add('d-none');
    document.getElementById('stepUploadSection').classList.remove('d-none');
    alert(`Erro na requisição: ${err.message}`);
  }
}

// Renderização da Lista de Navegação
function renderQuestionNav() {
  const container = document.getElementById('questionNavList');
  container.innerHTML = '';

  questoesData.forEach((q, idx) => {
    const item = document.createElement('div');
    item.className = `question-nav-item ${idx === currentIndex ? 'active' : ''}`;
    item.onclick = () => selectQuestion(idx);

    const gabBadge = q.gabaritoOficial 
      ? `<span class="badge bg-success font-monospace">${q.gabaritoOficial}</span>`
      : `<span class="badge bg-secondary">Sem Gab</span>`;

    item.innerHTML = `
      <div class="d-flex align-items-center gap-2 text-truncate">
        <span class="fw-bold font-monospace">Q${String(q.posicao).padStart(2, '0')}</span>
        <span class="small text-muted text-truncate" style="max-width: 130px;">${q.materiaNome || 'Geral'}</span>
      </div>
      <div>${gabBadge}</div>
    `;

    container.appendChild(item);
  });
}

function selectQuestion(idx) {
  if (idx < 0 || idx >= questoesData.length) return;
  salvarEdicaoAtual();
  currentIndex = idx;
  renderQuestionNav();
  renderQuestionDetail(idx);
}

function navegarQuestao(delta) {
  selectQuestion(currentIndex + delta);
}

// Renderização do Editor Visual da Questão Selecionada
function renderQuestionDetail(idx) {
  const q = questoesData[idx];
  if (!q) return;

  document.getElementById('lblSelectedNumero').textContent = `Q${String(q.posicao).padStart(2, '0')}`;
  document.getElementById('lblSelectedIdOrigem').textContent = q.idOrigem || `ID_Q${q.posicao}`;
  document.getElementById('editMateria').value = q.materiaNome || '';
  document.getElementById('editDificuldade').value = q.dificuldade || 'FACIL';
  document.getElementById('editGabaritoLetra').value = q.gabaritoOficial || '';
  document.getElementById('editEnunciado').value = q.enunciado || '';

  const altsContainer = document.getElementById('containerAlternativas');
  altsContainer.innerHTML = '';

  (q.alternativas || []).forEach((alt, aIdx) => {
    const card = document.createElement('div');
    const isCorrect = alt.correta || (alt.letra === q.gabaritoOficial);
    card.className = `alt-card ${isCorrect ? 'correct' : ''}`;
    
    card.innerHTML = `
      <button type="button" class="alt-badge-btn" onclick="definirAlternativaCorreta('${alt.letra}')" title="Marcar como correta">
        ${alt.letra}
      </button>
      <textarea class="alt-input" rows="2" oninput="atualizarTextoAlternativa(${aIdx}, this.value)">${alt.texto || ''}</textarea>
    `;

    altsContainer.appendChild(card);
  });
}

// Atualizações e Edições em Tempo Real
function salvarEdicaoAtual() {
  if (!questoesData[currentIndex]) return;
  const q = questoesData[currentIndex];
  q.materiaNome = document.getElementById('editMateria').value;
  q.dificuldade = document.getElementById('editDificuldade').value;
  q.enunciado = document.getElementById('editEnunciado').value;
}

function definirAlternativaCorreta(letra) {
  const q = questoesData[currentIndex];
  if (!q) return;
  q.gabaritoOficial = letra.toUpperCase();
  document.getElementById('editGabaritoLetra').value = q.gabaritoOficial;

  q.alternativas.forEach(alt => {
    alt.correta = (alt.letra === q.gabaritoOficial);
  });

  renderQuestionDetail(currentIndex);
  renderQuestionNav();
}

function atualizarGabaritoManual(letra) {
  definirAlternativaCorreta(letra.trim().toUpperCase());
}

function atualizarTextoAlternativa(altIdx, novoTexto) {
  const q = questoesData[currentIndex];
  if (q && q.alternativas && q.alternativas[altIdx]) {
    q.alternativas[altIdx].texto = novoTexto;
  }
}

function excluirQuestaoAtual() {
  if (confirm(`Tem certeza que deseja remover a Questão Q${questoesData[currentIndex].posicao}?`)) {
    questoesData.splice(currentIndex, 1);
    if (currentIndex >= questoesData.length) currentIndex = Math.max(0, questoesData.length - 1);
    document.getElementById('statTotalQuestoes').textContent = questoesData.length;
    renderQuestionNav();
    renderQuestionDetail(currentIndex);
  }
}

function adicionarNovaQuestao() {
  const nextPos = questoesData.length + 1;
  const novaQ = {
    posicao: nextPos,
    idOrigem: `${currentBanca}_MANUAL_Q${String(nextPos).padStart(2, '0')}`,
    materiaNome: 'Geral',
    dificuldade: 'FACIL',
    enunciado: 'Novo enunciado...',
    gabaritoOficial: 'A',
    anulada: false,
    alternativas: [
      { letra: 'A', texto: 'Alternativa A', correta: true },
      { letra: 'B', texto: 'Alternativa B', correta: false },
      { letra: 'C', texto: 'Alternativa C', correta: false },
      { letra: 'D', texto: 'Alternativa D', correta: false },
      { letra: 'E', texto: 'Alternativa E', correta: false }
    ]
  };
  questoesData.push(novaQ);
  selectQuestion(questoesData.length - 1);
}

// Filtro e Busca
function filtrarQuestoes() {
  const termo = document.getElementById('searchQuestoes').value.toLowerCase();
  const items = document.querySelectorAll('.question-nav-item');
  questoesData.forEach((q, idx) => {
    const match = (q.enunciado || '').toLowerCase().includes(termo) ||
                  (q.materiaNome || '').toLowerCase().includes(termo) ||
                  String(q.posicao).includes(termo);
    if (items[idx]) {
      items[idx].style.display = match ? 'flex' : 'none';
    }
  });
}

// Ações em Lote
function aplicarAcoesEmLote() {
  const start = parseInt(document.getElementById('batchStartQ').value) || 1;
  const end = parseInt(document.getElementById('batchEndQ').value) || questoesData.length;
  const materia = document.getElementById('batchMateriaNome').value.trim();
  const dif = document.getElementById('batchDificuldade').value;

  questoesData.forEach(q => {
    if (q.posicao >= start && q.posicao <= end) {
      if (materia) q.materiaNome = materia;
      if (dif) q.dificuldade = dif;
    }
  });

  const modal = bootstrap.Modal.getInstance(document.getElementById('batchModal'));
  if (modal) modal.hide();

  renderQuestionNav();
  renderQuestionDetail(currentIndex);
}

// Exportação JSON
async function exportarJson() {
  salvarEdicaoAtual();
  try {
    const response = await fetch('/api/export-json', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        questoes: questoesData,
        filename: `payload_${currentBanca.toLowerCase()}_${new Date().getTime()}.json`
      })
    });

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `payload_${currentBanca.toLowerCase()}_questoes.json`;
    document.body.appendChild(a);
    a.click();
    a.remove();
  } catch (err) {
    alert(`Erro ao exportar JSON: ${err.message}`);
  }
}

// Envio para o Backend Trajetória
function abrirModalEnvio() {
  salvarEdicaoAtual();
  document.getElementById('sendModalTotalCount').textContent = questoesData.length;
  document.getElementById('sendProgressArea').classList.add('d-none');
  document.getElementById('sendResultLogs').classList.add('d-none');
  document.getElementById('sendResultLogs').innerHTML = '';
  document.getElementById('btnConfirmarEnvio').disabled = false;

  const modal = new bootstrap.Modal(document.getElementById('sendModal'));
  modal.show();
}

async function executarEnvioBackend() {
  const apiUrl = document.getElementById('cfgApiUrl').value || 'http://localhost:8080/api/admin/ingestao/questoes';
  const token = document.getElementById('cfgApiToken').value || '';

  const progressBar = document.getElementById('sendProgressBar');
  const progressStatus = document.getElementById('sendProgressStatus');
  const progressArea = document.getElementById('sendProgressArea');
  const logArea = document.getElementById('sendResultLogs');
  const btn = document.getElementById('btnConfirmarEnvio');

  btn.disabled = true;
  progressArea.classList.remove('d-none');
  logArea.classList.remove('d-none');
  progressBar.style.width = '30%';
  progressBar.textContent = '30%';
  progressStatus.textContent = 'Disparando requisições para a API...';

  try {
    const response = await fetch('/api/send-backend', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        questoes: questoesData,
        apiUrl: apiUrl,
        token: token
      })
    });

    const data = await response.json();
    progressBar.style.width = '100%';
    progressBar.textContent = '100%';

    if (data.success) {
      progressBar.className = 'progress-bar bg-success';
      progressStatus.textContent = `✓ Sucesso! ${data.enviadas || questoesData.length} questões enviadas com sucesso!`;
      logArea.innerHTML = `<div class="text-success fw-bold">✓ Envio concluído com sucesso!</div>`;
      if (data.detalhes) {
        data.detalhes.forEach(d => {
          logArea.innerHTML += `<div>[${d.status}] ${d.idOrigem}</div>`;
        });
      }
    } else {
      progressBar.className = 'progress-bar bg-danger';
      progressStatus.textContent = `Falha no envio: ${data.error || 'Verifique se a API está online'}`;
      logArea.innerHTML = `<div class="text-danger fw-bold">✕ Erro no envio: ${data.error || 'Verifique se a API em ' + apiUrl + ' está rodando.'}</div>`;
    }
  } catch (err) {
    progressBar.className = 'progress-bar bg-danger';
    progressBar.style.width = '100%';
    progressStatus.textContent = `Erro de conexão com o servidor: ${err.message}`;
    logArea.innerHTML = `<div class="text-danger fw-bold">✕ Erro de conexão: ${err.message}</div>`;
  }
}
