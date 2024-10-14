#Vou reunir tudo que necessitar de conexão ao banco em um arquivo só
from flask import current_app, g
import mysql.connector
import db_connection_data

#Verifica se já tem uma conexão no banco, caso contrário, cria uma nova
def getdb():
    if 'db' not in g or not g.db.is_connected():
        g.db = mysql.connector.connect(
            host=db_connection_data.host,
            user=db_connection_data.db_user,
            password=db_connection_data.db_password,
            database=db_connection_data.db_database
        )
    return g.db

#Função para fechar a conexão após cada solicitação para evitar múltiplas conexões
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None and db.is_connected():
        db.close()

#Traz o ID de todos os usuários
def get_users():
    db = getdb()
    cursor = db.cursor(dictionary=True)
    cursor.execute('select id_usuario from usuarios')
    usuarios = cursor.fetchall()
    cursor.close()
    return usuarios

#Retorna o ID e a senha a partir do nome do usuário
def get_password_user(user_name):
    db = getdb()
    cursor = db.cursor(dictionary=True)
    print('select id_usuario,senha from usuarios where usuario ="'+user_name+'"')
    cursor.execute('select id_usuario,senha from usuarios where usuario ="'+user_name+'"')
    rt = cursor.fetchone()    
    cursor.close()
    return rt

#Retorna o ID e a senha a partir do ID
def get_password_id(id):
    db = getdb()
    cursor = db.cursor(dictionary=True)
    print('select id_usuario,senha from usuarios where id_usuario ='+id)
    cursor.execute('select id_usuario,senha from usuarios where id_usuario ='+id)
    rt = cursor.fetchone()    
    cursor.close()
    return rt

class cliente():
    #Retorna todos os clientes
    def get_clientes():
        db = getdb()
        cursor = db.cursor(dictionary=True)
        cursor.execute('select * from clientes')
        clientes = cursor.fetchall()    
        print(clientes)
        cursor.close()
        return clientes
    
    #Insere um cliente novo na tabela
    def insert_cliente(nome,telefone,data_nascimento,endereco,facebook,instagram):
        db = getdb()
        cursor = db.cursor(dictionary=True)
        print('insert into clientes (nome,telefone,data_nascimento,endereco,facebook,instagram) values ("'+nome+'","'+telefone+'",'+data_nascimento+','+endereco+','+facebook+','+instagram+')')
        cursor.execute('insert into clientes (nome,telefone,data_nascimento,endereco,facebook,instagram) values ("'+nome+'","'+telefone+'",'+data_nascimento+','+endereco+','+facebook+','+instagram+')')
        db.commit()  
        cursor.close()
        return 1
    
    def update_cliente(id,nome,telefone,data_nascimento,endereco,facebook,instagram):
        db = getdb()
        cursor = db.cursor(dictionary=True)
        cursor.execute('update clientes set (nome,telefone,data_nascimento,endereco,facebook,instagram) values ('+nome+','+telefone+','+data_nascimento+','+endereco+','+facebook+','+instagram+') where id_cliente='+id)
        db.commit()  
        affected_rows = cursor.rowcount
        if affected_rows is not None and affected_rows > 0:
            cursor.close()
            return True
        else:
            return False

    def delete_cliente(cliente_id):
        db = getdb()
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute('DELETE FROM clientes WHERE id_cliente = %s', (cliente_id,))
            db.commit()
        except Exception as e:
            db.rollback()
            raise e 
        finally:
            cursor.close()
    
class agendamentos():

    def get_agendamentos():
        db = getdb()
        cursor = db.cursor(dictionary=True)
        cursor.execute('select * from agendamentos')
        agendamentos = cursor.fetchall()    
        print(agendamentos)
        cursor.close()
        return agendamentos
    
    def insert_agendamentos(id_cliente,id_procedimento,data_agendamento,hora_agendamento,data_realização,status,observacoes):
        db = getdb()
        cursor = db.cursor(dictionary=True)
        cursor.execute('insert into agendamentos (id_cliente,id_procedimento,data_agendamento,hora_agendamento,data_realização,status,observacoes) values ('+id_cliente+','+id_procedimento+','+data_agendamento+','+hora_agendamento+','+data_realização+','+status+','+observacoes+')')
        db.commit()
        cursor.close()
        return cursor.lastrowid()
    
    def update_agendamentos(id_cliente,id_procedimento,data_agendamento,hora_agendamento,data_realização,status,observacoes):
        db = getdb()
        cursor = db.cursor(dictionary=True)
        cursor.execute('update agendamentos set (id_cliente,id_procedimento,data_agendamento,hora_agendamento,data_realização,status,observacoes) values ('+id_cliente+','+id_procedimento+','+data_agendamento+','+hora_agendamento+','+data_realização+','+status+','+observacoes+')')
        db.commit()
        cursor.close()
        affected_rows = cursor.rowcount
        if affected_rows is not None and affected_rows > 0:
            cursor.close()
            return True
        else:
            return False

class servico():

    def get_servico():
        db = getdb()
        cursor = db.cursor(dictionary=True)
        cursor.execute('select * from Procedimentos')
        procedimentos = cursor.fetchall()    
        print(procedimentos)
        cursor.close()
        return procedimentos
    
    def insert_servico(id_procedimento,nome,descricao):
        db = getdb()
        cursor = db.cursor(dictionary=True)
        cursor.execute('insert Procedimentos set (id_cliente,id_procedimento,data_agendamento,hora_agendamento,data_realização,status,observacoes) values ('+id_cliente+','+id_procedimento+','+data_agendamento+','+hora_agendamento+','+data_realização+','+status+','+observacoes+')')
        db.commit()
        cursor.close()
        return cursor.lastrowid()
    
    def update_servico(id_procedimento,nome,descricao):
        db = getdb()
        cursor = db.cursor(dictionary=True)
        cursor.execute('update Procedimentos set (id_procedimento,nome,descricao) values ('+id_cliente+','+id_procedimento+','+data_agendamento+','+hora_agendamento+','+data_realização+','+status+','+observacoes+')')
        db.commit()
        cursor.close()
        affected_rows = cursor.rowcount
        if affected_rows is not None and affected_rows > 0:
            cursor.close()
            return True
        else:
            return False