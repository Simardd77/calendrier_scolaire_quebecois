# Foire aux questions

## Installation et configuration

### Q : Comment installer l'intégration ?
**R :** Vous pouvez l'installer via HACS (recommandé) ou manuellement. Consultez le [README](README.md) pour les instructions détaillées.

### Q : Quelles versions de Home Assistant sont prises en charge ?
**R :** Home Assistant 2026.1.0 et versions ultérieures.

### Q : Ai-je besoin de logiciels supplémentaires ?
**R :** Pour les fonctionnalités OCR, il faut installer Tesseract. Les dépendances Python sont installées automatiquement.

## Configuration

### Q : Comment ajouter une source de calendrier ?
**R :** Utilisez le service `school_calendar_hub.add_source` ou l'interface du flux de configuration.

### Q : Quels formats de fichiers sont pris en charge ?
**R :** PDF, iCalendar (.ics) et sites web HTML.

### Q : Puis-je avoir plusieurs sources de calendrier ?
**R :** Oui ! Ajoutez autant de sources que nécessaire.

### Q : À quelle fréquence le rafraîchissement se produit-il ?
**R :** Par défaut, toutes les 1 heure. Vous pouvez modifier ce paramètre dans la configuration.

## Utilisation

### Q : Pourquoi mes événements n'apparaissent-ils pas ?
**R :**
1. Vérifiez que l'entité est disponible : `calendar.school_calendar_hub_*`
2. Activez le débogage et consultez les journaux
3. Essayez un rafraîchissement manuel : `school_calendar_hub.refresh_calendar`

### Q : Comment dépanner les problèmes d'analyse ?
**R :** Activez le débogage et vérifiez les journaux. Vous pouvez aussi utiliser manuellement le service `school_calendar_hub.parse_pdf`.

### Q : Que fait le mode d'apprentissage ?
**R :** Le moteur d'apprentissage analyse les événements extraits pour améliorer la précision des analyses futures. Plus il y a de données, meilleurs sont les résultats.

### Q : Puis-je entraîner le parseur manuellement ?
**R :** Oui, utilisez le service `school_calendar_hub.train_parser`.

## Dépannage

### Q : L'OCR ne fonctionne pas. Que faire ?
**R :** Assurez-vous que Tesseract est installé :
- **macOS** : `brew install tesseract`
- **Ubuntu** : `sudo apt-get install tesseract-ocr`
- **Windows** : Téléchargez depuis [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki)

### Q : L'intégration ne se charge pas. Quel est le problème ?
**R :**
1. Vérifiez la version de Home Assistant (2026.1.0+)
2. Consultez les journaux pour les erreurs spécifiques
3. Assurez-vous que toutes les dépendances sont installées
4. Redémarrez Home Assistant

### Q : L'analyse PDF est très lente
**R :** L'OCR peut être lent pour des PDF volumineux. Vous pouvez :
- Désactiver l'OCR si ce n'est pas nécessaire
- Diviser les gros PDF en fichiers plus petits
- Augmenter les ressources système

### Q : L'utilisation mémoire est élevée
**R :** Le moteur d'apprentissage stocke des échantillons. Pour réduire cela :
1. Désactivez le mode d'apprentissage si nécessaire
2. Effacez les données en cache manuellement
3. Redémarrez l'intégration

## Personnalisation

### Q : Puis-je créer un parseur personnalisé pour mon école ?
**R :** Oui ! Créez un parseur dans `custom_components/school_calendar_hub/engines/parsers/`.

### Q : Puis-je ajouter des sources spécifiques au Québec ?
**R :** Oui. Ajoutez des sources ciblées dans la configuration ou personnalisez le moteur de découverte.

### Q : Comment modifier les noms des entités ?
**R :** Les noms sont générés automatiquement à partir des noms des sources. Modifiez les noms des sources pour personnaliser les entités.

### Q : Puis-je l'utiliser sans OCR ?
**R :** Oui, désactivez l'OCR dans la configuration. L'intégration utilisera l'extraction de texte et la correspondance de motifs.

## Performance et optimisation

### Q : Comment améliorer la précision de l'analyse ?
**R :**
1. Utilisez des parseurs spécifiques pour votre école
2. Activez le mode d'apprentissage
3. Fournissez plus d'exemples de calendriers
4. Augmentez le volume de données d'entraînement

### Q : Puis-je synchroniser avec d'autres instances de Home Assistant ?
**R :** Actuellement, chaque instance fonctionne indépendamment. La synchronisation nécessiterait un service externe.

## Développement

### Q : Puis-je contribuer ?
**R :** Oui ! Consultez [DEVELOPMENT.md](DEVELOPMENT.md) pour les directives.

### Q : Comment signaler des bogues ?
**R :** Créez un problème sur [GitHub Issues](https://github.com/yourusername/ha-school-calendar-hub/issues).

### Q : Comment demander des fonctionnalités ?
**R :** Utilisez [GitHub Discussions](https://github.com/yourusername/ha-school-calendar-hub/discussions).

## Avancé

### Q : Puis-je l'utiliser avec des automatisations ?
**R :** Oui ! Déclenchez des automatisations à partir de :
- événements de calendrier
- valeurs de capteurs (prochain événement, compteur, état)
- capteurs binaires (école ouverte, congé, événement du jour)

### Q : Puis-je sauvegarder ma configuration ?
**R :** La configuration est stockée dans Home Assistant. Utilisez la fonction de sauvegarde intégrée.

### Q : Comment supprimer complètement l'intégration ?
**R :** Allez dans Paramètres → Appareils et services, sélectionnez l'intégration, puis cliquez sur Supprimer.

## Support

Pour plus d'aide :
- 📚 [Documentation complète](School_Calendar_Hub_Documentation_Pack/README.md)
- 🐛 [Signaler un problème](https://github.com/yourusername/ha-school-calendar-hub/issues)
- 💬 [Discussions](https://github.com/yourusername/ha-school-calendar-hub/discussions)
- 📧 Assistance par email disponible
