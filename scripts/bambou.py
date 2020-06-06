import numpy as np

nbPoints = 30
seuil = 10

data = np.random.randint(20,size=nbPoints)  # nbPoints données dans [0,20]
angles = np.arange(nbPoints)  # Des pseudo-angles
print(data)
dataSup10 = data < seuil  # tableau True,False des données < seuil  (proche(<seuil) : bambou, loin(>seuil) : rien càd passe entre les bambous)
# tableau des indices où il y a une transition True->False ou False->True (les bords des bambous)
transition = [x for x in range(1,nbPoints) if (dataSup10[x]==True and dataSup10[x-1]==False) or (dataSup10[x]==False and dataSup10[x-1]==True)]
print(transition)
# liste des intervalles [debutBambou,finBambou] et aussi [finBambou,debutBambou]
lesInterv = np.split(data,transition)
lesIntervAngle = np.split(angles,transition)
# uniquement la liste des intervalles [debutBambou,finBambou] càd des distances < seuil donc un intervalle = 1 bambou
if dataSup10[0] == True:  # Si on commenca par un bambou
    lesBambous = [lst for id,lst in enumerate(lesInterv) if id%2==0]
    lesAnglesDesBambous = [lst for id,lst in enumerate(lesIntervAngle) if id%2==0]
else:  # sinon, c'est que l'on était entre 2 lesBambous
    lesBambous = [lst for id,lst in enumerate(lesInterv) if id%2!=0]
    lesAnglesDesBambous = [lst for id,lst in enumerate(lesIntervAngle) if id%2!=0]
print(lesBambous)
print(lesAnglesDesBambous)
# calcul des distances moyennes pour chaque bambou
lesDistancesMoyennes = [np.mean(ar) for ar in lesBambous]
# et des angles moyens
lesAnglesMoyens = [np.mean(ar) for ar in lesAnglesDesBambous]
# Calcul des coord (X,Y) des centres des bambous à partir de leur coord polaire  ATTENTION : les angles doivent être en radian
coord = [(rayon*np.cos(angle), rayon*np.sin(angle)) for (rayon, angle) in zip(lesDistancesMoyennes, lesAnglesMoyens)]
print(coord)
# Et sous forme de 2 vecteurs (vecteur des X et vecteur des Y)
lesX = [rayon*np.cos(angle) for (rayon, angle) in zip(lesDistancesMoyennes, lesAnglesMoyens)]
lesY = [rayon*np.sin(angle) for (rayon, angle) in zip(lesDistancesMoyennes, lesAnglesMoyens)]
# Après, il faut faire un RANSAC avec lesX et lesY
# Doc de la fonction RANSAC ainsi qu'un exemple simple :  https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.RANSACRegressor.html
# Exemple plus complet avec comparaison avec une simple régression linéiare : https://scikit-learn.org/stable/auto_examples/linear_model/plot_ransac.html
