from flask import Flask, render_template, request, redirect, url_for, flash 
from config import config
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required
import os 
import requests
from Rotuer_Netmiko import CSR1000v
from netmiko import ConnectHandler
from requests.auth import HTTPBasicAuth

#models
from models.ModelUser import ModelUser

#entities
from models.entities.User import User 

app = Flask(__name__)
csrf=CSRFProtect()
db=MySQL(app)
login_manager_app = LoginManager(app)


@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)
    

@app.route("/")
def home():
    return  redirect(url_for('login'))
  


@app.route("/login",  methods=['GET','POST'])
def login():
    if request.method == 'POST':
        print(request.form['username'])
        print(request.form['password'])
        user = User(0,request.form['username'], request.form['password'])
        print(user.password)
        logged_user = ModelUser.login(db, user)

        if logged_user != None: 
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('index'))
            else: 
                flash('Contraseña Erronea')
                return render_template('login.html')
        else:
            flash('Usuario no Encontrado')
            return render_template('login.html')
    else:
        return render_template('login.html')
    

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return "<h1>404 Pagina no encontrada </h1>"

@app.route("/index")
@login_required
def index():
    R1 = ['R1 RestConf', '192.168.124.129', '/RestConf', 'success']
    R2 = ['R2 SSH', CSR1000v['host'], '/SSH', 'primary']
    Routers = [R1, R2]
   
    data ={
        'titulo': 'Inicio',
        'valor2' : 'cualquiercosa',
        'listaR' : Routers
    }
    return render_template('index.html', data= data)

@app.route("/SSH")
@login_required
def ssh():
    net_connect = ConnectHandler(**CSR1000v)
    output  = net_connect.send_command('show ip int brief')
    net_connect.disconnect()
    lines = output.split('\n')

    # Índices de posición para cada columna
    interface_end = 22
    ip_address_end = 39
    ok_end = 43
    method_end = 50
    status_end = 72
    protocol_end = len(lines[0])

    inter = []
    # Procesar cada línea
    for line in lines:
        interface = line[:interface_end].strip()
        ip_address = line[interface_end:ip_address_end].strip()
        ok = line[ip_address_end:ok_end].strip()
        method = line[ok_end:method_end].strip()
        status = line[method_end:status_end].strip()
        protocol = line[status_end:protocol_end].strip()
         # Añadir los valores a la lista como un diccionario
        inter.append({
            'interface': interface,
            'ip_address': ip_address,
            'ok': ok,
            'method': method,
            'status': status,
            'protocol': protocol
        })

    data ={
        'titulo': 'Conexcion via SSH Python',
        'valor2' : 'cualquiercosa',
        'inter' : inter
    }
    return render_template('ssh.html', data= data)

@app.route("/SSHA")
@login_required
def sshA():
    with open('comandos.txt', 'r') as file:
        file_content = file.read()
    data ={
        'titulo': 'Conexcion via SSH Python',
        'valor2' : 'cualquiercosa',
        'file_content' : file_content
    }
    return render_template('sshA.html', data= data)

@app.route("/SSHC", methods=['GET', 'POST'])
@login_required
def sshC():
    if request.method == 'POST':
        # Leer el contenido del textarea
        commands = request.form['content'].strip().split('\n')
        net_connect = ConnectHandler(**CSR1000v)
      
        net_connect.send_config_set(commands)
        print(commands)
        net_connect.disconnect()
    return redirect(url_for('ssh'))


@app.route("/SSHI")
@login_required
def sshI():
    net_connect = ConnectHandler(**CSR1000v)
    output  = net_connect.send_command('show star')
    net_connect.disconnect()
    lines = output.split('\n')
   
    file_content = output

    data ={
        'titulo': 'SSH START',
        'valor2' : 'cualquiercosa',
        'file_content' : file_content
    }
    return render_template('restconf.html', data=data)

url = "https://192.168.124.130/restconf/data/Cisco-IOS-XE-native:native"

# Datos de autenticación
username = 'admin'
password = 'admin'


@app.route("/RestConf")
@login_required
def RestConf():
    #os.system('python Rotuer_Netmiko.py')
    response = requests.get(url, auth=HTTPBasicAuth(username, password), verify=False)
    file_content = response.text
    if response.status_code == 200:
        #data = response.json()  # Convertir la respuesta JSON en un diccionario de Python
        print(response)  # Imprimir los datos obtenidos
    else:
        print(f"Error al realizar la solicitud: {response.status_code} - {response.text}")

    data ={
        'titulo': 'RestConf',
        'valor2' : 'cualquiercosa',
        'file_content' : file_content
    }
    return render_template('restconf.html', data=data)


if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()
