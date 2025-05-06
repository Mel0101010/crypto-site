from flask import render_template, request, jsonify
from crypto_utils.factorizer import factorize_number
from crypto_utils.hash_cracker import crack_hash
from crypto_utils.rsa_utils import analyze_rsa_key

def register_routes(app):
    # Page d'accueil
    @app.route('/')
    def index():
        return render_template('index.html')
    
    # Pages des outils
    @app.route('/factorizer')
    def factorizer_page():
        return render_template('factorizer.html')
    
    @app.route('/hash-cracker')
    def hash_cracker_page():
        return render_template('hash-cracker.html')
    
    @app.route('/rsa-extractor')
    def rsa_extractor_page():
        return render_template('rsa-extractor.html')
    
    # API pour le factorizer
    @app.route('/api/factorize', methods=['POST'])
    def api_factorize():
        data = request.get_json()
        number = data.get('number')
        method = data.get('method')
        result = factorize_number(number, method)
        return jsonify(result)
    
    # API pour le hash cracker
    @app.route('/api/crack-hash', methods=['POST'])
    def api_crack_hash():
        data = request.get_json()
        hash_value = data.get('hash')
        hash_type = data.get('type')
        wordlist = data.get('wordlist')
        result = crack_hash(hash_value, hash_type, wordlist)
        return jsonify(result)
    
    # API pour l'analyse RSA
    @app.route('/api/analyze-rsa', methods=['POST'])
    def api_analyze_rsa():
        data = request.get_json()
        key_type = data.get('keyType')
        key_content = data.get('keyContent')
        options = data.get('options', {})
        result = analyze_rsa_key(key_type, key_content, options)
        return jsonify(result)
