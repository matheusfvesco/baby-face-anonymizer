from pathlib import Path
import argparse

def main(images_path, labels_path, output_path, train_ratio):
    images_path = Path(images_path)
    labels_path = Path(labels_path)
    output_path = Path(output_path)

    total_labels = list(labels_path.glob("*.txt"))
    total_images = [images_path / f"{label.stem}.png" for label in total_labels]

    num_train = int(len(total_labels) * train_ratio)
    train_labels = total_labels[:num_train]
    train_images = total_images[:num_train]
    val_labels = total_labels[num_train:]
    val_images = total_images[num_train:]

    train_output = output_path / "train"
    train_images_output = train_output / "images"
    train_labels_output = train_output / "labels"
    train_output.mkdir(parents=True, exist_ok=True)
    train_images_output.mkdir(parents=True, exist_ok=True)
    train_labels_output.mkdir(parents=True, exist_ok=True)

    val_output = output_path / "val"
    val_images_output = val_output / "images"
    val_labels_output = val_output / "labels"
    val_output.mkdir(parents=True, exist_ok=True)
    val_images_output.mkdir(parents=True, exist_ok=True)
    val_labels_output.mkdir(parents=True, exist_ok=True)

    # symlinks images and labels
    for image, label in zip(train_images, train_labels):
        image_out = train_images_output / image.name
        label_out = train_labels_output / label.name
        image_out.symlink_to(image.resolve())
        label_out.symlink_to(label.resolve())

    for image, label in zip(val_images, val_labels):
        image_out = val_images_output / image.name
        label_out = val_labels_output / label.name
        image_out.symlink_to(image.resolve())
        label_out.symlink_to(label.resolve())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("images_root")
    parser.add_argument("labels_root")
    parser.add_argument("output_root")
    parser.add_argument("--train_ratio", type=float, default=0.8)
    args = parser.parse_args()

    images_path = Path(args.images_root)
    labels_path = Path(args.labels_root)
    output_path = Path(args.output_root)
    main(images_path, labels_path, output_path, args.train_ratio)