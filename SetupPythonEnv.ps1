# Define the path to the virtual environment directory
$envPath = "venv"

# Check if a Python interpreter is available
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python is not installed or not in your PATH. Please install Python and try again."
    exit 1
}

# Create a virtual environment
Write-Host "Creating virtual environment..."
python -m venv $envPath

# Check if the virtual environment was created successfully
if (-not (Test-Path $envPath)) {
    Write-Host "Failed to create the virtual environment. Please check your Python installation."
    exit 1
}

# Activate the virtual environment
Write-Host "Activating virtual environment..."
& .\venv\Scripts\Activate

# Check if requirements.txt exists
if (-Not (Test-Path "requirements.txt")) {
    Write-Host "No requirements.txt found. Please ensure it is in the current directory."
    exit 1
}

# Install the requirements
Write-Host "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Deactivate the virtual environment
Write-Host "Setup complete. Virtual environment is active."
