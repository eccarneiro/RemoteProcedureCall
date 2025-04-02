import xmlrpc.client

def main():
    server = xmlrpc.client.ServerProxy("http://localhost:8000")
    session_id = None
    
    while True:
        if session_id is None:
            print("\n=== Sistema de Estoque RPC ===")
            print("1. Login")
            print("2. Sair")
            choice = input("Escolha uma opção: ")
            
            if choice == "1":
                username = input("Usuário: ")
                password = input("Senha: ")
                session_id = server.login(username, password)
                if session_id:
                    print(f"Login bem-sucedido! Session ID: {session_id}")
                else:
                    print("Falha no login!")
            
            elif choice == "2":
                print("Saindo...")
                break
            
            else:
                print("Opção inválida!")
        
        else:
            print("\n=== Sistema de Estoque RPC ===")
            print("1. Ver estoque")
            print("2. Adicionar produto (admin)")
            print("3. Atualizar estoque")
            print("4. Alterar preço (admin)")
            print("5. Registrar novo usuário (admin)")
            print("6. Deletar usuário (admin)")
            print("7. Logout")
            choice = input("Escolha uma opção: ")
            
            if choice == "1":
                stock = server.get_stock(session_id)
                if isinstance(stock, str):
                    print(stock)
                else:
                    for product, details in stock.items():
                        print(f"{product}: Quantidade={details['quantity']}, Preço={details['price']}")
            
            elif choice == "2":
                product = input("Nome do produto: ")
                qty = int(input("Quantidade: "))
                price = float(input("Preço: "))
                print(server.add_product(session_id, product, qty, price))
            
            elif choice == "3":
                product = input("Nome do produto: ")
                qty_change = int(input("Mudança na quantidade (positiva ou negativa): "))
                print(server.update_stock(session_id, product, qty_change))
            
            elif choice == "4":
                product = input("Nome do produto: ")
                price = float(input("Novo preço: "))
                print(server.set_price(session_id, product, price))
            
            elif choice == "5":
                new_username = input("Novo usuário: ")
                new_password = input("Senha: ")
                role = input("Role (user/admin): ").lower()
                print(server.register_user(session_id, new_username, new_password, role))
            
            elif choice == "6":
                username = input("Usuário a deletar: ")
                print(server.delete_user(session_id, username))
            
            elif choice == "7":
                print(server.logout(session_id))
                session_id = None
            
            else:
                print("Opção inválida!")

if __name__ == "__main__":
    main()