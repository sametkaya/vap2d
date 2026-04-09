# VAP2D - Vessel Analysis Program for 2D Images

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://github.com/sametkaya/vap2d)

VAP2D is a **cross-platform**, open-source software for quantitative analysis of 2D vessel images. It enables automated detection of branch points and endpoints, calculation of vessel lengths and densities, and generation of detailed reports using both **Traditional Image Processing (TIP)** and **Deep Learning (DL)** methods.

## ✨ Features

- 🔬 **Vessel Analysis**: Detect branch points, endpoints, vessel paths, and calculate lengths/densities
- 🤖 **Dual Detection Methods**: Choose between Traditional Image Processing (TIP) or Deep Learning (DL)
- ⚙️ **Pre-processing Pipeline**: Noise removal, segmentation, and skeletonization
- 📊 **Report Generation**: Export results in CSV or PDF format
- 🖥️ **User-Friendly GUI**: Intuitive PySide6-based interface
- 🌐 **Cross-Platform**: Runs on Windows, Linux, and macOS
- 🐳 **Docker Support**: Easy deployment with containerized environment

---

## 📁 Repository Structure

```
VAP2D/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker configuration
├── LICENSE                 # GPL-3.0 license
├── README.md
│
├── DeepLearning/           # Deep Learning detection module
│   └── DeepLearningObjectDetection.py  # DL-based branch/endpoint detection
│
├── System/                 # Core image processing modules
│   ├── ImageOperation.py   # TIP methods (morphological filters, hit-or-miss)
│   ├── Skeletonize.py      # Medial axis transform for skeletonization
│   ├── Segmentation.py     # Threshold-based segmentation
│   └── Denoise.py          # Noise filtering algorithms
│
├── Windows/                # GUI window classes (PySide6)
│   ├── MainWindow.py       # Main application window
│   └── ...
│
├── GraphicItems/           # Custom Qt graphic items for visualization
│
├── Resources/              # Additional resources (icons, styles)
│
├── detectron2/             # Facebook's Detectron2 library
│                           # Pre-configured for Faster R-CNN object detection
│                           # Used by Deep Learning module
│
├── Sample_Data/            # 📂 SAMPLE DATASET FOR TESTING
│   └── HFHS13/             # Henry Ford Health System cerebral vessel images
│       ├── HFHS13_z00.tif  # 2D vessel slice images
│       ├── HFHS13_z01.tif
│       ├── HFHS13_z02.tif
│       └── ...             # (100 images total)
│
└── doc/
    └── screens/            # Application screenshots
```

### Key Components Explained

| Directory | Description |
|-----------|-------------|
| `System/ImageOperation.py` | **TIP Methods**: Contains morphological filters for detecting 8 branch point patterns and 16 endpoint patterns using hit-or-miss algorithm |
| `DeepLearning/` | **DL Methods**: Faster R-CNN model with hybrid post-processing for precise center localization |
| `detectron2/` | Facebook's object detection library, pre-configured for vessel detection task |
| `Sample_Data/HFHS13/` | **Test Dataset**: Cerebral vessel images from Henry Ford Health System for reproducibility testing |

---

## 📦 Sample Data

The repository includes the **HFHS13 dataset** containing 2D cerebral vessel images for testing and validation:

```
Sample_Data/
└── HFHS13/
    ├── HFHS13_z00.tif
    ├── HFHS13_z01.tif
    ├── HFHS13_z02.tif
    ├── ...
    └── HFHS13_z99.tif    (100 images total)
```

### Supported Input Formats

| Input Type | Description | Pre-processing Required |
|------------|-------------|------------------------|
| **Raw Images** | Grayscale vessel images (.tif, .png, .bmp, .jpg) | Yes (denoise → segment → skeletonize) |
| **Binary Skeleton** | Pre-skeletonized binary images | No (direct analysis) |

> **Note**: For best results, input images should be 8-bit grayscale. The software accepts both raw vessel images (requiring pre-processing) and pre-skeletonized binary images (ready for direct analysis).

---

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Pull and run with GUI support (Linux)
docker pull sametkaya/vap2d:v2.2
docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix sametkaya/vap2d:v2.2
```

### Option 2: Local Installation

```bash
# 1. Clone the repository
git clone https://github.com/sametkaya/vap2d.git
cd vap2d
```

```bash
# 2. Create virtual environment
python -m venv venv_vap2d
```

```bash
# 3. Activate virtual environment
# On Windows:
venv_vap2d\Scripts\activate

# On Linux/macOS:
source venv_vap2d/bin/activate
```

```bash
# 4. Install dependencies
pip install -r requirements.txt
```

```bash
# 5. Run the application
python main.py
```

---

## 📖 Quick Start Example Workflow

Here's a minimal example to analyze a vessel image using the sample data:

### Step 1: Load Sample Image
1. Click **"Load Image"** button
2. Navigate to: `Sample_Data/HFHS13/`
3. Select any image (e.g., `HFHS13_z00.tif`)

### Step 2: Pre-process (for raw images)
1. Click **"Denoise"** → Removes noise artifacts
2. Click **"Segment"** → Enhances vessel structures  
3. Click **"Skeletonize"** → Converts to binary skeleton

### Step 3: Analyze
1. Select detection method:
   - **"Img Processing"** → Traditional Image Processing (faster, no GPU needed)
   - **"Deep Learning"** → DL-based detection (more robust, GPU recommended)
2. Click **"Analyze"** button
3. View detected branch points (green) and endpoints (red)

### Step 4: Export Results
1. Click **"Report"** button
2. Choose CSV or PDF format
3. Results include: vessel count, lengths, densities, coordinates

---

## 🤖 Detection Methods

### Traditional Image Processing (TIP)
- **No GPU required** - runs on CPU
- Uses morphological hit-or-miss algorithm
- Detects 8 branch point patterns and 16 endpoint patterns
- **Best for**: Clean, high-contrast skeleton images
- **Location**: `System/ImageOperation.py`

### Deep Learning (DL)
- **GPU recommended** (NVIDIA CUDA 11.8+) but works on CPU
- Pre-trained Faster R-CNN model included
- Hybrid approach: DL detection + TIP post-processing for precise centers
- **Best for**: Noisy images, complex vessel structures
- **Location**: `DeepLearning/DeepLearningObjectDetection.py`

### Pre-trained Model Information

| Property | Value |
|----------|-------|
| Model | Faster R-CNN with ResNet-50 backbone |
| Performance | AP = 0.989 at IoU=0.50 |
| Training Data | COCO-format labeled vessel images |
| Retraining | Not required for standard vessel images |

> **Note**: For custom datasets with significantly different characteristics, retraining may improve results. See our publications [7, 8] for training procedures.

---

## 💻 System Requirements

### Minimum Requirements

| Component | Requirement |
|-----------|-------------|
| **OS** | Windows 10+, Ubuntu 20.04+, macOS 12+ |
| **RAM** | 4 GB |
| **Storage** | 500 MB |
| **Python** | 3.9+ |

### Recommended (for Deep Learning mode)

| Component | Requirement |
|-----------|-------------|
| **RAM** | 16 GB |
| **GPU** | NVIDIA GPU with CUDA 11.8+ |
| **Storage** | 2 GB |

> **Performance Note**: Deep Learning mode runs on CPU but is approximately 10x slower than GPU. For production use with DL method, an NVIDIA GPU is recommended.

---

## 🐳 Docker

### Docker Hub
- **Repository**: https://hub.docker.com/r/sametkaya/vap2d
- **Latest Version**: v2.2
- **Platforms**: Linux (AMD64, ARM64), Windows (via Docker Desktop)

### Platform-Specific Instructions

#### 🐧 Linux
```bash
docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix sametkaya/vap2d:v2.2
```

#### 🪟 Windows
1. Install [VcXsrv](https://sourceforge.net/projects/vcxsrv/)
2. Start with "Disable access control" enabled
3. Run:
```bash
docker run -e DISPLAY=host.docker.internal:0 sametkaya/vap2d:v2.2
```

#### 🍎 macOS
1. Install [XQuartz](https://www.xquartz.org/)
2. Enable "Allow connections from network clients"
3. Run:
```bash
docker run -e DISPLAY=host.docker.internal:0 sametkaya/vap2d:v2.2
```

---

## 📸 Screenshots

#### Load raw image
<img src="doc/screens/scrn1.png" alt="Load Image" width="400">

#### Denoising
<img src="doc/screens/scrn2.png" alt="Denoise" width="400">

#### Segmentation
<img src="doc/screens/scrn3.png" alt="Segment" width="400">

#### Analysis Results
<img src="doc/screens/scrn5.png" alt="Analyze" width="400">

#### Branch Points Detection
<img src="doc/screens/scrn6.png" alt="Branch Points" width="400">

#### Endpoints Detection
<img src="doc/screens/scrn7.png" alt="Endpoints" width="400">

#### Vessel Paths with Length Info
<img src="doc/screens/scrn8.png" alt="Vessel Paths" width="400">

#### Report Screen
<img src="doc/screens/scrn_report.png" alt="Report" width="400">

---

## 🛠️ Troubleshooting

### Common Issues

**Import errors:**
```bash
pip install -r requirements.txt --upgrade
```

**Deep Learning not working:**
- Ensure PyTorch is installed with CUDA support
- Check GPU: `python -c "import torch; print(torch.cuda.is_available())"`

**Docker GUI issues:**
- Linux: Run `xhost +local:docker` before starting container
- Windows: Ensure X server is running with access control disabled

---

## 🤝 Contributing

1. 🍴 Fork this repository
2. 🌿 Create a new branch: `git checkout -b feature/new-feature`
3. ✏️ Make your changes and commit: `git commit -m 'Add new feature'`
4. 📤 Push your branch: `git push origin feature/new-feature`
5. 🔄 Open a Pull Request

---

## 📚 Citation

If you use VAP2D in your research, please cite:

```bibtex
@article{vap2d2025,
  title={VAP2D: A Program for Quantitative Analysis of 2D Vessel Images},
  author={Kaya, Samet and Dik, Sümeyye Zülal and Kiraz, Berna},
  journal={Journal of Open Research Software},
  year={2025}
}
```

### Related Publications
- [Branch and End Points Detection using Deep Learning](https://doi.org/10.2339/politeknik.1492002) - Journal of Polytechnic, 2024
- [Hyperparameter Optimization for Vessel Detection](https://doi.org/10.1109/ASYU62119.2024.10757007) - IEEE ASYU, 2024

---

## 📄 License

This project is licensed under the [GNU General Public License v3.0](LICENSE).

---

## 📞 Contact & Support

- **Author**: Samet Kaya
- **Email**: skaya@fsm.edu.tr
- **GitHub Issues**: [Open an issue](https://github.com/sametkaya/vap2d/issues)
- **Institution**: Fatih Sultan Mehmet Vakıf University, Istanbul, Turkey

For questions, bug reports, or feature requests, please [open an issue](https://github.com/sametkaya/vap2d/issues) or contact via email.

---

## 🙏 Acknowledgements

This work was supported by the Fatih Sultan Mehmet Vakıf University Scientific Research Projects (SRP) Unit under grant number 22022B1Ç01D.

---

**VAP2D** - Making vessel analysis accessible, reproducible, and efficient.
