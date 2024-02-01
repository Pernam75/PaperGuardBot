<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://media.discordapp.net/attachments/1015252420277846046/1202647844675387412/PaperGuardBot.png?ex=65ce3816&is=65bbc316&hm=505fae41a2e4669b540babe5c02d9fe03ffa9d5168e1edb36ef06b6a009bda7f&=&format=webp&quality=lossless&width=565&height=565" alt="PaperGuardBot Logo"></a>
</p>

<h3 align="center">PaperGuardBot</h3>

<div align="center">

[![Check Rules](https://img.shields.io/badge/see-rules-0078D4?logo=microsoftonedrive&link=https%3A%2F%2Fefrei365net-my.sharepoint.com%2F%3Ab%3A%2Fg%2Fpersonal%2Fjules_rubin_efrei_net%2FEcw-ANTxu5dNggBS3hHW0cgBI143_KRtDaYLvA6Z4ukHZw%3Fe%3DTlxje9)](https://efrei365net-my.sharepoint.com/:b:/g/personal/jules_rubin_efrei_net/Ecw-ANTxu5dNggBS3hHW0cgBI143_KRtDaYLvA6Z4ukHZw?e=Tlxje9)
[![See Report](https://img.shields.io/badge/see-report-0078D4?logo=microsoftonedrive&link=https%3A%2F%2Fefrei365net-my.sharepoint.com%2F%3Aw%3A%2Fg%2Fpersonal%2Fjules_rubin_efrei_net%2FEUFkISgdWf5EqGDJPeu_ofABOdyzVniqtlue1JXqeEUsqA%3Fe%3D3jowMr)](https://efrei365net-my.sharepoint.com/:w:/g/personal/jules_rubin_efrei_net/EUFkISgdWf5EqGDJPeu_ofABOdyzVniqtlue1JXqeEUsqA?e=3jowMr)
[![See Presentation](https://img.shields.io/badge/see-presentation-B7472A?logo=microsoftpowerpoint&link=https%3A%2F%2Fefrei365net-my.sharepoint.com%2F%3Ab%3A%2Fg%2Fpersonal%2Fjules_rubin_efrei_net%2FEcw-ANTxu5dNggBS3hHW0cgBI143_KRtDaYLvA6Z4ukHZw%3Fe%3DTlxje9)](https://efrei365net-my.sharepoint.com/:b:/g/personal/jules_rubin_efrei_net/Ecw-ANTxu5dNggBS3hHW0cgBI143_KRtDaYLvA6Z4ukHZw?e=Tlxje9)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="center"> Unleash the power of secure document exploration with PaperGuardBot! Our cutting-edge chatbot, fueled by the llama2 model, revolutionizes PDF interaction, ensuring GDPR compliance and safeguarding your data. Dive into seamless, protected information retrieval for a smarter and safer document experience.
    <br> 
</p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Built Using](#built_using)
- [TODO](../TODO.md)
- [Authors](#authors)

## 🧐 About <a name = "about"></a>

PaperGuardBot is an innovative chatbot powered by the llama2 model, designed to provide secure and efficient interaction with PDF documents. Ensuring compliance with the European RGPD, the bot's unique approach allows users to query relevant information within uploaded documents without compromising data security. Whether for research, analysis, or information retrieval, PaperGuardBot offers a safe and reliable solution for exploring PDF content seamlessly.


## 🏁 Getting Started <a name = "getting_started"></a>

To experience the seamless document interaction provided by PaperGuardBot, follow these steps:

### Prerequisites

Navigate to [Pinecone](https://www.pinecone.io/). Create an account and obtain your API key. Pinecone is a vector database that allows you to store and query vectors. It is used to store the vectors of the documents that you upload to PaperGuardBot. Pinecone respects your privacy according to the [GDPR](https://gdpr.eu/what-is-gdpr/).

### Backend (Docker Container)
1. Clone the repository:

   ```bash
   git clone <repository-url>
    ```
2. Navigate to the backend folder:

   ```bash
   cd backend
    ```
3. Build and run the Docker container:

   ```bash
   docker-compose up --build
    ```

This will initialize the backend services required for secure document processing.

### Frontend

Visit the [PaperGuardBot Frontend](https://www.julesrubin.com/) and explore the intuitive user interface for interacting with PDF documents.

Provide the following information to the frontend:

- Pinecone API key
- Pinecone index name
- Websocket URL (ws://localhost:8080)

Now, both the frontend and backend are ready for a cohesive PaperGuardBot experience!

## 🎈 Usage <a name="usage"></a>

PaperGuardBot is designed to provide a seamless and secure document interaction experience. To use the bot, follow these steps:

1. Upload one or more PDF documents into the frontend interface. This will automatically upload the documents to Pinecone and store their vectors.
2. Once the documents are uploaded, you can interact with them using the chatbot. You can ask the bot to retrieve specific information from the documents or ask him to summarize, reformulate, or translate the documents.
3. The bot will return the requested information. As the documents are stored in Pinecone and the LLM model is running in your docker container, the bot will never send your documents to a third party. Your documents are safe and secure.

## ⛏️ Built Using <a name = "built_using"></a>

- [Python](https://www.python.org/) - Backend programming language
- [Pinecone](https://www.pinecone.io/) - Vector database
- [Docker](https://www.docker.com/) - Containerization
- [Flask](https://flask.palletsprojects.com/en/2.0.x/) - Backend framework
- [Streamlit](https://streamlit.io/) - Frontend framework
- [HuggingFace](https://huggingface.co/) - LLM and embedding models

## ✍️ Authors <a name = "authors"></a>

- [@SenShiben - Ayman Ben Hajjaj](https://github.com/Senshiben-efrei) - Backend, LLM model, and embedding model.
- [@Pernam75 - Jules Rubin](https://github.com/Pernam75) - Frontend, vector database, and API.
