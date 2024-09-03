-- Tabela de Usuários
CREATE TABLE Usuarios (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    nome_usuario VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL, -- Armazenar senhas hash
    foto_perfil VARCHAR(255) DEFAULT 'url_padrao.jpg', -- URL da foto de perfil
    status ENUM('online', 'offline', 'ocupado', 'ausente') DEFAULT 'offline', -- Status do usuário
    ultimo_visto TIMESTAMP, -- Última vez que foi visto
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX (email),
    INDEX (nome_usuario)
);

-- Tabela de Conversas
CREATE TABLE Conversas (
    id_conversa INT PRIMARY KEY AUTO_INCREMENT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    esta_ativa BOOLEAN DEFAULT TRUE -- Indica se a conversa está ativa
);

-- Tabela de Participantes da Conversa
CREATE TABLE ParticipantesConversa (
    id_participante INT PRIMARY KEY AUTO_INCREMENT,
    id_conversa INT NOT NULL,
    id_usuario INT NOT NULL,
    adicionado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_conversa) REFERENCES Conversas(id_conversa),
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario),
    UNIQUE (id_conversa, id_usuario) -- Garante participantes únicos em cada conversa
);

-- Tabela de Mensagens
CREATE TABLE Mensagens (
    id_mensagem INT PRIMARY KEY AUTO_INCREMENT,
    id_conversa INT NOT NULL,
    id_remetente INT NOT NULL,
    id_destinatario INT NOT NULL,
    mensagem TEXT NOT NULL,
    tipo_mensagem ENUM('texto', 'imagem', 'video', 'arquivo') NOT NULL, -- Tipo da mensagem
    enviado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    lida BOOLEAN DEFAULT FALSE, -- Indica se a mensagem foi lida
    FOREIGN KEY (id_conversa) REFERENCES Conversas(id_conversa),
    FOREIGN KEY (id_remetente) REFERENCES Usuarios(id_usuario),
    FOREIGN KEY (id_destinatario) REFERENCES Usuarios(id_usuario),
    INDEX (id_conversa),
    INDEX (id_remetente)
);

-- Tabela de Grupos
CREATE TABLE Grupos (
    id_grupo INT PRIMARY KEY AUTO_INCREMENT,
    nome_grupo VARCHAR(100) NOT NULL UNIQUE, -- Nome do grupo
    descricao_grupo TEXT, -- Descrição opcional do grupo
    foto_grupo VARCHAR(255) DEFAULT 'url_padrao.jpg', -- URL da foto do grupo
    criado_por INT NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (criado_por) REFERENCES Usuarios(id_usuario)
);

-- Tabela de Membros do Grupo
CREATE TABLE MembrosGrupo (
    id_membro INT PRIMARY KEY AUTO_INCREMENT,
    id_grupo INT NOT NULL,
    id_usuario INT NOT NULL,
    adicionado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    e_admin BOOLEAN DEFAULT FALSE, -- Indica se o usuário é administrador
    papel ENUM('admin', 'membro', 'moderador') DEFAULT 'membro',
    FOREIGN KEY (id_grupo) REFERENCES Grupos(id_grupo),
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario),
    UNIQUE (id_grupo, id_usuario) -- Garante associações únicas de membros em grupos
);

-- Tabela de Mensagens do Grupo
CREATE TABLE MensagensGrupo (
    id_mensagem INT PRIMARY KEY AUTO_INCREMENT,
    id_grupo INT NOT NULL,
    id_remetente INT NOT NULL,
    mensagem TEXT NOT NULL,
    tipo_mensagem ENUM('texto', 'imagem', 'video', 'arquivo') NOT NULL, -- Tipo da mensagem
    enviado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    lida BOOLEAN DEFAULT FALSE, -- Indica se a mensagem foi lida pelos membros do grupo
    FOREIGN KEY (id_grupo) REFERENCES Grupos(id_grupo),
    FOREIGN KEY (id_remetente) REFERENCES Usuarios(id_usuario),
    INDEX (id_grupo),
    INDEX (id_remetente)
);

-- Tabela de Notificações
CREATE TABLE Notificacoes (
    id_notificacao INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    id_mensagem INT, -- Pode ser nulo para notificações não relacionadas a mensagens
    id_grupo INT, -- Pode ser nulo para notificações não relacionadas a grupos
    tipo_notificacao ENUM('mensagem', 'convite_grupo', 'atualizacao_grupo', 'mencao_grupo') NOT NULL,
    conteudo_notificacao TEXT, -- Conteúdo adicional da notificação
    lida BOOLEAN DEFAULT FALSE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario),
    FOREIGN KEY (id_mensagem) REFERENCES Mensagens(id_mensagem) ON DELETE SET NULL,
    FOREIGN KEY (id_grupo) REFERENCES Grupos(id_grupo) ON DELETE SET NULL,
    INDEX (id_usuario)
);

-- Tabela de Configurações de Usuário
CREATE TABLE ConfiguracoesUsuario (
    id_usuario INT PRIMARY KEY,
    tema ENUM('claro', 'escuro') DEFAULT 'claro',
    notificacoes_ativas BOOLEAN DEFAULT TRUE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)
);

-- Tabela de Usuários Bloqueados
CREATE TABLE UsuariosBloqueados (
    id_bloqueio INT PRIMARY KEY AUTO_INCREMENT,
    id_bloqueador INT NOT NULL,
    id_bloqueado INT NOT NULL,
    bloqueado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_bloqueador) REFERENCES Usuarios(id_usuario),
    FOREIGN KEY (id_bloqueado) REFERENCES Usuarios(id_usuario),
    UNIQUE (id_bloqueador, id_bloqueado) -- Garante bloqueios únicos entre usuários
);


OBS: Remover o campos id_destinatario na tabela mesagem, pois parace desnecessario/
