
def translate(texts, source, target):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    from html import unescape
    from google.cloud import translate_v2 as translate
    translate_client = translate.Client()

    # Remove duplicates from texts
    texts = list(set(texts))


    # Do batch of maximum 128 texts at a time
    texts_chunks = [texts[i:i+128] for i in range(0, len(texts), 128)]
    results = []

    for texts_chunk in texts_chunks:
      # Translate each chunk of texts
      translations = translate_client.translate(texts_chunk, target_language=target, source_language=source)
      results.extend(translations)

    # Results is a list of dictionaries, with input and translatedText
    # Return a dictionnary with input as key, and result as value
    return {input: unescape(result['translatedText']) for input, result in zip(texts, results)}