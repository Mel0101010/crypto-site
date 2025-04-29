/**
 * Script principal pour CryptoTools
 * Contient les fonctions communes utilisées dans toutes les pages
 */

document.addEventListener('DOMContentLoaded', function() {
    // Fonctions communes à toutes les pages
    
    // Gestion des boutons Clear
    const clearButtons = document.querySelectorAll('[id="clear-btn"]');
    clearButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Réinitialiser les champs de texte
            const textInputs = document.querySelectorAll('input[type="text"], textarea');
            textInputs.forEach(input => {
                input.value = '';
            });
            
            // Réinitialiser les résultats
            const resultBoxes = document.querySelectorAll('.result-box');
            resultBoxes.forEach(box => {
                const defaultText = box.id === 'result-box' ? 'Les résultats apparaîtront ici...' : 
                                    box.id === 'key-info' ? 'Les informations apparaîtront ici...' :
                                    box.id === 'vulnerability-info' ? 'Les vulnérabilités apparaîtront ici...' :
                                    box.id === 'factors-info' ? 'Les facteurs apparaîtront ici...' :
                                    'Les résultats apparaîtront ici...';
                box.innerHTML = `<p>${defaultText}</p>`;
            });
            
            // Cacher les informations de résultat
            const resultInfo = document.getElementById('result-info');
            if (resultInfo) {
                resultInfo.classList.add('hidden');
            }
        });
    });
    
    // Fonction pour afficher/masquer les options selon le mode sélectionné
    const setupToggleOptions = function(triggerName, options) {
        const triggers = document.querySelectorAll(`input[name="${triggerName}"]`);
        if (triggers.length === 0) return;
        
        triggers.forEach(trigger => {
            trigger.addEventListener('change', function() {
                const selectedValue = this.value;
                
                // Cacher toutes les options
                Object.values(options).forEach(option => {
                    document.getElementById(option).classList.add('hidden');
                });
                
                // Afficher l'option correspondante
                if (options[selectedValue]) {
                    document.getElementById(options[selectedValue]).classList.remove('hidden');
                }
            });
        });
    };
    
    // Configuration pour la page hash-cracker
    setupToggleOptions('attack-mode', {
        'dictionary': 'dictionary-options',
        'bruteforce': 'bruteforce-options'
    });

    // Fonction pour formater les grands nombres
    window.formatBigNumber = function(number) {
        if (typeof number !== 'string') {
            number = number.toString();
        }
        
        if (number.length <= 10) return number;
        
        return number.substring(0, 5) + '...' + number.substring(number.length - 5);
    };
    
    // Fonction pour copier du texte dans le presse-papiers
    window.copyToClipboard = function(text) {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        
        alert('Copié dans le presse-papiers !');
    };
    
    // Fonction pour afficher une erreur
    window.showError = function(message, elementId = 'result-box') {
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = `<p class="error-message" style="color: var(--accent-color);">${message}</p>`;
        }
    };
    
    // Fonction pour afficher le temps d'exécution
    window.showExecutionTime = function(startTime) {
        const executionTime = Date.now() - startTime;
        const executionTimeElement = document.getElementById('execution-time');
        if (executionTimeElement) {
            executionTimeElement.textContent = executionTime;
        }
        
        // Afficher les infos de résultat
        const resultInfo = document.getElementById('result-info');
        if (resultInfo) {
            resultInfo.classList.remove('hidden');
        }
        
        return executionTime;
    };

    // Gestionnaire d'erreurs global
    window.addEventListener('error', function(event) {
        console.error('Erreur capturée:', event.error);
        showError('Une erreur s\'est produite : ' + event.error.message);
    });
});
