import shutil
import os

SOURCE = "dataset_kaggle"   # dataset asli 6 kelompok
TARGET = "dataset"          # hasil extract untuk 2 kelompok (Segar & Busuk)

for split in ["train", "test"]:
    segar_dir = os.path.join(TARGET, split, "Segar")
    busuk_dir = os.path.join(TARGET, split, "Busuk")
    os.makedirs(segar_dir, exist_ok=True)
    os.makedirs(busuk_dir, exist_ok=True)

    split_path = os.path.join(SOURCE, split)
    if not os.path.exists(split_path):
        print(f"Folder tidak ditemukan: {split_path} (skip)")
        continue

    for folder in os.listdir(split_path):
        src = os.path.join(split_path, folder)
        if not os.path.isdir(src):
            continue

        if folder.lower().startswith("fresh"):
            dst = segar_dir
        elif folder.lower().startswith("rotten"):
            dst = busuk_dir
        else:
            print(f"Folder '{folder}' diabaikan (tidak dikenali)")
            continue

        count = 0
        for file in os.listdir(src):
            src_file = os.path.join(src, file)
            if os.path.isfile(src_file):
                # tambahkan prefix nama folder asal agar tidak ada nama file bertabrakan
                new_name = f"{folder}_{file}"
                shutil.copy(src_file, os.path.join(dst, new_name))
                count += 1

        print(f"Copied {count} file dari '{folder}' -> '{os.path.basename(dst)}' ({split})")

print("\nSelesai! Cek folder dataset/train dan dataset/test")
