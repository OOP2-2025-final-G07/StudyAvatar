

 


  

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


# Study Avatar

勉強時間と教科を記録し、勉強時間、教科によって、キャラクターの見た目が変わるアプリ。メインは、勉強時間記録機能。サブ機能で育成機能。 

## 概要
**Study Avatar** は、日々の勉強時間を記録し、その成果を「アバターの進化」として視覚化する学習管理アプリケーションです。
単なる記録ツールではなく、学習量や教科の偏りに応じてパートナーであるアバターが姿を変えることで、ユーザーの継続的なモチベーションをサポートします。
Flask をベースとしたバックエンドと、Chart.js を用いた科学的な分析機能を備えています。

## アピールポイント



## 各機能の説明


### ■ 勉強タイマー
* 教科（理系・文系）とタイトルを選択して計測スタート。
* 計測中はパートナーのアバターがメッセージで応援し、集中力を高める。

### ■ 進捗ダッシュボード
* **今日のパートナー**: 現在のアバター画像と、リアルタイムの進捗ゲージを表示します。
* **学習ログ**: 最新5件の記録をトップページから素早く確認できる。

### ■ 設定管理
* 進化の難易度設定の切り替えや、直近7日間分のアバターレベルの一括再計算が可能。
  

### ■ デバックモード
* 　app.pyの　if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
  を
  app.pyの　if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)に変更することで、
  デバックモードを解放できる

## 使い方

1.  **環境構築**
    仮想環境を作成し、必要なライブラリをインストールします。
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install Flask peewee
    ```

2.  **起動**
    `app.py` を実行して、ブラウザでアクセスします。
    ```bash
    python app.py
    ```
    起動後、ブラウザで `http://localhost:8080` を開いてください。

## 作業分担


| 学籍番号・氏名 | 作業内容 |
|--------------|--------|
| [K24017 伊藤源太](https://github.com/tanukiponta) | 見た目 |
| [K24031 海老原巧翔](https://github.com/ebiharaaa0909) | 勉強データの集計 |
| [K24071 佐々木 知哉](https://github.com/to-sasaki333) | 勉強データの登録処理、時間計測の処理 |
| [K24084 鷲見叶芽](https://github.com/KanameSumi) | キャラクターデザインと管理 |
