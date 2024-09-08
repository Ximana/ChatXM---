V. 1 - Nas lista de usuarios e grupos deve aparecer o ponteiro como uma mao indicando que e um link
V. 2 - Ao clizar na foto de perlfil do contacto ao conversar levar a pagina de perfil do 
    mesmo, ou, seja, Como passar variavel ajax numa rota flask
    V. 2.1 - Al clicar num usuario bloqueado mostrar a pagina de perfil do mesmo
3 - Clicar e visualizar as mensagens  e detalhes do grupo clicado
    3.1 - Melhorar o estado/status (online, offline)


4 - Adicionar a funcionalidade enviar mensagem(individual e em grupo)
5 - Adicionar a funcionalidade pesquisa de usuarios no sidebar
6 - Adicionar a funcionalidade de alterar a foto de perfil

7 - Adicionar a funcionalidade para alterar o tema do chat(claro ou escuro)

_________________________________________________________________

Melhorar o design do chat


________________________________________________________________________

Atualize o meu codigo para que ao clicar num grupo da lista de grupos mostra as mensagens deste grupo(a conversa completa)
em que o usuario logado faz parte,  Siga a logica usada para carregar as conversas e mensagens das individuais.

 // Função para listar todos os usuários
function listarUsuarios() {
    $.ajax({
        url: "{{ url_for('chat.listar_usuarios') }}",
        method: 'GET',
        success: function (response) {
            $('#contacts').empty();
            response.forEach(function (item) {
                let statusClass = item.status === 'online' ? 'text-success' : 'text-danger';
                $('#contacts').append(`
                    <div class="chat-user" data-id-usuario="${item.id_usuario}">
                        <img src="{{ url_for('static', filename='img/usuarios/') }}${item.foto_perfil}" class="rounded-circle" alt="User Image">
                        <div class="chat-info">
                            <h6>${item.nome_usuario} <small><i class="fas fa-circle ${statusClass}"></i> ${item.status}</small></h6>
                        </div>
                    </div>
                `);
            });
            // Adicionar evento de clique após inserir os itens
            adicionarEventoClique();
        }
    });
}

// Função para adicionar evento de clique
function adicionarEventoClique() {
    $('.chat-user').off('click').on('click', function() {
        let id_usuario = $(this).data('id-usuario');
        carregarConversa(id_usuario);
    });
}

Atualize a funcao `listarGrupos()` para ter a logica do `listarUsuarios()`.


// Adicionar a data de criação da conversa apenas uma vez, no início
            if (response.mensagens.length > 0) {
                var conversaData = new Date(response.mensagens[0].enviado_em);
                $('.chat-body').append(`<p class="small text-muted">Conversa iniciada em ${conversaData.toLocaleDateString('pt-BR', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}</p>`);
            }

// Verificar se a data mudou, mas não adicionar para a primeira mensagem
                var msgDate = new Date(msg.enviado_em).toLocaleDateString();
                if (msgDate !== currentDate && currentDate !== '') {
                    $('.chat-body').append(`<p class="small text-muted">${new Date(msg.enviado_em).toLocaleDateString('pt-BR', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}</p>`);
                }
                currentDate = msgDate;