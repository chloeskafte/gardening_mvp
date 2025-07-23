import spacy
import re
from collections import Counter
import json

class GardeningNERAnalyser:
    """
    Named Entity Recognition analyser for gardening guides using spaCy.
    """
    
    def __init__(self):
        """Initialise the NER analyser with spaCy model."""
        try:
            # Load English language model
            self.nlp = spacy.load("en_core_web_sm")
            print("✅ spaCy model loaded successfully")
        except OSError:
            print("⚠️  spaCy model not found. Installing...")
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")
            print("✅ spaCy model installed and loaded")
    
    def extract_gardening_entities(self, text):
        """
        Extract named entities and gardening-specific terms from text.
        
        Args:
            text (str): Text to analyse
            
        Returns:
            dict: Dictionary containing different types of entities
        """
        # Process the text with spaCy
        doc = self.nlp(text)
        
        # Extract standard named entities
        entities = {
            'PERSON': [],
            'ORG': [],
            'GPE': [],  # Countries, cities, etc.
            'DATE': [],
            'TIME': [],
            'QUANTITY': [],
            'CARDINAL': [],  # Numbers
            'ORDINAL': [],
            'PRODUCT': [],
            'EVENT': [],
            'WORK_OF_ART': [],
            'LAW': [],
            'LANGUAGE': [],
            'FAC': [],  # Buildings, airports, etc.
            'LOC': [],  # Non-GPE locations
            'MONEY': [],
            'PERCENT': []
        }
        
        # Extract entities by type
        for ent in doc.ents:
            if ent.label_ in entities:
                entities[ent.label_].append({
                    'text': ent.text,
                    'start': ent.start_char,
                    'end': ent.end_char,
                    'label': ent.label_
                })
        
        # Extract gardening-specific terms (custom patterns)
        gardening_terms = self._extract_gardening_terms(text)
        
        # Extract plant names (common gardening plants)
        plant_names = self._extract_plant_names(text)
        
        # Extract gardening techniques/actions
        gardening_techniques = self._extract_gardening_techniques(text)
        
        return {
            'standard_entities': entities,
            'gardening_terms': gardening_terms,
            'plant_names': plant_names,
            'gardening_techniques': gardening_techniques,
            'summary': self._create_summary(entities, gardening_terms, plant_names, gardening_techniques)
        }
    
    def _extract_gardening_terms(self, text):
        """Extract gardening-specific terminology."""
        gardening_patterns = [
            r'\b(soil|compost|fertilizer|mulch|seeds|seedlings|transplant|harvest|prune|water|irrigation|drainage)\b',
            r'\b(garden|plot|bed|row|container|pot|greenhouse|shed|tool|shovel|rake|hoe|trowel)\b',
            r'\b(organic|pesticide|herbicide|fungicide|pest|disease|blight|mildew|rot)\b',
            r'\b(sunlight|shade|full sun|partial shade|hardiness zone|climate|season|spring|summer|autumn|winter)\b',
            r'\b(germination|pollination|photosynthesis|root|stem|leaf|flower|fruit|vegetable|herb)\b'
        ]
        
        terms = []
        for pattern in gardening_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                terms.append({
                    'text': match.group(),
                    'start': match.start(),
                    'end': match.end(),
                    'category': 'gardening_term'
                })
        
        return terms
    
    def _extract_plant_names(self, text):
        """Extract plant names by category (vegetables, fruits, herbs, flowers, etc.), using regex for plurals."""
        categories = {
            'vegetable': [
                r'carrots?', r'beetroots?', r'broccolis?', r'cabbages?', r'cauliflowers?', r'lettuces?', r'spinach', r'silverbeet',
                r'peas?', r'beans?', r'zucchinis?', r'pumpkins?', r'potatoes?', r'onions?', r'leeks?', r'radishes?', r'turnips?',
                r'parsnips?', r'celery', r'spring onions?', r'garlic', r'tomatoes?', r'capsicums?', r'bell peppers?', r'chillies?', 
                r'cucumbers?', r'squash', r'corn', r'kale', r'brussels sprouts?'
            ],
            'fruit': [
                r'apples?', r'pears?', r'plums?', r'cherries?', r'peaches?', r'nectarines?', r'apricots?', r'quinces?', r'figs?',
                r'strawberries?', r'raspberries?', r'blackberries?', r'blueberries?', r'grapes?', r'gooseberries?', r'currants?',
                r'lemons?', r'mandarins?', r'avocados?'
            ],
            'herb': [
                r'parsley', r'coriander', r'basil', r'rosemary', r'thyme', r'oregano', r'mint', r'chives', r'sage', r'cilantro', r'dill'
            ],
            'flower': [
                r'roses?', r'tulips?', r'daffodils?', r'marigolds?', r'sunflowers?'
            ]
        }

        plants = []
        for category, patterns in categories.items():
            pattern = r'\b(' + '|'.join(patterns) + r')\b'
            for match in re.finditer(pattern, text, re.IGNORECASE):
                plants.append({
                    'text': match.group(),
                    'start': match.start(),
                    'end': match.end(),
                    'category': category
                })
        return plants
    
    def _extract_gardening_techniques(self, text):
        """Extract gardening techniques and actions."""
        technique_patterns = [
            r'\b(planting|sowing|watering|fertilizing|pruning|harvesting|weeding|mulching|composting)\b',
            r'\b(transplanting|thinning|pinching|deadheading|staking|trellising|crop rotation)\b',
            r'\b(seed starting|germination|hardening off|direct sowing|indoor growing)\b',
            r'\b(organic gardening|companion planting|succession planting|intercropping)\b'
        ]
        
        techniques = []
        for pattern in technique_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                techniques.append({
                    'text': match.group(),
                    'start': match.start(),
                    'end': match.end(),
                    'category': 'gardening_technique'
                })
        
        return techniques
    
    def _create_summary(self, entities, gardening_terms, plant_names, gardening_techniques):
        """Create a summary of the extracted entities."""
        summary = {
            'total_entities': sum(len(entities[label]) for label in entities),
            'total_gardening_terms': len(gardening_terms),
            'total_plant_names': len(plant_names),
            'total_techniques': len(gardening_techniques),
            'most_common_entities': {},
            'most_common_plants': Counter([p['text'].lower() for p in plant_names]).most_common(10),
            'most_common_techniques': Counter([t['text'].lower() for t in gardening_techniques]).most_common(10)
        }
        
        # Count most common entities by type
        for label in entities:
            if entities[label]:
                summary['most_common_entities'][label] = Counter([e['text'] for e in entities[label]]).most_common(5)
        
        return summary
    
    def analyse_text_file(self, text_file_path):
        """
        Analyse a text file and return NER results.
        
        Args:
            text_file_path (str): Path to the text file to analyse
            
        Returns:
            dict: Analysis results
        """
        try:
            with open(text_file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            print(f"Analysing text file: {text_file_path}")
            print(f"Text length: {len(text)} characters")
            
            results = self.extract_gardening_entities(text)
            
            # Save results to JSON file
            output_file = text_file_path.replace('.txt', '_ner_analysis.json')
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Analysis complete! Results saved to: {output_file}")
            
            # Print summary
            self._print_summary(results['summary'])
            
            return results
            
        except FileNotFoundError:
            print(f"❌ Error: File '{text_file_path}' not found.")
            return None
        except Exception as e:
            print(f"❌ Error analyzing file: {e}")
            return None
    
    def _print_summary(self, summary):
        """Print a formatted summary of the analysis."""
        print("\n" + "="*50)
        print("📊 NER ANALYSIS SUMMARY")
        print("="*50)
        print(f"Total entities found: {summary['total_entities']}")
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
    """Main function to run NER analysis on extracted PDF text."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python ner_analyzer.py <extracted_text_file>")
        print("Example: python ner_analyzer.py indolent_kitchen_gardening_extracted.txt")
        return
    
    text_file = sys.argv[1]
    
    # Initialise analyser
    analyser = GardeningNERAnalyser()
    
    # Analyse the text file
    analyser.analyse_text_file(text_file)

if __name__ == "__main__":
    main() 