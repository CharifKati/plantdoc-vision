import os
import cv2
from tqdm import tqdm
import albumentations as A


aug = A.Compose(
    [
        A.RandomResizedCrop(
            size=(224, 224),
            scale=(0.8, 1.0),
            ratio=(0.75, 1.33),
        ),
        A.HorizontalFlip(p=0.5),
        A.RandomBrightnessContrast(p=0.2),
    ]
)


def augment_folder(src_dir: str, dst_dir: str, copies: int = 5) -> None:
    """
    Walk `src_dir`, augment each image and save results under `dst_dir`,
    preserving the relative sub-folder layout. A progress bar is shown for
    each directory.
    """
    for root, _, files in os.walk(src_dir):
        rel = os.path.relpath(root, src_dir)
        target = os.path.join(dst_dir, rel)
        os.makedirs(target, exist_ok=True)

        for fname in tqdm(files, desc=rel, unit="file"):
            if not fname.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
                continue
            in_path = os.path.join(root, fname)
            img = cv2.imread(in_path)
            if img is None:
                continue  # skip broken files

            base, ext = os.path.splitext(fname)
            # copy the original
            cv2.imwrite(os.path.join(target, fname), img)

            for i in range(copies):
                out_img = aug(image=img)["image"]
                out_name = f"{base}_aug{i}{ext}"
                cv2.imwrite(os.path.join(target, out_name), out_img)


if __name__ == "__main__":
    src = "merged_dataset"
    dst = "merged_dataset_aug"
    if os.path.abspath(src) == os.path.abspath(dst):
        raise ValueError("source and destination must be different")
    augment_folder(src, dst, copies=3)