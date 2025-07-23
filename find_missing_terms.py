import re
from collections import Counter

# Load the extracted text
with open('indolent_kitchen_gardening_extracted.txt', 'r', encoding='utf-8') as f:
    text = f.read().lower()

# List of gardening terms already in your patterns (flattened), now including common Canberra vegetables/fruits
existing_terms = {
    # Original terms
    'soil', 'compost', 'fertilizer', 'mulch', 'seeds', 'seedlings', 'transplant', 'harvest', 'prune', 'water',
    'irrigation', 'drainage', 'garden', 'plot', 'bed', 'row', 'container', 'pot', 'greenhouse', 'shed', 'tool',
    'shovel', 'rake', 'hoe', 'trowel', 'organic', 'pesticide', 'herbicide', 'fungicide', 'pest', 'disease',
    'blight', 'mildew', 'rot', 'sunlight', 'shade', 'full sun', 'partial shade', 'hardiness zone', 'climate',
    'season', 'spring', 'summer', 'autumn', 'winter', 'germination', 'pollination', 'photosynthesis', 'root',
    'stem', 'leaf', 'flower', 'fruit', 'vegetable', 'herb', 'planting', 'sowing', 'watering', 'fertilizing',
    'pruning', 'harvesting', 'weeding', 'mulching', 'composting', 'transplanting', 'thinning', 'pinching',
    'deadheading', 'staking', 'trellising', 'crop rotation', 'seed starting', 'hardening off', 'direct sowing',
    'indoor growing', 'organic gardening', 'companion planting', 'succession planting', 'intercropping',
    # Common Canberra vegetables
    'carrot', 'carrots', 'beetroot', 'broccoli', 'cabbage', 'cauliflower', 'lettuce', 'spinach', 'silverbeet',
    'peas', 'beans', 'zucchini', 'pumpkin', 'potato', 'potatoes', 'onion', 'onions', 'leek', 'leeks', 'radish',
    'turnip', 'parsnip', 'celery', 'spring onion', 'spring onions', 'garlic', 'tomato', 'tomatoes', 'capsicum',
    'bell pepper', 'chilli', 'chillies', 'cucumber', 'corn', 'kale', 'brussels sprouts',
    # Common Canberra fruits
    'apple', 'apples', 'pear', 'pears', 'plum', 'plums', 'cherry', 'cherries', 'peach', 'peaches', 'nectarine',
    'nectarines', 'apricot', 'apricots', 'quince', 'quinces', 'fig', 'figs', 'strawberry', 'strawberries',
    'raspberry', 'raspberries', 'blackberry', 'blackberries', 'blueberry', 'blueberries', 'grape', 'grapes',
    'gooseberry', 'gooseberries', 'currant', 'currants', 'lemon', 'lemons', 'mandarin', 'mandarins',
    # Herbs
    'parsley', 'coriander', 'basil', 'rosemary', 'thyme', 'oregano', 'mint', 'chives', 'sage'
}

# Common English stopwords to ignore
stopwords = {
    'the', 'and', 'for', 'with', 'from', 'into', 'over', 'when', 'where', 'you', 'your', 'they', 'their', 'these',
    'those', 'will', 'have', 'has', 'are', 'was', 'not', 'can', 'may', 'all', 'one', 'two', 'three', 'four', 'five',
    'six', 'seven', 'eight', 'nine', 'ten', 'it', 'in', 'on', 'at', 'by', 'to', 'of', 'as', 'be', 'is', 'or', 'an',
    'a', 'we', 'if', 'so', 'do', 'no', 'up', 'out', 'some', 'more', 'most', 'any', 'each', 'many', 'much', 'such',
    'only', 'own', 'same', 'than', 'too', 'very', 'just', 'even', 'still', 'also', 'after', 'before', 'again',
    'once', 'about', 'because', 'how', 'while', 'during', 'without', 'within', 'between', 'through', 'since',
    'until', 'although', 'though', 'nor', 'yet', 'both', 'either', 'neither', 'whether', 'why', 'which', 'what',
    'who', 'whose', 'whom', 'here', 'there', 'every', 'another', 'few', 'less', 'least', 'great', 'greater',
    'greatest', 'best', 'better', 'worst', 'bad', 'worse', 'good', 'new', 'old', 'young', 'first', 'last', 'next',
    'previous', 'other', 'none'
}

# Find all words
words = re.findall(r'\b[a-z]{3,}\b', text)

# Count frequency, filter out stopwords and existing terms
filtered = [w for w in words if w not in stopwords and w not in existing_terms]
counts = Counter(filtered)

print("Most common potential gardening terms not in your patterns:")
for word, count in counts.most_common(30):
    print(f"{word}: {count}")