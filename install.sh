#!/bin/bash
# Guide d'installation pour Calendrier Scolaire Québécois

echo "==============================================="
echo "Calendrier Scolaire Québécois - Guide d'installation"
echo "==============================================="
echo ""

# Vérification de la version Python
echo "1. Vérification de la version Python..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "   ✓ Python $python_version trouvé"
echo ""

# Vérification de Home Assistant
echo "2. Préparation pour Home Assistant..."
echo "   - Copiez custom_components/school_calendar_hub dans ~/.homeassistant/custom_components/"
echo "   - Ou installez via HACS : https://github.com/yourusername/ha-school-calendar-hub"
echo ""

# Installation des dépendances
echo "3. Installation des dépendances..."
pip install -r custom_components/school_calendar_hub/requirements.txt 2>/dev/null || echo "   - Installez via le gestionnaire de paquets de Home Assistant"
echo ""

# Optionnel : installation des dépendances de dev
echo "4. Pour le développement :"
echo "   pip install -r requirements-dev.txt"
echo "   pytest tests/"
echo ""

# Configuration
echo "5. Configuration :"
echo "   - Allez dans Home Assistant : Paramètres → Appareils et services → Intégrations"
echo "   - Recherchez 'Calendrier Scolaire Québécois'"
echo "   - Cliquez sur 'Créer une intégration'"
echo "   - Suivez le flux de configuration"
echo ""

# Vérification
echo "6. Vérification :"
echo "   - Vérifiez les entités : Outils de développement → État"
echo "   - Recherchez : calendar.school_calendar_hub_*"
echo "   - Recherchez : sensor.school_calendar_hub_*"
echo "   - Recherchez : binary_sensor.school_calendar_hub_*"
echo ""

echo "==============================================="
echo "✓ Installation terminée !"
echo "==============================================="
echo ""
echo "Prochaines étapes :"
echo "1. Ajoutez votre première source de calendrier"
echo "2. Vérifiez les journaux pour d'éventuelles erreurs"
echo "3. Personnalisez les paramètres de l'intégration"
echo "4. Créez des automatisations basées sur les événements"
echo ""
echo "Documentation : voir README.md et DEVELOPMENT.md"
echo "==============================================="
