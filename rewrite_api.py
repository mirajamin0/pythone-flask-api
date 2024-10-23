from flask import Flask, request, jsonify
from langdetect import detect, LangDetectException

app = Flask(__name__)

# Sample rewrite logic for different languages
def rewrite_text(text, lang):
    if lang == 'en':  # English
        return text[::-1]  # Example: reverse the text for demonstration
    elif lang == 'es':  # Spanish
        return text.upper()  # Example: convert text to uppercase
    elif lang == 'fr':  # French
        return text.replace('e', 'é')  # Example: replace 'e' with 'é'
    else:
        return f"[{lang}] " + text  # Fallback: prefix language code to the text

@app.route('/rewrite', methods=['POST'])
def rewrite():
    try:
        # Parse the input JSON request
        data = request.get_json()
        text = data.get('text')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400

        # Detect the language of the input text
        try:
            detected_language = detect(text)
        except LangDetectException:
            return jsonify({'error': 'Could not detect the language'}), 400

        # Rewrite the text based on the detected language
        rewritten_text = rewrite_text(text, detected_language)

        # Return the original and rewritten text
        return jsonify({
            'original_text': text,
            'detected_language': detected_language,
            'rewritten_text': rewritten_text
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
