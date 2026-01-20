# AI Web Builder Agent

A modern, AI-powered web development tool that generates complete HTML websites with embedded CSS and JavaScript based on natural language descriptions.

## Features

- **Split-Screen UI**: Chat interface on the left, live preview on the right
- **AI-Powered**: Uses OpenAI's GPT-4o to generate professional websites
- **Real-Time Preview**: See your website being built instantly in the iframe
- **Modern Tech Stack**:
  - Frontend: Vanilla HTML/CSS/JavaScript (no frameworks)
  - Backend: Python with FastAPI
  - AI: OpenAI GPT-4o API
- **Modern CSS**: Uses oklch colors, CSS Grid/Flexbox, custom properties, container queries
- **Responsive Design**: Works on mobile, tablet, and desktop
- **Dark/Light Mode**: Automatic and manual theme switching
- **Accessibility**: Full ARIA support, keyboard navigation, focus management
- **Download**: Export generated websites as single HTML files
- **Open in New Tab**: Preview generated websites in a separate browser tab

## Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- pip (Python package manager)

## Installation

1. **Clone or download the repository**

2. **Navigate to the agent directory**:
   ```bash
   cd agent
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set your OpenAI API key**:
   
   Option A - Set as environment variable:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```
   
   Option B - Create a `.env` file in the `agent` directory:
   ```env
   OPENAI_API_KEY=your-api-key-here
   ```

## Usage

### Starting the Server

Run the server from the `agent` directory:

```bash
python server.py
```

The server will start on `http://127.0.0.1:8000`

### Accessing the Application

Open your browser and navigate to:
- **Frontend**: http://127.0.0.1:8000
- **API Documentation**: http://127.0.0.1:8000/docs

### Using the Interface

1. **Type your request** in the chat input field (e.g., "Create a landing page for a coffee shop with a hero section, menu, and contact form")
2. **Click Send** or press Enter
3. **Watch** the AI generate your website in real-time in the preview panel
4. **Refresh** the preview if needed
5. **Open** the generated website in a new tab
6. **Download** the HTML file to use in your projects

## Configuration

You can configure the server using environment variables:

- `HOST`: Server host (default: `127.0.0.1`)
- `PORT`: Server port (default: `8000`)
- `RELOAD`: Enable auto-reload during development (default: `false`)
- `OPENAI_API_KEY`: Your OpenAI API key

Example:
```bash
HOST=0.0.0.0 PORT=3000 RELOAD=true OPENAI_API_KEY=sk-... python server.py
```

## Project Structure

```
weber-test/
├── index.html              # Frontend UI (HTML/CSS/JS)
├── agent/
│   ├── main.py            # AI Agent core logic
│   ├── server.py          # FastAPI web server
│   ├── requirements.txt    # Python dependencies
│   └── output/            # Generated websites (auto-created)
```

## API Endpoints

### `POST /api/chat`
Generate a website based on user request.

**Request Body**:
```json
{
  "message": "Create a landing page for a coffee shop",
  "api_key": "sk-..." // Optional, can be set via environment
}
```

**Response**:
```json
{
  "code": "<html>...</html>",
  "explanation": "I've created...",
  "error": null
}
```

### `GET /api/history`
Get conversation history.

**Response**:
```json
{
  "history": [...],
  "has_code": true
}
```

### `POST /api/clear`
Clear conversation history.

**Request Body**:
```json
{
  "confirm": true
}
```

### `POST /api/download`
Get generated code for download.

**Response**:
```json
{
  "code": "<html>...</html>",
  "filename": "generated-website.html"
}
```

### `GET /api/status`
Get agent status.

**Response**:
```json
{
  "has_api_key": true,
  "has_generated_code": false,
  "conversation_length": 0
}
```

## Development

### Running in Development Mode

Enable auto-reload for faster development:

```bash
RELOAD=true python server.py
```

### Modifying the Frontend

Edit `index.html`. Changes will be reflected when you refresh the browser (no rebuild needed).

### Modifying the Backend

Edit files in the `agent/` directory. With `RELOAD=true`, the server will automatically restart.

## How It Works

1. **User Input**: You describe the website you want in natural language
2. **API Request**: Frontend sends the request to the Python backend
3. **AI Processing**: Python backend calls OpenAI's GPT-4o API with a detailed system prompt
4. **Code Generation**: AI generates complete HTML with embedded CSS and JavaScript
5. **Preview Update**: Frontend receives the code and injects it into the iframe
6. **File Saving**: Generated code is available for download

## AI Agent Capabilities

The agent is trained to:
- Generate semantic HTML5 structure
- Use modern CSS (Grid, Flexbox, custom properties)
- Create responsive designs
- Ensure accessibility (ARIA labels, keyboard navigation)
- Include minimal JavaScript for interactivity
- Use placeholder images when needed
- Follow modification requests to update existing code

## Troubleshooting

### "API key not set" error
Make sure you've set the `OPENAI_API_KEY` environment variable or provide it via the frontend.

### Server won't start
Check that all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Preview not updating
Try clicking the "Refresh" button in the preview panel header.

### Generated code looks broken
This can happen with complex requests. Try being more specific or breaking down your request into smaller parts.

## License

This project is provided as-is for educational and development purposes.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.
