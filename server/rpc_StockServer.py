from xmlrpc.server import SimpleXMLRPCServer
from threading import Lock
import time
import hashlib

# Dados em memória
users = {
    "admin": hashlib.sha256("admin123".encode('utf-8')).hexdigest(), 
    "user": hashlib.sha256("user456".encode('utf-8')).hexdigest()   
}
stock = {
    "laptop": {"quantity": 10, "price": 1500.00},
    "phone": {"quantity": 25, "price": 800.00},
    "tablet": {"quantity": 15, "price": 600.00},
    "headphones": {"quantity": 50, "price": 150.00},
    "monitor": {"quantity": 20, "price": 300.00},
    "keyboard": {"quantity": 40, "price": 50.00},
    "mouse": {"quantity": 60, "price": 25.00},
    "printer": {"quantity": 5, "price": 200.00},
    "scanner": {"quantity": 8, "price": 120.00},
    "router": {"quantity": 12, "price": 100.00},
    "webcam": {"quantity": 30, "price": 70.00},
    "microphone": {"quantity": 20, "price": 40.00},
}
stock_lock = Lock()
sessions = {} 

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def login(username, password):
    print(f"Tentativa de login - Usuário: {username}")
    print(f"Senha recebida (hash): {hash_password(password)}")
    print(f"Hash esperado: {users.get(username)}")
    if username in users and users[username] == hash_password(password):
        session_id = hashlib.sha256(f"{username}{time.time()}".encode('utf-8')).hexdigest()
        sessions[session_id] = {"username": username, "role": "admin" if username == "admin" else "user"}
        print(f"Login bem-sucedido! Session ID: {session_id}")
        return session_id
    print("Falha no login: usuário ou senha inválidos")
    return None

def logout(session_id):
    if session_id in sessions:
        del sessions[session_id]
        return "Logout realizado com sucesso!"
    return "Sessão inválida."

def check_session(session_id, admin_only=False):
    if session_id not in sessions:
        return False, "Sessão inválida ou expirada."
    if admin_only and sessions[session_id]["role"] != "admin":
        return False, "Permissão negada: apenas administradores."
    return True, ""

def get_stock(session_id):
    valid, msg = check_session(session_id)
    if not valid:
        return msg
    return stock

def register_user(session_id, new_username, new_password, role="user"):
    valid, msg = check_session(session_id, admin_only=True)
    if not valid:
        return msg
    if new_username in users:
        return "Usuário já existe!"
    if role not in ["user", "admin"]:
        return "Role inválido! Use 'user' ou 'admin'."
    users[new_username] = hash_password(new_password)
    return f"Usuário {new_username} registrado com sucesso como {role}!"

def delete_user(session_id, username):
    valid, msg = check_session(session_id, admin_only=True)
    if not valid:
        return msg
    if username not in users:
        return "Usuário não encontrado!"
    if username == "admin":
        return "Não é possível deletar o usuário admin!"
    del users[username]
    for sid, session in list(sessions.items()):
        if session["username"] == username:
            del sessions[sid]
    return f"Usuário {username} deletado com sucesso!"

def add_product(session_id, product_name, quantity, price):
    valid, msg = check_session(session_id, admin_only=True)
    if not valid:
        return msg
    with stock_lock:
        if product_name in stock:
            return "Produto já existe!"
        if quantity < 0 or price < 0:
            return "Quantidade e preço devem ser não-negativos!"
        stock[product_name] = {"quantity": quantity, "price": price}
        return f"Produto {product_name} adicionado com sucesso!"

def update_stock(session_id, product_name, quantity_change):
    valid, msg = check_session(session_id)
    if not valid:
        return msg
    with stock_lock:
        if product_name not in stock:
            return "Produto não encontrado!"
        new_quantity = stock[product_name]["quantity"] + quantity_change
        if new_quantity < 0:
            return "Estoque insuficiente!"
        stock[product_name]["quantity"] = new_quantity
        return f"Estoque de {product_name} atualizado para {new_quantity}."

def set_price(session_id, product_name, new_price):
    valid, msg = check_session(session_id, admin_only=True)
    if not valid:
        return msg
    with stock_lock:
        if product_name not in stock:
            return "Produto não encontrado!"
        if new_price < 0:
            return "Preço não pode ser negativo!"
        stock[product_name]["price"] = new_price
        return f"Preço de {product_name} atualizado para {new_price}."

def main():
    server = SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
    print("Servidor RPC de estoque rodando na porta 8000...")
    
    server.register_function(login, "login")
    server.register_function(logout, "logout")
    server.register_function(register_user, "register_user")
    server.register_function(delete_user, "delete_user")
    server.register_function(get_stock, "get_stock")
    server.register_function(add_product, "add_product")
    server.register_function(update_stock, "update_stock")
    server.register_function(set_price, "set_price")
    
    server.serve_forever()

if __name__ == "__main__":
    main()