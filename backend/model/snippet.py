# model/snippet.py

import re

def generate_snippet(document_text, full_query, window=35):
    text_lower = document_text.lower()
    match_to_use = None
    found_text = ""

    phrase_pattern = r'\b' + re.escape(full_query.lower()) + r'\b'
    phrase_match = re.search(phrase_pattern, text_lower)

    if phrase_match:
        match_to_use = phrase_match
        found_text = full_query.lower()
    else:
        keywords = full_query.lower().split()
        for keyword in keywords:
            keyword_pattern = r'\b' + re.escape(keyword) + r'\b'
            keyword_match = re.search(keyword_pattern, text_lower)
            if keyword_match:
                match_to_use = keyword_match
                found_text = keyword
                break
    
    if not match_to_use:
        return document_text[:window*2] + '...'

    keyword_pos = match_to_use.start()
    keyword_len = len(found_text)
    
    start = max(0, keyword_pos - window)
    end = min(len(document_text), keyword_pos + keyword_len + window)
    
    snippet = document_text[start:end]
    
    original_text_in_snippet = document_text[keyword_pos : keyword_pos + keyword_len]
    highlighted_snippet = snippet.replace(original_text_in_snippet, original_text_in_snippet.upper())
    
    if start > 0:
        highlighted_snippet = '... ' + highlighted_snippet
    if end < len(document_text):
        highlighted_snippet = highlighted_snippet + ' ...'
        
    return highlighted_snippet