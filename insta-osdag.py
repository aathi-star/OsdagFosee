import subprocess
import sys
import os
from pathlib import Path

def run_command(command):
    """Run a shell command and return the result."""
    import subprocess
    return subprocess.run(command, shell=True)


def cleanup_miktex():
    """Remove MiKTeX repository if it exists."""
    print("Cleaning up MiKTeX repository...")
    try:
        # Remove the MiKTeX repository file if it exists
        run_command("sudo rm -f /etc/apt/sources.list.d/miktex.list")
        # Update package lists after removal
        run_command("sudo apt-get update")
        print("MiKTeX repository cleanup complete.")
    except Exception as e:
        print(f"Error during cleanup: {e}")
        sys.exit(1)

def install_curl():
    """Check and install Curl."""
    print("Checking for Curl...")
    try:
        result = subprocess.run(["curl", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            print("Curl is already installed.")
        else:
            print("Curl not found. Installing Curl...")
            run_command("sudo apt-get update && sudo apt-get install -y curl")
            print("Curl installation complete.")
    except FileNotFoundError:
        print("Curl command not found, proceeding with installation.")
        run_command("sudo apt-get update && sudo apt-get install -y curl")
        print("Curl installation complete.")

def install_texlive():
    """Check and install basic TeX Live."""
    print("Checking for TeX Live...")
    try:
        result = subprocess.run(["pdflatex", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            print("TeX Live is already installed.")
        else:
            print("TeX Live not found. Installing basic TeX Live...")
            run_command("sudo apt-get update")
            run_command("sudo apt-get install -y texlive")
            print("TeX Live installation complete.")
    except FileNotFoundError:
        print("TeX Live command not found, proceeding with installation.")
        run_command("sudo apt-get update")
        run_command("sudo apt-get install -y texlive")
        print("TeX Live installation complete.")

def install_miniconda():
    """Check and install Miniconda."""
    print("Checking for Miniconda...")
    try:
        result = subprocess.run(["conda", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            print("Miniconda is already installed.")
        else:
            print("Miniconda not found. Downloading and installing Miniconda...")
            miniconda_url = "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
            run_command(f"curl -o Miniconda3-latest-Linux-x86_64.sh {miniconda_url}")
            run_command(f"bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda3")
            os.environ["PATH"] = f"{os.path.expanduser('~')}/miniconda3/bin:" + os.environ["PATH"]
            print("Miniconda installed.")
    except FileNotFoundError:
        print("Conda command not found, proceeding with installation.")
        miniconda_url = "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
        run_command(f"curl -o Miniconda3-latest-Linux-x86_64.sh {miniconda_url}")
        run_command(f"bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda3")
        os.environ["PATH"] = f"{os.path.expanduser('~')}/miniconda3/bin:" + os.environ["PATH"]
        print("Miniconda installed.")

def setup_conda_environment():
    """Set up the Conda environment and install Osdag."""
    print("Setting up Conda environment for Osdag...")
    try:
        # Directly add Conda paths to the script environment
        conda_bin_path = f"{os.path.expanduser('~')}/miniconda3/bin"
        os.environ["PATH"] = conda_bin_path + ":" + os.environ["PATH"]
        print(f"Conda path added to environment: {conda_bin_path}")

        # Create the Conda environment
        print("Creating the Conda environment...")
        run_command(f"{conda_bin_path}/conda create -n osdag-env osdag::osdag -c conda-forge -y")
        print("Conda environment 'osdag-env' created successfully.")

        # Activate the environment
        print("Activating Conda environment 'osdag-env'...")
        run_command(f"{conda_bin_path}/conda activate osdag-env")

        # Install Mamba
        print("Installing Mamba...")
        run_command(f"{conda_bin_path}/conda install -n osdag-env mamba -y")
        print("Mamba installation complete.")

        # Use Mamba to install Osdag
        print("Installing Osdag using Mamba...")
        run_command(f"{conda_bin_path}/mamba install -n osdag-env osdag::osdag -c conda-forge -y")
        print("Osdag installation complete.")
    except Exception as e:
        print(f"Error during Conda environment setup: {e}")
        sys.exit(1)

def create_launcher_script():
    """Create a shell script to launch Osdag."""
    launcher_path = Path.home() / "Desktop" / "Launch_Osdag.sh"
    launcher_content = (
        "#!/bin/bash\n"
        "source ~/miniconda3/bin/activate\n"
        "conda activate osdag-env\n"
        "osdag\n"
    )
    with open(launcher_path, "w") as f:
        f.write(launcher_content)
    launcher_path.chmod(0o755)
    print(f"Launcher script created at: {launcher_path}")

if __name__ == "__main__":
    print("Starting automated installation...")
    cleanup_miktex()  # Added cleanup step
    install_curl()
    install_texlive()
    install_miniconda()
    setup_conda_environment()
    create_launcher_script()
    print("Installation complete!")

