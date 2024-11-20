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
example-known-multiple
├── Antony_John_Blinken
│   ├── Antony_John_Blinken.jpg
│   ├── Antony_John_Blinken1.jpg
│   └── Antony_John_Blinken2.jpg
├── Barack_Obama
│   ├── Barack_Obama.jpg
│   ├── Barack_Obama2.jpg
│   └── Barack_Obama3.jpg
├── Bill_Clinton
│   ├── Bill_Clinton.jpg
│   ├── Bill_Clinton1.jpg
│   └── Bill_Clinton2.jpg
├── Donald_John_Trump
│   ├── Donald_John_Trump.jpg
│   ├── Donald_John_Trump1.jpg
│   └── Donald_John_Trump2.jpg
├── Elon_Musk
│   ├── Elon_Musk.jpg
│   ├── Elon_Musk1.jpg
│   └── Elon_Musk2.jpg
├── Hillary_Clinton
│   ├── Hillary_Clinton.jpg
│   ├── Hillary_Clinton1.jpg
│   └── Hillary_Clinton2.jpg
├── Jensen_Huang
│   ├── Jensen_Huang.jpg
│   ├── Jensen_Huang1.jpg
│   └── Jensen_Huang2.jpg
├── Joe_Biden
│   ├── Joe_Biden.jpg
│   ├── Joe_Biden1.jpg
│   └── Joe_Biden2.jpg
├── Kamala_Harris
│   ├── Kamala_Harris.jpg
│   ├── Kamala_Harris1.jpg
│   └── Kamala_Harris2.jpg
├── Marco_Rubio
│   ├── Marco_Rubio.jpg
│   ├── Marco_Rubio1.jpg
│   └── Marco_Rubio2.jpg
├── Mark_Zuckerberg
│   ├── Mark_Zuckerberg.jpg
│   ├── Mark_Zuckerberg1.jpg
│   └── Mark_Zuckerberg2.jpg
├── Michelle_Obama
│   ├── Michelle_Obama.jpg
│   ├── Michelle_Obama1.jpg
│   └── Michelle_Obama2.jpg
├── Morris_Chang
│   ├── Morris_Chang.jpg
│   ├── Morris_Chang1.jpg
│   └── Morris_Chang2.jpg
├── Robyn_Rihanna
│   ├── Robyn_Rihanna.jpg
│   ├── Robyn_Rihanna1.jpg
│   └── Robyn_Rihanna2.jpg
├── Taylor_Swift
│   ├── Taylor_Swift.jpg
│   ├── Taylor_Swift1.jpg
│   └── Taylor_Swift2.jpg
├── Tim_Cook
│   ├── Tim_Cook.jpg
│   ├── Tim_Cook1.jpg
│   └── Tim_Cook2.jpg
├── beyonce
│   ├── beyonce.jpg
│   ├── beyonce1.jpg
│   └── beyonce2.jpg
├── 林百里
│   ├── 林百里.jpg
│   ├── 林百里2.jpg
│   └── 林百里3.jpg
├── 安倍晉三
│   ├── 安倍晉三.jpg
│   ├── 安倍晉三1.jpg
│   └── 安倍晉三2.jpg
└── 岸田文雄
    ├── 岸田文雄.jpg
    ├── 岸田文雄1.jpg
    └── 岸田文雄2.jpg
```

### Auto compare

```bash
python app_autorun.py
```

### stream video, identify multiple known people

```bash
python stream.py
```

## Other links

- [github: face_recognition](https://github.com/ageitgey/face_recognition)
- [基於python語言使用OpenCV搭配dlib實作人臉偵測與辨識](https://www.tpisoftware.com/tpu/articleDetails/950)
