document.addEventListener('DOMContentLoaded', () => {
    // Conecta-se ao servidor WebSocket
    const socket = io();
    const listaElement = document.getElementById('lista-senhas');

const optionsMenu = document.querySelector('.options-menu');

    // Lógica para abrir/fechar o menu
    if (optionsMenu) {
        optionsMenu.addEventListener('click', (event) => {
            event.stopPropagation(); 
            optionsMenu.classList.toggle('menu-aberto');
        });
    }    window.addEventListener('click', () => {
        if (optionsMenu && optionsMenu.classList.contains('menu-aberto')) {
            optionsMenu.classList.remove('menu-aberto');
        }
    });

    // Função que busca e redesenha a fila inteira
    async function atualizarPainel() {
        try {
            const response = await fetch('/api/painel');
            if (!response.ok) throw new Error('Erro de rede');
            
            const fila = await response.json();
            
            if (!listaElement) return;

            if (fila.length === 0) {
                listaElement.innerHTML = '<li class="fila-vazia">Nenhuma senha na fila no momento.</li>';                return;
            }
            listaElement.innerHTML = fila.map((item,index) => {
                if (index === 0) {
                    return `<li>
                                <span><strong>${item.numero_formatado}</strong> - ${item.nome}</span>
                                <button class="atender-btn" data-id="${item.id}">
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" /></svg>
                                    Atender
                                </button>
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
        const atenderBtn = event.target.closest('.atender-btn');
        if (atenderBtn) {
            const senhaId = atenderBtn.getAttribute('data-id');
            fetch(`/atender/${senhaId}`, { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.status !== 'success') {
                        console.error('Falha ao marcar como atendido.');
                    }
                });
        }
    });

    const limparBtn = document.getElementById('limpar-btn');
    if (limparBtn) {
        limparBtn.addEventListener('click', (event) => {
            event.stopPropagation();
            if (confirm('Se você limpar a fila não será possível recuperá-la novemente.')) {
                fetch('/limpar-fila', { method: 'POST' });
            }
        });
    }
    
    atualizarPainel();
});