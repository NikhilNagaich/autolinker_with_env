# My Fullstack App - Frontend

This project is a React application designed to work in conjunction with a FastAPI backend. It provides a user interface for extracting blog content from given URLs and displaying the results.

## Project Structure

```
my-fullstack-app
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
```

## Getting Started

### Prerequisites

- Node.js (version 14 or higher)
- npm (version 5.6 or higher)

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the frontend directory:
   ```
   cd my-fullstack-app/frontend
   ```
3. Install the dependencies:
   ```
   npm install
   ```

### Running the Application

To start the development server, run:
```
npm start
```
This will launch the application in your default web browser at `http://localhost:3000`.

### Usage

1. Navigate to the Input Page to enter a blog URL.
2. Click "Start" to begin the extraction process.
3. Monitor the Progress Page for the status of the extraction.
4. Once completed, view the Results Page to see the extracted blogs and links, with options to download the results.

## Environment Variables

To configure the application, create a `.env` file in the root of the frontend directory with the following content:
```
REACT_APP_API_URL=http://your_backend_url/api
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.