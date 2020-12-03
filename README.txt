This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>

Informations:
	Software: Threshold of visual perception Experiment [TVPe]
	Version: 0.1.1
	Date: 03/12/2020
	Copyright 2020 Benjamin Borello

Changelogs:
	v0.1.1:
		-Ajout backward masking + forward masking
		-Ajout ISI (inter stimulus interval): T/2
		-Le mot apparaissant est désormais choisi aléatoirement parmi la liste contenu dans 'words.txt'
		-Bug empechant occasionellement l'affichage du mot et/ou du masque corrigé (pour le moment)

Utilisation:
	1.Le fichier 'words.txt' contient la liste des mots utilisés pendant l'experience, modifiez le à votre guise:
			<!> Attention à ne pas laisser de ligne vide <!>
	1'b.Si vous avez modifier la liste des mots alors que le programme est déjà lancé,
				allez dans les paramètres puis cliquez sur le bouton 'Recharger liste mots'.
	2.Démarrer l'experience
	3.Pendant l'experience:
		Le sujet doit presser la:
			touche <n> quand il a réussi à lire lire le mot
			touche <c> si il n'a pas réussi à lire le mot
	3.Fin de l'experience, retour au menu

Nouveau sujet:
	Faire attention au changement du numéro du sujet.
	Il n'est pas necessaire de re parametrer l'experience mais cela est tout de même possible.

<!> Limite technique: <!>
	Windows:
		-Précision de 16ms
	Linux:
		-Précision de 1ms

To do:
	-Verification quand S trouve le bon mot
	-Position aleatoire du mot à chaque apparition
	-Traitement des résultats, statistiques
