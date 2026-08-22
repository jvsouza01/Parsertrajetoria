// Estado Global da Aplicação
let questoesData = [];
let currentIndex = 0;
let currentBanca = 'FCC';
let geminiApiKey = localStorage.getItem('gemini_api_key') || '';

// Inicialização de Elementos e Eventos
document.addEventListener('DOMContentLoaded', () => {
  setupTheme();
  setupDragAndDrop();
  setupInputs();
  setupClipboardPaste();
  initAiConfig();
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

// Configuração de IA
function initAiConfig() {
  const inputKey = document.getElementById('inputGeminiApiKey');
  if (inputKey) {
    inputKey.value = geminiApiKey;
  }
}

function toggleApiKeyVisibility() {
  const input = document.getElementById('inputGeminiApiKey');
  const icon = document.getElementById('iconShowKey');
  if (input.type === 'password') {
    input.type = 'text';
    icon.className = 'bi bi-eye-slash';
  } else {
    input.type = 'password';
    icon.className = 'bi bi-eye';
  }
}

function salvarConfiguracaoIA() {
  const input = document.getElementById('inputGeminiApiKey');
  if (input && input.value.trim()) {
    geminiApiKey = input.value.trim();
    localStorage.setItem('gemini_api_key', geminiApiKey);
  }
}

async function testarConexaoGemini() {
  const inputKey = document.getElementById('inputGeminiApiKey').value.trim() || geminiApiKey;
  const resultDiv = document.getElementById('aiTestResult');
  resultDiv.className = 'alert alert-info py-2 px-3 small rounded-3 mb-0';
  resultDiv.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span> Testando conexão com Gemini...';
  resultDiv.classList.remove('d-none');

  try {
    const response = await fetch('/api/ai/test-key', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ api_key: inputKey })
    });

    const data = await response.json();
    if (data.success) {
      resultDiv.className = 'alert alert-success py-2 px-3 small rounded-3 mb-0';
      resultDiv.innerHTML = `✓ <strong>Conectado com sucesso!</strong> Modelo ativo: <code>${data.model}</code>`;
      salvarConfiguracaoIA();
    } else {
      resultDiv.className = 'alert alert-danger py-2 px-3 small rounded-3 mb-0';
      resultDiv.innerHTML = `✗ <strong>Falha na conexão:</strong> ${data.error}`;
    }
  } catch (err) {
    resultDiv.className = 'alert alert-danger py-2 px-3 small rounded-3 mb-0';
    resultDiv.innerHTML = `✗ <strong>Erro na requisição:</strong> ${err.message}`;
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

// Captura de Prints / Ctrl+V da Área de Transferência
function setupClipboardPaste() {
  document.addEventListener('paste', (e) => {
    // Apenas se a tela de revisão estiver ativa
    if (document.getElementById('stepReviewSection').classList.contains('d-none')) return;
    
    const items = (e.clipboardData || e.originalEvent.clipboardData).items;
    for (const item of items) {
      if (item.type.indexOf('image') !== -1) {
        const blob = item.getAsFile();
        handleImagemUpload(blob);
        break;
      }
    }
  });
}

// Upload e Vinculação de Imagens da Questão
async function handleImagemUpload(file) {
  if (!file || !questoesData[currentIndex]) return;
  const q = questoesData[currentIndex];

  const formData = new FormData();
  formData.append('image', file);
  formData.append('idOrigem', q.idOrigem || `Q${q.posicao}`);

  try {
    const response = await fetch('/api/upload-image', {
      method: 'POST',
      body: formData
    });

    const data = await response.json();
    if (data.success) {
      q.imagemUrl = data.imagemUrl;
      renderQuestionDetail(currentIndex);
      renderQuestionNav();
    } else {
      alert(`Erro no upload da imagem: ${data.error}`);
    }
  } catch (err) {
    alert(`Erro ao enviar imagem: ${err.message}`);
  }
}

function removerImagemQuestao() {
  if (questoesData[currentIndex]) {
    questoesData[currentIndex].imagemUrl = null;
    renderQuestionDetail(currentIndex);
    renderQuestionNav();
  }
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
  formData.append('api_key', geminiApiKey);

  const engine = document.querySelector('input[name="extractionEngine"]:checked')?.value || 'gemini';
  const targetEndpoint = engine === 'gemini' ? '/api/ai/parse-pdf' : '/api/parse';

  // Exibe Loading
  const loadingText = document.getElementById('loadingStatusText');
  if (engine === 'gemini') {
    loadingText.textContent = 'Processando páginas com Google Gemini (resolvendo colunas, gabaritos e alternativas)...';
  } else {
    loadingText.textContent = 'Extraindo páginas em alta velocidade e estruturando alternativas...';
  }

  document.getElementById('stepUploadSection').classList.add('d-none');
  document.getElementById('loadingSection').classList.remove('d-none');

  try {
    const response = await fetch(targetEndpoint, {
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
      alert('Nenhuma questão foi detectada. Verifique se o PDF é legível.');
      document.getElementById('stepUploadSection').classList.remove('d-none');
      return;
    }

    // Atualiza estatísticas com segurança
    const elStatTotal = document.getElementById('statTotalQuestoes');
    if (elStatTotal) elStatTotal.textContent = questoesData.length;

    const gabCount = questoesData.filter(q => q.gabaritoOficial).length;
    const elStatGabaritos = document.getElementById('statGabaritosEncontrados');
    if (elStatGabaritos) elStatGabaritos.textContent = gabCount;

    const elBatchEnd = document.getElementById('batchEndQ');
    if (elBatchEnd) elBatchEnd.value = questoesData.length;

    // Mostra tela de revisão
    const stepReview = document.getElementById('stepReviewSection');
    if (stepReview) stepReview.classList.remove('d-none');
    
    currentIndex = 0;
    renderQuestionNav();
    renderQuestionDetail(0);

  } catch (err) {
    const loadingSec = document.getElementById('loadingSection');
    if (loadingSec) loadingSec.classList.add('d-none');
    
    const stepUpload = document.getElementById('stepUploadSection');
    if (stepUpload) stepUpload.classList.remove('d-none');
    
    console.error('Erro na requisição ou renderização:', err);
    alert(`Erro na requisição: ${err.message}`);
  }
}

// Renderização da Lista de Navegação
function renderQuestionNav() {
  const container = document.getElementById('questionNavList');
  if (!container) return;
  container.innerHTML = '';

  questoesData.forEach((q, idx) => {
    const item = document.createElement('div');
    item.className = `question-nav-item ${idx === currentIndex ? 'active' : ''}`;
    item.onclick = () => selectQuestion(idx);

    const gabBadge = q.gabaritoOficial 
      ? `<span class="badge bg-success font-monospace">${q.gabaritoOficial}</span>`
      : `<span class="badge bg-secondary">Sem Gab</span>`;

    let aiAuditBadge = '';
    if (q.aiAudit) {
      if (q.aiAudit.statusRevisao === 'APROVADO_AUTO') {
        aiAuditBadge = `<span class="badge status-badge-aprovado ms-1" title="Aprovado pela IA (${Math.round(q.aiAudit.confianca * 100)}%)"><i class="bi bi-check-circle-fill"></i></span>`;
      } else {
        aiAuditBadge = `<span class="badge status-badge-pendente ms-1" title="Atenção: Necessita revisão manual"><i class="bi bi-exclamation-triangle-fill"></i></span>`;
      }
    }

    const imgBadge = q.imagemUrl 
      ? `<i class="bi bi-image text-success ms-1" title="Imagem anexada"></i>` 
      : (q.temImagem ? `<i class="bi bi-image text-warning ms-1" title="Contém figura/imagem detectada"></i>` : '');

    const materiaLabel = q.materiaNome 
      ? `<span class="small text-muted text-truncate" style="max-width: 110px;">${q.materiaNome}</span>`
      : `<span class="badge bg-secondary-subtle text-muted small font-monospace" title="Será classificado automaticamente pela IA do backend">IA Auto</span>`;

    item.innerHTML = `
      <div class="d-flex align-items-center gap-2 text-truncate">
        <span class="fw-bold font-monospace">Q${String(q.posicao).padStart(2, '0')}</span>
        ${materiaLabel}
      </div>
      <div class="d-flex align-items-center">${imgBadge} ${gabBadge} ${aiAuditBadge}</div>
    `;

    container.appendChild(item);
  });
}

function selectQuestion(idx) {
  if (!questoesData || idx < 0 || idx >= questoesData.length) return;
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
  if (!questoesData || !questoesData[idx]) return;
  const q = questoesData[idx];

  const elNum = document.getElementById('lblSelectedNumero');
  if (elNum) elNum.textContent = `Q${String(q.posicao).padStart(2, '0')}`;

  const elId = document.getElementById('lblSelectedIdOrigem');
  if (elId) elId.textContent = q.idOrigem || `ID_Q${q.posicao}`;

  const elMat = document.getElementById('editMateria');
  if (elMat) elMat.value = q.materiaNome || '';

  const elGab = document.getElementById('editGabaritoLetra');
  if (elGab) elGab.value = q.gabaritoOficial || '';

  const elTb = document.getElementById('editTextoBase');
  if (elTb) elTb.value = q.textoBase || q.textoApoio || '';

  const elEnun = document.getElementById('editEnunciado');
  if (elEnun) elEnun.value = q.enunciado || '';

  // Imagem / Preview
  const imgContainer = document.getElementById('containerImagemPreview');
  const dropZone = document.getElementById('dropZoneImagem');
  const imgEl = document.getElementById('imgQuestaoPreview');

  if (q.imagemUrl) {
    if (imgContainer) imgContainer.classList.remove('d-none');
    if (dropZone) dropZone.classList.add('d-none');
    if (imgEl) imgEl.src = q.imagemUrl.startsWith('/') ? q.imagemUrl : `/api/${q.imagemUrl}`;
  } else {
    if (imgContainer) imgContainer.classList.add('d-none');
    if (dropZone) dropZone.classList.remove('d-none');
    if (imgEl) imgEl.src = '';
  }

  // Painel de Auditoria de IA
  const auditCard = document.getElementById('aiAuditCard');
  if (q.aiAudit) {
    auditCard.classList.remove('d-none');
    document.getElementById('lblAiConfianca').textContent = `Confiança: ${Math.round((q.aiAudit.confianca || 1.0) * 100)}%`;
    document.getElementById('lblAiModel').textContent = q.aiAudit.modelUsed || 'Gemini';

    const badgeStatus = document.getElementById('badgeAiStatus');
    if (q.aiAudit.statusRevisao === 'APROVADO_AUTO') {
      badgeStatus.className = 'badge status-badge-aprovado';
      badgeStatus.innerHTML = '<i class="bi bi-check-lg me-1"></i> Aprovado Auto';
    } else {
      badgeStatus.className = 'badge status-badge-pendente';
      badgeStatus.innerHTML = '<i class="bi bi-exclamation-triangle me-1"></i> Pendente Revisão';
    }

    // Melhorias Aplicadas
    const melhoriasContainer = document.getElementById('containerAiMelhorias');
    melhoriasContainer.innerHTML = '';
    const melhorias = q.aiAudit.melhoriasAplicadas && q.aiAudit.melhoriasAplicadas.length > 0 
      ? q.aiAudit.melhoriasAplicadas 
      : ['Estrutura e gabarito validados'];

    melhorias.forEach(m => {
      const span = document.createElement('span');
      span.className = 'tag-badge';
      span.textContent = m;
      melhoriasContainer.appendChild(span);
    });

    // Alertas de Auditoria
    const alertasContainer = document.getElementById('containerAiAlertas');
    const lblAlertas = document.getElementById('lblAiAlertas');
    if (q.aiAudit.motivosRevisao && q.aiAudit.motivosRevisao.length > 0) {
      alertasContainer.classList.remove('d-none');
      lblAlertas.innerHTML = `<i class="bi bi-info-circle me-1"></i> <strong>Atenção:</strong> ${q.aiAudit.motivosRevisao.join(' | ')}`;
    } else {
      alertasContainer.classList.add('d-none');
    }
  } else {
    auditCard.classList.add('d-none');
  }

  // Alternativas
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
  if (!questoesData || !questoesData[currentIndex]) return;
  const q = questoesData[currentIndex];

  const elMat = document.getElementById('editMateria');
  if (elMat) {
    const matVal = (elMat.value || '').trim();
    q.materiaNome = (matVal === '[IA Automática (null)]' || matVal === '' || matVal === 'null') ? null : matVal;
  }
  
  const elTb = document.getElementById('editTextoBase');
  if (elTb) {
    const tbVal = (elTb.value || '').trim();
    q.textoBase = tbVal ? tbVal : null;
    q.textoApoio = q.textoBase;
  }
  
  const elEnun = document.getElementById('editEnunciado');
  if (elEnun) {
    q.enunciado = elEnun.value;
  }
}

function definirAlternativaCorreta(letra) {
  if (!questoesData || !questoesData[currentIndex]) return;
  const q = questoesData[currentIndex];
  q.gabaritoOficial = letra.toUpperCase();

  const elGab = document.getElementById('editGabaritoLetra');
  if (elGab) elGab.value = q.gabaritoOficial;

  (q.alternativas || []).forEach(alt => {
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
    materiaNome: null,
    textoBase: null,
    textoApoio: null,
    enunciado: 'Novo comando da questão...',
    gabaritoOficial: 'A',
    anulada: false,
    imagemUrl: null,
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

// Refinamento de IA Individual (1 Questão)
async function refinarQuestaoAtualIA() {
  salvarEdicaoAtual();
  const q = questoesData[currentIndex];
  if (!q) return;

  const btn = document.getElementById('btnRefinarQuestaoIA');
  const originalHtml = btn.innerHTML;
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span> Refinando...';

  try {
    const response = await fetch('/api/ai/enhance-question', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        questao: q,
        api_key: geminiApiKey,
        metadata: {
          banca: document.getElementById('inputBanca').value || currentBanca,
          cargo: document.getElementById('inputCargo').value || '',
          ano: document.getElementById('inputAno').value || '2025'
        }
      })
    });

    const data = await response.json();
    if (!data.success) {
      alert(`Erro na IA: ${data.error}`);
      return;
    }

    questoesData[currentIndex] = data.questao;
    renderQuestionNav();
    renderQuestionDetail(currentIndex);

  } catch (err) {
    alert(`Erro ao comunicar com a IA: ${err.message}`);
  } finally {
    btn.disabled = false;
    btn.innerHTML = originalHtml;
  }
}

// Refinamento em Lote com IA (Todas as Questões)
async function iniciarRefinamentoLoteIA() {
  if (!questoesData.length) return;
  salvarEdicaoAtual();

  const modalEl = document.getElementById('aiProgressModal');
  const modal = new bootstrap.Modal(modalEl);
  modal.show();

  const statusText = document.getElementById('aiProgressStatusText');
  const counterText = document.getElementById('aiProgressCounter');
  statusText.textContent = `Auditando ${questoesData.length} questões com Google Gemini...`;
  counterText.textContent = 'Enviando lote para auditoria estrutural e limpeza...';

  try {
    const response = await fetch('/api/ai/batch-enhance', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        questoes: questoesData,
        api_key: geminiApiKey,
        metadata: {
          banca: document.getElementById('inputBanca').value || currentBanca,
          cargo: document.getElementById('inputCargo').value || '',
          ano: document.getElementById('inputAno').value || '2025'
        }
      })
    });

    const data = await response.json();
    modal.hide();

    if (!data.success) {
      alert(`Erro no processamento em lote: ${data.error}`);
      return;
    }

    questoesData = data.questoes;
    renderQuestionNav();
    renderQuestionDetail(currentIndex);
    alert(`✓ ${questoesData.length} questões tratadas e auditadas com sucesso pelo Gemini!`);

  } catch (err) {
    modal.hide();
    alert(`Erro no processamento: ${err.message}`);
  }
}

// Vinculação de Texto de Apoio em Lote
function aplicarTextoApoioLote() {
  const start = parseInt(document.getElementById('textoApoioStartQ').value) || 1;
  const end = parseInt(document.getElementById('textoApoioEndQ').value) || questoesData.length;
  const textoApoio = document.getElementById('txtTextoApoioConteudo').value.trim();

  if (!textoApoio) {
    alert('Por favor, cole o texto de apoio que deseja vincular.');
    return;
  }

  questoesData.forEach(q => {
    if (q.posicao >= start && q.posicao <= end) {
      q.textoBase = textoApoio;
      q.textoApoio = textoApoio;
    }
  });

  const modal = bootstrap.Modal.getInstance(document.getElementById('textoApoioModal'));
  if (modal) modal.hide();

  renderQuestionNav();
  renderQuestionDetail(currentIndex);
  alert(`✓ Texto de apoio vinculado com sucesso ao campo textoBase das questões Q${String(start).padStart(2, '0')} até Q${String(end).padStart(2, '0')}!`);
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

// Ações em Lote (Matérias)
function aplicarAcoesEmLote() {
  const start = parseInt(document.getElementById('batchStartQ').value) || 1;
  const end = parseInt(document.getElementById('batchEndQ').value) || questoesData.length;
  const rawMateria = document.getElementById('batchMateriaNome').value.trim();
  const materiaFinal = (rawMateria === '[IA Automática (null)]' || rawMateria === '' || rawMateria === 'null') ? null : rawMateria;

  questoesData.forEach(q => {
    if (q.posicao >= start && q.posicao <= end) {
      q.materiaNome = materiaFinal;
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

// ==============================================================================
// CONTROLE DA ESTEIRA AUTOMÁTICA (PILOTO AUTOMÁTICO)
// ==============================================================================
let esteiraPollingInterval = null;
let isEsteiraRunning = false;

async function toggleEsteira() {
  if (isEsteiraRunning) {
    await stopEsteira();
  } else {
    await startEsteira();
  }
}

async function startEsteira() {
  const folderInput = document.getElementById('inputEsteiraFolder');
  const folder = folderInput ? folderInput.value.trim() : '';

  if (!folder) {
    alert('Por favor, informe a pasta com os PDFs das provas.');
    return;
  }

  try {
    const btn = document.getElementById('btnToggleEsteira');
    if (btn) btn.disabled = true;

    const response = await fetch('/api/batch/start', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        folder: folder,
        api_key: geminiApiKey
      })
    });

    const data = await response.json();
    if (data.success) {
      isEsteiraRunning = true;
      updateEsteiraUIState(true);
      startEsteiraPolling();
    } else {
      alert(`Aviso da esteira: ${data.message}`);
    }
  } catch (err) {
    alert(`Erro ao iniciar esteira: ${err.message}`);
  } finally {
    const btn = document.getElementById('btnToggleEsteira');
    if (btn) btn.disabled = false;
  }
}

async function stopEsteira() {
  try {
    const btn = document.getElementById('btnToggleEsteira');
    if (btn) btn.disabled = true;

    const response = await fetch('/api/batch/stop', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });

    const data = await response.json();
    isEsteiraRunning = false;
    updateEsteiraUIState(false);
  } catch (err) {
    alert(`Erro ao parar esteira: ${err.message}`);
  } finally {
    const btn = document.getElementById('btnToggleEsteira');
    if (btn) btn.disabled = false;
  }
}

function updateEsteiraUIState(running) {
  const btn = document.getElementById('btnToggleEsteira');
  const icon = document.getElementById('iconBtnEsteira');
  const lbl = document.getElementById('lblBtnEsteira');
  const badge = document.getElementById('esteiraStatusBadge');
  const pulse = document.getElementById('esteiraPulseBadge');

  if (running) {
    if (btn) {
      btn.className = 'btn btn-danger fw-bold w-100 py-2 shadow-sm d-flex align-items-center justify-content-center gap-2';
    }
    if (icon) icon.className = 'bi bi-pause-circle-fill fs-5';
    if (lbl) lbl.textContent = 'Pausar Esteira';
    if (badge) {
      badge.className = 'badge rounded-pill bg-success';
      badge.textContent = '🟢 Ativa / Monitorando';
    }
    if (pulse) pulse.classList.remove('d-none');
  } else {
    if (btn) {
      btn.className = 'btn btn-success fw-bold w-100 py-2 shadow-sm d-flex align-items-center justify-content-center gap-2';
    }
    if (icon) icon.className = 'bi bi-play-circle-fill fs-5';
    if (lbl) lbl.textContent = 'Ligar Esteira';
    if (badge) {
      badge.className = 'badge rounded-pill bg-secondary';
      badge.textContent = '⚪ Parada';
    }
    if (pulse) pulse.classList.add('d-none');
  }
}

function startEsteiraPolling() {
  if (esteiraPollingInterval) clearInterval(esteiraPollingInterval);
  pollEsteiraStatus();
  esteiraPollingInterval = setInterval(pollEsteiraStatus, 2500);
}

async function pollEsteiraStatus() {
  try {
    const response = await fetch('/api/batch/status');
    const data = await response.json();

    isEsteiraRunning = data.running;
    updateEsteiraUIState(data.running);

    // Atualiza métricas
    if (data.stats) {
      const elProvas = document.getElementById('metricProvasProcessadas');
      if (elProvas) elProvas.textContent = data.stats.provas_processadas || 0;

      const elQuestoes = document.getElementById('metricQuestoesExtraidas');
      if (elQuestoes) elQuestoes.textContent = data.stats.questoes_extraidas || 0;

      const elErros = document.getElementById('metricErros');
      if (elErros) elErros.textContent = data.stats.erros || 0;
    }

    // Arquivo ativo
    const elActive = document.getElementById('lblEsteiraActiveFile');
    if (elActive) {
      elActive.textContent = data.active_file ? `Processando: ${data.active_file}` : (data.running ? 'Monitorando pasta por novos PDFs...' : 'Esteira desligada');
    }

    // Renderiza Logs do Console
    const consoleBox = document.getElementById('esteiraConsoleLogs');
    if (consoleBox && data.logs && data.logs.length > 0) {
      consoleBox.innerHTML = data.logs.map(log => {
        let colorClass = 'text-light';
        if (log.level === 'success') colorClass = 'text-success fw-bold';
        else if (log.level === 'warning') colorClass = 'text-warning';
        else if (log.level === 'error') colorClass = 'text-danger fw-bold';

        return `<div class="${colorClass}">[${log.time}] ${log.msg}</div>`;
      }).join('');
      consoleBox.scrollTop = consoleBox.scrollHeight;
    }

  } catch (err) {
    console.error('Erro ao consultar status da esteira:', err);
  }
}

async function abrirPastaSaida() {
  try {
    const response = await fetch('/api/batch/open-folder', { method: 'POST' });
    const data = await response.json();
    if (!data.success) {
      alert(`Não foi possível abrir a pasta: ${data.error}`);
    }
  } catch (err) {
    alert(`Erro ao abrir pasta: ${err.message}`);
  }
}

// Inicia polling se o modal for aberto
document.addEventListener('DOMContentLoaded', () => {
  const modalEl = document.getElementById('esteiraModal');
  if (modalEl) {
    modalEl.addEventListener('show.bs.modal', () => {
      pollEsteiraStatus();
      startEsteiraPolling();
    });
  }
});


