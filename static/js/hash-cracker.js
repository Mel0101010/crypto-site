/**
 * Hash-cracker.js - Script pour le crackage de hash
 * Gère l'interface utilisateur et les appels API pour tenter de retrouver le texte original d'un hash
 */

document.addEventListener('DOMContentLoaded', function() {
    const hashInput = document.getElementById('hash-input');
    const hashType = document.getElementById('hash-type');
    const attackModes = document.querySelectorAll('input[name="attack-mode"]');
    const dictionarySelect = document.getElementById('dictionary-select');
    const charsetSelect = document.getElementById('charset-select');
    const lengthMax = document.getElementById('length-max');
    const crackBtn = document.getElementById('crack-btn');
    const resultBox = document.getElementById('result-box');
    const loadingIndicator = document.getElementById('loading-indicator');

    // Événement pour le bouton de crackage
    crackBtn.addEventListener('click', function() {
        const hashToCrack = hashInput.value.trim();
        
        // Validation de l'entrée
        if (!hashToCrack) {
            showError('Veuillez entrer un hash à cracker.');
            return;
        }

        // Obtenir le mode d'attaque sélectionné
        let attackMode = 'dictionary'; // Valeur par défaut
        attackModes.forEach(input => {
            if (input.checked) {
                attackMode = input.value;
            }
        });

        // Préparer les données pour l'API selon le mode d'attaque
        const requestData = {
            hash: hashToCrack,
            type: hashType.value,
            mode: attackMode
        };

        // Ajouter les paramètres spécifiques au mode
        if (attackMode === 'dictionary') {
            requestData.dictionary = dictionarySelect.value;
        } else if (attackMode === 'bruteforce') {
            requestData.charset = charsetSelect.value;
            requestData.maxLength = parseInt(lengthMax.value, 10);
            
            // Validation de la longueur maximale
            if (requestData.maxLength > 10) {
                showError('La longueur maximale est limitée à 10 caractères pour des raisons de performance.');
                return;
            }
        }

        // Afficher l'indicateur de chargement
        loadingIndicator.classList.remove('hidden');
        resultBox.classList.add('hidden');

        // Temps de début pour mesurer la performance
        const startTime = Date.now();

        // Appel à l'API pour cracker le hash
        fetch('/api/crack-hash', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erreur lors du crackage du hash. Vérifiez votre entrée.');
            }
            return response.json();
        })
        .then(data => {
            // Masquer l'indicateur de chargement
            loadingIndicator.classList.add('hidden');
            resultBox.classList.remove('hidden');

            // Afficher les résultats
            displayCrackingResults(data);

            // Afficher le temps d'exécution
            const executionTime = showExecutionTime(startTime);
            
            // Afficher le nombre de tentatives
            const attemptsElement = document.getElementById('attempts');
            if (attemptsElement) {
                attemptsElement.textContent = data.attempts || 'N/A';
            }
        })
        .catch(error => {
            // Masquer l'indicateur de chargement
            loadingIndicator.classList.add('hidden');
            resultBox.classList.remove('hidden');
            
            // Afficher l'erreur
            showError('Erreur: ' + error.message);
        });
    });

    // Fonction pour afficher les résultats du crackage
    function displayCrackingResults(data) {
        if (!data.success) {
            resultBox.innerHTML = `
                <p class="error-message" style="color: var(--accent-color);">
                    Échec du crackage: ${data.error || 'Le hash n\'a pas pu être résolu avec les paramètres fournis.'}
                </p>`;
            return;
        }

        // En cas de succès
        if (data.found) {
            resultBox.innerHTML = `
                <div class="success-message" style="color: var(--secondary-color);">
                    <p><strong>Hash cracké avec succès!</strong></p>
                    <p>Hash: <code>${data.hash}</code></p>
                    <p>Texte original: <code style="background-color: #f0f8ff; padding: 2px 5px;">${data.original}</code></p>
                    <p>Algorithme: ${data.type.toUpperCase()}</p>
                    <p>Mode utilisé: ${data.mode === 'dictionary' ? 'Dictionnaire' : 'Force brute'}</p>
                </div>`;
        } else {
            resultBox.innerHTML = `
                <p>Aucune correspondance trouvée pour ce hash.</p>
                <p>Essayez avec un autre mode d'attaque ou modifiez les paramètres.</p>`;
        }
    }

    // Simuler le crackage (pour le développement front-end)
    function simulateCracking(hash, type, mode) {
        // Quelques exemples pour le développement
        const examples = {
            '5f4dcc3b5aa765d61d8327deb882cf99': {
                success: true,
                found: true,
                hash: '5f4dcc3b5aa765d61d8327deb882cf99',
                original: 'password',
                type: 'md5',
                mode: mode,
                attempts: 15467
            },
            'aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d': {
                success: true,
                found: true,
                hash: 'aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d',
                original: 'hello',
                type: 'sha1',
                mode: mode,
                attempts: 8732
            }
        };

        // Si l'exemple existe, le retourner, sinon simuler un échec
        return examples[hash] || {
            success: true,
            found: false,
            hash: hash,
            type: type,
            mode: mode,
            attempts: 1000000
        };
    }
});
