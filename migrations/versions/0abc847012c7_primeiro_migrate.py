"""Primeiro migrate

Revision ID: 0abc847012c7
Revises: 
Create Date: 2024-09-03 01:57:51.376585

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0abc847012c7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Conversas',
    sa.Column('id_conversa', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('criado_em', sa.TIMESTAMP(), nullable=True),
    sa.Column('atualizado_em', sa.TIMESTAMP(), nullable=True),
    sa.Column('esta_ativa', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id_conversa')
    )
    op.create_table('Usuarios',
    sa.Column('id_usuario', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nome_usuario', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('numero_telefone', sa.String(length=30), nullable=True),
    sa.Column('senha', sa.String(length=255), nullable=False),
    sa.Column('foto_perfil', sa.String(length=255), nullable=True),
    sa.Column('status', sa.Enum('online', 'offline'), nullable=True),
    sa.Column('ultimo_visto', sa.TIMESTAMP(), nullable=True),
    sa.Column('criado_em', sa.TIMESTAMP(), nullable=True),
    sa.Column('atualizado_em', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('id_usuario'),
    sa.UniqueConstraint('numero_telefone')
    )
    with op.batch_alter_table('Usuarios', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_Usuarios_email'), ['email'], unique=True)

    op.create_table('ConfiguracoesUsuario',
    sa.Column('id_configuracao_usuario', sa.Integer(), nullable=False),
    sa.Column('tema', sa.Enum('claro', 'escuro'), nullable=True),
    sa.Column('notificacoes_ativas', sa.Boolean(), nullable=True),
    sa.Column('criado_em', sa.TIMESTAMP(), nullable=True),
    sa.Column('atualizado_em', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['id_configuracao_usuario'], ['Usuarios.id_usuario'], ),
    sa.PrimaryKeyConstraint('id_configuracao_usuario')
    )
    op.create_table('Grupos',
    sa.Column('id_grupo', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nome_grupo', sa.String(length=100), nullable=False),
    sa.Column('descricao_grupo', sa.Text(), nullable=True),
    sa.Column('foto_grupo', sa.String(length=255), nullable=True),
    sa.Column('criado_por', sa.Integer(), nullable=False),
    sa.Column('criado_em', sa.TIMESTAMP(), nullable=True),
    sa.Column('atualizado_em', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['criado_por'], ['Usuarios.id_usuario'], ),
    sa.PrimaryKeyConstraint('id_grupo')
    )
    op.create_table('Mensagens',
    sa.Column('id_mensagem', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('id_conversa', sa.Integer(), nullable=False),
    sa.Column('id_remetente', sa.Integer(), nullable=False),
    sa.Column('id_destinatario', sa.Integer(), nullable=False),
    sa.Column('mensagem', sa.Text(), nullable=False),
    sa.Column('tipo_mensagem', sa.Enum('texto', 'imagem', 'video', 'arquivo'), nullable=False),
    sa.Column('enviado_em', sa.TIMESTAMP(), nullable=True),
    sa.Column('lida', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['id_conversa'], ['Conversas.id_conversa'], ),
    sa.ForeignKeyConstraint(['id_destinatario'], ['Usuarios.id_usuario'], ),
    sa.ForeignKeyConstraint(['id_remetente'], ['Usuarios.id_usuario'], ),
    sa.PrimaryKeyConstraint('id_mensagem')
    )
    with op.batch_alter_table('Mensagens', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_Mensagens_id_conversa'), ['id_conversa'], unique=False)
        batch_op.create_index(batch_op.f('ix_Mensagens_id_remetente'), ['id_remetente'], unique=False)

    op.create_table('ParticipantesConversa',
    sa.Column('id_participante_conversa', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('id_conversa', sa.Integer(), nullable=False),
    sa.Column('id_usuario', sa.Integer(), nullable=False),
    sa.Column('adicionado_em', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['id_conversa'], ['Conversas.id_conversa'], ),
    sa.ForeignKeyConstraint(['id_usuario'], ['Usuarios.id_usuario'], ),
    sa.PrimaryKeyConstraint('id_participante_conversa')
    )
    op.create_table('UsuariosBloqueados',
    sa.Column('id_usuario_bloqueado', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('id_bloqueador', sa.Integer(), nullable=False),
    sa.Column('id_bloqueado', sa.Integer(), nullable=False),
    sa.Column('bloqueado_em', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['id_bloqueado'], ['Usuarios.id_usuario'], ),
    sa.ForeignKeyConstraint(['id_bloqueador'], ['Usuarios.id_usuario'], ),
    sa.PrimaryKeyConstraint('id_usuario_bloqueado')
    )
    op.create_table('MembrosGrupo',
    sa.Column('id_membro_grupo', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('id_grupo', sa.Integer(), nullable=False),
    sa.Column('id_usuario', sa.Integer(), nullable=False),
    sa.Column('adicionado_em', sa.TIMESTAMP(), nullable=True),
    sa.Column('e_admin', sa.Boolean(), nullable=True),
    sa.Column('papel', sa.Enum('admin', 'membro', 'moderador'), nullable=True),
    sa.ForeignKeyConstraint(['id_grupo'], ['Grupos.id_grupo'], ),
    sa.ForeignKeyConstraint(['id_usuario'], ['Usuarios.id_usuario'], ),
    sa.PrimaryKeyConstraint('id_membro_grupo')
    )
    op.create_table('MensagensGrupo',
    sa.Column('id_mensagem_grupo', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('id_grupo', sa.Integer(), nullable=False),
    sa.Column('id_remetente', sa.Integer(), nullable=False),
    sa.Column('mensagem', sa.Text(), nullable=False),
    sa.Column('tipo_mensagem', sa.Enum('texto', 'imagem', 'video', 'arquivo'), nullable=False),
    sa.Column('enviado_em', sa.TIMESTAMP(), nullable=True),
    sa.Column('lida', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['id_grupo'], ['Grupos.id_grupo'], ),
    sa.ForeignKeyConstraint(['id_remetente'], ['Usuarios.id_usuario'], ),
    sa.PrimaryKeyConstraint('id_mensagem_grupo')
    )
    with op.batch_alter_table('MensagensGrupo', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_MensagensGrupo_id_grupo'), ['id_grupo'], unique=False)
        batch_op.create_index(batch_op.f('ix_MensagensGrupo_id_remetente'), ['id_remetente'], unique=False)

    op.create_table('Notificacoes',
    sa.Column('id_notificacao', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('id_usuario', sa.Integer(), nullable=False),
    sa.Column('id_mensagem', sa.Integer(), nullable=True),
    sa.Column('id_grupo', sa.Integer(), nullable=True),
    sa.Column('tipo_notificacao', sa.Enum('mensagem', 'convite_grupo', 'atualizacao_grupo', 'mencao_grupo'), nullable=False),
    sa.Column('conteudo_notificacao', sa.Text(), nullable=True),
    sa.Column('lida', sa.Boolean(), nullable=True),
    sa.Column('criado_em', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['id_grupo'], ['Grupos.id_grupo'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['id_mensagem'], ['Mensagens.id_mensagem'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['id_usuario'], ['Usuarios.id_usuario'], ),
    sa.PrimaryKeyConstraint('id_notificacao')
    )
    with op.batch_alter_table('Notificacoes', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_Notificacoes_id_usuario'), ['id_usuario'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Notificacoes', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_Notificacoes_id_usuario'))

    op.drop_table('Notificacoes')
    with op.batch_alter_table('MensagensGrupo', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_MensagensGrupo_id_remetente'))
        batch_op.drop_index(batch_op.f('ix_MensagensGrupo_id_grupo'))

    op.drop_table('MensagensGrupo')
    op.drop_table('MembrosGrupo')
    op.drop_table('UsuariosBloqueados')
    op.drop_table('ParticipantesConversa')
    with op.batch_alter_table('Mensagens', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_Mensagens_id_remetente'))
        batch_op.drop_index(batch_op.f('ix_Mensagens_id_conversa'))

    op.drop_table('Mensagens')
    op.drop_table('Grupos')
    op.drop_table('ConfiguracoesUsuario')
    with op.batch_alter_table('Usuarios', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_Usuarios_email'))

    op.drop_table('Usuarios')
    op.drop_table('Conversas')
    # ### end Alembic commands ###
