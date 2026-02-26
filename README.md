# PlantDoc Vision

Plant disease detection via leaf image analysis. Upload a photo and get a diagnosis with treatment recommendations.

---

## What this is
Deep learning system for plant disease detection built during a hackathon.
Trained MobileNetV2 on 226,000+ labeled leaf images — 99.6% validation accuracy.

## Security features
- Input validation and OpenCV-based image integrity checks
- Rate limiting (10 requests/minute per IP)
- Automated strike-based temporary IP bans for DoS mitigation
- Sanitized API responses to prevent data leakage
- Structured event logging and request analytics dashboard


## Requirements

**Python 3.11** (not 3.12+)
- https://www.python.org/downloads/release/python-3119/
- Check "Add Python to PATH" during install

**Microsoft Visual C++ Redistributable x64**
- https://aka.ms/vs/17/release/vc_redist.x64.exe
- Restart your PC after installing

---

## Installation
```bash
git clone https://github.com/CharifKati/plantdoc.git
cd plantdoc/code
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
uvicorn api:app --host 127.0.0.1 --port 8001
```

Open http://127.0.0.1:8001

---

## Running after first install
```bash
cd path\to\code
venv\Scripts\activate.bat
uvicorn api:app --host 127.0.0.1 --port 8001
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| No module named torch | Run the torch install command above |
| TensorFlow DLL error | Install VC++ Redistributable and restart |
| PowerShell blocks activation | Run: `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` |
| Fatal error in launcher | Delete venv folder and redo installation |
| Port in use | Change to `--port 8002` |

> Note: Training pipeline uses PyTorch (MobileNetV2).
> The Grad-CAM visualization module uses TensorFlow/Keras
> and was built during the hackathon as a separate diagnostic tool.

## Model weights and GitHub

The trained model weights (e.g. `plantdoc_model_base.pth`) are ~11MB and are small enough to keep in the repository if you prefer a self-contained project.

Recommended options:
- Commit the `*.pth` file directly (convenient for demos and small teams).
- Or host the weights on cloud storage and add a download link here if you prefer keeping the repo lightweight.

If you want to remove the file from git history later, use a history-rewriting tool such as the BFG or `git filter-repo`.
