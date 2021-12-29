# Apix
Apix est un petit utilitaire très simple qui vise à rendre la lecture des fichiers de résultats des campagnes de positionnnement de la plateforme Pix/PixOrga plus aisée et agréable.
Le développement de cet utilitaire n'est en rien lié au GIP Pix et relève d'une initiative individuelle et personnelle. La marque Pix reste la propriété pleine et entière du GIP Pix.
### Dépendances et modules externes nécessaires
Apix a été écrit en Python 3. Il n'est pas compatible avec Python 2. 
Le développement et les tests ont été effectués avec Python 3.7.3.
Les modules externes suivants sont nécessaires:
* PyQt6 >= 6.1.0
* pyqt6-plugins >= 6.1.0.2.2
* PyQt6-Qt6 >= 6.2.2
* PyQt6-sip >= 13.2.0
* qt6-applications >= 6.1.0.2.2

Si vous souhaitez modifier la GUI d'Apix, deux modules supplémentaires sont recommandés:
* pyqt6-tools >= 6.1.0.3.2 - Ce module permet de pouvoir lancer le "_Designer_" Qt pour Python, un éditeur WYSIWYG
* qt6-tools >= 6.1.0.1.2 - Nécessaire pour que le module précédemment nommé fonctionne

### Récupération du code et installation
   #### Récupérer le code
Pour télécharger Apix, deux solutions s'ofrent à vous:
* Télécharger le code sous la forme d'une archive zip puis l'extraire dans un dossier de votre choix sur votre système
* Cloner le dépôt (depuis la ligne de commande):
  * `git clone https://github.com/SntPx/Apix /chemin/vers/dossier/`
  
   #### Installation
Il n'y a pas de processus d'installation d'Apix à proprement parler.
Il est toutefois nécessaire de télécharger et d'installer les modules externes nécessaires.
Pour ce faire, dans la ligne de commande, placez-vous dans le dossier accueillant Apix et lancez:
* `pip install -r ./requirements.txt`

Une fois que la commande pip se termine, vous pouvez lancer Apix, depuis la ligne de commande: `python3 apix.py`

   #### Lancement sous Windows
Vous pouvez lancer Apix sans passer par la ligne de commande, une fois l'installation des modules nécessaires faite, en double cliquant sur `apix.pyw`

### Captures d'écran
* Candidats ayant atteint le score minimal défini:
  ![alt Demo 1](https://act-now.fr/apix/Apix_Demo1.png)
  ![alt Demo 2](https://act-now.fr/apix/Apix_Demo2.png) 
  
* Candidats n'ayant pas atteint le score minimal défini:
  ![alt Demo 3](https://act-now.fr/apix/Apix_Demo3.png)
  ![alt Demo 4](https://act-now.fr/apix/Apix_Demo4.png)