This README explains how to use the script to extract keywords from PDFs, generate clean hashtags, and save the results in a JSON file. It includes setting up a virtual environment, installing necessary libraries, and cleaning text for better keyword extraction. Additionally, it provides a complete script that processes PDFs from a specified folder and creates summaries with a limit on the number of hashtags.

#### Step 1: Install Python (if not already installed)
Make sure you have Python 3 installed. You can download it from the official [Python website](https://www.python.org/).

#### Step 2: Create a Virtual Environment
A virtual environment allows you to manage project-specific dependencies without affecting other Python projects on your machine.

```bash
# Create a virtual environment named 'hashtag_generator'
python3 -m venv hashtag_generator

# Activate the virtual environment
# On Windows
hashtag_generator\Scripts\activate

# On macOS and Linux
source hashtag_generator/bin/activate
```

#### Step 3: Install Required Libraries
After activating the virtual environment, install **spaCy** and other necessary libraries:

```bash
# Install spaCy
pip install spacy

# Download the Italian language model for spaCy (adjust if working with a different language)
python -m spacy download en_core_web_sm

# Install PyMuPDF for PDF text extraction
pip install PyMuPDF

# Install any other utilities like JSON handling
pip install tqdm
```

This setup will allow you to process English text, extract keywords, and handle PDF files.

#### Step 4: usage (with virtualenv active)

```bash
python hashtag_generator.py /path/to/pdf_folder --max_tags 10 --output results.json --lang_model en_core_web_sm
```

*where*

- **`/path/to/pdf_folder`**: Replace this with the path to your folder containing PDF files.
- **`--max_tags 10`**: Specifies that a maximum of 10 hashtags should be generated for each PDF.
- **`--output results.json`**: Specifies the name of the JSON output file.
- **`--lang_model en_core_web_sm`**: Uses the English language model (you can switch to another language model if needed).

### English Commond Models:

`en_core_web_sm` (small model, fast with basic NLP features), `en_core_web_md` (medium model, includes word vectors for better semantic understanding), `en_core_web_lg` (large model, provides detailed word vectors for improved context awareness), `en_core_web_trf` (transformer-based model, offers the highest accuracy using deep learning but is resource-intensive).

### Common Models for Other Languages:
spaCy also supports models for other major languages, each with versions similar to those for English:

- **Italian**: `it_core_news_sm`, `it_core_news_md`, `it_core_news_lg`
- **French**: `fr_core_news_sm`, `fr_core_news_md`, `fr_core_news_lg`
- **Spanish**: `es_core_news_sm`, `es_core_news_md`, `es_core_news_lg`
- **German**: `de_core_news_sm`, `de_core_news_md`, `de_core_news_lg`
