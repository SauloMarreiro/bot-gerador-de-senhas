document.addEventListener('DOMContentLoaded', () => {
    // Conecta-se ao servidor WebSocket
    const socket = io();
    const listaElement = document.getElementById('lista-senhas');

    // Função que busca e redesenha a fila inteira
    async function atualizarPainel() {
        try {
            const response = await fetch('/api/painel');
            if (!response.ok) throw new Error('Erro de rede');
            
            const fila = await response.json();
            
            if (!listaElement) return;

            if (fila.length === 0) {
                listaElement.innerHTML = '<li>Nenhuma senha na fila no momento.</li>';
                return;
            }
            
            // Agora criamos um item de lista com um botão
            listaElement.innerHTML = fila.map((item,index) => {
                if (index === 0) {
                    return `<li>
                                <span><strong>${item.numero_formatado}</strong> - ${item.nome}</span>
                                <button class="atender-btn" data-id="${item.id}">Atender</button>
                            </li>`;
                }
                else{
                    return `<li>
                    <span><strong>${item.numero_formatado}</strong> - ${item.nome}</span>
                            </li>`;

                    
                }
            }).join('');

        } catch (error) {
            console.error("Falha ao atualizar o painel:", error);
            if(listaElement) {
                listaElement.innerHTML = '<li>Erro ao carregar a fila.</li>';
            }
        }
    }

    // Fica "ouvindo" o aviso do servidor
    socket.on('fila_atualizada', (data) => {
        console.log('Aviso recebido do servidor:', data.message);
        // Quando o aviso chega, simplesmente manda atualizar o painel
        atualizarPainel();
    });

    // Lida com cliques nos botões "Atender"
    listaElement.addEventListener('click', (event) => {
        if (event.target && event.target.classList.contains('atender-btn')) {
            const senhaId = event.target.getAttribute('data-id');
            
            // Envia o comando POST para o servidor
            fetch(`/atender/${senhaId}`, { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.status !== 'success') {
                        console.error('Falha ao marcar como atendido.');
                    }
                });
        }
    });

    // Dentro do painel.js
    const limparBtn = document.getElementById('limpar-btn');
    if (limparBtn) {
        limparBtn.addEventListener('click', () => {
            if (confirm('Tem certeza que...')) {
                fetch('/limpar-fila', { method: 'POST' });
            }
        });
    }
    
    // Carrega o painel pela primeira vez quando a página abre
    atualizarPainel();
});