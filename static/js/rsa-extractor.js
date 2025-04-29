/**
 * RSA-extractor.js - Script pour l'extraction des facteurs d'une clé RSA
 * Gère l'interface utilisateur et les appels API pour analyser les clés RSA
 */

document.addEventListener('DOMContentLoaded', function() {
    const keyTypeSelector = document.getElementById('key-type');
    const keyInput = document.getElementById('key-input');
    const analyzeBtn = document.getElementById('analyze-btn');
    const keyInfoBox = document.getElementById('key-info');
    const vulnerabilityInfoBox = document.getElementById('vulnerability-info');
    const factorsInfoBox = document.getElementById('factors-info');
    const loadingIndicator = document.getElementById('loading-indicator');
    
    // Options d'analyse
    const commonFactorsCheck = document.getElementById('check-common-factors');
    const fermatCheck = document.getElementById('check-fermat');
    const smallExponentCheck = document.getElementById('check-small-exponent');
    const sharedPrimesCheck = document.getElementById('check-shared-primes');

    // Événement pour le bouton d'analyse
    analyzeBtn.addEventListener('click', function() {
        const keyContent = keyInput.value.trim();
        
        // Validation de l'entrée
        if (!keyContent) {
            showError('Veuillez entrer une clé RSA ou un modulus à analyser.', 'key-info');
            return;
        }

        // Préparer les données pour l'API
        const requestData = {
            keyType: keyTypeSelector.value,
            keyContent: keyContent,
            options: {
                checkCommonFactors: commonFactorsCheck.checked,
                useFermat: fermatCheck.checked,
                checkSmallExponent: smallExponentCheck.checked,
                checkSharedPrimes: sharedPrimesCheck.checked
            }
        };

        // Afficher l'indicateur de chargement
        loadingIndicator.classList.remove('hidden');
        keyInfoBox.classList.add('hidden');
        vulnerabilityInfoBox.classList.add('hidden');
        factorsInfoBox.classList.add('hidden');

        // Temps de début pour mesurer la performance
        const startTime = Date.now();

        // Appel à l'API pour analyser la clé RSA
        fetch('/api/analyze-rsa', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erreur lors de l\'analyse de la clé RSA. Vérifiez votre entrée.');
            }
            return response.json();
        })
        .then(data => {
            // Masquer l'indicateur de chargement
            loadingIndicator.classList.add('hidden');
            keyInfoBox.classList.remove('hidden');
            vulnerabilityInfoBox.classList.remove('hidden');
            factorsInfoBox.classList.remove('hidden');

            // Afficher les résultats
            displayRSAAnalysisResults(data);

            // Afficher le temps d'exécution
            const executionTime = showExecutionTime(startTime);
            
            // Afficher les méthodes utilisées
            const methodsUsedElement = document.getElementById('methods-used');
            if (methodsUsedElement && data.methodsUsed) {
                methodsUsedElement.textContent = data.methodsUsed.join(', ');
            }
        })
        .catch(error => {
            // Masquer l'indicateur de chargement
            loadingIndicator.classList.add('hidden');
            keyInfoBox.classList.remove('hidden');
            
            // Afficher l'erreur
            showError('Erreur: ' + error.message, 'key-info');
        });
    });

    // Fonction pour afficher les résultats de l'analyse RSA
    function displayRSAAnalysisResults(data) {
        if (!data.success) {
            keyInfoBox.innerHTML = `
                <h4>Informations sur la clé</h4>
                <p class="error-message" style="color: var(--accent-color);">
                    Échec de l'analyse: ${data.error || 'Une erreur inconnue s\'est produite.'}
                </p>`;
            return;
        }

        // Afficher les informations sur la clé
        keyInfoBox.innerHTML = `
            <h4>Informations sur la clé</h4>
            <table class="info-table">
                <tr>
                    <td><strong>Type de clé:</strong></td>
                    <td>${data.keyType}</td>
                </tr>
                <tr>
                    <td><strong>Taille de la clé:</strong></td>
                    <td>${data.keySize} bits</td>
                </tr>
                <tr>
                    <td><strong>Modulus (N):</strong></td>
                    <td><code title="${data.modulus}">${formatBigNumber(data.modulus)}</code></td>
                </tr>
                <tr>
                    <td><strong>Exposant public (e):</strong></td>
                    <td>${data.publicExponent}</td>
                </tr>
            </table>`;

        // Afficher les vulnérabilités
        if (data.vulnerabilities && data.vulnerabilities.length > 0) {
            let vulnHTML = `<h4>Vulnérabilités détectées</h4><ul class="vulnerability-list">`;
            data.vulnerabilities.forEach(vuln => {
                vulnHTML += `
                    <li>
                        <strong>${vuln.name}</strong>
                        <p>${vuln.description}</p>
                        <p><em>Risque: ${vuln.severity}</em></p>
                    </li>`;
            });
            vulnHTML += `</ul>`;
            vulnerabilityInfoBox.innerHTML = vulnHTML;
        } else {
            vulnerabilityInfoBox.innerHTML = `
                <h4>Vulnérabilités détectées</h4>
                <p>Aucune vulnérabilité connue n'a été détectée.</p>`;
        }

        // Afficher les facteurs s'ils ont été trouvés
        if (data.factorsFound) {
            let factorsHTML = `<h4>Facteurs extraits</h4>`;
            factorsHTML += `
                <div>
                    <p><strong>p</strong> = <code title="${data.p}">${formatBigNumber(data.p)}</code></p>
                    <p><strong>q</strong> = <code title="${data.q}">${formatBigNumber(data.q)}</code></p>
                </div>
                <div class="extra-info">
                    <p><strong>Factorisation vérifiée:</strong> ${data.p * data.q === data.modulus ? 'Oui' : 'Non'}</p>
                    <p><strong>Méthode utilisée:</strong> ${data.factorizationMethod}</p>
                </div>`;
            
            if (data.privateExponent) {
                factorsHTML += `
                    <div class="key-components">
                        <p><strong>Exposant privé (d):</strong> <code title="${data.privateExponent}">${formatBigNumber(data.privateExponent)}</code></p>
                    </div>`;
            }
            
            factorsInfoBox.innerHTML = factorsHTML;
        } else {
            factorsInfoBox.innerHTML = `
                <h4>Facteurs extraits</h4>
                <p>La factorisation du modulus n'a pas réussi avec les méthodes disponibles.</p>
                <p>La clé pourrait être sécurisée contre les attaques de factorisation connues.</p>`;
        }
    }

    // Fonction pour afficher le temps d'exécution
    function showExecutionTime(startTime) {
        const endTime = Date.now();
        const executionTime = (endTime - startTime) / 1000; // en secondes
        
        const timeElement = document.getElementById('execution-time');
        if (timeElement) {
            timeElement.textContent = executionTime.toFixed(2) + ' secondes';
        }
        
        return executionTime;
    }

    // Fonction pour formater un grand nombre
    function formatBigNumber(num) {
        if (typeof num !== 'string') {
            num = num.toString();
        }
        
        if (num.length <= 20) {
            return num;
        }
        
        // Afficher les premiers et derniers chiffres avec "..." au milieu
        return num.substring(0, 10) + '...' + num.substring(num.length - 10);
    }

    // Fonction pour afficher une erreur
    function showError(message, elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = `
                <div class="error-box">
                    <i class="fas fa-exclamation-circle"></i>
                    <p>${message}</p>
                </div>`;
            element.classList.remove('hidden');
        }
    }

    // Gestion des options avancées (affichage/masquage)
    const advancedOptionsToggle = document.getElementById('toggle-advanced-options');
    const advancedOptionsPanel = document.getElementById('advanced-options');
    
    if (advancedOptionsToggle && advancedOptionsPanel) {
        advancedOptionsToggle.addEventListener('click', function() {
            if (advancedOptionsPanel.classList.contains('hidden')) {
                advancedOptionsPanel.classList.remove('hidden');
                advancedOptionsToggle.innerHTML = '<i class="fas fa-chevron-up"></i> Masquer les options avancées';
            } else {
                advancedOptionsPanel.classList.add('hidden');
                advancedOptionsToggle.innerHTML = '<i class="fas fa-chevron-down"></i> Afficher les options avancées';
            }
        });
    }
    
    // Gestion du bouton de copie des facteurs
    const copyFactorsBtn = document.getElementById('copy-factors');
    if (copyFactorsBtn) {
        copyFactorsBtn.addEventListener('click', function() {
            const factorsText = document.querySelectorAll('#factors-info code');
            if (factorsText.length > 0) {
                let textToCopy = '';
                factorsText.forEach(factor => {
                    textToCopy += factor.getAttribute('title') + '\n';
                });
                
                navigator.clipboard.writeText(textToCopy.trim())
                    .then(() => {
                        const originalText = copyFactorsBtn.textContent;
                        copyFactorsBtn.innerHTML = '<i class="fas fa-check"></i> Copié!';
                        setTimeout(() => {
                            copyFactorsBtn.innerHTML = originalText;
                        }, 1500);
                    })
                    .catch(err => {
                        console.error('Erreur lors de la copie:', err);
                    });
            }
        });
    }
    
    // Gestion de la soumission du formulaire
    const rsaForm = document.getElementById('rsa-form');
    if (rsaForm) {
        rsaForm.addEventListener('submit', function(e) {
            e.preventDefault();
            analyzeBtn.click();
        });
    }
    
    // Support pour le glisser-déposer des fichiers
    const dropZone = document.getElementById('key-dropzone');
    if (dropZone && keyInput) {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, preventDefaults, false);
        });
        
        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }
        
        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, highlight, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, unhighlight, false);
        });
        
        function highlight() {
            dropZone.classList.add('highlight');
        }
        
        function unhighlight() {
            dropZone.classList.remove('highlight');
        }
        
        dropZone.addEventListener('drop', handleDrop, false);
        
        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            
            if (files.length > 0) {
                const file = files[0];
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    keyInput.value = e.target.result;
                };
                
                reader.readAsText(file);
            }
        }
    }
});
