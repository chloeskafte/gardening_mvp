import spacy
import re
import json
from collections import Counter
from gardening_terms import PLANT_CATEGORIES, GARDENING_TERMS, GARDENING_TECHNIQUES

def extract_terms_by_category(text, categories):
    results = []
    for category, patterns in categories.items():
        pattern = r'\b(' + '|'.join(patterns) + r')\b'
        for match in re.finditer(pattern, text, re.IGNORECASE):
            results.append({
                'text': match.group(),
                'start': match.start(),
                'end': match.end(),
                'category': category
            })
    return results

def extract_terms(text, patterns, category):
    results = []
    pattern = r'\b(' + '|'.join(patterns) + r')\b'
    for match in re.finditer(pattern, text, re.IGNORECASE):
        results.append({
            'text': match.group(),
            'start': match.start(),
            'end': match.end(),
            'category': category
        })
    return results

class GardeningNERAnalyser:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")

    def extract_gardening_entities(self, text):
        gardening_terms = extract_terms(text, GARDENING_TERMS, 'gardening_term')
        plant_names = extract_terms_by_category(text, PLANT_CATEGORIES)
        gardening_techniques = extract_terms(text, GARDENING_TECHNIQUES, 'gardening_technique')
        return {
            'gardening_terms': gardening_terms,
            'plant_names': plant_names,
            'gardening_techniques': gardening_techniques,
            'summary': self._create_summary(gardening_terms, plant_names, gardening_techniques)
        }

    def _create_summary(self, gardening_terms, plant_names, gardening_techniques):
        summary = {
            'total_gardening_terms': len(gardening_terms),
            'total_plant_names': len(plant_names),
            'total_techniques': len(gardening_techniques),
            'most_common_plants': Counter([p['text'].lower() for p in plant_names]).most_common(10),
            'most_common_techniques': Counter([t['text'].lower() for t in gardening_techniques]).most_common(10)
        }
        return summary

    def analyse_text_file(self, text_file_path):
        try:
            with open(text_file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            results = self.extract_gardening_entities(text)
            output_file = text_file_path.replace('.txt', '_ner_analysis.json')
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            self._print_summary(results['summary'])
            return results
        except FileNotFoundError:
            print(f"❌ Error: File '{text_file_path}' not found.")
            return None
        except Exception as e:
            print(f"❌ Error analysing file: {e}")
            return None

    def _print_summary(self, summary):
        print("\n" + "="*50)
        print("📊 NER ANALYSIS SUMMARY")
        print("="*50)
        print(f"Gardening terms: {summary['total_gardening_terms']}")
        print(f"Plant names: {summary['total_plant_names']}")
        print(f"Gardening techniques: {summary['total_techniques']}")
        if summary['most_common_plants']:
            print(f"\n🌱 Most common plants:")
            for plant, count in summary['most_common_plants']:
                print(f"   {plant}: {count}")
        if summary['most_common_techniques']:
            print(f"\n🔧 Most common techniques:")
            for technique, count in summary['most_common_techniques']:
                print(f"   {technique}: {count}")
        print("="*50)

def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python ner_analyzer_refactored.py <extracted_text_file>")
        return
    text_file = sys.argv[1]
    analyser = GardeningNERAnalyser()
    analyser.analyse_text_file(text_file)

if __name__ == "__main__":
    main() 