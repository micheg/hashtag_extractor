import os
import json
import fitz  # PyMuPDF
from tqdm import tqdm
import spacy
from collections import Counter
import re
import argparse

class HashtagGenerator:
    def __init__(self, lang_model='en_core_web_sm', max_tags=5):
        # Load the language model
        self.nlp = spacy.load(lang_model)
        self.max_tags = max_tags

    @staticmethod
    def clean_text(text):
        """Clean text by removing extra spaces, numbers, and unwanted characters."""
        text = re.sub(r'\s+', ' ', text)  # Remove multiple spaces and new lines
        text = re.sub(r'\b\d+\b', '', text)  # Remove isolated numbers
        text = text.strip()  # Remove leading/trailing whitespace
        return text

    def extract_hashtags(self, text):
        """Extract hashtags, summary, and word count from text."""
        cleaned_text = self.clean_text(text)
        doc = self.nlp(cleaned_text)
        keywords = []

        # Extract keywords based on nouns, proper nouns, adjectives, and verbs
        for token in doc:
            if token.pos_ in ['NOUN', 'PROPN', 'ADJ', 'VERB']:
                # Ensure the token is alphabetic
                if re.match(r'^[a-zA-Z]+$', token.lemma_):
                    keywords.append(token.lemma_.lower())

        # Count the frequency of keywords and limit the number of tags
        most_common_keywords = Counter(keywords).most_common(self.max_tags)
        hashtags = ['#' + keyword[0].replace(' ', '') for keyword in most_common_keywords]

        # Create a cleaned summary using the first 3 sentences
        summary = self.clean_text(" ".join([str(sent) for sent in doc.sents][:3]))

        return {
            "hashtags": hashtags,
            "summary": summary,
            "word_count": len([token.text for token in doc if not token.is_punct])
        }

    @staticmethod
    def extract_text_from_pdf(pdf_path):
        """Extracts text from a PDF file."""
        try:
            doc = fitz.open(pdf_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
        except fitz.FileDataError as e:
            print(f"Error reading PDF: {e}")
            return ""
        return text

    def process_folder(self, folder_path, output_json="output.json"):
        """Processes all PDFs in a folder and generates a JSON file with metadata."""
        results = []
        
        for file_name in tqdm(os.listdir(folder_path)):
            if file_name.lower().endswith(".pdf"):
                pdf_path = os.path.join(folder_path, file_name)
                text = self.extract_text_from_pdf(pdf_path)
                hashtags_data = self.extract_hashtags(text)
                hashtags_data["file_name"] = file_name
                results.append(hashtags_data)
        
        # Write the results to a JSON file
        with open(output_json, "w", encoding='utf-8') as json_file:
            json.dump(results, json_file, ensure_ascii=False, indent=4)
        
        print(f"Data saved to {output_json}")

def main():
    parser = argparse.ArgumentParser(description="Process PDFs to extract hashtags and summaries.")
    parser.add_argument('folder_path', type=str, help='Path to the folder containing PDF files')
    parser.add_argument('--max_tags', type=int, default=5, help='Maximum number of hashtags to extract')
    parser.add_argument('--output', type=str, default='output.json', help='Output JSON file name')
    parser.add_argument('--lang_model', type=str, default='en_core_web_sm', help='spaCy language model to use')

    args = parser.parse_args()

    generator = HashtagGenerator(lang_model=args.lang_model, max_tags=args.max_tags)
    generator.process_folder(args.folder_path, output_json=args.output)

if __name__ == '__main__':
    main()
