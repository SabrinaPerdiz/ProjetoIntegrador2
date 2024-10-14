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
@app.route("/clientes", methods=['GET'])
@login_required
def clientes_cadastrados():
    strings = load_strings('adm','clients')
    return render_template("/adm/Client/jinja_clients_list.html",clientes=db.cliente.get_clientes(), strings=strings, nav_strings=nav_strings)

@app.route("/clientes/<int:cliente_id>", methods=['DELETE'])
@login_required
def delete_cliente(cliente_id):
    try:
        db.cliente.delete_cliente(cliente_id)
        flash(status['success_register_user'], 'success')
        return jsonify({"success": True}), 200
    except Exception as e:
        flash(f"Erro ao deletar cliente", 'danger')
        return jsonify({"error": str(e)}), 400

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
        # retorno = db.cliente.insert_cliente(nome,telefone,data_nascimento,endereco,facebook,instagram)
        retorno = 'nom'
        if retorno != None:
            flash( status['success_register_user'], 'success')
            return redirect(url_for('cadastro_cliente'))
    return render_template("/adm/Client/jinja_client_register.html", nav_strings=nav_strings, strings=strings)   

#Tela Serviços Cadastrados
@app.route("/serviços")
@login_required
def servicos_cadastrados():
    strings = load_strings('adm','works')
    return render_template("/adm/Work/jinja_works_list.html",works=db.servico.get_servico(), strings=strings, nav_strings=nav_strings)

#Tela Cadastro de Serviços
@app.route("/serviços/cadastro", methods=['GET','POST'])
@login_required
def cadastro_servico():
    strings = load_strings('adm','register_work')
    if request.method == 'POST':
        # retorno = db.cliente.insert_cliente(nome,telefone,data_nascimento,endereco,facebook,instagram)
        retorno = 'nom'
        if retorno != None:
            flash( status['success_register_work'], 'success')
            return redirect(url_for('cadastro_servico'))
    return render_template("/adm/Work/jinja_work_register.html", nav_strings=nav_strings, strings=strings)   

#Tela Agendamentos Cadastrados
@app.route("/agendamentos")
@login_required
def agendamentos_cadastrados():
    strings = load_strings('adm','schedulings')
    return render_template("/adm/Schedule/jinja_schedules_list.html",schedulings=db.agendamentos.get_agendamentos(), strings=strings, nav_strings=nav_strings)

#Tela Cadastro de Agendamentos
@app.route("/agendamentos/cadastro", methods=['GET','POST'])
@login_required
def cadastro_agendamento():
    strings = load_strings('adm','register_schedule')
    if request.method == 'POST':
        # retorno = db.cliente.insert_cliente(nome,telefone,data_nascimento,endereco,facebook,instagram)
        retorno = 'nom'
        if retorno != None:
            flash( status['success_register_schedule'], 'success')
            return redirect(url_for('cadastro_agendamento'))
    return render_template("/adm/Schedule/jinja_schedule_register.html", nav_strings=nav_strings, strings=strings) 


# Rota de logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))

if __name__ == '__main__':
    app.run(debug=True)

