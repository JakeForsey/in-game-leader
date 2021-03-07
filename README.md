

Setup

1. Update https://github.com/JaidedAI/EasyOCR

```
cd Builds
git clone https://github.com/JaidedAI/EasyOCR.git
```


Original requirements.txt
```
torch
torchvision>=0.5
opencv-python
scipy
numpy
Pillow
scikit-image
python-bidi
PyYAML
```

Updated requirements.txt
```
torch===1.7.1+cu110
torchvision===0.8.2+cu110
opencv-python
scipy
numpy
Pillow
scikit-image
python-bidi
PyYAML
```

2. Install dependencies

pipenv install

3. Run tests

```
(in-game-leader) \in-game-leader>python -m unittest
```