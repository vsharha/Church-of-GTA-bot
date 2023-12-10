import os
import cv2
import hurry.filesize as h


def write_frames(file_name, n):
    capture = cv2.VideoCapture(file_name)

    dir_name = create_dir()
    print("Saving to", dir_name)

    while True:
        success, image = capture.read()

        if not success:
            print("Error")
            break

        current_frame_id = capture.get(cv2.CAP_PROP_POS_FRAMES)
        file_path = os.path.join(dir_name, f"frame{current_frame_id}.jpg")
        cv2.imwrite(file_path, image)

        capture.set(cv2.CAP_PROP_POS_FRAMES, current_frame_id + n-1)
        print(f"{current_frame_id}")

    print(len(os.listdir(dir_name)), "files")
    print(get_dir_size(dir_name))


def create_dir():
    id = 1
    while True:
        dir_name = f"vid{id}/"
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            break
        id += 1
    return dir_name


def get_dir_size(dir_name):
    size_bytes = 0

    for path, dirs, files in os.walk(dir_name):
        for f in files:
            file_path = os.path.join(path, f)
            size_bytes += os.path.getsize(file_path)

    return h.size(size_bytes)


if __name__ == "__main__":
    while True:
        while True:
            file_name = input("File name > ")
            if os.path.exists(file_name):
                break
            print("Directory doesn't exist")

        try:
            n = int(input("Capture every nth frame > "))
        except ValueError:
            n = 20

        write_frames(file_name, n)

        op = input("Another video? [Y/N] > ").casefold() or "y"

        if op != "y":
            break
