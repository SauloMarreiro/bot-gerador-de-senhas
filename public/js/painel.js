document.addEventListener('DOMContentLoaded', () => {
    // --- Variáveis Principais ---
    const socket = io();
    const listaElement = document.getElementById('lista-senhas');
    const optionsMenu = document.querySelector('.options-menu');

    // --- Lógica do Menu Dropdown ---
    if (optionsMenu) {
        optionsMenu.addEventListener('click', (event) => {
            event.stopPropagation();
            optionsMenu.classList.toggle('menu-aberto');
        });
    }
    window.addEventListener('click', () => {
        if (optionsMenu && optionsMenu.classList.contains('menu-aberto')) {
            optionsMenu.classList.remove('menu-aberto');
        }
    });

    // --- Funções ---
    async function atualizarPainel() {
        try {
            const response = await fetch('/api/painel');
            if (!response.ok) throw new Error('Erro de rede');
            const fila = await response.json();
            if (!listaElement) return;

            if (fila.length === 0) {
                listaElement.innerHTML = '<li class="fila-vazia">Nenhuma senha na fila no momento.</li>';
                return;
            }
            
            listaElement.innerHTML = fila.map((item, index) => {
                const isAtendido = item.status === 'atendido';
                const classeLi = isAtendido ? 'class="atendido"' : '';

                const botaoHtml = (index === 0 && !isAtendido) 
                    ? `<button class="atender-btn" data-id="${item.id}">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                        </svg>
                        Atender
                       </button>`
                    : '';

                return `<li ${classeLi}>
                            <span><strong>${item.numero_formatado}</strong> - ${item.nome}</span>
                            ${botaoHtml}
                        </li>`;
            }).join('');
        } catch (error) {
            console.error("Falha ao atualizar o painel:", error);
            if (listaElement) listaElement.innerHTML = '<li>Erro ao carregar a fila.</li>';
        }
    }

    // --- Ouvintes de Eventos (Listeners) ---
    socket.on('fila_atualizada', (data) => {
        console.log('Aviso recebido:', data ? data.message : 'Atualização');
        atualizarPainel();
    });

    if (listaElement) {
        listaElement.addEventListener('click', (event) => {
            const atenderBtn = event.target.closest('.atender-btn');
            if (atenderBtn) {
                const senhaId = atenderBtn.getAttribute('data-id');
                atenderBtn.disabled = true;
                fetch(`/atender/${senhaId}`, { method: 'POST' }).then(response => {
                    if (!response.ok) atenderBtn.disabled = false;
                });
            }
        });
    }

    const limparBtn = document.getElementById('limpar-btn');
    if (limparBtn) {
        limparBtn.addEventListener('click', (event) => {
            event.stopPropagation();
            if (confirm('Tem certeza que deseja apagar TODAS as senhas da fila?')) {
                fetch('/limpar-fila', { method: 'POST' });
            }
        });
    }

    // --- Carga Inicial ---
    atualizarPainel();
});