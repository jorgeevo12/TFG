import os
import subprocess

def download_multiwoz(data_dir="data"):
    """Clona el repositorio MultiWOZ si no existe."""
    if not os.path.exists(os.path.join(data_dir, "multiwoz")):
        os.makedirs(data_dir, exist_ok=True)
        subprocess.run([
            "git", "clone", 
            "https://github.com/budzianowski/multiwoz.git",
            os.path.join(data_dir, "multiwoz")
        ])
    else:
        print("MultiWOZ ya está descargado.")

if __name__ == "__main__":
    download_multiwoz()