# My Fullstack Application

This project is a full-stack application consisting of a FastAPI backend and a React frontend. The application is designed to extract blog content from a given URL and provide suggestions for internal linking.

## Project Structure

```
my-fullstack-app
├── backend
│   ├── api
│   │   └── main.py
│   ├── db
│   │   ├── save_to_supabase.py
│   │   ├── supabase_client.py
│   │   └── supabase_schema.sql
│   ├── embeddings
│   │   └── generate_embeddings.py
│   ├── input
│   │   ├── crawl_urls.py
│   │   ├── extract_content.py
│   │   └── preprocess.py
│   ├── matching
│   │   ├── gpt_anchor_suggester.py
│   │   └── match_blogs.py
│   ├── pipeline.py
│   ├── import_nltk.py
│   ├── requirements.txt
│   └── README.md
├── frontend
│   ├── public
│   │   └── index.html
│   ├── src
│   │   ├── App.tsx
│   │   ├── index.tsx
│   │   ├── components
│   │   │   ├── InputPage.tsx
│   │   │   ├── ProgressPage.tsx
│   │   │   ├── ResultsPage.tsx
│   │   │   └── common
│   │   │       └── DownloadButton.tsx
│   │   ├── types
│   │   │   └── index.ts
│   │   └── utils
│   │       └── extractor.ts
│   ├── package.json
│   ├── tsconfig.json
│   └── README.md
├── .gitignore
├── README.md
└── render.yaml
```

## Getting Started

### Prerequisites

- Node.js (version 14 or higher)
- npm (version 5.6 or higher)
- Python (version 3.7 or higher)
- pip (Python package installer)

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd my-fullstack-app
   ```

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```
2. Install the Python dependencies:
   ```
   pip install -r requirements.txt
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```
2. Install the JavaScript dependencies:
   ```
   npm install
   ```

### Running the Application

- **Backend**: Start the FastAPI server:
  ```
  uvicorn api.main:app --host 0.0.0.0 --port 8000
  ```

- **Frontend**: Start the React application:
  ```
  npm start
  ```

### Deployment

Follow the instructions in the `render.yaml` file for deploying the application on Render.

## Environment Variables

Create a `.env` file in the backend directory to store sensitive environment variables. Example:
```
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
OPENAI_API_KEY=your_openai_api_key
REACT_APP_API_URL=http://your_backend_url/api
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.