// frontend/js/auth.js

// Define a URL base da nossa API. É importante que o servidor backend esteja rodando neste endereço.
const API_URL = 'http://127.0.0.1:5000';

// Pega referências aos elementos do HTML com os quais vamos interagir.
const loginForm = document.getElementById('login-form');
const errorMessage = document.getElementById('error-message');

// Adiciona um "ouvinte" ao evento de 'submit' do formulário.
// A função dentro do 'addEventListener' será executada quando o usuário clicar no botão "Autenticar".
loginForm.addEventListener('submit', async (event) => {
    // 1. Impede o comportamento padrão do formulário, que é recarregar a página.
    event.preventDefault();

    // 2. Limpa mensagens de erro de tentativas anteriores.
    errorMessage.textContent = '';

    // 3. Coleta os dados digitados nos campos de input.
    const username = event.target.username.value;
    const password = event.target.password.value;

    try {
        // 4. Envia os dados para o endpoint de login da nossa API backend.
        // Usamos a função 'fetch' para fazer uma requisição de rede.
        const response = await fetch(`${API_URL}/api/login`, {
            method: 'POST', // O método HTTP para enviar dados de criação/login.
            headers: {
                // Informa ao servidor que estamos enviando dados no formato JSON.
                'Content-Type': 'application/json',
            },
            // Converte o objeto JavaScript com os dados para uma string JSON.
            body: JSON.stringify({ username, password }),
        });

        // 5. Converte a resposta do servidor (que está em JSON) para um objeto JavaScript.
        const data = await response.json();

        // 6. Verifica se a resposta da requisição foi bem-sucedida (status de 200 a 299).
        if (!response.ok) {
            // Se não foi, lança um erro com a mensagem que o backend enviou (ex: "Credenciais inválidas!").
            throw new Error(data.message || 'Erro na autenticação.');
        }

        // 7. Se o login foi bem-sucedido, armazena as informações recebidas no 'localStorage'.
        // O localStorage é um armazenamento no navegador que persiste mesmo se a aba for fechada.
        localStorage.setItem('authToken', data.token); // O token de segurança.
        localStorage.setItem('userRole', data.role); // O papel do usuário (ex: 'admin_seguranca').
        localStorage.setItem('username', data.username); // O nome do usuário para exibição.

        // 8. Redireciona o usuário para a página principal do sistema.
        window.location.href = 'dashboard.html';

    } catch (error) {
        // 9. Se qualquer erro ocorrer no bloco 'try' (seja de rede ou da API),
        // ele será capturado aqui e a mensagem de erro será exibida na página.
        errorMessage.textContent = error.message;
    }
});
