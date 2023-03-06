from sklearn.cluster import DBSCAN
from imutils import build_montages
import numpy as np
import argparse
import pickle
import cv2


ap = argparse.ArgumentParser()
ap.add_argument('-e', '--encodings', required=True, help='path to serialized db of facial encodings')
ap.add_argument('-j', '--jobs', type=int, default=-1, help='# of parallel jobs to run (-1 will use all CPUs)')
args = vars(ap.parse_args())


print('[INFO] loading encodings...')
data = pickle.loads(open(args['encodings'], 'rb').read())
data = np.array(data)
encodings = [d['encoding'] for d in data]


# cluster the embeddings
print('[INFO] clustering...')
clt = DBSCAN(metric='euclidean', n_jobs=args['jobs'])
clt.fit(encodings)

# determine the total number of unique faces found in the dataset
labelIDs = np.unique(clt.labels_)
numUniqueFaces = len(np.where(labelIDs > -1)[0])
print(f'[INFO] # unique faces: {numUniqueFaces}')

# loop over the unique face integers
for labelID in labelIDs:
    print(f'[INFO] faces for face ID: {labelID}')
    idxs = np.where(clt.labels_ == labelID)[0]
    idxs = np.random.choice(idxs, size=min(25, len(idxs)), replace=False)

    faces = []
    for i in idxs:
        image = cv2.imread(data[i]['imagePath'])
        (top, right, bottom, left) = data[i]['loc']
        face = image[top:bottom, left:right]
        face = cv2.resize(face, (96, 96))
        faces.append(face)
        
    montage = build_montages(faces, (96, 96), (5, 5))[0]
    title = f'Face ID #{labelID}'
    title = 'Unknown Faces' if labelID == -1 else title
    cv2.imshow(title, montage)
    cv2.waitKey(0)