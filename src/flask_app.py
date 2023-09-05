from io import TextIOWrapper

from bs4 import BeautifulSoup
import flask
from flask import request, jsonify
import requests

from bigram_frequency import get_bigram_counts


app = flask.Flask(__name__)

DEFAULT_NUM_BIGRAMS = 10


@app.route('/bigrams_from_file', methods=['POST'])
def bigrams_from_file():
    # get file from request
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}, 400)

    num_bigrams = request.args.get('num_bigrams', DEFAULT_NUM_BIGRAMS, type=int)

    text_stream = TextIOWrapper(request.files['file'].stream, encoding='utf-8')
    bigrams, bigram_counts = get_bigram_counts(text_stream)

    return jsonify({
        'bigrams': bigrams[:num_bigrams].tolist(),
        'bigram_counts': bigram_counts[:num_bigrams].tolist(),
    })


@app.route('/bigrams_from_wiki', methods=['GET'])
def bigrams_from_wiki():
    """ Get bigram counts from a Wikipedia article.

    Returns the 10 most frequent bigrams in the article content.
    (If implemented, the number of returned bigrams could be changed by passing the `num_bigrams` query parameter.)
    """
    page, num_bigrams = request.args.get('page'), request.args.get('num_bigrams', DEFAULT_NUM_BIGRAMS, type=int)
    if not page:
        return jsonify({'error': 'No page name specified'}, 400)

    r = requests.get(f'https://en.wikipedia.org/wiki/{page}')
    if r.status_code != 200:
        return jsonify({'error': f'Wikipedia returned status code {r.status_code} for page {page}'}, 400)

    soup = BeautifulSoup(r.content, 'html.parser')

    # Find the div with id="bodyContent", which contains the article only
    target_div = soup.find('div', id='bodyContent')
    if not target_div:
        return jsonify({'error': 'No div with id="bodyContent" found'}, 400)

    # Get all the text within the div, including child elements
    all_text = target_div.get_text(separator=' ')
    bigrams, bigram_counts = get_bigram_counts(all_text)

    return jsonify({
        'bigrams': bigrams[:num_bigrams].tolist(),
        'bigram_counts': bigram_counts[:num_bigrams].tolist(),
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0')  # allow connections from outside, i.e. from the host machine if running in a container on
    # this development server
