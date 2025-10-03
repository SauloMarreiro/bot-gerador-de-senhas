async function atualizarPainel() {
    try {
        const response = await fetch('/api/painel');
        if (!response.ok) {
            throw new Error('Erro de rede ao buscar a fila.');
        }
        
        const fila = await response.json();
        const listaElement = document.getElementById('lista-senhas');
        
        if (!listaElement) return;

        if (fila.length === 0) {
            listaElement.innerHTML = '<li>Nenhuma senha na fila no momento.</li>';
            return;
        }
        
        listaElement.innerHTML = fila.map((item) => {
            const numero = item.numero_formatado.replace(/</g, "&lt;").replace(/>/g, "&gt;");
            const nome = item.nome.replace(/</g, "&lt;").replace(/>/g, "&gt;");
            const tipo = item.tipo.replace(/</g, "&lt;").replace(/>/g, "&gt;");
            
            return `<li><strong>${numero}</strong> - ${nome} (${tipo})</li>`;
        }).join('');

    } catch (error) {
        console.error("Falha ao atualizar o painel:", error);
        const listaElement = document.getElementById('lista-senhas');
        if(listaElement) {
            listaElement.innerHTML = '<li>Erro ao carregar a fila. Tente novamente.</li>';
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    atualizarPainel(); // Carrega imediatamente
    setInterval(atualizarPainel, 3000); // E depois atualiza a cada 3 segundos
});