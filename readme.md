## usages

### identify one unknown image

```bash
python app.py
```

this scripts provide two ways to identify unknown person image

#### one picture model

Only one known image is needed, the model directory structure is like this:

```bash
known
├── biden.png
├── celeba-11.jpg
├── celeba-20.jpg
├── celeba-30.jpg
├── celeba-50.jpg
```

#### multiple picture model

Multiple known images are needed, the model directory structure is shown as below. This will provide better accuracy

```bash
known-multiple
├── biden
│   └── biden_1.png
│   └── biden_2.png
│   └── biden_3.png
├── celeba-11
│   └── celeba-10_1.jpg
│   └── celeba-10_2.jpg
│   └── celeba-10_3.jpg
├── celeba-20
│   └── celeba-20_1.jpg
│   └── celeba-20_2.jpg
│   └── celeba-20_3.jpg
├── celeba-30
│   └── celeba-30_1.jpg
│   └── celeba-30_2.jpg
│   └── celeba-30_3.jpg
├── celeba-50
│   └── celeba-50_1.jpg
│   └── celeba-50_2.jpg
│   └── celeba-50_3.jpg
```

### stream video, identify multiple known people

```bash
python stream.py
```

## Other links

- [github: face_recognition](https://github.com/ageitgey/face_recognition)
- [基於python語言使用OpenCV搭配dlib實作人臉偵測與辨識](https://www.tpisoftware.com/tpu/articleDetails/950)
