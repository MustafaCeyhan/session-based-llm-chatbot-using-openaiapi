# AI Personal Assistant

This project is an AI-powered personal assistant built using **Streamlit** for the frontend and **FastAPI** for the backend. The backend interacts with the OpenAI API to generate responses, and the frontend provides a user-friendly chat interface.

## Features
- **Chat Interface**: Users can interact with the AI assistant via a chat interface.
- **Session Management**: Each conversation is associated with a unique session ID.
- **Conversation History**: The chat history is stored in an SQLite database.
- **OpenAI Integration**: The backend uses the OpenAI API to generate responses.

---

## Prerequisites

Before running the project, ensure you have the following installed:

1. **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
2. **Docker Compose**: [Install Docker Compose](https://docs.docker.com/compose/install/)

---

## Project Structure

```
ai-personal-assistant/
├── backend/
│   ├── app.py/                  # Backend application code
│   ├── Dockerfile            # Dockerfile for the backend
├── frontend/
│   ├── streamlit_app.py/                  # Frontend application code
│   ├── Dockerfile            # Dockerfile for the frontend
├── docker-compose.yml        # Docker Compose configuration
└── README.md                 # Project documentation
```

---

## Setup and Running the Project

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/ai-personal-assistant.git
cd ai-personal-assistant
```

### Step 2: Build and Run the Services

Use Docker Compose to build and run the backend and frontend services:

```bash
docker-compose up --build
```

This will:
1. Build the Docker images for the backend and frontend.
2. Start the backend service on port `8000`.
3. Start the frontend service on port `8501`.

### Step 3: Access the Application

- **Frontend**: Open your browser and go to `http://localhost:8501`.
- **Backend**: The backend API will be available at `http://localhost:8000`.

---

## Using the Application

1. **Enter OpenAI API Key**:
   - On the left sidebar of the Streamlit frontend, enter your OpenAI API key.

2. **Start Chatting**:
   - Type your message in the chat input box and press Enter.
   - The AI assistant will respond to your queries.

3. **Reset Conversation**:
   - Use the "Start New Conversation" button in the sidebar to reset the chat history.

---

## Docker Compose Configuration

The `docker-compose.yml` file defines two services:

1. **Backend**:
   - Built from the `./backend/Dockerfile`.
   - Exposes port `8000` for the FastAPI backend.

2. **Frontend**:
   - Built from the `./frontend/Dockerfile`.
   - Exposes port `8501` for the Streamlit frontend.
   - Depends on the backend service.

---

## Backend Details

The backend is built using **FastAPI** and provides the following functionality:

- **API Endpoint**: `POST /llm`
  - Accepts a JSON payload with the user's question, conversation history, session ID, and OpenAI API key.
  - Returns the AI-generated response.

- **Database**:
  - Conversations are stored in an SQLite database (`conversations.db`).

---

## Frontend Details

The frontend is built using **Streamlit** and provides the following functionality:

- **Chat Interface**:
  - Users can enter their OpenAI API key in the sidebar.
  - Users can interact with the AI assistant via a chat interface.

- **Session Management**:
  - Each conversation is associated with a unique session ID.

---

## Stopping the Services

To stop the services, run:

```bash
docker-compose down
```

---

## Troubleshooting

1. **Docker Compose Fails to Start**:
   - Ensure Docker and Docker Compose are installed correctly.
   - Check the logs for errors using `docker-compose logs`.

2. **Frontend Cannot Connect to Backend**:
   - Ensure the backend service is running and accessible at `http://localhost:8000`.
   - Verify the frontend is correctly configured to call the backend API.

3. **OpenAI API Key Not Working**:
   - Ensure the API key is valid and has sufficient credits.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **OpenAI**: For providing the GPT-3.5-turbo model.
- **Streamlit**: For the easy-to-use frontend framework.
- **FastAPI**: For the high-performance backend framework.

---

Feel free to customize this `README.md` to better suit your project. Let me know if you need further assistance!