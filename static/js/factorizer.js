/**
 * Factorizer.js - Script pour la factorisation de nombres
 * Gère l'interface utilisateur et les appels API pour la factorisation
 */

document.addEventListener('DOMContentLoaded', function() {
    const numberInput = document.getElementById('number-input');
    const factorizeBtn = document.getElementById('factorize-btn');
    const methodInputs = document.querySelectorAll('input[name="method"]');
    const resultBox = document.getElementById('result-box');
    const loadingIndicator = document.getElementById('loading-indicator');

    // Événement pour le bouton de factorisation
    factorizeBtn.addEventListener('click', function() {
        const numberToFactorize = numberInput.value.trim();
        
        // Validation de l'entrée
        if (!numberToFactorize) {
            showError('Veuillez entrer un nombre à factoriser.');
            return;
        }

        // Vérifier que l'entrée est un nombre valide
        if (!/^\d+$/.test(numberToFactorize)) {
            showError('Veuillez entrer un nombre entier positif valide.');
            return;
        }

        // Obtenir la méthode sélectionnée
        let selectedMethod = 'trial-division'; // Valeur par défaut
        methodInputs.forEach(input => {
            if (input.checked) {
                selectedMethod = input.value;
            }
        });

        // Afficher l'indicateur de chargement
        loadingIndicator.classList.remove('hidden');
        resultBox.classList.add('hidden');

        // Temps de début pour mesurer la performance
        const startTime = Date.now();

        // Appel à l'API pour factoriser
        fetch('/api/factorize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                number: numberToFactorize,
                method: selectedMethod
            }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erreur lors de la factorisation. Vérifiez votre entrée.');
            }
            return response.json();
        })
        .then(data => {
            // Masquer l'indicateur de chargement
            loadingIndicator.classList.add('hidden');
            resultBox.classList.remove('hidden');

            // Afficher les résultats
            displayFactorizationResults(data);

            // Afficher le temps d'exécution
            const executionTime = showExecutionTime(startTime);
            
            // Afficher la méthode utilisée
            const methodUsedElement = document.getElementById('method-used');
            if (methodUsedElement) {
                methodUsedElement.textContent = data.method || selectedMethod;
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

    // Fonction pour afficher les résultats de factorisation
    function displayFactorizationResults(data) {
        if (!data.success) {
            resultBox.innerHTML = `
                <p class="error-message" style="color: var(--accent-color);">
                    Échec de la factorisation: ${data.error || 'Une erreur inconnue s\'est produite.'}
                </p>`;
            return;
        }

        // En cas de succès
        if (data.prime) {
            resultBox.innerHTML = `
                <p><strong>${data.number}</strong> est un nombre premier.</p>`;
        } else {
            // Afficher les facteurs
            let factorsHTML = '<p>Factorisation de <strong>' + data.number + '</strong> :</p>';
            factorsHTML += '<ul>';
            
            // Si les facteurs sont fournis en format puissance
            if (data.factorization) {
                data.factorization.forEach(factor => {
                    const base = factor.base;
                    const exponent = factor.exponent;
                    factorsHTML += `<li>${base}${exponent > 1 ? '<sup>' + exponent + '</sup>' : ''}</li>`;
                });
            } 
            // Si les facteurs sont fournis dans un tableau simple
            else if (data.factors) {
                // Grouper les facteurs
                const factorCounts = {};
                data.factors.forEach(factor => {
                    factorCounts[factor] = (factorCounts[factor] || 0) + 1;
                });
                
                // Afficher chaque facteur avec son exposant
                for (const [factor, count] of Object.entries(factorCounts)) {
                    factorsHTML += `<li>${factor}${count > 1 ? '<sup>' + count + '</sup>' : ''}</li>`;
                }
            }
            
            factorsHTML += '</ul>';
            
            resultBox.innerHTML = factorsHTML;
        }
    }

    // Simuler la factorisation (pour le développement front-end)
    function simulateFactorization(number, method) {
        // Cas simples pour le développement
        const examples = {
            '143': {
                success: true,
                number: '143',
                prime: false,
                factorization: [
                    { base: 11, exponent: 1 },
                    { base: 13, exponent: 1 }
                ],
                method: method
            },
            '1024': {
                success: true,
                number: '1024',
                prime: false,
                factorization: [
                    { base: 2, exponent: 10 }
                ],
                method: method
            },
            '17': {
                success: true,
                number: '17',
                prime: true,
                method: method
            }
        };

        return examples[number] || {
            success: true,
            number: number,
            prime: false,
            factors: [2, 2, number / 4],
            method: method
        };
    }
});
