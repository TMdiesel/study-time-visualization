# Google Colaboratoryを用いた実行方法
[Google Colaboratory](https://colab.research.google.com/notebooks/welcome.ipynb?hl=ja)はブラウザからPythonを実行できるGoogleのサービスです。

## 手順
下記手順でsample画像を出力できます。
1. リポジトリをダウンロードする。
1. `Colab_Notebooks`をGoogle Driveのマイドライブ上にアップロードする。
2. [Google Colaboratory](https://colab.research.google.com/notebooks/welcome.ipynb?hl=ja)にアクセスして、Google Driveにアップロードした`Colab_Notebooks`内の`main.ipynb`を開く。
3. 全てのセルを実行する。

実際に使う際は下記手順を行ってください。
1. 勉強時間を記録したcsvファイルを用意して、`Colab_Notebooks`内に保存する。  
    `sample.csv`と同じ形式でcsvファイルを作成してください。
    各行には左から`日付,タスク番号,開始時間,終了時間,メモ`を書きます。
1. `main.ipynb`内の2つ目のセルにて、filename(読み込むcsvファイルの名前)、task_dict(タスク番号とタスクの対応関係)、savename(出力する画像の名前)を指定する。
3. 全てのセルを実行する。
