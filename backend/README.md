# README for the Backend

This project is a FastAPI backend for a full-stack application designed to extract blog content from given URLs. It interacts with a Supabase database for data storage and retrieval, and it includes various functionalities for crawling, extracting, and processing blog data.

## Project Structure

```
my-fullstack-app
├── backend
│   ├── api
│   │   └── main.py          # Entry point for the FastAPI application.
│   ├── db
│   │   ├── save_to_supabase.py  # Handles saving data to Supabase.
│   │   ├── supabase_client.py    # Contains the Supabase client setup.
│   │   └── supabase_schema.sql    # SQL schema for the Supabase database.
│   ├── embeddings
│   │   └── generate_embeddings.py  # Functions for generating embeddings.
│   ├── input
│   │   ├── crawl_urls.py         # Functions for crawling URLs.
│   │   ├── extract_content.py     # Functions for extracting content from URLs.
│   │   └── preprocess.py          # Functions for preprocessing text.
│   ├── matching
│   │   ├── gpt_anchor_suggester.py  # Functions for suggesting anchors using GPT.
│   │   └── match_blogs.py          # Functions for matching blogs based on similarity.
│   ├── pipeline.py                 # Main pipeline logic for the application.
│   ├── import_nltk.py             # Script to import NLTK data.
│   ├── requirements.txt            # Lists Python dependencies.
│   └── README.md                   # Documentation for the backend.
```

## Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the backend directory:
   ```
   cd my-fullstack-app/backend
   ```
3. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

### Running the Application

To start the FastAPI application, run:
```
uvicorn api.main:app --host 0.0.0.0 --port 8000
```
This will launch the application, and it will be accessible at `http://localhost:8000`.

### Environment Variables

Create a `.env` file in the backend directory to store sensitive environment variables. Example:
```
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
OPENAI_API_KEY=your_openai_api_key
```

### Deployment

This backend is designed to be deployed on Render. Follow the instructions in the main project README for deployment steps.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.