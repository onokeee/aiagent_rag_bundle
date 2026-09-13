# -*- coding: utf-8 -*-
"""スクレイピングのサンプル（ダミー）。

「取り込み」画面の「スクレイピングで取得する」は、このフォルダ（scrapers/）直下の
.py を別プロセスで実行し、fetch(out_dir) が out_dir に書いた Excel／CSV を表に取り込みます。
取得したファイルはサーバに残しません（表に入れたら消します）。

このファイルはインターネットに出ず、その場で作ったダミーの表を書くだけです。
動作確認と、自分のスクリプトを書くときの雛形に使ってください。

約束は1つだけ:

    def fetch(out_dir):        # out_dir は pathlib.Path。ここにファイルを書く
        ...
        return out_dir / "xxx.xlsx"   # 戻り値は任意（アプリは out_dir の中身を見る）

  ・書けるのは .xlsx / .xlsm / .csv / .tsv / .txt。複数書いてよい（登録時にどれを使うか選ぶ）
  ・ファイル名が毎回変わる（日付入りなど）場合でも、1つしか出来ていなければそれが使われる
  ・失敗は例外を投げるだけでよい。メッセージは管理画面と管理者メールにそのまま出る
  ・print した内容は、失敗したときの説明に末尾だけ添えられる
  ・時間の上限（タイムアウト）は登録ごとに画面で決める（既定5分）

実際にサイトから取るときは requests / selenium などを、アプリと同じ Python 環境に
入れて使います。例:

    import requests
    def fetch(out_dir):
        r = requests.get("https://example.com/export/daily.xlsx", timeout=60)
        r.raise_for_status()
        (out_dir / "daily.xlsx").write_bytes(r.content)

ファイル名の先頭が _ のものは部品扱いで画面に出ません（共通処理を _common.py に
置いて import する、といった使い方ができます）。
"""
import random
from datetime import date, timedelta


def fetch(out_dir):
    import pandas as pd

    # 日ごとに少しだけ値が変わるようにして、「全件入れ替え」で表が更新される様子が
    # 分かるようにしてある（乱数の種が日付なので、同じ日に何度実行しても同じ）
    today = date.today()
    rng = random.Random(today.toordinal())
    sites = ["第1工場", "第2工場", "物流センター"]
    rows = []
    for i in range(14):
        d = today - timedelta(days=13 - i)
        for s in sites:
            rows.append({
                "日付": d.isoformat(),
                "拠点": s,
                "気温": round(rng.uniform(12.0, 31.0), 1),
                "湿度": rng.randint(35, 85),
                "電力使用量": rng.randint(800, 2400),
            })
    daily = pd.DataFrame(rows)
    by_site = (daily.groupby("拠点", as_index=False)
                    .agg(平均気温=("気温", "mean"), 電力合計=("電力使用量", "sum")))
    by_site["平均気温"] = by_site["平均気温"].round(1)

    # Excel（シート2枚）と CSV の両方を書く。登録時にどちらを使うか選べる
    xlsx = out_dir / "ダミー観測.xlsx"
    with pd.ExcelWriter(xlsx) as w:
        daily.to_excel(w, sheet_name="日次", index=False)
        by_site.to_excel(w, sheet_name="拠点別", index=False)
    daily.to_csv(out_dir / "ダミー観測.csv", index=False, encoding="utf-8-sig")
    print(f"{len(daily)} 行を書きました: {xlsx.name}")
    return xlsx
