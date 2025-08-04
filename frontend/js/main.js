// frontend/js/main.js

const API_URL = 'http://127.0.0.1:5000';

// --- SELEÇÃO DE ELEMENTOS DO DOM ---
// Pegamos referências a todos os elementos HTML que vamos manipular.
const usernameDisplay = document.getElementById('username-display');
const logoutBtn = document.getElementById('logout-btn');
const recursosTableBody = document.querySelector('#recursos-table tbody');
const addRecursoBtn = document.getElementById('add-recurso-btn');

// Elementos do Modal
const modal = document.getElementById('recurso-modal');
const modalTitle = document.getElementById('modal-title');
const recursoForm = document.getElementById('recurso-form');
const closeBtn = document.querySelector('.close-btn');
const recursoIdInput = document.getElementById('recurso-id');

// Pega informações do usuário salvas no localStorage durante o login.
const userRole = localStorage.getItem('userRole');
const token = localStorage.getItem('authToken');

// --- FUNÇÃO DE INICIALIZAÇÃO ---
// Esta função é executada assim que o HTML da página é totalmente carregado.
document.addEventListener('DOMContentLoaded', () => {
    // 1. Proteção de Rota: Se não houver token, o usuário não está logado.
    if (!token) {
        // Redireciona de volta para a página de login.
        window.location.href = 'index.html';
        return; // Para a execução do script.
    }

    // 2. Personalização da UI: Exibe o nome do usuário no cabeçalho.
    const username = localStorage.getItem('username');
    if (username) {
        usernameDisplay.textContent = username;
    }

    // 3. Configuração de Permissões: Mostra/esconde botões com base no papel do usuário.
    setupPermissions();

    // 4. Carregamento de Dados: Busca os recursos da API e preenche a tabela.
    loadRecursos();
});

// --- CONTROLE DE PERMISSÕES ---
function setupPermissions() {
    // Apenas 'gerente' e 'admin_seguranca' podem ver o botão de adicionar.
    if (userRole === 'gerente' || userRole === 'admin_seguranca') {
        addRecursoBtn.style.display = 'inline-block'; // Mostra o botão
    }
}

// --- LÓGICA DE DADOS (CRUD) ---

// READ: Busca e exibe todos os recursos.
async function loadRecursos() {
    try {
        const response = await fetch(`${API_URL}/api/recursos`, {
            headers: { 'x-access-token': token }
        });

        // Se o token for inválido ou expirar, o backend retornará 401.
        if (response.status === 401) {
            logout(); // Desloga o usuário.
            return;
        }

        const data = await response.json();
        recursosTableBody.innerHTML = ''; // Limpa a tabela antes de adicionar os novos dados.

        if (data.recursos.length === 0) {
            recursosTableBody.innerHTML = `<tr><td colspan="5" style="text-align:center;">Nenhum recurso cadastrado.</td></tr>`;
        } else {
            data.recursos.forEach(recurso => {
                const row = document.createElement('tr');
                // Preenche a linha com os dados do recurso.
                row.innerHTML = `
                    <td>${recurso.nome}</td>
                    <td>${recurso.tipo}</td>
                    <td>${recurso.quantidade}</td>
                    <td>${recurso.status}</td>
                    <td class="actions-column">
                        ${(userRole === 'gerente' || userRole === 'admin_seguranca') ? `<button onclick="handleEdit(${recurso.id})">Editar</button>` : ''}
                        ${(userRole === 'admin_seguranca') ? `<button onclick="handleDelete(${recurso.id})">Excluir</button>` : ''}
                    </td>
                `;
                recursosTableBody.appendChild(row);
            });
        }
    } catch (error) {
        console.error('Erro ao carregar recursos:', error);
        recursosTableBody.innerHTML = `<tr><td colspan="5" style="text-align:center;">Erro ao carregar dados.</td></tr>`;
    }
}

// CREATE / UPDATE: Lida com o envio do formulário do modal.
recursoForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const id = recursoIdInput.value; // Pega o ID (se houver, é uma edição).
    const recursoData = {
        nome: document.getElementById('nome').value,
        tipo: document.getElementById('tipo').value,
        quantidade: document.getElementById('quantidade').value,
        status: document.getElementById('status').value,
    };

    // Define o método e a URL com base na existência de um ID.
    const method = id ? 'PUT' : 'POST';
    const url = id ? `${API_URL}/api/recursos/${id}` : `${API_URL}/api/recursos`;

    try {
        const response = await fetch(url, {
            method,
            headers: {
                'Content-Type': 'application/json',
                'x-access-token': token
            },
            body: JSON.stringify(recursoData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message);
        }

        closeModal(); // Fecha o modal em caso de sucesso.
        loadRecursos(); // Recarrega a tabela.
        // Se a função existir no outro script, a chama para atualizar os gráficos.
        if (typeof loadDashboardData === 'function') {
            loadDashboardData();
        }
    } catch (error) {
        alert(`Erro ao salvar recurso: ${error.message}`);
    }
});

// DELETE: Lida com o clique no botão de excluir.
async function handleDelete(id) {
    // Pede confirmação antes de uma ação destrutiva.
    if (confirm('Tem certeza que deseja excluir este recurso?')) {
        try {
            const response = await fetch(`${API_URL}/api/recursos/${id}`, {
                method: 'DELETE',
                headers: { 'x-access-token': token }
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message);
            }
            loadRecursos(); // Recarrega a tabela.
            if (typeof loadDashboardData === 'function') {
                loadDashboardData();
            }
        } catch (error) {
            alert(`Erro ao excluir recurso: ${error.message}`);
        }
    }
}

// --- CONTROLE DO MODAL ---
function openModal(mode, recurso = {}) {
    recursoForm.reset();
    recursoIdInput.value = '';

    if (mode === 'edit') {
        modalTitle.textContent = 'Editar Recurso';
        recursoIdInput.value = recurso.id;
        document.getElementById('nome').value = recurso.nome;
        document.getElementById('tipo').value = recurso.tipo;
        document.getElementById('quantidade').value = recurso.quantidade;
        document.getElementById('status').value = recurso.status;
    } else {
        modalTitle.textContent = 'Adicionar Novo Recurso';
    }
    modal.classList.add('show');
}

// Função para ser chamada pelo botão de Editar.
async function handleEdit(id) {
    // Para editar, primeiro buscamos os dados atuais do recurso.
    try {
        const response = await fetch(`${API_URL}/api/recursos`, { headers: { 'x-access-token': token } });
        const data = await response.json();
        const recurso = data.recursos.find(r => r.id === id);
        if (recurso) {
            openModal('edit', recurso);
        }
    } catch (error) {
        alert('Erro ao buscar dados do recurso para edição.');
    }
}


function closeModal() {
    modal.classList.remove('show');
}

// Eventos para abrir e fechar o modal.
addRecursoBtn.addEventListener('click', () => openModal('add'));
closeBtn.addEventListener('click', closeModal);
// Fecha o modal se o usuário clicar fora da área de conteúdo.
window.addEventListener('click', (event) => {
    if (event.target === modal) {
        closeModal();
    }
});

// --- LOGOUT ---
function logout() {
    localStorage.clear(); // Limpa todo o armazenamento local.
    window.location.href = 'index.html';
}
logoutBtn.addEventListener('click', logout);
