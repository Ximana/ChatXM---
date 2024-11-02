V. 1 - Nas lista de usuarios e grupos deve aparecer o ponteiro como uma mao indicando que e um link
V. 2 - Ao clizar na foto de perlfil do contacto ao conversar levar a pagina de perfil do 
    mesmo, ou, seja, Como passar variavel ajax numa rota flask
    V. 2.1 - Al clicar num usuario bloqueado mostrar a pagina de perfil do mesmo
V 3 - Clicar e visualizar as mensagens  e detalhes do grupo clicado
    3.1 - Melhorar o estado/status (online, offline)


4 - Adicionar a funcionalidade enviar mensagem(individual e em grupo)
5 - Adicionar a funcionalidade pesquisa de usuarios no sidebar
6 - Adicionar a funcionalidade de alterar a foto de perfil

7 - Adicionar a funcionalidade para alterar o tema do chat(claro ou escuro)

_________________________________________________________________

Melhorar o design do chat


________________________________________________________________________


Ficou pereito mas quero que as novas mensagens na lista de conversa aparecam em negrito 
$('#all-messages').append(`
                    <div class="chat-user" data-id-usuario="${item.id_usuario}">
                        <img src="{{ url_for('static', filename='img/usuarios/') }}${item.foto_perfil}" class="rounded-circle" alt="User Image">
                        <div class="chat-info">
                            <h6>${item.nome_usuario} <small><i class="fas fa-circle ${statusClass}"></i> ${item.status}</small></h6>
                            <small class="text-dark">${item.mensagem}</small><!-- novas mensagens -->
                        </div>
                    </div>
                `);

E adicione um badge bootstrap "<span class="badge badge-secondary">numero de mensagens</span>" sempre que haver nova mensagem.