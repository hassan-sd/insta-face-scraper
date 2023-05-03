import os
import sys
import cv2
import dlib
import instaloader
import face_recognition
from typing import List
import face_recognition
from sklearn.cluster import DBSCAN
from PIL import Image
import numpy as np

def get_usernames(input_data: str) -> List[str]:
    if os.path.isfile(input_data):
        with open(input_data, "r") as f:
            usernames = [line.strip() for line in f.readlines()]
    else:
        usernames = [input_data]
    return usernames

def download_images(username: str, max_images: int = 50):
    loader = instaloader.Instaloader(
        dirname_pattern=username,
        filename_pattern="{mediaid}.jpg",  # Save images with .jpg extension
        download_pictures=True,
        download_videos=False,  # Don't download videos
        download_video_thumbnails=False,
        download_geotags=False,
        download_comments=False,
        save_metadata=False,  # Don't save metadata files
        compress_json=False,
        post_metadata_txt_pattern=""
    )

    profile = instaloader.Profile.from_username(loader.context, username)
    posts = profile.get_posts()

    count = 0
    for post in posts:
        if count >= max_images:
            break

        if post.is_video:
            continue  # Skip video posts

        loader.download_post(post, target=username)
        count += 1

    # Remove any extra files (e.g., txt, json.xz) that might have been saved
    for filename in os.listdir(username):
        if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
            file_path = os.path.join(username, filename)
            os.remove(file_path)

def detect_and_save_faces(username: str, output_dir: str = "faces"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    image_files = [f for f in os.listdir(username) if f.lower().endswith((".jpg", ".jpeg", ".png"))]

    face_encodings = []
    face_locations = []
    face_image_paths = []

    for image_file in image_files:
        image_path = os.path.join(username, image_file)
        image = cv2.imread(image_path)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        current_face_locations = face_recognition.face_locations(rgb_image, model="hog")

        current_face_encodings = face_recognition.face_encodings(rgb_image, current_face_locations)

        face_encodings.extend(current_face_encodings)
        face_locations.extend(current_face_locations)
        face_image_paths.extend([image_path] * len(current_face_locations))

    if not face_encodings:
        print(f"No faces detected in {username} images.")
        return

    clustering_model = DBSCAN(eps=0.5, min_samples=2, metric="euclidean")
    labels = clustering_model.fit_predict(face_encodings)

    padding = 50
    for label, face_location, image_path in zip(labels, face_locations, face_image_paths):
        top, right, bottom, left = face_location

        top = max(top - padding, 0)
        left = max(left - padding, 0)
        bottom = min(bottom + padding, rgb_image.shape[0])
        right = min(right + padding, rgb_image.shape[1])

        image = cv2.imread(image_path)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        face_image = rgb_image[top:bottom, left:right]

        face_image_pil = Image.fromarray(face_image)
        width, height = face_image_pil.size

        min_size = 768
        if width < min_size or height < min_size:
            new_width = max(min_size, width)
            new_height = max(min_size, height)
            aspect_ratio = float(width) / float(height)
            
            if width < height:
                new_width = int(new_height * aspect_ratio)
            else:
                new_height = int(new_width / aspect_ratio)
            
            face_image_pil = face_image_pil.resize((new_width, new_height), Image.ANTIALIAS)
            face_image = np.array(face_image_pil)

        person_dir = os.path.join(username, output_dir, f"person_{label}")

        os.makedirs(person_dir, exist_ok=True)

        output_filename = f"{os.path.splitext(os.path.basename(image_path))[0]}_face.jpg"
        output_filepath = os.path.join(person_dir, output_filename)

        cv2.imwrite(output_filepath, cv2.cvtColor(face_image, cv2.COLOR_RGB2BGR))


if __name__ == "__main__":
    input_data = input("Enter a profile username or a path to a text file with usernames: ")
    max_photos = int(input("Enter the number of photos to download per profile: "))
    usernames = get_usernames(input_data)

    for username in usernames:
        print(f"Downloading images from {username}...")
        download_images(username, max_photos)
        print(f"Extracting faces from {username}'s images...")
        detect_and_save_faces(username)
        print(f"Done processing {username}!")
