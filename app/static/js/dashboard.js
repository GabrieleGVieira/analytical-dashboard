// Variáveis globais para os gráficos
let chartVendasTempo, chartVendasCategoria, chartVendasRegiao, chartTopProdutos, chartDesempenhoVendedores;

// Função principal para carregar dashboard
function carregarDashboard() {
    const dataInicio = document.getElementById('dataInicio').value;
    const dataFim = document.getElementById('dataFim').value;
    
    carregarKPIs(dataInicio, dataFim);
    carregarGraficoVendasTempo(dataInicio, dataFim);
    carregarGraficoVendasCategoria(dataInicio, dataFim);
    carregarGraficoVendasRegiao(dataInicio, dataFim);
    carregarGraficoTopProdutos(dataInicio, dataFim);
    carregarMargemLucro(dataInicio, dataFim)
    carregarGraficoDesempenhoVendedores(dataInicio, dataFim)
    carregarTabelaVendedores(dataInicio, dataFim)
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
    let url = '/api/analytics/sales-by-category';
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

function carregarGraficoDesempenhoVendedores(dataInicio, dataFim) {
    let url = '/api/analytics/seller-ranking';
    const params = new URLSearchParams();
    if (dataInicio) params.append('data_inicio', dataInicio);
    if (dataFim) params.append('data_fim', dataFim);
    if (params.toString()) url += '&' + params.toString();

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const ranking = data.ranking || [];

            // Ordena por índice de performance e pega os top 10
            const topVendedores = ranking
                .sort((a, b) => b.indice_performance - a.indice_performance)
                .slice(0, 10);

            const ctx = document.getElementById('chartDesempenhoVendedores').getContext('2d');

            if (chartDesempenhoVendedores) chartDesempenhoVendedores.destroy();

            chartDesempenhoVendedores = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: topVendedores.map(v => v.vendedor),
                    datasets: [{
                        label: 'Índice de Performance (%)',
                        data: topVendedores.map(v => v.indice_performance),
                        borderRadius: 12,
                        backgroundColor: topVendedores.map(v =>
                            v.indice_performance >= 80 ? 'rgba(34,197,94,0.7)' : // verde
                            v.indice_performance >= 60 ? 'rgba(250,204,21,0.7)' : // amarelo
                            'rgba(239,68,68,0.7)' // vermelho
                        ),
                    }]
                },
                options: {
                    indexAxis: 'y', // horizontal (troque para 'x' se quiser vertical)
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Top 10 Vendedores – Índice de Performance'
                        },
                        legend: { display: false },
                        tooltip: {
                            callbacks: {
                                label: ctx => `${ctx.parsed.x.toFixed(2)}%`
                            }
                        }
                    },
                    scales: {
                        x: {
                            beginAtZero: true,
                            max: 100,
                            title: { display: true, text: 'Índice de Performance (%)' },
                            ticks: { callback: v => v + '%' }
                        },
                        y: {
                            ticks: { color: '#374151' }
                        }
                    }
                }
            });
        })
        .catch(err => console.error('Erro ao carregar gráfico de desempenho:', err));
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

function carregarTabelaVendedores(dataInicio, dataFim) {
    let url = '/api/analytics/seller-ranking';
    const params = new URLSearchParams();
    if (dataInicio) params.append('data_inicio', dataInicio);
    if (dataFim) params.append('data_fim', dataFim);
    if (params.toString()) url += '?' + params.toString();

    fetch(url)
        .then(res => res.json())
        .then(data => {
            const ranking = data.ranking || [];

            // Destroi tabela existente antes de recriar (para recarregar filtros)
            if ($.fn.DataTable.isDataTable('#tabelaVendedores')) {
                $('#tabelaVendedores').DataTable().destroy();
            }

            // Preenche as linhas
            const tbody = document.querySelector('#tabelaVendedores tbody');
            tbody.innerHTML = ranking.map(v => `
                <tr>
                    <td>${v.vendedor}</td>
                    <td>R$ ${v.vendas_totais.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</td>
                    <td>R$ ${v.lucro_total.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</td>
                    <td>${v.margem_lucro.toFixed(2)}%</td>
                    <td>${v.quantidade_vendida}</td>
                    <td>R$ ${v.meta_valor.toLocaleString('pt-BR')}</td>
                    <td>${v.meta_batida.toFixed(2)}%</td>
                    <td>
                        <span class="badge ${v.indice_performance >= 80 ? 'bg-success' : v.indice_performance >= 60 ? 'bg-warning text-dark' : 'bg-danger'}">
                            ${v.indice_performance.toFixed(2)}%
                        </span>
                    </td>
                </tr>
            `).join('');

            // Inicializa DataTable com recursos interativos
            $('#tabelaVendedores').DataTable({
                pageLength: 10,
                order: [[7, 'desc']], // ordena inicialmente por índice de performance
                language: {
                    url: 'https://cdn.datatables.net/plug-ins/1.13.6/i18n/pt-BR.json'
                }
            });
        })
        .catch(err => console.error('Erro ao carregar tabela de vendedores:', err));
}
