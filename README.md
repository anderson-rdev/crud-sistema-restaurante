🍽️ Sistema de Gerenciamento de Restaurantes (CLI)

Aplicação de linha de comando para gerenciamento de restaurantes e avaliações, com persistência de dados em MongoDB. Desenvolvida como parte da disciplina Banco de Dados Avançado, ministrada pela Profa. MSc. Viviane Guimarães Ribeiro.

 📋 Funcionalidades
 
Menu interativo com as seguintes opções:

1. ✅ Cadastrar um novo restaurante
2. 📋 Listar todos os restaurantes
3. ✏️ Editar dados de um restaurante
4. ❌ Remover um restaurante
5. 📝 Adicionar avaliação a um restaurante
6. 🔍 Listar avaliações de um restaurante
7. 🔄 Editar uma avaliação existente
8. 🗑️ Remover uma avaliação
9. 📊 Exibir média de avaliações por restaurante (ordenado por nome)
10. 🚪 Encerrar aplicação

 🧰 Tecnologias Utilizadas

 - Python 3.x
 - MongoDB (banco NoSQL)
 - PyMongo (driver para integração com MongoDB)

 ⚙️ Configuração do Ambiente (Windows)

1. Abra o PowerShell e acesse a pasta "Meus Documentos":

   ```bash
   cd C:\Users\SeuUsuario\Documents
   ```

2. Crie e acesse a pasta do projeto:

   ```bash
   mkdir crud_mongodb
   cd crud_mongodb
   ```

3. Crie e ative um ambiente virtual, e instale o PyMongo:

   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   pip install pymongo
   ```
