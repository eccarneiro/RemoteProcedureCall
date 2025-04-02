# Sistema de Gerenciamento de Estoque com RPC

Este projeto foi desenvolvido como parte do meu aprendizado na disciplina de **Sistemas Distribuídos**, cursada no curso de **Engenharia de Software**. O objetivo principal foi me aprofundar nos conceitos teóricos abordados em aula, aplicando-os na prática por meio da implementação de um sistema distribuído simples, baseado em **Remote Procedure Call (RPC)**.

## Contexto
Na disciplina, estudamos como sistemas distribuídos permitem a comunicação entre diferentes processos ou máquinas, abstraindo a complexidade da rede e possibilitando a execução de funções remotas como se fossem locais. Para explorar isso, escolhi criar um sistema de gerenciamento de estoque que utiliza o protocolo XML-RPC do Python, simulando a interação entre um cliente e um servidor.

## Funcionalidades
O sistema é composto por dois componentes principais:
- **Servidor RPC**: Gerencia um estoque de produtos e usuários, oferecendo operações como:
  - Autenticação de usuários (login/logout).
  - Cadastro e exclusão de usuários (restrito a administradores).
  - Adição, atualização e consulta de produtos no estoque.
  - Controle de concorrência com `threading.Lock` para evitar condições de corrida.
- **Cliente RPC**: Interface interativa que se conecta ao servidor e permite ao usuário executar as operações acima.

### Exemplos de Uso
- Login como `admin` (senha: `admin123`) para gerenciar o sistema.
- Adicionar um novo produto: `monitor`, 5 unidades, R$ 300,00.
- Atualizar o estoque de `phone` com +10 unidades.
- Registrar um novo usuário como `joao` com senha `joao789`.

## Tecnologias Utilizadas
- **Python**: Linguagem principal do projeto.
- **xmlrpc**: Biblioteca nativa do Python para implementar RPC.
- **hashlib**: Para criptografia de senhas com SHA-256.
- **threading**: Para controle de concorrência no acesso ao estoque.

## Aprendizados
Ao desenvolver este projeto, consolidei os seguintes conceitos de Sistemas Distribuídos:
- **Comunicação cliente-servidor**: Entendi como o RPC abstrai a comunicação em rede, permitindo chamadas de funções remotas.
- **Gerenciamento de estado**: Implementei um sistema de sessões para autenticação e controle de permissões (admin vs. usuário comum).
- **Concorrência**: Usei `Lock` para garantir que operações no estoque fossem thread-safe, simulando cenários de múltiplos acessos.
- **Segurança básica**: Apliquei hash em senhas para simular autenticação segura.

## Como Executar
1. **Pré-requisitos**: Python 3.x instalado.
2. **Iniciar o servidor**:
   ```bash
   python rpc_stock_server.py
   ```
   - O servidor roda em `localhost:8000`.
3. **Iniciar o cliente**:
   ```bash
   python rpc_stock_client.py
   ```
   - Use as credenciais padrão: `admin`/`admin123` ou `user`/`user456`.

## Limitações
- O estoque e os usuários são armazenados em memória (não persistentes).
- Não há interface gráfica, apenas um cliente de terminal.
- A segurança é básica (apenas hash de senhas, sem criptografia na comunicação).

## Próximos Passos
- Adicionar persistência com um banco de dados (ex.: SQLite).
- Implementar um protocolo mais moderno como gRPC.
- Criar uma interface web para o cliente.

Este projeto foi uma ótima oportunidade para conectar teoria e prática, e estou animado para continuar explorando sistemas distribuídos em futuros trabalhos!
