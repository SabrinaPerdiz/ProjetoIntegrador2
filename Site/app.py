from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_required, current_user, login_user, logout_user
from dotenv import load_dotenv
import importlib
import os
import db


app = Flask(__name__)
app.secret_key = 'chave'
app.app_context().push()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
db.getdb()

# Carregar variáveis do arquivo .env_local
load_dotenv(dotenv_path='.env_local')

def load_strings(module_access,module_name):
    if module_access == '':
        module = importlib.import_module(f"static.strings.{module_name}_strings")
    else:
        module = importlib.import_module(f"static.strings.{module_access}.{module_name}_strings")
    return module.STRINGS

status = load_strings('','status')
nav_strings = load_strings('adm','dashboard')

class User(UserMixin):

    def __init__(self, username, password):
        self.id = username
        self.password = password

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

@login_manager.user_loader
def load_user(user_id):
    usuario = db.get_password_user(user_id)
    return User(usuario['id_usuario'],usuario['senha'])


#Tela inicial
@app.route("/")
def homepage():
    strings = load_strings('landpage','home')
    phone_number = os.getenv('PHONE_NUMBER')
    return render_template("/landpage/jinja_home.html", strings=strings, phone_number=phone_number)

#Lista de agendamentos
@app.route("/agendamento")
def agendamento():
    return render_template("/landpage/jinja_agendamento.html")

#Tela de login
@app.route("/login", methods=['GET', 'POST'])
def login():
    strings = load_strings('landpage','login')
    if current_user.is_authenticated:
         return redirect(url_for('dashboard'))
    else:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            ret = db.get_password_user(username)
            if ret != None:
                user = User(username,password)
                if user.password == password:
                    login_user(user)
                    return redirect(url_for('dashboard'))
            else:
                flash(status['user_not_found'], 'danger')
                return redirect(url_for('login'))
        
        return render_template('/landpage/jinja_login.html', strings=strings)

#Tela principal do administrador
@app.route("/dashboard")
@login_required
def dashboard():
    strings = load_strings('adm','dashboard')
    return render_template("/adm/jinja_dashboard.html",nav_strings=strings, strings=strings)

#Tela Clientes Cadastrados
@app.route("/clientes")
@login_required
def clientes_cadastrados():
    strings = load_strings('adm','clients')
    mock_clients = db.cliente.get_clientes()
    return render_template("/adm/Client/jinja_clients_list.html",clientes=db.cliente.get_clientes(), strings=strings, nav_strings=nav_strings)

#Tela Cadastro de Clientes
@app.route("/clientes/cadastro", methods=['GET','POST'])
@login_required
def cadastro_cliente():
    strings = load_strings('adm','register_client')
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        data_nascimento = '"'+request.form['data_nascimento']+'"' if request.form['data_nascimento'] != '' else "null"
        facebook = '"'+request.form['facebook']+'"' if request.form['facebook'] != '' else "null"
        instagram = '"'+request.form['instagram']+'"' if request.form['instagram'] != '' else "null"
        endereco = '"'+request.form['endereco']+'"' if request.form['endereco'] != '' else "null"
        retorno = db.cliente.insert_cliente(nome,telefone,data_nascimento,endereco,facebook,instagram)
        retorno = 'nom'
        if retorno != None:
            flash( status['success_register_user'], 'success')
            return redirect(url_for('clientes_cadastrados'))
    return render_template("/adm/Client/jinja_client_register.html", nav_strings=nav_strings, strings=strings, cliente=None)

#Rota de deleção de Clientes
@app.route("/clientes/<int:cliente_id>", methods=['GET', 'DELETE', 'POST'])
@login_required
def delete_cliente(cliente_id):
    strings = load_strings('adm','register_client')
    if request.method == 'DELETE':
        try:
            db.cliente.delete_cliente(cliente_id)
            flash(status['success_delete_user'], 'success')
            return jsonify({"success": True}), 200
        except Exception as e:
            flash(status['error_delete_user'], 'danger')
            return jsonify({"error": str(e)}), 400
    if request.method == 'GET':
         return render_template("/adm/Client/jinja_client_register.html", nav_strings=nav_strings, strings=strings,cliente=db.cliente.get_cliente(cliente_id))
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        data_nascimento = request.form['data_nascimento'] if request.form['data_nascimento'] != "" else "null"
        facebook = request.form['facebook'] if request.form['facebook'] != '' else "null"
        instagram = request.form['instagram'] if request.form['instagram'] != '' else "null"
        endereco = request.form['endereco'] if request.form['endereco'] != '' else "null"
        retorno = db.cliente.update_cliente(cliente_id,nome,telefone,data_nascimento,endereco,facebook,instagram)
        retorno = 'nom'
        if retorno != None:
            flash( status['success_edit_user'], 'success')
            return redirect(url_for('clientes_cadastrados'))
        else:
            flash( status['error_edit_user'], 'success')


#Tela Serviços Cadastrados
@app.route("/serviços")
@login_required
def servicos_cadastrados():
    strings = load_strings('adm','works')
    return render_template("/adm/Work/jinja_works_list.html",works=db.servico.get_servicos() * 13, strings=strings, nav_strings=nav_strings)

#Tela Cadastro de Serviços
@app.route("/serviços/cadastro", methods=['GET','POST'])
@login_required
def cadastro_servico():
    strings = load_strings('adm','register_work')
    if request.method == 'POST':
        # Informações do serviço
        # retorno = db.servico.insert_servico()
        retorno = 'nom'
        if retorno != None:
            flash( status['success_register_work'], 'success')
            return redirect(url_for('cadastro_servico'))
    return render_template("/adm/Work/jinja_work_register.html", nav_strings=nav_strings, strings=strings, work=None)  

#Rota de deleção de Serviços
@app.route("/serviços/<int:service_id>", methods=['GET', 'DELETE', 'POST'])
@login_required
def delete_service(service_id):
    strings = load_strings('adm','register_work')
    if request.method == 'DELETE':
        try:
            db.servico.delete_servico(service_id)
            flash(status['success_delete_work'], 'success')
            return jsonify({"success": True}), 200
        except Exception as e:
            flash(status['error_delete_work'], 'danger')
            return jsonify({"error": str(e)}), 400
    if request.method == 'GET':
         return render_template("/adm/Work/jinja_work_register.html", nav_strings=nav_strings, strings=strings,work=db.servico.get_servico(service_id))
    if request.method == 'POST':
        # Informações do serviço
        # retorno = db.servico.update_servico(service_id,)
        retorno = 'nom'
        if retorno != None:
            flash( status['success_edit_work'], 'success')
            return redirect(url_for('servicos_cadastrados'))
        else:
            flash( status['error_edit_work'], 'success')

#Tela Agendamentos Cadastrados
@app.route("/agendamentos")
@login_required
def agendamentos_cadastrados():
    strings = load_strings('adm','schedulings')
    return render_template("/adm/Schedule/jinja_schedules_list.html",schedulings=db.agendamento.get_agendamentos(), strings=strings, nav_strings=nav_strings)

#Tela Cadastro de Agendamentos
@app.route("/agendamentos/cadastro", methods=['GET','POST'])
@login_required
def cadastro_agendamento():
    strings = load_strings('adm','register_schedule')
    if request.method == 'POST':
        # Informações do agendamento
        # retorno = db.agendamento.insert_agendamento()
        retorno = 'nom'
        if retorno != None:
            flash( status['success_register_schedule'], 'success')
            return redirect(url_for('cadastro_agendamento'))
    return render_template("/adm/Schedule/jinja_schedule_register.html", nav_strings=nav_strings, strings=strings, schedule=None) 

#Rota de deleção de Agendamentos
@app.route("/agendamentos/<int:schedule_id>", methods=['GET', 'DELETE'])
@login_required
def delete_schedule(schedule_id):
    strings = load_strings('adm','register_schedule')
    if request.method == 'DELETE':
        try:
            db.agendamento.delete_agendamento(schedule_id)
            flash(status['success_delete_schedule'], 'success')
            return jsonify({"success": True}), 200
        except Exception as e:
            flash(status['error_delete_schedule'], 'danger')
            return jsonify({"error": str(e)}), 400
    if request.method == 'GET':
         return render_template("/adm/Schedule/jinja_schedule_register.html", nav_strings=nav_strings, strings=strings,schedule=db.agendamento.get_agendamento(schedule_id))
    if request.method == 'POST':
        # Informações do agendamento
        # retorno = db.agendamento.update_schedule(schedule_id,)
        retorno = 'nom'
        if retorno != None:
            flash( status['success_edit_schedule'], 'success')
            return redirect(url_for('agendamentos_cadastrados'))
        else:
            flash( status['error_edit_schedule'], 'success')

# Rota de logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))

if __name__ == '__main__':
    app.run(debug=True)

