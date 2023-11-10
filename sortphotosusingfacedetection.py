# write a program to sort photos by persons using face detection and put them in folders named after respective persons
 
import os, shutil
import face_recognition

formats = [".jpg",".jpeg",".bmp",".webp"]

# directory containing photos with name of the persons as the filename
makeencodingdir = r"--path to the folder--"

# create a dictionary to store face encodings for each person
encodings = {}

# loop over named files so that face detection can learn its encodings and save it in a dictionary
for filename in os.listdir(makeencodingdir):
    photopath = os.path.join(makeencodingdir, filename)
    if os.path.isfile(photopath) and [i for i in formats if i in filename]:
        image = face_recognition.load_image_file(photopath)
        facelocations = face_recognition.face_locations(image)
        if facelocations:
            # Assuming there's only one person in each photo
            encoding = face_recognition.face_encodings(image, facelocations)[0]
            # Use the file name (person's name) as the key
            encodings[os.path.splitext(filename)[0]] = encoding

# Directory to store sorted photos
categoriseddir = r"--path to the folder--"

# test photos directory
tosortdir = r"--path to the folder--"

os.makedirs(categoriseddir, exist_ok=True)

# loop over the test photos directory and sort the photos
for filename in os.listdir(tosortdir):
    photopath = os.path.join(tosortdir, filename)
    if os.path.isfile(photopath) and [i for i in formats if i in filename]:
        image = face_recognition.load_image_file(photopath)
        facelocations = face_recognition.face_locations(image)
        if facelocations:
            encoding = face_recognition.face_encodings(image, facelocations)[0]
            for name, known_encoding in encodings.items():
                # Compare the current face encoding with the stored encodings
                match = face_recognition.compare_faces([known_encoding], encoding)
                if match[0]:
                    # Move the photo to the respective person's directory
                    persondir = os.path.join(categoriseddir, name)
                    os.makedirs(persondir, exist_ok=True)
                    shutil.copy(photopath, os.path.join(persondir, filename))

