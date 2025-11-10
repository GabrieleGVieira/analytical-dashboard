// Variáveis globais para os gráficos
let chartVendasTempo, chartVendasCategoria, chartVendasRegiao, chartTopProdutos, chartVendasMultiplosPeriodos;

// Função principal para carregar dashboard
function carregarDashboard() {
    const dataInicio = document.getElementById('dataInicio').value;
    const dataFim = document.getElementById('dataFim').value;
    
    carregarKPIs(dataInicio, dataFim);
    carregarGraficoVendasTempo(dataInicio, dataFim);
    carregarGraficoVendasCategoria(dataInicio, dataFim);
    carregarGraficoVendasRegiao(dataInicio, dataFim);
    carregarGraficoTopProdutos(dataInicio, dataFim);
    carregarGraficoVendasMultiplosPeriodos(dataInicio, dataFim);
    carregarMargemLucro(dataInicio, dataFim)
}

// Carrega KPIs
function carregarKPIs(dataInicio, dataFim) {
    let url = '/data/kpis';
    const params = new URLSearchParams();
    if (dataInicio) params.append('data_inicio', dataInicio);
    if (dataFim) params.append('data_fim', dataFim);
    if (params.toString()) url += '?' + params.toString();
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            document.getElementById('kpiReceitaTotal').textContent = 
                formatarMoeda(data.receita_total);
            document.getElementById('kpiNumVendas').textContent = 
                formatarNumero(data.num_vendas);
            document.getElementById('kpiTicketMedio').textContent = 
                formatarMoeda(data.ticket_medio);
        })
        .catch(error => console.error('Erro ao carregar KPIs:', error));
}

// Carrega gráfico de vendas ao longo do tempo
function carregarGraficoVendasTempo(dataInicio, dataFim) {
    let url = '/api/analytics/long-term-sales';
    const params = new URLSearchParams();
    if (dataInicio) params.append('data_inicio', dataInicio);
    if (dataFim) params.append('data_fim', dataFim);
    if (params.toString()) url += '?' + params.toString();
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('chartVendasTempo').getContext('2d');
            
            if (chartVendasTempo) {
                chartVendasTempo.destroy();
            }
            
            chartVendasTempo = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Valor (R$)',
                        data: data.valores,
                        borderColor: 'rgb(13, 110, 253)',
                        backgroundColor: 'rgba(13, 110, 253, 0.1)',
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        legend: {
                            display: true,
                            position: 'top'
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                callback: function(value) {
                                    return 'R$ ' + value.toLocaleString('pt-BR');
                                }
                            }
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Erro ao carregar gráfico:', error));
}

// Carrega gráfico de vendas por categoria
function carregarGraficoVendasCategoria(dataInicio, dataFim) {
    let url = '/data/vendas-categoria';
    const params = new URLSearchParams();
    if (dataInicio) params.append('data_inicio', dataInicio);
    if (dataFim) params.append('data_fim', dataFim);
    if (params.toString()) url += '?' + params.toString();
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('chartVendasCategoria').getContext('2d');
            
            if (chartVendasCategoria) {
                chartVendasCategoria.destroy();
            }
            
            chartVendasCategoria = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Vendas (R$)',
                        data: data.valores,
                        backgroundColor: [
                            'rgba(13, 110, 253, 0.8)',
                            'rgba(25, 135, 84, 0.8)',
                            'rgba(255, 193, 7, 0.8)',
                            'rgba(220, 53, 69, 0.8)',
                            'rgba(13, 202, 240, 0.8)'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                callback: function(value) {
                                    return 'R$ ' + value.toLocaleString('pt-BR');
                                }
                            }
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Erro ao carregar gráfico:', error));
}

// Carrega gráfico de vendas por região
function carregarGraficoVendasRegiao(dataInicio, dataFim) {
    let url = '/data/vendas-regiao';
    const params = new URLSearchParams();
    if (dataInicio) params.append('data_inicio', dataInicio);
    if (dataFim) params.append('data_fim', dataFim);
    if (params.toString()) url += '?' + params.toString();
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('chartVendasRegiao').getContext('2d');
            
            if (chartVendasRegiao) {
                chartVendasRegiao.destroy();
            }
            
            chartVendasRegiao = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: data.labels,
                    datasets: [{
                        data: data.valores,
                        backgroundColor: [
                            'rgba(13, 110, 253, 0.8)',
                            'rgba(25, 135, 84, 0.8)',
                            'rgba(255, 193, 7, 0.8)',
                            'rgba(220, 53, 69, 0.8)',
                            'rgba(13, 202, 240, 0.8)'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const label = context.label || '';
                                    const value = formatarMoeda(context.parsed);
                                    const percentual = data.percentuais[context.dataIndex];
                                    return `${label}: ${value} (${percentual}%)`;
                                }
                            }
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Erro ao carregar gráfico:', error));
}

// Carrega gráfico de top produtos
function carregarGraficoTopProdutos(dataInicio, dataFim) {
    let url = '/data/top-produtos?limite=10';
    const params = new URLSearchParams();
    if (dataInicio) params.append('data_inicio', dataInicio);
    if (dataFim) params.append('data_fim', dataFim);
    params.append('limite', '10');
    url += '&' + params.toString();
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('chartTopProdutos').getContext('2d');
            
            if (chartTopProdutos) {
                chartTopProdutos.destroy();
            }
            
            chartTopProdutos = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Vendas (R$)',
                        data: data.valores,
                        backgroundColor: 'rgba(25, 135, 84, 0.8)'
                    }]
                },
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        x: {
                            beginAtZero: true,
                            ticks: {
                                callback: function(value) {
                                    return 'R$ ' + value.toLocaleString('pt-BR');
                                }
                            }
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Erro ao carregar gráfico:', error));
}

// Event listeners
document.getElementById('aplicarFiltros').addEventListener('click', function() {
    carregarDashboard();
});

document.getElementById('limparFiltros').addEventListener('click', function() {
    document.getElementById('dataInicio').value = '';
    document.getElementById('dataFim').value = '';
    carregarDashboard();
});

// Upload de arquivo
document.getElementById('uploadButton').addEventListener('click', function() {
    const form = document.getElementById('uploadForm');
    const formData = new FormData(form);
    
    fetch('/api/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Erro: ' + data.error);
        } else {
            alert('Arquivo processado com sucesso! ' + data.registros + ' registros importados.');
            bootstrap.Modal.getInstance(document.getElementById('uploadModal')).hide();
            form.reset();
            carregarDashboard();
        }
    })
    .catch(error => {
        alert('Erro ao fazer upload: ' + error);
    });
});

// Funções auxiliares
function formatarMoeda(valor) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(valor);
}

function formatarNumero(valor) {
    return new Intl.NumberFormat('pt-BR').format(valor);
}

function formatarPercentual(valor) {
  if (valor === null || valor === undefined || isNaN(valor)) return '-';
  const percentual = valor > 1 ? valor / 100 : valor;

  return new Intl.NumberFormat('pt-BR', {
    style: 'percent',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(percentual);
}


function carregarGraficoVendasMultiplosPeriodos(dataInicio, dataFim) {
    let url = '/api/analytics/multiple-period-sales';
    const params = new URLSearchParams();
    if (dataInicio) params.append('data_inicio', dataInicio);
    if (dataFim) params.append('data_fim', dataFim);
    if (params.toString()) url += '?' + params.toString();

    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            const ctx = document.getElementById('chartVendasMultiplosPeriodos').getContext('2d');

            if (chartVendasMultiplosPeriodos) {
                chartVendasMultiplosPeriodos.destroy();
            }

            chartVendasMultiplosPeriodos = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [
                        {
                            label: 'Quantidades',
                            data: data.quantidades,
                            borderColor: 'rgba(75, 192, 192, 1)',
                            backgroundColor: 'rgba(75, 192, 192, 0.2)',
                            borderWidth: 2,
                            fill: false,
                            tension: 0.4
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        legend: {
                            display: true,
                            position: 'top'
                        },
                        title: {
                            display: true,
                            text: 'Comparação de Vendas - Período Atual x Anterior'
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                callback: function(value) {
                                    return value;
                                }
                            }
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Erro ao carregar gráfico múltiplos períodos:', error));
}

function carregarMargemLucro(dataInicio, dataFim) {
    let url = '/api/analytics/profit-margin';
    const params = new URLSearchParams();
    if (dataInicio) params.append('data_inicio', dataInicio);
    if (dataFim) params.append('data_fim', dataFim);
    if (params.toString()) url += '?' + params.toString();

    fetch(url)
        .then(response => response.json())
        .then(data => {
            document.getElementById('kpiMargemDeLucro').textContent =
                formatarPercentual(data.margem_percentual);
        })
        .catch(error => console.error('Erro ao carregar KPIs:', error));
}


