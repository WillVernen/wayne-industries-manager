// frontend/js/dashboard.js

// A API_URL é definida em main.js, mas a redefinimos aqui por clareza.
const DASHBOARD_API_URL = 'http://127.0.0.1:5000/api/dashboard';
const authToken = localStorage.getItem('authToken');

// Variáveis para armazenar as instâncias dos gráficos.
// Isso nos permite destruí-las antes de redesenhar para evitar bugs.
let tipoChart = null;
let statusChart = null;

// Função principal para carregar os dados e chamar as funções de renderização.
async function loadDashboardData() {
    try {
        const response = await fetch(DASHBOARD_API_URL, {
            headers: { 'x-access-token': authToken }
        });

        if (!response.ok) {
            throw new Error('Não foi possível carregar os dados do dashboard.');
        }

        const data = await response.json();
        renderRecursosPorTipoChart(data.recursos_por_tipo);
        renderRecursosPorStatusChart(data.recursos_por_status);

    } catch (error) {
        console.error('Erro no dashboard:', error);
    }
}

// Função para renderizar o gráfico de "Recursos por Tipo" (gráfico de rosca).
function renderRecursosPorTipoChart(data) {
    const ctx = document.getElementById('recursosPorTipoChart').getContext('2d');
    const labels = Object.keys(data);
    const values = Object.values(data);

    // Se o gráfico já existir, destrua-o antes de criar um novo.
    if (tipoChart) {
        tipoChart.destroy();
    }

    tipoChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels.length > 0 ? labels : ['Nenhum dado'],
            datasets: [{
                label: 'Recursos por Tipo',
                data: values.length > 0 ? values : [1],
                backgroundColor: [
                    'rgba(54, 162, 235, 0.8)',
                    'rgba(255, 206, 86, 0.8)',
                    'rgba(75, 192, 192, 0.8)',
                ],
                borderColor: 'rgba(255, 255, 255, 0.1)',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'top', labels: { color: '#e0e0e0' } },
                title: { display: true, text: 'Distribuição de Recursos por Tipo', color: '#e0e0e0', font: { size: 16 } }
            }
        }
    });
}

// Função para renderizar o gráfico de "Recursos por Status" (gráfico de barras).
function renderRecursosPorStatusChart(data) {
    const ctx = document.getElementById('recursosPorStatusChart').getContext('2d');
    const labels = Object.keys(data);
    const values = Object.values(data);

    if (statusChart) {
        statusChart.destroy();
    }

    statusChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels.length > 0 ? labels : ['Nenhum dado'],
            datasets: [{
                label: 'Status dos Recursos',
                data: values.length > 0 ? values : [0],
                backgroundColor: [
                    'rgba(75, 192, 192, 0.8)',
                    'rgba(255, 159, 64, 0.8)',
                    'rgba(255, 99, 132, 0.8)',
                ],
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                title: { display: true, text: 'Status Atual dos Recursos', color: '#e0e0e0', font: { size: 16 } }
            },
            scales: {
                x: { ticks: { color: '#a0a0a0' }, grid: { color: 'rgba(255, 255, 255, 0.1)' } },
                y: { ticks: { color: '#a0a0a0' }, grid: { color: 'rgba(255, 255, 255, 0.1)' } }
            }
        }
    });
}

// Carrega os dados do dashboard assim que o script é lido.
loadDashboardData();
