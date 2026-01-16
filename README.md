# StudyAvatar
勉強時間と教科を記録し、勉強時間、教科によって、キャラクターの見た目が変わるアプリ。メインは、勉強時間記録機能。サブ機能で育成機能。 

## テーマ    



## アピールポイント  


  
## 作業分担

| 学籍番号・氏名 | 作業内容 |
|--------------|--------|
| k24017 伊藤源太 | 見た目 |
| k24031 海老原巧翔 | 勉強データの集計 |
| [K24071 佐々木 知哉](https://github.com/to-sasaki333) | 勉強データの登録処理、時間計測の処理 |
| [K24084 鷲見叶芽](https://github.com/KanameSumi) | キャラクターデザインと管理 |

## 動作条件: require


```bash
python 3.13.7

# python lib
Flask==3.1.2
peewee==3.18.3

# frontend lib (CDN)
Chart.js
```

## 使い方: usage
　　
以下のようにapp.pyを実行し、ブラウザから下記のUPLにアクセスしてください。

```bash
$ python app.py
# Try accessing "http://localhost:8080" in your browser.
```
(※環境によっては python3 app.py と入力してください)
