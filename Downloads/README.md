# Tải ZIP bản port Unity/native

Các file sau có URL HTTPS thật. Không cần artifact của chat.

- [Actor thử nhanh — 5 MB](https://raw.githubusercontent.com/a002lamlam-ship-it/372dragon/unity-port-downloads-20261027/Downloads/UnityOriginalActors-Starter.zip)
- [Map và script Unity — 52 MB](https://raw.githubusercontent.com/a002lamlam-ship-it/372dragon/unity-port-downloads-20261027/Downloads/UnityMapPort.zip)
- [Source server + dữ liệu combat — 71 MB](https://raw.githubusercontent.com/a002lamlam-ship-it/372dragon/unity-port-downloads-20261027/Downloads/NativeServerChanges.zip)

## Tải toàn bộ art

Một số ZIP art vượt giới hạn file của GitHub nên được chia thành các phần nhị phân. Dùng script sau để tải, ghép lại thành ZIP gốc và kiểm SHA-256 tự động:

```bash
curl -fL https://raw.githubusercontent.com/a002lamlam-ship-it/372dragon/unity-port-downloads-20261027/Downloads/get-downloads.py -o get-downloads.py
python3 get-downloads.py --all --out DragonPort-Downloads
```

Không mở riêng file .part01/.part02. Script ghép chúng về ZIP gốc; các ZIP gốc được giải nén chung vào project Unity. Không sửa project Unity khi chỉ tải file.

Hướng dẫn import: [ART-COMBAT.md](ART-COMBAT.md).

| ZIP sau khi tải/ghép | MB | SHA-256 |
|---|---:|---|
| UnityOriginalActors-Starter.zip | 5.06 | `e4efceb09bb99e96d23ac3d095c84a076f2d2be0fbe94d79e51bb5e32593bb9a` |
| UnityMapPort.zip | 51.98 | `0e730a657ee920b388d383aa4d728e9ada8a150c20bbdba9a3c61763192b445a` |
| NativeServerChanges.zip | 70.64 | `271c50d4a2f69eee774f2d532a906819b1593d591f669d7beba1436eee18a189` |
| UnityOriginalArt-01.zip | 105.02 | `12ecb0a3638176db788d5db5ccfc12a4077fbef78c1d03191faa81a3a0a40a7e` |
| UnityOriginalArt-02.zip | 113.98 | `c26210c15abe10e4eeea048327e169fa153bd9844a5f65e60554e01aa17fce7a` |
| UnityOriginalArt-03.zip | 89.20 | `c23bec43439373f30c4b106778dd6dfcfee33d3100d747c53ba6237293383e93` |
| UnityOriginalArt-04.zip | 99.30 | `123baa67b0613ebe032f62dba66524be98b78a45ae9c01a86f94e92b72488283` |
| UnityOriginalArt-05.zip | 112.15 | `208ce9ea2f3f4e866d5c3d80a64122485ca84eafe439c3379a536cacfce0e0b9` |
| UnityOriginalArt-06.zip | 131.31 | `9c4b22dc3bc580e37d4d4465db5030c69174a4cf3a683caf0c2623bfe5769c2b` |
| UnityOriginalArt-07.zip | 106.02 | `7a977e07ec2edb3f90a79a5f60e10f7fa3396fa258711e0df868454fbb83a4f1` |
| UnityOriginalArt-08.zip | 97.96 | `1c9e3b0f6141762a9a7156c1219952c6ed2b3a253c58a65358aab56320018956` |
| UnityOriginalArt-09.zip | 104.77 | `f0d7092c5cadf9fec8d8242837c8b897ce555a87419619fcf58735d38a3d01c1` |
| UnityOriginalArt-10.zip | 100.24 | `7df8e499aa2f1c77c7a2fd731cef61c718c11e9cce6cb2dbfc261affc8c0208f` |
| UnityOriginalArt-11.zip | 95.13 | `310d7b42bd25a6dae2b6ee2ff13bbbe5602bcaaa253ac34b4324287f871cd7e0` |
| UnityOriginalArt-12.zip | 106.81 | `ac68bf8644e3549e30cc2c098fed61de109ca0b582a1da04f245f6aa40f71a9a` |
| UnityOriginalArt-13.zip | 108.47 | `2f80c48a205d3283f75950289c851abd9d28b20317328446d9d265f10d58509c` |
| UnityOriginalArt-14.zip | 105.33 | `785d89329e8088fcdf836d6392ca79dcbc9aa9d5e1d6da0ba932b3c0227901d5` |
| UnityOriginalArt-15.zip | 110.52 | `a2179acc2196ceaf6261a4170f2b0c29e42ea5a948ef43d946a2dfeb02c23696` |
| UnityOriginalArt-16.zip | 102.19 | `0a0a3e912e88dd06320c8921bea77e935b950996ca6fa436e5180f15dbfb349c` |
| UnityOriginalArt-17.zip | 90.62 | `846b1415a2f3e7815a31b5c1837db9ae3e7446fbe6434fd043e17bb43c041125` |
| UnityOriginalArt-18.zip | 92.79 | `f7a719bee3fa592c9714b383480980ec34cc28feb682e27f31f158141a8850fe` |
| UnityOriginalArt-19.zip | 106.14 | `23338e24f2752eaa36a3062ff5b20a0f9e05d2c0907f326d45626125ae8bf6cf` |
| UnityOriginalArt-20.zip | 95.95 | `00842f6784d89672178d4d82650be44fca165c8b479e0cdfdf12271fcb6d7d4a` |
| UnityOriginalArt-21.zip | 86.40 | `9c3d8a8070246ef81dae40d7f58c79ddd70ca6d3a56f3c9ac45a47df49ecaa40` |
| UnityOriginalArt-22.zip | 92.41 | `aed088cce0a59a1c9d25453ff8575835ffdd8fc7c08cc4e098205ec34046e54b` |
| UnityOriginalArt-23.zip | 48.22 | `6d20d180115072f9b735fad2d631c9b0079bf45e76ddb9f70cced305333353bf` |
