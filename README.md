# 📜 Criador de Personagens LSBC

Bem-vindo ao sistema de criação de personagens do universo **Lost Secrets of the Brazilian Coast (LSBC)** – um cenário de RPG histórico alternativo ambientado no início do século XVIII, com intrigas políticas, artefatos científicos e aventuras no Atlântico Sul.

Este projeto permite criar, editar, visualizar e exportar personagens para campanhas no sistema LSBC, utilizando uma interface moderna construída com **[Streamlit](https://streamlit.io/)**.

---

## 🚀 Funcionalidades

- 🧬 **Distribuição de Atributos** com visualização de bônus manuais e de classe.
- 🏹 **Escolha de Classes e Especializações**, com progressão de nível até o 10.
- ⚙️ **Equipamentos iniciais**, com opção de adicionar armas, armaduras ou itens personalizados.
- ✨ **Seleção de Truques** (poderes/mecanismos científicos) por nível e tipo.
- 📥 **Importação e Exportação** de personagens via JSON.
- 📄 **Resumo completo do personagem**, incluindo atributos, equipamentos, truques e status gerais.

---

## 🗂 Estrutura do Projeto

```plaintext
📁 personagem_rpg/
├── pages/
│   ├── 1_Info_Geral.py          # Aba de informações básicas
│   ├── 2_Classe_e_Origem.py     # Aba de seleção de classe e origem
│   ├── 3_Atributos.py           # Aba de distribuição de atributos
│   ├── 4_Habilidades.py         # (em desenvolvimento)
│   ├── 5_Equipamentos.py        # Aba de escolha e criação de equipamentos
│   ├── 6_Misticismo.py          # (opcional) truques e poderes especiais
│   └── 7_Resumo.py              # Visualização final e exportação
├── dados_sistema.py             # Lógica e dados centrais (classes, armas, cálculos)
├── estilo.py                    # Estilização visual da interface
└── README.md                    # Este arquivo
```

---

## 🛠 Requisitos

- Python 3.9 ou superior
- Instalar dependências:

```bash
pip install -r requirements.txt
```

---

## ▶️ Como rodar

Execute o aplicativo localmente com o Streamlit:

```bash
streamlit run pages/1_Info_Geral.py
```

---

## 🔄 Exportar e Importar Personagens

- Você pode **baixar** o personagem atual como um arquivo `.json` na aba "Resumo".
- Também é possível **importar** um personagem salvo anteriormente e continuar a edição.

---

## 🧠 Sobre o Universo LSBC

O cenário LSBC é um RPG de baixa fantasia inspirado nas obras de Julio Verne, Daniel Defoe e Robert Louis Stevenson, onde a razão, o conflito entre impérios e a ciência primitiva moldam um mundo alternativo nos tempos da exploração marítima. Mais detalhes estão disponíveis na futruramente no site.

---

## 📌 TODO

- [ ] Implementar sistema de habilidades e perícias.
- [ ] Validação automática da ficha.
- [ ] Visualização de truques aprendidos com efeitos.
- [ ] Integração com plataforma de campanha.

---

## 🧑‍💻 Licença

Este projeto é distribuído sob a [Licença MIT](LICENSE).

---

> Projeto criado com ❤️ por mestres e jogadores do universo LSBC.
