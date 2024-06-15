# Resume Analyzer Project

## Overview

The Resume Analyzer project is a Python-based application designed to automate the process of parsing resumes, extracting relevant details, and ranking them based on job descriptions. It leverages cutting-edge technologies such as OpenAI's GPT models and Azure's AI Document Intelligence to process and understand resumes efficiently.

## Features

- **Automated Resume Parsing**: Extract text from PDF resumes using Azure AI Document Intelligence API.
- **Data Extraction and Structuring**: Convert unstructured resume text into structured JSON format using OpenAI's GPT models.
- **Resume Ranking**: Rank resumes based on their relevance to specific job descriptions, utilizing OpenaAI's GPT-4.
- **Scalable Processing**: Handle multiple resumes simultaneously with a state graph that manages the flow of data through various processing nodes.

## Future Features

- **Enhanced Personalization**: Customization options for different job sectors and roles.
- **Improved AI Accuracy**: Implement feedback loops to improve AI model predictions over time.
- **User Interface**: Develop a web-based interface for easier interaction and management of resume processing.
- **Integration with HR Systems**: Allow seamless integration with existing HR management systems for direct application use.

## Setup Instructions

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-repository/hiring-agent.git
   cd hiring-agent
   ```

2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:

   - Copy `.env.sample` to `.env`.
   - Fill in the necessary API keys and endpoints in `.env`.

4. **Run the Application**:
   ```bash
   python graph.py
   ```

## How to Contribute

1. **Fork the Repository**: Start by forking the repository to your GitHub account.
2. **Clone Your Fork**: Clone the forked repository to your local machine.
3. **Create a New Branch**: Create a new branch for your feature or bug fix.
4. **Make Your Changes**: Implement your feature or fix bugs and commit your changes.
5. **Write Tests**: Add tests to ensure your changes do not break existing functionality.
6. **Submit a Pull Request**: Push your changes to your fork and submit a pull request to the main repository.

## Edge Cases to Be Aware Of

- **PDF Format Variations**: The application might encounter PDFs with complex formatting that could affect text extraction accuracy. (Example: Images)
- **API Limitations**: Be mindful of rate limits and potential downtimes of external APIs like Azure and OpenAI.
- **Data Privacy**: Ensure that the handling of personal data in resumes complies with data protection regulations.

## Folder Structure

```
hiring-agent
│
├── .env.sample
├── .gitignore
├── .env
├── graph.py
├── graphSimple.py
├── requirements.txt
├── utils.py
├── README.md
├── main.py
│
├── Data
│   ├── Resumes
└── Prompt
    └── prompt.py
```

## Code Flow

1. **Environment and Configuration Files**:

   - `.env`: Contains environment variables for API keys and endpoints.
   - `.env.sample`: Sample configuration for setting up `.env`.
   - `.gitignore`: Specifies intentionally untracked files to ignore.

2. **Python Scripts**:

   - `main.py`: The main entry point for the application. It initializes and runs the resume processing flow (Does not uses LangGraph).
   - `graph.py` and `graphSimple.py`: Defines the flow of operations using a state graph. These scripts manage the parsing and ranking of resumes using a graph-based approach.
   - `utils.py`: Contains utility functions for the application (used in main.py)
   - `Prompt/prompt.py`: Contains prompts for AI models to generate structured data from resumes and to rank them based on job descriptions.

3. **Data Handling**:

   - `Data/`: Directory containing resume PDFs to be processed.

4. **Resume Parsing and Ranking Process**:

   - The process starts by loading resumes from the `Data/` directory.
   - `parse_resume_node`: Uses Azure AI Document Intelligence API to extract text from resumes.
   - `get_resume_details_node`: Utilizes OpenAI's GPT model to parse the extracted text into structured JSON format.
   - `rank_resumes_node`: Ranks the parsed resumes based on relevance to a given job description using another OpenAI GPT model prompt.
   - The graph (`StateGraph`) in `graph.py` defines nodes for each of these steps and edges to control the flow from one operation to the next.

5. **Dependencies**:

   - `requirements.txt`: Lists all Python libraries required for the project, ensuring consistent setups across different environments.

6. **Documentation**:
   - `README.md`: Provides an overview of the project, setup instructions, and usage details.

## Code Explanation

### Key Python Files in the Repository:

1. **`main.py`**:

   - **Purpose**: This is the main script that orchestrates the parsing and ranking of resumes. (Note that we dont use langgraph in this approach. Run graph.py directly for a graph based approach)
   - **Functionality**:
     - Iterates over all the resumes one by one parsing text from the resume, extracting details and finally ranking them.
     - Utilizes Azure's AI Document Intelligence API to parse the PDF resumes and OpenAI's GPT models to extract structured data and rank the resumes.
     - The script handles multiple resumes stored in a specified directory and processes each sequentially.
     - After processing, it outputs the parsed details and the ranking scores.

2. **`graph.py`**:

   - **Purpose**: Uses a more complex state graph for handling resume parsing and ranking.
   - **Functionality**:
     - Similar to `main.py`, but designed to handle a more complex flow and larger scale of resume processing.
     - Implements detailed error handling and retry mechanisms, particularly in interactions with external APIs (Azure and OpenAI).
     - Each node in the graph represents a step in processing (e.g., loading a resume, parsing details, ranking), and edges define the flow from one step to the next.
     - Outputs are detailed logs of each step, including successes and failures.

3. **`graphSimple.py`**:

   - **Purpose**: Provides a simplified version of the resume processing graph. (Only processes one resume)
   - **Functionality**:
     - A streamlined version of `graph.py`, used for testing or demonstration purposes with less complexity in error handling and fewer processing steps.
     - Focuses on the core functionalities of loading, parsing, and possibly a simplified ranking mechanism.

4. **`utils.py`**:

   - **Purpose**: Contains utility functions used across the project.
   - **Functionality**:
     - Includes functions like `fix_json`, which is used to correct formatting issues in JSON strings extracted from resumes or API responses.
     - Contains functions for Resume parsing, Ranking, etc which are used in main.py
     - This script is crucial for ensuring data integrity and format consistency across the application.

5. **`Prompt/prompt.py`**:
   - **Purpose**: Defines various prompts used with the OpenAI API to guide the AI in extracting and ranking information.
   - **Functionality**:
     - Contains predefined text prompts that instruct the AI on how to process resumes, what information to extract, and how to format the output.
     - These prompts are critical for ensuring that the AI's responses are aligned with the application's requirements.

#### Additional Files and Directories:

- **`.env.sample` and `.env`**: These files store configuration settings and API keys necessary for interacting with external services like Azure and OpenAI.
- **`requirements.txt`**: Lists all Python libraries required to run the project, ensuring easy setup and consistent environments across different setups.
- **`README.md`**: Provides an overview of the project, setup instructions, and usage guidelines.
- **`Data/` directory**: Contains sample resumes in PDF format, used as input for the application to parse and rank.

### Summary:

This project is a sophisticated application of modern AI tools for automating the parsing and evaluation of resumes. It demonstrates the integration of state management, external AI services, and practical use cases like job application processing.
