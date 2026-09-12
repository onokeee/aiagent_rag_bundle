"""assets.py — 画面の素材（HTML・CSS・JS）。

このファイルにはロジックが1行も無い。中身は次の2つの辞書だけ:

  TEMPLATES     … Jinja2 のテンプレート12本。core.py の create_app が
                   DictLoader(TEMPLATES) で読む。
  STATIC_FILES  … css/app.css と js/app.js。core.py の /static/<path> が
                   ETag を付けて配る。

core.py から分けてあるのは、ここが 900,000字あって
（core.py 全体のほぼ半分。うち help.html だけで 465,000字）、
ヘルプの文言を1行直すだけでコード本体の差分になってしまうため。
分けても配り方は変わらない（core.py が import して使う）。

編集するときの注意:
  ・文字列は raw 文字列（r 付きの三重引用符）で囲んである。
    中のバックスラッシュは正規表現やJSのエスケープとしてそのまま生きるので、
    囲みを外さないこと。
  ・ヘルプ（help.html）の第5部は raw ブロックで囲ってある。Jinja が
    評価しない範囲なので、その中に if を書いても効かない。
    表示を出し分けたいときは raw ブロックの外側で囲うこと。
  ・js/app.js と css/app.css を直したら、画面の見た目だけでなく
    検証スクリプト（t6_static / t15_er_bind / t18_ui_guards）も通すこと。
"""

TEMPLATES = {

# --- _icons.html ---
"_icons.html": r"""{# 線画アイコン。絵文字の代わりにこれを使う。

   使い方:  {% raw %}{{ icon('chat') }}   {{ icon('save', 'icon--sm') }}{% endraw %}
   JS から:  iconSvg('save')  （common.js）

   輪郭だけの24pxグリッドで統一し、色は currentColor に従わせる。
   新しく足すときは同じ画風（stroke のみ・塗りなし）を守ること。 #}

{% macro icon(name, cls='') -%}
<svg class="icon {{ cls }}" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-{{ name }}"/></svg>
{%- endmacro %}

<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <defs>
    <symbol id="i-chat" viewBox="0 0 24 24">
      <path d="M21 12a8 8 0 0 1-8 8H7l-4 3v-6.5A8 8 0 0 1 11 4h2a8 8 0 0 1 8 8Z"/>
    </symbol>
    <symbol id="i-catalog" viewBox="0 0 24 24">
      <path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v18H6.5A2.5 2.5 0 0 1 4 18.5Z"/>
      <path d="M4 18.5A2.5 2.5 0 0 1 6.5 16H20"/>
    </symbol>
    <symbol id="i-database" viewBox="0 0 24 24">
      <ellipse cx="12" cy="5.5" rx="7.5" ry="2.8"/>
      <path d="M4.5 5.5v6c0 1.55 3.36 2.8 7.5 2.8s7.5-1.25 7.5-2.8v-6"/>
      <path d="M4.5 11.5v6c0 1.55 3.36 2.8 7.5 2.8s7.5-1.25 7.5-2.8v-6"/>
    </symbol>
    <symbol id="i-book" viewBox="0 0 24 24">
      <path d="M4 5.2A2.2 2.2 0 0 1 6.2 3H12v16H6.2A2.2 2.2 0 0 0 4 21.2Z"/>
      <path d="M20 5.2A2.2 2.2 0 0 0 17.8 3H12v16h5.8A2.2 2.2 0 0 1 20 21.2Z"/>
    </symbol>
    <symbol id="i-model" viewBox="0 0 24 24">
      <rect x="4.5" y="4.5" width="15" height="15" rx="4"/>
      <circle cx="12" cy="12" r="3.2"/>
    </symbol>
    <symbol id="i-mail" viewBox="0 0 24 24">
      <rect x="3" y="5" width="18" height="14" rx="2.5"/>
      <path d="m3.6 6.8 7.3 5.2a2 2 0 0 0 2.2 0l7.3-5.2"/>
    </symbol>
    <symbol id="i-spark" viewBox="0 0 24 24">
      <path d="M12 3.2 13.9 9l5.8 1.9-5.8 1.9L12 18.6l-1.9-5.8L4.3 11l5.8-1.9Z"/>
      <path d="M18.5 3.5v3M20 5h-3"/>
    </symbol>
    <symbol id="i-save" viewBox="0 0 24 24">
      <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2Z"/>
      <path d="M7 3v6h8M8 21v-6h8v6"/>
    </symbol>
    <symbol id="i-undo" viewBox="0 0 24 24">
      <path d="M8.5 14 4 9.5 8.5 5"/><path d="M4 9.5h10a5.25 5.25 0 0 1 0 10.5H11"/>
    </symbol>
    <symbol id="i-redo" viewBox="0 0 24 24">
      <path d="m15.5 14 4.5-4.5L15.5 5"/><path d="M20 9.5H10a5.25 5.25 0 0 0 0 10.5h3"/>
    </symbol>
    <symbol id="i-filter" viewBox="0 0 24 24">
      <path d="M4 5.5h16l-6.2 7.3v5.4l-3.6 2v-7.4Z"/>
    </symbol>
    <symbol id="i-x" viewBox="0 0 24 24"><path d="M6 6l12 12M18 6 6 18"/></symbol>
    <symbol id="i-maximize" viewBox="0 0 24 24">
      <path d="M8 3H5a2 2 0 0 0-2 2v3M16 3h3a2 2 0 0 1 2 2v3M8 21H5a2 2 0 0 1-2-2v-3M16 21h3a2 2 0 0 0 2-2v-3"/>
    </symbol>
    <symbol id="i-minimize" viewBox="0 0 24 24">
      <path d="M8 3v3a2 2 0 0 1-2 2H3M21 8h-3a2 2 0 0 1-2-2V3M3 16h3a2 2 0 0 1 2 2v3M16 21v-3a2 2 0 0 1 2-2h3"/>
    </symbol>
    <symbol id="i-alert" viewBox="0 0 24 24">
      <path d="M10.3 4 2.9 17a2 2 0 0 0 1.7 3h14.8a2 2 0 0 0 1.7-3L13.7 4a2 2 0 0 0-3.4 0Z"/>
      <path d="M12 9v4.5M12 17h.01"/>
    </symbol>
    <symbol id="i-trash" viewBox="0 0 24 24">
      <path d="M4 7h16M9.5 7V5a1 1 0 0 1 1-1h3a1 1 0 0 1 1 1v2"/>
      <path d="M6.5 7 7.4 19a2 2 0 0 0 2 1.9h5.2a2 2 0 0 0 2-1.9L17.5 7"/>
    </symbol>
    <symbol id="i-file" viewBox="0 0 24 24">
      <path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8Z"/>
      <path d="M14 3v5h5"/>
    </symbol>
    <symbol id="i-folder" viewBox="0 0 24 24">
      <path d="M3 7.5A2 2 0 0 1 5 5.5h3.6a2 2 0 0 1 1.5.7l1.2 1.4H19a2 2 0 0 1 2 2v7.9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z"/>
    </symbol>
    <symbol id="i-image" viewBox="0 0 24 24">
      <rect x="3.5" y="4.5" width="17" height="15" rx="2.5"/>
      <circle cx="9" cy="10" r="1.6"/><path d="m4.5 17.5 5-4.5 4 3.3 3-2.3 3.5 3"/>
    </symbol>
    <symbol id="i-user" viewBox="0 0 24 24">
      <circle cx="12" cy="8" r="4"/><path d="M4.5 20.5a7.5 7.5 0 0 1 15 0"/>
    </symbol>
    <symbol id="i-back" viewBox="0 0 24 24"><path d="M19 12H5M11 6l-6 6 6 6"/></symbol>
    <symbol id="i-down" viewBox="0 0 24 24"><path d="m6 9.5 6 6 6-6"/></symbol>
    <symbol id="i-chart" viewBox="0 0 24 24">
      <path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>
    </symbol>
  <symbol id="i-help" viewBox="0 0 24 24">
      <circle cx="12" cy="12" r="9"/><path d="M9.6 9.2a2.4 2.4 0 1 1 3.3 2.3c-.7.3-.9.8-.9 1.6M12 16.6h.01"/>
    </symbol>
  <symbol id="i-table" viewBox="0 0 24 24">
      <rect x="3.5" y="4.5" width="17" height="15" rx="2"/>
      <path d="M3.5 9.5h17M9.5 9.5v10"/>
    </symbol>
    <symbol id="i-tool" viewBox="0 0 24 24">
      <path d="M14.5 6.5a4 4 0 0 1 5.2 5.2l-8 8a2.5 2.5 0 0 1-3.6-3.6l8-8"/>
      <path d="m9 9-5.2 5.2a3 3 0 0 0 4.2 4.2"/>
    </symbol>
  </defs>
</svg>
""",

# --- base.html ---
"base.html": r"""{% from "_icons.html" import icon %}<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{% block title %}{{ app_title }}{% endblock %}</title>
{# タブのアイコン。無いとブラウザが /favicon.ico を取りに来て 404 がログに残り続ける #}
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 24 24%27%3E%3Cellipse cx=%2712%27 cy=%275.5%27 rx=%277.5%27 ry=%272.8%27 fill=%27none%27 stroke=%27%23b8552f%27 stroke-width=%271.8%27/%3E%3Cpath d=%27M4.5 5.5v6c0 1.55 3.36 2.8 7.5 2.8s7.5-1.25 7.5-2.8v-6M4.5 11.5v6c0 1.55 3.36 2.8 7.5 2.8s7.5-1.25 7.5-2.8v-6%27 fill=%27none%27 stroke=%27%23b8552f%27 stroke-width=%271.8%27/%3E%3C/svg%3E">
<link rel="stylesheet" href="{{ url_for('static', filename='css/app.css') }}">
</head>
<body class="{% block body_class %}{% endblock %}">
{% include "_icons.html" %}
<div class="layout">
  <aside class="sidebar" id="sidebar">
    {# 管理者以外はチャットしか使えないので、行き先が1つだけのメニューは出さない。
       URLを直に叩かれても admin_required で止まるので、ここは見た目の整理。 #}
    {# 各画面が何をする所かは data-desc に持たせ、マウスを乗せたときに出す。
       画面の上に固定で置くと、毎回読むものでもないのに場所だけ取り続けるため。
       吹き出しは body 直下に描かれるので、サイドバーの幅で切れない。 #}
    {% if user.is_admin %}
    <div class="sidebar__section">
      <a class="navlink {{ 'is-active' if nav.startswith('chat.') }}" href="{{ url_for('chat.index') }}"
         data-desc="データについて日本語で質問すると、AIがSQLを書いて答えます。">
        {{ icon('chat') }} チャット</a>
      <a class="navlink {{ 'is-active' if nav.startswith('catalog.') or nav.startswith('imp.') }}" href="{{ url_for('catalog.index') }}"
         data-desc="データとテーブルの説明・結合・用語・例文・ツール・取り込み。ここに書いた内容がそのまま AI の理解になります。">
        {{ icon('catalog') }} データカタログ</a>
      <a class="navlink {{ 'is-active' if nav.startswith('knowledge.') }}" href="{{ url_for('knowledge.index') }}"
         data-desc="社内文書を検索するナレッジベース（LightRAG）の接続先を登録します。ここに書いた説明が、AIがどのナレッジベースを調べるかの判断材料になります。">
        {{ icon('book') }} ナレッジベース</a>
      <a class="navlink {{ 'is-active' if nav.startswith('models.') }}" href="{{ url_for('models.index') }}"
         data-desc="チャット画面で選べるモデルを決めます。">
        {{ icon('model') }} モデル設定</a>
      <a class="navlink {{ 'is-active' if nav.startswith('mail.') }}" href="{{ url_for('mail.index') }}"
         data-desc="送信サーバ・差出人・送ってよい宛先を決めます。">
        {{ icon('mail') }} メール設定</a>
      <a class="navlink {{ 'is-active' if nav.startswith('usage.') }}" href="{{ url_for('usage.index') }}"
         data-desc="このアプリの使われ方の集計（管理者だけ）。">
        {{ icon('chart') }} 利用状況</a>
    </div>
    {% endif %}
    <div class="sidebar__section">
      {# 上の「チャット」は管理者限定の囲みの中にある。一般利用者は
         ヘルプやテーブル画面を開くと、戻る道が無くなってしまうのでここにも置く #}
      {% if not user.is_admin %}
      <a class="navlink {{ 'is-active' if nav.startswith('chat.') }}" href="{{ url_for('chat.index') }}"
         data-desc="データについて日本語で質問すると、AIがSQLを書いて答えます。">
        {{ icon('chat') }} チャット</a>
      {% endif %}
      <a class="navlink {{ 'is-active' if nav.startswith('help.') }}" href="{{ url_for('help.index') }}"
         data-desc="全機能の説明書と、システム構成の説明。">
        {{ icon('help') }} ヘルプ</a>
    </div>

    {% block sidebar %}{% endblock %}

    <div class="spacer"></div>
    <div class="sidebar__section">
      <div class="sidebar__user">{{ icon('user', 'icon--sm') }}
        <span>{{ user.display_name or user.username }}</span></div>
      <div class="small muted mb">{{ user.username }}{% if user.groups %}／{{ user.groups|join(', ') }}{% endif %}</div>
      <form method="post" action="{{ url_for('auth.logout') }}">
        <button class="btn btn--sm" style="width:100%">ログアウト</button>
      </form>
    </div>
  </aside>

  {# サイドバーの境目。ドラッグで幅を変え、クリックで折りたたむ。 #}
  <div class="resizer" id="sidebarResizer" role="separator" tabindex="0"
       aria-label="サイドバーの幅を変える"
       data-tip="クリックして折りたたむ　ドラッグしてサイズ変更"
       data-tip-open="クリックして開く　ドラッグしてサイズ変更"></div>

  <div class="main">
    {# 見出しを持たない画面では、その場所ごと出さない。空の見出しを置くと
       そのぶん本文が下がるだけになる。画面の説明はサイドバーの項目に
       マウスを乗せると出る（data-desc）。 #}
    {% set _h = self.heading() | trim %}
    {% set _s = self.subheading() | trim %}
    {% if _h or _s %}
    <header class="topbar">
      <div>
        {% if _h %}<h1>{% block heading %}{% endblock %}</h1>{% endif %}
        {% if _s %}<div class="sub">{% block subheading %}{% endblock %}</div>{% endif %}
      </div>
    </header>
    {% endif %}
    {% block body %}{% endblock %}
  </div>
</div>

<div class="toasts" id="toasts"></div>
{% block scripts %}{% endblock %}
{# 統合スクリプト（旧 common/er/manage/各画面JS）。画面の window.* 変数を
   見て自分の画面のぶんだけ動くので、必ずインライン変数より後に読む #}
<script src="{{ url_for('static', filename='js/app.js') }}"></script>
</body>
</html>
""",

# --- catalog.html ---
"catalog.html": r"""{% extends "base.html" %}
{% from "_icons.html" import icon %}
{% block title %}データカタログ — {{ app_title }}{% endblock %}
{# 見出しは置かない。画面の説明はサイドバーの項目にマウスを乗せると出る #}


{% block body %}
<div class="content content--wide">
{% if not target %}
  <div class="empty">
    <div class="empty__icon">{{ icon('database') }}</div>
    <div>データがまだ取り込まれていません。</div>
    <div class="mt"><a class="btn btn--primary" href="{{ url_for('imp.index') }}">データを取り込む</a></div>
  </div>
{% else %}

  {% for w in drift %}<div class="alert alert--warn">{{ w }}</div>{% endfor %}

  {# タブ・充実度・DB選択を1本の帯にまとめる。段を分けるとそれだけで
     縦を60px以上使い、いちばん見たいテーブル一覧が画面から押し出される。
     充実度はクリックでそのタブへ移動する（テーブル説明は未記入だけに絞って開く）。 #}
  <div class="tabs tabs--bar">
    <button class="tab is-active" data-pane="tables">テーブル</button>
    <button class="tab" data-pane="er">結合・ER図</button>
    <button class="tab" data-pane="glossary">用語集・例文</button>
    <button class="tab" data-pane="tools">ツール</button>
    <button class="tab" data-pane="views">ビュー</button>
    <a class="tab" href="{{ url_for('imp.index') }}">取り込み</a>

    <div class="tabs__end">
      <div class="metrics metrics--inline">
        <button class="metric metric--link" data-jump="tables" data-filter="missing"
                title="クリックで、説明が未記入のテーブルだけを表示">
          <div class="metric__label">テーブル説明</div>
          <div class="metric__value" id="mTables">{{ coverage.tables[0] }}/{{ coverage.tables[1] }}</div></button>
        <button class="metric metric--link" data-jump="tables" title="クリックでテーブル一覧へ">
          <div class="metric__label">列の説明</div>
          <div class="metric__value" id="mCols">{{ coverage.columns[0] }}/{{ coverage.columns[1] }}</div></button>
        <button class="metric metric--link" data-jump="er" title="クリックで結合・ER図へ">
          <div class="metric__label">結合定義</div>
          <div class="metric__value">{{ coverage.relationships }}</div></button>
        <button class="metric metric--link" data-jump="glossary" data-sec="gl" title="クリックで用語集へ">
          <div class="metric__label">用語集</div>
          <div class="metric__value" id="mGloss">{{ coverage.glossary }}</div></button>
        <button class="metric metric--link" data-jump="glossary" data-sec="ex" title="クリックで例文へ">
          <div class="metric__label">例文</div>
          <div class="metric__value" id="mEx">{{ coverage.examples }}</div></button>
      </div>
    </div>
  </div>

  <!-- ================= DB・テーブル ================= -->
  <div class="tabpane is-active" id="pane-tables">
    {# 定期取り込みの全体状態（DBに紐づかない）。スケジューラが止まっているときの警告と、
       対象テーブルが無くなった設定の始末。正常なら何も出ない。中身は manage.js が描く #}
    <div id="schedBanner"></div>
    <div id="orphanJobs"></div>

    {# 「データ全体の説明」欄は置かない。全体に書いた文章は表の入れ替えに
       追随できず腐るので、複数の表にまたがる前提は各まとまりのメモに書く。
       ここにはデータ全体の規模（サイズ・更新日）の1行だけ出す（manage.js が書く） #}
    <div class="small muted mb" id="dbManageInfo">読み込み中…</div>

    {# 目当てのテーブル・列を探すための道具。説明や実際の値の中身も検索対象 #}
    <div class="row mb" style="align-items:center">
      <input type="text" id="tblFilter" style="max-width:320px"
             placeholder="テーブル・列・説明・実際の値で絞り込み">
      <button class="btn btn--sm" id="tblMissing"
              title="テーブルの説明が空のものだけを表示">説明なしだけ</button>
      <div class="spacer"></div>
      <button class="btn btn--ghost btn--sm" id="tblOpenAll">すべて開く</button>
      <button class="btn btn--ghost btn--sm" id="tblCloseAll">すべて閉じる</button>
    </div>
    <div class="small muted mb hidden" id="tblFilterInfo"></div>
    {# 表名「元DB名__表名」の規約があるときは元DBごとに折りたたむ（114表対策）。
       規約に沿わないDBでは従来どおりのフラット一覧になる #}
    {% for g in table_groups %}
    {% if grouped and g.key %}
    <details class="acc acc--group" data-group="{{ g.key }}">
      <summary>
        <strong>{{ g.key }}</strong>
        <span class="muted small">{{ g.tables|length }}テーブル</span>
        {% if g.memo %}<span class="badge badge--ok">メモあり</span>{% endif %}
      </summary>
      <div class="acc__body">
        {# まとまりのメモ（複数の表にまたがる前提）と、名前の変更。
           まとまりの名前は表名の接頭辞そのもの。
           メモは、このまとまりの表を選んでいるときだけAIに渡る #}
        <div class="row mb gmemo" data-group="{{ g.key }}">
          <div class="grow">
            <label class="field">このまとまりのメモ
              <span class="muted" style="font-weight:400">— 複数の表にまたがる前提・決めごと（例: 指標の定義、記録の範囲）。この中の表を使うときだけAIに渡ります</span></label>
            <textarea class="g-memo" rows="2">{{ g.memo }}</textarea>
            <div class="mt row" style="gap:6px">
              <button class="btn btn--sm btn--primary g-save">保存</button>
              <button class="btn btn--sm g-check" {{ 'disabled' if not llm_ready }}
                      title="いま書かれている内容がデータと合っているかをAIに確かめさせます。&#10;文章は書き換えません（指摘が出るだけです）">AIに点検させる</button>
            </div>
            <div class="gcheck mt hidden"></div>
          </div>
          <div style="flex:none;width:200px">
            <label class="field" title="まとまりの名前は表名の接頭辞そのもの。変えると配下の全テーブルが改名されます（説明・関連・用語・例文・検算は引き継がれます）">名前</label>
            <div class="row" style="gap:6px">
              <input type="text" class="g-key" value="{{ g.key }}" style="min-width:0">
              <button class="btn btn--sm g-rename" title="配下の全テーブルを新しい名前で改名します">変更</button>
            </div>
          </div>
        </div>
    {% endif %}
    {% for t in g.tables %}
    <details class="acc" data-table="{{ t.name }}">
      <summary>
        <strong>{{ t.name }}</strong>
        {% if t.is_view %}<span class="badge" title="実体を持たないビュー。定義の変更は「ビュー」タブで行います">ビュー</span>{% endif %}
        <span class="muted small">{{ '{:,}'.format(t.rows) if t.rows is not none else '行数不明' }} / {{ t.columns|length }}列</span>
        {% if t.description %}<span class="badge badge--ok">説明あり</span>
        {% else %}<span class="badge badge--warn">説明なし</span>{% endif %}
        {% if t.ai_draft %}<span class="badge badge--accent">AI下書き・未確認</span>{% endif %}
        <div class="spacer"></div>
        {# 削除は行の右端に置く。中を開かなくても押せるが、押すと
           巻き添えの一覧を見せる確認が出るので、その場では消えない #}
        <button class="btn btn--sm btn--icon t-drop" data-table="{{ t.name }}"
                data-rows="{{ t.rows or 0 }}" data-is-view="{{ 1 if t.is_view else 0 }}"
                title="{{ t.name }} を削除する{% if t.is_view %}（ビューの定義だけを消します。元のテーブルは残ります）{% endif %}"
                aria-label="{{ t.name }} を削除する"
                >{{ icon('trash', 'icon--sm') }}</button>
      </summary>
      <div class="acc__body">
        <div class="row mb">
          <div class="grow">
            <label class="field">テーブルの説明（1行 = 何のレコードか）</label>
            <textarea class="t-desc" rows="2">{{ t.description }}</textarea>
          </div>
          <button class="btn btn--sm t-draft" {{ 'disabled' if not llm_ready }}>AIに下書きさせる</button>
        </div>
        <div class="tablewrap mb">
          <table class="data">
            <thead><tr><th>列</th><th>型</th><th>説明</th><th>コード値の意味</th><th>実際の値</th></tr></thead>
            <tbody>
            {% for c in t.columns %}
              <tr data-col="{{ c.name }}">
                <td>{{ c.name }}{% if c.pk %} <span class="badge">PK</span>{% endif %}</td>
                <td class="muted">{{ c.type }}</td>
                <td style="min-width:240px"><input type="text" class="c-desc" value="{{ c.description }}"></td>
                <td style="min-width:200px"><input type="text" class="c-vals"
                    value="{% for k, v in c.codes.items() %}{{ k }}={{ v }}{{ '; ' if not loop.last }}{% endfor %}"
                    placeholder="1=受付; 2=出荷済"></td>
                <td class="muted" title="{{ c.actual }}">{{ c.actual }}</td>
              </tr>
            {% endfor %}
            </tbody>
          </table>
        </div>
        <button class="btn btn--primary btn--sm t-save">このテーブルを保存</button>
        {% if t.sample_rows %}
        <details class="acc mt">
          <summary>サンプル行を見る</summary>
          <div class="acc__body">
          {# 先頭数行だけでは判断できないので、全行を別タブで開く入口を必ず置く #}
          <div class="row mb" style="align-items:center">
            <span class="small muted">先頭 {{ t.sample_rows|length }} 行のみ</span>
            <div class="spacer"></div>
            <a class="btn btn--sm btn--ghost" target="_blank" rel="noopener"
               title="{{ t.name }} の全行を別タブで開きます（読み取り専用）"
               href="{{ url_for('tableview.index') }}?db={{ target|urlencode }}&table={{ t.name|urlencode }}"
               >{{ icon('table', 'icon--sm') }}テーブル全体を閲覧</a>
          </div>
          <div class="tablewrap"><table class="data">
            <thead><tr>{% for c in t.sample_columns %}<th>{{ c }}</th>{% endfor %}</tr></thead>
            <tbody>{% for r in t.sample_rows %}<tr>{% for v in r %}<td>{{ v }}</td>{% endfor %}</tr>{% endfor %}</tbody>
          </table></div></div>
        </details>
        {% endif %}
        {# 管理（取り込み元・定期取り込み・更新履歴・削除）。開いたときに manage.js が描く #}
        <details class="acc mt t-manage" data-table="{{ t.name }}">
          <summary>管理（取り込み元・定期取り込み・更新履歴・削除）</summary>
          <div class="acc__body t-manage__body"><div class="small muted">読み込み中…</div></div>
        </details>
      </div>
    </details>
    {% endfor %}
    {% if grouped and g.key %}
      </div>
    </details>
    {% endif %}
    {% endfor %}
  </div>

  <!-- ================= ER図 ================= -->
  <div class="tabpane" id="pane-er">
    <div class="er" id="erRoot">
      <div class="er__toolbar">
        {# 保存・元に戻す・やり直す。ツールチップの中身は er.js の syncHistoryUi が
           「次に何を戻すか」に合わせて書き換える #}
        <span class="er__tools">
          <button class="btn btn--sm btn--icon hastip hastip--l" id="erSave" disabled
                  aria-label="配置を保存" data-tip="配置を保存（Ctrl+S）">{{ icon('save') }}</button>
          <button class="btn btn--sm btn--icon hastip hastip--l" id="erUndo" disabled
                  aria-label="元に戻す" data-tip="元に戻す（Ctrl+Z）">{{ icon('undo') }}</button>
          <button class="btn btn--sm btn--icon hastip hastip--l" id="erRedo" disabled
                  aria-label="やり直す" data-tip="やり直す（Ctrl+Y）">{{ icon('redo') }}</button>
        </span>
        <button class="btn btn--sm" id="erFull">全画面</button>
        {% if grouped %}
        {# 表が多いときの絞り込み。元DB（表名の「__」より前）単位で表示する #}
        <select id="erGroup" style="width:auto"
                title="表示するグループを選びます。関連で繋がっている隣のまとまりの表（破線の枠）も一緒に出ます。&#10;まだ関連の無い、別のまとまりの表と線を結ぶときは「すべて」を選んでください">
          <option value="">すべて（{{ tables|length }}表）</option>
          {% for g in table_groups %}{% if g.key %}
          <option value="{{ g.key }}">{{ g.key }}（{{ g.tables|length }}）</option>
          {% endif %}{% endfor %}
        </select>
        <button class="btn btn--sm" id="erSuggest"
                title="列名から推測した「登録されていない結合の候補」を赤い線で重ねます。&#10;線をクリックすると内容を確かめて登録できます。&#10;画面に出ている表どうしの候補だけが描かれます">結合候補</button>
        <button class="btn btn--sm" id="erAddTable"
                title="いま表示しているまとまりに、別のまとまりの表を1つずつ足します。&#10;またぎの関連を引くときに、「すべて」で104表を出さずに済みます">＋ 別のまとまりの表</button>
        {% endif %}
      </div>
      <div class="er__viewport" id="erViewport">
        <svg class="er__svg" id="erSvg"></svg>
        <div class="er__world" id="erWorld"></div>
      </div>
      <div class="er__legend">
        <b>IPA表記</b>　<u>下線</u>＝主キー　<u style="text-decoration-style:dashed">破線</u>＝外部キー
        線の両端の <b>1</b>・<b>*</b>＝多重度　実線＝登録済み／短い破線＝FOREIGN KEY
        複数の列から出た線が1本に合流＝複合キー（その組で1つの結合。「複合キー(n列)」の印つき）
        <span id="erUsageLegend" class="hidden">　｜　<b>利用状況</b>:
          線の色が濃いほど分析でよく使われた結合　薄い灰色＝未使用（検算されていない経路）。
          線の上の数字は累積の使用回数</span>
      </div>
      <div class="er__panel hidden" id="erPanel"></div>
    </div>
    <div class="small muted mt">
      列の右端から相手テーブルの列へドラッグ＝関連を作成 ／ 線をクリック＝多重度・削除 ／
      テーブル見出しをドラッグ＝移動 ／ 何もない所をドラッグ＝画面移動 ／ ホイール＝拡大縮小
      <br>左上の {{ icon('undo', 'icon--sm') }} {{ icon('redo', 'icon--sm') }} で、移動・関連・主キーの変更をすべて1手ずつ戻す／やり直す（Ctrl+Z / Ctrl+Y）。
      {{ icon('save', 'icon--sm') }} はテーブルの配置を保存（Ctrl+S。関連などは操作した時点で保存済み）
    </div>

  </div>

  <!-- ================= 用語集・例文 ================= -->
  <div class="tabpane" id="pane-glossary">
    {# 用語集と例文は編集する場面が別なので、切り替えて片方ずつ広く使う #}
    <div class="seg mb">
      <button type="button" class="seg__btn is-active" data-sec="gl">業務用語 <span class="seg__count" id="segGlN">0</span></button>
      <button type="button" class="seg__btn" data-sec="ex">質問とSQLの例文 <span class="seg__count" id="segExN">0</span></button>
      <button type="button" class="seg__btn" data-sec="ck">検算 <span class="seg__count" id="segCkN">0</span></button>
    </div>

    <div id="sec-gl">
      <div class="card">
        <div class="card__desc">
          質問にこの言葉が出ると、AIはこの定義に従います。<b>説明は自然言語で構いません。</b>
          SQL式を入れておくとその式をそのまま使い、空欄なら説明からAIが組み立てます。
          置き場所は、その用語が使うテーブルを選び、複数テーブルにまたがるものだけ「DB全体」にします。
        </div>
        <div class="row mb" style="align-items:center">
          <input type="text" id="glFilter" style="max-width:260px"
                 placeholder="用語・説明・SQL・テーブル名で絞り込み">
          <span class="small muted" id="glCount"></span>
          <div class="spacer"></div>
          <button class="btn btn--sm" id="glDraft" {{ 'disabled' if not llm_ready }}
                  title="説明が書かれていてSQL式が空の用語すべてに、AIがSQL式を下書きします">説明からSQL式を下書き</button>
          <button class="btn btn--sm" id="glVerifyAll" title="全用語のSQL式を実データに当てて確かめます">すべて検証</button>
          <button class="btn btn--primary btn--sm" id="glSave">保存</button>
        </div>
        <div class="md">
          <div class="md__side">
            <button class="btn btn--sm" id="glAdd" style="width:100%">＋ 用語を追加</button>
            <div class="mlist" id="glList"></div>
          </div>
          <div class="md__main" id="glEditor"></div>
        </div>
      </div>
    </div>

    <div id="sec-ck" class="hidden">
      <div class="card">
        <div class="card__desc">
          <b>一致するはずの2つの数字</b>を登録しておくと、AIがそのテーブルに触れる
          SQLを実行するたびに自動で突き合わせ、食い違っていたらチャットに警告を出します
          （例: 入金の合計 = 請求のうち入金済みの合計）。
          同じ「売上」でも明細から数えるか請求から数えるかで答えが変わる——
          その食い違いに、聞いた人が気づけるようにする仕組みです。
          結果はデータが変わるまで記憶されるので、質問のたびに重い集計が走ることはありません。
        </div>
        <div class="row mb" style="align-items:center">
          <span class="small muted" id="ckCount"></span>
          <div class="spacer"></div>
          <button class="btn btn--sm" id="ckVerifyAll" title="全ルールをいま実行して、左右の値と差を確かめます">すべて検算</button>
          <button class="btn btn--primary btn--sm" id="ckSave">保存</button>
        </div>
        <div class="md">
          <div class="md__side">
            <button class="btn btn--sm" id="ckAdd" style="width:100%">＋ ルールを追加</button>
            <div class="mlist" id="ckList"></div>
          </div>
          <div class="md__main" id="ckEditor"></div>
        </div>
      </div>
    </div>

    <div id="sec-ex" class="hidden">
      <div class="card">
        <div class="card__desc">
          正しいと確認済みの質問とSQLの組。そのままAIのお手本になります（最大{{ examples_max }}件）。
          <b>説明は任意です。</b>「なぜこの書き方なのか」「どこに気をつけるか」を書いておくと、
          AIは似た質問のときも同じ勘所を守ります。
          チャットで回答が正しかったときの「この質問とSQLを例文として保存」からも増えます。
        </div>
        <div class="row mb" style="align-items:center">
          <input type="text" id="exFilter" style="max-width:260px"
                 placeholder="質問・SQLで絞り込み">
          <span class="small muted" id="exCount"></span>
          <div class="spacer"></div>
          <button class="btn btn--sm" id="exVerifyAll" title="全例文のSQLが実際に通るか確かめます">すべて検証</button>
          <button class="btn btn--primary btn--sm" id="exSave">保存</button>
        </div>
        <div class="md">
          <div class="md__side">
            <button class="btn btn--sm" id="exAdd" style="width:100%">＋ 例文を追加</button>
            <div class="mlist" id="exList"></div>
          </div>
          <div class="md__main" id="exEditor"></div>
        </div>
      </div>
    </div>
  </div>

  <!-- ================= ツール ================= -->
  <div class="tabpane" id="pane-tools">
    <div class="card">
      <div class="card__title">ユーザー定義ツール</div>
      <div class="card__desc">
        AIが呼び出せる専用ツールです。よく聞かれることを登録しておくと、
        AIが毎回SQLを書き起こさずに済み、答えのぶれもなくなります。<br>
        <b>やりたいことを日本語で書くだけで作れます。</b>SQLも設定も要りません。
        AIがカタログを見て使うテーブルを自分で決め、SQLを組み立て、
        実際のデータで動かした結果を見せてから登録します。
      </div>
      <div id="toolList"></div>
      <div class="row mt">
        <button class="btn btn--primary btn--sm" id="toolWizard">＋ ツールを作る</button>
      </div>
    </div>

    <div class="card">
      <div class="card__title">組み込みツール</div>
      <div class="card__desc">
        アプリに最初から入っているツールです。ここに出ている説明とパラメータが、
        そのまま <b>AIに渡っている内容</b>です。展開すると中身を確認できます。<br>
        説明を書き換えると、AIの「使うかどうか」の判断を調整できます（呼びすぎ・呼ばなすぎの対策）。
        空欄なら元の説明が使われます。
      </div>
      <div class="row mb" style="align-items:center">
        <input type="text" id="btFilter" style="max-width:280px"
               placeholder="ツール名・説明で絞り込み">
        <div class="spacer"></div>
        <span class="small muted" id="btCount"></span>
      </div>
      <div id="builtinList"></div>
    </div>
  </div>
  <!-- ================= ビュー ================= -->
  <div class="tabpane" id="pane-views">
    <div class="card">
      <div class="card__title">ビュー</div>
      <div class="card__desc">
        よく使う結合や絞り込みに名前を付けて保存します。<b>データは複製されず</b>、
        開くたびに元のテーブルから最新が計算されます。<br>
        登録するとテーブルと同じ扱いになり、テーブル一覧・ER図・チャットの表選択に出ます。
        説明や列の説明、用語も<b>テーブルと同じように付けられます</b>（「テーブル」タブで編集）。
      </div>
      <div id="viewList"></div>
      <div class="row mt">
        <button class="btn btn--primary btn--sm" id="viewNew">＋ ビューを作る</button>
      </div>
    </div>

    <div class="card hidden" id="viewEditor">
      <div class="card__title" id="viewEditorTitle">ビューを作る</div>

      <label class="field">1. どんな一覧が欲しいか、日本語で書く</label>
      <input type="text" id="viewPurpose" placeholder="例: 発注に部品名と仕入先名を付けた一覧">
      <div class="row mt mb">
        <button class="btn btn--sm btn--primary" id="viewDraft">AIにSQLを組み立てさせる</button>
        <span class="small muted">または</span>
        <button class="btn btn--sm" id="viewManual">SQLを自分で書く</button>
      </div>

      <div id="viewNote"></div>

      <div id="viewSqlWrap" class="hidden">
        <label class="field">2. SQL（SELECT文だけ。登録済みの結合はそのまま使えます）</label>
        <textarea id="viewSql" rows="8" class="mono" style="width:100%"
                  placeholder="SELECT ..."></textarea>
        <div id="viewExplain"></div>
        <div class="row mt mb">
          <button class="btn btn--sm" id="viewRun">実データで動かして確かめる</button>
        </div>
        <div id="viewPreview"></div>

        <label class="field mt">3. 名前と説明</label>
        <div class="row mb">
          <input type="text" id="viewName" class="mono" style="max-width:320px"
                 placeholder="まとまり__名前">
          <input type="text" id="viewDesc" class="grow"
                 placeholder="この一覧が何かの説明（AIが読みます）">
        </div>
        <div class="small muted mb">
          名前は「まとまり__名前」の形にしてください（まとまりは表と同じ接頭辞）。
          説明はそのままAIに渡り、どんなときに使うかの判断材料になります。
        </div>
        <div class="row">
          <button class="btn btn--primary btn--sm" id="viewSave">保存</button>
          <button class="btn btn--ghost btn--sm" id="viewCancel">やめる</button>
        </div>
      </div>
    </div>
  </div>


  {# 未保存の変更があるときだけ現れる。どこに何件あるかと、まとめて保存する口 #}
  <div class="savebar hidden" id="savebar">
    <span class="small" id="savebarText"></span>
    <button class="btn btn--primary btn--sm" id="saveAll">まとめて保存 (Ctrl+S)</button>
  </div>

{% endif %}
</div>
{% endblock %}

{% block scripts %}
{% if target %}
<script>
window.CAT = {
  db: {{ target|tojson }},
  grouped: {{ grouped|tojson }},
  examplesMax: {{ examples_max|tojson }},
  er: {{ er|tojson }},
  suggestions: {{ suggestions|tojson }},
  tables: {{ tables|tojson }},
  dbGlossary: {{ db_glossary|tojson }},
  examples: {{ examples|tojson }},
  custom: {{ custom|tojson }},
  builtin: {{ builtin|tojson }},
  builtinOverrides: {{ builtin_overrides|tojson }},
  checks: {{ checks|tojson }},
  // 用語集・例文・検算を開いたときの中身の印。保存時に送り返して、
  // その間に別の場所で足されたものを黙って消さないようにする
  stamps: {{ stamps|tojson }},
  views: {{ views|tojson }},
  llmReady: {{ llm_ready|tojson }},
  // グラフ種別ごとの必須項目。種別によって要る欄が違うので、
  // サーバの定義をそのまま渡して画面側で入力欄を出し分ける
  chartFields: {{ chart_fields|tojson }},
  intervals: {{ intervals|tojson }}
};
window.MANAGE = { intervals: {{ intervals|tojson }}, refresh: () => loadManage(true) };
</script>
{% endif %}
{% endblock %}
""",

# --- chat.html ---
"chat.html": r"""{% extends "base.html" %}
{% from "_icons.html" import icon %}
{% block title %}チャット — {{ app_title }}{% endblock %}
{# チャットだけ画面固定（ログの中をスクロールさせる）。CSSの .is-chat 参照 #}
{% block body_class %}is-chat{% endblock %}
{# 見出しは置かない。何の画面かはサイドバーで分かるので、ログに縦を使う。 #}

{% block sidebar %}
<div class="sidebar__section">
  <div class="sidebar__label">モデル</div>
  <select id="modelPick" title="使うモデルを選ぶ"></select>
  <div class="row mt" style="gap:8px;align-items:center">
    <span id="modelBadge" class="badge" title="このモデルが画像を扱えるか"></span>
    <div class="spacer"></div>
  </div>
  {# カタログ全体がこのモデルに収まらないときだけ現れる(中身は models.status の scope.note) #}
  <div id="modelWarn" class="alert alert--warn small mt" style="display:none"></div>
</div>

{# 節は開閉できる。既定を畳んでおくのは、DBもナレッジベースも数が多く、
   開いたままだと履歴までスクロールしないと届かないため。
   開閉の状態は common.js が localStorage に覚える。 #}
{# データ一覧。DBという概念は見せない（このアプリのDBは常に1つで裏方の実装詳細）。
   テーブルを元DBグループで折りたたみ、「何があるか」を確かめられるようにする #}
<details class="sidebar__section sbsec" id="secData">
  <summary>
    <span class="sidebar__label">SQLite3</span>
    <span class="badge" id="tblCount">{{ "%d / %d"|format(data.on_count, data.total) if data else 0 }}</span>
    {# summary の中のボタンは押しても開閉しない（common.js が止めている） #}
    {% if data and data.total %}
    <button class="btn btn--sm btn--ghost sbsec__act" id="tblAll"
            title="すべてを対象にする／すべて外す">全選択</button>
    {% endif %}
  </summary>
  <div class="sbsec__body">
  {% if not data or not data.total %}
    <div class="small muted">データがまだ取り込まれていません。
      {% if user.is_admin %}<a href="{{ url_for('imp.index') }}">データ取り込み</a>から始められます。{% endif %}</div>
  {% else %}
    <div class="small muted" style="margin-bottom:6px">
      チェックしたものだけをAIが使います。ふだんは全部つけたままで構いません
      （質問に必要な表はアプリが自動で選びます）。名前にマウスを乗せると説明が出ます。</div>
    {% if data.problem %}
    <div class="small muted" style="margin-bottom:6px">⚠ {{ data.problem }}</div>
    {% endif %}
    {% macro table_row(t) %}
      <div class="dbpick__table">
        <input type="checkbox" class="tblpick" data-table="{{ t.name }}"
               {{ 'checked' if t.on }} title="AIが使う対象にする">
        <a href="{{ url_for('tableview.index') }}?db={{ data.db|urlencode }}&table={{ t.name|urlencode }}"
           target="_blank" rel="noopener" class="dbpick__tname"
           data-desc-title="{{ t.name }}" data-desc="{{ t.description }}{% if t.problem %}
⚠ 定期取り込み: {{ t.problem }}{% endif %}
（クリックで中身を別タブで開きます）"
           data-desc-meta="{{ '{:,}行'.format(t.rows) if t.rows is not none else '行数不明' }} / {{ t.columns }}列">{{ t.name }}</a>
        {% if t.problem %}<span class="warnmark" title="{{ t.problem }}">{{ icon('alert', 'icon--sm') }}</span>{% endif %}
      </div>
    {% endmacro %}
    {% for g in data.groups %}
      {% if data.grouped and g.key %}
      <div class="dbpick">
        <div class="dbpick__head">
          <input type="checkbox" class="grppick" data-group="{{ g.key }}"
                 title="このまとまりをまとめて選ぶ／外す"
                 onclick="event.stopPropagation()">
          <span class="dbpick__name">{{ g.key }}</span>
          {% if g.tables|selectattr('problem', 'defined')|list %}<span class="warnmark">{{ icon('alert', 'icon--sm') }}</span>{% endif %}
          <span class="badge">{{ g.tables|length }}</span>
        </div>
        <div class="dbpick__tables">
          {% for t in g.tables %}{{ table_row(t) }}{% endfor %}
        </div>
      </div>
      {% else %}
      <div class="dbpick is-open">
        <div class="dbpick__tables">
          {% for t in g.tables %}{{ table_row(t) }}{% endfor %}
        </div>
      </div>
      {% endif %}
    {% endfor %}
  {% endif %}
  </div>
</details>

{# 社内文書の検索先。1件も登録が無ければ chat.js がこの節ごと隠す
   （使えないものを並べても、選びようがないため）。 #}
<details class="sidebar__section sbsec" id="kbSection" style="display:none">
  <summary>
    <span class="sidebar__label">LightRAG</span>
    <span class="badge" id="kbCount"></span>
    {# summary の中のボタンは押しても開閉しない（common.js が止めている） #}
    <button class="btn btn--sm btn--ghost sbsec__act" id="kbAll"
            title="すべてを検索対象にする／すべて外す">全選択</button>
  </summary>
  <div class="sbsec__body">
    <div class="small muted" style="margin-bottom:6px">
      チェックしたものだけをAIが調べます。名前にマウスを乗せると中身の説明が出ます。</div>
    <div id="kbList"></div>
    <details class="acc mt">
      <summary class="small muted" style="cursor:pointer;padding:4px 0">検索設定</summary>
      <div id="kbFields"></div>
      <div class="row mt">
        <button class="btn btn--sm btn--primary" id="kbSave">保存</button>
        <button class="btn btn--sm btn--ghost" id="kbReset">初期値に戻す</button>
      </div>
    </details>
  </div>
</details>

<details class="sidebar__section sbsec" id="secHistory" open>
  <summary>
    <span class="sidebar__label">チャット履歴</span>
    <button class="btn btn--sm sbsec__act" id="newChat">＋ 新規</button>
  </summary>
  <div class="sbsec__body">
    <div id="historyList"></div>
  </div>
</details>
{% endblock %}

{% block body %}
<div class="chat">
  <div class="chat__log" id="log">
    {# 中身は chat.js の renderEmpty() が描く。例文はカタログ由来で変わるので、
       テンプレートとJSの両方に同じものを書かない。 #}
    <div class="chat__inner" id="logInner"></div>
  </div>

  <div class="chat__composer">
    {# 上を読んでいるあいだだけ出る「最新へ」。入力欄のすぐ上に浮かせる。 #}
    <button class="jumpdown" id="jumpDown" type="button"
            title="最新のメッセージへ" aria-label="最新のメッセージへ">
      {{ icon('down') }}
    </button>
    <div class="composer__inner" id="attachRow" style="display:none">
      <div id="attachList" class="attachlist"></div>
    </div>
    <div class="composer__inner">
      <textarea id="input" rows="1" placeholder="{{ placeholder }}"></textarea>
      <button class="btn btn--primary" id="send" style="height:44px;padding:0 18px">送信</button>
    </div>
  </div>

  {# 画像をドラッグしてきたときだけ出る。添付はここへ落とすか、貼り付けで行う。 #}
  <div class="dropzone" id="dropzone" aria-hidden="true">
    <div class="dropzone__box">
      {{ icon('image', 'icon--lg') }}
      <span id="dropzoneText">画像をドロップして添付</span>
    </div>
  </div>
</div>
{% endblock %}

{% block scripts %}
<script src="/vendor/plotly.min.js"></script>
<script>
window.CHAT_INIT = {
  chatId: {{ (chat_id or '')|tojson }},
  history: {{ history|tojson }},
  autoDownload: {{ auto_download|default(true)|tojson }},
  llmReady: {{ llm_ready|tojson }},
  isAdmin: {{ user.is_admin|tojson }},
  knowledge: {{ knowledge|tojson }},
  starters: {{ starters|tojson }}
};
</script>
{% endblock %}
""",

# --- help.html ---
"help.html": r"""{% extends "base.html" %}
{% block title %}ヘルプ — {{ app_title }}{% endblock %}

{% block body %}
{# help クラスは「表のセルを折り返す」ための目印。table.data は本来
   1行1件のデータ格子用（white-space: nowrap で1行に収める）で、
   長い説明文を入れるヘルプでは1行目の途中で切れてしまう #}
<div class="content help">

  {# ページ内の目次。この5部がこのページのすべて #}
  <div class="card">
    <div class="card__title">ヘルプ</div>
    <div class="card__desc">
      このページは{% if user.is_admin %}5{% else %}4{% endif %}部構成です。<a href="#manual"><b>第1部 全機能の説明書</b></a> …
      画面ごとに、できること・使い方・裏で起きることを全部書いてあります。
      <a href="#arch"><b>第2部 システム構成の説明</b></a> … どこで何が動いていて、
      データがどこに置かれ、何が安全のために守られているか。
      <a href="#spec"><b>第3部 技術仕様</b></a> …
      処理の順序・アルゴリズム・しきい値・上限を、実装のとおりに書いた技術者向けの章。
      <a href="#glossary"><b>第4部 用語解説</b></a> …
      生成AI・SQL・ER図など、説明に出てくる専門用語そのものの意味を基礎から解説する章。
      {% if user.is_admin %}<a href="#impl"><b>第5部 実装リファレンス</b></a> …
      コードを触る人向けに、10のサブシステムの「どう動くか」を実装のとおりに書いた章。
      各節の最後に、実装を読まないと分からない<b>落とし穴</b>を集めてあります。
      <span class="small muted">（この章は管理者にだけ表示されます）</span>{% endif %}
    </div>
  </div>

  <!-- ==================================================================== -->
  <!-- 第1部 全機能の説明書 -->
  <!-- ==================================================================== -->
  <h2 id="manual" class="mt" style="font-size:20px">第1部 全機能の説明書</h2>

  <div class="card mt">
    <div class="card__title">1. チャット</div>
    <div class="card__desc">全員が使えるメイン画面。データと文書について日本語で質問すると、AIが調べて答えます。</div>
    <div class="tablewrap">
      <table class="data">
        <thead><tr><th style="width:210px">機能</th><th>説明</th></tr></thead>
        <tbody>
          <tr><td>質問する</td>
              <td>日本語で入力して送信（Enter）。AIが必要なテーブルを自分で選び、SELECT文を書いて
                  集計します。実行したSQLは回答に必ず表示され、その下に
                  <b>「このSQLがしていること」</b>の日本語の解説が付きます（SQLを読めなくても、
                  何をどう数えた結果かが分かります）。
                  文書の質問（手順・原因・規則）はナレッジベースを検索し、<b>[出典n]の番号つき</b>で
                  答えます。両方を組み合わせた質問（「一番停止が多い装置の対処方法は？」）もそのまま
                  聞けます。範囲の取り方で答えが変わる質問には、AIのほうから確認してきます。</td></tr>
          <tr><td>モデルの選択</td>
              <td>サイドバー上部のプルダウン。候補は管理者が「モデル設定」で決めた一覧で、選択は
                  利用者ごとに保存されます。「画像OK」の表示があるモデルでは、貼り付け（Ctrl+V）や
                  ドラッグ＆ドロップで画像を添付して質問できます。</td></tr>
          <tr><td>SQLite3 の選択</td>
              <td>サイドバーのチェックが「AIに見せるテーブルの範囲」です。まとまり単位・テーブル単位で
                  付け外しでき、外したテーブルはAIから<b>存在しないもの</b>として扱われます
                  （説明も渡らず、SQLで名指ししても実行を拒否）。選択は利用者ごとに保存され、
                  新しく取り込まれた表は自動で対象に入ります。名前クリックで中身を別タブ表示。</td></tr>
          <tr><td>LightRAG の選択</td>
              <td>同様に「AIが検索してよい文書の範囲」。名前にマウスを乗せると中身の説明が出ます。
                  「検索設定」で件数などの効き方も調整できます（利用者ごと）。両方とも0件にすると
                  質問は受け付けられません（その旨の案内が出ます）。</td></tr>
          <tr><td>書き直して送信</td>
              <td>自分の過去の発言にあるボタン。押した瞬間にそれ以降のやり取りが消え、
                  書き直した質問で続きから聞き直せます。</td></tr>
          <tr><td>グラフ・ファイル出力</td>
              <td>「グラフにして」「Excelにして」と頼むだけ。棒・折れ線・構成比など54種のグラフ、
                  Excel／CSV／Word／PowerPointのファイルが作れます。ファイルは画面から
                  ダウンロードでき、会話を開き直せば再ダウンロードもできます。</td></tr>
          <tr><td>メール送信</td>
              <td>「〇〇さんに送って」と頼むと、宛先を連絡先の表から実名で探し、下書きカードを
                  画面に出します。<b>送信されるのは、人がカードで承認したときだけ</b>。送れる宛先は
                  管理者が許可したドメインに限られます。</td></tr>
          <tr><td>⭐ 例文登録</td>
              <td>うまく答えられた質問は、回答の⭐からカタログの「例文」に登録できます。
                  例文はAIのお手本になり、似た質問への精度が上がります。AIが「登録しますか？」と
                  聞いてくることもあります（用語の定義も同様）。</td></tr>
          <tr><td>検算の警告</td>
              <td>回答の裏で、関係する検算（あらかじめ登録した「一致するはずの2つの数字」）が
                  自動で走ります。ずれていたときだけ、画面とAIの両方に警告が割り込みます。</td></tr>
          <tr><td>履歴</td>
              <td>会話は自動保存され、サイドバーの履歴から開き直せます（表・グラフ・ファイルも
                  そのまま復元）。履歴は本人の画面にだけ表示されます。</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="card mt">
    <div class="card__title">使い方の注意（チャット）</div>
    <div class="card__desc">
      知らないと結果を読み違えたり、できるはずのことを諦めたりしやすいポイントです。
    </div>
    <div class="tablewrap">
      <table class="data">
        <thead><tr><th style="width:210px">場面</th><th>注意</th></tr></thead>
        <tbody>
          <tr><td>表の選択を絞る</td>
              <td>外した表は<b>存在しないもの</b>としてAIは答えます。さらに、外した表を使う
                  例文・用語・関連もまとめてプロンプトから外れるため、「全選択なら正解できた
                  質問が、絞ると急に下手になる」ことがあります。答えがおかしいときは、
                  まずサイドバーのチェック状態を確認してください。</td></tr>
          <tr><td>大きな表を見せたとき</td>
              <td>画面の表は2,000行で切り詰められ（その旨の注記が付きます）、
                  <b>AIが実際に読んでいるのは先頭40行だけ</b>です。件数・合計・最大値・順位は
                  表をAIに「読ませて」判断させず、「◯◯を集計して」とSQLで計算させてください。</td></tr>
          <tr><td>「さっきの結果」の使い回し</td>
              <td>結果の使い回しはサーバのメモリ上にあり、<b>サーバ再起動・結果のあふれ
                  （40件）・表の選択変更</b>で失効します。失効すると同じSQLで取り直しになるため、
                  データが更新されていれば数字が変わることがあります。また、同じ質問の中では
                  同じSQLは再実行されません（最新が欲しければ新しい質問として送る）。</td></tr>
          <tr><td>作ったファイル</td>
              <td>ダウンロードは<b>作った本人だけ</b>（URLを共有しても他の人は開けません）。
                  実体はサーバのメモリにあり、再起動や上限（200件）で消えます。会話には2MBまで
                  保存され再ダウンロードできますが、<b>2MBを超えるファイルは作った直後が
                  唯一の入手機会</b>です。</td></tr>
          <tr><td>会話の寿命</td>
              <td>会話は1人100本まで・最終更新から90日で自動削除されます（開いて見るだけでは
                  延びません）。また、会話が長いほど毎回の送信量が増えて遅く・高くなるため、
                  <b>話題が変わったら新しい会話</b>にするのがおすすめです。</td></tr>
          <tr><td>書き直して送信</td>
              <td>指定した発言から後のやり取り（回答・ファイル含む）は<b>完全に消えて</b>
                  やり直しになります。残したいファイルは先に保存してください。</td></tr>
          <tr><td>回答が途中で止まる</td>
              <td>1つの質問でAIがツールを使えるのは10回まで。多段の依頼（分析→グラフ→
                  Excel→レポート）は途中で一区切りになることがあります。「続けて」と送るか、
                  質問を分けてください。同じ操作の繰り返しも自動で打ち切られます。</td></tr>
          <tr><td>過去の会話の続き</td>
              <td>過去の会話を開いて続けると、<b>当時ではなく「今の」カタログ・用語定義</b>で
                  AIが動きます。定義が変わっていれば同じ質問でも答えは変わります。</td></tr>
          <tr><td>検算の警告</td>
              <td>警告は「不一致が見つかったときだけ」出ます。<b>警告が無いことは
                  「検証して問題なし」の意味ではありません</b>（関係する表に触れない質問では
                  検算自体が走りません）。</td></tr>
          <tr><td>文書検索（ナレッジベース）</td>
              <td>サイドバーで1つも選んでいないと、AIは文書の存在自体を知りません。逆に
                  関係ないものまで選ぶと、限られた文脈を分け合って本命の文書が薄まります。
                  <b>質問に関係するものだけ選ぶ</b>と精度が上がります。</td></tr>
          <tr><td>画像の添付</td>
              <td>1つの質問に4枚・1枚8MBまで（5枚目以降は黙って外れます）。貼ってから時間を
                  置く・サーバが再起動すると画像が失われたまま送られることがあるので、
                  貼ったらすぐ送ってください。画像を使った会話は画像対応モデルのまま続けること。</td></tr>
          <tr><td>メール</td>
              <td>AIにできるのは<b>下書きまで</b>。送信されるのは画面のボタンを押したときだけで、
                  送れる宛先は管理者が登録した許可リストに完全一致するアドレスに限られます。</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  {% if user.is_admin %}
  <div class="card mt">
    <div class="card__title">2. データカタログ（管理者）</div>
    <div class="card__desc">
      ここに書いた内容が<b>そのままAIの理解</b>になります。回答の質はカタログの質で決まります。
      未保存の変更は下部の「まとめて保存 (Ctrl+S)」でまとめて確定できます。
    </div>
    <div class="tablewrap">
      <table class="data">
        <thead><tr><th style="width:210px">タブ／機能</th><th>説明</th></tr></thead>
        <tbody>
          <tr><td>テーブル — 説明を書く</td>
              <td>表の説明（「1行＝何のレコードか」）と、列ごとの説明・コード値の意味を書きます。
                  「AIに下書きさせる」で草案を作らせ、人が直して保存する流れが速いです。
                  「実際の値」列には実データの値域が自動表示されるので、見ながら書けます。
                  検索欄は表名・列名・説明・実際の値まで対象。「説明なしだけ」で未記入だけに絞れます。</td></tr>
          <tr><td>テーブル — まとまり</td>
              <td>表は「まとまり__表名」の規約で領域ごとに束ねられます（まとまりは名前から自動で
                  決まる整理単位。詳細は第2部）。まとまりの見出しを開くと<b>メモ</b>が書けます。
                  メモは「複数の表にまたがる前提」（指標の定義・記録の範囲など）の置き場で、
                  そのまとまりの表を使うときだけAIに渡ります。<b>名前の変更</b>もここから：
                  まとまりの名前は表名の接頭辞そのものなので、変更すると配下の全テーブルが
                  まとめて改名され、記述はすべて引き継がれます。</td></tr>
          <tr><td>テーブル — 管理</td>
              <td>各表の「管理」を開くと、取り込み元・定期取り込みの状態・更新履歴・行数などが
                  見られます。<b>「名前・まとまりを変更」</b>で表の改名／別のまとまりへの移動ができ、
                  説明・関連・用語・例文・検算・定期取り込み・利用者の選択まで全部ついてきます。
                  削除は一覧の行の右端（マウスを乗せると出るゴミ箱）。削除時は巻き添えになる
                  記述の一覧を確認してから実行でき、カタログも一緒に片づきます。</td></tr>
          <tr><td>結合・ER図</td>
              <td>表どうしの繋がり（AIがJOINに使う関連）を管理します。列の右端から相手の列へ
                  ドラッグで作成、線をクリックで多重度（N:1＝多対1 など）の変更・削除。
                  Ctrl+Z/Ctrl+Yで取り消し・やり直し、Ctrl+Sで配置保存。表示はまとまり単位で、
                  関連で繋がった隣のまとまりの表は破線枠で自動表示。「＋別のまとまりの表」で
                  相手を1つずつ足せます。線の濃さは過去の分析で実際に使われた回数
                  （薄い灰色＝未使用）。登録時には実データで値の重なりを検証し、
                  繋がらない線は保存前に止まります。</td></tr>
          <tr><td>結合・ER図 — 結合候補</td>
              <td>「結合候補」ボタンで、未登録の結合の推測が<b>赤い点線</b>で重なります。推測は
                  列名（同じ名前の列が相手の単独主キー等）と<b>実データの値の一致率</b>の両方で行い、
                  値が全く重ならない候補は出しません。赤線をクリック→根拠と一致率を確認→
                  「この結合を登録」。関連を消すと候補に即座に戻ります。</td></tr>
          <tr><td>用語集</td>
              <td>「質問にこの言葉が出たら必ずこの定義に従う」という言葉の辞書。<b>説明は自然言語だけで
                  効きます</b>（SQL式は任意。あればその式をそのまま使い、なければAIが説明から組み立て）。
                  置き場所は迷ったら「全体」で構いません。「検証」で式を実データに当てて確かめられ、
                  該当行の実物まで表示されます。SQL式の下には日本語の読み下しが自動表示されます。</td></tr>
          <tr><td>質問とSQLの例文</td>
              <td>「この質問には、このSQLが正解」というお手本（最大200件）。チャットの⭐からも
                  貯まります。「検証」で実行結果の先頭5行まで確認でき、SQLの日本語解説も
                  自動表示。「ツールにする」で例文をそのままユーザー定義ツールに変換できます。</td></tr>
          <tr><td>検算</td>
              <td>「一致するはずの2つのSQL」を登録しておくと、AIがその表に触れるSQLを実行する
                  たびに自動で突き合わせ、<b>ずれたときだけ</b>警告します（許容差％と、不一致時に
                  差の実体を見せるドリルダウンSQLも設定可）。text-to-SQLの最大のリスク
                  「正しいSQLなのに業務的には別の数字」への安全網です。</td></tr>
          <tr><td>ツール</td>
              <td>組み込み44ツールの説明・パラメータ・<b>実装コード</b>（実際に何をするか）を確認でき、
                  説明の上書きや「AIに渡さない」設定ができます。ユーザー定義ツール（よく使うSQLを
                  名前つきの道具に）もここで管理します。</td></tr>
          <tr><td>取り込み</td>
              <td>Excel／CSV／TXTをテーブルにします。ファイルを選ぶ→シート・区切り・見出し行を
                  確認→型推定つきのプレビュー→<b>まとまりを選び</b>テーブル名を付けて実行。
                  「できるテーブル: 社内Webリンク集__links」と結果が常に表示され、既存の表と重なる場合は
                  警告が出ます。取得日時列（いつ時点のデータか）は必須で自動付与。
                  更新のしかたは「全件入れ替え」と「追記」（追記は定期取り込み専用で、
                  間隔・開始日時・保持回数を決めて登録。内蔵スケジューラが自動実行）。</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="card mt">
    <div class="card__title">3. ナレッジベース／4. モデル設定／5. メール設定（管理者）</div>
    <div class="tablewrap">
      <table class="data">
        <thead><tr><th style="width:210px">画面</th><th>説明</th></tr></thead>
        <tbody>
          <tr><td>ナレッジベース</td>
              <td>社内文書の検索先（LightRAGサーバ）を登録します。URLとAPIキーを入れて接続テスト。
                  <b>ここに書く説明文が、AIがどのナレッジベースを調べるかの判断材料</b>になるので、
                  中身が分かる説明を書いてください。0件だとAIに検索ツール自体が渡りません。</td></tr>
          <tr><td>モデル設定</td>
              <td>チャットで選べるモデルの候補と既定を決めます。「一覧を取得」でAPIから使える
                  モデルを取り直せます。候補から外しても、誰かが使用中のモデルは選択肢に残ります。</td></tr>
          <tr><td>メール設定</td>
              <td>送信サーバ（SMTP）・差出人・送ってよい宛先ドメイン・宛先件数の上限を決めます。
                  既定は試送モード（実際には送らない）。接続確認ボタンで疎通を確かめられます。</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="card mt">
    <div class="card__title">6. アカウントと権限</div>
    <div class="tablewrap">
      <table class="data">
        <thead><tr><th style="width:210px">項目</th><th>説明</th></tr></thead>
        <tbody>
          <tr><td>権限</td>
              <td>一般利用者＝チャットとヘルプ。管理者＝全画面（カタログ・取り込み・各設定）。
                  管理者だけに渡るAIツールは、一般利用者のAIには渡りません。</td></tr>
          <tr><td>アカウント管理</td>
              <td>サーバ上のコマンドで行います:
                  <code>python core.py users list / add / passwd / remove</code>。
                  社内LDAPへの切り替え口も用意されています（設定ファイルで切替）。</td></tr>
        </tbody>
      </table>
    </div>
  </div>
  <div class="card mt">
    <div class="card__title">使い方の注意（カタログと運用・管理者）</div>
    <div class="card__desc">
      カタログの「書き方」と運用操作が、AIへの届き方・自動削除・警告にどう効くかの要点です。
      迷ったら原則は1つ: <b>SQL式には表名を書く。書かないなら説明だけにする。</b>
    </div>
    <div class="tablewrap">
      <table class="data">
        <thead><tr><th style="width:210px">場面</th><th>注意</th></tr></thead>
        <tbody>
          <tr><td>用語のSQL式</td>
              <td>式はAIに<b>無検証で「そのまま」</b>使われます。誤った式は全利用者の回答を
                  同じ形で歪めます（説明文だけなら、AIが列情報から組み立て直すので自己修正が
                  効きます）。また、<b>表名を書いていない式</b>は、表を絞った瞬間に用語ごと
                  プロンプトから外れ、表の削除時にも自動では消えません（削除の確認画面に
                  「自動では消えない用語」として出ます）。</td></tr>
          <tr><td>用語の説明文</td>
              <td>説明文の中に表名を書くと、その表が選択外になったとき用語ごと外れます
                  （選択外の表名の漏洩を防ぐ仕組み）。説明は用語の対象範囲の中で書くこと。</td></tr>
          <tr><td>例文</td>
              <td>登録した瞬間から「正しいと確認済みの例」としてAIのお手本になります。
                  <b>実行して結果を確認したSQLだけ</b>を登録し、締め日・除外条件などの前提は
                  補足欄に書いてください。同じSQLの再登録は追加ではなく質問文の上書き、
                  上限は200件です。</td></tr>
          <tr><td>カタログが大きくなったら</td>
              <td>モデルの文脈に収まらないと各表の<b>列名だけが削られ</b>、例文・用語・メモは
                  残ります。例文や用語を増やしすぎることが列名を犠牲にします。また
                  文脈の小さいモデルを選んだ利用者だけ要約モードに落ちるため、
                  「人によって答えの質が違う」原因になります。</td></tr>
          <tr><td>用語の置き場所</td>
              <td>表に付けた用語は、カタログが大きい環境では<b>名前しか渡りません</b>
                  （定義はAIが取りに行ったときだけ）。全体に置いた用語は常に定義まで渡ります。
                  常に効かせたい定義は全体へ、表とセットの定義は表へ。</td></tr>
          <tr><td>まとまりメモ</td>
              <td>メモは「その接頭辞の表が選択中」のときだけ渡ります。最後の表を消すと
                  メモも自動で消え、移動先に既にメモがある「まとまりの統合」では
                  旧メモは引き継がれず破棄されます。残したい内容は先に写してください。</td></tr>
          <tr><td>表の命名</td>
              <td>「__」の後ろが同じ名前の表が複数のまとまりにあると、AIに
                  「全体はUNION ALLで合算せよ」の指示が自動で入ります。<b>接尾辞は合算指示を
                  兼ねる</b>ので、構成の違う表に同じ接尾辞を付けないでください。</td></tr>
          <tr><td>実データの露出</td>
              <td>値の種類が20以下の列は<b>実データの値と件数がそのままAI（外部API）に
                  渡ります</b>。サンプル行も先頭3行が渡ります。機微な値を含む表の扱いに注意。
                  また表の除外は分析範囲の絞り込みであって閲覧制御ではありません
                  （ER図やテーブル詳細からは見えます）。</td></tr>
          <tr><td>カタログの編集</td>
              <td>編集のたびにプロンプトキャッシュが外れ、直後の質問は遅く・高くなります。
                  <b>細かく直すよりまとめて直す</b>方が得です。同じ画面を2人で開いて保存すると
                  後勝ちで上書きされます（変更履歴には残ります）。</td></tr>
          <tr><td>取り込み: 日付とコード</td>
              <td>日付は必ずTEXTで入るため、元ファイル側で <code>2026-09-05</code> のような
                  ゼロ埋め書式に統一しないと並べ替え・期間絞り込みが狂います。列の型は
                  登録時のデータで固定されるので、登録時に先頭ゼロの無かったコード列は
                  INTEGERになり、後から来た「0123」は黙って123になります。</td></tr>
          <tr><td>取り込み: 追記の保持回数</td>
              <td>保持回数を後から<b>減らすと、次の実行で超過分が即・不可逆に削除</b>されます。
                  取得日時が空の旧行は保持回数の管理外で残り続けます。追記は手動実行できません
                  （CLIの refresh --all は検査を通らないため、追記ジョブがある環境では
                  気軽に叩かないこと）。</td></tr>
          <tr><td>取り込み: 全件入れ替えのジョブ</td>
              <td>保存時に自動で「リアルタイム更新・定期実行なし」になります。更新されるのは
                  <b>誰かが質問したときのファイル変更検知だけ</b>で、変更検知は更新時刻＋サイズ
                  です（同時刻・同サイズの差し替えは検知されません）。列構成は登録時に固定され、
                  元ファイルの列が増えても取り込まれません。</td></tr>
          <tr><td>表の削除</td>
              <td>巻き添え削除は「SQLにその表名が書かれているか」の文字列照合です。表名を
                  書いた用語・例文・検算は消え、書いていないものは残ります（確認画面の一覧を
                  必ず見ること）。「ジョブを残す」を選ぶと<b>次の定期実行で表が復活</b>します。
                  ユーザー定義ツールは巻き添え削除の対象外なので手で直してください。</td></tr>
          <tr><td>改名</td>
              <td>カタログ・定期取り込み・利用者の選択は追随しますが、<b>チャット履歴と
                  取り込み履歴は旧名のまま</b>です。過去の会話のSQLを再実行すると
                  「表がありません」になります。</td></tr>
          <tr><td>ユーザー定義ツール</td>
              <td>AIに渡るのは名前・説明・引数だけで<b>SQL本文は見えません</b>。式が古くても
                  AIは検査も修正もできず使い続けるため、データ変更時は人が検証すること。
                  定義が壊れると（エラー表示なしに）AIのツール一覧から黙って外れます。
                  組み込みツールの説明の上書きは<b>丸ごと差し替え</b>で、元の使い方の指示ごと
                  消える点にも注意。</td></tr>
          <tr><td>検算のルール</td>
              <td>左右のSQLは<b>1行1列の集計値</b>を返す形で書くこと（複数行でもエラーに
                  ならず先頭だけで比べる無意味な検算になります）。許容差は相対％（既定0.5%）で、
                  金額が大きいと0.5%でも大きな差を見逃します。壊れたルールは黙ってスキップ
                  されるので、カタログ画面の「検算」で定期的に実行して点検してください。</td></tr>
        </tbody>
      </table>
    </div>
  </div>
  {% endif %}

  <!-- ==================================================================== -->
  <!-- 第2部 システム構成の説明 -->
  <!-- ==================================================================== -->
  <h2 id="arch" class="mt" style="font-size:20px">第2部 システム構成の説明</h2>

  <div class="card mt">
    <div class="card__title">質問が答えになるまで</div>
    <div class="card__desc">
      AIは何も知らない状態から出発しません。<b>データカタログに書かれた内容がそのままAIの理解</b>に
      なり、答えのあとには検算が自動で走ります。
    </div>
    <svg viewBox="0 0 760 300" style="width:100%;max-width:760px" xmlns="http://www.w3.org/2000/svg"
         font-size="13" text-anchor="middle">
      <defs>
        <marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
          <path d="M0 0L10 5L0 10z" fill="var(--muted)"/>
        </marker>
      </defs>
      <!-- 利用者 -->
      <rect x="20" y="110" width="110" height="56" rx="8" fill="none" stroke="var(--border-2)"/>
      <text x="75" y="134" fill="var(--text)">利用者</text>
      <text x="75" y="152" fill="var(--muted)" font-size="11">日本語で質問</text>
      <!-- AI -->
      <rect x="220" y="98" width="150" height="80" rx="8" fill="none" stroke="var(--accent)" stroke-width="2"/>
      <text x="295" y="128" fill="var(--text)" font-weight="bold">AI</text>
      <text x="295" y="148" fill="var(--muted)" font-size="11">SQLを書く／検索する</text>
      <!-- カタログ -->
      <rect x="220" y="222" width="150" height="56" rx="8" fill="none" stroke="var(--border-2)"/>
      <text x="295" y="245" fill="var(--text)">データカタログ</text>
      <text x="295" y="263" fill="var(--muted)" font-size="11">説明・用語・例文 = AIの知識</text>
      <!-- データ -->
      <rect x="470" y="40" width="130" height="56" rx="8" fill="none" stroke="var(--border-2)"/>
      <text x="535" y="63" fill="var(--text)">SQLite3</text>
      <text x="535" y="81" fill="var(--muted)" font-size="11">テーブル（読み取り専用）</text>
      <!-- 文書 -->
      <rect x="470" y="120" width="130" height="56" rx="8" fill="none" stroke="var(--border-2)"/>
      <text x="535" y="143" fill="var(--text)">LightRAG</text>
      <text x="535" y="161" fill="var(--muted)" font-size="11">社内文書（出典つき）</text>
      <!-- 検算 -->
      <rect x="470" y="200" width="130" height="56" rx="8" fill="none" stroke="var(--border-2)" stroke-dasharray="5 4"/>
      <text x="535" y="223" fill="var(--text)">検算</text>
      <text x="535" y="241" fill="var(--muted)" font-size="11">ずれたときだけ警告</text>
      <!-- 回答 -->
      <rect x="650" y="110" width="95" height="56" rx="8" fill="none" stroke="var(--border-2)"/>
      <text x="697" y="134" fill="var(--text)">回答</text>
      <text x="697" y="152" fill="var(--muted)" font-size="11">SQL・出典つき</text>
      <!-- 矢印 -->
      <line x1="130" y1="138" x2="212" y2="138" stroke="var(--muted)" marker-end="url(#ar)"/>
      <line x1="295" y1="222" x2="295" y2="186" stroke="var(--muted)" marker-end="url(#ar)"/>
      <line x1="370" y1="118" x2="462" y2="72" stroke="var(--muted)" marker-end="url(#ar)"/>
      <line x1="370" y1="145" x2="462" y2="147" stroke="var(--muted)" marker-end="url(#ar)"/>
      <line x1="370" y1="168" x2="462" y2="222" stroke="var(--muted)" marker-end="url(#ar)"/>
      <line x1="600" y1="138" x2="642" y2="138" stroke="var(--muted)" marker-end="url(#ar)"/>
    </svg>
    <div class="small muted mt">
      安全のための決まり: AIが実行できるのは<b>読み取り（SELECT）だけ</b>で、データの書き換えは
      できません。チェックを外した表・文書には触れません。メールは許可済みの宛先にしか送れず、
      送信前に必ず人の確認が入ります。
    </div>
  </div>

  <div class="card mt">
    <div class="card__title">カタログがAIの理解になる（知識の4層）</div>
    <div class="card__desc">
      知識は必ず「対象物」に付けます。全体に書く欄はありません（対象の入れ替えで説明が
      腐るのを防ぐ設計）。対象を選んでいるときだけAIに渡るので、書きすぎても他の質問の
      邪魔をしません。
    </div>
    <svg viewBox="0 0 760 210" style="width:100%;max-width:760px" xmlns="http://www.w3.org/2000/svg"
         font-size="13" text-anchor="middle">
      <defs>
        <marker id="ar2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
          <path d="M0 0L10 5L0 10z" fill="var(--muted)"/>
        </marker>
      </defs>
      <rect x="20"  y="30" width="160" height="66" rx="8" fill="none" stroke="var(--border-2)"/>
      <text x="100" y="56" fill="var(--text)">テーブル・列の説明</text>
      <text x="100" y="76" fill="var(--muted)" font-size="11">1行＝何か、コード値の意味</text>
      <rect x="200" y="30" width="160" height="66" rx="8" fill="none" stroke="var(--border-2)"/>
      <text x="280" y="56" fill="var(--text)">まとまりのメモ</text>
      <text x="280" y="76" fill="var(--muted)" font-size="11">複数の表にまたがる前提</text>
      <rect x="380" y="30" width="160" height="66" rx="8" fill="none" stroke="var(--border-2)"/>
      <text x="460" y="56" fill="var(--text)">用語集</text>
      <text x="460" y="76" fill="var(--muted)" font-size="11">言葉の定義（自然言語でOK）</text>
      <rect x="560" y="30" width="160" height="66" rx="8" fill="none" stroke="var(--border-2)"/>
      <text x="640" y="56" fill="var(--text)">例文・検算</text>
      <text x="640" y="76" fill="var(--muted)" font-size="11">正解のお手本と、数字の突き合わせ</text>
      <line x1="380" y1="110" x2="380" y2="140" stroke="var(--muted)" marker-end="url(#ar2)"/>
      <rect x="230" y="148" width="300" height="46" rx="8" fill="none" stroke="var(--accent)" stroke-width="2"/>
      <text x="380" y="176" fill="var(--text)">そのままAIの理解になる</text>
    </svg>
  </div>

  <div class="card mt">
    <div class="card__title">「まとまり」とは</div>
    <div class="card__desc">
      テーブル名の前半（<code>人事_勤怠__employees</code> の <code>人事_勤怠</code>）から自動で決まる<b>束ね方</b>です。
      物理的な入れ物ではなく、DBの実体は統合.db 1つだけ。1つの表は必ず1つのまとまりに属し
      （取り込み時に選択必須。規約のアンダースコアは画面が自動で組み立てます。名前は日本語でOK）、
      まとまりはメモ（複数の表にまたがる前提）を持ちます。サイドバーの一括チェック・
      カタログの折りたたみ・ER図の表示単位・結合候補の優先順位・「全社＝全拠点をUNION ALLで合算」の
      自動案内が、すべてこの束ね方の上に乗っています。名前・所属はあとから変更できます
      （変更は管理者がデータカタログ画面から行います。配下の表の改名として実行され、記述は引き継がれます）。
    </div>
  </div>

  <div class="card mt">
    <div class="card__title">構成の概要</div>
    <div class="card__desc">
      アプリ本体は1台のサーバで動くFlaskアプリ。データはサーバ上のファイルに置かれ、
      外部に出て行くのはLLMの呼び出しだけです。
    </div>
    <svg viewBox="0 0 760 430" style="width:100%;max-width:760px" xmlns="http://www.w3.org/2000/svg"
         font-size="13" text-anchor="middle">
      <defs>
        <marker id="ar3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
          <path d="M0 0L10 5L0 10z" fill="var(--muted)"/>
        </marker>
      </defs>

      <!-- ブラウザ -->
      <rect x="20" y="60" width="130" height="64" rx="8" fill="none" stroke="var(--border-2)"/>
      <text x="85" y="86" fill="var(--text)">ブラウザ</text>
      <text x="85" y="106" fill="var(--muted)" font-size="11">社内PC（素のHTML/JS）</text>

      <!-- 取り込み元 -->
      <rect x="20" y="300" width="130" height="64" rx="8" fill="none" stroke="var(--border-2)" stroke-dasharray="5 4"/>
      <text x="85" y="326" fill="var(--text)">取り込み元フォルダ</text>
      <text x="85" y="346" fill="var(--muted)" font-size="11">Excel / CSV</text>

      <!-- アプリサーバ（外枠） -->
      <rect x="210" y="30" width="280" height="370" rx="10" fill="none" stroke="var(--accent)" stroke-width="2"/>
      <text x="350" y="54" fill="var(--text)" font-weight="bold">アプリサーバ（Flask・1台）</text>

      <rect x="230" y="70" width="240" height="48" rx="6" fill="none" stroke="var(--border-2)"/>
      <text x="350" y="90" fill="var(--text)">画面（チャット・カタログ ほか）</text>
      <text x="350" y="107" fill="var(--muted)" font-size="11">ログイン必須／画面ごとに権限</text>

      <rect x="230" y="130" width="240" height="48" rx="6" fill="none" stroke="var(--border-2)"/>
      <text x="350" y="150" fill="var(--text)">AIエージェント</text>
      <text x="350" y="167" fill="var(--muted)" font-size="11">SQLは SELECT専用ガード を通る</text>

      <rect x="230" y="190" width="240" height="48" rx="6" fill="none" stroke="var(--border-2)"/>
      <text x="350" y="210" fill="var(--text)">取り込み・定期実行</text>
      <text x="350" y="227" fill="var(--muted)" font-size="11">DBに書けるのはここだけ（管理者）</text>

      <!-- 保存ファイル -->
      <rect x="230" y="256" width="240" height="128" rx="6" fill="none" stroke="var(--border-2)"/>
      <text x="350" y="278" fill="var(--text)">保存ファイル（サーバ内）</text>
      <text x="350" y="300" fill="var(--muted)" font-size="11">data/統合.db（SQLite・唯一のDB）</text>
      <text x="350" y="320" fill="var(--muted)" font-size="11">統合.db.meta.yaml（カタログ）</text>
      <text x="350" y="340" fill="var(--muted)" font-size="11">users/（会話履歴・個人設定）</text>
      <text x="350" y="360" fill="var(--muted)" font-size="11">knowledge_bases.json（接続先の登録簿）</text>

      <!-- 外部・社内サービス -->
      <rect x="560" y="60" width="180" height="64" rx="8" fill="none" stroke="var(--border-2)"/>
      <text x="650" y="84" fill="var(--text)">ChatGPT-API</text>
      <text x="650" y="104" fill="var(--muted)" font-size="11">HTTPS・社外。envでローカルLLMに切替可</text>

      <rect x="560" y="160" width="180" height="64" rx="8" fill="none" stroke="var(--border-2)"/>
      <text x="650" y="184" fill="var(--text)">LightRAGサーバ群</text>
      <text x="650" y="204" fill="var(--muted)" font-size="11">社内・HTTP。文書の検索だけ</text>

      <rect x="560" y="260" width="180" height="64" rx="8" fill="none" stroke="var(--border-2)"/>
      <text x="650" y="284" fill="var(--text)">SMTPサーバ</text>
      <text x="650" y="304" fill="var(--muted)" font-size="11">社内。許可宛先へ・承認後のみ</text>

      <!-- 矢印 -->
      <line x1="150" y1="92" x2="202" y2="92" stroke="var(--muted)" marker-end="url(#ar3)"/>
      <text x="176" y="82" fill="var(--muted)" font-size="10">HTTP</text>
      <line x1="150" y1="322" x2="222" y2="230" stroke="var(--muted)" marker-end="url(#ar3)"/>
      <line x1="350" y1="238" x2="350" y2="248" stroke="var(--muted)" marker-end="url(#ar3)"/>
      <line x1="490" y1="92" x2="552" y2="92" stroke="var(--muted)" marker-end="url(#ar3)"/>
      <line x1="490" y1="160" x2="552" y2="185" stroke="var(--muted)" marker-end="url(#ar3)"/>
      <line x1="490" y1="230" x2="552" y2="285" stroke="var(--muted)" marker-end="url(#ar3)"/>
    </svg>
  </div>

  <div class="card mt">
    <div class="card__title">データの置き場所（data/ フォルダ）</div>
    <div class="tablewrap">
      <table class="data">
        <thead><tr><th style="width:260px">ファイル</th><th>役割</th></tr></thead>
        <tbody>
          <tr><td class="mono small">統合.db</td>
              <td>唯一のSQLite。すべてのテーブルがここに入ります（DBは常に1つ・巻き戻し無し。
                  書き込めるのは取り込み機能だけで、AIは読み取り専用）。</td></tr>
          <tr><td class="mono small">統合.db.meta.yaml</td>
              <td>データカタログの実体。表・列の説明、まとまりのメモ、関連、用語、例文、
                  検算、ER図の配置。全員で1つを共有（編集は管理者のみ）。</td></tr>
          <tr><td class="mono small">knowledge_bases.json</td>
              <td>ナレッジベースの登録簿（URL・APIキー・説明・有効/停止）。</td></tr>
          <tr><td class="mono small">users/&lt;名前&gt;/</td>
              <td>利用者ごとの保存領域。会話履歴（chats/）と個人設定（prefs.yaml: モデル選択・
                  表とKBのチェック・検索設定）。退職者はフォルダごと消せば片づきます。</td></tr>
          <tr><td class="mono small">import_jobs.yaml ／ import_history.jsonl</td>
              <td>定期取り込みの設定と、取り込みの実行記録（成功・失敗とも）。</td></tr>
          <tr><td class="mono small">model_settings.yaml ／ mail_settings.yaml</td>
              <td>モデル候補・既定、メール送信の設定（各画面から編集）。</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  {% if user.is_admin %}
  <div class="card mt">
    <div class="card__title">全体図（システム構成）</div>
    <div class="card__desc">
      仕組みの設計を1枚にした図。<b style="color:#b8552f">茶色の線が質問の進む道</b>、
      <b style="color:#2e7d5b">緑の線が回答の戻る道</b>。個々のツール名・テーブル名・接続先URLは
      この図には載せず、下の「サーバ一覧」「まとまりとテーブルの一覧」「ツール一覧」に
      いまの状態が自動で表示されます。配色は固定（スライド用）なので、印刷や資料への転用は
      この図をそのまま使えます。
    </div>
    <div style="overflow-x:auto;border:1px solid var(--border);border-radius:8px;background:#ffffff">
      <div style="min-width:760px">
<svg xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;display:block" viewBox="0 0 1200 620" role="img"
     aria-label="システム構成図。質問は❶利用者のブラウザ→アプリの画面へ。❷AIオーケストレーションがカタログの知識を添えてAIモデル（外部API）に思考を依頼し、❸モデルがツール実行を指示、❹ツールだけがデータベース（読み取り専用）と文書検索サーバ群に触れる。②〜④を必要なだけ往復し、❺回答が画面へ逐次表示で戻る。取り込みだけがDBへ書き込む別経路。">
  <style>
    text { font-family: "IBM Plex Sans JP", "Yu Gothic UI", "Meiryo", sans-serif; }
    .zone { fill: none; stroke: #e2d9cf; stroke-width: 1.6; }
    .b    { fill: #faf7f3; stroke: #e2d9cf; stroke-width: 1.1; }
    .ba   { fill: #ffffff; stroke: #b8552f; stroke-width: 1.6; }
    .ea   { stroke: #b8552f; stroke-width: 2.4; fill: none; }
    .er   { stroke: #2e7d5b; stroke-width: 2.4; fill: none; }
    .ed   { stroke: #7a6f64; stroke-width: 1.2; fill: none; stroke-dasharray: 5 4; }
    .t    { fill: #2a231d; font-size: 14px; font-weight: 700; }
    .s    { fill: #2a231d; font-size: 11.5px; }
    .m    { fill: #7a6f64; font-size: 11px; }
    .cap  { fill: #7a6f64; font-size: 12px; font-weight: 700; letter-spacing: .08em; }
    .num  { fill: #ffffff; font-size: 11px; font-weight: 700; text-anchor: middle; }
  </style>
  <defs>
    <marker id="za" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
      <path d="M0,0 L8,4.5 L0,9 z" fill="#b8552f"/></marker>
    <marker id="zr" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
      <path d="M0,0 L8,4.5 L0,9 z" fill="#2e7d5b"/></marker>
    <marker id="zm" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M0,0 L7,4 L0,8 z" fill="#7a6f64"/></marker>
  </defs>

  <!-- 利用者 -->
  <rect class="zone" x="24" y="60" width="180" height="180" rx="10"/>
  <text class="cap" x="40" y="84">利用者</text>
  <rect class="b" x="40" y="100" width="148" height="76" rx="8"/>
  <text class="t" x="54" y="126">ブラウザ</text>
  <text class="s" x="54" y="146">チャットなどの画面を</text>
  <text class="s" x="54" y="162">開くだけ（導入物なし）</text>
  <text class="m" x="40" y="222">権限は一般／管理者の2段階</text>

  <!-- アプリサーバ -->
  <rect class="zone" x="252" y="36" width="500" height="540" rx="10"/>
  <text class="cap" x="268" y="60">アプリサーバ（1台）</text>

  <rect class="b" x="276" y="76" width="452" height="62" rx="8"/>
  <text class="t" x="290" y="100">画面と認証</text>
  <text class="s" x="290" y="120">ログイン・権限の入口。回答は逐次表示でブラウザへ流す</text>

  <rect class="ba" x="276" y="162" width="452" height="102" rx="8"/>
  <text class="t" x="290" y="186">AIオーケストレーション</text>
  <text class="s" x="290" y="206">質問を計画に → ツールを選んで実行 → 結果を検算 → 回答を組み立て</text>
  <text class="s" x="290" y="222">データの知識（カタログ）を毎回添えて、AIモデルと必要なだけ往復</text>
  <text class="m" x="290" y="244">往復は上限つき。実行の中身はすべて記録され、画面から確認できる</text>

  <rect class="b" x="276" y="288" width="452" height="76" rx="8"/>
  <text class="t" x="290" y="312">ツール群（回答づくりの部品）</text>
  <text class="s" x="290" y="332">データ検索・集計・統計・グラフ・ファイル出力・文書検索・メール下書き など</text>
  <text class="m" x="290" y="350">実名と説明は下の「ツール一覧」に自動表示（管理者が追加・停止できる）</text>

  <rect class="b" x="276" y="388" width="452" height="62" rx="8"/>
  <text class="t" x="290" y="412">取り込み・定期実行</text>
  <text class="s" x="290" y="432">Excel/CSVを表に変換。データベースへ書き込む唯一の経路（AIは書けない）</text>

  <rect class="b" x="276" y="474" width="452" height="62" rx="8"/>
  <text class="t" x="290" y="498">データカタログ管理（管理者）</text>
  <text class="s" x="290" y="518">説明・関連・用語・例文・検算・ER図を編集し、AIに渡す知識を育てる</text>

  <!-- 右列 -->
  <rect class="zone" x="800" y="36" width="376" height="104" rx="10"/>
  <text class="cap" x="816" y="60">AIモデル（外部API）</text>
  <rect class="b" x="816" y="72" width="344" height="52" rx="8"/>
  <text class="s" x="830" y="92">本番=ChatGPT-API ⇄ 開発=ローカルLLM</text>
  <text class="m" x="830" y="110">コードを変えず、設定だけで切り替え</text>

  <rect class="zone" x="800" y="164" width="376" height="150" rx="10"/>
  <text class="cap" x="816" y="188">データ層</text>
  <rect class="b" x="816" y="200" width="344" height="50" rx="8"/>
  <text class="t" x="830" y="220">データベース（SQLite・1つ）</text>
  <text class="s" x="830" y="238">全テーブルがここに入る。AIからは読み取り専用</text>
  <rect class="b" x="816" y="256" width="344" height="46" rx="8"/>
  <text class="t" x="830" y="276">データカタログ（知識の置き場）</text>
  <text class="s" x="830" y="292">説明・関連・用語・例文・検算。全員で1つを共有</text>

  <rect class="zone" x="800" y="338" width="376" height="96" rx="10"/>
  <text class="cap" x="816" y="362">文書検索サーバ群</text>
  <rect class="b" x="816" y="374" width="344" height="48" rx="8"/>
  <text class="s" x="830" y="394">社内文書のナレッジベース（LightRAG・複数台）</text>
  <text class="m" x="830" y="412">登録簿で追加・停止。一覧は下の「サーバ一覧」に自動表示</text>

  <rect class="zone" x="800" y="458" width="376" height="96" rx="10"/>
  <text class="cap" x="816" y="482">記録</text>
  <rect class="b" x="816" y="494" width="344" height="48" rx="8"/>
  <text class="s" x="830" y="514">チャット履歴・実行ログ・各種設定</text>
  <text class="m" x="830" y="532">サーバ内のファイルに保存</text>

  <!-- 質問の道（茶） -->
  <path class="ea" d="M188 116 H276" marker-end="url(#za)"/>
  <circle cx="216" cy="116" r="9" fill="#b8552f"/><text class="num" x="216" y="120">1</text>
  <text class="m" x="200" y="102">質問</text>

  <path class="ea" d="M728 190 C770 176, 780 150, 812 118" marker-end="url(#za)"/>
  <circle cx="770" cy="162" r="9" fill="#b8552f"/><text class="num" x="770" y="166">2</text>
  <text class="m" x="700" y="152">思考を依頼</text>

  <path class="ea" d="M812 130 C784 168, 772 190, 732 214" marker-end="url(#za)"/>
  <circle cx="782" cy="192" r="9" fill="#b8552f"/><text class="num" x="782" y="196">3</text>

  <path class="ea" d="M728 316 C766 300, 780 264, 812 232" marker-end="url(#za)"/>
  <circle cx="772" cy="284" r="9" fill="#b8552f"/><text class="num" x="772" y="288">4</text>
  <path class="ea" d="M728 340 C766 348, 780 368, 812 388" marker-end="url(#za)"/>

  <!-- 回答の道（緑） -->
  <path class="er" d="M276 128 H188" marker-end="url(#zr)"/>
  <circle cx="232" cy="128" r="9" fill="#2e7d5b"/><text class="num" x="232" y="132">5</text>
  <text class="m" x="212" y="148">回答</text>

  <!-- 知識・記録の供給（点線） -->
  <path class="ed" d="M812 268 C776 258, 760 240, 732 232" marker-end="url(#zm)"/>
  <text class="m" x="744" y="252">知識を添える</text>
  <path class="ed" d="M728 418 C780 402, 792 300, 812 230" marker-end="url(#zm)"/>
  <text class="m" x="762" y="404">書き込み</text>
  <path class="ed" d="M728 505 C760 508, 780 510, 812 512" marker-end="url(#zm)"/>
  <text class="m" x="748" y="528">実行の記録</text>

  <!-- 読み方 -->
  <text class="m" x="252" y="602">読み方: ❶質問 → ❷カタログの知識を添えてAIモデルへ → ❸ツール実行の指示 → ❹データに触れるのはツールだけ（②〜④を必要なだけ往復）→ ❺回答が画面へ。</text>
</svg>
      </div>
    </div>
  </div>

  <div class="card mt">
    <div class="card__title">サーバ一覧（接続先のURL）</div>
    <div class="card__desc">
      アプリ本体はこのページのURLのポート8000です（例: <code>http://サーバのIP:8000</code>）。
      ナレッジベースの一覧は「ナレッジベース」画面の登録簿から、いまの状態をそのまま表示しています。
    </div>
    <div class="tablewrap">
      <table class="data">
        <thead><tr><th style="width:220px">ナレッジベース</th><th>URL</th>
                   <th style="width:80px">状態</th><th style="width:90px">APIキー</th></tr></thead>
        <tbody>
        {% for b in bases %}
          <tr>
            <td>{{ b.name }}</td>
            <td class="small mono">{{ b.base_url }}</td>
            <td>{{ '有効' if b.enabled else '停止' }}</td>
            <td class="small muted">{{ '設定済み' if b.has_api_key else '未設定' }}</td>
          </tr>
        {% endfor %}
        </tbody>
      </table>
    </div>
    <div class="small muted mt">
      接続の生死・文書件数の確認は LightRAG 側の <code>check-servers.ps1</code> でまとめて行えます。
      環境の切替（本番=ChatGPT-API ⇄ 開発=ローカルLLM）はコードを変えずに設定ファイルだけで
      行います。手順はバンドル直下の「本番切替手順.md」へ。
    </div>
  </div>
  {% endif %}

  <div class="card mt">
    <div class="card__title">まとまりとテーブルの一覧（{{ groups_now|length }}まとまり・{{ total_tables }}表）</div>
    <div class="card__desc">
      いまのデータベースの中身をそのまま表示しています（追加・改名・削除は自動で反映されます）。
      実際のテーブル名は「まとまり__テーブル名」です（例:
      {% if groups_now %}<code>{{ groups_now[0].key }}__{{ groups_now[0].tables[0].suffix }}</code>{% endif %}）。
    </div>
    <div class="tablewrap">
      <table class="data">
        <thead><tr><th style="width:240px">まとまり</th><th>テーブル（行数）</th></tr></thead>
        <tbody>
        {% for gr in groups_now %}
          <tr>
            <td><b>{{ gr.key }}</b>
                <span class="muted small">{{ gr.tables|length }}表</span>
                {% if gr.memo %}<span class="badge badge--ok">メモあり</span>{% endif %}</td>
            <td class="small">
              {%- for t in gr.tables -%}
                <span class="mono">{{ t.suffix }}</span>{% if t.rows is not none %}<span class="muted">（{{ '{:,}'.format(t.rows) }}）</span>{% endif %}
                {%- if not loop.last %}、 {% endif -%}
              {%- endfor -%}
            </td>
          </tr>
        {% endfor %}
        </tbody>
      </table>
    </div>
  </div>

  <div class="card mt">
    <div class="card__title">ツール一覧（{{ tools_now|length }}件）</div>
    <div class="card__desc">
      AIが回答づくりに使える処理の一覧で、いまの状態をそのまま表示しています。
      管理者がデータカタログの「ツール」で行った無効化・説明の差し替え・ユーザー定義ツールの
      追加は、自動でここに反映されます。
    </div>
    <div class="tablewrap">
      <table class="data">
        <thead><tr><th style="width:240px">ツール</th><th>説明</th>
                   <th style="width:100px">種別</th><th style="width:70px">状態</th></tr></thead>
        <tbody>
        {% for t in tools_now %}
          <tr>
            <td>{% if t.label %}<b>{{ t.label }}</b><br>{% endif %}
                <span class="mono small muted">{{ t.name }}</span></td>
            <td class="small">{{ t.desc }}</td>
            <td class="small">{{ t.kind }}</td>
            <td>{{ '有効' if t.enabled else '停止' }}</td>
          </tr>
        {% endfor %}
        </tbody>
      </table>
    </div>
  </div>

  <!-- ==================================================================== -->
  <!-- 第3部 技術仕様 -->
  <!-- ==================================================================== -->
  <h2 id="spec" class="mt" style="font-size:20px">第3部 技術仕様</h2>

  <div class="card mt">
    <div class="card__desc">
      ここから先は、実装のとおりに書いた技術者向けの章です。処理の順序・判定条件・
      しきい値・上限をすべて載せています。数値は現在の設定値で、
      「変更可」は起動フォルダの <code>env</code> ファイルで上書きできるもの、
      「固定」は <code>config.py</code> を書き換えないと変わらないものです。
    </div>
  </div>

  <div class="card mt">
    <div class="card__title">3-1. 実行基盤</div>
    <div class="tablewrap">
      <table class="data">
        <thead><tr><th style="width:210px">項目</th><th>内容</th></tr></thead>
        <tbody>
          <tr><td>構成</td>
              <td>Python + Flask の1プロセス。画面（Jinja2テンプレート）とAPIを同じサーバが返します。
                  機能ごとに11個のブループリント（チャット／カタログ／取り込み／メール／モデル／
                  ナレッジ／表示／ヘルプ／認証ほか）に分かれています。</td></tr>
          <tr><td>起動</td>
              <td><code>python core.py</code>。内部では waitress（1プロセス・マルチスレッドの
                  本番用サーバ・スレッド8）が待ち受けるため、<b>開発も本番も同じコマンド</b>で起動できます。
                  ホストは全アドレス（0.0.0.0）、ポートは <b>8000</b>、
                  デバッグは既定で無効（切り替えは core.py 末尾の DEBUG。有効にするとブラウザからサーバ上のコードを実行できてしまうため、本番では False のまま）。
                  <b>起動コード（core.py 末尾）は環境変数を読みません</b>（他のソフトが設定した PORT を拾う事故を避けるため）。</td></tr>
          <tr><td>本番向けの起動</td>
              <td>同じ <code>python core.py</code> のままで本番運用できます。コマンドから直接起動する
                  <code>waitress-serve --host=0.0.0.0 --port=8000 --threads=8 --call core:create_app</code> や
                  <code>gunicorn -w 1 -b 0.0.0.0:8000 'core:create_app()'</code> も同等です。
                  <b>ワーカーは必ず1本</b>（スケジューラのスレッドがワーカー数だけ立ち、同じ取り込みを
                  多重実行するため）。同時アクセスはスレッド数で稼ぎます。
                  前段にnginxを置く場合は逐次表示のため <code>proxy_buffering off;</code> が必要です。</td></tr>
          <tr><td>起動時の処理順</td>
              <td>設定 → ブループリント登録 → リクエスト前処理の登録 → 管理者不在の警告 →
                  DBが無ければ空DBを作成 → 応答ヘッダに <code>Cache-Control: no-store</code> →
                  取り込みスケジューラ開始。</td></tr>
          <tr><td>アップロード上限</td>
              <td>1リクエスト 64MB（サーバ全体）。取り込みファイルは別途100MB制限（後述）。</td></tr>
          <tr><td>CLI</td>
              <td><code>python core.py users list|add|passwd|remove</code>（利用者管理）と
                  <code>python core.py refresh [--all|--job ID|--list]</code>（定期取り込みの実行）。
                  refresh の終了コードは 0=全成功または対象なし、1=1本でも失敗。cronから叩けます。</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="card mt">
    <div class="card__title">3-2. 1つの質問が処理される順序</div>
    <div class="card__desc">
      AIは「考える → 道具を使う → 結果を見てまた考える」を繰り返します。その繰り返しの制御が以下です。
    </div>
    <div class="tablewrap">
      <table class="data">
        <thead><tr><th style="width:210px">段階</th><th>内容</th></tr></thead>
        <tbody>
          <tr><td>前処理</td>
              <td>質問の空チェック → API設定の確認 → 結果キャッシュの「今回の質問」の区切りを打つ →
                  会話の読み込み → 画像の検査 → <b>先に質問を保存</b>（途中で切れても質問は残る）→
                  対象テーブルの決定 → リアルタイム取り込みの確認 →
                  最新のカタログでシステムプロンプトを作り直して先頭に差し替え。</td></tr>
          <tr><td>往復の上限</td>
              <td><b>10回</b>（変更可）。上限に達すると最終回答をまとめ、
                  「ツールの呼び出しが10回に達したので、ここで一区切りにしました」と表示します。</td></tr>
          <tr><td>同じ呼び出しの検出</td>
              <td>同じ（ツール名・引数）の組み合わせは<b>2回目から実行せず差し戻し</b>、
                  差し戻しが2回続いたら打ち切って回答をまとめます。成功の繰り返しと
                  失敗の連鎖でメッセージを出し分けます。</td></tr>
          <tr><td>空応答</td>
              <td>本文もツール呼び出しも無い応答は、履歴から取り除いて<b>1回だけ</b>やり直します
                  （この再試行も10回のうち1回を消費）。</td></tr>
          <tr><td>出力が途中で切れた場合</td>
              <td>モデルの出力上限に達した回答には「『続けて』と送ると続きを書きます」の注記を付けます。</td></tr>
          <tr><td>ツールの失敗</td>
              <td>アプリ側では再試行しません。エラーの内容をAIに返し、AIが引数を直して呼び直します
                  （同じ引数なら上記の重複検出で止まります）。</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="card mt">
    <div class="card__title">3-3. システムプロンプトの構成</div>
    <div class="card__desc">
      毎回この順で組み立て直します（会話ごとに固定せず、カタログの変更が即座に効くようにするため）。
    </div>
    <div class="tablewrap">
      <table class="data">
        <thead><tr><th style="width:60px">順</th><th style="width:250px">ブロック</th><th>内容</th></tr></thead>
        <tbody>
          <tr><td>1</td><td>導入文</td><td>役割の宣言。文書検索が使えるかどうかで2種類。</td></tr>
          <tr><td>2</td><td># 振る舞い</td>
              <td>実データを根拠にする・推測で答えない・日本語・用語集に従う。
                  登録の提案は1回の回答につき最大1つ。検算の警告が来たら末尾に注記する。</td></tr>
          <tr><td>3</td><td># 可視化の方針</td><td>グラフの使い分けと、同じデータの使い回し方。</td></tr>
          <tr><td>4</td><td># SQLで書けないこと</td><td>統計・予測などは専用ツールを使うこと。</td></tr>
          <tr><td>5</td><td># ファイル出力</td><td>Excel/CSV/Word/PowerPointの作り方。</td></tr>
          <tr><td>6</td><td># 利用可能なツール</td><td>権限と有効・無効を反映した一覧（名前・引数・説明）。</td></tr>
          <tr><td>7</td><td># 社内文書</td><td>検索対象を1件も選んでいなければ、このブロックごと出しません。</td></tr>
          <tr><td>8</td><td># 状態に問題があるデータ</td><td>定期取り込みが失敗している表があるときだけ。</td></tr>
          <tr><td>9</td><td># SQLルール</td><td>書き方の約束。</td></tr>
          <tr><td>10</td><td># 選択中のデータカタログ</td>
              <td>表・列の説明、主キー、結合キー、まとまりのメモ、用語、例文。詳細は次項。</td></tr>
          <tr><td>11</td><td>現在時刻</td><td>秒までのISO形式（「今月」などの相対表現の基準）。</td></tr>
        </tbody>
      </table>
    </div>
    <div class="small muted mt">
      カタログ本文の見出しは <code>## 使えるデータ</code> / <code>結合キー（JOINにはこれを使う）:</code> /
      <code>テーブルをまたぐ業務用語（質問にこの言葉が出たら必ずこの定義に従う）:</code> /
      <code>正しいと確認済みの質問とSQLの例:</code>。表ごとは
      <code>### 表名（N行）</code> と列一覧・サンプル3行。
      <b>検算だけはプロンプトに載りません</b>（ツールの実行結果に混ぜ込む方式）。
    </div>
  </div>

  <div class="card mt">
    <div class="card__title">3-4. AIに見せるテーブルの決め方</div>
    <div class="tablewrap">
      <table class="data">
        <thead><tr><th style="width:210px">段階</th><th>内容</th></tr></thead>
        <tbody>
          <tr><td>① 利用者の選択</td>
              <td>サイドバーで外した表を最初に落とします。0件になればそこで終了。</td></tr>
          <tr><td>② 全部入るか判定</td>
              <td>カタログ全文の文字数が上限以下なら<b>絞らずに全部渡します</b>（選び漏れゼロ・
                  プロンプトが毎回同じで再利用が効く）。動作モードは auto（既定）／router（常に絞る）／
                  all（常に全部）の3種。</td></tr>
          <tr><td>上限の計算</td>
              <td><code>モデルの文脈長 × 0.5 ÷ 0.55</code>を、下限4,000字・上限400,000字で丸めた値。
                  例: 文脈長105万のモデル → 40万字（上限で頭打ち）、12.8万のモデル → 約11.6万字。</td></tr>
          <tr><td>③ 表ルーター</td>
              <td>収まらないときだけ、質問文と<b>要約版</b>カタログを別のモデル呼び出しに渡して
                  関係する表を選ばせます。表の総数が8以下なら呼びません。
                  使うモデルは画面で選んだものではなく<b>設定で固定されたモデル</b>、温度0・最大300トークン、
                  直前の質問3件を手がかりに渡します。失敗したら<b>絞らずに要約モードへ</b>
                  （ルーターの不調で答えられなくなるのが最悪のため）。</td></tr>
          <tr><td>④ 会話中の表を復活</td>
              <td>この会話で実際にSQLが触った表は、ルーターの選から漏れても必ず戻します
                  （「それをグラフに」のような続きの質問のため）。</td></tr>
          <tr><td>⑤ 関連から1ホップ補完</td>
              <td>登録済みの関連をたどり、選ばれた表が参照している先（マスタ等）を機械的に足します。
                  <b>子→親の一方向・1ホップだけ</b>（逆方向や連鎖にすると芋づる式に増えるため）。</td></tr>
          <tr><td>⑥ それでも溢れたら</td>
              <td>詳細版をやめて要約版（列名なし）に落とし、その旨の注意書きを添えます。</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="card mt">
    <div class="card__title">3-5. 文脈長の見積り</div>
    <div class="card__desc">
      文字数からトークン数を推定する係数は、日本語主体の本文が <b>0.55</b>、ツール定義のJSONが <b>0.31</b>
      （実測にもとづく値）。モデル設定画面の使用量メーターは、推定ではなく実際に組み立てた
      プロンプトを測って表示します。
    </div>
    <div class="tablewrap">
      <table class="data">
        <thead><tr><th style="width:280px">モデル</th><th>文脈長（トークン）</th></tr></thead>
        <tbody>
          <tr><td>gpt-5.6 系</td><td>1,050,000</td></tr>
          <tr><td>gpt-4.1 系</td><td>1,047,576</td></tr>
          <tr><td>gpt-5 / mini / nano</td><td>400,000</td></tr>
          <tr><td>o1 / o3 / o4 系</td><td>200,000（o1-mini のみ 128,000）</td></tr>
          <tr><td>gpt-4o / gpt-4o-mini / gpt-4-turbo</td><td>128,000</td></tr>
          <tr><td>gpt-4-32k / gpt-4</td><td>32,768 / 8,192</td></tr>
          <tr><td>gpt-3.5-turbo 系</td><td>16,385</td></tr>
          <tr><td>表に無いモデル</td><td>128,000として扱い、画面に「推定」と表示（管理者が上書き可）</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="card mt">
    <div class="card__title">3-6. 逐次表示（ストリーミング）と会話履歴</div>
    <div class="tablewrap">
      <table class="data">
        <thead><tr><th style="width:210px">項目</th><th>内容</th></tr></thead>
        <tbody>
          <tr><td>通信方式</td>
              <td>Server-Sent Events。イベントは5種類 —
                  <code>delta</code>（文字が届くたび）/ <code>text_end</code>（ひとまとまり終了）/
                  <code>running</code>（ツール実行開始。日本語名を添えて表示）/
                  <code>item</code>（表・グラフ・ファイルなどの描画物）/ <code>end</code>（会話IDとタイトル）。</td></tr>
          <tr><td>中断したとき</td>
              <td>画面を閉じる・更新すると接続が切れます。<b>そこまでの内容は必ず保存されます</b>
                  （完了イベントだけ送られません）。</td></tr>
          <tr><td>履歴の2本立て</td>
              <td><code>messages</code>（AIに送る列）と <code>render_log</code>（画面に描く列）を別に持ちます。
                  システムプロンプトは保存せず、開くたびに最新のカタログで作り直します。</td></tr>
          <tr><td>APIに送る量</td>
              <td>選んでいるモデルが一度に読める量に収まるよう、<b>古いやり取りから順に外して送ります</b>
                  （直近のやり取りと、いちばん最初の指示は必ず残します）。要約はしません。
                  外したぶんは「（以前のやり取りは省略しています）」と伝わるので、
                  AIが勝手に忘れたふりをすることはありません。<br>
                  質問に付けた画像は、直近の何回かを過ぎると本文から外します
                  （画面の表示には残ります）。1枚で数MBあるものを毎回送り続けないためです。<br>
                  ツールの結果は残したまま送ります。長い会話ほど費用と時間は増えますが、
                  上限を超えて失敗することはありません。</td></tr>
          <tr><td>書き直して送信</td>
              <td>指定した「何回目の発言か」の直前で、AIに送る列と画面の列をそれぞれ切り詰めます。
                  本文を空で送ると巻き戻すだけ（元の文面を入力欄に戻す）。この経路は常に非ストリーミング。</td></tr>
          <tr><td>時刻</td>
              <td>各アイテムに秒精度の時刻が付きます（質問は送信時刻、回答は完了時刻）。</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="card mt">
    <div class="card__title">3-7. モデル呼び出しの再試行</div>
    <div class="tablewrap">
      <table class="data">
        <thead><tr><th style="width:210px">種類</th><th>挙動</th></tr></thead>
        <tbody>
          <tr><td>混雑（レート制限）</td>
              <td>最大<b>3回</b>まで待って投げ直します（変更可）。待ち時間は
                  ①応答の <code>retry-after</code> ②エラー文中の「try again in …」＋0.5秒
                  ③手がかりが無ければ 2秒→4秒→8秒 の順で決め、いずれも<b>20秒</b>で頭打ち。
                  3回で解消しなければ、ここまでのデータは残したまま中断を知らせます。
                  OpenAIのSDK自体も2回再試行するので、その上乗せになります。</td></tr>
          <tr><td>モデルが受け付けない引数</td>
              <td>エラー文を読んで引数を直し、最大4回まで投げ直します（推論の指定・温度・
                  最大トークンの指定方法の違いを吸収）。学習した調整はプロセスが動いている間だけ覚えます。</td></tr>
          <tr><td>それ以外の失敗</td>
              <td>再試行せず、原因ごとに読みやすい文言へ変換して画面に出します
                  （応答の乱れ／ローカルLLMのメモリ不足／時間切れ ほか）。</td></tr>
          <tr><td>共通の設定</td>
              <td>温度は<b>0</b>（SQL生成の安定のため）、上位確率と最大トークンは既定で未指定、
                  ツールの選択は常にAIに任せる設定。</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="card mt">
    <div class="card__title">3-8. SQL実行の安全機構（4層）</div>
    <div class="card__desc">
      AIが書いたSQLは、次の4つの関門をすべて通ったものだけが実行されます。
    </div>
    <div class="tablewrap">
      <table class="data">
        <thead><tr><th style="width:180px">層</th><th>内容</th></tr></thead>
        <tbody>
          <tr><td>① 構文の検査</td>
              <td>前後の空白と末尾の <code>;</code> を落とし、<b>引用符の中身を伏せた検査用のコピー</b>を作って
                  コメントを除去してから判定します（文字列の中の「delete」やセミコロンで誤判定しないため。
                  実行するのは元のSQL）。拒否するのは —
                  空／複数文（<code>;</code> が残る）／<code>SELECT</code>・<code>WITH</code> 以外で始まる／
                  書き込み・定義系の語（insert, update, delete, drop, alter, create, truncate, attach,
                  detach, reindex, vacuum, pragma, grant, revoke, begin, commit, rollback, savepoint,
                  merge の19語）／<code>REPLACE INTO</code> の並び。
                  なお単独の <code>replace</code> は文字列関数なので通します。</td></tr>
          <tr><td>② 読み取り専用で接続</td>
              <td>空のメモリDBを土台に、各データベースを<b>読み取り専用モード</b>で接続します。
                  1つのSQLで扱えるのは10個まで（SQLiteの制限）。</td></tr>
          <tr><td>③ 実行直前の遮断</td>
              <td>SQLiteの認可コールバックで、許可するのは「参照」「読み取り」「関数呼び出し」だけ。
                  さらに<b>選択されていない表への読み取りはその場で拒否</b>します。
                  プロンプトから消すだけではAIが名前を覚えている場合に読めてしまうため、
                  最後の関門をデータ層に置いています。</td></tr>
          <tr><td>④ 時間と件数の制限</td>
              <td>実行時間は<b>10秒</b>（SQLiteの命令1万回ごとに経過を確認して中断）。
                  取得は<b>2,000行</b>まで（上限+1行だけ取って「超えたか」を判定し、
                  超えていれば実際の総件数を数え直して警告を添えます）。
                  ファイル出力だけは別枠で最大100万行（Excelは1,048,575行で丸め）。
                  AIに渡すのは先頭40行だけで、画面には全行渡します。</td></tr>
        </tbody>
      </table>
    </div>
    <div class="small muted mt">
      補足: データの選択は「見る範囲を絞る」ためのもので、③の遮断が実際のアクセス制御です。
      カタログ画面の検証機能など、SQLが名指ししたデータベースは選択外でも接続されます。
    </div>
  </div>

  <div class="card mt">
    <div class="card__title">3-9. エラーの言い換えと結果の使い回し</div>
    <div class="tablewrap">
      <table class="data">
        <thead><tr><th style="width:210px">項目</th><th>内容</th></tr></thead>
        <tbody>
          <tr><td>エラーの変換</td>
              <td>SQLiteのエラーは「何が悪いか」だけでなく「次に何をすべきか」まで書いた文に置き換えます。
                  <b>存在しない関数</b>は代わりに使うものを名指しで案内（24語の対応表。標準偏差・中央値・
                  パーセンタイル→統計ツール、相関→相関分析、date_trunc→strftime、concat→<code>||</code>、
                  top→LIMIT など）。<b>列名の誤り</b>は「推測で列名を作らず describe_table で確認」、
                  <b>構文エラー</b>は「ウィンドウ関数の一部・PIVOTは使えない、専用ツールに任せる」と添えます。
                  これを添えないとAIが同じ書き方を何度も繰り返します。</td></tr>
          <tr><td>結果の使い回し</td>
              <td>取得したデータには識別子（result_id）が付き、後続のツールはSQLの代わりに
                  それを指せます（「集計→グラフ→レポート」で同じSQLが3回走るのを防ぐ）。
                  <b>覚えておくのは40件・総セル数40万まで</b>で、超えると古いものから捨てます。
                  時間による期限はなく、プロセスを再起動すると消えます。</td></tr>
          <tr><td>取り違え防止</td>
              <td>識別子は「同じデータの選択範囲」でしか引けません（当てずっぽうのIDで
                  選んでいないデータは出ません）。AIが指示に従わず同じSQLを書き直してきた場合も、
                  <b>同じ質問の中で・同じ範囲で・空白の違いを無視して同一</b>なら機械的に使い回します。</td></tr>
          <tr><td>切り詰めの引き継ぎ</td>
              <td>2,000行で切れたデータを、より多くの行を扱えるツール（ファイル出力）が使うときは、
                  元のSQLで自動的に取り直します。</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="card mt">
    <div class="card__title">3-10. ツール基盤</div>
    <div class="tablewrap">
      <table class="data">
        <thead><tr><th style="width:210px">項目</th><th>内容</th></tr></thead>
        <tbody>
          <tr><td>定義の形式</td>
              <td>OpenAIのfunction calling形式（名前・説明・引数のJSONスキーマ）。
                  グラフ系は共通の引数定義から機械生成しています。
                  実際に渡る一覧は下の「ツール一覧」に自動表示されます。</td></tr>
          <tr><td>AIに渡すまでの絞り込み</td>
              <td>権限で除外（管理者専用のツールは一般利用者のAIには渡しません）→
                  管理者が無効にしたものを除外 → 説明の差し替えを適用 →
                  文書検索ツール（登録があるときだけ・選択中の対象名を埋め込んで動的生成）→
                  ユーザー定義ツール（定義に不備が無いものだけ）。</td></tr>
          <tr><td>引数の受け取り</td>
              <td>配列で受ける引数に文字列が1つ来たら要素1つの配列に直します
                  （直さないと日本語の列名が1文字ずつに散り、「『地』という列がありません」という
                  意味不明なエラーになります）。必須引数が欠けていれば、
                  何が足りないかと確認方法を添えて差し戻します。0やfalseは正しい値として通します。</td></tr>
          <tr><td>実行の流れ</td>
              <td>引数のJSON解釈 → 権限チェック → 引数の整形 → 必須チェック →
                  引数の木を再帰的にたどってSQLを収集（レポートの節やExcelのシートの中まで）→
                  実行 → 検算の自動割り込み。<b>ツール内の例外はすべて捕まえて</b>
                  エラーとして返します（1つの失敗でアプリを落とさない）。</td></tr>
          <tr><td>SQLの日本語解説</td>
              <td>SQLを組み立てるツール（24種）の宣言に <code>explanation</code> 引数を
                  <b>ツール定義の組み立て時に一括で足して</b>います（1か所で配るので、
                  ツールを増やしても自動で付きます）。AIはSQLと同じ呼び出しの中で解説も書くため、
                  <b>追加のAI呼び出しは発生しません</b>。必須にはしていないので、解説が無くても
                  SQLは実行されます（過去の会話も従来どおり表示されます）。
                  ユーザー定義ツールのSQLは人が登録したものなので、AIの解説ではなく
                  登録時の説明文を出します。</td></tr>
          <tr><td>2つの戻り値</td>
              <td>AI向け（トークン節約のため先頭40行と要約）と画面向け（全行）を作り分けます。
                  グラフはAI向けに行データを入れず「描画した」という事実と識別子だけを返します。</td></tr>
          <tr><td>ユーザー定義ツール</td>
              <td>Pythonは書かせず、SQLとパラメータ定義だけ。パラメータは必ずバインド変数として渡すので
                  SQLインジェクションは起こりません。検査は — 名前（英字始まり・英数字と_・48文字以内・
                  組み込みや既存と重複しない）／説明必須／SQL必須／パラメータ名と型／
                  <b>SQL中の <code>:名前</code> と定義の対応を双方向で</b>／出力形式ごとの必要項目。</td></tr>
          <tr><td>組み込みの上書き</td>
              <td>無効化は「どれか1つのデータで無効なら無効」（安全側）、説明は最初に見つかったものを採用。</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="card mt">
    <div class="card__title">3-11. データの自動プロファイル</div>
    <div class="card__desc">
      人が何も書かなくても分かることは、AIに渡す前に自動で調べます。
    </div>
    <div class="tablewrap">
      <table class="data">
        <thead><tr><th style="width:210px">項目</th><th>内容</th></tr></thead>
        <tbody>
          <tr><td>集める情報</td>
              <td>列（名前・型・NULL可否・主キーと複合キー内の順番）／外部キー宣言／行数／
                  サンプル<b>5行</b>／列ごとの統計。ビューも対象です。</td></tr>
          <tr><td>列の統計</td>
              <td>値の種類が<b>20以下</b>なら「値と件数の一覧（多い順）」を、
                  21以上なら「最小値と最大値」を持ちます。これがカタログ画面の「実際の値」欄と、
                  AIに渡すコード値の手がかりになります。行数200万を超える表は統計をスキップ。</td></tr>
          <tr><td>時間の制限</td>
              <td>プロファイル用の問い合わせは<b>30秒</b>で中断（行数だけ取れないときは「行数不明」）。</td></tr>
          <tr><td>キャッシュ</td>
              <td>結果は <code>data/.profile_cache/</code> にJSONで保存。
                  <b>更新時刻とファイルサイズが一致するときだけ</b>再利用します（内容のハッシュは取りません）。
                  カタログ本文の組み立て結果も、DB・カタログ・プロファイルの更新時刻をキーに
                  最大64件まで覚えます。</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="card mt">
    <div class="card__title">3-12. 整合性の警告（カタログ画面の⚠）</div>
    <div class="card__desc">
      カタログに書いてある内容が、実際のデータとずれていないかを毎回照合します。検出するのは次の8種類です。
    </div>
    <div class="tablewrap">
      <table class="data">
        <thead><tr><th style="width:280px">種類</th><th>判定</th></tr></thead>
        <tbody>
          <tr><td>説明のある表が存在しない</td><td>カタログにあってデータベースに無い（以降その表の検査は飛ばす）</td></tr>
          <tr><td>説明のある列が存在しない</td><td>同上（列単位）</td></tr>
          <tr><td>指定した主キーの列が無い</td><td>人が指定した主キーの列が実在しない</td></tr>
          <tr><td>関連の列が無い／表が無い</td><td>関連の端点が実在しない（他データベースを指すものは対象外）</td></tr>
          <tr><td>例文が存在しない表を使用</td><td>例文のSQLに、実在しない「まとまり__表名」が出てくる</td></tr>
          <tr><td>検算が存在しない表を使用</td><td>左右のSQLとドリルダウンを合わせて判定</td></tr>
          <tr><td>用語のSQL式が存在しない表を使用</td><td>SQL式を持つ用語のみ対象</td></tr>
        </tbody>
      </table>
    </div>
    <div class="small muted mt">
      表名の抽出はUnicode対応の語切り出しで行うため、日本語のテーブル名も正しく拾います。
      判定対象は「まとまり__表名」形式の名前だけです。
    </div>
  </div>

  <div class="card mt">
    <div class="card__title">3-13. 結合候補の判定ロジック</div>
    <div class="card__desc">
      ER図の「結合候補」ボタンで出る赤い点線は、次の3つの規則で作られます。
      すでに登録済みの関連と、データベースの外部キー宣言にあるものは候補から除きます。
    </div>
    <div class="tablewrap">
      <table class="data">
        <thead><tr><th style="width:200px">規則</th><th>条件</th></tr></thead>
        <tbody>
          <tr><td>① 列名からの推測</td>
              <td><code>〜_id</code> で終わる列について、<code>〜</code> / <code>〜s</code> / <code>〜es</code>
                  という名前の表を探します。相手の主キーが<b>複合キーなら候補にしません</b>
                  （1列だけで結ぶと誤りになるため）。結合先は相手の主キー、無ければ
                  <code>id</code> か同名の列。</td></tr>
          <tr><td>② 同じ名前の主キー</td>
              <td>相手の<b>単独主キー</b>と同じ名前の列を探します。
                  ただし「まとまり違いの同じ形の表どうし」（例: 拠点別の同名表）は除外。
                  同じまとまりの中に候補があればそちらを優先し、
                  <b>手がかりが無いまま候補が4つ以上あるときは曖昧すぎるとして出しません</b>。</td></tr>
          <tr><td>③ 値の一致からの発見</td>
              <td>列名が違っても、実データの値が重なっていれば候補にします。
                  自分側の値が<b>5種類以上</b>、相手側（単独主キー）も<b>5種類以上</b>で、
                  <b>一致率90%以上</b>が条件。さらに、同じまとまりに相手がいなければ
                  <b>相手が1つに絞れるときだけ</b>出します（日付列が全拠点のカレンダーに
                  一致してしまうような氾濫を防ぐため）。</td></tr>
          <tr><td>①②への一致率の付与</td>
              <td>名前から作った候補にも実データを当て、一致率を注記します。
                  <b>1件も重ならない候補は削除</b>します（結合しても1行も繋がらない＝間違い）。</td></tr>
          <tr><td>値の読み方</td>
              <td>対象は型がTEXTかINTEGERの列。1列あたり<b>最大200種類</b>を標本として読み、
                  単独主キーだけは<b>最大2万件</b>を全件読みます。結果はデータベースの更新時刻をキーに
                  キャッシュ（関連を触るたびに全列を読み直さないため）。</td></tr>
          <tr><td>実績からの候補</td>
              <td>上記とは別に、過去の分析SQLで実際にJOINされたのに未登録の組み合わせを、
                  使用回数の多い順に<b>8件まで</b>提示します。</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="card mt">
    <div class="card__title">3-14. 関連（リレーション）の扱い</div>
    <div class="tablewrap">
      <table class="data">
        <thead><tr><th style="width:210px">項目</th><th>内容</th></tr></thead>
        <tbody>
          <tr><td>多重度の表記</td>
              <td>N:1（多対1）／1:N（1対多）／1:1／N:M（多対多）。図の線には
                  <code>*</code> と <code>1</code> を両端に描きます（IPA表記に合わせ矢印は使いません）。</td></tr>
          <tr><td>向きの自動修正</td>
              <td>from/to は描画順ではなく「どちらが参照している側か」を表します。
                  片方だけが単独主キーなら、そちらを親側にして<b>自動で入れ替え、多重度も反転</b>します
                  （逆向きに登録されると参照整合性の検査が反対の意味になるため）。</td></tr>
          <tr><td>複合キーの結合</td>
              <td>複数列の組で1つの結合になる関連（複合キー）は、<b>1本の線</b>として登録します。
                  ER図では、対象の列それぞれから出た線がいったん合流し、1本の幹で相手側へ渡り、
                  相手側でまた各列へ分かれる形で描きます（1つの結合であることと、使っている列の
                  両方が分かるように）。
                  すでに関連がある表ペアへ2組目の列をドラッグすると「複合キーとして列を追加するか、
                  別の関連か」を確認します（作成者と承認者のように、同じ表を別の意味で2回参照する
                  関連は「別」が正解のため、機械では決めず人が選びます）。保存形式は
                  <code>表.(列1, 列2)</code> のように括弧で列をまとめ、AIには「全列を同時に
                  結合条件にする」と明示して渡します。列の組で一意になる場合は、
                  単独列の重複警告を出しません。</td></tr>
          <tr><td>登録時の実データ検証</td>
              <td>保存前に必ず実データを照合し、結果を3段階で返します。
                  <b>阻止</b>=値が1件も一致しない。<b>警告</b>=一致しない値が30%以上／型が違う／
                  主キー同士を結んでいる／参照先の値が一意でない／区分値とIDを結んでいる疑い
                  （相手の値が10種類以上あるのに自分は10種類以下で、相手の半分未満しか使っていない）。
                  <b>情報</b>=親に無い値が少しある。警告は確認のうえ強行できますが、阻止は保存できません。</td></tr>
          <tr><td>主キーの決め方</td>
              <td>人が指定した主キー（実在する列だけに絞る）→ データベースの宣言 → 無し、の順。
                  人が指定した場合はプロンプトに「（人が指定）」と明記し、複合キーなら
                  「結合するときは全列を条件にする」、キー無しなら「重複行があり得る」と添えます。</td></tr>
          <tr><td>線の濃さ</td>
              <td>全利用者の会話履歴から実行済みSQLを集め、JOINの端点を正規表現で解析して
                  使用回数を数えています（薄い灰色＝未使用）。向きは問わず同一視します。</td></tr>
          <tr><td>ER図の座標</td>
              <td>保存があればそれ、無ければ4列グリッドに自動配置。保存は送られたノードだけを
                  上書きするマージ方式で、壊れた項目は読み飛ばします（1つの不備で図全体が
                  出なくなるのを避けるため）。</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="card mt">
    <div class="card__title">3-15. 業務用語</div>
    <div class="tablewrap">
      <table class="data">
        <thead><tr><th style="width:210px">項目</th><th>内容</th></tr></thead>
        <tbody>
          <tr><td>構造</td>
              <td>1つの用語は「説明」と「SQL式（任意）」を持ちます。置き場所は
                  表ごとと全体（テーブルをまたぐ）の2階層。</td></tr>
          <tr><td>プロンプトへの載り方</td>
              <td>SQL式があれば「この式をそのまま使う」、無ければ「列情報をもとに自分で組み立てる」と
                  添えます。<b>説明だけでも効きます</b>。
                  表ごとの用語は、詳細を渡すときだけ定義を載せ、一覧のときは名前だけ知らせます。</td></tr>
          <tr><td>選択外への漏れ防止</td>
              <td>表を絞っているときは、<b>SQL式が表示中の表しか引かない</b>かつ
                  <b>説明文に表示外の表名が出てこない</b>用語だけを渡します
                  （説明文を素通しにすると、選んでいない表の名前と役割が漏れるため）。
                  関連と例文にも同じ絞り込みが掛かります。</td></tr>
          <tr><td>「検証」の判定</td>
              <td>式が触れる表を、①式中の表名 ②画面での選択 ③式中の語がすべて列名として存在する表
                  （最も列数の少ない＝限定的なもの1つ）の順で推定します。
                  複数表なら登録済みの関連でJOINを組み立て、関連が無ければ総当たりになる旨を注記します。
                  まず<b>条件式</b>として評価し（該当件数と全体件数、該当行を3行まで表示）、
                  失敗したら<b>計算式</b>として再評価します。</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="card mt">
    <div class="card__title">3-16. 例文と検算</div>
    <div class="tablewrap">
      <table class="data">
        <thead><tr><th style="width:210px">項目</th><th>内容</th></tr></thead>
        <tbody>
          <tr><td>例文の上限</td>
              <td><b>200件</b>。例文は毎回プロンプトに載るため、増やすほど表の説明が押し出されます。
                  上限を超えた分は保存されず、入らなかった件数を画面で知らせます（黙って捨てません）。</td></tr>
          <tr><td>例文の重複判定</td>
              <td>「質問文」と「空白と大小を無視したSQL」の<b>組み合わせ</b>が同じものだけを1件に。
                  質問文だけ・SQLだけの一致は重複としません（同じ質問に拠点ごとの別SQLが
                  正当に共存するため）。</td></tr>
          <tr><td>例文の検証</td>
              <td>実行して5行まで取得。判定は OK／0行（条件が厳しすぎないか）／エラー。</td></tr>
          <tr><td>検算の構造</td>
              <td>「一致するはずの2つのSQL」＋許容差＋不一致時に差の中身を見せるSQL。
                  左右のSQLは<b>1行1列の数値</b>を返すこと。許容差の既定は<b>0.5%</b>
                  （丸め誤差を拾わない程度）。</td></tr>
          <tr><td>検算の発火条件</td>
              <td>ツールが実行したSQLが触れた表と、検算の左右のSQLが触れる表が<b>重なるときだけ</b>走ります。
                  比較は「差 ÷ 左右の絶対値の大きい方 × 100」が許容差以下なら一致。両方0なら一致。
                  <b>一致したとき・実行できなかったときは何も言いません</b>
                  （毎回「問題ありません」と出しても読まれなくなるため）。
                  不一致のときだけ、画面とAIの両方に割り込みます。ドリルダウンは不一致時のみ実行し8行まで。</td></tr>
          <tr><td>検算のキャッシュ</td>
              <td>ルールの内容とデータの更新時刻の組でキャッシュ。同じ警告は1つの会話で1回だけ出します。</td></tr>
          <tr><td>検算の保存</td>
              <td>同じ名前は許します（拠点ごとに同名の検算を持つのが普通のため）。
                  内容が完全に同じものだけを1件に間引き、落とした件数を知らせます。</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="card mt">
    <div class="card__title">3-16b. ビュー</div>
    <div class="tablewrap">
      <table class="data">
        <thead><tr><th style="width:210px">項目</th><th>内容</th></tr></thead>
        <tbody>
          <tr><td>実体</td>
              <td>SQLiteの <code>CREATE VIEW</code>。保存されるのは<b>SELECT文だけ</b>で、データは複製されません
                  （20万行の表にビューを作ってもファイルは1バイトも増えません）。開くたびに元の表から
                  計算し直すので、常に最新です。書き込みはできません（読み取り専用）。</td></tr>
          <tr><td>作り方</td>
              <td>日本語で「欲しい一覧」を書くとAIがSQLを組み立て、その場で実データに当てて確かめます。
                  通らなければエラーを添えて1回だけ書き直させます。SQLを自分で書くこともできます。
                  保存前には必ず実行し、動かないSQLはカタログに入れません。</td></tr>
          <tr><td>安全</td>
              <td>定義SQLはSELECT専用ガードを通します（書き込み・DDL・複数文は登録できません）。
                  ビューを読むときも通常の権限が効き、<b>元の表を選択から外している人はビューも読めません</b>
                  （SQLiteのオーソライザが元の表への読み取りを止めるため）。</td></tr>
          <tr><td>扱い</td>
              <td>名前は表と同じ「まとまり__名前」の規約。登録するとテーブル一覧（「ビュー」の印つき）・
                  ER図・チャットの表選択に出て、説明・列の説明・用語も表と同じように付けられます。
                  削除すると定義だけが消え、元の表とデータは残ります。</td></tr>
          <tr><td>注意</td>
              <td>SQLiteには結果を保存しておく仕組み（マテリアライズドビュー）がありません。重い集計を
                  毎回計算することになるので、そのぶん時間がかかります。元の表を削除・改名すると
                  ビューは動かなくなり、一覧に「動きません」と出ます（作り直してください）。</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="card mt">
    <div class="card__title">3-17. 取り込みの内部処理</div>
    <div class="tablewrap">
      <table class="data">
        <thead><tr><th style="width:210px">項目</th><th>内容</th></tr></thead>
        <tbody>
          <tr><td>対応形式</td>
              <td><code>.csv .tsv .txt .xlsx .xlsm</code>（固定）。Excelとそれ以外は拡張子で分岐します。</td></tr>
          <tr><td>文字コードの推定</td>
              <td>CSV系は utf-8-sig → cp932 → utf-8 → shift_jis → euc_jp の順に試します。
                  全滅したら「UTF-8かShift_JISで保存し直してください」と案内。</td></tr>
          <tr><td>区切りの推定</td>
              <td>指定が無ければ .tsv はタブ、それ以外は自動判定。
                  画面ではカンマ／タブ／パイプ／セミコロン／空白も選べます。</td></tr>
          <tr><td>型の推定</td>
              <td>空白を除いて<b>全件が数値ならINTEGER/REAL、1件でも数値でなければTEXT</b>。
                  ただし<b>先頭ゼロ（0123）・桁区切り・全角数字・小数表記の整数</b>は
                  「コード」とみなしてTEXTのまま残します（社員番号の先頭ゼロが消える事故を防ぐため）。
                  <b>日付を判定する仕組みはなく、日付はTEXTになります</b>。
                  推定はプレビューが読む2,000行から行い、書き込み直前に全行を再検査して、
                  数値にできない値があればその列をTEXTに降格し、降格した列名を警告します。</td></tr>
          <tr><td>テーブル名の正規化</td>
              <td>全角を半角にし、記号と空白を <code>_</code> に。<b>日本語はそのまま残ります</b>。
                  数字始まりは先頭に <code>_</code>、SQLiteの予約語67語は末尾に <code>_</code>、
                  <b>64文字</b>で切り詰め。まとまりの区切り <code>__</code> だけは保持します。</td></tr>
          <tr><td>更新のしかた</td>
              <td>全件入れ替え（毎回DROPして作り直し）と追記（既存列と照合し、
                  足りない列があれば中止）。<b>取得日時列はどちらのモードでも必ず付きます</b>
                  （「いつ時点のデータか」が分からないと断面を説明できないため）。</td></tr>
          <tr><td>世代の保持</td>
              <td>追記のときだけ保持回数を指定（1〜<b>800</b>、既定値なし＝必ず自分で決める）。
                  古い世代の削除は取得日時の新しい順に指定回数だけ残し、それ以外を削除します
                  （取得日時が空の行は消しません）。</td></tr>
          <tr><td>件数と大きさの上限</td>
              <td>1テーブル<b>100万行</b>、1ファイル<b>100MB</b>、
                  フォルダの一覧は2,000件まで、プレビューは30行表示。</td></tr>
          <tr><td>取り込み元の制限</td>
              <td>許可フォルダの中だけ。実パスに解決してから判定するので <code>..</code> や
                  リンク経由の脱出はできません。ドライブ直下やファイルシステムのルートは登録を拒否。
                  Excelのロックファイル（<code>~$</code>）や隠しファイルは無視。
                  <b>データベースは data/ 直下にしか作れません</b>。
                  アップロードは既定で無効（サーバの許可フォルダに一本化した方が追跡でき、
                  定期取り込みにもそのまま載せられるため）。</td></tr>
          <tr><td>SQLの組み立て</td>
              <td>テーブル名・列名は引用符をエスケープして囲み、値は必ずプレースホルダで渡します。</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="card mt">
    <div class="card__title">3-18. 定期実行と後片付け</div>
    <div class="tablewrap">
      <table class="data">
        <thead><tr><th style="width:210px">項目</th><th>内容</th></tr></thead>
        <tbody>
          <tr><td>スケジューラ</td>
              <td>アプリ起動時に1本だけ常駐スレッドを立てます（多重起動はスレッド名で防止、
                  終了時に自動停止）。巡回は<b>60秒ごと</b>（最短5秒）。
                  間隔は 手動のみ／15分／1時間／3時間／6時間／1日／1週間。
                  次回時刻は「前回実行＋間隔」（未実行なら開始日時、無ければ即時）。
                  1周が例外で落ちてもループは止めません。</td></tr>
          <tr><td>実行時の安全弁</td>
              <td>元ファイルが許可フォルダ外なら実行しない／設定した列が1つもファイルに無ければ
                  「区切り・見出し行・シートが変わった可能性」として中止／
                  <b>データ0件（見出しだけ）なら失敗扱いにして前回の内容を残す</b>（表を空にしない）。
                  取り込みとジョブ定義の書き換えは同じ鍵で直列化します。</td></tr>
          <tr><td>問題の検出と通知</td>
              <td>失敗／型の降格／<b>予定の2周期ぶん遅れ</b>の3種を検出し、サイドバーの⚠・
                  AIへの注記・管理者へのメールに使います。通知は状態の<b>変わり目だけ</b>
                  （起動直後の1周目は送りません）。</td></tr>
          <tr><td>手動実行の制限</td>
              <td>追記モードで定期実行が設定されているものは手動実行できません
                  （次回予定がずれ、保存回数を1回余計に使うため）。</td></tr>
          <tr><td>削除の後片付け</td>
              <td>表を消すと、説明・列の説明・関連・ER図の配置・用語（<b>SQL式がその表を引くものだけ</b>。
                  説明だけの用語は残す）・例文・検算・定期取り込みの設定を一緒に片づけ、
                  まとまりの最後の表なら、まとまりのメモも消します。
                  削除前の「巻き添えの一覧」は同じ処理を<b>書き込まずに数えるだけ</b>で作ります。</td></tr>
          <tr><td>改名</td>
              <td>実テーブルの改名に加え、カタログ全文を語の境界つきで置換し、
                  定期取り込みの設定と利用者ごとの選択も付け替えます。
                  途中で失敗したら実テーブルもカタログも<b>元に戻します</b>。
                  まとまりの名前変更は、配下の表を1つずつ改名する形で実行します。</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="card mt">
    <div class="card__title">3-19. 文書検索（ナレッジベース）</div>
    <div class="tablewrap">
      <table class="data">
        <thead><tr><th style="width:210px">項目</th><th>内容</th></tr></thead>
        <tbody>
          <tr><td>通信</td>
              <td>検索は各サーバの <code>/query/data</code> にPOST、認証はAPIキーをヘッダで送ります。
                  疎通確認は <code>/health</code>、キーの有効性は <code>/documents/pipeline_status</code>
                  （どちらも15秒）。検索のタイムアウトは<b>180秒</b>。再試行はしません。</td></tr>
          <tr><td>複数サーバの並列</td>
              <td>最大<b>8台</b>を同時に呼びます。1台が失敗しても他は続行し、
                  失敗したサーバだけを結果に記録します。全滅したときだけ、原因をまとめて知らせます。</td></tr>
          <tr><td>既定値</td>
              <td>検索方式 mix（他に hybrid / local / global / naive）、
                  取得チャンク数10（1〜100）、関連情報の広さ40（1〜200）、
                  文脈の上限12,000字（1,000〜20,000）。利用者ごとに変更できます。
                  AIが多めのチャンク数を指定してきても「利用者設定の2倍」「100件」で頭打ちにします。</td></tr>
          <tr><td>結果の統合</td>
              <td>本文のハッシュで重複を除き、<b>まず各サーバから1件ずつ（短いものから）</b>採り、
                  以降は順番に回しながら文字数の予算まで詰めます（1台が予算を独占しないため）。
                  出典番号は採用順の連番で、出典一覧にはサーバ名・ファイル名・スコア・
                  本文の先頭200字を付けます。</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="card mt">
    <div class="card__title">3-20. グラフと統計のアルゴリズム</div>
    <div class="card__desc">
      グラフは <b>Plotly</b>、統計は <b>SciPy / statsmodels / NumPy / pandas</b>。
      scikit-learn は使っていません。有意水準は 0.05。
    </div>
    <div class="tablewrap">
      <table class="data">
        <thead><tr><th style="width:210px">機能</th><th>中身</th></tr></thead>
        <tbody>
          <tr><td>グラフ</td>
              <td><b>54種・6分類</b>（比較12／推移11／構成8／分布8／関係12／指標3）。
                  画面へは図をJSONで渡し、Word・PowerPointへは画像化して貼ります
                  （画像化に失敗しても文書生成は止めず、表と説明だけで作ります）。
                  2軸グラフは棒を左軸・折れ線を右軸に置きます。</td></tr>
          <tr><td>基本統計</td>
              <td>件数・平均・標準偏差・最小・四分位・中央値・最大。グループ指定で群ごとに算出。</td></tr>
          <tr><td>相関</td>
              <td>ピアソン（既定）／スピアマン。偏相関・時差相関にも対応。</td></tr>
          <tr><td>外れ値</td>
              <td>5手法 — 四分位範囲（既定・係数1.5）／Zスコア（既定3）／修正Zスコア（MAD）／
                  パーセンタイル／マハラノビス距離（複数列）。</td></tr>
          <tr><td>仮説検定</td>
              <td><b>13手法</b> — 1標本t／<b>Welchのt</b>（等分散を仮定しない）／対応のあるt／
                  Mann-Whitney U／Wilcoxon／一元配置分散分析／Kruskal-Wallis／カイ二乗（独立性）／
                  カイ二乗（適合度）／母比率／正規性（Shapiro-Wilk）／等分散性（Levene）／相関。
                  効果量も併せて出します（Cohen's d、η²、Cramer's V ほか）。
                  分散分析で有意かつ3群以上なら、全ペアに<b>Bonferroni補正</b>つきの多重比較を行います。
                  カイ二乗は期待度数5未満が2割を超えると警告します。</td></tr>
          <tr><td>回帰</td>
              <td>最小二乗（OLS）／ロジスティック／ポアソン。文字列の説明変数は自動でダミー化。
                  係数・標準誤差・p値・95%信頼区間を出し、OLSでは<b>多重共線性（VIF>10）</b>と
                  <b>残差の自己相関（Durbin-Watson が1.5〜2.5の外）</b>を警告。
                  30行以上なら<b>7:3のホールドアウト検証</b>で当てはまりの良さも報告します。</td></tr>
          <tr><td>予測</td>
              <td>7手法 — 直近値／ドリフト／移動平均／線形／Holt／Holt-Winters／ARIMA
                  （次数はAICで自動選択）。自動選択では、季節性の指定があり2周期分あればHolt-Winters、
                  8点以上ならHolt、それ以外は線形。区間は残差の標準偏差から±1.96σ（95%）。
                  8点以上なら<b>ローリング・バックテスト</b>で誤差（MAE/MAPE）も報告します。
                  最低4点必要、予測期間は1〜120。</td></tr>
          <tr><td>時系列</td>
              <td>移動平均・前期比・累計・前年同期比、傾向は線形回帰、
                  季節分解は加法モデル（2周期分必要）、自己相関は最大6ラグ。</td></tr>
          <tr><td>シミュレーション</td>
              <td>モンテカルロ: 試行1万回（100〜20万）、乱数の種は固定で再現性あり。
                  分布は正規／一様／三角／対数正規／ポアソン／二項／<b>実データそのまま</b>／固定値。
                  式は組み込み関数を無効にした環境で評価します。感度分析つき。</td></tr>
          <tr><td>信頼区間</td>
              <td>ブートストラップ法。復元抽出5,000回（200〜5万）、パーセンタイル法で2.5%〜97.5%。
                  群ごとの比較では信頼区間の重なりも判定します。</td></tr>
          <tr><td>クラスタ分析</td>
              <td>k-means（k-means++で初期化、標準化あり）。<b>kは自動選択可</b>（2〜8を総当たりし、
                  シルエット係数が最大のものを採用。0.25未満なら「はっきり分かれていない」と警告）。
                  各クラスタの特徴は、全体平均から0.8標準偏差以上ずれた列を最大3つ拾って言語化します。</td></tr>
          <tr><td>ABC分析</td>
              <td>合計の降順に累計構成比を出し、既定で70%までA・90%までB・残りC。</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="card mt">
    <div class="card__title">3-21. ファイル出力とメール</div>
    <div class="tablewrap">
      <table class="data">
        <thead><tr><th style="width:210px">項目</th><th>内容</th></tr></thead>
        <tbody>
          <tr><td>生成ライブラリ</td>
              <td>Excel=openpyxl、Word=python-docx、PowerPoint=python-pptx、CSV/テキスト/ZIP=標準ライブラリ。</td></tr>
          <tr><td>行数と名前</td>
              <td>ファイル出力は最大100万行（Excelは1,048,575行）。Wordの1表は40行、
                  PowerPointの1表は12行まで。ファイル名は使用禁止文字を除き80文字で切り、
                  <code>_年月日_時分</code> を付けます。シート名は31文字で、重複には連番を付けます。</td></tr>
          <tr><td>受け渡し</td>
              <td>生成物は<b>ディスクに書かず</b>メモリに置き、ランダムなトークンのURLで渡します。
                  <b>持ち主が一致しないと渡しません</b>（URLを推測されても他人のファイルは取れません）。
                  <b>時間の期限は無く、200件を超えると古いものから消え、再起動で全部消えます</b>。
                  会話履歴には2MBまで埋め込み、それを超えると再ダウンロードはできません。</td></tr>
          <tr><td>メールの組み立て</td>
              <td>差出人・宛先・Cc・返信先・件名・日時・Message-IDを付けます。
                  <b>Bccはヘッダに書かず</b>送信時の宛先にだけ入れます。</td></tr>
          <tr><td>宛先の検索</td>
              <td>列名のヒント（メール・氏名・部署）から対象の表を推測し、
                  先頭12列を対象に部分一致で検索します（値はプレースホルダ渡し）。
                  アドレスは「メール列のうち @ を含む最初の値」を採用。</td></tr>
          <tr><td>送信の制限</td>
              <td>宛先はTo+Cc+Bccの合計で<b>20件</b>まで。
                  実際に送れるのは<b>許可リストに完全一致するアドレスだけ</b>で、
                  <b>リストが空なら誰にも送れません</b>（未設定＝全許可にはしません）。
                  既定は試送モード（SMTPに接続せず内容だけ返す）。
                  SMTPのパスワードは設定ファイルではなく起動環境の設定からのみ読みます。</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="card mt">
    <div class="card__title">3-22. 認証と権限</div>
    <div class="tablewrap">
      <table class="data">
        <thead><tr><th style="width:210px">項目</th><th>内容</th></tr></thead>
        <tbody>
          <tr><td>認証方式</td>
              <td>2種類を設定で切り替え。<b>local</b>＝サーバ上のユーザー定義ファイル、
                  <b>http</b>＝社内の認証APIへ問い合わせ（ユーザー名とパスワードのキー名、
                  成功の判定に使う項目、表示名とグループの項目、タイムアウト10秒を設定で指定）。
                  APIが400/401/403を返せば「認証失敗」、それ以外の異常は「認証エラー」として区別します。</td></tr>
          <tr><td>パスワードの保存</td>
              <td><b>PBKDF2-HMAC-SHA256、20万回、ソルト16バイト（利用者ごとに個別生成）</b>。
                  平文は保存しません。反復回数は保存値から読むので、後で回数を変えても
                  古いパスワードのまま検証できます。比較は時間差の出ない方法で行います。</td></tr>
          <tr><td>非常口の管理者</td>
              <td>認証APIが落ちても入れるように、設定ファイルに1つだけ管理者を直接書けます。
                  <b>パスワードを空にするとこのアカウント自体が無効</b>になります
                  （空パスワードでのログイン事故を防ぐため）。
                  同じIDが入力されたときは、パスワードが違っても外部認証には回しません
                  （同名の別人と取り違えないため）。</td></tr>
          {# この節は全利用者に出る。動作確認用アカウントの名前と
             「IDとパスワードが同じ」という決め方は、そのまま他人になりすます
             手がかりになるので書かない（設定の在り処だけ示す） #}
          <tr><td>常設の一般ユーザー</td>
              <td>設定ファイル（auth.py の BUILTIN_USERS）に書かれた、動作確認用の
                  固定アカウント。チャットだけ使える一般権限です。管理者と同じく、
                  IDが一致したら外部認証には回しません。
                  <b>本番ではリストを空にして、この仕組みごと止めてください。</b></td></tr>
          <tr><td>セッション</td>
              <td>署名付きCookie。<b>ブラウザを閉じると切れます</b>（永続化しません）。
                  JavaScriptから読めない設定・同一サイト送信の制限つき。
                  署名鍵はファイルに保存して再起動でログアウトしないようにしています
                  （無ければ自動生成）。</td></tr>
          <tr><td>権限の判定</td>
              <td>所属グループに管理者グループ名が含まれるかどうか。
                  管理者専用の画面とAPIはサーバ側で止めます（画面からメニューを隠すだけでは、
                  URLを直接叩かれると素通りするため）。APIは403、画面は403ページを返します。</td></tr>
          <tr><td>利用者管理</td>
              <td>サーバ上で <code>python core.py users add &lt;名前&gt; --admin</code> など。
                  パスワードは対話式に2回入力（コマンドラインに書くと履歴に残る旨を警告します）。
                  削除はユーザー定義だけで、その人の設定・履歴フォルダは残ります。</td></tr>
          <tr><td>その他の防御</td>
              <td>ナレッジベースのAPIキーは画面・APIの応答から必ず落とします（設定済みか否かだけ返す）。
                  チャットからのカタログ登録は既定で管理者のみ
                  （カタログは全利用者のプロンプトに載るため）。</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="card mt">
    <div class="card__title">3-23. 保存レイアウト（ファイルの中身）</div>
    <div class="tablewrap">
      <table class="data">
        <thead><tr><th style="width:250px">場所</th><th>内容</th></tr></thead>
        <tbody>
          <tr><td class="mono small">data/統合.db</td>
              <td>唯一のSQLite。data/直下の <code>*.db</code> を名前順に読みます。</td></tr>
          <tr><td class="mono small">data/統合.db.meta.yaml</td>
              <td>カタログ本体。書き出すのは 表・まとまり・関連・用語・例文・検算・ER配置・
                  ユーザー定義ツール・組み込みの上書き。<b>空の項目は書きません</b>。
                  複数行の文章はブロック形式で出力し、人が直接開いて直せる形にしています。</td></tr>
          <tr><td class="mono small">data/.profile_cache/</td>
              <td>自動プロファイルのJSON（自動生成・編集不可）。</td></tr>
          <tr><td class="mono small">data/import_jobs.yaml</td><td>定期取り込みの設定。</td></tr>
          <tr><td class="mono small">data/import_dirs.yaml</td><td>画面から追加した取り込み許可フォルダ。</td></tr>
          <tr><td class="mono small">data/import_history.jsonl</td>
              <td>取り込み履歴（1行1件の追記型）。日時・表・成否・件数・削除数・保持回数・
                  元ファイル・実行者・所要秒などを記録。<b>5,000件</b>を超えたら
                  （1.1倍に達した時点でまとめて）古い分を間引きます。</td></tr>
          <tr><td class="mono small">data/catalog_history.jsonl</td>
              <td>カタログの変更履歴（追記型、2,000件で間引き）。変更前後の値を保持します。</td></tr>
          <tr><td class="mono small">data/knowledge_bases.json</td>
              <td>文書検索の接続先。APIキーを含むため権限を絞り、
                  一時ファイル経由の<b>原子的な置き換え</b>で書きます。</td></tr>
          <tr><td class="mono small">data/model_settings.yaml</td><td>選べるモデル・既定・画像対応・文脈長の上書き。</td></tr>
          <tr><td class="mono small">data/mail_settings.yaml</td>
              <td>メール設定。<b>そのまま画面に出す前提なので秘密は入れません</b>
                  （SMTPのユーザー・パスワード・暗号化方式は起動環境の設定のみ）。</td></tr>
          <tr><td class="mono small">data/users/&lt;利用者&gt;/prefs.yaml</td>
              <td>個人設定。読み書きするのは4項目だけ（モデル／検索対象から外したナレッジベース／
                  検索の効き方／分析対象から外した表）。Cookieでなくファイルに置くのは、
                  ログアウトやブラウザを閉じても残すためです。</td></tr>
          <tr><td class="mono small">data/users/&lt;利用者&gt;/chats/</td>
              <td>会話の実体（1会話1ファイル）と一覧ファイル。一覧を分けているのは、
                  サイドバーを描くたびに全会話を読まないため。一覧が壊れても実体から作り直します。
                  <b>システムプロンプトは保存しません</b>（開くたびに最新のカタログで作り直すため）。
                  自動削除は<b>100本</b>を超えた分と、<b>90日</b>より古いもの（変更なし・0で無期限）。</td></tr>
          <tr><td class="mono small">.flask_secret / auth_users.yaml</td>
              <td>プロジェクト直下。前者はセッションの署名鍵（自動生成）、後者は利用者の定義。</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="card mt">
    <div class="card__title">3-24. 同時実行の制御</div>
    <div class="tablewrap">
      <table class="data">
        <thead><tr><th style="width:250px">対象</th><th>方式</th></tr></thead>
        <tbody>
          <tr><td>定期取り込みのジョブ</td>
              <td>再入可能な鍵で直列化（裏で回るスケジューラと画面の「今すぐ更新」が
                  同時に走りうるため）。同じ表へ同時に書きません。</td></tr>
          <tr><td>各種の設定・履歴ファイル</td>
              <td>取り込み履歴／カタログ履歴／個人設定／モデル設定／メール設定／
                  ナレッジ登録簿／生成ファイル置き場／画像キャッシュに、それぞれ書き込み用の鍵。</td></tr>
          <tr><td>カタログの保存</td>
              <td>ファイルロックは持たず、<b>書き込み口を管理者だけに絞る</b>ことで代えています。
                  読み込みは共有キャッシュをそのまま返すため書き換え禁止で、
                  編集時は必ず複製を渡します（下見の処理がキャッシュを壊す事故があったため）。</td></tr>
          <tr><td>SQLiteの待ち時間</td>
              <td>書き込み接続は30秒待ち。分析用の読み取りは時間制限を別方式（前述）で持ちます。</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="card mt">
    <div class="card__title">3-25. 主な設定値の一覧</div>
    <div class="card__desc">
      「変更可」は起動フォルダの <code>env</code> ファイルで上書きできます（<code>export</code> 付きの行も可）。
    </div>
    <div class="tablewrap">
      <table class="data">
        <thead><tr><th style="width:280px">設定</th><th style="width:190px">既定値</th><th>区分</th></tr></thead>
        <tbody>
          <tr><td>ツール往復の上限</td><td>10</td><td>変更可</td></tr>
          <tr><td>1回の取得行数</td><td>2,000行</td><td>固定</td></tr>
          <tr><td>SQLの実行時間</td><td>10秒</td><td>固定</td></tr>
          <tr><td>AIに渡すサンプル行</td><td>40行</td><td>固定</td></tr>
          <tr><td>ファイル出力の行数</td><td>1,000,000行</td><td>変更可</td></tr>
          <tr><td>カタログを丸ごと渡す上限</td><td>4,000〜400,000字</td><td>固定</td></tr>
          <tr><td>テーブルの絞り込み方式</td><td>auto</td><td>変更可</td></tr>
          <tr><td>プロファイルの時間制限／サンプル行／値一覧の上限</td><td>30秒／5行／20種</td><td>固定</td></tr>
          <tr><td>取り込みの行数／ファイル容量</td><td>1,000,000行／100MB</td><td>変更可</td></tr>
          <tr><td>取得日時の列名</td><td>取得日時</td><td>変更可</td></tr>
          <tr><td>スケジューラの巡回間隔</td><td>60秒</td><td>変更可</td></tr>
          <tr><td>アップロードの可否</td><td>無効</td><td>変更可</td></tr>
          <tr><td>文書検索のタイムアウト／並列数</td><td>180秒／8台</td><td>変更可</td></tr>
          <tr><td>宛先の上限／試送モード</td><td>20件／有効</td><td>変更可</td></tr>
          <tr><td>会話の保存期間／本数</td><td>90日／100本</td><td>期間のみ変更可</td></tr>
          <tr><td>混雑時の再試行／最大待ち</td><td>3回／20秒</td><td>変更可</td></tr>
          <tr><td>裏方処理に使うモデル</td><td>設定ファイルで固定（画面の選択とは別）</td><td>固定</td></tr>
          <tr><td>温度（生成のばらつき）</td><td>0</td><td>変更可</td></tr>
          <tr><td>画像の枚数／容量</td><td>4枚／8MB</td><td>変更可</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="card mt">
    <div class="card__title">3-26. 記録（サーバの標準出力）</div>
    <div class="card__desc">
      記録はすべてサーバの標準出力に出ます（ログファイルへの書き出しや世代管理は行いません）。
      行の先頭に <code>[分類]</code> が付きます。
    </div>
    <div class="tablewrap">
      <table class="data">
        <thead><tr><th style="width:200px">分類</th><th>内容</th></tr></thead>
        <tbody>
          <tr><td class="mono small">[scheduler 日時]</td><td>定期取り込みの巡回開始・各ジョブの成否・管理者への通知・巡回中のエラー</td></tr>
          <tr><td class="mono small">[import] / [rename]</td><td>テーブルの削除・改名（実行した利用者名つき）</td></tr>
          <tr><td class="mono small">[models] / [mailer]</td><td>モデル設定・メール設定の変更（利用者名つき）、試送の宛先と本文</td></tr>
          <tr><td class="mono small">[llm]</td><td>混雑による待機と再送、モデルごとの呼び出し方の自動調整</td></tr>
          <tr><td class="mono small">[router] / [results] / [verify]</td><td>表の絞り込みの失敗、同じSQLの使い回し、検算のエラー（回答は継続）</td></tr>
          <tr><td class="mono small">[rag] / [realtime] / [report]</td><td>文書検索の失敗、リアルタイム更新の結果、画像化の失敗</td></tr>
          <tr><td class="mono small">[catalog] / [chats] / [history] ほか</td><td>各ファイルの読み書きの失敗、期限切れ会話の削除件数</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  {% if user.is_admin %}
  <div class="card mt">
    <div class="card__title">3-27. 設計上の制約（運用で気をつける点）</div>
    <div class="card__desc">
      隠さず書いておきます。いずれも「1台・小規模・社内」という前提のうえで、
      複雑さを増やさないために選んだ割り切りです。
    </div>
    <div class="tablewrap">
      <table class="data">
        <thead><tr><th style="width:250px">制約</th><th>内容と対処</th></tr></thead>
        <tbody>
          <tr><td>ワーカーは1本</td>
              <td>スケジューラが常駐スレッドなので、プロセスを増やすと同じ取り込みが多重実行されます。
                  同時アクセスはスレッド数で増やしてください。</td></tr>
          <tr><td>生成ファイルはメモリ上</td>
              <td>再起動すると未ダウンロードのファイルは消えます（200件で古いものから破棄）。
                  結果の使い回し用のデータも同様です。</td></tr>
          <tr><td>カタログ保存は後勝ち</td>
              <td>管理者が2人同時に保存すると、後から保存した内容で上書きされます（競合の検知なし）。
                  変更履歴は残るので、内容の復元は可能です。</td></tr>
          <tr><td>会話ファイルも後勝ち</td>
              <td>同じ人が2つのタブから同時に送ると、後から終わった方で上書きされます。</td></tr>
          <tr><td>会話履歴は切り詰めない</td>
              <td>長い会話ほど毎回の送信量が増え、費用と時間が伸びます。
                  区切りのよいところで新しい会話を始めるのが安全です。</td></tr>
          <tr><td>SQLの解析は正規表現</td>
              <td>「どの表に触れたか」の判定はSQLの構文解析ではなく名前の照合です。
                  用途が「多い・少ない・ゼロ」の把握なので、多少の取りこぼしで結論は変わりません。</td></tr>
          <tr><td>日付の型推定は無い</td>
              <td>取り込み時、日付はTEXTとして入ります。並べ替えや期間の絞り込みは
                  ISO形式（YYYY-MM-DD）で書いておくと辞書順で正しく動きます。</td></tr>
        </tbody>
      </table>
    </div>
  </div>
  {% endif %}

  <!-- ==================================================================== -->
  <!-- 第4部 用語解説 -->
  <!-- ==================================================================== -->
  <h2 id="glossary" class="mt" style="font-size:20px">第4部 用語解説</h2>

  <div class="card mt">
    <div class="card__desc">
      このアプリの説明に出てくる専門用語を、基礎から解説する章です。各用語は
      「一般的な意味」→「<b>このアプリでは</b>どう使われているか」の順で書いてあります。
      第1〜3部を読んでいて分からない言葉が出てきたら、ここに戻ってください。
    </div>
  </div>

  <div class="card mt">
      <div class="card__title">4-1. 生成AIの基礎</div>
      <div class="card__desc">
        チャットの答えを書いているのは「生成AI」と呼ばれるプログラムです。生成AIは確率で文章を作る道具で、
        間違うことがあります（だからこのアプリには、SQLの表示・出典・検算という人が確かめる仕組みがあります）。
        最初にこのカードを読むと、以降の用語解説と第1〜3部の説明が読みやすくなります。
      </div>
      <div class="tablewrap">
        <table class="data">
          <thead><tr><th style="width:210px">用語</th><th>説明</th></tr></thead>
          <tbody>
            <tr><td>生成AI／LLM（大規模言語モデル）</td>
                <td>大量の文章から「この言葉の次に来やすい言葉」を予測することを学んだプログラムで、
                    その予測を繰り返して文章を組み立てます。中に人が入って答えているわけではなく、
                    Web検索とも別物です（どこかにある文章を探して写すのではなく、その場で文章を作っているため）。
                    このうち文章を読み書きするタイプをLLM（大規模言語モデル）と呼びます。
                    <b>このアプリでは</b>チャットの回答の書き手がこの生成AIです。確率で文章を作る以上は
                    間違い得るため、根拠のSQLを必ず表示し、文書の答えには出典番号を付け、
                    検算を裏で走らせています。</td></tr>
            <tr><td>AIモデル</td>
                <td>モデルはAIの「銘柄」のことで、同じ会社のAIでも銘柄ごとに賢さ・速さ・料金・
                    一度に読める量が違います（車の車種のようなものです）。<b>このアプリでは</b>サイドバー上部の
                    プルダウンで切り替えられ、選択は利用者ごとに保存されます。候補と既定は管理者が
                    「モデル設定」で決めているため、迷ったら既定のままで問題ありません。</td></tr>
            <tr><td>推論モデル（reasoning）</td>
                <td>答えを書き始める前に、内部で長く「考える」工程を挟むタイプのモデルを指す近年の区分です。
                    段取りの多い問題に強い代わりに、返事が遅くなります。<b>このアプリでは</b>候補に
                    入っていれば同じプルダウンから選べます（o1・o3系など）。複雑な集計や多段の依頼では、
                    待ち時間が延びる代わりに正答しやすくなります。</td></tr>
            <tr><td>画像対応（マルチモーダル）</td>
                <td>文章だけでなく画像も読み取れるモデルの呼び名です（複数の種類の情報を扱えるため
                    マルチモーダルと呼びます）。<b>このアプリでは</b>モデル選択の「画像OK」表示が目印で、
                    エラー画面の写真や帳票の画像を貼り付け（Ctrl+V）やドラッグ＆ドロップで添付して
                    質問できます。枚数などの制限は第1部「使い方の注意（チャット）」を参照してください。</td></tr>
            <tr><td>ChatGPTとこのアプリの関係</td>
                <td>ChatGPTはOpenAI社のAIを個人が画面で使うサービスで、API（ChatGPT-API）は同じ会社のAIを
                    プログラムから部品として借りるための窓口です。<b>このアプリでは</b>後者を使い、
                    OpenAIのAIを回答エンジンとして借りています。そのため質問文と、カタログの説明・
                    データの一部（サンプル行や集計結果など）が、暗号化された通信でOpenAIへ送られます。
                    送った内容がAIの学習に使われるかどうかは契約・設定に依存するため、ここでは断定しません
                    （気になる場合は管理者に確認してください）。</td></tr>
            <tr><td>ローカルLLM</td>
                <td>インターネットの向こうのサービスではなく、社内のパソコン・サーバの中だけで動くAIのことです。
                    データが社外に出ない・利用料がかからない利点の代わりに、同世代の商用モデルより賢さは落ちます。
                    <b>このアプリでは</b>コードを変えずに設定ファイルの切り替えだけで、開発時はローカルLLM
                    （Ollama等）・本番はChatGPT-APIと使い分けられる作りになっています。</td></tr>
            <tr><td>プロンプト／システムプロンプト</td>
                <td>プロンプトは、AIに毎回渡す指示と資料の全文のことです。AIはプロンプトに載っているものしか
                    知らないため、そこに何を載せるかで回答の質が決まります。<b>このアプリでは</b>利用者の
                    質問文の裏で、アプリがカタログ（表・列の説明）・用語集・例文などを自動で足しており、
                    この自動で足す部分がシステムプロンプトです（組み立ての中身は3-3を参照）。
                    第1〜3部に何度も出てくる「プロンプトに載る／外れると答えが変わる」という話の土台です。</td></tr>
            <tr><td>トークン</td>
                <td>AIが文章を読み書きするときの単位で、料金も読める量の上限もこの単位で数えます。
                    日本語ではおおむね1〜2文字が1トークンに相当します（モデルにより多少変わります）。
                    <b>このアプリでは</b>管理者画面「モデル設定」の「文脈量（トークン）」の登録や、
                    カタログをどこまでAIに見せるかの上限計算（3-5）にこの単位を使っています。
                    なおファイル出力の説明（3-21）に出てくる「ランダムなトークン」は、
                    受け渡し用の合言葉という意味の別の言葉です（同じ字ですが無関係のため注意）。</td></tr>
            <tr><td>文脈長（コンテキストウィンドウ）</td>
                <td>AIが一度に読める量の上限で、モデルごとに決まっています。作業机の広さのようなもので、
                    机に載り切らない資料は読んでもらえません。<b>このアプリでは</b>上限に収まらないとき、
                    カタログを要約版（列名なし）に落として渡すため回答の質が下がります（3-4）。
                    また会話が長いほど毎回の送信量が増えるため、第1部の「話題が変わったら新しい会話に」
                    という助言はここから来ています。</td></tr>
            <tr><td>プロンプトキャッシュ</td>
                <td>同じ書き出しで始まるプロンプトは、2回目からその部分の処理を省いて高速・割安に済ませる
                    というAPI側の仕組みです。先頭部分が同じ間だけ効き、途中で内容が変わると
                    そこから後ろは効きません。<b>このアプリでは</b>カタログを編集するとプロンプトの中身が
                    変わってキャッシュが外れ、直後の質問が遅く・高くなります。管理者向けの
                    「細かく直すよりまとめて直す方が得」という助言の理由がこれです。</td></tr>
            <tr><td>ハルシネーション（もっともらしい誤り）</td>
                <td>AIが存在しない事実を、自信のある口調で作ってしまう性質です。故障ではなく、
                    確率で文章を作る原理から来るもので、完全にはなくせません。<b>このアプリでは</b>数字を
                    必ずSQLで実データから計算させ、実行したSQLを回答に表示し、文書の答えには出典番号を
                    付けています（AIの記憶ではなく実データを根拠にし、人が確かめられるようにするため）。
                    それでも<b>SQLや出典の付いていない断定はうのみにしない</b>のが安全です。</td></tr>
            <tr><td>回答が毎回違う理由（温度）</td>
                <td>AIは「次に来やすい言葉」を確率で選びながら文章を作るため、同じ質問でも言い回しや構成が
                    毎回変わります。これは故障ではなく仕様です。温度はそのばらつきの大きさを決める
                    調整つまみで、0に近いほど毎回同じ答えに近づきます。<b>このアプリでは</b>温度を0に設定し、
                    集計のSQLが安定するようにしています（3-25。温度の指定を受け付けないモデルでは、
                    そのモデルの標準設定で動きます）。それでも文章部分の表現は多少揺れますが、
                    同じSQLなら計算結果は同じです。</td></tr>
            <tr><td>AIは学習する？会話を覚えている？</td>
                <td>会話したりデータを登録したりするだけで、モデル本体が自動的に賢くなることはありません。
                    「学習」（モデル自体を作り替える工程）と「その場で読ませる」（プロンプトに載せる）は
                    別物です。<b>このアプリでは</b>回答が良くなるのはカタログや例文を毎回プロンプトに載せて
                    読ませているためで、モデル自体は変わっていません。会話の記憶も同じで、AIは毎回その会話の
                    全文を読み直しているだけです（3-6）。会話の中で教えただけのことが別の会話に引き継がれないのは
                    このためで、覚えさせたいことはカタログ・用語・例文に登録します（毎回読ませられるため）。</td></tr>
            <tr><td>Few-shot（フューショット）</td>
                <td>正解の例を数件見せるだけで、AIがその型を真似て精度が上がるという一般的な性質の名前です。
                    例を見せてもモデル自体は何も変わっておらず、前項の「学習」とは別物です。
                    <b>このアプリでは</b>回答の星印（例文登録）で登録した例文が「正しいと確認済みの
                    質問とSQLの例」としてプロンプトに載り、似た質問への正答率を上げます（3-16）。
                    例文登録が効くのはこの性質のためです。</td></tr>
          </tbody>
        </table>
      </div>
      <div class="small muted mt">
        補足: ここでの「AI」はすべてAPI経由で借りているもので、個人のChatGPTアカウントやその履歴とは
        無関係です。各記述の詳しい仕組みは、括弧内の番号の第3部カードを参照してください。
      </div>
    </div>

  <div class="card mt">
      <div class="card__title">4-2. AIが道具を使う仕組み（tool calling・エージェント）</div>
      <div class="card__desc">文章を書くだけのはずの生成AIが、SQL実行やグラフ作成という「作業」をこなせる仕組みを説明します。実際にデータへ触るのはアプリ側の道具（ツール）で、AIは依頼を出すだけです。回答の途中に出る「SQL実行 (SELECT)」などの表示は、その道具が動いた瞬間です。</div>
      <div class="tablewrap">
        <table class="data">
          <thead><tr><th style="width:210px">用語</th><th>説明</th></tr></thead>
          <tbody>
            <tr><td>ツール呼び出し（tool calling／function calling）</td>
                <td>AIが「この道具を、この引数で使いたい」という依頼文を返し、それを受け取ったプログラム側が実際の作業を行う分業の仕組みです。AI本人は文章を書いているだけで、手は動かしていません。<b>このアプリでは</b>チャット途中の「SQL実行 (SELECT)」「グラフ描画」の表示が、依頼を受けたアプリが道具を動かしている瞬間です。AIはデータベースに直接触れないため、<b>読むだけ</b>（<code>SELECT</code>専用）の約束をアプリ側で確実に守れます（安全機構は4層。詳細は3-8を参照）。</td></tr>
            <tr><td>AIエージェント</td>
                <td>「考える→道具を使う→結果を見てまた考える」を自律的に繰り返す仕組みの呼び名です。1回の受け答えで終わらず、目的に向かって段取りを自分で組み立てる点が特徴です。<b>このアプリでは</b>1つの質問の中でSQL実行→グラフ→レポートと往復するのがこれにあたります。暴走を防ぐため往復は<b>10回</b>で一区切りになり、「続けて」と送ると再開できます（詳細は3-2を参照）。</td></tr>
            <tr><td>オーケストレーション</td>
                <td>複数の処理を指揮して、順番や受け渡しを段取りすることです。オーケストラの指揮者（各奏者に出番を指示する役）からの転用語です。<b>このアプリでは</b>上記の往復（AIへの依頼・道具の実行・結果の受け渡し）の交通整理役がこれにあたります。第2部の全体図（管理者にのみ表示されます）では「AIオーケストレーション」の箱として描かれています。</td></tr>
            <tr><td>text-to-SQL（テキスト・トゥ・エスキューエル）</td>
                <td>日本語などの普通の文章からSQLを自動生成する技術の総称です。例えば「地域ごとの売上合計は？」という質問を<code>SELECT 地域, SUM(金額) FROM 注文 GROUP BY 地域</code>のようなSQLに翻訳します。<b>このアプリでは</b>チャットで集計を頼んだときにAIがSQLを組み立てる部分がこの技術です。最大のリスクは翻訳を誤ること（もっともらしいが違う集計が返り得るため）なので、実行したSQLを回答に必ず表示し、検算で人が確かめられるようにしています（検算は3-16を参照）。</td></tr>
            <tr><td>API（エーピーアイ）</td>
                <td>プログラム同士が会話するための「窓口」の総称です（Application Programming Interface）。人が画面のボタンを押す代わりに、プログラムが決まった形式で依頼を送り、返事を受け取ります。<b>このアプリでは</b>ChatGPT-API（社外のAIモデル）とLightRAGサーバ（社内の文書検索）をこの窓口経由で呼び出しています。説明書で「外部API」とあれば、窓口越しに借りている社外サービスの意味です。</td></tr>
            <tr><td>APIキー</td>
                <td>APIを使うときに提示する合鍵にあたる文字列です。漏れると他人のプログラムが自分になりすまして窓口を使えるため、パスワードと同じ扱いで守る必要があります。<b>このアプリでは</b>登録済みのAPIキーを画面では「設定済み」の表示や伏せ字にとどめ、実値をむやみに出さないようにしています（漏えいを防ぐため）。</td></tr>
            <tr><td>SDK（エスディーケー）</td>
                <td>あるサービスに接続するための公式の部品集です（Software Development Kit）。窓口（API）の細かい作法が部品として用意されており、自前で作り込むより間違いが減ります。<b>このアプリでは</b>OpenAIのSDKでAIモデルを呼び出しています。混雑時の再試行がSDK側で2回・アプリ側でさらに掛かる「二重の再試行」の登場人物です（詳細は3-7を参照）。</td></tr>
            <tr><td>逐次表示（ストリーミング・SSE）</td>
                <td>全部できあがってから渡すのではなく、できた端から順に流す通信方式です。SSE（Server-Sent Events）はそのための具体的な技術の名前です。<b>このアプリでは</b>回答が少しずつ流れて見えるのは演出ではなく、AIが実際に文章を書いている速度がそのまま画面に届いています（詳細は3-6を参照）。</td></tr>
            <tr><td>レート制限</td>
                <td>単位時間あたりの利用回数の上限のことで、混雑時にサービス側が出す一時的な「お断り」です。故障ではありません。<b>このアプリでは</b>自動で待って投げ直してもなお通らないときに「混み合っています（レート制限）」と表示します。少し時間をおいて「続けて」と送ると再開できます。それまでに取得したデータは残っており、上限も時間の経過で解除されます（再試行の詳細は3-7を参照）。</td></tr>
            <tr><td>タイムアウト</td>
                <td>待ち時間の上限に達したら、処理を諦めて打ち切る仕組みです。処理が壊れたのではなく、時間切れです（無限に待つと画面が止まったままになるため）。<b>このアプリでは</b>重いSQLや文書検索で起きることがあります。期間を絞る・対象の表を減らすなど質問を軽くして送り直すと通りやすくなります（同じ内容のまま待っても、掛かる時間は変わらないため）。</td></tr>
            <tr><td>結果の引換券（<code>result_id</code>）</td>
                <td>一度計算した結果に番号を付けて取り置き、次からは番号だけで呼び出す仕組みで、取り置き（キャッシュ）の一種です。クリーニング店の引換券のように、番号があれば現物を運び直さずに済みます。<b>このアプリでは</b>SQLの結果をグラフやExcel作成へ渡すときの内部の引換券です。回答文に<code>result_id</code>のような英字が見えても異常ではありません（同じSQLを2度流さないための仕組みのため。詳細は3-9を参照）。</td></tr>
          </tbody>
        </table>
      </div>
      <div class="small muted mt">補足: 道具がエラーなく動いたことと、集計が質問の意図どおりであることは別です。<b>エラーが出ない＝正しい集計、ではない</b>ため、大事な数値は回答に表示されたSQLと検算（3-16）で確かめてください。</div>
    </div>

  <div class="card mt">
      <div class="card__title">4-3. データベースとSQL</div>
      <div class="card__desc">
        回答に毎回表示される「実行したSQL」を、暗号ではなく根拠として眺められるようになるためのカードです。
        データベースの基本の約束と、SQLのごく基本だけを説明します。SQLを全部読める必要はありません。
      </div>
      <div class="tablewrap">
        <table class="data">
          <thead><tr><th style="width:210px">用語</th><th>説明</th></tr></thead>
          <tbody>
            <tr><td>SQL（エスキューエル）</td>
                <td>データベース（次項）に指示を出すための世界共通の言語で、人が読める英単語でできています。
                    例えば <code>SELECT 地域, SUM(金額) FROM 注文 GROUP BY 地域</code> は
                    「注文の表から、地域ごとに金額を合計して読み出す」という意味です。
                    <b>このアプリでは</b>AIが質問に合わせてSQLを書き、実行したSQLが回答に必ず表示されます。
                    全部読めなくても、<code>FROM</code> の後ろの表名と <code>WHERE</code> の条件だけ眺めれば
                    「どの表をどう絞ったか」の確認になります（読み違いの多くはこの2点で気づけるため）。</td></tr>
            <tr><td>データベース（DB）</td>
                <td>複数の表をひとまとめに管理し、SQLで質問すると答えを返してくれる仕組みです。
                    ただのファイル置き場やExcelブックと違い、大量のデータでも壊れにくく、
                    誰が集計しても同じ答えになります（全員が同じ1つのデータを見るため、
                    手元コピーごとの食い違いが起きません）。
                    <b>このアプリでは</b>DBは<b>1つだけ</b>で、AIはそこを<b>読むだけ</b>です。</td></tr>
            <tr><td>テーブル・行・列（レコード・カラム）</td>
                <td>表のことをテーブル、横の1行を1件の記録（レコード）、縦の項目を列（カラム）と呼びます。
                    Excelのシートに近いですが、1つのテーブルには同じ形の行しか入らない約束があり、
                    小計行やメモ書きが混ざらないこの約束が集計の信頼性を生みます。
                    <b>このアプリでは</b>取り込んだExcelの1シート・CSVの1ファイルが
                    それぞれ1つのテーブルになり、
                    AIはサイドバーで選ばれたテーブルだけを対象に集計します。</td></tr>
            <tr><td>SELECT文（セレクト）</td>
                <td><code>SELECT</code> は「読み出すだけ」の命令で、データを1文字も書き換えません。
                    前置きの計算を書く <code>WITH</code> もこの仲間です。
                    <b>このアプリでは</b>AIが実行できるのは <code>SELECT</code>（または <code>WITH</code>）で始まる
                    1つの文だけです。そのためAIがどんなSQLを書いても、
                    データが消えたり変わったりすることはありません（この割り切りが安全設計の核です。
                    関門の全体像は3-8を参照）。</td></tr>
            <tr><td>書き込み系のSQL（INSERT・UPDATEなど）</td>
                <td>SQLにはデータを変えてしまう命令もあります。代表は
                    <code>INSERT</code>（行の追加）・<code>UPDATE</code>（書き換え）・<code>DELETE</code>（削除）・
                    <code>DROP</code>（表ごと破棄）です。
                    <b>このアプリでは</b>この4語を含む19語のどれかが入ったSQLは、
                    実行前の検査で拒否されます（読み取り専用を守るため。語の一覧は3-8を参照）。
                    関門リストに並ぶ英単語は、いずれも「データや設定を変える命令と、
                    その足がかりになる命令」の仲間です。</td></tr>
            <tr><td>クエリ</td>
                <td>データベースへの問い合わせの総称で、実務ではSQL文とほぼ同じ意味で使われるカタカナ語です。
                    <b>このアプリでは</b>AIの回答文や技術者との会話で「クエリ」と出てきたら、
                    「実行したSQL」のことと読み替えて差し支えありません。</td></tr>
            <tr><td>SQLite（エスキューライト）</td>
                <td>サーバを別に立てず、ファイル1個で完結する軽量データベースの製品名です。
                    スマートフォンや家電にも組み込まれ、世界で最も広く使われているデータベースとも言われます。
                    <b>このアプリでは</b>唯一のDBがSQLiteで、サイドバーの「SQLite3」の正体です。
                    ただし標準偏差・中央値・相関などを計算する命令を持たないため、
                    統計は「統計分析」などの専用ツールが分担します（分担の詳細は3-20を参照）。</td></tr>
            <tr><td>WHEREとGROUP BY（ウェア・グループバイ）</td>
                <td><code>WHERE</code> は条件に合う行だけに絞る句（例: <code>WHERE 年度 = 2025</code>）、
                    <code>GROUP BY</code> は「地域ごと」「月ごと」のようなまとめ単位を決めて
                    合計や件数を計算する句で、この2つがSQLの2大基本句です。
                    <b>このアプリでは</b>件数・合計・順位を求めるとき、AIに表を読ませて数えさせるより
                    SQLで計算させる方が確実です（AIが読むのは先頭40行だけで、SQLの計算には読み間違いが無いため）。
                    第1部「使い方の注意（チャット）」の「大きな表を見せたとき」の注意はこの理屈によります。</td></tr>
            <tr><td>JOIN（ジョイン・結合）</td>
                <td>2つのテーブルを共通の列で横につないで、1つの表のように扱う操作です。
                    ExcelのVLOOKUPで別シートから情報を引いてくる操作に近いものです。
                    <b>このアプリでは</b>カタログに登録された「関連」が「この列で <code>JOIN</code> してよい」という
                    AIへの手がかりになります。関連が正しく登録されているほどAIの結合は正確になります
                    （候補の出し方と検証は3-13・3-14を参照）。</td></tr>
            <tr><td>UNION ALL（ユニオンオール）</td>
                <td>同じ形のテーブルを縦に積んで1つにまとめる操作です。
                    横につなぐ <code>JOIN</code> に対し、こちらは行を積み増して合算します。
                    <b>このアプリでは</b>拠点別の表から全社集計を作る場面で登場し、
                    同じ名前の表が複数のまとまりにあると「全体は <code>UNION ALL</code> で合算せよ」という
                    指示がAIに自動で入ります。</td></tr>
            <tr><td>クロス集計（ピボットテーブル）</td>
                <td>行×列のかけ合わせで集計する表です（例: 行に製品・列に月で売上を並べる）。
                    Excelのピボットテーブルと同じ概念です。
                    <b>このアプリでは</b>チャットの「クロス集計」ツールが作ります
                    （SQLiteには表をこの形に展開する構文が無いため）。実数のほか
                    構成比でも出せ（行ごと・列ごと・全体の3モード）、
                    色の濃淡で値の大小を見せるヒートマップ表示も選べます。</td></tr>
            <tr><td>NULL（ヌル）</td>
                <td>0でも空文字でもない「値が無い」ことを表す特別な状態です。
                    平均や列を指定した件数の計算では、NULLの行は自動的に対象から外れます。
                    <b>このアプリでは</b>取り込み時の空欄セルがNULLとして保存されるため、
                    <b>手計算と微妙に合わない集計の代表的な原因</b>になります。
                    数字が合わないときは、空欄の割合をAIに聞いてみてください
                    （「データ品質チェック」ツールが列ごとの空の割合を数えます）。</td></tr>
            <tr><td>データ型（TEXT・INTEGER・REAL）</td>
                <td>データベースでは列ごとに、文字（<code>TEXT</code>）・整数（<code>INTEGER</code>）・
                    小数（<code>REAL</code>）のどれを入れるかが固定されます。
                    Excelと違いセル単位でなく列単位で決まるため集計が安定しますが、
                    「0123」のようなコードを数値の列に入れると先頭のゼロが失われて123になります。
                    <b>このアプリでは</b>取り込みプレビューが読む2,000行から型を推定し、
                    先頭ゼロのコードは <code>TEXT</code> のまま残します。推定された型は、
                    取り込みを行う管理者が取り込み画面の「列の設定」で確認・変更します
                    （内部処理は3-17を参照）。</td></tr>
            <tr><td>SQLエラーの読み方</td>
                <td>SQLが失敗すると英語の短いエラーが返ります。<code>no such table</code> は表の名前違い、
                    <code>no such column</code> は列の名前違い、<code>syntax error</code> は文の書き方の誤り、
                    <code>ambiguous</code> は「どの表の列か曖昧」という意味です。
                    <b>このアプリでは</b>主なエラーは「次に何をすべきか」を添えた文に言い換えられ、
                    AIが自分で書き直します（詳細は3-9を参照）。それでも失敗が続くときは、
                    言い方を変えて聞き直すか、管理者に頼んでカタログの列説明や用語を書き足してもらうと
                    直ることが多いです（AIが名前や意味を推測せずに済むようになるため）。</td></tr>
          </tbody>
        </table>
      </div>
      <div class="small muted mt">
        補足: 表ではSQLの命令語を大文字で書いていますが、小文字でも意味は同じです
        （SQLは命令語の大文字・小文字を区別しないため）。AIが書くSQLでも表記が混ざることがあります。
      </div>
    </div>

  <div class="card mt">
      <div class="card__title">4-4. ER図とデータ設計の用語</div>
      <div class="card__desc">
        管理画面の「結合・ER図」や、チャットにAIが描くER図を「データの地図」として読めるようになるためのカードです。
        表と表の「つながり」にまつわる設計用語をまとめます。
      </div>
      <div class="tablewrap">
        <table class="data">
          <thead><tr><th style="width:210px">用語</th><th>説明</th></tr></thead>
          <tbody>
            <tr><td>ビュー</td>
              <td>よく使うSELECT文に名前を付けて保存したもので、「名前を付けた検索条件」です。
                  データは複製されず、開くたびに元の表から計算し直されるので常に最新になります
                  （Excelでいえば、値を貼り付けたシートではなく、数式のまま置いてあるシートに近い考え方です）。
                  <b>このアプリでは</b>管理者がデータカタログの「ビュー」タブで作れます。作ったビューは
                  テーブルと同じように扱われ、チャットからも使えます。正しい結合を1つ固定しておけるので、
                  AIが毎回結合を組み立て直して間違える余地がなくなります（詳細は3-16bを参照）。</td></tr>
          <tr><td>ER図（イーアールず）</td>
                <td>表（エンティティ＝実体）と表同士の関係（リレーションシップ）を、箱と線で描いた「データの地図」です。
                    どの表とどの表をつなげて集計できるかが一目で分かります
                    （Excelのシート一覧だけでは、シート同士の対応関係までは分からないため）。
                    <b>このアプリでは</b>チャットで「ER図を見せて」と頼むと、誰でもAIに表示してもらえます
                    （チャット側は<b>読むだけ</b>で、線の追加や変更はできません。
                    編集は管理者が管理画面の「結合・ER図」で行います）。
                    まずは箱＝表・線＝結合できる関係、と読んでください。</td></tr>
            <tr><td>関連（リレーション）</td>
                <td>「この表のこの列と、あの表のあの列が対応する」というつながりの登録のことです。
                    ER図の線1本が、この登録1件にあたります。複合キー（複数列の組で結ぶ関連）は、
                    <b>対象の列それぞれから出た線が合流して1本になる</b>形で描かれ、
                    どの列で結んでいるかが目で追えます（中ほどに「複合キー(n列)」の印つき）。
                    <b>このアプリでは</b>AIが<code>JOIN</code>（表の結合）を書くときの根拠になるため、
                    関連の登録の充実がそのまま回答の正確さに効きます
                    （登録が無い結合は、AIが列名などから推測するしかなくなるため）。詳細は3-14を参照。</td></tr>
            <tr><td>主キー</td>
                <td>1行を必ず特定できる「背番号」の列です（社員番号・ロット番号など）。
                    1列で決まらないときは、複数列の組み合わせで特定する複合キーもあります（設備番号＋日付で1日1行、など）。
                    <b>このアプリでは</b>結合候補の判定（3-13）も、データ品質チェックの「主キー重複」の警告も、
                    すべてこの概念の上に載っています。</td></tr>
            <tr><td>外部キー</td>
                <td>他の表の主キーを、自分の列として持つことで表がつながる仕組みです
                    （注文明細が商品コードを持ち、商品マスタを参照する、など）。
                    <b>このアプリでは</b>データ品質チェックの「親に存在しない外部キー」という警告は、
                    参照先のない迷子の値が見つかったという意味です（マスタ未登録・削除済みの参照などで起こります）。</td></tr>
            <tr><td>多重度（1:N・N:1・N:M）</td>
                <td>線の両端に書く「1」と「多」の記号で、行同士の対応の数を表します。
                    たとえば作業実績が何百行あっても、参照する設備の行は1行、という関係はN:1（多対1）、
                    逆から見れば1:N（1対多）、両側とも多ならN:M（多対多）と読みます。
                    <b>このアプリでは</b>矢印を描かないIPA（情報処理推進機構）流の表記で、
                    線の両端に <code>1</code> と <code>*</code>（多）を置きます。
                    多の側を1と取り違えたまま結合すると、行が増えて集計が膨らみ得ます。
                    そのため片方だけが単独の主キー（その1列だけで行を特定できる列）のときは、
                    登録時に自動で向きを直します（詳細は3-14を参照）。</td></tr>
            <tr><td>参照整合性（さんしょうせいごうせい）</td>
                <td>子の表が持つ値は、親の表に必ず存在する、という整合の約束です
                    （明細にある商品コードは商品マスタに必ずいる、など）。
                    <b>このアプリでは</b>関連を登録するとき、この約束が守られているかを実データで検証します。
                    「値が1件も一致しません」なら保存できず、「親に無い値があります」なら件数付きで知らせます
                    （詳細は3-14を参照）。</td></tr>
            <tr><td>マスタと明細</td>
                <td>マスタは名簿・台帳にあたる親側の表（商品マスタ・社員マスタなど）、
                    明細（トランザクション）は出来事を1行1件で記録する子側の表（注文明細・作業実績など）を指す、
                    業務システムの慣用語です。ふつう明細がマスタを外部キーで参照し、多重度はN:1になります。
                    <b>このアプリでは</b>統計ツールに内部で渡される「集計せず明細（1行1件）を返す」という指定も
                    この語で読めます（集計はSQLではなくツール側で行うため）。</td></tr>
            <tr><td>一意（いちい／ユニーク）</td>
                <td>その列に同じ値が2つと現れない、重複ゼロの状態を指すIT用語です
                    （日常語より狭く、「唯一・かぶりなし」の意味に限定されます）。
                    <b>このアプリでは</b>関連の登録時に出る「参照先（1側）の値が一意ではありません」という警告は、
                    結合相手を1行に絞れない状態＝<code>JOIN</code>で行が増えて集計が膨らみ得る状態、という意味です。</td></tr>
            <tr><td>コード値</td>
                <td>1＝良品・2＝不良のように、意味を短い記号に置き換えた値のことです（区分値とも呼びます）。
                    意味そのものはデータからは読み取れません（数字を見ても、どちらが良品かは決められないため）。
                    <b>このアプリでは</b>カタログの「コード値の意味」欄に対応表が書かれて初めて、AIが正しく集計に使えます。
                    値の一覧は「実際の値」欄に自動で出るため、管理者が意味を書き足すだけで済みます。</td></tr>
            <tr><td>値域（ちいき）</td>
                <td>その列が実際に取り得る値の範囲を指す用語です（1〜5の整数・2020年〜2026年の日付、など）。
                    <b>このアプリでは</b>カタログ画面の「実際の値」欄に自動表示されるのがこの実測値で、
                    値の種類が20以下なら値と件数の一覧、21以上なら最小値と最大値が出ます（詳細は3-11を参照）。
                    管理者が列の説明を書くときの手がかりになります。</td></tr>
            <tr><td>ビュー</td>
                <td>SQLで定義された「仮想の表」です。実体のデータを持たず、開くたびに元の表から計算されます
                    （値を持たず数式だけでできたExcelシートに近いものです）。
                    <b>このアプリでは</b>カタログや自動プロファイル（3-11）の対象に、普通の表と同じ顔で並びます。</td></tr>
            <tr><td>データ品質のチェック観点</td>
                <td>主キーの重複＝二重計上、空の列＝欠損、親に無い外部キー＝突合漏れ、という
                    「データの健康診断」の観点です。どれも集計結果を直接ゆがめます
                    （重複は合計を膨らませ、欠損は件数を欠けさせ、突合漏れは結合時に行を落とすため）。
                    <b>このアプリでは</b>チャットの「データ品質チェック」ツールが、
                    行数・主キーの重複・空の列・親に存在しない外部キー・日付の範囲をこの観点で調べます。
                    ただし<b>警告が無い＝データが正しい、ではありません</b>
                    （形式のゆがみを見るだけで、値の中身が業務として正しいかまでは判定できないため）。</td></tr>
          </tbody>
        </table>
      </div>
      <div class="small muted mt">
        補足: 見た目の凡例（下線＝主キー・破線の下線＝外部キー・線の両端の <code>1</code> と <code>*</code>＝多重度）は
        「結合・ER図」画面にも表示されています。チャットにAIが描くER図も同じ記法・同じデータで描かれるため、
        画面で見える図とAIの理解（結合の定義）は必ず一致します。
      </div>
    </div>

  <div class="card mt">
      <div class="card__title">4-5. 文書検索の用語（RAG・ナレッジベース）</div>
      <div class="card__desc">規定や手順書など「文書」への質問に答える仕組みの背景にある検索技術の用語をまとめます。数字の集計はSQL、文書の内容はここで説明する検索、と質問の行き先が分かれることを押さえるのが目的です（仕組みの数値仕様は3-19を参照）。</div>
      <div class="tablewrap">
        <table class="data">
          <thead><tr><th style="width:210px">用語</th><th>説明</th></tr></thead>
          <tbody>
            <tr>
              <td>RAG（ラグ・検索拡張生成）</td>
              <td>Retrieval-Augmented Generation（検索で補強した文章生成）の略で、AIが答えを書く前に関係する文書を検索し、見つかった部分を読ませてから書かせる方式です。AIが元から何でも知っているのではなく、質問のたびに資料を調べてから答える「持ち込み可の試験」のような仕組みです。<b>このアプリでは</b>ナレッジベースへの質問がこの方式で動いており、AIは検索で取り出した本文を根拠に回答を書きます。接続先の製品名「LightRAG」の「RAG」もこの略です。</td>
            </tr>
            <tr>
              <td>ナレッジベース</td>
              <td>一般には、規定・手順書・過去の事例といった知識を蓄積しておく置き場を指す言葉です。<b>このアプリでは</b>LightRAGサーバ1台に預けた文書のまとまりを1つのナレッジベースと呼び、このヘルプでは「KB」と略すことがあります。サイドバーの「LightRAG」でチェックを入れたナレッジベースだけが検索対象になります（用途の違う文書群を混ぜずに使い分けるため）。</td>
            </tr>
            <tr>
              <td>LightRAG（ライトラグ）</td>
              <td>文書を預かり、索引を作って検索に応じるオープンソースの検索サーバの製品名（固有名詞）です。<b>このアプリでは</b>本体とは別のサーバとして動いており、管理者が「ナレッジベース」画面にURLとAPIキーを登録して接続します（索引作成が重い処理のため、サーバを分けています）。利用者が直接操作することはありません。通信の詳細は3-19を参照してください。</td>
            </tr>
            <tr>
              <td>ベクトル検索・埋め込み</td>
              <td>言葉や文章を数値の並び（ベクトル）に変換することを埋め込み（エンベディング）と呼びます。その数値どうしの近さで「意味が似た文章」を探すのがベクトル検索です。キーワードが一致しなくても、「不具合」と聞いて「故障」の記述を見つけられます。その代わり、文字の一致を探すCtrl+F検索と違い、<b>確実にあるはずの文書を取りこぼすこともあります</b>（一致ではなく意味の近さで選ぶため）。<b>このアプリでは</b>ナレッジベース検索の土台がこの方式なので、見つからないときは言い方を変えて聞き直すのが有効です。</td>
            </tr>
            <tr>
              <td>ナレッジグラフとエンティティ</td>
              <td>エンティティは文書に登場する物・人・概念（設備名・材料名・工程名など）のことで、それらのつながりを網の目のように整理したものがナレッジグラフです。「AはBの部品」「CはDの原因」といった関係をたどれるため、離れた文書同士も結び付けられます。<b>このアプリでは</b>LightRAGが文書の取り込み時にこの網を自動で作り、検索設定の「エンティティ／関係の取得数」は、この網からいくつ拾ってAIに見せるかの指定です（検索モードが naive のときは使われません）。</td>
            </tr>
            <tr>
              <td>チャンク（文書の断片）</td>
              <td>文書を検索しやすい大きさに切った断片のことです（英語で「かたまり」の意味）。長い文書を丸ごと照合するのではなく、断片の単位で質問に近いところだけを取り出します。<b>このアプリでは</b>検索設定の「1つのナレッジベースから取る文章数」がこの断片の数で、増やすと拾える情報は増えますが、検索が遅くなりAIに送る量も増えます（読ませる文章が長くなるため）。</td>
            </tr>
            <tr>
              <td>検索モード（mix・hybrid・local・global・naive）</td>
              <td>LightRAGに用意された、検索の進め方の選択肢です。<code>mix</code>＝ナレッジグラフとベクトル検索の併用、<code>local</code>＝特定の物事についての具体的な話向き、<code>global</code>＝全体像や傾向の質問向き、<code>hybrid</code>＝localとglobalの併用、<code>naive</code>＝グラフを使わない単純なベクトル検索のみ、という使い分けです。<b>このアプリでは</b>サイドバーの「検索設定」の「検索モード」で利用者ごとに選べますが、迷ったら既定の<code>mix</code>のままで構いません。</td>
            </tr>
            <tr>
              <td>出典（[出典n]）</td>
              <td>回答の根拠となった文書を指す番号で、論文や報告書の引用番号と同じ役割です。<b>このアプリでは</b>文書を使った回答に「[出典1]」のような番号が付き、回答に添えられる出典一覧で、番号からナレッジベース名・ファイル名をたどって原本に当たれます。ただし<b>番号があっても本文はAIの要約</b>なので、重要な判断の前には原本を確認してください（要約の過程で条件やただし書きが落ちることがあるため）。</td>
            </tr>
            <tr>
              <td>自然言語（しぜんげんご）</td>
              <td>プログラム言語や検索用の特別な構文ではない、人間が普段使う言葉を指すIT用語です。日本語も英語も自然言語です。<b>このアプリでは</b>チャットの質問がまさに自然言語で、特別な書式や記号を覚えなくても普通の日本語で聞けば伝わります。画面の説明欄にある「自然言語で構いません」という注記も同じ意味です。AIは書かれた文をそのまま読んで理解するため、隣の席の人に説明するつもりで書くのが一番効きます。</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

  <div class="card mt">
      <div class="card__title">4-6. 統計・分析の用語</div>
      <div class="card__desc">
        統計ツールの結果表や所見に出てくる専門用語をまとめます。数式は使わず、「その数字をどう読めばよいか」だけを説明します。
        手法名をすべて覚える必要はなく、結果に出てきたときに引く辞書として使ってください。
      </div>
      <div class="tablewrap">
        <table class="data">
          <thead><tr><th style="width:210px">用語</th><th>説明</th></tr></thead>
          <tbody>
            <tr><td>平均・中央値・標準偏差</td>
                <td>平均は合計÷件数、中央値は小さい順に並べたときの真ん中の値、標準偏差はばらつきの大きさを測る物差しです。
                    ごく大きな値が少数混じる「裾の長い」データでは平均がそちらに引っ張られるため、中央値の方が実感に合います。
                    <b>このアプリでは</b>基本統計の結果表に3つとも並びます。分布分析では、右に裾が長いデータに「平均より中央値を見た方が実感に合います」という所見が自動で付きます。
                    管理図に出る「±3σ」は、平均から標準偏差3個分の幅という意味です。</td></tr>
            <tr><td>四分位（しぶんい）・パーセンタイル・箱ひげ図</td>
                <td>四分位は、データを小さい順に並べて4等分する区切り（25%・50%＝中央値・75%）です。
                    パーセンタイルは「下から数えて何%目の値か」で、90パーセンタイルなら全体の9割がその値以下に収まります。
                    箱ひげ図はこれを図にしたもので、箱＝真ん中の50%・箱の中の線＝中央値・ヒゲの外の点＝外れ値の候補、と読みます。
                    <b>このアプリでは</b>基本統計の結果表に四分位が並び、グラフの種類「箱ひげ」でカテゴリ別のばらつきを見比べられます。</td></tr>
            <tr><td>ヒストグラムと確率分布</td>
                <td>ヒストグラムは、連続する数値を階級（ビン）に区切り、区間ごとの件数を棒にした図です。
                    棒グラフが項目ごとの値を比べるのに対し、ヒストグラムは1つの数値の散らばり方を見ます（棒の間に隙間がないのはこのため）。
                    分布の基本形は正規分布 — 左右対称の釣り鐘型です。
                    <b>このアプリでは</b>分布分析がヒストグラムの度数表と「どの分布に近いか」の推定を返します。
                    結果に分布名（対数正規＝右に長い裾・指数＝小さい値ほど多い・一様＝どの値もほぼ同じ、など）が出たときは、どんな形かが分かれば十分です。</td></tr>
            <tr><td>外れ値（はずれち）と異常検知</td>
                <td>外れ値は、いつもの水準から大きく離れた値のことです。
                    IQR（四分位範囲）・Zスコア・MADといった名前は、「どれだけ離れたら外れとみなすか」の物差しの種類です。
                    <b>外れ値＝誤りとは限りません</b> — 実際に起きた特異な事象のこともあるため、削除より先に原因の確認が要ります。
                    <b>このアプリでは</b>外れ値の抽出に5手法を使い分け（詳細は3-20を参照）、時系列の異常検知は前後の期間と比べる方式のため、一時的な外れと、水準そのものが変わる変化点（段差）を区別できます。</td></tr>
            <tr><td>相関と散布図</td>
                <td>相関係数は、2つの数値が一緒に動く度合いを-1〜1で表した数です（プラスは同方向・マイナスは逆方向）。
                    散布図は点1つ＝1件で、点が斜めに並ぶほど相関が強いと読みます。
                    <b>相関があっても因果とは限りません</b>（第3の要因が両方を動かしていることがあるため）。
                    <b>このアプリでは</b>相関の検定を頼むと、所見に強弱の目安（0.2未満＝ほぼ無相関〜0.7以上＝強い相関）とこの注意が添えられます。
                    第3の要因の影響を除いてから相関を見るのが偏相関、先月の値が今月に効く関係を見るのが時差相関（ラグ相関）です。</td></tr>
            <tr><td>仮説検定・p値・有意水準</td>
                <td>仮説検定は、「その差は偶然の範囲か」を確率で判定する手続きです。
                    p値は「本当は差がなくても、偶然でそれくらいの差が出る確率」で、小さいほど偶然では説明しにくくなります。
                    有意水準0.05は「p値がこれを下回ったら偶然とは考えにくいとみなす」という線引きの約束事です。
                    <b>このアプリでは</b>有意水準は<b>0.05</b>で、所見の「有意差あり／なし」はこの線引きの結果を言葉にしたものです。</td></tr>
            <tr><td>検定の手法名と効果量</td>
                <td>t検定＝2群の平均の差、分散分析＝3群以上の比較、カイ二乗＝割合の偏り、Mann-Whitneyなどの順位系＝外れ値に強い、多重比較補正＝何度も比べるときの厳しめの調整、という使い分けです。
                    効果量（Cohen's d など）は「差の大きさそのもの」を表す数です。
                    <b>有意＝大きな差、ではありません</b>（件数が多いと、わずかな差でも有意になるため）。
                    <b>このアプリでは</b>13手法を備え、結果には効果量が併記されます。分散分析で有意なら Bonferroni 補正つきの多重比較まで自動で行います（詳細は3-20を参照）。</td></tr>
            <tr><td>回帰分析</td>
                <td>結果（目的変数）を、要因の候補（説明変数）で説明する式を当てはめる分析です。
                    係数は「その要因が1増えたときの効き目」、R²（決定係数）は「あてはまりの良さ」を0〜1で表した数と読みます。
                    <b>このアプリでは</b>部署などの文字列の列を自動でダミー変数（区分を0／1の列に開いたもの）にし、VIF（説明変数どうしが似すぎている度合い）や残差（予測と実績のずれ）の偏りを警告します。
                    所見には「回帰は因果を証明するものではない」という注意も付きます（詳細は3-20を参照）。</td></tr>
            <tr><td>時系列分析</td>
                <td>時間順のデータを、トレンド（長期の傾向）＋季節性（毎年・毎月繰り返す周期パターン）＋残り、に分解して見る分析です。
                    移動平均は直近数期の平均でギザギザを均す基本技、自己相関は「何期前の自分と似ているか」、前年同月比は季節性を打ち消して比べるための比較です。
                    <b>このアプリでは</b>移動平均・前期比・自己相関（最大6ラグ）を一度にまとめて返し、周期を指定すると前年同期比と季節分解も加わります（詳細は3-20を参照）。</td></tr>
            <tr><td>予測と誤差指標（MAPE・MAE）</td>
                <td>予測は1本の線ではなく、幅（予測区間）で読むのが基本です（先になるほど不確かさが増すため）。
                    MAPE（外した割合の平均、%）とMAE（外した量の平均）は、過去のデータで測った予測の成績表です。
                    結果に出る Holt-Winters や ARIMA は「過去の動きのくせを織り込んで先を延ばす、定番の時系列モデル」程度の理解で十分です。
                    <b>このアプリでは</b>95%の予測区間つきで返り、8点以上あればバックテスト（過去の一部を隠して当てる検証）で誤差も報告します。
                    <b>施策や外部要因の変化は予測に反映されません</b>（過去の形をなぞる手法のため）。詳細は3-20を参照してください。</td></tr>
            <tr><td>信頼区間・ブートストラップ・モンテカルロ</td>
                <td>いずれも「点でなく幅で考える」ための道具です。
                    信頼区間は「本当の値がこの幅にある確からしさ（95%など）」、ブートストラップは手元のデータから何度も引き直して幅を出す方法、モンテカルロは不確かな入力でサイコロを大量に振り、結果の幅と確率を見る方法です。
                    感度分析は「どの前提が結果を最も揺らすか」の特定です。
                    <b>このアプリでは</b>ブートストラップは5,000回の引き直し、モンテカルロは10,000回の試行が既定で、乱数の種を固定しているため同じ条件なら同じ結果になります（再現性のため。詳細は3-20を参照）。</td></tr>
            <tr><td>クラスタ分析（k-means）</td>
                <td>似たもの同士を自動でグループ分けする手法で、k-meansはその代表格です（kはグループ数）。
                    単位の違う列が混ざると大きい数字の列に結果が引きずられるため、揃えてから分けます（標準化）。
                    シルエット係数は分かれ具合の採点で、1に近いほどきれいに分かれています。
                    <b>このアプリでは</b>標準化は自動で行われ、kも自動選択できます。シルエット係数が0.25未満なら「はっきり分かれていない」と警告します（詳細は3-20を参照）。</td></tr>
            <tr><td>ABC分析とパレート図</td>
                <td>売上などの大きい順に並べ、累計の構成比でA／B／Cに区分し、少数の重要品目に管理を集中するための定番手法です。
                    「上位2割で全体の8割を占める」という経験則（パレートの法則）が土台にあります。
                    パレート図は棒（個別の値）＋折れ線（累計%）の組み合わせで読みます。
                    <b>このアプリでは</b>既定で累計70%までがA・90%までがB・残りがCです（詳細は3-20を参照）。</td></tr>
            <tr><td>業務分析の型（ファネル・コホート・併売・寄与度・生存時間）</td>
                <td>ファネルは工程を漏斗に見立て、どの段階で落ちる・詰まるかを見ます。
                    コホートは同じ時期に始めたグループを追いかけ、どれだけ残っているか（継続率）を見ます。
                    併売（へいばい）は一緒に買われる組み合わせを探します（リフト1.0前後＝無関係、が基準）。
                    寄与度は全体の増減を区分ごとの貢献に分解するもので、増減の内訳はウォーターフォール図で描けます。
                    生存時間分析は壊れる・やめるまでの期間を、まだ起きていない件（打ち切り）を捨てずに測ります（捨てて平均すると必ず短く見積もるため。MTBFやWeibullはこの仲間です）。
                    <b>このアプリでは</b>いずれもチャットから頼める分析ツールとして入っています。</td></tr>
          </tbody>
        </table>
      </div>
      <div class="small muted mt">
        補足: 各手法の対応範囲と既定値（試行回数・有意水準など）は3-20にまとまっています。
        結果に添えられる所見には数値の読み方が日本語で書かれているため、まず所見を読み、分からない言葉だけをこの表で引くのが近道です。
      </div>
    </div>

  <div class="card mt">
    <div class="card__title">4-7. パソコン・ネットワーク・ファイルの基礎</div>
    <div class="card__desc">サーバやCookieなど、Webアプリを使ううえで前提になっているパソコンとネットワークの基礎、そしてファイル形式の約束をまとめます。「サーバの再起動でファイルが消える」「CSVが文字化けする」といった注意書きの理屈が、ここを読むと分かります。</div>
    <div class="tablewrap">
      <table class="data">
        <thead><tr><th style="width:210px">用語</th><th>説明</th></tr></thead>
        <tbody>
          <tr>
            <td>サーバ</td>
            <td>みんながネットワーク越しに接続して使う共用のコンピュータのことです。目の前のPCとは<b>別の機械</b>で、画面に映っていても中身が手元にあるとは限りません。<b>このアプリでは</b>本体・取り込んだデータ・AIが作ったファイルがすべてサーバ側にあります。注意書きの「サーバの再起動で消えます」は、この共用の機械を再起動したときの話で、手元のPCの再起動とは無関係です。</td>
          </tr>
          <tr>
            <td>Webアプリとブラウザ</td>
            <td>Webアプリは、EdgeやChromeなどのブラウザでURLを開くだけで使えるアプリの形です。プログラムの本体はサーバ側で動くため、インストール型のソフトと違って各自のPCに導入作業をする必要がありません。<b>このアプリでは</b>この形を採っています。構成図（第2部）の「素のHTML/JS」という表記は、画面がブラウザに元から備わっている仕組みだけで動く作りであることを表し、この場合も各自のPCに追加のソフトは要りません。</td>
          </tr>
          <tr>
            <td>URL・IPアドレス・ポート番号</td>
            <td>IPアドレスは機械の住所、ポート番号は同じ機械の中の窓口の番号です。<code>http://サーバのIP:8000</code> というURLは「この住所の機械の、8000番の窓口」と読めます。<b>このアプリでは</b>本体がポート8000で待ち受けています。URLは場所を指すだけで<b>鍵ではない</b>ため、同僚にURLを送っても、本人がログインしていなければログイン画面に回されます。</td>
          </tr>
          <tr>
            <td>HTTPとHTTPS</td>
            <td>ブラウザとサーバが通信するときの約束（通信規約）で、末尾にSが付くHTTPSは中身が暗号化されます。ブラウザのアドレス欄の鍵マークは、このHTTPSの印です。<b>このアプリでは</b>社外へ出るChatGPT-APIの呼び出しがHTTPS、社内で完結するアプリ本体やLightRAGとのやり取りがHTTPです。構成図（第2部）の「HTTPS・社外」「社内・HTTP」という注記は、この区別を表しています（社内だけを通る通信は暗号化なしで割り切っているため）。</td>
          </tr>
          <tr>
            <td>社内ネットワークとインターネット</td>
            <td>社内ネットワークは会社の中だけで通じる網、インターネットは世界中につながる網で、両者の間には境目があります。<b>このアプリでは</b>本体が社内ネットワークの内側で動き、外へ出て行く通信はAIモデル（ChatGPT-API）の呼び出しだけです（メールの送信も、社内のメールサーバに渡すところまでです）。社外や在宅の回線から開けないのは故障ではなく、この境目の内側にあるためです。</td>
          </tr>
          <tr>
            <td>セッションとCookie（クッキー）</td>
            <td>セッションは「ログインしている状態」の継続、Cookieはそれを覚えておくためにブラウザ側に置かれる小さなメモです。画面を開くたびにこのメモが名札の役割をして、「さっきログインした本人です」とサーバに伝えます。<b>このアプリでは</b>署名付きCookie（偽造や書き換えをサーバが見破れるように印を付けたもの）を使い、<b>ブラウザを閉じるとログアウト</b>になります。Cookieを削除するとログインが外れるのも、名札を捨てたのと同じ状態になるためです。サーバの再起動ではログアウトしません（詳細は3-22を参照）。</td>
          </tr>
          <tr>
            <td>認証と認可（権限）</td>
            <td>認証は「あなたは誰か」の本人確認、認可は「その人にその操作を許すか」の判定で、別々の段階です。<b>このアプリでは</b>ログインが認証にあたり、同じアプリでも一般利用者と管理者で見える画面や押せるボタンが違うのが認可です（詳細は3-22を参照）。第3部に出てくるSQLiteの「認可コールバック」もこの仲間で、AIの書いたSQLを最後の関門で<b>読むだけ</b>に絞る門番の役割をします（詳細は3-8を参照）。</td>
          </tr>
          <tr>
            <td>メモリとディスク</td>
            <td>コンピュータの記憶には2種類あり、メモリは高速ですが電源断や再起動で消える作業机、ディスクは低速でも残る引き出しにあたります。<b>このアプリでは</b>AIが作ったExcelなどのダウンロードファイルの実体をディスクに書かず、サーバのメモリに置いています。そのため<b>サーバの再起動や保管の上限で消えます</b>。必要なファイルは案内が出ているうちに手元へ保存してください（後から同じURLでは取り出せなくなるため）。詳細は3-21を参照してください。</td>
          </tr>
          <tr>
            <td>キャッシュ</td>
            <td>一度調べた・作った結果の取り置きで、2回目以降を速くする仕組みの総称です。速さと引き換えに、取り置きが古いままだと最新の状態とずれることがあります。<b>このアプリでは</b>「さっきの結果」の使い回しがその一例で、サーバの再起動などで失効すると同じSQLで取り直しになります（詳細は3-9を参照）。画面の表示が崩れたときに「ブラウザのキャッシュを消して再読み込み（Ctrl+F5）」と案内されるのも、古い取り置きを捨てるための定番の対処です。</td>
          </tr>
          <tr>
            <td>拡張子（かくちょうし）</td>
            <td>ファイル名の末尾に付く <code>.csv</code> や <code>.xlsx</code> のことで、ファイルの種類を表す約束です。Windowsの初期設定では表示されないため、エクスプローラーの「表示」メニューで「ファイル名拡張子」にチェックを入れると確認できます。<b>このアプリでは</b>取り込み（管理者の操作）で受け付ける形式が <code>.csv</code>・<code>.tsv</code>・<code>.txt</code>・<code>.xlsx</code>・<code>.xlsm</code> に固定されており、Excel系かCSV系かも拡張子で見分けています（詳細は3-17を参照）。</td>
          </tr>
          <tr>
            <td>CSV（シーエスブイ）／TSV</td>
            <td>値をカンマ（CSV）またはタブ（TSV）で区切って並べただけの文字ファイルです。Excelで開くと表に見えますが、色・数式・複数シートは持てない別物です。<b>このアプリでは</b>AIが作るダウンロードファイルの形式のひとつがCSVです。また、管理者が使う取り込み画面の「区切り文字」の選択は、この区切り記号の指定にあたります（自動判定でうまく列に分かれないときに手で直せるようにするため）。</td>
          </tr>
          <tr>
            <td>文字コードと文字化け</td>
            <td>文字コードは、文字をコンピュータ内部の番号に対応づける表（UTF-8・Shift_JISなど）のことで、複数の方式があります。書いたときと違う表で読むと「譁�蟄�」のように化けますが、ファイル自体が壊れたわけではありません（対応表を取り違えているだけのため）。<b>このアプリでは</b>ダウンロード用のCSVを、Excelで開いても化けない <code>utf-8-sig</code> という方式で作ります。古いシステム向けにShift_JISが必要なときは、チャットで「Shift_JISで」と頼むと <code>cp932</code>（Shift_JISの一種）で作れます。取り込みでは主要な文字コードを自動で順に試すため、たいていはそのまま読めます。それでも化けたときは、元ファイルをメモ帳で開いて「名前を付けて保存」で文字コードをUTF-8にしてから、取り込み直してください（取り込みの操作は管理者が行います）。</td>
          </tr>
          <tr>
            <td>Markdown（マークダウン）</td>
            <td><code>#</code> で見出し、<code>|</code> で表、のように記号で構造を書く軽いテキストの書式です。専用ソフトは不要で、メモ帳でも開ける普通の文字ファイルです。<b>このアプリでは</b>レポートのダウンロード形式 <code>md</code> がこれにあたります。AIの回答の見出しや表も、この書式を画面用に変換して表示しています。</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="small muted mt">補足: ブラウザの「キャッシュの削除」と「Cookieの削除」は設定画面で隣り合っていることが多く、キャッシュだけ消すつもりでCookieまで消してログインが外れることがあります（削除の対象にチェックが入っていないか確かめてから実行してください）。</div>
  </div>

  {% if user.is_admin %}
  <div class="card mt">
      <div class="card__title">4-8. 管理者向けの運用用語</div>
      <div class="card__desc">
        管理者が設定変更・起動・保守の場面で出会う技術用語をまとめます。
        ここでは概念だけを説明し、具体的な手順や設定値は第3部の該当カード（3-1〜3-27）を参照してください。
      </div>
      <div class="tablewrap">
        <table class="data">
          <thead><tr><th style="width:210px">用語</th><th>説明</th></tr></thead>
          <tbody>
            <tr><td>環境変数と<code>env</code>ファイル</td>
                <td>プログラムの外側から設定値を渡す仕組みが環境変数で、コード本体を書き換えずに動作を変えられます（設定のたびにプログラムを直すと、間違いの入り込む余地が増えるため）。envファイルは、その設定を「名前=値」の行で並べたテキストファイルです。
                    <b>このアプリでは</b>起動フォルダの <code>env</code> ファイル（先頭にドットの無い名前）が、3-25の一覧で「変更可」とされた設定を上書きする入口です。
                    ただし待ち受けのアドレスとポートは環境変数を読まず、<code>core.py</code> 末尾に書いた値がそのまま使われます（他のソフトが設定した <code>PORT</code> を拾って別のポートで起動する事故を防ぐため）。読み込みの詳細は3-1・3-25を参照してください。</td></tr>
            <tr><td>CLI（コマンドライン）と終了コード</td>
                <td>画面のボタンではなく、文字だけの画面（端末）に命令文を打ち込む操作方法をCLIと呼びます。たとえば <code>python core.py users add</code> は「Pythonに <code>core.py</code> を実行させ、続く <code>users add</code> で指示を渡す」と読みます。
                    終了コードは命令が終わるときに返す数字で、<b>0＝成功・0以外＝失敗</b>が世界共通の約束です（人が画面を見ていなくても、自動化の仕組みが成否を判定できるため）。
                    <b>このアプリでは</b>利用者管理（<code>users</code>）と定期取り込み（<code>refresh</code>）がCLIで、<code>refresh</code> は0＝全成功または対象なし・1＝1本でも失敗を返します（3-1参照）。</td></tr>
            <tr><td>スケジューラ・ジョブ・cron（クーロン）</td>
                <td>スケジューラは決めた時刻や間隔で自動的に処理を走らせる係、ジョブはそこに登録された1件の仕事です。cronはUNIX系OSに昔からある定時実行の仕組みの名前で、Windowsの「タスクスケジューラ」が同じ役どころです。
                    <b>このアプリでは</b>誰も画面を開いていない夜中でも定期取り込みが動くのは、アプリ内蔵のスケジューラが60秒ごと（変更可）に各ジョブの期限を確認しているためです。
                    別経路として、OS側のcronから <code>python core.py refresh</code> を実行する方法も用意されています（アプリ内蔵側が止まっていても確実に動かすため）。詳細は3-18を参照してください。</td></tr>
            <tr><td>PythonとFlask（フラスク）</td>
                <td>Pythonはこのアプリを書いているプログラミング言語、FlaskはPythonでWebアプリを作るための土台（フレームワーク）です。どちらも道具の名前だと分かれば、第3部の文の主語が読めるようになります。
                    同類の道具として、画面の雛形に値を流し込むJinja2（ジンジャ）、機能単位の部品であるブループリントという名前も出てきます。
                    <b>このアプリでは</b>Python+Flaskの1プロセスで画面とAPIの両方を返し、チャット／カタログ／取り込みなど11個のブループリントに分かれています（3-1参照）。</td></tr>
            <tr><td>本番用サーバとリバースプロキシ</td>
                <td>本番用サーバは、多数の同時アクセスを安定してさばくためのWebサーバで、waitress（ウェイトレス）やgunicorn（ガニコーン）が代表です（Flask付属の簡易サーバは開発向けのため）。このアプリの <code>python core.py</code> は内部でwaitressを使って待ち受けるので、本番でも同じコマンドのまま載せ替えは不要です。
                    リバースプロキシは利用者とアプリの間に置く中継サーバのことで、代表がnginx（エンジンエックス）です。
                    <b>このアプリでは</b>nginxを前段に置く場合、回答の逐次表示（ストリーミング）が中継でため込まれないよう <code>proxy_buffering off;</code> の指定が必要です（切らないと回答がまとめて一度に届くため）。起動コマンドは3-1を参照してください。</td></tr>
            <tr><td>プロセス・スレッド・ワーカー</td>
                <td>プロセスは独立した1人の作業員、スレッドはその作業員がこなす掛け持ち作業、ワーカーはリクエストをさばくために立てる作業単位（多くはプロセス）を指します。作業員を増やせば速くなりそうですが、全員が同じ道具箱を前提にしている場合は逆に壊れます。
                    <b>このアプリでは</b>運用の最重要ルールとして<b>ワーカーは必ず1本</b>にします（プロセスを増やすと内蔵スケジューラがその数だけ立って同じ取り込みを多重実行し、メモリ上に持つ生成ファイル置き場も分裂するため）。
                    同時アクセスはスレッド数（waitress の <code>--threads</code>）で増やします。waitress は元から1プロセスのため、この心配はありません（3-1・3-27参照）。</td></tr>
            <tr><td>標準出力とログ</td>
                <td>標準出力はプログラムが文字を流す既定の出口で、端末から起動するとその画面に流れて見えます。ログは動作の記録という意味の言葉で、出口（標準出力）と記録（ログ）は別の概念です。
                    <b>このアプリでは</b>ログファイルを作らず、記録はすべて標準出力へ流します（ファイルの肥大化や世代管理という保守作業を持ち込まないため）。
                    ファイルに残したい場合は、起動時に出力先を振り向けます（リダイレクト。例: <code>python core.py &gt; app.log 2&gt;&amp;1</code>）。行頭の分類は3-26を参照してください。</td></tr>
            <tr><td>JSON・YAML・JSONL</td>
                <td>いずれも人がそのまま読み書きできるテキストのデータ書式です。JSON（ジェイソン）は波括弧で入れ子を表す形式、YAML（ヤムル）は字下げで構造を表す設定向きの形式、JSONLは1行1件のJSONを下に積み上げていく追記型の形式です（1行足すだけで済み、全件を書き直さずに済むため履歴向きです）。
                    <b>このアプリでは</b>カタログ（<code>.meta.yaml</code>）や各種設定がYAML、会話の実体がJSON、取り込み・カタログの変更履歴がJSONL（<code>import_history.jsonl</code> など）です。
                    メモ帳でも開けますが、字下げや記号を1つ壊すだけで読み込みに失敗するため、編集は画面から行うのが安全です（3-23参照）。</td></tr>
            <tr><td>ハッシュ化</td>
                <td>元に戻せない一方向の変換です。パスワードは平文（そのままの文字）を保存せず、変換後のハッシュだけを保存し、ログイン時は入力を同じ方法で変換して突き合わせます（保存場所を見られてもパスワードそのものは漏れないため）。
                    ソルトは同じパスワードでも別の保存値になるようにする混ぜ物、反復回数は総当たりの解読を遅くするための繰り返し回数です。
                    <b>このアプリでは</b>PBKDF2-SHA256（反復20万回・ソルトは利用者ごとに個別）でパスワードを保存します（3-22参照）。
                    なお同じ「ハッシュ」という言葉は、検索結果の重複除去などに使う「内容の指紋」の意味でも登場します — こちらは秘密を守る用途ではなく、内容が同じかどうかを見分ける別場面です。</td></tr>
            <tr><td>SQLインジェクションとプレースホルダ</td>
                <td>SQLインジェクションは、入力欄に書いた文字列にSQLの断片を紛れ込ませて、データを盗んだり壊したりする古典的な攻撃です。
                    プレースホルダ（バインド変数）はそれを封じる書き方で、SQL文には <code>:dept</code> のような目印だけを置き（例: <code>WHERE 部署 = :dept</code>）、値は文に混ぜず別口で渡します（値が命令として解釈される余地が無くなるため）。
                    <b>このアプリでは</b>ユーザー定義ツールのパラメータが必ずバインド変数として渡ります。3-10にある「SQLインジェクションは起こりません」という記述の根拠がこの仕組みです。</td></tr>
            <tr><td>JSONスキーマ</td>
                <td>項目の名前・型（文字列や数値といった値の種類）・必須かどうか・説明といった「データの形の決まり事」を、機械が読める形で宣言する書式です。tool calling（AIに道具を使わせる仕組み）では、この書式で各道具の引数の形をAIに教えます。
                    <b>このアプリでは</b>ツールの定義がOpenAIのfunction calling形式（名前・説明・引数のJSONスキーマ）で、ユーザー定義ツールの画面で書くパラメータ定義がこれにあたります（3-10参照）。</td></tr>
            <tr><td>正規表現</td>
                <td>文字のパターンで照合するための記法です。たとえば <code>\w</code> は「単語の部品になる1文字」（英数字やアンダースコアのほか、日本語の文字も含みます）を表し、組み合わせると「この表名が独立した単語として現れる箇所」を機械的に探せます。
                    <b>このアプリでは</b>SQLがどの表に触れたかの判定や、ER図の線の濃さの数え上げが、SQLの厳密な構文解析ではなく正規表現による名前の照合で動いています。多少の取りこぼしを許す設計上の割り切りで、その前提は3-27に書かれています。</td></tr>
            <tr><td>SMTP・ドメイン・LDAP（エルダップ）</td>
                <td>SMTP（エスエムティーピー）はメール送信の世界共通規格です。Outlookなどのメールソフトを介さず、アプリが送信サーバへ直接メールを渡す経路で、メール設定画面の「接続確認」で疎通（つながるかどうか）を確かめられます。
                    ドメインはメールアドレスの@より後ろの部分で、組織を表す単位です。LDAPは社内共通のアカウント台帳（ディレクトリサービス）の規格です。
                    <b>このアプリでは</b>実際に送れる宛先は管理者が1件ずつ登録した許可リストのアドレスだけで、そもそも登録できるアドレスもドメイン単位で制限できます（社外のドメインを入口で締め出すため。3-21参照）。
                    また現在のローカル利用者管理は社内共通認証（LDAPなど）へ切り替えるまでの暫定で、社内認証APIへの切り替え口が用意されています（3-22参照）。</td></tr>
            <tr><td>排他制御と原子的な置き換え</td>
                <td>排他制御は、同じものを同時に触って壊さないための順番待ちです。触る人が鍵（ロック）を取り、持っている間は他の人が待つことで、作業が1列に並びます（これを直列化と呼びます）。
                    原子的（アトミック）な置き換えは、書き換え途中の壊れた状態が決して外から見えない書き換え方で、完成品を一時ファイルとして隣に作り、最後に一瞬で差し替えます（途中で止まっても古い完成品が無事に残るため）。
                    <b>このアプリでは</b>第3部に出てくる「鍵で直列化」「一時ファイル経由の原子的な置き換え」がこの2語のことで、定期取り込みの多重実行防止や設定・履歴ファイルの書き込みに使われています（3-23・3-24参照）。</td></tr>
          </tbody>
        </table>
      </div>
    </div>

  {% endif %}

{# 第5部は「コードを触る人向け」。保存レイアウト・権限の一覧・認証の設定など、
   運用の内側が書いてあるので管理者だけに出す。
   囲いは {% raw %} の外側に置くこと。{% raw %} の中は Jinja が評価しないので、
   中に {% if %} を書いても文字として出るだけで効かない。 #}
{% if user.is_admin %}
{% raw %}
  <!-- ==================================================================== -->
  <!-- 第5部 実装リファレンス（管理者のみ） -->
  <!-- ==================================================================== -->
  <h2 id="impl" class="mt" style="font-size:20px">第5部 実装リファレンス</h2>

  <div class="card mt">
    <div class="card__desc">
      このアプリの中身を、コードを読む人向けに書き起こした章です。<b>「何ができるか」ではなく「どう動くか」</b>——処理の順序・分岐条件・データ構造・しきい値を、実装のとおりに並べています。<br>第3部が「使う人が知っておくとよい仕様」なのに対して、ここは<b>これから core.py（37,458行）を触る人が、最初に読むためのもの</b>です。重なる話題もありますが、粒度が違います。<br>各節の最後に<b>「落とし穴」</b>を置きました。<b>実装を読まないと分からないことだけ</b>を集めた欄で、ここだけ拾い読みしても意味が通ります。<br><span class="small muted">行番号は改修のたびに変わるので書いていません。関数名で探してください。</span>
    </div>
  </div>

  <div class="card mt">
    <div class="card__title">この部の目次</div>
    <div class="card__desc">
      <a href="#impl-map"><b>5-0. コードの地図</b></a> ／ <a href="#impl-request"><b>5-1. 1問が処理される全経路</b></a> ／ <a href="#impl-prompt"><b>5-2. システムプロンプトの組み立て</b></a> ／ <a href="#impl-router"><b>5-3. AIに見せる表の決め方</b></a> ／ <a href="#impl-sqlguard"><b>5-4. SQL実行の安全機構</b></a> ／ <a href="#impl-tools"><b>5-5. ツール基盤</b></a> ／ <a href="#impl-catalog"><b>5-6. データカタログ</b></a> ／ <a href="#impl-ingest"><b>5-7. 取り込み・改名・削除</b></a> ／ <a href="#impl-rag"><b>5-8. 文書検索（LightRAG）</b></a> ／ <a href="#impl-chart"><b>5-9. グラフ・分析・ファイル出力</b></a> ／ <a href="#impl-auth"><b>5-10. 認証・権限・保存レイアウト</b></a>
    </div>
  </div>

  <div class="card mt">
    <div class="card__title" id="impl-map">5-0. コードの地図</div>
    <div class="card__desc">元は58個のモジュールに分かれていたものを1ファイルへ畳んであります。畳んだあとも <code>import db</code> や <code>catalog.load_meta()</code> がそのまま動くよう、起動時に <code>sys.modules</code> へ自分自身を<b>31個の別名</b>で登録しています。このため<b>モジュールの境界は実行時には存在せず、名前空間は1つ</b>です——同名の <code>def</code> と <code>import</code> がぶつかると、後に書いた方が勝ちます。<span class="small muted">（実際に <code>def inspect</code> が標準ライブラリの <code>import inspect</code> に食われて、機能が死んでいたことがあります）</span></div>
    <div class="tablewrap"><table class="data"><thead><tr><th style="width:210px">項目</th><th>内容</th></tr></thead><tbody>
      <tr><td>規模</td><td>core.py <b>37,458行</b>（1,482,688字）。トップレベルの関数 829、クラス 15、大文字の定数 199。ほかに auth.py（ログイン設定）と config.py（設定）。</td></tr>
      <tr><td>画面まわり</td><td>HTML・CSS・JS もこのファイルの中にあります。Jinja2 は <code>DictLoader(TEMPLATES)</code> で読み、静的ファイルは <code>/static/&lt;path&gt;</code> の自前ルートが ETag つきで返します。<br>・<code>js/app.js</code> … 324,473 字<br>・<code>css/app.css</code> … 50,785 字<br>・<code>help.html</code> … 123,920 字<br>・<code>catalog.html</code> … 20,285 字<br>・<code>chat.html</code> … 6,383 字<br>・<code>models.html</code> … 5,366 字</td></tr>
      <tr><td>ルート</td><td>全 <b>84</b> 本。catalog 29、chat 15、imp 15、knowledge 7、usage 4、mail 3、models 3、tableview 3、auth 2、api 2、help 1。<br>権限は2段だけで、<code>admin_required</code> が60本、<code>login_required</code> が21本、認証なしが3本（ログイン・ログアウト・Plotly配布）。どちらのデコレータも <code>request.path.startswith("/api/")</code> を見て、「APIならJSONで401/403、画面ならリダイレクトか権限ページ」を出し分けます。</td></tr>
    </tbody></table></div>
    <div class="card__title mt">ファイル内の並び</div>
    <div class="tablewrap"><table class="data"><thead><tr><th style="width:300px">節</th><th style="width:110px">開始行</th><th>行数</th></tr></thead><tbody>
      <tr><td>元 advanced.py（統計・予測・業務分析。行番号は inspect で動的に取得される）</td><td class="mono small">75</td><td class="mono small">1,687</td></tr>
      <tr><td>元 analysis.py</td><td class="mono small">1,762</td><td class="mono small">233</td></tr>
      <tr><td>元 db.py</td><td class="mono small">1,995</td><td class="mono small">491</td></tr>
      <tr><td>元 filecheck.py</td><td class="mono small">2,486</td><td class="mono small">390</td></tr>
      <tr><td>元 chats.py</td><td class="mono small">2,876</td><td class="mono small">330</td></tr>
      <tr><td>元 history.py</td><td class="mono small">3,206</td><td class="mono small">157</td></tr>
      <tr><td>元 catalog_history.py</td><td class="mono small">3,363</td><td class="mono small">58</td></tr>
      <tr><td>元 prefs.py</td><td class="mono small">3,421</td><td class="mono small">84</td></tr>
      <tr><td>元 models.py</td><td class="mono small">3,505</td><td class="mono small">522</td></tr>
      <tr><td>元 catalog.py</td><td class="mono small">4,027</td><td class="mono small">1,654</td></tr>
      <tr><td>元 verify.py</td><td class="mono small">5,681</td><td class="mono small">302</td></tr>
      <tr><td>元 sqlusage.py</td><td class="mono small">5,983</td><td class="mono small">282</td></tr>
      <tr><td>元 usage.py</td><td class="mono small">6,265</td><td class="mono small">600</td></tr>
      <tr><td>元 exports.py</td><td class="mono small">6,865</td><td class="mono small">96</td></tr>
      <tr><td>元 excel.py</td><td class="mono small">6,961</td><td class="mono small">233</td></tr>
      <tr><td>元 charts.py</td><td class="mono small">7,194</td><td class="mono small">880</td></tr>
      <tr><td>元 figures.py</td><td class="mono small">8,074</td><td class="mono small">95</td></tr>
      <tr><td>元 docx_report.py</td><td class="mono small">8,169</td><td class="mono small">430</td></tr>
      <tr><td>元 pptx_report.py</td><td class="mono small">8,599</td><td class="mono small">756</td></tr>
      <tr><td>元 business.py</td><td class="mono small">9,355</td><td class="mono small">409</td></tr>
      <tr><td>元 importer.py</td><td class="mono small">9,764</td><td class="mono small">941</td></tr>
      <tr><td>元 jobs.py</td><td class="mono small">10,705</td><td class="mono small">560</td></tr>
      <tr><td>元 scheduler.py</td><td class="mono small">11,265</td><td class="mono small">126</td></tr>
      <tr><td>元 cleanup.py</td><td class="mono small">11,391</td><td class="mono small">498</td></tr>
      <tr><td>元 mailer.py</td><td class="mono small">11,889</td><td class="mono small">814</td></tr>
      <tr><td>元 custom_tools.py</td><td class="mono small">12,703</td><td class="mono small">250</td></tr>
      <tr><td>元 tools/results.py</td><td class="mono small">12,953</td><td class="mono small">151</td></tr>
      <tr><td>元 tools/common.py</td><td class="mono small">13,104</td><td class="mono small">263</td></tr>
      <tr><td>元 tools/schemas.py</td><td class="mono small">13,367</td><td class="mono small">1,564</td></tr>
      <tr><td>元 tools/business.py</td><td class="mono small">14,931</td><td class="mono small">300</td></tr>
      <tr><td>元 tools/files.py</td><td class="mono small">15,231</td><td class="mono small">315</td></tr>
      <tr><td>元 tools/mail.py</td><td class="mono small">15,546</td><td class="mono small">73</td></tr>
      <tr><td>元 tools/query.py</td><td class="mono small">15,619</td><td class="mono small">730</td></tr>
      <tr><td>元 tools/reports.py</td><td class="mono small">16,349</td><td class="mono small">490</td></tr>
      <tr><td>元 tools/stats.py</td><td class="mono small">16,839</td><td class="mono small">103</td></tr>
      <tr><td>元 tools/usage.py</td><td class="mono small">16,942</td><td class="mono small">38</td></tr>
      <tr><td>元 rag/client.py</td><td class="mono small">16,980</td><td class="mono small">187</td></tr>
      <tr><td>元 rag/registry.py</td><td class="mono small">17,167</td><td class="mono small">170</td></tr>
      <tr><td>元 rag/settings.py</td><td class="mono small">17,337</td><td class="mono small">113</td></tr>
      <tr><td>元 rag/retriever.py</td><td class="mono small">17,450</td><td class="mono small">203</td></tr>
      <tr><td>元 tools/knowledge.py</td><td class="mono small">17,653</td><td class="mono small">171</td></tr>
      <tr><td>元 tools/__init__.py</td><td class="mono small">17,824</td><td class="mono small">418</td></tr>
      <tr><td>元 llm.py</td><td class="mono small">18,242</td><td class="mono small">1,196</td></tr>
      <tr><td>元 web.py（Flask ルーティング・画面）</td><td class="mono small">19,438</td><td class="mono small">54</td></tr>
      <tr><td>元 web/filestore.py</td><td class="mono small">19,492</td><td class="mono small">34</td></tr>
      <tr><td>元 web/helpers.py</td><td class="mono small">19,526</td><td class="mono small">248</td></tr>
      <tr><td>元 web/auth_bp.py</td><td class="mono small">19,774</td><td class="mono small">54</td></tr>
      <tr><td>元 web/chat_bp.py</td><td class="mono small">19,828</td><td class="mono small">1,305</td></tr>
      <tr><td>元 web/catalog_bp.py</td><td class="mono small">21,133</td><td class="mono small">1,511</td></tr>
      <tr><td>元 web/import_bp.py</td><td class="mono small">22,644</td><td class="mono small">560</td></tr>
      <tr><td>元 web/mail_bp.py</td><td class="mono small">23,204</td><td class="mono small">44</td></tr>
      <tr><td>元 web/models_bp.py</td><td class="mono small">23,248</td><td class="mono small">49</td></tr>
      <tr><td>元 web/knowledge_bp.py</td><td class="mono small">23,297</td><td class="mono small">155</td></tr>
      <tr><td>元 web/table_bp.py</td><td class="mono small">23,452</td><td class="mono small">524</td></tr>
      <tr><td>元 web/api_bp.py</td><td class="mono small">23,976</td><td class="mono small">34</td></tr>
      <tr><td>元 web/__init__.py</td><td class="mono small">24,010</td><td class="mono small">137</td></tr>
      <tr><td>元 manage_users.py（CLI: python core.py users …）</td><td class="mono small">24,147</td><td class="mono small">126</td></tr>
      <tr><td>元 refresh.py（CLI: python core.py refresh …）</td><td class="mono small">24,273</td><td class="mono small">13,185</td></tr>
    </tbody></table></div>
  </div>

  <div class="card mt">
    <div class="card__title" id="impl-request">5-1. 1問が処理される全経路</div>
    <div class="card__desc">利用者の1問は _begin_turn で検証・スコープ確定・質問の保存まで済ませたあと、_advance（非ストリーミング）または _stream_advance（SSE）のエージェントループに入り、llm.chat → tools.dispatch → 結果を messages に戻す、を最大 config.MAX_AGENT_STEPS（既定10）往復して最終回答に至る。会話は「LLMに送る列 messages」と「画面に描く列 render_log」の2本で持ち、両者はユーザー発言の通し番号でしか対応付かない。ツール結果には _attach_verification が相互検算を付け、不一致は LLM 側（verification_warnings）と画面側（検算カード）の両方へ流し込む。打ち切りは「同じ呼び出しの繰り返し（_Guard）」「往復上限」「空応答」の3系統で、いずれもツールを外した最後の1回（_append_final_answer）で回答を絞り出してから停止理由を画面に残す。</div>
    <div class="tablewrap"><table class="data"><thead><tr><th style="width:210px">項目</th><th>内容</th></tr></thead><tbody>
      <tr><td>1. 1問が通る経路の全体像</td><td><div class="mt">エンドポイントは2本あるが、前処理と後処理は完全に共通で、違うのはループの中身（逐次 yield するか、最後にまとめて返すか）だけ。</div><pre class="mono small">POST /api/chat/stream   … ブラウザの既定（chat.js の send → sendStreaming）
POST /api/chat/send     … フォールバック（sendStreaming が false を返したときだけ）

  ├ _begin_turn()                        # 共通の前処理。失敗は _TurnError
  │    text 検証 → llm.is_configured()
  │    rag.set_current_user(g.user)      # threading.local
  │    results.new_turn()                # 同一質問内のSQL使い回しの区切り
  │    chat = _load_current()            # session[&#x27;chat_id&#x27;] から読む／無ければ空
  │    images, show = _images_from(...)  # 画像トークン → base64
  │    messages.append(llm.user_message(text, images))
  │    render_log.append({role:&#x27;user&#x27;, kind:&#x27;text&#x27;, ...})
  │    _persist(chat)                    # ★ここで一度保存する（理由は §2）
  │    scope = _auto_scope(text, chat)   # 表ルーターを含む（§3）
  │    if not scope and not rag.rag_available(): raise _TurnError
  │    _realtime_refresh(scope)          # 失敗しても質問は止めない
  │    messages[0] = system(build_system_prompt(scope, admin, model))
  │
  ├ _advance(chat, scope, text)          # /send
  │   または _stream_advance(...)        # /stream（ジェネレータ）
  │
  └ _persist(chat) → chats.save_chat(...)
       /send   … _reply() の中で保存し、新規ぶんの render_log を JSON で返す
       /stream … generate() の finally で保存し、その後 SSE の &#x27;end&#x27; を送る</pre><div class="mt"><code>/api/chat/rewind</code> も同じ部品を使うが <code>_begin_turn</code> は通らず（自前で system と user を積む）、<b>常に非ストリーミング</b>で <code>_advance</code> を呼び、<code>_reply(chat, 0, replace=True)</code> で画面を全部描き直させる。</div></td></tr>
      <tr><td>2. _begin_turn — 順序そのものが仕様</td><td><div class="mt">この関数は「何をするか」より「どの順でやるか」に意味がある。</div><div class="tablewrap"><table class="data"><thead><tr><th>順</th><th>処理</th><th>なぜその位置か</th></tr></thead><tbody><tr><td>1</td><td>text 空チェック / <code>llm.is_configured()</code></td><td>何も始まっていないうちに弾く</td></tr><tr><td>2</td><td><code>rag.set_current_user(g.user)</code></td><td><code>tools.dispatch</code> は利用者を引数に持たない。処理中スレッドの threading.local 経由で渡す</td></tr><tr><td>3</td><td><code>results.new_turn()</code></td><td>「新しい質問だ」と宣言し、前の質問の結果の使い回しを断つ（質問直前にリアルタイム取り込みが走るので、古い数字を返す事故を防ぐ）</td></tr><tr><td>4</td><td>画像の vision 判定</td><td>保存より前。ここで落ちても会話は汚れない</td></tr><tr><td>5</td><td><b>messages/render_log に質問を積んで <code>_persist</code></b></td><td>ルーターのLLM呼び出しやリアルタイム取り込みは数十秒かかることがある。保存が後ろだと、送信直後に別チャットへ切り替えて戻る（<code>/api/chat/open</code> は保存ファイルを読む）と質問が消えて見える</td></tr><tr><td>6</td><td><code>_auto_scope</code></td><td>質問文が要るのでユーザー発言の後</td></tr><tr><td>7</td><td>scope も KB も無ければ <code>_TurnError</code></td><td>この時点で質問は保存済み。コメントも「答えの無い質問が1件残る」と認めている</td></tr><tr><td>8</td><td><code>_realtime_refresh(scope)</code></td><td>例外は握って print だけ。読めなければ前回取り込んだ内容で答える、が決めごと</td></tr><tr><td>9</td><td>system プロンプトを <code>messages[0]</code> に差し替え</td><td>スコープが決まってからでないと組めない。ユーザー発言より後に作るが、置き場所は必ず index 0 なので並びは崩れない</td></tr></tbody></table></div><div class="mt"><code>_load_current()</code> は session の chat_id が無い／読めないとき、黙って <code>{&quot;id&quot;: None, &quot;messages&quot;: [], &quot;render_log&quot;: []}</code> を返す（＝新しい会話が始まる）。</div></td></tr>
      <tr><td>3. _auto_scope と表ルーター</td><td><div class="mt">利用者はサイドバーで表の ON/OFF しか触らない。「AIに何を見せるか」は質問ごとにここが決める。</div><pre class="mono small">scope = build_scope({全DBファイル名: []})     # 全DB・全表
off   = rag.excluded_tables(g.user)           # prefs の tables_off（除外方式）
scope から off を落とす（空になったDBごと消す）

if SCOPE_MODE == &#x27;all&#x27;:          return scope
limit = models.inline_limit_for(models.current(g.user))
if SCOPE_MODE == &#x27;auto&#x27; and catalog.inline_length(scope) &lt;= limit:
    return scope                 # 全部入り＝選び漏れゼロ・プロンプト同一でキャッシュ最大

history = render_log の user/text の content（全部。route_tables 側で末尾3件に絞る）
picked  = llm.route_tables(question, scope, history)
if picked:
    chat[&#x27;table_names&#x27;] のピン留めを足す      # &#x27;DBファイル名.表名&#x27; を rpartition(&#x27;.&#x27;) で割る
    picked = llm.expand_tables_by_relations(picked, scope)   # 関係線で1ホップ補完
    picked から再度 off を落とす              # ピン留めと補完は off を知らないため
    s[&#x27;tables&#x27;] = picked[s[&#x27;name&#x27;]]</pre><div class="mt"><code>route_tables</code>（llm 側）の中身:</div><div class="mt">・表の総数が <b>8以下なら None</b>（絞る意味がないので全部渡す）。<br>・カードは <code>db_text_cached(..., full=False)</code> の要約版。<b>列名は入っていない</b>（説明・行数・業務用語だけで選ばせる）。<br>・呼ぶモデルは常に <code>config.OPENAI_MODEL</code>（裏方用の固定モデル）で、利用者が選んだモデルではない。<code>temperature=0, max_tokens=300</code>。<br>・応答から <code>\[.*?\]</code> を正規表現で1つ取り出して json.loads。<code>[&quot;*&quot;]</code> が入っていたら None。<br>・名前は <code>alias.table</code> と <code>table</code> 単独の両方で引ける対応表を作り、単独名が複数DBで衝突するものだけ落とす（ルーターは形式を崩しがちで、厳格一致だと正解まで捨ててしまうため）。<br>・<b>例外は握って None</b>。ルーターの不調で答えられなくなるのが最悪、という判断。None は「絞らない」＝要約モードへのフォールバック。</div><div class="mt"><code>expand_tables_by_relations</code> は、判定を<b>元の選択のスナップショット <code>base</code></b> に対して行う。育つ集合に対して判定すると1ホップのつもりが連鎖してハブ表経由で雪だるま式に増えるため。方向も <code>from</code>（子）→ <code>to</code>（参照先）の一方向だけ。</div></td></tr>
      <tr><td>4. build_system_prompt — 毎ターン組み直す</td><td><div class="mt">system は保存されない（<code>save_chat</code> が <code>role != &#x27;system&#x27;</code> でフィルタする）。会話を開くたび・質問のたびに最新のカタログで作り直す。構成は次の順:</div><div class="mt">・intro（KBがあるかで文面が変わる）<br>・振る舞い / 可視化の方針 / SQLで書けないこと / ファイル出力<br>・<b>利用可能なツール一覧</b> — <code>tools.build_tools(scope, admin=admin)</code> を実際に呼んで <code>name(引数) : description</code> を並べる。渡していないツールを説明に書くと、AIが呼ぼうとして失敗するだけになるため、宣言と説明の出どころを1本にしてある<br>・<code>kb_note</code>（KBが1件も無ければ節ごと出さない）<br>・<code>stale_note</code> — <code>jobs.problems_by_table()</code> で定期取り込みが失敗している表があれば「回答冒頭に注意書きを添えろ」と指示<br>・SQLルール。<code>naming</code> はDBの数で分岐する。<b>DBが1つのときは「テーブル名はそのまま書く」</b>とだけ言い、DB名をAIに教えない（画面にDBという概念を出していないので、回答にDB名が出ると利用者に通じない）<br>・<code>catalog.prompt_for_scope(scope, limit=inline_cap)</code><br>・現在時刻（<code>datetime.now().isoformat(timespec=&#x27;seconds&#x27;)</code>）</div><div class="mt"><code>inline_cap</code> は <code>models.inline_limit_for(model)</code> = <code>context × 0.5 ÷ 0.55</code> を <code>INLINE_LIMIT_MIN(4,000)</code> と <code>INLINE_LIMIT_MAX(400,000)</code> で丸めた値。<code>prompt_for_scope</code> は全文がこの値以下なら詳細版、超えたら要約版＋「<b>列名は1つも載っていません</b>、無いと判断せず describe_table を呼べ」という長い但し書きを付ける。</div></td></tr>
      <tr><td>5. エージェントループ（_advance）と終了条件</td><td><pre class="mono small">guard = _Guard(); retried_empty = False
for _ in range(config.MAX_AGENT_STEPS):          # 既定10
    msg = llm.chat(messages, tools.build_tools(scope, admin=_is_admin()),
                   model=models.current(g.user))  # ← 毎回作り直す
    messages.append(_msg_to_dict(msg))
    if msg.content: render_log.append(text アイテム)
    calls = _extract_calls(msg)
    if not calls: ...（終了条件1・2）
    fresh = [c for c in calls if not guard.seen(c)]
    render_log.extend(_call_previews(fresh, scope, question))
    _execute(chat, calls, scope, guard)
    if guard.stuck: ...（終了条件3）
...（終了条件4）</pre><div class="tablewrap"><table class="data"><thead><tr><th>#</th><th>条件</th><th>判定</th><th>起きること</th></tr></thead><tbody><tr><td>1</td><td>content あり・tool_calls なし</td><td><code>if not calls</code> かつ content が空白でない</td><td><code>_note_if_cut</code>（finish_reason==&#x27;length&#x27; なら <code>_CUT_MESSAGE</code>）→ return。<b>これが正常な最終回答</b></td></tr><tr><td>2</td><td>content も tool_calls も空</td><td>同上 else</td><td><code>messages.pop()</code> で空の assistant を履歴から消す。1回目は <code>retried_empty=True</code> にして<b>ツール付きのまま再試行</b>（ここで大抵復帰）、2回目は <code>_append_final_answer</code>、それも空なら <code>_EMPTY_MESSAGE</code></td></tr><tr><td>3</td><td>同じ呼び出しの繰り返しが2回</td><td><code>guard.stuck</code>（<code>repeats &gt;= _Guard.LIMIT == 2</code>）</td><td><code>_append_final_answer</code> → <code>guard.stop_reason</code>（<code>_LOOP_MESSAGE</code> or <code>_STUCK_MESSAGE</code>）</td></tr><tr><td>4</td><td>ループが10回終わった</td><td>for が尽きる</td><td><code>_append_final_answer</code> → <code>_LIMIT_MESSAGE</code></td></tr><tr><td>5</td><td><code>llm.chat</code> が例外</td><td>try/except</td><td><code>kind:&#x27;error&#x27;</code> を render_log に積んで return（最終回答なし）</td></tr></tbody></table></div><div class="mt">終了条件2の <code>continue</code> は <b>for のイテレーションを1つ消費する</b>（＝空応答が1回起きると実質9往復になる）。</div><div class="mt"><code>_append_final_answer</code> は <code>messages + [{role:&#x27;user&#x27;, content:&#x27;…ツールは使えません…&#x27;}]</code> を <code>tool_defs=None</code> で投げ、<b>返ってきた assistant だけを messages に append する</b>。注入した user 発言は履歴に残さない。これで内部指示が会話に漏れず、かつ「messages 内の user の個数 = render_log 内の user/text の個数」が保たれる（巻き戻しの前提。§9）。失敗しても print だけして None を返す。</div></td></tr>
      <tr><td>6. _Guard — 同じ呼び出しの見張り</td><td><div class="mt">キーは <code>(name, arguments文字列.strip())</code>。<b>引数JSONの文字列そのまま</b>なので、空白の違うJSONは別の呼び出しになる。</div><div class="mt">・<code>failed: dict[key -&gt; 理由]</code> … 失敗した呼び出し<br>・<code>done: set[key]</code> … <b>成功した呼び出しも覚える</b>。実測で「同じ文書検索を10回・103秒、毎回正解を得ていたのに無回答」があったため、成功も2回目は実行せず差し戻す<br>・<code>repeated(call)</code> が呼ばれるたび <code>repeats += 1</code>。<b>呼び出し単位ではなく総数</b>で、2 に達したら <code>stuck</code><br>・差し戻し文は前回が成功か失敗かで変える。成功なら「結果はもう会話に載っている。それを使って回答を書け」、失敗なら「引数を直せ。直せないなら別の方法に切り替えろ」<br>・<code>stop_reason</code> は <code>done</code> があって <code>failed</code> が空なら <code>_LOOP_MESSAGE</code>（堂々巡り）、それ以外は <code>_STUCK_MESSAGE</code>（失敗の連鎖）</div><div class="mt"><code>_call_previews</code> は <code>fresh</code>（未実行）だけを対象にするので、繰り返された呼び出しはSQLカードが画面に出ない。</div></td></tr>
      <tr><td>7. ツール実行 — _execute → dispatch → _attach_verification</td><td><pre class="mono small">for c in calls:
    if guard.seen(c):
        messages.append({role:&#x27;tool&#x27;, tool_call_id:c[&#x27;id&#x27;], content: guard.repeated(c)})
        continue                       # 実行しない。時間もお金も使わない
    res = tools.dispatch(c[&#x27;name&#x27;], c[&#x27;arguments&#x27;], scope, scope, admin=_is_admin())
    guard.note(c, res)
    content = res[&#x27;llm_content&#x27;]
    alerts  = _fresh_alerts(chat, res.get(&#x27;verify_alerts&#x27;) or [])
    if alerts: content = _merge_alerts(content, alerts)
    messages.append({role:&#x27;tool&#x27;, tool_call_id:c[&#x27;id&#x27;], content: content})
    if res.get(&#x27;render&#x27;): render_log.append(dict(res[&#x27;render&#x27;]))
    for a in alerts: render_log.append(verify.render_item(a))</pre><div class="mt">差し戻す場合も <b>tool メッセージは必ず積む</b>（tool_call_id に応答が無いとAPIが次を受け付けない）。</div><div class="mt"><code>tools.dispatch</code> の順序:</div><div class="mt">・<code>arguments</code> を json.loads（失敗は <code>_err</code>）<br>・<code>name in ADMIN_TOOLS and not admin</code> → 拒否。build_tools でも渡していないが、<b>守りは2箇所で持つ</b><br>・<code>_coerce_lists</code> — 配列で受ける引数に素の文字列が来たら1要素の配列にする（日本語列名が1文字ずつに散る事故を潰す）<br>・<code>_missing_required</code> — 必須なのに来なかった引数を名指しで返す（<code>_HAS_DEFAULT = {title, filename, chart_type, purpose}</code> は除外）<br>・<code>_gather_sqls(args, scope, sqls)</code> — 引数の入れ子を再帰で歩き、<code>sql</code> と <code>result_id</code>（→ 預けたSQL）を全部拾う<br>・<code>_HANDLERS[name]</code> を実行 → <code>_attach_verification(res, sqls, scope)</code>。ハンドラが無ければユーザー定義ツール（<code>_run_custom</code>、SQLは <code>render_sql(tool)</code> を sqls に足す）</div><div class="mt"><code>_attach_verification</code> は <code>res[&#x27;ok&#x27;]</code> かつ SQL があるときだけ <code>verify.alerts_for(sqls, scope)</code> を呼び、不一致だけを <code>res[&#x27;verify_alerts&#x27;]</code> に積む。<b>検証自体の例外で回答は止めない</b>（print して素通り）。</div><div class="mt"><code>_fresh_alerts</code> は render_log 全体の <code>verify_key</code> を見て、この会話で既に見せた警告を捨てる。key には検算のデータ版（<code>res[&#x27;version&#x27;]</code>）が入っているので、データが変われば同じルールでもまた1回だけ出る。<code>_merge_alerts</code> は llm_content が JSON dict なら <code>verification_warnings</code> キーを足し、そうでなければ本文の末尾に <code>【検算の不一致】</code> を連結する。</div></td></tr>
      <tr><td>8. ストリーミング（/api/chat/stream）と SSE</td><td><div class="mt"><code>_sse(event, data)</code> は <code>event: X\ndata: {json}\n\n</code> を作るだけ。イベントは5種類。</div><div class="tablewrap"><table class="data"><thead><tr><th>event</th><th>中身</th><th>出るところ</th></tr></thead><tbody><tr><td><code>delta</code></td><td><code>{text}</code></td><td><code>llm.chat_stream</code> が <code>(&#x27;text&#x27;, 差分)</code> を返すたび</td></tr><tr><td><code>text_end</code></td><td><code>{}</code></td><td>ひとまとまりの本文が終わった時点。<b>tool_calls がある場合も無い場合も出す</b></td></tr><tr><td><code>running</code></td><td><code>{name, label}</code></td><td>1つのツールを実行する直前（<code>TOOL_LABELS</code> の日本語名）</td></tr><tr><td><code>item</code></td><td><code>_web_log</code> した描画アイテム1つ</td><td>プレビュー（SQLカード）・ツールの描画物・検算カード・停止注記・エラー</td></tr><tr><td><code>end</code></td><td><code>{chat_id, title}</code></td><td><code>generate()</code> の finally、<code>_persist</code> の<b>後</b></td></tr></tbody></table></div><div class="mt">ループ本体は <code>_advance</code> と同型だが、実行が<b>1呼び出しずつ</b>になる（<code>running</code> を出してから <code>_execute(chat, [c], ...)</code>、直後に <code>_web_log(render_log, before)</code> で新規ぶんだけ item にする）。</div><div class="mt">エンドポイント側の段取りにも理由がある:</div><div class="mt">・<code>chat[&#x27;id&#x27;]</code> をここで確定して <code>session[&#x27;chat_id&#x27;]</code> に入れる。<b>応答を流し始めるとセッションに書けない</b>（Cookie が出せない）ので、後から入れても消える<br>・<code>turn_id = results.current_turn()</code> をリクエストスレッドで捕まえ、<code>generate()</code> の中で <code>rag.set_current_user(user)</code> と <code>results.set_turn(turn_id)</code> を<b>やり直す</b>。この2つは threading.local で、<code>stream_with_context</code> が引き継ぐのは Flask の g / session だけ<br>・<code>GeneratorExit</code>（画面を閉じた・更新した）は <code>aborted=True</code> にして再送出。finally で <code>_persist</code> はするが <code>end</code> は送らない（切断後に yield すると RuntimeError になるだけ）<br>・レスポンスヘッダに <code>X-Accel-Buffering: no</code>（nginx のバッファ抑止）</div><div class="mt">クライアント側（chat.js <code>sendStreaming</code>）は <code>EventSource</code> が POST を使えないので <code>fetch</code> + <code>ReadableStream</code> を自前でパースする。<code>false</code> を返す＝フォールバックするのは <b>fetch が投げたときと <code>!res.ok || !res.body</code> のときだけ</b>。途中で切れた場合は <code>true</code> を返すので <code>/api/chat/send</code> への再送は起きない。</div></td></tr>
      <tr><td>9. messages と render_log がなぜ2本あるか</td><td><div class="tablewrap"><table class="data"><thead><tr><th></th><th>messages</th><th>render_log</th></tr></thead><tbody><tr><td>用途</td><td>次のターンでAPIに送る会話</td><td>画面の描画・保存・監査</td></tr><tr><td>要素</td><td><code>{role: system/user/assistant/tool, content, tool_calls?, tool_call_id?}</code></td><td><code>{role, kind, at, …kind別}</code></td></tr><tr><td>保存</td><td>system は除いて保存</td><td>全部保存（bytes は base64 に符号化）</td></tr><tr><td>情報量</td><td>ツール結果は先頭40行（<code>SAMPLE_ROWS_FOR_LLM</code>）のサマリJSON</td><td>表は全行、グラフの元データ、ファイルの実体</td></tr></tbody></table></div><div class="mt">分けている理由は3つあり、どれも一方だけでは成立しない。</div><div class="mt">・<b>粒度が逆</b>。LLMには全行を渡さない（トークン）が、画面には全行を出す。逆にSQLカードの <code>explanation</code> や検算カードは画面のためのもので、messages には別形式で入る。<br>・<b>バイト列</b>。Excel/CSV/画像は JSON に載らない。<code>_encode_item</code> が <code>CHAT_EMBED_FILE_MAX_BYTES</code>(2MB) までは base64、超えるものは <code>_no_data: True</code> にして本体を捨てる。messages 側にファイル名しか入らないのはこのため。<br>・<b>system を保存しない</b>。カタログが育ったら過去の会話も新しい定義で続けたいので、<code>save_chat</code> が system を落とし、開くたびに <code>build_system_prompt</code> で作り直す。</div><div class="mt">副産物として render_log は<b>監査ログ</b>になっている。<code>usage.collect</code> は render_log の <code>kind</code> を数えて sql/chart/table/file/report の件数を出し、<code>_asked</code> は user/text の <code>at</code> と次の応答の <code>at</code> の差で「その質問に何秒待たされたか」を出す。<code>verify.collect_sqls</code> は render_log の SQL と messages の tool_calls 引数の両方から実行SQLを集め、会話単位で重複を除く。</div><div class="mt">2本をつなぐ唯一の目盛りが<b>ユーザー発言の通し番号</b>。<code>_count_turns</code> は render_log の <code>role==&#x27;user&#x27; and kind==&#x27;text&#x27;</code> を数え、<code>_web_log</code> がそれを <code>turn</code> として各吹き出しに振る。<code>_split_at_turn</code> は同じ番号で messages 側（<code>role==&#x27;user&#x27;</code> の n 個目）と render_log 側を切る。</div></td></tr>
      <tr><td>10. 保存・_web_log・巻き戻し</td><td><div class="mt"><b><code>_persist(chat)</code></b></div><div class="mt">・render_log が空で id も無ければ何もしない（新しい会話は話すまでファイルを作らない）。既にある会話は空でも保存する（巻き戻しで全部消したとき、古いやり取りが復活しないように）<br>・<code>db_names</code> = render_log の SQL から <code>db.dbs_named_in</code> で集めたDB名の累積<br>・<code>table_names</code> = 各DBのプロファイルの表名を <code>(?&lt;!\w)表名(?!\w)</code> で SQL に当てて拾った <code>&quot;DBファイル名.表名&quot;</code> の累積。これが次の質問で表ルーターのピン留めになる</div><div class="mt"><b><code>_web_log(render_log, start)</code></b> は保存形式 → ブラウザ形式。3つ副作用がある。</div><div class="mt">・user/text に <code>turn</code> を振る（<code>start</code> より前を数えてから続きを振る）<br>・<code>item[&#x27;data&#x27;]</code>（bytes）を持つアイテムは <code>_fs_put</code> で<b>新しいダウンロードトークンを発行</b>して <code>url</code> に差し替える。呼ぶたび別トークンになり、置き場はプロセス内メモリ200件・所有者一致でしか読めない<br>・<code>kind==&#x27;sql&#x27;</code> に <code>TOOL_LABELS</code> の日本語ラベルを付ける</div><div class="mt"><b><code>/api/chat/rewind</code></b></div><div class="mt">・<code>turn</code> 必須、<code>text</code> は任意。<code>_split_at_turn</code> が messages と render_log を同じ位置で切る（どちらかで見つからなければ ValueError → 400）<br>・<code>text</code> が空なら切るだけ（<code>restored</code> に元の文面を返して入力欄に戻す）<br>・<code>text</code> があれば <code>_auto_scope</code> → <code>_realtime_refresh</code> → system を入れ直し → user を積んで <code>_advance</code>。送信と同じ規則で「scope も KB も無ければ 400」<br>・応答は必ず <code>replace=True</code>（画面を全部描き直す）</div></td></tr>
      <tr><td>11. LLM呼び出し層（llm.chat / chat_stream / _create）</td><td><div class="mt"><code>chat()</code> と <code>chat_stream()</code> は同じ kwargs を組む: <code>model</code>（既定 <code>config.OPENAI_MODEL</code>）、<code>messages</code>、<code>tools</code>、<code>tool_choice=&#x27;auto&#x27;</code>、<code>temperature=config.OPENAI_TEMPERATURE</code>（既定0）、任意で <code>top_p</code> / <code>max_tokens</code>。<code>chat_stream</code> は <code>stream=True</code> を足す。</div><div class="mt">両者とも <code>_create(**kwargs)</code> を通る。<code>_create</code> は2種類の再試行を持つ。</div><div class="mt">・<b>引数の作法学習</b>: 400 のエラー文を <code>_fix_for</code> で読み、<code>reasoning_effort</code> を <code>none</code> にする／落とす、<code>temperature</code>・<code>top_p</code> を落とす、<code>max_tokens</code> → <code>max_completion_tokens</code> に置き換える、を試して <code>_QUIRKS[model]</code> に覚える。1回の呼び出しで最大 <code>_MAX_FIX = 4</code> 回。400 は推論前に弾かれるので費用はかからない。覚えた内容はプロセスの寿命だけ<br>・<b>レート制限(429)</b>: <code>retry-after</code> ヘッダ → エラー文の <code>try again in X</code>（+0.5秒） → <code>2^n</code> 秒 の順で待ち時間を決め、<code>LLM_RATE_LIMIT_MAX_WAIT</code>(20秒) で頭打ち。<code>LLM_RATE_LIMIT_RETRIES</code>(3) 回で諦めて <code>RateLimited</code> を投げる</div><div class="mt"><code>chat()</code> は <code>msg.finish_reason = resp.choices[0].finish_reason</code> を<b>SDKのオブジェクトに後付け</b>する（<code>_note_if_cut</code> が <code>&#x27;length&#x27;</code> を見るため）。属性を拒まれても本体の動作は変えない。</div><div class="mt"><code>chat_stream()</code> は <code>StreamedMessage</code> を組み立てる。tool_calls は複数チャンクに分かれて届くので <code>delta.tool_calls[].index</code> で束ね、<code>name</code> も <code>arguments</code> も<b>文字列連結</b>する。最後に <code>(&#x27;done&#x27;, out)</code> を1回だけ yield する。</div><div class="mt">呼び出し側の <code>_friendly_llm_error</code> が例外文を言い換える（<code>error parsing tool call</code> / <code>out of memory</code> / <code>timeout</code> の3種を特別扱いし、それ以外は先頭160文字だけ添える）。</div></td></tr>
      <tr><td>12. 本日入った変更が経路のどこに触るか</td><td><div class="mt">・<b>SQLの日本語解説</b>: <code>tools.build_tools</code> が <code>name in SQL_TOOLS</code> のツール宣言に <code>_with_explanation</code> で <code>explanation</code> 引数を注入する（<b>required には足さない</b> — 解説を書き損ねただけで質問が止まるのを避けるため）。<code>_call_previews</code> が <code>args.get(&#x27;explanation&#x27;)</code> を <code>kind:&#x27;sql&#x27;</code> アイテムに載せ、chat.js が SQL の下に「このSQLがしていること」として出す。ユーザー定義ツールの場合だけは AI の解説ではなく<b>登録時の description</b> を使う。<br>・<code>drop_table</code> の <code>sqlite_master</code> 判定・まとまりメモの点検 / drift_warnings / dirty 管理は、この経路（質問処理）には直接入ってこない。効くとすれば <code>build_system_prompt</code> が載せるカタログ本文の中身が変わる点だけ。</div></td></tr>
      <tr><td>主なデータ構造</td><td>・scope = [{path: str, alias: str, name: &#x27;DBファイル名.db&#x27;, tables: [表名], meta: {...meta.yaml...}}]（build_scope が生成。tables は選択後の表だけ）<br>・messages = [{role: &#x27;system&#x27;|&#x27;user&#x27;|&#x27;assistant&#x27;|&#x27;tool&#x27;, content: str|[part], tool_calls?: [{id, type:&#x27;function&#x27;, function:{name, arguments}}], tool_call_id?: str}]<br>・render_log アイテム = {role: &#x27;user&#x27;|&#x27;assistant&#x27;, kind: ..., at: ISO秒, ...kind別}。kind は text / sql / table / chart / chart_dual / report / report_doc / file / error / mail_draft / glossary_term / example_proposal / er / table_link / sources<br>・kind:&#x27;sql&#x27; = {tool, sql, purpose, explanation, question, tables: [{db, table}]}（tables は tables_in_sql が最大6件。画面ではカタログへのリンクになる）<br>・calls = [{id, name, arguments}]（_extract_calls。arguments は未パースのJSON文字列のまま _Guard のキーに使う）<br>・tools.dispatch の戻り = {ok: bool, llm_content: str(JSON), render: dict|None, verify_alerts?: [alert]}<br>・verify alert = {key: &#x27;verify||owner||name||指紋||データ版&#x27;, name, left_label, left, right_label, right, diff, pct, tolerance_pct, drill}<br>・results のエントリ = {scope: scope_key, columns, rows, truncated, sql, norm_sql, turn, label}（result_id で他ツールへ引き渡す）<br>・SSE 1件 = &#x27;event: &lt;delta|text_end|running|item|end&gt;\ndata: &lt;JSON&gt;\n\n&#x27;<br>・保存形式（chats/&lt;ID&gt;.json） = {id, title, created_at, updated_at, db_names, table_names, tables, messages(systemを除く), render_log(_encode_item済み)}</td></tr>
      <tr><td>定数・しきい値</td><td>・config.MAX_AGENT_STEPS = 10（env で変更可）… 1質問あたりの LLM 往復上限。空応答の再試行も1回ぶん消費する<br>・_Guard.LIMIT = 2 … 同じ呼び出しの差し戻しが通算2回で打ち切り（呼び出し単位ではなく総数）<br>・config.OPENAI_TEMPERATURE = 0 / OPENAI_MODEL = &#x27;gpt-5.6-sol&#x27;（ルーターと下書きは常にこの固定モデル）<br>・config.SCOPE_MODE = &#x27;auto&#x27;（auto / router / all）… auto は「収まるなら全部入り、超えたらルーター」<br>・route_tables: 表の総数 8以下ならルーターを呼ばない。会話履歴は末尾3件、temperature=0, max_tokens=300<br>・models.INLINE_LIMIT_MIN = 4,000 / INLINE_LIMIT_MAX = 400,000 文字、CATALOG_CONTEXT_RATIO = 0.5、llm.TOKENS_PER_CHAR_TEXT = 0.55（ツール定義JSONは 0.31）<br>・config.SAMPLE_ROWS_FOR_LLM = 40 … LLM に返す行数。MAX_RESULT_ROWS = 2,000（画面・result_id の預かり）、EXPORT_MAX_ROWS = 1,000,000（ファイル出力）<br>・config.IMAGE_MAX_COUNT = 4 / IMAGE_MAX_MB = 8、llm.IMAGE_MIMES = png/jpeg/gif/webp<br>・llm._MAX_FIX = 4（引数の作法を直す回数）、config.LLM_RATE_LIMIT_RETRIES = 3、LLM_RATE_LIMIT_MAX_WAIT = 20秒<br>・config.CHAT_EMBED_FILE_MAX_BYTES = 2MB … これを超えるファイルは会話に本体を保存しない（_no_data）<br>・filestore _MAX_ITEMS = 200（ダウンロードトークンの保持数、プロセス内メモリ）<br>・results.MAX_ENTRIES = 40 / MAX_CELLS = 400,000（result_id の置き場。古い順に捨てる）<br>・config.CHAT_HISTORY_LIMIT = 100本 / CHAT_HISTORY_DAYS = 90日<br>・_attachments_for: &#x27;all&#x27; 指定時は直近5件（made[-5:]）、tables_in_sql の上限は6表</td></tr>
    </tbody></table></div>
    <div class="card__title mt">落とし穴（21件）</div>
    <div class="tablewrap"><table class="data"><thead><tr><th style="width:60px">#</th><th>内容</th></tr></thead><tbody>
      <tr><td class="mono small">01</td><td>_begin_turn は _auto_scope より前に質問を保存する。そのため「いま調べられるものがありません」の _TurnError だけは<b>質問が保存済みの状態で</b>返る。さらにブラウザは /stream が 400 を返すと sendStreaming が false を返して /send にフォールバックし、そこで _begin_turn がもう一度走るので、<b>同じ質問が会話に2回積まれて2回保存される</b>。</td></tr>
      <tr><td class="mono small">02</td><td>_append_final_answer は「回答を書け」という user メッセージを LLM には送るが messages には append しない（返ってきた assistant だけ積む）。これが無いと messages 側の user 個数と render_log 側の user/text 個数がずれ、_split_at_turn（巻き戻し）が別の位置で切ってしまう。</td></tr>
      <tr><td class="mono small">03</td><td>_Guard は失敗だけでなく<b>成功した呼び出しも覚える</b>。正しい結果が返っていても2回目は実行せず「もう答えを書け」と差し戻す。実測で「同じ文書検索を10回・103秒、毎回正解を得ていたのに無回答」が起きたための措置。</td></tr>
      <tr><td class="mono small">04</td><td>空の最終回答は messages.pop() で履歴から取り除く。取り除かないと空の assistant 発言が残り、次の質問でも真似されて<b>そのチャットがずっと無言になる</b>。</td></tr>
      <tr><td class="mono small">05</td><td>_stream_advance の <code>if msg is None: return</code> は、chat_stream が (&#x27;done&#x27;, …) を返さなかった場合の逃げ道。停止注記もエラーも出さずに黙って終わる（finally の _persist と &#x27;end&#x27; だけ走る）。</td></tr>
      <tr><td class="mono small">06</td><td>_web_log は純関数ではない。bytes を持つアイテムを渡すたび _fs_put で<b>新しいダウンロードトークンを発行する</b>。同じファイルを再描画すると別URLになり、古いトークンは200件のLRUから押し出されて404になりうる。</td></tr>
      <tr><td class="mono small">07</td><td>threading.local に置いているのは rag のカレントユーザーと results のターンIDの2つだけ。stream_with_context が引き継ぐのは Flask の g / session なので、generate() の冒頭で set_current_user / set_turn を<b>やり直さないと</b>同じSQLを2回実行してしまう。</td></tr>
      <tr><td class="mono small">08</td><td>/stream は本文を流す前に chat[&#x27;id&#x27;] を確定して session に入れる。流し始めるとセッションCookieを出せないため、後から入れても消えて次の質問が別会話になる。</td></tr>
      <tr><td class="mono small">09</td><td>tools.dispatch(name, args, scope, scope, admin=...) の第4引数 entries には scope をそのまま渡している（ユーザー定義ツールの探索範囲＝同じスコープ）。</td></tr>
      <tr><td class="mono small">10</td><td>_Guard.key は arguments の<b>生の文字列</b>。意味的に同じでも空白や順序が違うJSONは別の呼び出しと見なされ、差し戻しが効かない。</td></tr>
      <tr><td class="mono small">11</td><td>_call_previews は fresh（未実行）の呼び出しだけを描く。繰り返された呼び出しは画面にSQLカードが出ないので、ログだけ見ると「実行されていない」ように見える。</td></tr>
      <tr><td class="mono small">12</td><td>ストリーミングでは assistant の本文が delta として流れ、同じ内容が render_log にも text アイテムとして積まれるが、item イベントとしては送られない。ライブ表示と再読み込み後の表示が一致するのはこのため（片方でも送ると二重に出る）。</td></tr>
      <tr><td class="mono small">13</td><td>build_tools と models.current はループの<b>毎イテレーション</b>で呼ばれる。1往復ごとに prefs の YAML 読み込み・custom_tools.collect_everywhere・knowledge_tool_schemas が走る。</td></tr>
      <tr><td class="mono small">14</td><td>route_tables が使うカードは full=False の要約版で<b>列名が入っていない</b>。表の選択は説明文・行数・業務用語だけで行われるので、カタログの説明が薄い表はルーターに拾われにくい。</td></tr>
      <tr><td class="mono small">15</td><td>expand_tables_by_relations は base（元の選択のスナップショット）に対してだけ判定する。out に対して判定すると1ホップのつもりが連鎖し、設備マスタのようなハブ表経由でDBの大半が付いてくる。方向も 子(from)→親(to) の一方向のみ。</td></tr>
      <tr><td class="mono small">16</td><td>サイドバーで外した表（prefs の tables_off）は _auto_scope の入口と、ピン留め・関係補完の<b>後</b>の2回落としている。1回目だけだと会話の続きで除外したはずの表が戻ってくる。</td></tr>
      <tr><td class="mono small">17</td><td>_persist の table_names 収集は <code>(?&lt;!\w)表名(?!\w)</code> の正規表現でSQL本文に当てているだけ。列名や文字列リテラルと同名の表があれば誤って拾う（逆にこの \w が無いと日本語表名がまったく当たらない）。</td></tr>
      <tr><td class="mono small">18</td><td>llm.chat は SDK のメッセージオブジェクトに finish_reason を<b>後付けで代入</b>している。SDK側が拒めば黙って None のままになり、出力上限で切れても _CUT_MESSAGE が出ない。</td></tr>
      <tr><td class="mono small">19</td><td>検算の重複抑止（_fresh_alerts）は verify_key を render_log 全体から集める。key にデータ版が入っているので、データが更新されると同じルールの警告がもう一度だけ出る。</td></tr>
      <tr><td class="mono small">20</td><td>_execute は差し戻し時も tool ロールのメッセージを必ず積む。tool_call_id に対応する応答が無いと次の API 呼び出しが通らないため、「実行しない」と「応答しない」は別物として扱っている。</td></tr>
      <tr><td class="mono small">21</td><td>explanation 引数は SQL_TOOLS のツール宣言にだけ注入され、画面に出るのは <code>_call_previews</code> が <code>&#x27;sql&#x27; in args</code> を満たしたときだけ。result_id だけで前の結果を使い回す呼び出しはSQLカード自体が出ないので、解説も表示されない。</td></tr>
    </tbody></table></div>
  </div>

  <div class="card mt">
    <div class="card__title" id="impl-prompt">5-2. システムプロンプトの組み立て</div>
    <div class="card__desc">質問1回ごとに、選択スコープのデータカタログをテキストへ直列化し、振る舞い規則・ツール一覧・SQLルールと合わせて1本の system メッセージへ組み上げる部分。中核は <code>build_system_prompt</code>（llm 相当）と、その中で呼ばれる <code>catalog.prompt_for_scope</code> → <code>db_text_cached</code> → <code>db_text</code> → <code>table_text</code> の連鎖。カタログが選択中モデルの読める量を超えたときは、上流（<code>_auto_scope</code> の表ルーター）で表を絞り、それでも溢れたら <code>prompt_for_scope</code> が「表の1行要約だけ・列名なし」の要約モードへ落とし、詳細は <code>describe_table</code> ツールで取りに行かせる。文字数→トークンの換算は実測係数（日本語 0.55／JSON 0.31 トークン/字）による概算で、モデル差は文脈量テーブル＋管理者上書き＋呼び出し引数の学習（<code>_QUIRKS</code>）で吸収する。</div>
    <div class="tablewrap"><table class="data"><thead><tr><th style="width:210px">項目</th><th>内容</th></tr></thead><tbody>
      <tr><td>全体像 — いつ・どこで組まれ、どこに置かれるか</td><td><div class="mt">system プロンプトは会話に1本だけ持ち、<b>毎ターン丸ごと作り直して <code>chat[&quot;messages&quot;][0]</code> を差し替える</b>。組み立てる場所は2か所だけ。</div><div class="tablewrap"><table class="data"><thead><tr><th>呼び出し元</th><th>契機</th></tr></thead><tbody><tr><td><code>_begin_turn</code>（<code>/api/chat/send</code> と <code>/api/chat/stream</code> の共通前処理）</td><td>通常の質問</td></tr><tr><td>巻き戻し・書き直しのエンドポイント</td><td>途中のターンをやり直すとき</td></tr></tbody></table></div><div class="mt">どちらも同じ引数で呼ぶ：</div><pre class="mono small">llm.build_system_prompt(scope, admin=_is_admin(), model=models.current(g.user))</pre><div class="mt">順序が重要な点が2つある。</div><div class="mt">・<b>ユーザー発言を保存してからスコープを決める。</b> <code>_begin_turn</code> は <code>chat[&quot;messages&quot;].append(user_message(...))</code> と <code>_persist(chat)</code> を先に済ませてから <code>_auto_scope</code> を呼ぶ。表ルーターのLLM呼び出しがローカルLLMだと数十秒かかり、その間に別チャットへ切り替えて戻ると質問が消えて見えるため（コメントに明記）。<br>・<b>system は後から index 0 に差し込む。</b> すでに先頭が system でなければ <code>insert(0, ...)</code> してから上書きするので、発言の並び順は崩れない。</div><div class="mt">ツール定義（<code>tools.build_tools(scope, admin=...)</code>）は system と違い、<code>_advance</code> / <code>_stream_advance</code> の<b>エージェントループの毎ステップで作り直される</b>。system は1ターンに1回。</div><div class="mt">このほか、カタログ直列化そのものは AI下書き系でも使われる（<code>draft_view</code> / <code>draft_tool</code> が <code>catalog.prompt_for_scope(...)</code> を limit 無しで呼び、専用の system 文と組み合わせる）。こちらは <code>build_system_prompt</code> を通らない。</div></td></tr>
      <tr><td>build_system_prompt の構成要素と順序</td><td><div class="mt">戻り値は1本のf文字列。ブロックの並びは固定で、次のとおり。</div><div class="tablewrap"><table class="data"><thead><tr><th>#</th><th>ブロック</th><th>出所・条件</th></tr></thead><tbody><tr><td>1</td><td><code>intro</code>（1〜2行）</td><td><code>rag_targets()</code> が空でなければ「社内の業務アシスタント…ナレッジベースも検索できます」、空なら「SQLiteデータベースの分析アシスタント」</td></tr><tr><td>2</td><td><code># 振る舞い</code></td><td>固定文。実データ厳守・不確かなら <code>describe_table</code>・業務用語優先・カタログ育成の提案（用語/例文）・<code>verification_warnings</code> の扱い</td></tr><tr><td>3</td><td><code># 可視化の方針（チャットにグラフを描く）</code></td><td>固定文。目的別の <code>plot_*</code> 選択、<code>result_id</code> の使い回し</td></tr><tr><td>4</td><td><code># SQLで書けないこと（必ず専用ツールを使う）</code></td><td>固定文。STDDEV/MEDIAN/CORR/PIVOT が無いので <code>pivot_table</code> / <code>analyze_stats</code> へ誘導</td></tr><tr><td>5</td><td><code># ファイル出力</code></td><td>固定文。<code>export_excel</code> / <code>export_csv</code> / <code>export_text</code>、表が無くても <code>rows</code> で出せること</td></tr><tr><td>6</td><td><code># 利用可能なツール</code> + <code>tool_list</code></td><td><code>tools.build_tools(scope, admin)</code> の結果を <code>- name(引数名, ...) : description</code> に整形。末尾に、ユーザー定義ツールがあれば「※ 上記のうち次はこの環境専用…」の1行</td></tr><tr><td>7</td><td><code>kb_note</code></td><td>ナレッジベースが1件以上のときだけ。<code># 社内文書（ナレッジベース）</code> 節＋KB名/説明の一覧＋出典番号の作法</td></tr><tr><td>8</td><td><code>stale_note</code></td><td><code>jobs.problems_by_table()</code> に該当があるときだけ。<code># 状態に問題があるデータ（重要）</code></td></tr><tr><td>9</td><td><code># SQLルール</code></td><td>固定文＋<code>naming</code> を1行差し込む</td></tr><tr><td>10</td><td><code># 選択中のデータカタログ</code></td><td><code>catalog.prompt_for_scope(scope, limit=inline_cap)</code> の戻り値まるごと</td></tr><tr><td>11</td><td><code>現在時刻: &lt;ISO8601 秒精度&gt;</code></td><td><code>datetime.now().isoformat(timespec=&quot;seconds&quot;)</code></td></tr></tbody></table></div><div class="mt"><b>inline_cap の決定</b>（関数の冒頭）</div><pre class="mono small">inline_cap = None
if model:
    import models as models_mod   # 循環import回避のため関数内import
    inline_cap = models_mod.inline_limit_for(model)</pre><div class="mt"><code>model</code> を渡さない呼び出しでは <code>None</code> のまま <code>prompt_for_scope</code> に入り、そちらの既定（<code>catalog.inline_limit()</code> = 400,000字）が使われる。</div><div class="mt"><b><code>naming</code> の4分岐</b>（<code>aliases = [s[&quot;alias&quot;] for s in scope]</code>）</div><div class="mt">・2件以上 … 「複数のDBが対象です（…）。テーブル名は必ず『エイリアス.テーブル名』で修飾すること」<br>・1件 … 「テーブル名はそのまま書く（前に何かを付けて修飾しない）」。<b>DB名をAIに教えない</b>のが明示的な設計判断で、画面にDBという概念を出していないため、回答やSQLにDB名が出ると利用者に意味が通じなくなる<br>・0件かつKBあり … 「いま対象にできるデータがありません…ナレッジベースの検索で答えられる範囲で」<br>・0件かつKBなし … 「対象にできるDBがありません。『データ取り込み』でDBを作るよう案内すること」</div><div class="mt"><b><code>stale_note</code> の作り方</b></div><div class="mt"><code>jobs.problems_by_table()</code> は <code>{(db_file, table): [problem,...]}</code>。<code>in_scope = {s[&quot;name&quot;] for s in scope}</code>（＝DBファイル名の集合）に db_file が入っているものだけを拾い、<code>- {alias}.{table}: {message}（{since} 以降）</code> の行にする。文面は「古い」と断定せず、<code>degraded</code>（数値列が文字で保存された）の可能性も併記させる — データは新しいのに集計の方が信用できない場合があるため。</div><div class="mt"><b>tool_list と explanation 引数</b></div><div class="mt"><code>build_tools</code> は <code>SQL_TOOLS</code>（<code>run_sql_query</code> / <code>pivot_table</code> / <code>analyze_stats</code> / 各 <code>plot_*</code> / <code>compare_periods</code> 系 / <code>hypothesis_test</code> 系）に <code>_with_explanation</code> を通し、<code>explanation</code>（日本語解説3〜5行）プロパティを注入する。<code>required</code> には<b>足さない</b>（解説を書き損ねただけで質問全体が止まるのを避けるため）。system プロンプト側にはこの引数の説明文は書かれず、<code>tool_list</code> の行に引数名として <code>explanation</code> が並ぶだけ。書き方の指示は <code>_EXPLANATION_PARAM[&quot;description&quot;]</code>（＝tools 配列側）にある。</div></td></tr>
      <tr><td>catalog.db_text — 1DB分のカタログ本文</td><td><div class="mt"><code>db_text(alias, db_path, tables, full)</code> は <code>profile_db()</code>（自動プロファイル）と <code>load_meta()</code>（人が書いた .meta.yaml）を合成して1本のテキストにする。出力の並びは固定。</div><pre class="mono small">names   = tables or 全表名          # tables が None でも [] でも全表になる
shown   = set(names)
limited = tables is not None and len(shown) &lt; len(profile[&quot;tables&quot;])</pre><div class="mt">・<code>## 使えるデータ</code><br>・<b><code>limited</code> のときだけ</b>「※ 利用者がいま対象にしているのは、下に挙げる表だけです。ここに無いデータは存在しないものとして答えてください。…」。絞っていることを明示しないと、AIが知識で知っている他データの話を始めて最後に「使えません」と言う、という実害への対処<br>・<b>兄弟まとまりの自動注記</b>（<code>_sibling_groups</code> の各ファミリに1行、後述）<br>・<b>まとまりメモ</b> … <code>by_group</code> に出てくる接頭辞を名前順に回し、<code>db_groups(meta)[g][&quot;description&quot;]</code> が空でなければ <code>【まとまり名】\nメモ本文</code><br>・空行<br>・表カード本体<br>・<code>full=True</code> … 各表の <code>table_text(..., full=True)</code> を1枚ずつ、間に空行<br>・<code>full=False</code> … <code>テーブル一覧:</code> の見出しの下に <code>table_text(..., full=False)</code> を1行ずつ<br>・<code>結合キー（JOINにはこれを使う）:</code> … FK宣言行 → メタの <code>relationships</code> の順。<code>rels</code> も <code>fk_lines</code> もどちらも空なら見出しごと出さない<br>・<code>テーブルをまたぐ業務用語（質問にこの言葉が出たら必ずこの定義に従う）:</code> … <code>db_glossary(meta)</code> を <code>glossary_lines</code> で整形<br>・<code>正しいと確認済みの質問とSQLの例:</code> … <code>Q:</code> / （あれば）<code>補足:</code> / <code>SQL:</code> の3行を例文の数だけ</div><div class="mt"><b>結合キーの複合キー対応</b></div><div class="mt"><code>rel_pairs(r, &quot;&quot;)</code> が列ペアを2つ以上返した関連は、条件を AND でつないだ形に展開する。</div><pre class="mono small">- 受注.部門 = 部門M.部門 AND 受注.年度 = 部門M.年度 (N:1) ※複合キー: 2列すべてを同時に結合条件へ。片方の列だけで結ばない</pre><div class="mt">単一列（またはペアが解けない場合）は保存されている文字列をそのまま <code>- from = to (多重度)</code> で出す。</div><div class="mt"><b>limited のときの漏れ止め</b></div><div class="mt">表を絞ったときは、関連・用語・例文も「表示中の表しか触れていないもの」に間引く。ここを素通しにすると、載せていない表の名前が例文のSQLから漏れ、AIが「あるはず」と判断してその表を読みに行ってしまうため。判定は2つの内部関数で、どちらも <code>(?&lt;![\w.])表名(?![\w])</code> の正規表現で本文を走査する。</div><div class="tablewrap"><table class="data"><thead><tr><th>関数</th><th>真になる条件</th><th>適用先</th></tr></thead><tbody><tr><td><code>_mentions_only_shown(text)</code></td><td>表名が1つ以上ヒットし、<b>すべて</b> shown に入る</td><td><code>relationships</code> の from/to、例文の <code>sql</code>、用語の <code>sql</code></td></tr><tr><td><code>_no_hidden_tables(text)</code></td><td>ヒットした表がすべて shown（<b>1つもヒットしなければ True</b>）</td><td>用語の <code>description</code></td></tr></tbody></table></div><div class="mt">まとまりメモと兄弟まとまり注記には、この間引きが<b>かかっていない</b>。</div></td></tr>
      <tr><td>table_text — 表カード1枚の中身</td><td><div class="mt"><code>table_text(alias, tname, profile, meta, full)</code>。プロファイルに無い表は <code>- {tname} : (プロファイル未取得)</code> の1行で返る。</div><div class="mt"><b>表名にDB名（エイリアス）を付けない。</b> docstring に理由がある — DBは常に1つで、AIにその名前を教えると回答やSQLにまでDB名が出てきて、画面にDB概念を出していない利用者には意味不明になる。引数 <code>alias</code> は受け取るが本文には使わない。</div><div class="mt"><b>full=False（1行要約）</b></div><pre class="mono small">- 受注明細（12,345行） : 受注の明細行。1行=1商品 / 業務用語: 有効な受注, 実売上</pre><div class="mt">・見出しは <code>{表名}（{行数:,}行）</code>、行数が取れていなければ <code>行数不明</code><br>・説明があれば <code> : </code> に続けて。<code>tmeta[&quot;ai_draft&quot;]</code> が真なら末尾に <code>（AI推測・未確認）</code><br>・業務用語は<b>名前だけ</b>を列挙する。定義は載せず、必要なら <code>describe_table</code> で取りに行かせる</div><div class="mt"><b>full=True（詳細カード）</b></div><pre class="mono small">### 受注明細（12,345行）
受注の明細行。1行=1商品
主キー（人が指定）: (受注番号, 行番号) の複合キー → この組み合わせで1行が一意。結合するときは2列すべてを条件にする。
列:
- 受注番号 TEXT PK : 受注のID / 値: A001(3), A002(2), ...
- 状態 INTEGER : 進捗 / 値: 1=受付(120), 2=出荷済(300), NULL(4)
- 金額 REAL / 範囲: 100 〜 980000
サンプル行 [&#x27;受注番号&#x27;, &#x27;行番号&#x27;, ...]:
  [&#x27;A001&#x27;, 1, ...]
受注明細 の業務用語（質問にこの言葉が出たら必ずこの定義に従う）:
- 有効な受注: キャンセル以外
    SQL式: 状態 &lt;&gt; 9   ← この式をそのまま使う</pre><div class="mt">主キー行は <code>effective_pk(profile, meta, tname)</code> の結果で3通りに分岐する。</div><div class="tablewrap"><table class="data"><thead><tr><th>pk_src / 列数</th><th>出力</th></tr></thead><tbody><tr><td>2列以上</td><td><code>主キー{note}: (c1, c2) の複合キー → この組み合わせで1行が一意。結合するときは2列すべてを条件にする。</code></td></tr><tr><td>1列</td><td><code>主キー{note}: c1</code></td></tr><tr><td>0列</td><td><code>主キー: なし（宣言が無く、指定もされていない）。重複行があり得るので COUNT(DISTINCT ...) の要否に注意する。</code></td></tr></tbody></table></div><div class="mt"><code>note</code> は <code>override</code> のとき <code>（人が指定）</code>、<code>declared</code> / <code>none</code> のときは空文字。複合キーを構成順で明示するのは、主キーが「1行が何を表すか（粒度）」の手がかりだから。</div><div class="mt">列行のパーツ組み立て順は <code>名前 型</code> → <code>PK</code> → <code>: 説明</code> → 値情報。値情報は<b>排他の3択</b>で、上から順に最初に当たったものだけ。</div><div class="mt">・<code>col_stats[列][&quot;values&quot;]</code> があれば <code>/ 値: </code> + <code>_fmt_value_list</code>（<code>値=ラベル(件数)</code> 形式、メタの <code>values</code> 辞書でラベル補完、None は <code>NULL</code>）<br>・無くてメタに <code>values</code> があれば <code>/ コード値: k=v, k=v</code><br>・無くて <code>col_stats[列][&quot;min&quot;]</code> があれば <code>/ 範囲: min 〜 max</code></div><div class="mt">サンプル行は <code>t[&quot;sample_rows&quot;][:3]</code>（プロファイルは5行保持しているが3行しか出さない）。列名は <code>sample_columns</code> をPythonのリストのまま <code>str()</code> で貼る。</div><div class="mt">最後に、その表固有の用語があれば <code>{tname} の業務用語（質問にこの言葉が出たら必ずこの定義に従う）:</code> と <code>glossary_lines(gl)</code>。<code>glossary_lines</code> は SQL式がある用語には <code>SQL式: … ← この式をそのまま使う</code>、無い用語には <code>（SQL式は未登録。上の列情報をもとに自分で組み立てる）</code> を必ず添える。</div></td></tr>
      <tr><td>_sibling_groups — 兄弟まとまりの自動注記</td><td><div class="mt">「生産実績__daily」と「生産実績_関西工場__daily」のような、拠点・区分違いで同じ構成を持つまとまりの対を、<b>スキーマから機械的に</b>見つけて注記する。人に書かせない理由はコメントに明記されている — 書かせると表の入れ替えで腐るため。</div><div class="mt">アルゴリズムは union-find。</div><pre class="mono small">suffix_owner: 接頭辞を除いた部分（t.split(&quot;__&quot;, 1)[1]） -&gt; それを持つまとまりの集合
parent: まとまり -&gt; 代表（経路圧縮つき find）
suffix_owner の各集合について、先頭以外を先頭にマージ
戻り値: 2件以上のまとまりを含むファミリだけを、内側も外側もソートして返す</pre><div class="mt">入力の <code>by_group</code> は <b><code>db_text</code> が「表示中の表」からだけ</b>組み立てる（<code>&quot;__&quot; in t</code> の表を接頭辞でまとめたもの）。したがって選択外のまとまりの名前が注記から漏れることはない。</div><div class="mt">出力される文面（ファミリ1つにつき1行）：</div><pre class="mono small">※ 生産実績・生産実績_関西工場 は同じ構成の表を持つまとまりです（拠点・区分などの分かれ）。全体・合計を求められたら、該当する表を UNION ALL で合算すること。どれか1つのまとまりを黙って代表にしない。</pre><div class="mt">名前の一致だけで判定し、意味までは断定しない（文面も事実だけを言う）と docstring にある。同じ趣旨の指示は表ルーターの system プロンプト <code>_ROUTE_TABLE_SYSTEM</code> 側にもあり（「同じ領域が拠点・区分ごとに複数の表に分かれていることがある。『全社』『合計』のように範囲を限定しない質問なら、その領域の表をすべて選ぶ」）、絞り込み段と本番プロンプト段の両方で二重に効かせている。</div></td></tr>
      <tr><td>prompt_for_scope — full=True/False の切り替え</td><td><pre class="mono small">def prompt_for_scope(scope, limit=None):
    if not scope:
        return &quot;（対象にできるDBがありません。「データ取り込み」でDBを作るよう案内してください。）&quot;
    full = &quot;\n&quot;.join(db_text_cached(s[&quot;alias&quot;], s[&quot;path&quot;], s.get(&quot;tables&quot;), full=True) for s in scope)
    if len(full) &lt;= (limit if limit is not None else inline_limit()):
        return full
    compact = &quot;\n&quot;.join(db_text_cached(..., full=False) for s in scope)
    return compact + &quot;\n&quot; + 【重要】…</pre><div class="mt">判定は<b>必ず詳細版を組み立ててから長さで比べる</b>（要約版は溢れたときだけ作る）。詳細版は <code>db_text_cached</code> に載るので、捨てても次回の判定で再利用される。</div><div class="mt"><code>limit</code> 省略時のフォールバックは <code>catalog.inline_limit()</code>。中身は <code>models.prompt_inline_limit()</code> → <code>INLINE_LIMIT_MAX</code>（400,000字）で、<code>except</code> で <code>config.PROMPT_INLINE_LIMIT_CHARS</code>（80,000）に落ちる分岐は一枚化された現構成では到達しない（<code>import models</code> は core 自身に解決される）。</div><div class="mt"><b>要約モードに落ちたときに付く警告文</b>（原文の要点）</div><div class="mt">・「対象のDBが多いため、上には各テーブルの説明までしか載せていません。<b>列名は1つも載っていません。</b>」<br>・「上に見当たらないという理由で『その列は無い』『そのテーブルは無い』と判断してはいけない」<br>・「名前から中身が推測できるテーブルは、まず <code>describe_table</code> で列を見てから答えること」<br>・「ユーザーに『その情報は無い』と答えてよいのは、関係しそうなテーブルを <code>describe_table</code> で実際に確認した後だけ」</div><div class="mt">この文面がある理由もコメントにある — 列名が載っていないことを言わずに渡すと、AIが「その列は無い」と早合点して、できることまで断ってしまう。</div><div class="mt"><b><code>describe_table</code> 側の受け口</b>（<code>describe_table_text</code>）は、要約モードの逃げ道として設計されている。</div><div class="mt">・<code>table</code> に <code>alias.table</code> が入ってきても、先頭がスコープ内のエイリアスと一致するときだけ剥がす（表名自体にドットが入る可能性を潰さないため）<br>・<code>db_alias</code> 未指定なら <code>scope[0]</code>（DBは常に1つなので、呼ぶ側が名前を知らなくてよい）<br>・利用者がサイドバーで外した表は <code>&quot;エラー: テーブル &#x27;…&#x27; は、いまの対象に入っていません。&quot;</code> を返す（プロンプトへの載せ方と挙動を揃える）<br>・通過したら <code>table_text(..., full=True)</code> をそのまま返す</div></td></tr>
      <tr><td>文脈長の見積り（tokens_for / budget / inline_limit_for）</td><td><div class="mt">正確なトークン数はAPIに投げないと分からないが、それでは画面を開くたびに課金が発生する。そこで実測から係数を出して概算する（コメントに実測値が残っている：gpt-4o-mini・11DB選択で、要約版 system 28,851字＋ツール定義 44,377字 → 入力 29,265トークン／全文版 71,879字 → 52,395トークン。差分から 43,028字 = 23,130トークン = 0.537 トークン/字）。</div><pre class="mono small">TOKENS_PER_CHAR_TEXT = 0.55   # 日本語主体の本文（カタログ・指示）
TOKENS_PER_CHAR_JSON = 0.31   # ツール定義のJSON（英字と記号が多い）
tokens_for(chars, kind) = int(max(0, chars) * ratio)</pre><div class="mt">係数は実測に対して +1.2% / +1.7% と<b>やや多めに出る</b>ようにしてある（「余裕がある」と言いすぎない方が安全なため）。</div><div class="mt"><b>モデルごとのカタログ上限</b></div><pre class="mono small">context, known = models.context_window(model)
capacity = int(context * CATALOG_CONTEXT_RATIO / llm.TOKENS_PER_CHAR_TEXT)   # 0.5 / 0.55
return max(INLINE_LIMIT_MIN, min(prompt_inline_limit(), capacity))           # [4,000, 400,000]</pre><div class="mt">文脈の半分をカタログに、残り半分をツール定義・履歴・SQL結果・回答に割り当てる配分。実際の値：</div><div class="tablewrap"><table class="data"><thead><tr><th>文脈</th><th>該当モデル例</th><th>上限（字）</th></tr></thead><tbody><tr><td>8,192</td><td>gpt-4</td><td>7,447</td></tr><tr><td>16,385</td><td>gpt-3.5-turbo</td><td>14,895</td></tr><tr><td>128,000</td><td>gpt-4o / gpt-4o-mini / o1-mini / 既定</td><td>116,363</td></tr><tr><td>200,000</td><td>o1 / o3 / o4 系</td><td>181,818</td></tr><tr><td>400,000</td><td>gpt-5 系</td><td>363,636</td></tr><tr><td>1,047,576 / 1,050,000</td><td>gpt-4.1 系 / gpt-5.6</td><td>400,000（天井で頭打ち）</td></tr></tbody></table></div><div class="mt"><code>context_window(model)</code> の決まり方は <b>管理者の登録（完全一致→部分一致）&gt; <code>config.MODEL_CONTEXT_WINDOWS</code>（長い名前から部分一致）&gt; <code>MODEL_CONTEXT_DEFAULT</code>（128,000・戻り値の第2要素が False＝推定）</b>。部分一致にしてあるのは <code>gpt-4o-mini-2024-07-18</code> のような日付つきスナップショットを拾うため。表に無いゲートウェイ独自名・他社モデルは「モデル設定」画面の <code>context_overrides</code> で登録する。</div><div class="mt"><b><code>budget(scope, model, admin)</code></b> は画面（モデル設定）に出す実測ベースの見積り。推定せず、実際に <code>build_system_prompt</code> を組み立てて測る（カタログはキャッシュ済みなので速い）。</div><pre class="mono small">system        = build_system_prompt(scope, admin, model)
used_catalog  = len(catalog.prompt_for_scope(scope))        # ← limit を渡していない
catalog_chars = catalog.inline_length(scope)                 # 全文にした場合の長さ
tool_chars    = len(json.dumps(build_tools(scope, admin)))
fixed_chars   = max(0, len(system) - used_catalog)           # カタログ以外の固定ぶん
now           = tokens_for(len(system)) + tokens_for(tool_chars, &quot;json&quot;)
at_limit      = tokens_for(fixed_chars + limit) + tool_tokens
suggest_max_chars = int((context * 0.5 - tool_tokens - tokens_for(fixed_chars)) / 0.55)</pre><div class="mt"><code>base_tokens</code>（= ツール定義 + 固定ぶん）を返しているのは、画面で上限スライダを動かしたときに<b>サーバと同じ式で</b>再計算できるようにするため。</div></td></tr>
      <tr><td>溢れたときの落とし方（3段）</td><td><div class="mt">上流から順に3段の防御があり、<code>config.SCOPE_MODE</code>（<code>auto</code> / <code>router</code> / <code>all</code>、既定 <code>auto</code>）がどこから始めるかを決める。</div><div class="mt"><b>第1段：<code>_auto_scope</code> — 収まるなら何もしない</b></div><pre class="mono small">scope = build_scope(全DB・全表)
scope から rag.excluded_tables(g.user) の表を落とす   # サイドバーで外した表
SCOPE_MODE == &quot;all&quot;                      → そのまま返す（第2段に任せる）
SCOPE_MODE == &quot;auto&quot; かつ inline_length(scope) &lt;= inline_limit_for(現モデル)
                                         → そのまま返す（ルーターを呼ばない）
それ以外                                  → 表ルーターへ</pre><div class="mt">ルーターを省くのは「選び漏れゼロ」かつ「プロンプトが毎回同一でキャッシュ最大」という2つの効果を狙ったもの。利用者の除外を<b>いちばん外側で</b>適用するのは、以降の判断（収まるか・ルーターに何を見せるか）を除外後の姿で行うため。</div><div class="mt"><b>第2段：表ルーター（<code>route_tables</code>）— 表を絞って詳細を保つ</b></div><div class="mt">・<code>_ROUTE_TABLE_SYSTEM</code> に「JSON配列だけを出せ」「迷ったら含める」「マスタ（結合相手）も選べ」「全部要る・判断できないときは <code>[&quot;*&quot;]</code>」を指示<br>・入力は <code>db_text_cached(..., full=False)</code> の要約カード＋直前3件の質問＋今回の質問<br>・呼び出しは <code>temperature=0, max_tokens=300</code>、応答から <code>re.search(r&quot;\[.*?\]&quot;, ..., re.DOTALL)</code> でJSON配列を切り出す<br>・対応表 <code>known</code> は <code>alias.table</code> と（一意なら）裸の表名の両方を受ける。ルーターLLMは形式を崩しがちで、厳格一致だと正しい選択まで捨ててしまうため<br>・<b>失敗したら None を返す</b>（例外・<code>[&quot;*&quot;]</code>・1件も引けなかった、のいずれも）。絞らずに第3段へ落ちる。「ルーターの不調で答えられなくなるのがいちばん悪い」<br>・<code>total &lt;= 8</code>（表が少ない）なら絞る意味がないので None</div><div class="mt">絞ったあとの補正が2つ。</div><div class="mt">・<b>ピン留め</b> … <code>chat[&quot;table_names&quot;]</code>（この会話で実際にSQLが触った表）を選に足す。「それをグラフに」のような続き質問はルーターに手がかりが無いため。形式は <code>DBファイル名.テーブル名</code> で、DBファイル名自体が <code>.db</code> を含むので <code>rpartition(&quot;.&quot;)</code> で最後のドットで割る<br>・<b><code>expand_tables_by_relations</code></b> … カタログの関連線で1ホップぶんの結合相手を機械的に足す。ここはAIの判断に任せず決め打ち（必要な表の取りこぼしがSQL精度の上限を決めるため）。暴走防止として (a) 判定は<b>元の選択のスナップショット <code>base</code></b> に対して行い、育っていく集合に対しては行わない（連鎖して2ホップになるのを防ぐ）、(b) 方向は「子(from) → 参照先(to)」の一方向のみ（逆をやるとハブ表を選んだ瞬間にDBの大半が付いてくる）</div><div class="mt">最後に、ピン留めと1ホップ補完は利用者の除外を知らないので、<code>off</code> で<b>もう一度落とし直す</b>。</div><div class="mt"><b>第3段：<code>prompt_for_scope</code> の要約モード</b></div><div class="mt">絞ったあとでも <code>len(full) &gt; limit</code> なら、表の1行要約だけ＋「列名は1つも載っていません／<code>describe_table</code> で確かめること」の警告に落ちる。<code>SCOPE_MODE=all</code> のときはここが唯一の防御になる。</div><div class="mt"><b>画面への説明</b>（<code>models._scope_note</code>）は、<code>SCOPE_MODE=all</code> のときだけ「詳細が渡らない要約モードになります」と警告し、それ以外は「使えるデータは変わりません。質問ごとに関係するデータだけへ自動で絞り、詳細を保って渡します」と言う。数字（カタログ全体○字 ＞ このモデルが読める量○字）は根拠として後ろに置く — 数字が先だと初見の利用者が「何かが壊れている」と読むため。</div></td></tr>
      <tr><td>キャッシュ（_TEXT_CACHE / プロファイル）</td><td><div class="mt">カタログ本文の組み立てはDBが多いと1回あたり数十msかかり、質問のたび・対象を選び直すたびに作り直すのは無駄なので <code>_TEXT_CACHE</code> に覚える。</div><pre class="mono small">def _text_key(alias, path, tables, full):
    return (alias, str(p), tuple(tables or ()), full,
            stamp(p), stamp(meta_path(p)), stamp(_cache_path(p)))   # 3つとも st_mtime_ns</pre><div class="mt">・DB本体・<code>.meta.yaml</code>・プロファイルJSONの<b>更新時刻をキーに含める</b>ので、カタログを直せば自動で作り直される（明示的な破棄が要らない）<br>・<code>stat()</code> に失敗したファイルは <code>0</code> として扱う<br>・件数が64を超えたら<b>辞書ごと clear</b>（古い世代を溜めない、LRUではない）<br>・<code>_text_key</code> 自体が例外を投げたら（stat失敗など）キャッシュを迂回して直接 <code>db_text</code> を呼ぶ</div><div class="mt"><code>forget(db_path)</code> はDBを消したときに呼ぶ。本文キャッシュは更新時刻で自動的に切り替わるが、プロファイルの<b>ファイル</b>キャッシュは残るので明示的に unlink する（同じ名前で作り直したときに古い中身が出てくるため）。</div><div class="mt">プロファイル側（<code>profile_db</code>）は <code>data/</code> の外に <code>.profile.json</code> を持ち、キーは <code>{&quot;v&quot;: 2, &quot;mtime&quot;: …, &quot;size&quot;: …}</code>。<code>v</code> は構造バージョンで、上げると古いキャッシュが一斉に無効になる。</div></td></tr>
      <tr><td>モデルごとの差の吸収</td><td><div class="mt">差の吸収は3層に分かれていて、system プロンプトの中身を変えるのは1つ目だけ。</div><div class="mt"><b>1. 文脈量 → カタログの載せ方</b>（<code>inline_limit_for</code> / <code>context_window</code>）</div><div class="mt">前述のとおり、モデル名の部分一致で文脈量を引き、その半分をカタログに割り当てる。名前の表に無いモデルは 128,000 と仮定し、画面には「推定」と出す（<code>_context_row</code> の <code>source</code> が <code>override</code> / <code>table</code> / <code>default</code> の3値）。</div><div class="mt"><b>2. 画像対応</b>（<code>is_vision</code>）</div><div class="mt">完全一致ではなく<b>名前の部分一致</b>。<code>_vision_keys()</code> は「モデル設定」画面の登録 &gt; <code>config.OPENAI_VISION_MODELS</code> の順。モデル名は環境によって違うため。<code>_begin_turn</code> は画像つきの質問を非対応モデルで弾く。<code>user_message</code> は画像が無ければ <code>content</code> を文字列のまま返す（画像非対応モデルに配列を渡すと弾かれることがある）。</div><div class="mt"><b>3. 呼び出し引数の作法</b>（<code>_create</code> / <code>_QUIRKS</code> / <code>_fix_for</code> / <code>_learn</code>）</div><div class="mt">モデル名の一覧で場合分けすると、ゲートウェイや新モデルのたびに保守が要る。そこで「1回投げて、断られた理由を読んで直して、覚える」方式にしてある。400 は推論前に弾かれるのでやり直しても課金されない、というのが成立の根拠。学習内容 <code>_QUIRKS</code> は<b>プロセスの寿命だけ</b>持つ（再起動後の最初の1回だけ余計に往復する）。</div><div class="tablewrap"><table class="data"><thead><tr><th>エラー文の特徴</th><th>直し方</th></tr></thead><tbody><tr><td><code>reasoning_effort</code> + <code>function tools</code></td><td><code>reasoning_effort=&quot;none&quot;</code> を set</td></tr><tr><td><code>reasoning_effort</code> + <code>does not support</code></td><td><code>reasoning_effort=&quot;none&quot;</code> を set</td></tr><tr><td><code>reasoning_effort</code> + <code>unrecognized</code></td><td>引数ごと drop</td></tr><tr><td><code>&#x27;temperature&#x27;</code> / <code>&#x27;top_p&#x27;</code> + <code>does not support</code> or <code>only the default</code></td><td>その引数を drop</td></tr><tr><td><code>max_tokens</code> と <code>max_completion_tokens</code> が両方出る</td><td><code>max_completion_tokens</code> に付け替え</td></tr></tbody></table></div><div class="mt">直しは1回の呼び出しにつき <code>_MAX_FIX = 4</code> 回まで。同じ直しを繰り返している（<code>set_</code> の内容がすでに適用済み）／drop 対象がそもそも無い、ときは諦めて例外を投げる。レート制限（429）は「引数の直し方の問題ではない」ので先に片付け、<code>retry-after</code> ヘッダ → エラー文の <code>try again in X</code>（ms/s/m を解釈し +0.5秒の余裕を足す） → 2/4/8秒の指数バックオフ、の順で待って投げ直す。使い切ると <code>RateLimited</code> を投げ、生JSONではなく人が読んで動ける文面にする。</div><div class="mt"><code>chat()</code> と <code>chat_stream()</code> はどちらも <code>_create()</code> を通るので、学習した調整は両方に効く。</div></td></tr>
      <tr><td>主なデータ構造</td><td>・scope エントリ（build_scope が作る）= {&quot;path&quot;: str(DBファイルの絶対パス), &quot;alias&quot;: SQLで使う英数字＋_のエイリアス, &quot;name&quot;: DBファイル名（例 &quot;統合.db&quot;）, &quot;tables&quot;: [表名, ...], &quot;meta&quot;: load_meta の結果}<br>・profile（profile_db）= {&quot;file&quot;, &quot;key&quot;: {&quot;v&quot;:2,&quot;mtime&quot;,&quot;size&quot;}, &quot;generated_at&quot;, &quot;tables&quot;: {表名: tableinfo}}<br>・tableinfo = {&quot;type&quot;: &quot;table&quot;|&quot;view&quot;, &quot;columns&quot;: [{&quot;name&quot;,&quot;type&quot;,&quot;notnull&quot;,&quot;pk&quot;,&quot;pk_seq&quot;}], &quot;fks&quot;: [{&quot;from&quot;,&quot;table&quot;,&quot;to&quot;}], &quot;row_count&quot;: int|None, &quot;sample_columns&quot;: [列名], &quot;sample_rows&quot;: [[値,...]], &quot;col_stats&quot;: {列名: {&quot;values&quot;: [[値,件数],...]} | {&quot;min&quot;,&quot;max&quot;}}}<br>・meta（.meta.yaml）= {&quot;tables&quot;: {表名: {&quot;description&quot;, &quot;ai_draft&quot;, &quot;primary_key&quot;: [列], &quot;columns&quot;: {列名: {&quot;description&quot;, &quot;values&quot;: {コード: ラベル}}}, &quot;glossary&quot;: {...}}}, &quot;groups&quot;: {接頭辞: {&quot;description&quot;: メモ}}, &quot;glossary&quot;: {用語: {...}}, &quot;relationships&quot;: [{&quot;from&quot;,&quot;to&quot;,&quot;cardinality&quot;}], &quot;examples&quot;: [{&quot;q&quot;,&quot;description&quot;,&quot;sql&quot;}], &quot;checks&quot;: [...], &quot;tools&quot;: [...], &quot;builtin_tools&quot;: {...}}<br>・用語エントリ（normalize_glossary 後）= {用語: {&quot;description&quot;: str, &quot;sql&quot;: str}}（値が文字列のYAMLは説明として扱う）<br>・関連の端点（parse_endpoint_cols）= (alias, table, [列, ...])。&quot;table.col&quot; / &quot;alias.table.col&quot; / &quot;table.(c1, c2)&quot; / &quot;alias.table.(c1, c2)&quot; を解く<br>・rel_pairs(rel, own_alias) = ((from側alias, table), (to側alias, table), [(from列, to列), ...]) または None（解けない・列数不一致）<br>・_sibling_groups の戻り値 = [[まとまり名, まとまり名, ...], ...]（2件以上のファミリのみ、内外ともソート済み）<br>・_TEXT_CACHE のキー = (alias, str(path), tuple(tables or ()), full, DBのmtime_ns, metaのmtime_ns, profile.jsonのmtime_ns)<br>・route_tables の戻り値 = {DBファイル名: [表名, ...]} または None（絞らない）<br>・budget の戻り値 = {&quot;model&quot;,&quot;context&quot;,&quot;context_known&quot;,&quot;limit_chars&quot;,&quot;catalog_chars&quot;,&quot;catalog_inlined&quot;,&quot;tool_tokens&quot;,&quot;base_tokens&quot;,&quot;tokens_per_char&quot;,&quot;now_tokens&quot;,&quot;now_pct&quot;,&quot;headroom_pct&quot;,&quot;at_limit_tokens&quot;,&quot;at_limit_pct&quot;,&quot;suggest_max_chars&quot;}<br>・problems_by_table の戻り値 = {(db_file, table): [{&quot;id&quot;,&quot;name&quot;,&quot;db_file&quot;,&quot;table&quot;,&quot;kind&quot;: &quot;failed&quot;|&quot;degraded&quot;|&quot;overdue&quot;,&quot;since&quot;,&quot;message&quot;}, ...]}<br>・build_tools の1要素 = {&quot;type&quot;:&quot;function&quot;, &quot;function&quot;: {&quot;name&quot;, &quot;description&quot;, &quot;parameters&quot;: {&quot;properties&quot;: {...(SQLツールには explanation が注入される)}, &quot;required&quot;: [...]}}}</td></tr>
      <tr><td>定数・しきい値</td><td>・TOKENS_PER_CHAR_TEXT = 0.55 — 日本語主体の本文1文字あたりのトークン概算。gpt-4o-mini・11DB選択での実測（43,028字 = 23,130トークン = 0.537）を切り上げた値。実測に対し +1.2%〜+1.7% 多めに出る<br>・TOKENS_PER_CHAR_JSON = 0.31 — ツール定義JSONの1文字あたりトークン概算（英字と記号が多い）<br>・CATALOG_CONTEXT_RATIO = 0.5（models 側）— モデル文脈のうちカタログに使ってよい割合。残り半分はツール定義・履歴・SQL結果・回答用<br>・INLINE_LIMIT_MIN = 4,000 / INLINE_LIMIT_MAX = 400,000（字）— inline_limit_for の床と天井。天井は「文脈が100万トークンでもカタログはここまで」の安全弁で、画面からは変えられない<br>・config.MODEL_CONTEXT_DEFAULT = 128,000（env で変更可）— 名前が表にも登録にも当たらないモデルの仮の文脈量。context_window の第2要素が False（＝推定）になる<br>・config.PROMPT_INLINE_LIMIT_CHARS = 80,000 — 旧env互換で読むだけ。現構成では到達しない（catalog.inline_limit の except 分岐でしか使われず、import models は core 自身に解決されるので失敗しない）<br>・config.SCOPE_MODE = &quot;auto&quot;（他に &quot;router&quot; / &quot;all&quot;。不正値は auto に丸める）<br>・route_tables の早期 return しきい値: 表の総数 &lt;= 8 なら絞らない（全部渡した方が確実）<br>・route_tables に渡す会話履歴: 直近3件の質問（history[-3:]）<br>・ルーター呼び出しのパラメータ: temperature=0, max_tokens=300<br>・_TEXT_CACHE の上限 64 件（超えたら辞書ごと clear。LRUではない）<br>・config.PROFILE_LOW_CARDINALITY = 20 — この distinct 数以下なら実値一覧、超えたら min/max を持つ<br>・config.PROFILE_SAMPLE_ROWS = 5（保持）／table_text が出すのは先頭3行<br>・config.PROFILE_STATS_MAX_ROWS = 2,000,000 — これ以上の行数の表は列統計をスキップ（＝値一覧も範囲も出ない）<br>・config.PROFILE_TIMEOUT_SEC = 30 — プロファイリング中の1クエリのタイムアウト<br>・catalog.EXAMPLES_MAX = 200 — 1DBあたりの例文上限。DB統一で全拠点分（現在105件）が1ファイルに集まるため、その全量が収まる値。ただし強制は保存時のみ<br>・config.MAX_AGENT_STEPS = 10 — 1質問あたりのツール往復上限（system は1ターン1回、ツール定義は毎ステップ再構築）<br>・_MAX_FIX = 4 — 1回の LLM 呼び出しで引数を直しにいく上限<br>・config.MODEL_CONTEXT_WINDOWS — gpt-5.6:1,050,000 / gpt-5系:400,000 / gpt-4.1系:1,047,576 / gpt-4o系:128,000 / o1,o3,o4:200,000（o1-mini は128,000）/ gpt-4:8,192 / gpt-3.5-turbo:16,385。名前の長い順に部分一致</td></tr>
    </tbody></table></div>
    <div class="card__title mt">落とし穴（15件）</div>
    <div class="tablewrap"><table class="data"><thead><tr><th style="width:60px">#</th><th>内容</th></tr></thead><tbody>
      <tr><td class="mono small">01</td><td>表名の検出に使う正規表現 <code>(?&lt;![\w.])表名(?![\w])</code> は、Python の <code>\w</code> が日本語も語構成文字として扱うため「生産実績__dailyの行数」のように<b>表名の直後に日本語の助詞が続くとマッチしない</b>。結果、<code>_no_hidden_tables(用語の説明文)</code> は非表示の表に触れていても True を返し、絞り込み時の漏れ止めをすり抜ける。同じ罠は <code>_memo_bad_tables</code> のコメントで明示的に語られている（あちらは「実在する表名の占める位置を先に塗る」逆向きの実装で回避している）が、db_text 側の2つの内部関数は素の正規表現のまま。</td></tr>
      <tr><td class="mono small">02</td><td><b>まとまりメモと兄弟まとまり注記だけ、<code>limited</code> のときの漏れ止めがかかっていない。</b> relationships・用語・例文は <code>_mentions_only_shown</code> / <code>_no_hidden_tables</code> で間引かれるのに、まとまりメモ（<code>【g】\nメモ本文</code>）は表示中のまとまりのぶんがそのまま入る。メモ本文が選択外の表に言及していれば、その名前はプロンプトに漏れる。drift_warnings のコメントも「メモはプロンプトの最上段に無印で入る」と書いていて、腐ると回答に直に効く場所。</td></tr>
      <tr><td class="mono small">03</td><td><b><code>budget()</code> の <code>used_catalog</code> は <code>prompt_for_scope(scope)</code> を limit 無しで呼ぶ</b>（＝上限 400,000字で判定）。一方 <code>build_system_prompt</code> は <code>inline_limit_for(model)</code> で判定する。モデル上限が 400,000字未満で、カタログがそれを超えている構成では、budget は「全文カタログの長さ」を引いてしまい <code>fixed_chars = max(0, len(system) - used_catalog)</code> が 0 に潰れる。画面の <code>at_limit_tokens</code> / <code>suggest_max_chars</code> が過小に出る。</td></tr>
      <tr><td class="mono small">04</td><td><b><code>stale_note</code> は DBファイル単位でしか絞らない。</b> <code>if db_file in in_scope</code> だけを見て <code>table</code> がそのスコープの <code>tables</code> に残っているかを確認しないので、表ルーターが外した表・利用者がサイドバーで除外した表についても「データが古い可能性」の注記がプロンプトに載る。</td></tr>
      <tr><td class="mono small">05</td><td><b><code>route_tables</code> の <code>total &lt;= 8</code> 判定は利用者の除外を無視する。</b> <code>prof[&quot;tables&quot;].keys()</code>（プロファイル全表）を数えるので、104表のうち3表だけを残していても total は 104 のままルーターが走る。一方、ルーターに見せるカード（<code>db_text_cached(..., full=False)</code>）は除外後の <code>s[&quot;tables&quot;]</code> を尊重する。両者の分母が食い違っている。</td></tr>
      <tr><td class="mono small">06</td><td><b><code>inline_length</code> と <code>prompt_for_scope</code> の長さが (DB数-1) 文字ずれる。</b> 前者は各DBの本文長を単純に足し、後者は <code>&quot;\n&quot;.join</code> した文字列を測る。DB1つの現構成では一致するが、複数DBだと <code>_auto_scope</code> の「収まる」判定と <code>prompt_for_scope</code> の「収まる」判定が境界で逆転しうる。</td></tr>
      <tr><td class="mono small">07</td><td><b>ビューは表と完全に同じ見た目でプロンプトに載る。</b> プロファイルは <code>sqlite_master</code> から <code>type IN (&#x27;table&#x27;,&#x27;view&#x27;)</code> を拾って <code>t[&quot;type&quot;]</code> に保持しているが、<code>table_text</code> も <code>db_text</code> も type を一切出力しない。AIから見てビューと実表の区別は付かない（「まとまり__名前」にすれば表と同じ扱いが全部効く、という設計の帰結）。</td></tr>
      <tr><td class="mono small">08</td><td><b>列行の <code>PK</code> マークは DB宣言の主キーだけ。</b> <code>- 名前 型 PK</code> は <code>c[&quot;pk&quot;]</code>（PRAGMA table_info）を見るので、<code>.meta.yaml</code> の <code>primary_key</code> で人が指定した主キーは列行に反映されない。見出しの <code>主キー（人が指定）: …</code> 行だけが情報源になる。</td></tr>
      <tr><td class="mono small">09</td><td><b>値情報の3択は排他で、順番に意味がある。</b> <code>col_stats[&quot;values&quot;]</code>（実データ由来）があればメタのコード値辞書はラベル補完にしか使われない。distinct が20を超える列や200万行超の表ではプロファイル統計が無いので、そこで初めてメタの <code>values</code> が <code>/ コード値:</code> として全件出る。同じ列でもデータ量次第で出力の形が変わる。</td></tr>
      <tr><td class="mono small">10</td><td><b>system プロンプトは毎ターン index 0 を丸ごと差し替える。</b> 表ルーターの選択がターンごとに変わるため、前のターンでカタログに載っていた表が次のターンでは消えることがある（履歴に残るツール結果はそのまま）。「ピン留め」（この会話でSQLが触った表を残す）はその緩和策だが、SQLを実行していない表には効かない。</td></tr>
      <tr><td class="mono small">11</td><td><b><code>現在時刻</code> が system プロンプトの最終行に置かれている。</b> カタログはその直前、tool_list はさらに前にあるので、毎ターン変わる部分が末尾に集まり、プレフィックス方式のプロンプトキャッシュはカタログまで効く。逆に、ツール一覧・KB一覧・stale_note はカタログより前なので、これらが変わるとカタログ以降のキャッシュも落ちる（KB選択が利用者ごとに違えば、利用者ごとに別プレフィックスになる）。</td></tr>
      <tr><td class="mono small">12</td><td><b><code>table_text</code> は表名にエイリアス（DB名）を付けない。</b> 一方 <code>route_tables</code> はカタログの <code>alias.table</code> 形式で選ばせる前提の system プロンプトを持ち、<code>describe_table</code> も <code>alias.table</code> を受ける。db_text/table_text の出力には <code>alias.</code> が現れないため、AIが <code>alias.table</code> 形式を使う手がかりは複数DB時の <code>naming</code> 文だけになる（<code>describe_table_text</code> が先頭のエイリアスを剥がす処理は、この不一致の受け皿）。</td></tr>
      <tr><td class="mono small">13</td><td><b>例文の EXAMPLES_MAX=200 は保存時にしか効かない。</b> <code>db_text</code> は <code>meta[&quot;examples&quot;]</code> を無制限に全件出力する。手書きYAMLや外部からの流し込みで200件を超えると、そのままプロンプトを圧迫し、表定義の説明を押し出す（EXAMPLES_MAX のコメントが警告している状況そのもの）。</td></tr>
      <tr><td class="mono small">14</td><td><b><code>limited</code> フラグは「表示中の表数 &lt; プロファイル全表数」で決まる。</b> 表ルーターが結果的に全表を選ぶと <code>limited</code> が False になり、「対象にしているのは下に挙げる表だけ」の注記も、関連・用語・例文の間引きも一切かからない。逆に <code>tables=[]</code>（空リスト）は <code>names = tables or 全表</code> により <code>tables=None</code> と同じ「全表・limited なし」になる。</td></tr>
      <tr><td class="mono small">15</td><td><b>一枚化の副作用：<code>import models</code> / <code>import llm</code> / <code>import catalog</code> はすべて core 自身に解決される</b>（ファイル冒頭で <code>sys.modules</code> にエイリアス登録）。関数内 import は「循環import回避」とコメントされているが、実体は自己参照。このため <code>catalog.inline_limit()</code> の <code>except: return config.PROMPT_INLINE_LIMIT_CHARS</code> は到達不能で、env の 80,000 は死んでいる。実効天井は常に 400,000。</td></tr>
    </tbody></table></div>
  </div>

  <div class="card mt">
    <div class="card__title" id="impl-router">5-3. AIに見せる表の決め方</div>
    <div class="card__desc">1質問ごとに「AIへ渡すカタログの範囲（scope）」を決めるサブシステム。利用者がDBや表を選ぶUIは無く、サイドバーにあるのは「外す」チェック（tables_off）だけで、残りはサーバが自動で決める。決定は _auto_scope が担い、(1)tables_off を最初に落とす → (2)SCOPE_MODE と「選択中モデルが読める文字数」でそのまま全部渡すか判断 → (3)収まらないときだけ LLM の表ルーター route_tables で絞り、会話でSQLが触った表のピン留めとカタログの関連1ホップ補完を足し、tables_off をもう一度引く、という順で進む。絞り込みはプロンプト（db_text の limited 注記と関連・用語・例文のフィルタ）だけでなく、SQLite の set_authorizer による読み取り拒否までデータ層で強制される。</div>
    <div class="tablewrap"><table class="data"><thead><tr><th style="width:210px">項目</th><th>内容</th></tr></thead><tbody>
      <tr><td>全体の流れ（1質問ぶん）</td><td><div class="mt">表の決め方は「質問ごとにサーバが決める」。利用者にDBやテーブルを選ばせるUIは無く、サイドバーにあるのは<b>外すためのチェック</b>だけ。</div><pre class="mono small">_begin_turn()
  ├ 質問テキスト検証 / LLM設定確認
  ├ rag.set_current_user(g.user)   ← 以降 prefs をスレッドローカルから引ける
  ├ chat[&quot;render_log&quot;] に今回の質問を append → _persist        ※重要（後述）
  ├ scope = _auto_scope(text, chat)        ← ここが本サブシステム
  ├ scope も KB も無ければ _TurnError で送信中止
  ├ _realtime_refresh(scope)
  └ chat[&quot;messages&quot;][0] = llm.build_system_prompt(scope, admin, model=models.current(g.user))</pre><div class="mt"><code>_begin_turn</code> は <code>/api/chat/send</code> と <code>/api/chat/stream</code> の共通前処理なので、通常送信でもストリーミングでも同じ経路を通る。system prompt は毎ターン作り直され、会話ファイルには保存されない（カタログの変更に追従させるため）。</div><div class="mt">決まった <code>scope</code> はプロンプトだけでなく <code>tools.build_tools(scope, ...)</code>、SQL実行（authorizer）、<code>describe_table</code>、<code>open_table</code> などツールの実処理すべてに同じ形で渡る。</div></td></tr>
      <tr><td>_auto_scope — 決定の順序</td><td><pre class="mono small">scope = build_scope({f.name: [] for f in db.list_db_files()})   # 全DB・全表
off   = set(rag.excluded_tables(g.user))
if off:
    各 s の tables から off を除く / 表が0になったDBは scope から落とす
if not scope: return scope                       # ← ここで終わる（モード判定より前）
if config.SCOPE_MODE == &quot;all&quot;: return scope
limit = models.inline_limit_for(models.current(g.user))
if config.SCOPE_MODE == &quot;auto&quot; and catalog.inline_length(scope) &lt;= limit:
    return scope                                 # 全部入り＝選び漏れゼロ
# --- ここから絞る（auto で溢れたとき / router モード）---
chat_history = render_log の role==user かつ kind==&quot;text&quot; の content 全部
picked = llm.route_tables(question, scope, chat_history)
if picked:
    ① chat[&quot;table_names&quot;] のピン留めを picked に足す
    ② picked = llm.expand_tables_by_relations(picked, scope)
    ③ 各DBについて sel = picked.get(name); off を**もう一度**引く; sel が空でなければ s[&quot;tables&quot;] = sel
return scope</pre><div class="mt">設計の要点は3つ。</div><div class="mt">・<b>tables_off はいちばん外側で落とす。</b> 以降の判定（収まるか・ルーターに何を見せるか）を、外した後の姿で行うため。<br>・<b>絞らない道を最優先する。</b> カタログ全体が入るなら絞らない。ルーターを省けば選び漏れがゼロになり、プロンプトが毎回同一になってプロンプトキャッシュが効く。<br>・<b>判断できないときは絞らない。</b> <code>route_tables</code> が None を返したらスコープはそのまま（＝上限超えなら <code>prompt_for_scope</code> の要約モードに落ちる）。ルーターの不調で答えられなくなるのがいちばん悪い、という判断。</div><div class="mt"><code>build_scope</code> は selection の値が空リストのとき <code>want = [...] or available</code> で全表に落ちるので、<code>{f.name: []}</code> は「そのDBの全表」を意味する。したがって <code>s[&quot;tables&quot;]</code> は常にリストであって None にはならない（この違いは後述の <code>limited</code> 判定に効く）。</div></td></tr>
      <tr><td>SCOPE_MODE の3値と上限の計算</td><td><div class="tablewrap"><table class="data"><thead><tr><th>値</th><th>挙動</th></tr></thead><tbody><tr><td><code>auto</code>（既定）</td><td>カタログ全文が選択中モデルの読める量に収まるならそのまま直載せ。収まらないときだけ表ルーター</td></tr><tr><td><code>router</code></td><td>常に表ルーター（<code>== &quot;router&quot;</code> という分岐は存在せず、all でも auto-fits でもない残り全部が routing に落ちることで実現している）</td></tr><tr><td><code>all</code></td><td>常に全表。上限を超えると <code>prompt_for_scope</code> が要約モードに落ちる（列名がAIに渡らない）</td></tr></tbody></table></div><div class="mt">上限 <code>limit</code> は <code>models.inline_limit_for(model)</code>:</div><pre class="mono small">context, known = context_window(model)              # 管理者override &gt; 公式表 &gt; 既定128000
capacity = int(context * 0.5 / 0.55)               # 文脈の半分 ÷ 日本語1文字あたりトークン
return max(4_000, min(400_000, capacity))</pre><div class="mt">測る側 <code>catalog.inline_length(scope)</code> は <code>db_text_cached(alias, path, s[&quot;tables&quot;], full=True)</code> の文字数合計。<code>build_system_prompt</code> も同じ <code>inline_limit_for(model)</code> を <code>prompt_for_scope(scope, limit=inline_cap)</code> に渡すので、判定と実際の埋め込みは同じ物差しで動く。</div><div class="mt"><code>db_text_cached</code> のキャッシュキーは (alias, path, tables, full, DBのmtime_ns, .meta.yaml の mtime_ns, プロファイルキャッシュの mtime_ns)。カタログを直せば自動で作り直される。エントリが64を超えたら丸ごとクリアする。</div></td></tr>
      <tr><td>route_tables — 表ルーターの中身</td><td><div class="mt">世に言うスキーマ・リンキング。<code>llm</code> 相当部の <code>_ROUTE_TABLE_SYSTEM</code> ＋ カタログのカードを1回投げて、JSON配列を受け取る。</div><div class="mt"><b>(a) 名前解決表 known を先に作る</b></div><pre class="mono small">for s in scope:
    for t in profile_db(s[&quot;path&quot;])[&quot;tables&quot;]:      # ← s[&quot;tables&quot;] ではなく全表
        total += 1
        &quot;alias.table&quot; と &quot;table&quot; の両方を known に登録（lower）
        既に別の (DB,表) が入っていたら ambiguous に記録
ambiguous のキーは known から削除
そのあと &quot;alias.table&quot; だけ全部入れ直す      # alias付きは必ず引けるようにする</pre><div class="mt">ルーターLLMは出力形式を崩しがちで、厳格一致にすると正しい選択まで捨ててしまうため、素の表名でも引けるようにしてある。ただし複数DBで名前が衝突する素の表名は捨てられ、<code>alias.table</code> でしか引けなくなる。</div><div class="mt"><b>(b) 早期リターン</b>: <code>total &lt;= 8</code> なら <code>None</code>（絞る意味がない）。</div><div class="mt"><b>(c) カード生成</b>: <code>db_text_cached(alias, path, s.get(&quot;tables&quot;), full=False)</code> をDBぶん連結。full=False の中身は</div><div class="mt">・<code>## 使えるデータ</code> ＋（絞っているときの注記）<br>・兄弟まとまりの注記（<code>_sibling_groups</code>）<br>・まとまりメモ（<code>【まとまり名】</code> ＋ 本文）<br>・<code>テーブル一覧:</code> … <code>- 表名（12,345行） : 説明 / 業務用語: A, B</code> の1行要約（列名は入らない）<br>・<code>結合キー（JOINにはこれを使う）:</code>（FK宣言＋カタログの関連）<br>・テーブルをまたぐ業務用語 / 確認済み例文</div><div class="mt"><b>(d) user メッセージ</b>: カード ＋ 空行 ＋ <code>（直前の質問: …）</code>×最大3 ＋ <code>今回の質問: …</code>。</div><div class="mt"><b>(e) 応答の解析</b></div><pre class="mono small">m = re.search(r&quot;\[.*?\]&quot;, content, re.DOTALL)
picked = json.loads(m.group(0)) if m else []</pre><div class="mt"><code>&quot;*&quot;</code> が含まれていれば None（全部要る＝絞らない）。各要素を <code>known</code> で引き、当たったものだけ <code>{DBファイル名: set(表名)}</code> に積む。1件も当たらなければ None。</div><div class="mt"><b>(f) 失敗時</b>: try 全体を except で受け、<code>print(&quot;[router] 表の振り分けに失敗したため絞りません: …&quot;)</code> して None。API障害・タイムアウト・JSON崩れ・上限で切れた応答、すべてここに落ちる。利用者にはエラーが出ず、単に絞られないだけ（＝要約モードへのフォールバック）。</div><div class="mt">システムプロンプト側の方針も読んでおくとよい: 「迷ったら含める。外しすぎて答えられないより多めの方がよい」「集計対象だけでなく結合相手のマスタも選ぶ」「拠点・区分ごとに分かれた表は、範囲を限定しない質問ならその領域の表をすべて選ぶ」。</div></td></tr>
      <tr><td>ピン留めと関連1ホップ補完</td><td><div class="mt"><b>ピン留め</b>（<code>_auto_scope</code> 内）: <code>chat[&quot;table_names&quot;]</code>（&quot;DBファイル名.表名&quot;）を <code>rpartition(&quot;.&quot;)</code> で割り、scope にあるDBのぶんだけ <code>picked</code> に足す。「それをグラフに」のような続き質問はルーターに手がかりが無いため、この会話で実際にSQLが触った表は選から漏れても残す、という趣旨。ただし現構成では table_names が埋まらない（gotchas 参照）。</div><div class="mt"><b>関連1ホップ補完</b> <code>expand_tables_by_relations(picked, scope)</code>:</div><pre class="mono small">base = picked のスナップショット        # 育っていく集合に対して判定しない
out  = picked のコピー
for s in scope:
  for rel in load_meta(s[&quot;path&quot;])[&quot;relationships&quot;]:
     (fa,ft,_), (ta,tt,_) = parse_endpoint_cols(rel[&quot;from&quot;], s[&quot;alias&quot;]), 同 to
     if ft が base に入っている: out に tt を足す（実在する表のときだけ）</pre><div class="mt">判定を base（元の選択）に対して行うのは、育っていく集合に対して判定すると追加された表が次の判定を呼んで連鎖し、1ホップのつもりが2ホップになって設備マスタのようなハブ経由で無関係な表まで雪だるま式に増えるため。</div><div class="mt">方向を <b>from→to（子→参照先）に限っている</b>のも同じ理由。逆向き（選んだマスタを参照している表を全部足す）をやると、ハブ表を選んだ瞬間にDBの大半が付いてくる。</div><div class="mt">この補完がAIの判断ではなく決め打ちなのは、「必要な表の取りこぼしがSQL精度の上限を決める」から。ルーターが結合相手を選び忘れても宣言済みの関係から機械的に埋められる。</div><div class="mt"><b>そのあと off を引き直す</b>。ピン留めも関連補完も tables_off を知らないので、ここで落とし直さないと会話の続きで除外したはずの表が戻ってきてしまう。</div></td></tr>
      <tr><td>利用者のチェック（tables_off）</td><td><div class="mt"><b>保存形式</b>は「選んだもの」ではなく「外したもの」。<code>prefs.KEYS = (&quot;model&quot;, &quot;rag_off&quot;, &quot;rag_settings&quot;, &quot;tables_off&quot;)</code> で、値は表名の素の配列（DB名は付かない）。理由はコメントに明記されている: 選択リスト方式にすると、新しく取り込んだ表が既存の利用者全員に見えないままになる。除外方式なら<b>新しい表は既定で対象に入る</b>。ナレッジベース（rag_off）とまったく同じ設計。</div><div class="mt"><b>読み出し</b>: <code>rag.excluded_tables(user)</code> → <code>prefs.load(user).get(&quot;tables_off&quot;)</code> を str 化して返すだけ。実在チェックはしない。</div><div class="mt"><b>保存</b>: <code>POST /api/tables/prefs</code>（<code>login_required</code>）。body は <code>{off: [表名, ...]}</code>。サーバ側で全DBの <code>profile_db(f)[&quot;tables&quot;]</code> に実在する名前だけ残してから書く。</div><div class="mt"><b>UI</b>（<code>wireScope</code>）: チェックボックスは押した時点で保存する。「保存」を押させると押し忘れたまま質問して「なぜあの表を見ないのか」になるため。送るのは <code>off = 未チェックのもの</code>。まとまり（接頭辞）の親チェックは配下を一括で切り替え、一部だけONなら indeterminate になる。<code>#tblAll</code> は「1つでも未チェックがあれば全選択、そうでなければ全解除」。</div><div class="mt"><b>適用される場所</b>（優先順位＝上から順に効く）:</div><div class="mt">・<code>_auto_scope</code> の先頭 — scope から物理的に落とす。ここが基準になるので、収まるかの判定もルーターに見せるカードも「外した後の姿」で行われる<br>・<code>_auto_scope</code> の末尾 — ピン留め・関連補完で戻ってきたぶんを再度落とす<br>・<code>catalog.db_text</code> — 表が減っていれば <code>limited</code> として注記＋関連/用語/例文をフィルタ<br>・<code>catalog.describe_table_text</code> — <code>entry[&quot;tables&quot;]</code> に無ければ説明も見せない（中身と扱いを揃える）<br>・<code>db.run_select</code>（<code>_make_authorizer</code>）— SQLite が実際に読む一歩手前で DENY</div><div class="mt">5がある理由もコメントに書かれている: プロンプトから消すだけでは、AIが名前を覚えている・推測できる場合に読めてしまうため、最後の関門はデータ層に置く。</div><pre class="mono small">allowed: set | None = set()
for s_ in use:                       # use = narrow_scope(sql, scope)
    if s_.get(&quot;tables&quot;): allowed |= set(s_[&quot;tables&quot;])
    else: allowed = None; break      # 表を持たないDBが1つでもあれば制限しない
...
conn.set_authorizer(_make_authorizer(allowed))</pre><div class="mt"><code>_authorizer</code> は <code>_ALLOWED_ACTIONS</code>（SELECT / READ / FUNCTION / RECURSIVE）以外を DENY し、SQLITE_READ のとき arg1（表名）が allowed に無ければ DENY（<code>sqlite_</code> 始まりは除外）。</div><div class="mt">全部外すと <code>_auto_scope</code> は空 scope を返し、KBも無ければ <code>_TurnError</code>「いま調べられるものがありません。」。KBがあれば scope=[] のまま進み、system prompt の naming が「いま対象にできるデータがありません。数値の集計はできないので、ナレッジベースの検索で答えられる範囲で答えること。」に切り替わる。</div></td></tr>
      <tr><td>絞ったときにプロンプトへ入る注記</td><td><div class="mt">注記は2種類ある。両方とも「絞ったこと」ではなく「見えていない情報がある」ことをAIに伝えるためのもの。</div><div class="mt"><b>(1) 表を絞ったときの注記</b>（<code>catalog.db_text</code>）。<code>limited = tables is not None and len(shown) &lt; len(profile[&quot;tables&quot;])</code> のとき、<code>## 使えるデータ</code> の直後に入る:</div><div class="mt">&gt; ※ 利用者がいま対象にしているのは、下に挙げる表だけです。ここに無いデータは存在しないものとして答えてください。他の表があるかのような案内・前置き・質問返しはしないこと。対象外の話を求められたら、サイドバーの SQLite3 でその表にチェックを入れるよう一言で伝えてください。</div><div class="mt">理由はコメントどおり: 絞っていることを明示しないと、AIは知識として知っている他データの話を始め、最後に「使えません」と言う（利用者からは「できないのに答える」に見える）。</div><div class="mt"><code>limited</code> のときは注記だけでなく<b>周辺情報も表示中の表に限定</b>される。素通しにすると載せていない表の名前が例文などから漏れ、AIが「あるはず」と判断して読みに行ってしまうため。</div><div class="tablewrap"><table class="data"><thead><tr><th>対象</th><th>フィルタ</th></tr></thead><tbody><tr><td>relationships</td><td><code>_mentions_only_shown(from + &quot; &quot; + to)</code> … 触れている表が1つ以上あり、全部が表示中</td></tr><tr><td>業務用語</td><td>SQL式は <code>_mentions_only_shown(sql)</code>、説明文は <code>_no_hidden_tables(description)</code>（表名が出てこなければ通す）</td></tr><tr><td>例文</td><td><code>_mentions_only_shown(ex[&quot;sql&quot;])</code></td></tr><tr><td>まとまりメモ</td><td>表示中の表から作った <code>by_group</code> のぶんだけ</td></tr><tr><td>兄弟まとまりの注記</td><td><code>_sibling_groups(by_group)</code> … 表示中の表だけから導くので、選択外のまとまり名は漏れない</td></tr></tbody></table></div><div class="mt">表名の照合は <code>(?&lt;![\w.])名前(?![\w])</code>。日本語の表名があるので <code>\w</code>（UNICODE）でなければ「品質__x」が「高品質__x」に当たる。</div><div class="mt"><b>(2) 要約モードの注記</b>（<code>catalog.prompt_for_scope</code>）。全文が limit を超えたときに compact 版へ落とし、末尾に付く:</div><div class="mt">&gt; 【重要】対象のDBが多いため、上には各テーブルの説明までしか載せていません。<b>列名は1つも載っていません。</b> … 上に見当たらないという理由で「その列は無い」「そのテーブルは無い」と判断してはいけない … ユーザーに「その情報は無い」と答えてよいのは、関係しそうなテーブルを describe_table で実際に確認した後だけです。</div><div class="mt"><b>画面側の注記</b>は別物で <code>models._scope_note(total, limit)</code>。<code>models.status()</code> の <code>scope.note</code> として返り、チャット画面の警告バーに出る。all モードのときだけ「要約モードになります…SCOPE_MODE を見直してください」、それ以外は「使えるデータは変わりません。カタログが大きいので、質問ごとに関係するデータだけへ自動で絞り、詳細を保って渡します」。安心を先に、数字（カタログ全体 約N字 ＞ このモデルが読める量 約M字）は根拠として後ろ、という並びにしてある。</div><div class="mt">なお、ルーターが実際に絞ったことをチャットログに出す仕掛けは無い。残るのは失敗時の <code>[router] …</code> の標準出力だけ。</div></td></tr>
      <tr><td>新しく取り込まれた表 / 改名 / 削除</td><td><div class="mt"><b>新規取り込み</b>: <code>profile_db</code> のキャッシュキーは <code>{v:2, mtime, size}</code> なので、DBファイルが変われば次の <code>profile_db</code> で自動的に作り直され、新しい表は即座に <code>build_scope</code> の <code>available</code> に入る。<code>tables_off</code> は除外方式なので、<b>新しい表は全利用者で既定ON</b>。取り込み側は <code>catalog.forget(path)</code> でプロファイルキャッシュと <code>_TEXT_CACHE</code> を捨てる。</div><div class="mt"><code>db_text_cached</code> のキーにDB・meta・プロファイルキャッシュの mtime_ns が入っているので、カタログ本文も自動で作り直される。</div><div class="mt"><b>ビュー</b>: <code>profile_db</code> は <code>type IN (&#x27;table&#x27;,&#x27;view&#x27;)</code> で拾うので、ビューは表と完全に同じ扱い（サイドバーのチェック対象・ルーターの候補・authorizer の allowed）。名前を「まとまり__名前」にすればまとまりにも入る。</div><div class="mt"><b>改名</b> <code>cleanup.rename_table</code>: 実表・カタログ・定期取り込みに加えて、<code>USER_META_DIR/*/prefs.yaml</code> を全走査して <code>tables_off</code> の中の旧名を新名に付け替える（全利用者ぶん）。失敗したら実表とカタログを巻き戻す。戻り値の <code>prefs</code> が書き換えた利用者数。</div><div class="mt"><b>削除</b> <code>POST /api/import/drop-table</code>（<code>admin_required</code>）→ <code>importer.drop_table</code> → <code>cleanup.clean_table</code>。<code>drop_table</code> は <code>sqlite_master</code> を <code>name = ? COLLATE NOCASE</code> で引いて <code>type</code> を見てから <code>DROP VIEW</code> / <code>DROP TABLE</code> を撃ち分け、無ければ 404。BINARY で引くと「見つからない→黙って何もしない」になり、呼び出し元は掃除だけ進めて表は残るのに知識だけ消える、という事故を防いでいる。返すのは実物の綴りで、掃除にはそれを使う。<code>clean_table</code> はカタログ・定期取り込み・（最後の1表なら）まとまりメモまで片づけるが、<b><code>tables_off</code> には触らない</b>。</div></td></tr>
      <tr><td>主なデータ構造</td><td>・scope = [{path: str, alias: str, name: str(DBファイル名), tables: [表名, ...], meta: dict}] … tools/llm がそのまま受け取る形式。build_scope が組み立て、_auto_scope が tables を書き換える<br>・picked（route_tables の戻り） = {DBファイル名: [表名, ...]} または None。内部では {DBファイル名: set(表名)} で持ち、最後に sorted して返す<br>・known（route_tables 内の名前解決表） = {&quot;alias.table&quot; または &quot;table&quot;（すべて lower）: (DBファイル名, 表名)}。曖昧な素の表名は ambiguous に入れて削除し、そのあと alias.table だけ入れ直す<br>・profile_db(path) = {file, key:{v,mtime,size}, generated_at, tables: {表名: {type: &#x27;table&#x27;|&#x27;view&#x27;, columns, fks, row_count, sample_columns, sample_rows, col_stats}}}<br>・prefs.yaml（USER_META_DIR/&lt;利用者&gt;/prefs.yaml） = {model, rag_off, rag_settings, tables_off}。KEYS に無いキーは読み書きとも捨てられる<br>・tables_off = [表名, ...] … 「外した表」の名前だけ（DB名は付かない）<br>・chat[&quot;table_names&quot;] = [&quot;DBファイル名.表名&quot;, ...] … この会話でSQLが触った表。ルーターの選から漏れても残すための控え<br>・meta[&quot;relationships&quot;] = [{from: &#x27;table.col&#x27; | &#x27;alias.table.(c1, c2)&#x27;, to: 同左, cardinality?}]（parse_endpoint_cols が解く）</td></tr>
      <tr><td>定数・しきい値</td><td>・SCOPE_MODE（config.py・env）: auto | router | all。既定 auto。この3つ以外の値は auto に丸められる（config.py の直後の if で強制）<br>・INLINE_LIMIT_MIN = 4_000 / INLINE_LIMIT_MAX = 400_000（core.py の models 相当部）。prompt_inline_limit() は常に INLINE_LIMIT_MAX を返す（管理画面から変えられない安全弁）<br>・CATALOG_CONTEXT_RATIO = 0.5 … モデル文脈のうちカタログに使ってよい割合。残り半分をツール定義・履歴・回答に残す<br>・TOKENS_PER_CHAR_TEXT = 0.55（日本語本文）／ TOKENS_PER_CHAR_JSON = 0.31（ツール定義JSON）。inline_limit_for の割り算に使うのは前者<br>・MODEL_CONTEXT_WINDOWS（config.py）＋ MODEL_CONTEXT_DEFAULT = 128000（env）。当てるのは部分一致で、長い名前から先に見る。管理者の context_overrides が最優先<br>・route_tables の早期リターンしきい値: 表の総数 total &lt;= 8 なら絞らない（全部渡した方が確実、という判断）<br>・route_tables のLLM呼び出し: model=config.OPENAI_MODEL（既定 &quot;gpt-5.6-sol&quot;）、temperature=0、max_tokens=300<br>・route_tables に渡す会話履歴: history[-3:]（呼び出し側は render_log の role=user・kind=text を全部渡す）<br>・expand_tables_by_relations: 1ホップのみ・from→to の向きのみ<br>・MAX_ATTACHED = 10（1SQLで ATTACH できるDB数。narrow_scope / widen_scope の打ち止め）<br>・PROMPT_INLINE_LIMIT_CHARS = 80000（env）… 現在は読むだけで使っていない。実効上限は inline_limit_for が決める</td></tr>
    </tbody></table></div>
    <div class="card__title mt">落とし穴（15件）</div>
    <div class="tablewrap"><table class="data"><thead><tr><th style="width:60px">#</th><th>内容</th></tr></thead><tbody>
      <tr><td class="mono small">01</td><td>route_tables に渡る「直前の質問」の末尾は、今回の質問そのもの。_begin_turn は render_log に今回のユーザー発言を append してから _auto_scope を呼び、_auto_scope は render_log の user/text を全部拾って渡す。route_tables は history[-3:] を『（直前の質問: …）』として並べたあとに『今回の質問: …』を足すので、同じ文が2回入る。実質の過去質問は2件しか効いていない。</td></tr>
      <tr><td class="mono small">02</td><td>route_tables の total（8件しきい値）と known は prof[&quot;tables&quot;] を直接なめており、s[&quot;tables&quot;]（tables_off 適用後）を見ていない。つまり (1) 利用者がほとんどの表を外していても total は104のまま、(2) known には外した表も載るので、LLMが外した表名を書けば解決してしまう。これを救っているのが _auto_scope 側の「off で再フィルタ」で、あれが無いと外した表が復活する。</td></tr>
      <tr><td class="mono small">03</td><td>picked に出てこないDBは、まったく絞られない。_auto_scope は <code>sel = picked.get(s[&quot;name&quot;])</code> で、None のときは s[&quot;tables&quot;] を触らない＝そのDBは全表のまま残る。DB1本の現構成では表面化しないが、複数DBだとルーターが言及しなかったDBが素通りする。</td></tr>
      <tr><td class="mono small">04</td><td>ピン留め（chat[&quot;table_names&quot;]）は現構成では事実上死んでいる。table_names を埋めるループは <code>for name in chat[&quot;db_names&quot;]</code> を回るが、db_names は db.dbs_named_in() が返す『SQLが alias. の形で名指ししたDB』だけ。DBが1つのときシステムプロンプトは「テーブル名はそのまま書く（前に何かを付けて修飾しない）」と指示しているので alias. は書かれず、db_names は空のまま → table_names も空 → 「それをグラフに」のような続き質問でルーターが外した表は戻ってこない。</td></tr>
      <tr><td class="mono small">05</td><td>_persist のコメントに『db_names は …（_auto_scope 参照）』とあるが、いまの _auto_scope は db_names を読まない（build_scope に全DBを渡している）。コメントだけが旧実装のまま残っている。</td></tr>
      <tr><td class="mono small">06</td><td>ビューは profile_db が sqlite_master の type IN (&#x27;table&#x27;,&#x27;view&#x27;) で拾うため、表とまったく同じ粒度でルーターの候補・サイドバーのチェック対象になる。しかし SQLite の authorizer はビュー経由の読み取りを『実体テーブルへの SQLITE_READ』として通知する（arg1=実体テーブル名、第5引数=ビュー名）。allowed にビューだけ入っていて実体テーブルが入っていないと <code>access to base.a is prohibited</code> で落ちる（実測確認済み）。ルーターがビューだけを選んだ場合や、利用者がビューを残して元表を外した場合に起きる。expand_tables_by_relations はカタログの関連しか見ないので、ここは補完されない。</td></tr>
      <tr><td class="mono small">07</td><td>絞られたことをAIに伝える文面は db_text の limited 注記1本しかなく、内容は『※ 利用者がいま対象にしているのは、下に挙げる表だけです…サイドバーの SQLite3 でその表にチェックを入れるよう一言で伝えてください』。ルーターが機械的に絞ったときも同じ文が出るので、AIは利用者のせいにして『サイドバーでチェックを』と案内する。利用者は何も外していないのに、である。</td></tr>
      <tr><td class="mono small">08</td><td>同じ理由で describe_table_text の拒否文も『いまの対象に入っていません。サイドバーの SQLite3 でチェックを入れると使えます。』で固定。ルーター起因の絞り込みでも同じ文言が返る。</td></tr>
      <tr><td class="mono small">09</td><td>チャット画面の警告バナー（models.status の scope.note）は catalog_total_chars() ＝ tables=None の全カタログで判定する。_auto_scope が実際に使うのは tables_off 適用後の inline_length(scope)。よって「表を大量に外したのでルーターは走らないのに、バナーだけは『自動で絞ります』と出続ける」ことが起きる。</td></tr>
      <tr><td class="mono small">10</td><td>表を削除しても tables_off は掃除されない。cleanup.clean_table はカタログ・定期取り込み・まとまりメモは片づけるが prefs.yaml には触らない（改名 rename_table は USER_META_DIR/*/prefs.yaml を全走査して付け替える。非対称）。残骸が消えるのは、その利用者が次にサイドバーのチェックを触ったときだけ（tables_prefs_save が実在する表名だけ残す）。結果、同じ名前で取り込み直すと、以前外していた利用者には最初から外れた状態で現れる。</td></tr>
      <tr><td class="mono small">11</td><td>ルーターのLLMは models.current(g.user)（利用者が選んだモデル）ではなく config.OPENAI_MODEL 固定で呼ばれる。一方、収まるかどうかの判定 inline_limit_for は利用者のモデルで行う。判定するモデルと振り分けるモデルが別物。</td></tr>
      <tr><td class="mono small">12</td><td>SCOPE_MODE の docstring と config の説明には router モードが書かれているが、_auto_scope に <code>== &quot;router&quot;</code> の分岐は無い。all でも auto-fits でもない全部が routing に落ちるので、結果として router は正しく動く（暗黙分岐）。</td></tr>
      <tr><td class="mono small">13</td><td>JSON解析は <code>re.search(r&quot;\[.*?\]&quot;, ..., re.DOTALL)</code> の非貪欲マッチ。<code>[[&quot;a&quot;],[&quot;b&quot;]]</code> のような入れ子を返されると <code>[[&quot;a&quot;]</code> を切り出して json.loads が落ちるが、それも try の中なので None（絞らない）になり、失敗は [router] の print だけで画面には出ない。</td></tr>
      <tr><td class="mono small">14</td><td>off フィルタ後に sel が空になったDBは s[&quot;tables&quot;] を書き換えない（<code>if sel:</code> のガード）ので、そのDBは全表（off適用後）のまま残る。ルーターが外した表しか選ばなかった場合、絞り込みが無効化される。</td></tr>
      <tr><td class="mono small">15</td><td>chat[&quot;table_names&quot;] の形式は「DBファイル名.表名」で、DBファイル名自体が .db を含む。分解は rpartition(&quot;.&quot;)（最後のドット）でなければならない。先頭で割ると 統合 / db.受注__明細 になる。</td></tr>
    </tbody></table></div>
  </div>

  <div class="card mt">
    <div class="card__title" id="impl-sqlguard">5-4. SQL実行の安全機構</div>
    <div class="card__desc">AI（LLM）や画面が組み立てたSQLは、例外なく core.py の <code>run_select</code> を通してだけ実行される。<code>run_select</code> は「文字列としての検証（validate_select）」「読み取り専用ATTACHで作った使い捨て接続（connect_scope + _ro_uri）」「SQLiteのオーソライザ（_make_authorizer）」「progress handler によるタイムアウトと fetchmany による行数上限」の4層で守られており、どの層も単独では抜けられても、上位層が同じ攻撃を別の理由で止めるように重ねてある。加えて、SQLが必要とするDBだけを繋ぐ <code>widen_scope</code> / <code>narrow_scope</code> と、SQLからDB名・表名を当てる正規表現群（<code>\w</code> が Unicode である前提で日本語表名に対応）が周辺にあり、失敗時のメッセージは <code>explain_error</code> がLLMの再試行を導く形に言い換える。書き込み系（取り込み・DROP・CREATE VIEW）はこの経路を通らない別系統である。</div>
    <div class="tablewrap"><table class="data"><thead><tr><th style="width:210px">項目</th><th>内容</th></tr></thead><tbody>
      <tr><td>全体像 — 4層の多層防御</td><td><div class="mt">元 <code>db.py</code> のヘッダコメントが宣言しているとおり、SELECT以外を実行させないために4層を重ねている。</div><div class="tablewrap"><table class="data"><thead><tr><th>層</th><th>実装</th><th>何を止めるか</th><th>抜けたときに次に止める層</th></tr></thead><tbody><tr><td>1. 構文チェック</td><td><code>validate_select</code></td><td>複文・SELECT/WITH以外・書込キーワード</td><td>2, 3</td></tr><tr><td>2. 読み取り専用接続</td><td><code>connect_scope</code> + <code>_ro_uri</code>（<code>?mode=ro</code>）</td><td>実際の書き込み（物理的に不可）</td><td>3</td></tr><tr><td>3. オーソライザ</td><td><code>_make_authorizer</code> + <code>conn.set_authorizer</code></td><td>SELECT/READ/FUNCTION 以外の全アクション、対象外の表の読み取り</td><td>—</td></tr><tr><td>4. タイムアウト</td><td><code>conn.set_progress_handler</code></td><td>暴走クエリ</td><td>—</td></tr></tbody></table></div><div class="mt"><code>run_select</code> の処理順序は次のとおり。</div><pre class="mono small">run_select(sql, scope, max_rows=None, timeout_s=None, params=None):
  1. scope が空 → ValueError（文面はLLM向けに「rows で渡せ」まで書いてある）
  2. safe_sql = validate_select(sql)          # 第1層。失敗は ValueError
  3. max_rows  = max_rows  or config.MAX_RESULT_ROWS   # 2000
     timeout_s = timeout_s or config.QUERY_TIMEOUT_SEC # 10
  4. use = narrow_scope(safe_sql, scope)      # 繋ぐDBを必要分に絞る
  5. allowed = 読んでよい表名の集合 or None    # 下記「allowed の作り方」
  6. conn = connect_scope([(path, alias) for use])     # 第2層。ここで ATTACH
  7. conn.set_authorizer(_make_authorizer(allowed))    # 第3層
  8. start = time.time()
     conn.set_progress_handler(lambda: 1 if time.time()-start &gt; timeout_s else 0, 10000)  # 第4層
  9. cur = conn.execute(safe_sql, params or {})        # 例外は explain_error で言い換え
 10. columns = [d[0] for d in cur.description] if cur.description else []
     rows = cur.fetchmany(max_rows + 1)
     truncated = len(rows) &gt; max_rows
     rows = [tuple(r) for r in rows[:max_rows]]
 11. finally: conn.close()
  → (columns, rows, truncated)</pre><div class="mt">手順6→7の順序は入れ替えられない。<code>connect_scope</code> の中で <code>ATTACH DATABASE</code> を撃つが、<code>_ALLOWED_ACTIONS</code> に <code>SQLITE_ATTACH</code> は入っていないため、先にオーソライザを付けると自分のATTACHが DENY される。接続は1回のSELECTごとに作って <code>finally</code> で閉じる使い捨てで、状態を持ち越さない。</div></td></tr>
      <tr><td>第1層 validate_select — SELECT専用パーサ</td><td><div class="mt"><code>validate_select(sql) -&gt; str</code> は「検査用のコピー」と「実行するSQL」を分けているのが要点。<b>実行するのはコメントを残したままの元のSQL</b>で、コメント除去は検査用コピーにしか使わない。理由はdocstringに書かれているとおり:</div><div class="mt">・<code>SELECT &#x27;2024/*x*/end&#x27;</code> → コメント除去すると <code>&#x27;2024 end&#x27;</code> になり、黙って値が変わる<br>・<code>WHERE note = &#x27;foo -- bar&#x27;</code> → 除去すると引用符が閉じず構文エラーになる</div><div class="mt">検査用コピーの作り方（<b>この順序も逆にできない</b>）:</div><pre class="mono small">cleaned = _trim_tail(sql)                                   # 前後空白 + 末尾の &#x27;;&#x27; 群を除去
probe   = _trim_tail(_strip_sql_comments(_blank_quoted(cleaned)))
         #            (2) コメント除去      (1) 引用符の中身を空に</pre><div class="mt">・<code>_blank_quoted</code> … <code>_QUOTED</code> にマッチした塊を「開始文字＋終了文字」だけに潰す。<code>&#x27;don&#x27;&#x27;t drop it&#x27;</code> → <code>&#x27;&#x27;</code>、<code>&quot;delete&quot;</code> → <code>&quot;&quot;</code>、<code>[delete]</code> → <code>[]</code>、`<code> </code>delete<code> </code><code> → </code> `<code> </code>。<code>&#x27;&#x27;</code> / <code>&quot;&quot;</code> のエスケープも1つの塊として食う。先にこれをやらないと、リテラル中の <code>--</code> をコメント開始と誤認する。<br>・<code>_strip_sql_comments</code> … <code>--</code> 行コメントを行末まで、<code>/* */</code> ブロックコメントを DOTALL で除去。<b>必ず <code>_blank_quoted</code> の後に呼ぶこと</b>とdocstringが明記している。</div><div class="mt">判定は probe に対して行う:</div><div class="tablewrap"><table class="data"><thead><tr><th>条件</th><th>エラー文</th></tr></thead><tbody><tr><td>sql が空・空白のみ</td><td>「SQLが空です。」</td></tr><tr><td>cleaned / probe が空</td><td>「実行可能なSQLがありません。」</td></tr><tr><td>probe に <code>;</code> が残る</td><td>「複数ステートメントは実行できません(SELECT文を1つだけ指定してください)。」</td></tr><tr><td>probe が <code>select</code> / <code>with</code> で始まらない（小文字化して判定）</td><td>「SELECT文(または WITH ... SELECT)のみ実行できます。」</td></tr><tr><td><code>_FORBIDDEN</code> または <code>_REPLACE_INTO</code> にヒット</td><td>「書き込み・DDL系のキーワード &#x27;…&#x27; は使用できません。読み取り専用です。」</td></tr></tbody></table></div><div class="mt"><code>_FORBIDDEN</code> は <code>\b(insert|update|delete|drop|alter|create|truncate|attach|detach|reindex|vacuum|pragma|grant|revoke|begin|commit|rollback|savepoint|merge)\b</code>（IGNORECASE）。<b><code>replace</code> は意図的に入っていない</b>。SQLite の <code>replace(X,Y,Z)</code> は文字列関数で「株式会社」を落とすといった用途でごく普通に使うため、書き込みになる <code>REPLACE INTO</code> の形だけを <code>_REPLACE_INTO</code>（<code>\breplace\s+into\b</code>）で別に見る。</div><div class="mt">実測した挙動（同じロジックを切り出して確認）:</div><div class="tablewrap"><table class="data"><thead><tr><th>SQL</th><th>結果</th><th>理由</th></tr></thead><tbody><tr><td><code>SELECT 1 -- ; DROP TABLE t</code></td><td>通る</td><td>probe ではコメントごと消える。SQLite も同じくコメント扱い</td></tr><tr><td><code>SELECT 1 -- x\n; SELECT 2</code></td><td>弾く</td><td>行コメントは改行で終わるので <code>;</code> が残る</td></tr><tr><td><code>SELECT * FROM &quot;delete&quot;</code> / <code>[delete]</code> / `<code> </code>delete<code> </code>`</td><td>通る</td><td>引用符の中身は空にされてからキーワード検査</td></tr><tr><td><code>SELECT * FROM create_log</code> / <code>受注create</code></td><td>通る</td><td><code>\b</code> 境界に当たらない（<code>_</code> も日本語も <code>\w</code>）</td></tr><tr><td><code>EXPLAIN SELECT 1</code>, <code>EXPLAIN QUERY PLAN …</code>, <code>VALUES(1)</code></td><td>弾く</td><td>select/with で始まらない</td></tr><tr><td><code>SELECT 1 WHERE &#x27;a&#x27; = &#x27;b;c&#x27;</code></td><td>通る</td><td>リテラル中の <code>;</code> は見えない</td></tr></tbody></table></div><div class="mt">返り値は <code>cleaned</code>（末尾 <code>;</code> を落としただけの元SQL）で、これがそのまま <code>conn.execute</code> に渡る。</div></td></tr>
      <tr><td>第2層 接続の作り方 — connect_scope / _ro_uri と URI の依存関係</td><td><pre class="mono small">_ro_uri(path) = Path(path).resolve().as_uri() + &quot;?mode=ro&quot;
              例: file:///C:/…/data/%E7%B5%B1%E5%90%88.db?mode=ro

connect_scope(paths_aliases):
    if len(paths_aliases) &gt; MAX_ATTACHED: raise ValueError(親切な説明つき)
    conn = sqlite3.connect(&quot;file::memory:&quot;, uri=True)     # main は空のインメモリ
    for path, alias in paths_aliases:
        conn.execute(f&#x27;ATTACH DATABASE ? AS &quot;{alias}&quot;&#x27;, (_ro_uri(path),))
    return conn</pre><div class="mt">設計の勘所:</div><div class="mt">・<b>main を実データにしない。</b> 空の <code>:memory:</code> を main に置き、実DBはすべて ATTACH。こうすると「main への書き込み」が起きても実ファイルには届かない。<br>・<b><code>?mode=ro</code> が効くのは main を <code>uri=True</code> で開いているから。</b> SQLite は ATTACH のURIファイル名解釈を「main接続が <code>SQLITE_OPEN_URI</code> で開かれているか」で決める。実測: <code>sqlite3.connect(&quot;:memory:&quot;)</code>（uri なし）に同じURIを ATTACH すると <code>OperationalError: unable to open database: file:///…?mode=ro</code> で失敗する。つまり <code>uri=True</code> を外すと黙って書けるようになるのではなく、接続自体が作れなくなって気づける。ro が効いていることも実測済み（<code>INSERT</code> → <code>attempt to write a readonly database</code>）。<br>・<b>alias は識別子として直接埋め込む。</b> <code>f&#x27;ATTACH DATABASE ? AS &quot;{alias}&quot;&#x27;</code> の alias は <code>alias_for</code> が <code>_ALIAS_BAD = re.compile(r&quot;[^\w]&quot;, re.UNICODE)</code> で記号・空白を <code>_</code> に潰した後の値なので識別子として安全（コメントにもそう書いてある）。パスの方はプレースホルダで渡す。<br>・<b><code>alias_for</code> は日本語を潰さない。</b> <code>[^\w]</code> を UNICODE で当てるので <code>売上.db</code> → <code>売上</code>。ASCIIだけに絞ると「店舗マスタ」が <code>_____</code> になり、複数の日本語DBを区別できなくなるため。先頭が数字なら <code>db_</code> を前置、<code>main</code>/<code>temp</code> は <code>_db</code> を後置（<code>_RESERVED_ALIASES</code>）。<code>aliases_for</code> は複数ファイルで衝突したら <code>_2</code>, <code>_3</code> と連番を振る。<br>・<code>path_for(name)</code> は <code>data/</code> に名前を連結せず、<code>list_db_files()</code> の列挙結果からファイル名一致で引く。<code>../</code> が来ても <code>data/</code> の外に出られない。</div></td></tr>
      <tr><td>第3層 set_authorizer — _make_authorizer と allowed</td><td><pre class="mono small">_ALLOWED_ACTIONS = {sqlite3.SQLITE_SELECT(21), sqlite3.SQLITE_READ(20), sqlite3.SQLITE_FUNCTION(31)}
+ SQLITE_RECURSIVE(33) があれば追加   # 環境によって存在しないため hasattr で確認

_make_authorizer(allowed):
    def _authorizer(action, arg1, arg2, db_name, trigger):
        if action not in _ALLOWED_ACTIONS:          return SQLITE_DENY
        if allowed is not None and action == SQLITE_READ and arg1:
            if str(arg1) not in allowed and not str(arg1).startswith(&quot;sqlite_&quot;):
                                                    return SQLITE_DENY
        return SQLITE_OK</pre><div class="mt"><b>5引数の意味</b>（SQLiteのauthorizerコールバックそのまま。実測で確認済み）:</div><div class="tablewrap"><table class="data"><thead><tr><th>引数</th><th>SQLITE_READ のとき</th><th>SQLITE_SELECT のとき</th></tr></thead><tbody><tr><td><code>action</code></td><td>20</td><td>21</td></tr><tr><td><code>arg1</code></td><td>テーブル名（またはビュー名）</td><td>None</td></tr><tr><td><code>arg2</code></td><td>列名</td><td>None</td></tr><tr><td><code>db_name</code></td><td>そのオブジェクトが居るDB名（<code>main</code> / ATTACHしたalias）</td><td>None</td></tr><tr><td><code>trigger</code></td><td>このアクセスを引き起こしたビュー名／トリガ名（直接の参照なら None）</td><td>ビュー名</td></tr></tbody></table></div><div class="mt"><code>_make_authorizer</code> は <code>db_name</code> と <code>trigger</code> を受け取るだけで使っていない。</div><div class="mt"><b>なぜここに置くのか</b>（docstring）: 「プロンプトから消すだけでは、AIが名前を覚えている・推測できる場合に読めてしまうため、最後の関門はデータ層に置く」。サイドバーで対象から外した表（<code>excluded_tables</code> = ユーザー設定 <code>tables_off</code>）と、表ルーターが絞った表が、そのまま SQLite が読む一歩手前で効く。</div><div class="mt"><b>allowed の作り方</b>（<code>run_select</code> 内）:</div><pre class="mono small">allowed: set | None = set()
for s_ in use:                       # use = narrow_scope の結果
    if s_.get(&quot;tables&quot;):
        allowed |= set(s_[&quot;tables&quot;])
    else:
        allowed = None               # ← 1つでも tables を持たない要素があれば
        break                        #    表単位の制限を「全部」やめる</pre><div class="mt">つまり allowed は <b>表名だけのフラットな集合</b>（DB名で修飾しない）で、<b>要素が1つでも tables を持たなければ None（＝表の制限なし）</b>になる。</div><div class="mt">allowed の供給元:</div><div class="tablewrap"><table class="data"><thead><tr><th>経路</th><th>tables の中身</th></tr></thead><tbody><tr><td><code>build_scope(selection)</code> → <code>_auto_scope</code></td><td>プロファイルの全表から、ユーザー除外（<code>tables_off</code>）を引き、表ルーター（<code>llm.route_tables</code> + <code>expand_tables_by_relations</code> + 会話中にSQLが触った表のピン留め）が絞った結果</td></tr><tr><td><code>widen_scope</code> が追加した要素</td><td><b>None</b></td></tr><tr><td><code>_sql_scope</code>（カタログの検証系）、<code>_view_run</code></td><td>キー自体が無い → <b>None</b></td></tr></tbody></table></div><div class="mt">DENY されたときの例外は実測で <code>sqlite3.DatabaseError: access to &lt;表&gt;.&lt;列&gt; is prohibited</code>（<code>OperationalError</code> ではない）。<code>run_select</code> の <code>except sqlite3.Error</code> は拾えるので、<code>explain_error</code> を通って <code>OperationalError</code> として再送出される。ただし <code>explain_error</code> にこの文面のパターンは無いので、英語のまま LLM に返る。</div><div class="mt"><code>sqlite_</code> で始まる名前は常に許す。<code>sqlite_master</code> を読むSELECTは通る（実測）。ただし <code>PRAGMA</code> は <code>_FORBIDDEN</code> と <code>_ALLOWED_ACTIONS</code>（<code>SQLITE_PRAGMA</code> を含まない）の両方で止まる。<code>SQLITE_FUNCTION</code> は関数名（<code>arg2</code>）で絞っていないが、この接続には <code>create_function</code> で何も登録していないため、SQLite組み込み関数だけが呼べる。</div></td></tr>
      <tr><td>第4層 タイムアウトと行数上限</td><td><div class="mt"><b>タイムアウト</b></div><pre class="mono small">start = time.time()
conn.set_progress_handler(lambda: 1 if (time.time() - start) &gt; timeout_s else 0, 10000)</pre><div class="mt">・10,000 VM命令ごとにコールバックが呼ばれ、非0を返すと SQLite が中断する。中断時の例外は実測で <code>sqlite3.OperationalError: interrupted</code>。<br>・<code>start</code> は execute の直前に一度だけ取り、リセットしない。1回の <code>run_select</code> 全体（execute + fetchmany）で <code>timeout_s</code> 秒。<br>・<code>timeout_s = timeout_s or config.QUERY_TIMEOUT_SEC</code> なので既定10秒。<code>0</code> を渡しても falsy で10秒に落ちる（無制限にはできない）。<br>・カタログのプロファイリングは別系統で、<code>_make_timeout(conn, seconds)</code> が <code>box[&quot;t&quot;]</code> を持ち、クエリごとに <code>reset()</code> を呼ぶ方式（100,000命令ごと、<code>config.PROFILE_TIMEOUT_SEC = 30</code>）。</div><div class="mt"><b>行数上限と truncated</b></div><pre class="mono small">rows = cur.fetchmany(max_rows + 1)      # 1行多く取る
truncated = len(rows) &gt; max_rows        # 多く取れたら「まだある」
rows = [tuple(r) for r in rows[:max_rows]]</pre><div class="mt">上限より1行多く取って、はみ出したかどうかで <code>truncated</code> を決める。<code>COUNT(*)</code> を撃たずに判定できるが、「本当は何行か」は分からない。それを補うのが <code>_total_rows(sql, scope)</code> で、<code>SELECT COUNT(*) FROM (元のSQL)</code> を <code>max_rows=1</code> で撃ち直す。重くて失敗し得るので、例外は握って <code>None</code> を返す（数えられなくても本体は返す）。</div><div class="mt"><code>truncated</code> の伝播:</div><div class="mt">・<code>fetch</code> が <code>(columns, rows, truncated, result_id, total_rows)</code> を返す。<code>total_rows</code> は切り詰めが起きたときだけ入る。<br>・<code>source_note(row_count, truncated, total, cap)</code> が LLM 向けの警告文を作る（「上限 2,000 行で切り詰めました。実際は N 行あります。…GROUP BY で集計するか、条件を絞って取り直してください。」）。<br>・<code>render_source_note(truncated, total)</code> が画面向けの印を作る。docstring に経緯が書かれている: 以前は警告が <code>llm_content</code> にしか入っておらず、表だけ「（上限で切り詰め）」が出て、グラフとレポートは断り書きなしに一部だけを描いていた。</div><div class="mt">道具ごとに上限が違う。画面・グラフは <code>config.MAX_RESULT_ROWS</code>（2,000）、ファイル出力は <code>config.EXPORT_MAX_ROWS</code>（既定1,000,000、Excelは <code>min(EXPORT_MAX_ROWS, 1_048_575)</code>）。<code>fetch</code> は result_id 経由でも、預けた結果が2,000行で切れていて、かつ今回の <code>max_rows</code> の方が大きければ、預けたときのSQLで取り直す（「集計→CSVに」でCSVだけ2,000行で欠ける事故を防ぐ）。</div></td></tr>
      <tr><td>スコープの伸縮 — widen_scope / narrow_scope / MAX_ATTACHED</td><td><div class="mt"><code>MAX_ATTACHED = 10</code>。SQLiteが同時にATTACHできる数の上限そのもの（実測: 11個目で <code>too many attached databases - max 10</code>。main の <code>:memory:</code> はこの数に入らない）。</div><div class="mt"><b><code>widen_scope(sql, scope)</code>（呼び出し側が run_select の前に呼ぶ）</b></div><div class="mt">選ばれていなくても、SQLが <code>alias.</code> の形で名指ししているDBを足す。ユーザー定義ツールや例文は作った人がDBを意識せずに書くため、選択中のDBだけを繋ぐと正しいSQLが <code>no such table</code> で落ちる。docstringは「DBの選択はもともと『見る範囲を絞る』ためのものでアクセス制御ではない（README参照）」と根拠を書いている。<code>len(out) &gt;= MAX_ATTACHED</code> で打ち止め（超えた分は元のエラーで気づける）。<b>足す要素は <code>&quot;tables&quot;: None</code></b>。</div><div class="mt"><b><code>narrow_scope(sql, scope)</code>（<code>run_select</code> が内部で呼ぶ）</b></div><pre class="mono small">if len(scope) &lt;= 1: return scope          # 単一DB環境では即 return
picked = []
(1) alias. の形で名指しされているDB
(2) 修飾なしの表名が一致するDB（(1) と混在したSQLでも取りこぼさない）
return picked[:MAX_ATTACHED] if picked else scope</pre><div class="mt">「選択中のDBを全部つなぐ必要はない」ため。docstringに経緯があり、11個以上選ぶと2表だけの問い合わせも実行できなくなっていた。<b>どちらでも判断できないときは全部を返す</b> — 勝手に減らして <code>no such table</code> にするより、元の分かりやすいエラー（<code>connect_scope</code> の「1つのSQLで扱えるDBは10個までです…『DB名.テーブル名』の形で書けば…」）の方がよい、という判断。</div><div class="mt">呼び出し順は <b>widen（呼び出し側）→ narrow（run_select 内）</b>。widen が足した <code>tables: None</code> の要素は、SQLがその alias を名指ししているからこそ足されたので narrow でも必ず残る → <code>allowed</code> が None になる。</div></td></tr>
      <tr><td>SQLから名前を当てる正規表現群と Unicode 対応</td><td><div class="mt">「このSQLはどのDB／どの表を触っているか」を当てる処理が、目的別に4つある。<b>すべて <code>\w</code>（Python3ではUnicode既定）に依存している</b>。</div><div class="tablewrap"><table class="data"><thead><tr><th>関数</th><th>正規表現</th><th>用途</th></tr></thead><tbody><tr><td><code>dbs_named_in(sql)</code></td><td><code>(?&lt;![\w.&quot;])</code> + alias + <code>\s*\.</code></td><td>全DBファイルを走査。SQLが名指ししているDBファイル名</td></tr><tr><td><code>widen_scope</code> / <code>narrow_scope</code>(1)</td><td>同上</td><td>繋ぐDBの決定</td></tr><tr><td><code>narrow_scope</code>(2) / <code>dbs_in_sql</code>(2)</td><td><code>(?&lt;![\w.&quot;])</code> + 表名 + <code>(?![\w&quot;])</code></td><td>修飾なしの表名からDBを当てる</td></tr><tr><td><code>dbs_in_sql(sql, scope)</code></td><td>上2つを <code>re.search().start()</code> で位置つき</td><td>例文の保存先DBを決める。alias が1つでも当たればその順、無ければ表名で最後の手段</td></tr><tr><td><code>tables_in_sql(sql, scope, limit=6)</code></td><td><code>sql.replace(&#x27;&quot;&#x27;,&#x27;&#x27;)</code> してから <code>(?&lt;![\w.])</code>…<code>(?![\w])</code></td><td>チャットのSQLプレビューからカタログの該当表へのリンク（最大6件）</td></tr></tbody></table></div><div class="mt"><b>なぜ <code>\w</code> でなければならないか（実測で確認）</b></div><div class="mt">・<code>SELECT * FROM 売上受注明細</code> に対して表名 <code>受注</code> を探す:<br>・<code>(?&lt;![\w.&quot;])受注(?![\w&quot;])</code>（Unicode <code>\w</code>）→ <b>当たらない</b>（<code>売</code>も<code>明</code>も語構成文字なので境界にならない）。正しい。<br>・<code>(?&lt;![A-Za-z0-9_.&quot;])受注(?![A-Za-z0-9_&quot;])</code>（ASCII限定）→ <b>当たってしまう</b>。存在しない参照を検出したことになる。<br>・同じ理由で <code>品質__defects</code> の中の <code>defects</code> にも当たらない（<code>_</code> が <code>\w</code>）。表名＝接頭辞付きの1本（<code>まとまり__名前</code>）という命名規約と噛み合っている。</div><div class="mt"><b>関数ごとに規則が違う点</b>（重要）</div><div class="mt">・<code>narrow_scope</code> / <code>dbs_in_sql</code> の lookbehind は <code>(?&lt;![\w.&quot;])</code> で <code>&quot;</code> を含むため、<b><code>&quot;品質__defects&quot;</code> と引用符付きで書かれた表名には当たらない</b>（実測）。<br>・<code>tables_in_sql</code> は先に <code>sql.replace(&#x27;&quot;&#x27;,&#x27;&#x27;)</code> で引用符を落としてから照合するので当たる。<br>・カタログ側の別実装（用語検証の参照表抽出）は <code>(?&lt;![\w.&quot;])&quot;?</code> + 名前 + <code>&quot;?(?![\w])</code> と、引用符を任意で許す3つ目の書き方をしている。<br>・一方で健全性チェックが組み立てるSQLは <code>_q(alias, table)</code> = <code>alias.&quot;表名&quot;</code> と必ず引用符を付ける。単一DB（<code>narrow_scope</code> が <code>len(scope) &lt;= 1</code> で即 return）だから問題になっていない。</div><div class="mt"><code>_ALIAS_BAD = re.compile(r&quot;[^\w]&quot;, re.UNICODE)</code> も同じ前提。SQLiteは非ASCIIの識別子をクオート無しで扱えるので、<code>売上.db</code> は <code>売上.受注</code> と書ける。</div></td></tr>
      <tr><td>explain_error — エラー文の言い換え</td><td><div class="mt"><code>run_select</code> は <code>conn.execute</code> の <code>sqlite3.Error</code> を捕まえ、<code>raise sqlite3.OperationalError(explain_error(e)) from e</code> で投げ直す。目的は「何が悪いか」だけでなく「代わりに何を使うか」までLLMに返すこと。</div><pre class="mono small">explain_error(e):
  msg = str(e)
  1) r&quot;no such function:\s*([A-Za-z_0-9]+)&quot; にヒット
       → _MISSING_FUNC_HINTS[fn.lower()] があれば
         「{msg} … SQLite には {fn}() がありません。SQLで書き直そうとせず、{hint} を使ってください。」
       → 無ければ「標準のSQLite関数だけで書き直すか、専用の分析ツールを使ってください。」
  2) r&quot;no such column:\s*(\S+)&quot; にヒット
       → 「列名が違います。describe_table でテーブルの列を確認してから書き直してください（推測で列名を作らないこと）。」
  3) &quot;syntax error&quot; を含む
       → 「SQLite で解釈できない書き方です。ウィンドウ関数の一部・WITHIN GROUP・PIVOT などは使えません。
           集計や統計は専用ツール（pivot_table / analyze_stats）に任せてください。」
  4) それ以外 → msg をそのまま</pre><div class="mt"><code>_MISSING_FUNC_HINTS</code> の意図はコメントに明記されている: 「エラーメッセージにこれを添えないと、LLMは同じ関数で何度も書き直す」。中身は他方言→SQLite/専用ツールの対応表（<code>stddev</code>/<code>median</code>/<code>percentile_cont</code> → <code>analyze_stats(method=&#x27;describe&#x27;)</code>、<code>corr</code> → <code>analyze_stats(method=&#x27;correlation&#x27;)</code>、<code>date_trunc</code> → <code>strftime</code>、<code>concat</code> → <code>||</code>、<code>listagg</code>/<code>string_agg</code> → <code>group_concat</code>、<code>top</code> → <code>LIMIT</code> など）。</div><div class="mt">この言い換えは <code>_run_sql_query</code> などのハンドラで <code>_err(f&quot;SQL実行エラー: {e}&quot;)</code> に包まれ、<code>llm_content</code> として次のエージェントステップでLLMに読ませる。<code>validate_select</code> の <code>ValueError</code> は try の外で投がるので <code>explain_error</code> を通らず、日本語のガード文言がそのままLLMに届く。</div></td></tr>
      <tr><td>run_select を通らない経路</td><td><div class="mt">「SQLは必ず run_select を通る」は AI と画面の<b>読み取り</b>に限った話。以下は別系統。</div><div class="tablewrap"><table class="data"><thead><tr><th>経路</th><th>接続</th><th>ガード</th></tr></thead><tbody><tr><td>取り込み（CSV/Excel → 表）</td><td><code>sqlite3.connect(db_path)</code>（書込可）</td><td>管理者専用 + アプリ側のロジック</td></tr><tr><td><code>drop_table</code></td><td>同上。<code>sqlite_master</code> を <code>WHERE name = ? COLLATE NOCASE</code> で引いて種類（table/view）を判定してから `DROP {VIEW</td><td>TABLE} IF EXISTS`</td><td>管理者専用。<code>data/</code> 外は拒否</td></tr><tr><td><code>create_view</code></td><td>同上。<code>CREATE VIEW {name} AS {sql}</code> と <b>SQLをf-stringで直接連結</b></td><td><b><code>_view_check_sql</code> → <code>db.validate_select</code> が唯一の関門</b>。docstringに「SQLは SELECT専用ガードを通ったものだけを渡すこと」と明記</td></tr><tr><td>プロファイリング</td><td><code>connect_ro</code>（<code>?mode=ro</code> の単一DB）</td><td>読み取り専用。<code>PRAGMA table_info</code> を撃つのでオーソライザは付けない</td></tr><tr><td><code>fetch</code> の result_id 経路</td><td>接続しない</td><td><code>results.get(scope, rid)</code> が <code>scope_key</code>（<b>pathのみ、tablesは見ない</b>）の一致だけ確認</td></tr></tbody></table></div><div class="mt">つまり <code>validate_select</code> は <code>run_select</code> 専用の関数ではない。<code>create_view</code> の文字列連結の安全性がここに乗っているので、緩めるとDDL注入になる。</div><div class="mt">なお <code>custom_tools.validate_custom_tool</code>（ユーザー定義ツールの保存時検証）は <code>validate_select</code> を呼ばない。名前・説明・パラメータ型・<code>:name</code> とパラメータ定義の対応（<code>bind_names</code> / <code>_BIND_RE = (?&lt;!:):([A-Za-z_][A-Za-z0-9_]*)</code>）・出力形式しか見ず、SELECT縛りがかかるのは実行時（<code>_run_custom</code> → <code>run_select</code>）だけ。ツール編集は <code>admin_required</code> なので運用上の穴ではないが、多層防御の枚数はここだけ1枚少ない。</div><div class="mt">バインド変数は <code>conn.execute(safe_sql, params or {})</code> の名前付きプレースホルダで渡る。<code>render_sql</code> は「UIのプレビュー用。実行時は :name のままバインドするので置換はしない」とdocstringが明言しており、プレビュー文字列と実行SQLで値の埋め込み方が違うことはない。</div></td></tr>
      <tr><td>セルフテスト</td><td><div class="mt"><code>python core.py selftest</code> → <code>_sql_guard_selftest()</code>。2部構成。</div><div class="mt">・<code>validate_select</code> に ok_cases 8本 / ng_cases 9本を通す。ok側は「文字列リテラルの中のキーワードや記号で弾かないこと」の回帰テスト（<code>replace(name,&#x27;株式会社&#x27;,&#x27;&#x27;)</code>、<code>x=&#x27;delete me&#x27;</code>、<code>note=&#x27;;&#x27;</code>、<code>s=&#x27;don&#x27;&#x27;t drop it&#x27;</code>、<code>&quot;delete&quot;</code>）。ng側は <code>DELETE</code>/<code>DROP</code>/<code>UPDATE</code>/<code>SELECT 1; DELETE FROM t</code>/<code>INSERT</code>/<code>PRAGMA</code>/<code>ATTACH</code>/<code>REPLACE INTO</code>/<code>SELECT * FROM t WHERE x=&#x27;a&#x27;; DROP TABLE t</code>。<br>・tempfile に a.db / b.db を作り、<code>run_select(&quot;SELECT t.v, u.w FROM a.t t JOIN b.u u ON t.id=u.id&quot;)</code> でATTACH横断JOINが通ることを確認。続いて <code>connect_scope</code> の接続に直接 <code>INSERT</code> を撃ち、<code>sqlite3.OperationalError</code> になれば読み取り専用が効いていると判定（例外が出なければ <code>!! 読み取り専用が効いていない</code> を出して終了コード1）。</div><div class="mt">ガードのすり抜けは例外ではなく <code>!! ガードすり抜け:</code> の出力になる（終了コードには反映されない）点に注意。</div></td></tr>
      <tr><td>主なデータ構造</td><td>・scope = [{&quot;path&quot;: str, &quot;alias&quot;: str, &quot;name&quot;: str, &quot;tables&quot;: list[str] | None, &quot;meta&quot;: dict}] — path と alias 以外は経路によって欠ける。tables が無い/None だと表単位の制限が外れる<br>・run_select 戻り値 = (columns: list[str], rows: list[tuple], truncated: bool)<br>・allowed = set[str] | None — 表名だけのフラットな集合（DB名で修飾しない）。None は「表の制限なし」<br>・authorizer コールバック = (action: int, arg1: str|None, arg2: str|None, db_name: str|None, trigger: str|None) -&gt; SQLITE_OK | SQLITE_DENY<br>・paths_aliases = [(path: str|Path, alias: str), ...] — connect_scope の引数<br>・fetch 戻り値 = (columns, rows, truncated, result_id: str, total_rows: int|None)<br>・results のエントリ = {&quot;scope&quot;: scope_key, &quot;columns&quot;: list, &quot;rows&quot;: list[tuple], &quot;truncated&quot;: bool, &quot;sql&quot;: str|None, &quot;norm_sql&quot;: str, &quot;turn&quot;: str, &quot;label&quot;: str|None}<br>・scope_key(scope) = &quot;|&quot;.join(sorted(各要素の path)) — tables は含まない<br>・dbs_in_sql 戻り値 = SQLに出てくる順に並べ替えた scope の部分列<br>・tables_in_sql 戻り値 = [{&quot;db&quot;: DBファイル名, &quot;table&quot;: 表名}]（最大 limit=6 件）<br>・custom tool = {&quot;name&quot;, &quot;description&quot;, &quot;sql&quot;, &quot;parameters&quot;: [{&quot;name&quot;,&quot;type&quot;,&quot;description&quot;,&quot;required&quot;}], &quot;render&quot;: table|chart|chart_dual|excel|csv|none, &quot;chart&quot;: {...}, &quot;enabled&quot;}</td></tr>
      <tr><td>定数・しきい値</td><td>・MAX_ATTACHED = 10（core.py, db層）— SQLiteの実上限と一致。実測で11個目が <code>too many attached databases - max 10</code>。main の :memory: は数に入らない<br>・config.MAX_RESULT_ROWS = 2000 — run_select の既定 max_rows、および results に預ける行数の上限<br>・config.QUERY_TIMEOUT_SEC = 10 — run_select の既定タイムアウト（秒）<br>・progress handler の命令間隔 = 10000（run_select）／ 100000（catalog の _make_timeout）<br>・config.SAMPLE_ROWS_FOR_LLM = 40 — LLMに返すサンプル行数<br>・config.EXPORT_MAX_ROWS = 1_000_000（env で変更可）。Excel は min(EXPORT_MAX_ROWS, 1_048_575) に丸める<br>・config.PROFILE_TIMEOUT_SEC = 30 — プロファイリング中の1クエリ<br>・_ALLOWED_ACTIONS = {SQLITE_SELECT=21, SQLITE_READ=20, SQLITE_FUNCTION=31} + SQLITE_RECURSIVE=33（hasattr で存在確認して追加）<br>・_FORBIDDEN のキーワード19語: insert update delete drop alter create truncate attach detach reindex vacuum pragma grant revoke begin commit rollback savepoint merge（replace は意図的に不在）<br>・VIEW_PREVIEW_ROWS = 20 — ビュー定義SQLのプレビュー行数<br>・results.MAX_ENTRIES = 40 / results.MAX_CELLS = 400_000 — 結果置き場の上限（古い順に破棄）<br>・_HEAVY_ROWS = 200_000 — これを超える表では健全性チェックの COUNT(DISTINCT) を省く<br>・検証環境: Python 3.12.10 / SQLite 3.49.1（数学関数コンパイル込み）</td></tr>
    </tbody></table></div>
    <div class="card__title mt">落とし穴（18件）</div>
    <div class="tablewrap"><table class="data"><thead><tr><th style="width:60px">#</th><th>内容</th></tr></thead><tbody>
      <tr><td class="mono small">01</td><td>allowed は「scope の要素が1つでも tables を持たなければ None」。widen_scope が足す要素は tables=None なので、SQLが別DBを alias. の形で名指しした瞬間に、表単位の制限が<b>全DB分まとめて</b>外れる。カタログ画面の検証系（_sql_scope / _view_run）が作る scope には tables キー自体が無いので、こちらも常に制限なし（管理者専用なので設計としては筋が通っている）</td></tr>
      <tr><td class="mono small">02</td><td>allowed は表名だけの集合で、authorizer が受け取る db_name を使っていない。同じ名前の表が複数DBにあると、選ばれていない側のDBの表も読めてしまう。単一DB（data/統合.db）運用ではまず表面化しないが、regex群と違ってDB名で分離していないことは実装を読まないと分からない</td></tr>
      <tr><td class="mono small">03</td><td>ビューを読むと SQLITE_READ が「ビュー名」と「実体の表名」の<b>両方</b>で飛ぶ（実測。実体側は第5引数 trigger にビュー名が入る）。profile_db は sqlite_master を type IN (&#x27;table&#x27;,&#x27;view&#x27;) で引いていて view も tables に入るので、ビューだけ許可して土台の表を許可しないと <code>access to X.Y is prohibited</code> で落ちる</td></tr>
      <tr><td class="mono small">04</td><td>表ルーター（_auto_scope → llm.route_tables）が絞った表が、そのまま SQLite層の allowed になる。ルーターが外した表をAIやユーザー定義ツールのSQLが触ると「列が違う」ではなく英語の prohibited エラーで落ちる。プロンプトの絞り込みとアクセス制御が同じ変数に同居している</td></tr>
      <tr><td class="mono small">05</td><td>オーソライザの DENY は sqlite3.DatabaseError（OperationalError ではない）で、文面は英語の <code>access to &lt;表&gt;.&lt;列&gt; is prohibited</code>。explain_error にこのパターンは無いので、そのままLLMとユーザーに出る</td></tr>
      <tr><td class="mono small">06</td><td><code>?mode=ro</code> が効くのは main を <code>sqlite3.connect(&quot;file::memory:&quot;, uri=True)</code> で開いているから（SQLiteはATTACHのURI解釈をmain接続のフラグで決める）。uri=True を落とすとATTACH自体が <code>unable to open database: file:///…?mode=ro</code> で失敗する（実測）。この2行は離れて見えるが結合している</td></tr>
      <tr><td class="mono small">07</td><td>connect_scope（ATTACH）→ set_authorizer の順序は入れ替え不可。_ALLOWED_ACTIONS に SQLITE_ATTACH が無いので、先にオーソライザを付けると自分のATTACHが DENY される</td></tr>
      <tr><td class="mono small">08</td><td>検査は「引用符の中身を空に → コメント除去 → 末尾の ; を落とす」の順でなければならず、逆にすると &#x27;foo -- bar&#x27; のリテラルが壊れる。かつ<b>実行するのはコメントを残した元のSQL</b>（除去版を実行すると &#x27;2024/*x*/end&#x27; が黙って &#x27;2024 end&#x27; に変わる）</td></tr>
      <tr><td class="mono small">09</td><td>validate_select をすり抜けても conn.execute 自体が複文を拒否する（実測: ProgrammingError &quot;You can only execute one statement at a time.&quot;）。<code>;</code> チェックは二重装備の1枚目</td></tr>
      <tr><td class="mono small">10</td><td>narrow_scope / dbs_in_sql の表名照合は lookbehind に <code>&quot;</code> を含むため、<code>&quot;表名&quot;</code> と引用符付きで書かれた表名には当たらない。tables_in_sql だけは先に <code>&quot;</code> を除去してから照合するので当たる。「SQLから表を当てる」処理が引用符の扱いだけ3通りある</td></tr>
      <tr><td class="mono small">11</td><td>表名の正規表現を ASCII限定クラスに書き換えてはいけない。<code>SELECT * FROM 売上受注明細</code> に対して表名 <code>受注</code> を探すと、Unicode <code>\w</code> では当たらない（正しい）が ASCII限定クラスでは当たる（誤検出）。実測で確認済み</td></tr>
      <tr><td class="mono small">12</td><td>timeout_s / max_rows に 0 を渡すと <code>or</code> で既定値（10秒 / 2000行）に落ちる。0 は falsy なので「無制限」を表現できない</td></tr>
      <tr><td class="mono small">13</td><td>progress handler による中断は fetchmany 中にも起こり得るが、fetchmany は try/except sqlite3.Error の<b>外</b>にある。この場合 explain_error を通らず生の <code>interrupted</code> が出る</td></tr>
      <tr><td class="mono small">14</td><td>_MISSING_FUNC_HINTS の sqrt / power は、この環境（SQLite 3.49.1、数学関数コンパイル込み）では実在するため永久に発火しない。<code>ifnull_</code> は綴りに <code>_</code> が付いていて no such function の関数名と一致しない、事実上の死んだ項目</td></tr>
      <tr><td class="mono small">15</td><td>EXPLAIN / EXPLAIN QUERY PLAN も VALUES(...) も弾かれる（select/with で始まらないため）。読み取り専用でも実行計画は見せない</td></tr>
      <tr><td class="mono small">16</td><td>result_id 経路（fetch）は run_select をまったく通らない。results.scope_key は path だけで tables を見ないので、表の絞り込みは「一度取り出して預けた結果」には効かない。さらに _store はプロセス全体で共有されており、ユーザー単位で分かれていない</td></tr>
      <tr><td class="mono small">17</td><td>validate_select は run_select 専用ではない。importer.create_view が <code>CREATE VIEW {name} AS {sql}</code> とf-stringで連結する際の唯一の関門でもあるので、ここを緩めるとDDL注入になる</td></tr>
      <tr><td class="mono small">18</td><td>custom_tools.validate_custom_tool は validate_select を呼ばない。ユーザー定義ツールのSELECT縛りは実行時の run_select だけで担保されている</td></tr>
    </tbody></table></div>
  </div>

  <div class="card mt">
    <div class="card__title" id="impl-tools">5-5. ツール基盤</div>
    <div class="card__desc">AIに渡す「関数の宣言（JSON Schema）」と「実処理（ハンドラ）」を別々に持ち、両者を名前で突き合わせて実行する層。宣言は BUILTIN_TOOLS（静的リテラル37個＋グラフ6個の機械生成＋ナレッジ1個、引退1個を除いて計43個）に集約し、build_tools が権限・無効化・説明上書き・動的なナレッジ宣言・ユーザー定義ツールを毎ステップ合成して LLM に渡す。実行は dispatch が引数JSONの解析から検算の割り込みまで一本道で通し、戻り値は必ず {ok, llm_content, render} の3キー（検算が引っかかったときだけ verify_alerts が生える）。ツールが取った表は results の置き場に預けて result_id を返し、後続のツールが同じSQLを書き直さずに使い回せるようにしている。</div>
    <div class="tablewrap"><table class="data"><thead><tr><th style="width:210px">項目</th><th>内容</th></tr></thead><tbody>
      <tr><td>全体像 — 4つの表と1つの入口</td><td><div class="mt">ツール基盤は「名前をキーにした4つの表」だけでできている。ツールを1つ足すときに触るのはこの4つ。</div><div class="tablewrap"><table class="data"><thead><tr><th>表</th><th>中身</th><th>誰が作るか</th></tr></thead><tbody><tr><td><code>BUILTIN_TOOLS</code></td><td>宣言（JSON Schema）のリスト</td><td>元 <code>tools/schemas.py</code> のリテラル ＋ <code>_chart_tools()</code> ＋ <code>KNOWLEDGE_TOOLS</code></td></tr><tr><td><code>_HANDLERS</code></td><td>ツール名 → 実処理の関数</td><td>各モジュールの <code>HANDLERS_*</code> を <code>_MODULES</code> 順に合成</td></tr><tr><td><code>SQL_TOOLS</code></td><td>SQLを引数で受け取るツール名の集合</td><td>各モジュールの <code>SQL_TOOLS_*</code> の和</td></tr><tr><td><code>ADMIN_TOOLS</code></td><td>管理者にだけ渡すツール名の集合</td><td>各モジュールの <code>ADMIN_TOOLS_*</code> の和</td></tr></tbody></table></div><div class="mt">合成の元になるのが <code>_MODULES</code>。<code>(HANDLERS_*, SQL_TOOLS_*, ADMIN_TOOLS_*)</code> の3つ組を、統合前のファイル順（query → stats → reports → mail → business → files → usage → knowledge）で並べたタプルで、コメントに「名前が重なったときにどちらが残るかを変えないため、順序は動かさないこと」と明記されている（辞書内包なので<b>後勝ち</b>）。</div><pre class="mono small">_HANDLERS   = {name: fn for m in _MODULES for name, fn in m[0].items()}
SQL_TOOLS   = {name for m in _MODULES for name in m[1]}
ADMIN_TOOLS = {name for m in _MODULES for name in m[2]}</pre><div class="mt">実測値:</div><div class="mt">・<code>_HANDLERS</code> は44個（query 19 / stats 10 / reports 3 / mail 2 / business 7 / files 1 / usage 1 / knowledge 1）。<br>・<code>BUILTIN_TOOLS</code> は43個。差の1個は引退した <code>plot_chart</code>（宣言だけ消して実処理は残してある）。<br>・<code>SQL_TOOLS</code> は25個（query 11 = 固定5 ＋ <code>_CHART_TOOLS</code> 6、stats 8、business 6）。うち宣言があるのは24個。<br>・<code>ADMIN_TOOLS</code> は <code>{&quot;explore_import_files&quot;, &quot;analyze_usage&quot;}</code> の2個だけ。</div><div class="mt"><code>SQL_TOOLS</code> に入れない判断にも理由がある。<code>data_quality</code> は引数でSQLを受け取らず自分でDBを見に行くので対象外。<code>scenario_analysis</code> と <code>monte_carlo_simulation</code> はSQLが任意なので外してある。<code>analyze_usage</code> と <code>search_knowledge_base</code> は材料がDBではない（履歴ファイル／ナレッジベース）。</div></td></tr>
      <tr><td>BUILTIN_TOOLS の組み立て — import時に3段階で書き換わる</td><td><div class="mt"><code>BUILTIN_TOOLS</code> という名前は import 中に3回意味が変わる。読む順序を間違えると何が入っているか分からなくなる。</div><div class="mt"><b>第1段: リテラルの構築</b>元 <code>tools/schemas.py</code> の巨大なリスト。静的に書かれたツールが37個、その途中に <code>*_chart_tools()</code> が展開されて用途別グラフ6個（<code>plot_comparison</code> / <code>plot_trend</code> / <code>plot_composition</code> / <code>plot_distribution</code> / <code>plot_relationship</code> / <code>plot_kpi</code>）が入る。グラフツールの宣言は <code>_CHART_TOOLS</code>（名前 → 分類・説明・使う指定・必須）と <code>_CHART_ARGS</code>（引数名 → スキーマ断片）から機械生成される。同じ引数の説明を6回書かないため。</div><div class="mt"><b>第2段: <code>_allow_result_id(BUILTIN_TOOLS)</code></b>宣言の木を再帰で全走査し、<code>properties</code> に <code>&quot;sql&quot;</code> があって <code>&quot;result_id&quot;</code> が無いノードすべてに次を足す。</div><div class="mt">・<code>result_id</code>（<code>_RESULT_ID</code>）… 前のツールが取ったデータを指す<br>・<code>rows</code>（<code>_INLINE_ROWS</code>）… 表そのものを直接渡す（DBを介さないデータ）<br>・<code>columns</code>（<code>_INLINE_COLUMNS</code>）… ただし <b><code>columns</code> が既にあるノードは上書きしない</b></div><div class="mt">さらに、そのノードの <code>required</code> から <code>&quot;sql&quot;</code> を取り除く。SQLの代わりに result_id や rows で来てもよくなるため。</div><div class="mt">再帰なので、トップレベルだけでなく <code>export_excel</code> の <code>sheets.items</code>（<code>properties</code> に <code>sql</code> がある）や、レポートの節のような入れ子にも同じ処理が効く。docstring に「1つずつ手で書き足すと必ず抜けるので、木をたどって機械的に付ける」とある。</div><div class="mt"><code>columns</code> を上書きしない理由はコメントに書かれている。<code>pivot_table</code> の <code>columns</code> は「列に展開する1列名」で<b>文字列</b>であり、ここで配列宣言に置き換えると後段の <code>_coerce_lists</code> が文字列を要素1つの配列に直してしまい、pandas 側で <code>unhashable type: &#x27;list&#x27;</code> になる。</div><div class="mt"><b>第3段: 引退フィルタ</b></div><pre class="mono small">_RETIRED = {&quot;plot_chart&quot;}
BUILTIN_TOOLS = [t for t in BUILTIN_TOOLS if t[&quot;function&quot;][&quot;name&quot;] not in _RETIRED]</pre><div class="mt"><code>plot_chart</code> は用途別グラフツールで完全に置き換えられる。同じことが2通りできるとAIが毎回迷い、宣言の文字数も倍かかるため宣言だけ落とす。実処理（<code>_plot_chart</code>）は <code>_HANDLERS</code> に残してあるので、過去の会話やユーザー定義の上書きは壊れない。</div><div class="mt"><b>第4段: ナレッジ宣言の合流（元 <code>tools/__init__.py</code> の冒頭）</b></div><pre class="mono small">BUILTIN_TOOLS = BUILTIN_TOOLS + KNOWLEDGE_TOOLS</pre><div class="mt">ここで合流させておく理由もコメントにある。<code>_missing_required</code> と <code>_coerce_lists</code> はどちらも <code>BUILTIN_TOOLS</code> から表を作るので、ここに入れておけば必須引数の検査と配列引数の直しがそのまま効く。ただし<b>AIに実際に渡す宣言は <code>build_tools</code> が組み立て直す</b>（<code>_DYNAMIC_TOOLS</code> を参照）。</div><div class="mt"><b>第5段: 派生表の凍結</b><code>BUILTIN_TOOLS</code> が確定した直後に、import時に一度だけ2つの表を作る。</div><div class="mt">・<code>_REQUIRED = _required_params()</code> … <code>{ツール名: (required の引数名, ...)}</code>。第2段で <code>sql</code> が抜かれた後の姿。<br>・<code>_LIST_PARAMS = _string_list_params()</code> … <code>{ツール名: {&quot;文字列の配列&quot;型の引数名, ...}}</code>。判定は <code>type == &quot;array&quot;</code> かつ <code>items.type == &quot;string&quot;</code>。<b>トップレベルの <code>properties</code> しか見ない</b>。</div></td></tr>
      <tr><td>build_tools — AIに渡す一覧の合成</td><td><div class="mt"><code>build_tools(entries, admin=False)</code> が、その1回の呼び出しでAIに渡す宣言リストを作る。<code>entries</code> は scope（<code>build_scope</code> が作る <code>{path, alias, name, tables, meta}</code> のリスト）がそのまま渡ってくる。scope に <code>meta</code>（.meta.yaml の中身）が入っているので、上書き設定をここから引ける。</div><div class="mt">処理順:</div><div class="mt">・<code>ov = custom_tools.builtin_overrides(entries)</code> — 全DBの <code>.meta.yaml</code> の <code>builtin_tools:</code> を合成。<b>無効化はどれか1つのDBで無効なら無効（安全側）／説明は最初に見つかったものを採用</b>。<br>・<code>BUILTIN_TOOLS</code> を1つずつ見る:<br>・<code>name in _DYNAMIC_TOOLS</code>（= <code>{&quot;search_knowledge_base&quot;}</code>）→ <b>スキップ</b>。下で組み立て直すため。<br>・<code>name in ADMIN_TOOLS and not admin</code> → スキップ。「渡さなければAIはその存在を知らないので、呼ばれること自体が起きない」。<br>・<code>ov[name][&quot;enabled&quot;] is False</code> → スキップ。<br>・<code>ov[name][&quot;description&quot;]</code> があれば <code>function.description</code> を差し替えた<b>浅いコピー</b>を作る（原本は壊さない）。<br>・<code>name in SQL_TOOLS</code> なら <code>_with_explanation(t)</code> を、そうでなければ <code>t</code> をそのまま追加。<br>・<code>knowledge_tool_schemas()</code> の結果を追加（0件か1件）。ここにも <code>enabled</code> / <code>description</code> の上書きを適用する。<br>・<code>custom_tools.collect_everywhere(entries)</code> のツールのうち、<code>validate_custom_tool(tool, set())</code> が空リストを返した（＝不備なし）ものだけ <code>to_schema()</code> して追加。</div><div class="mt"><b><code>knowledge_tool_schemas()</code></b> は <code>KNOWLEDGE_TOOLS[0]</code> を <code>json.loads(json.dumps(...))</code> で深くコピーしてから、</div><div class="mt">・<code>function.description</code> の末尾に「登録されているナレッジベース:\n- 名前: 説明」を連結<br>・<code>parameters.properties.knowledge_bases.items.enum</code> に名前のリストを設定</div><div class="mt">する。材料は <code>rag_targets()</code>（= 登録済みで有効なKBから、その利用者が除外したものを引いたもの）。<b>1件も無ければ空リストを返す＝ツールを渡さない</b>。存在しない情報源を探させても往復と費用が増えるだけ、という判断。名前と説明がAIの唯一の選択材料なので、ここが検索の当たり外れを最も左右する、とdocstringにある。</div><div class="mt"><code>build_tools</code> は <code>_advance</code> / <code>_stream_advance</code> のループ内で<b>毎ステップ呼ばれる</b>（<code>llm.chat(chat[&quot;messages&quot;], tools.build_tools(scope, admin=_is_admin()), ...)</code>）。同じ関数はシステムプロンプトのツール一覧（<code>build_system_prompt</code>）とトークン見積り（<code>tool_chars</code>）でも使われるので、AIが読む一覧・プロンプトの説明文・見積りの3者が必ず一致する。</div></td></tr>
      <tr><td>_with_explanation — SQLの日本語解説の注入</td><td><div class="mt">SQLを組み立てるツールの宣言に、共通の <code>explanation</code> 引数を後から差し込む。定義は1か所（<code>_EXPLANATION_PARAM</code>）にあり、<code>build_tools</code> が <code>name in SQL_TOOLS</code> の判定で配る。SQLツールを増やしても自動で付く。</div><div class="mt"><code>_EXPLANATION_PARAM</code> の説明文が要求しているのは「3〜5行」「SQLを読めない人にも分かる言葉で」「どの表を使うか → どうつないだか（結合の条件と、なぜその条件か）→ どう絞ったか・集計したか → 1行が何を表すか の順」「INNER JOIN のような構文用語を並べるのではなく、何をしているかを説明する」。</div><pre class="mono small">def _with_explanation(t):
    props に &quot;explanation&quot; が既にあれば t をそのまま返す（冪等）
    それ以外は {**t, &quot;function&quot;: {**fn, &quot;parameters&quot;: {
        **params,
        &quot;properties&quot;: {**props, &quot;explanation&quot;: _EXPLANATION_PARAM},
        &quot;required&quot;: list(params.get(&quot;required&quot;) or ()),   # 必須には足さない
    }}}</pre><div class="mt">必須にしない理由はコメントにある。「解説が無くてもSQLは実行できるべきで、必須にすると解説を書き損ねただけで質問全体が止まる」。</div><div class="mt">受け取り側は <code>_call_previews</code>。<b>実行前</b>のプレビューカードを作る所で、<code>c[&quot;name&quot;] in tools.SQL_TOOLS and &quot;sql&quot; in args</code> のときに <code>{&quot;kind&quot;: &quot;sql&quot;, &quot;tool&quot;, &quot;sql&quot;, &quot;purpose&quot;, &quot;explanation&quot;: args.get(&quot;explanation&quot;, &quot;&quot;), &quot;question&quot;, &quot;tables&quot;}</code> を積む。画面ではSQLの下に <code>white-space:pre-wrap</code> で出る。AIはSQLと同じツール呼び出しの中で解説も書くので、<b>追加のAI呼び出しは発生しない</b>。</div><div class="mt">ユーザー定義ツールのプレビューは別の分岐で、<code>explanation</code> に<b>登録時の <code>description</code></b> を入れる。SQLは人が登録したものなので、AIの解説ではなく登録者の説明を出す。</div><div class="mt"><code>explanation</code> が付く実数は24個。<code>SQL_TOOLS</code> は25個あるが、<code>plot_chart</code> は <code>BUILTIN_TOOLS</code> にいないので <code>build_tools</code> のループに乗らない（help.html の「24種」と一致する）。</div></td></tr>
      <tr><td>dispatch — 実行の全段</td><td><div class="mt"><code>dispatch(name, arguments_json, scope, entries=None, admin=False) -&gt; dict</code>。呼び出し元は <code>_execute</code> の1か所だけで、<code>tools.dispatch(c[&quot;name&quot;], c[&quot;arguments&quot;], scope, scope, admin=_is_admin())</code> と <b>scope を entries にも渡している</b>。</div><div class="mt">段は7つ。</div><div class="mt"><b>1. 引数JSONの解析</b><code>json.loads(arguments_json) if arguments_json else {}</code>。<code>JSONDecodeError</code> は <code>_err(&quot;ツール引数のJSON解析に失敗しました: ...&quot;)</code> にして返す。ここで例外を投げないので、モデルが壊れたJSONを吐いても会話は続く。</div><div class="mt"><b>2. 管理者判定</b></div><pre class="mono small">if name in ADMIN_TOOLS and not admin:
    return _err(f&quot;&#x27;{name}&#x27; は管理者だけが使えます。&quot;)</pre><div class="mt">コメントは「渡していないツールを名指しで呼ばれても実行しない（守りは2箇所で持つ）」。<code>build_tools</code> で渡さないのが1枚目、ここが2枚目。過去の会話の履歴からツール名を拾って呼ぶ経路があるため、宣言を渡さないだけでは足りない。</div><div class="mt"><b>3. <code>_coerce_lists(name, args)</code></b><code>_LIST_PARAMS[name]</code> に載っている引数に<b>素の文字列</b>が来ていたら、<code>[v.strip()]</code> に直す（空文字なら <code>[]</code>）。<b>args を破壊的に書き換えて同じ辞書を返す</b>。</div><div class="mt">理由がdocstringに書かれている。LLMは列名が1つのとき <code>index=&quot;地域&quot;</code> のように文字列で渡してくることがあり、そのまま渡すと文字列が1文字ずつに散って「『地』という列がありません」という人には意味の分からないエラーになる（日本語の列名だと必ずこうなる）。ここで直せば同じ形の引数13個すべてに効く。</div><div class="mt"><b>4. <code>_missing_required(name, args)</code></b><code>_REQUIRED[name]</code> を回して、<code>_HAS_DEFAULT</code>（<code>{&quot;title&quot;, &quot;filename&quot;, &quot;chart_type&quot;, &quot;purpose&quot;}</code>）に載っている引数はスキップ。残りのうち <code>None</code> または空の入れ物（<code>str/list/dict/tuple</code> で <code>len == 0</code>）だったものを集める。<b><code>0</code> や <code>False</code> は正しい値なので空とみなさない</b>。</div><div class="mt">1つでもあれば実行せず、次の文面で差し戻す。</div><pre class="mono small">&#x27;{name}&#x27; の必須の引数が指定されていません: {不足を「、」で連結}。
（{name} の必須引数は {_REQUIRED[name] を「、」で連結}）
この引数を入れて呼び直してください。列名が分からないときは、
先に describe_table か run_sql_query で列を確認すること。</pre><div class="mt">docstring の理由: 「LLMは required を落とすことがある。そのまま実処理へ渡すと pandas の &quot;&#x27;[None] not in index&#x27;&quot; のような内部エラーになって返る。これでは何を直せばよいか分からず、同じ呼び出しを繰り返して打ち切られる」。</div><div class="mt"><b>5. <code>_gather_sqls(args, scope, sqls)</code></b>引数の木を再帰でたどり、実行されるSQLを全部拾う。</div><div class="mt">・<code>k == &quot;sql&quot;</code> かつ非空文字列 → <code>acc.append(v)</code><br>・<code>k == &quot;result_id&quot;</code> かつ非空文字列 → <code>_results.get(scope, v)</code> を引いて、<code>entry[&quot;sql&quot;]</code> があれば append<br>・それ以外 → 値へ再帰（list も辿る）</div><div class="mt">レポートの節・Excelのシートのように入れ子の中にあるSQLも拾える。<b>ハンドラ実行の前</b>に走る。</div><div class="mt"><b>6. ハンドラ</b></div><pre class="mono small">handler = _HANDLERS.get(name)
if handler:
    try:    return _attach_verification(handler(args, scope), sqls, scope)
    except Exception as e:  return _err(f&quot;ツール &#x27;{name}&#x27; の実行でエラー: {e}&quot;)</pre><div class="mt"><code>except Exception</code> で全部捕まえる。コメントは「ツールの例外でアプリを落とさない」。</div><div class="mt">ハンドラが無ければユーザー定義ツールを探す:</div><pre class="mono small">tool = next((t for t in custom_tools.collect_everywhere(entries or []) if t.get(&quot;name&quot;) == name), None)
if tool is None:
    return {&quot;ok&quot;: False, &quot;llm_content&quot;: _json({&quot;error&quot;: f&quot;未知のツール: {name}&quot;}), &quot;render&quot;: None}
sqls.append(render_sql(tool))
return _attach_verification(_run_custom(tool, args, scope), sqls, scope)</pre><div class="mt"><b>組み込みが先に引かれる</b>ので、同名があれば組み込みが勝つ。未知ツールだけは <code>_err</code> を使わず手書きの辞書を返し、<code>render</code> を <code>None</code> にしている（画面にエラーカードを出さない）。</div><div class="mt"><b>7. <code>_attach_verification(res, sqls, scope)</code></b><code>res[&quot;ok&quot;]</code> が偽か <code>sqls</code> が空なら何もしない。そうでなければ <code>verify.alerts_for(sqls, scope)</code> を呼び、返ってきた不一致を <code>res[&quot;verify_alerts&quot;]</code> に積む。<b>検証自体の失敗では回答を止めない</b>（<code>except Exception</code> で <code>print</code> して <code>res</code> をそのまま返す）。</div><div class="mt"><code>alerts_for</code> は集めたSQLを実行しない。<code>tables_in()</code> でSQLに出てくる表名を拾い、その表に関係する検算ルールだけを走らせる。だからユーザー定義ツールの <code>:name</code> が残ったままのSQLを渡しても害はない。</div><div class="mt">呼び出し側（<code>_execute</code>）の扱い:</div><div class="mt">・<code>_fresh_alerts</code> でこの会話にまだ出していないものだけに絞る（キーは <code>verify||owner||name||SQL指紋||データの版</code>）<br>・<code>_merge_alerts</code> で <code>llm_content</code> のJSONに <code>verification_warnings</code> を差し込む（JSONとして読めなければ末尾に「【検算の不一致】」を連結）<br>・<code>verify.render_item(a)</code> を <code>render_log</code> に積む</div></td></tr>
      <tr><td>results — result_id の預かり所とスコープ照合</td><td><div class="mt">元 <code>tools/results.py</code>。ツールが取った表を短いあいだ覚えておき、名前（<code>result_id</code>）で指せるようにする置き場。</div><div class="mt"><b>なぜあるか</b>: 「集計 → グラフ → レポート」と進むとき、以前は各ツールが自分でSQLを実行していたので1つの問いに同じSQLが3回走り、往復の上限（<code>config.MAX_AGENT_STEPS</code> = 10）もそのぶん無駄に消えていた。副産物として、表とグラフが必ず同じデータを見る（実行し直す方式では、その間にデータが入れ替わると数字がずれ得た）。</div><div class="mt"><b>置き方</b>:</div><div class="mt">・プロセス内の <code>OrderedDict</code> 1つ（<code>_store</code>）。ワーカーは1つで運用する前提。<br>・<code>MAX_ENTRIES = 40</code> / <code>MAX_CELLS = 400_000</code>（行×列の合計）。<br>・<code>_evict()</code> はまず件数超過ぶんを古い順（<code>popitem(last=False)</code>）に捨て、次に総セル数が上限を超えているあいだ古い順に捨てる。ただし <b><code>len(_store) &gt; 1</code> の条件があるので、1件だけは上限を超えていても残る</b>。</div><div class="mt"><b>エントリの形</b>:</div><pre class="mono small">{&quot;scope&quot;: scope_key(scope), &quot;columns&quot;: [...], &quot;rows&quot;: [tuple, ...],
 &quot;truncated&quot;: bool, &quot;sql&quot;: str|None, &quot;norm_sql&quot;: str, &quot;turn&quot;: str, &quot;label&quot;: str|None}</pre><div class="mt"><code>scope_key</code> は <code>&quot;|&quot;.join(sorted(path))</code>。<code>normalize_sql</code> は空白と改行だけを潰す（<b>大文字小文字は揃えない</b> — <code>&#x27;A装置&#x27;</code> と <code>&#x27;a装置&#x27;</code> の違いが意味を持つため）。</div><div class="mt"><b>取り出し</b>: <code>get(scope, rid)</code> は <code>entry[&quot;scope&quot;] != scope_key(scope)</code> なら <code>None</code>。一致すれば <code>move_to_end(rid)</code> して LRU の新しい側へ移す。docstring は「IDを当てずっぽうで指されても、選んでいないDBの中身は出さない」。</div><div class="mt"><b>ターン（質問の区切り）</b>: <code>_turn_local</code>（<code>threading.local</code>）に <code>turn</code> を持つ。<code>_begin_turn</code> が <code>results.new_turn()</code> で <code>&quot;t_&quot; + uuid4().hex[:8]</code> を発行し、ストリーミングでは応答を流す側が別スレッドになるため <code>results.set_turn(turn_id)</code> で引き継ぐ。引き継がないと同じSQLが2回実行される。</div><div class="mt"><b><code>find_by_sql(scope, sql)</code></b>: 同じ<b>質問</b>・同じ<b>DBの組み合わせ</b>・同じ<b>正規化SQL</b> の3つが揃うエントリを新しい方から探す。<code>turn</code> が空（起動時の点検など質問の外）なら使い回さない。LLMには result_id を渡すよう指示しているが指示は強制力を持たない（gpt-4o-mini で頻発）ので、<code>fetch()</code> がここで機械的に止める。ヒットすると <code>[results] 同じSQLなので実行し直しません（r_xxxxxxxx を使い回します）</code> を print する。</div><div class="mt"><b>入口は <code>fetch(spec, scope, label=None, max_rows=None)</code></b>。判定順:</div><div class="mt">・<code>spec[&quot;rows&quot;] is not None</code> かつ（<code>rows</code> が真 <b>または</b> <code>sql</code>/<code>result_id</code> がどちらも空）→ <code>_inline_table()</code>。<b><code>rows: []</code> と <code>sql</code> が同時に来たらSQLを採る</b>。LLMは引数の雛形ごと <code>rows:[]</code> を付けてくることがあり、0行の表として返すと「データがあるのに無い」と答えてしまう（実測: COUNTが常に0行）。<br>・<code>result_id</code> が無ければ <code>find_by_sql</code> で補う。<br>・<code>result_id</code> があれば <code>results.get</code>。無ければ <code>AnalysisError(&quot;result_id &#x27;...&#x27; のデータが見つかりません。古くなって捨てられたか、別の会話の結果です。sql を指定して取り直してください。&quot;)</code>。<br>・預かりが切り詰め済みで、呼び出し側がもっと大きな <code>max_rows</code> を求めていて、元のSQLがあるなら<b>SQLで取り直す</b>（「集計→CSVに」でCSVだけ2,000行で欠ける事故を防ぐ）。<br>・どちらも無ければ <code>AnalysisError(&quot;sql と result_id のどちらも指定されていません。...&quot;)</code>。<br>・SQL実行の道: <code>db.widen_scope(sql, scope)</code> で必要なDBを繋いでから <code>db.run_select</code>。預けるのは <code>rows[:config.MAX_RESULT_ROWS]</code>（100万行をそのまま預けると1つで <code>MAX_CELLS</code> を食い潰すため）。</div><div class="mt">戻り値は <code>(columns, rows, truncated, result_id, total_rows)</code>。<code>total_rows</code> は切り詰めが起きたときだけ <code>_total_rows()</code> で数え直した本当の件数（重いSQLでは黙って諦めて <code>None</code>）。</div><div class="mt">分析ツールの結果表も預ける。<code>_report_result</code> は <code>scope is not None and rows</code> のとき各表に <code>result_id</code> を付けるので、統計の出力をそのままグラフやExcelに回せる。</div></td></tr>
      <tr><td>render と llm_content の使い分け</td><td><div class="mt">dispatch の戻り値は3キー。</div><pre class="mono small">{
  &quot;ok&quot;: bool,
  &quot;llm_content&quot;: str,     # LLMへ返すテキスト(JSON)。トークン節約のため要約。
  &quot;render&quot;: dict | None,  # UI描画用アイテム(app側が kind を見て解釈)
}</pre><div class="mt"><code>_execute</code> での扱いが対称になっている。</div><div class="mt">・<code>llm_content</code> → <code>chat[&quot;messages&quot;].append({&quot;role&quot;: &quot;tool&quot;, &quot;tool_call_id&quot;: c[&quot;id&quot;], &quot;content&quot;: content})</code><br>・<code>render</code> → 真なら <code>chat[&quot;render_log&quot;].append(dict(res[&quot;render&quot;]))</code></div><div class="mt"><b>作り分けの原則</b>は「AI向けは要約、画面向けは全行」。</div><div class="tablewrap"><table class="data"><thead><tr><th>ツール</th><th>llm_content</th><th>render</th></tr></thead><tbody><tr><td><code>run_sql_query</code></td><td><code>columns</code> / <code>row_count</code> / <b>先頭 <code>SAMPLE_ROWS_FOR_LLM</code>=40行</b> / <code>result_id</code> / <code>note</code> / <code>source_note</code> / <code>example_registered</code></td><td><code>kind: table</code> に<b>全行</b>（最大2,000行）</td></tr><tr><td><code>plot_chart</code> 系</td><td><code>status: &quot;chart_rendered&quot;</code> / <code>chart_type</code> / <code>columns</code> / <code>row_count</code> / <code>result_id</code> — <b>行データを入れない</b></td><td><code>kind: chart</code> に全行</td></tr><tr><td>分析系（<code>_report_result</code>）</td><td><code>notes</code> 全文 ＋ 各表の先頭40行 ＋ <code>meta</code>。表ごとに <code>result_id</code></td><td><code>kind: report</code> に表を丸ごと</td></tr><tr><td>ファイル出力</td><td><code>status: &quot;file_ready&quot;</code> / <code>filename</code> / <code>columns</code> / <code>row_count</code>。<b>バイト列は渡さない</b></td><td><code>kind: file</code> に <code>data</code>（bytes）と <code>sheets</code></td></tr><tr><td><code>describe_table</code></td><td><b>JSONではなく素のテキスト</b>（<code>catalog.describe_table_text</code> の戻り）</td><td><code>None</code></td></tr><tr><td>エラー（<code>_err</code>）</td><td><code>{&quot;error&quot;: message}</code></td><td><code>kind: error</code> の1枚カード</td></tr></tbody></table></div><div class="mt">グラフの行データをAI側に入れないのは、AIには「描いた」という事実と <code>result_id</code> があれば足りるため。逆に <code>notes</code>（所見）は AI に読ませたいので全文渡す。</div><div class="mt"><b>画面への最後の変換</b>は <code>render_item_for_web</code>。<code>data</code> と <code>sheets</code> を除いた全キーを <code>jsonable()</code>（NaN/inf を <code>None</code> に潰す）で通し、</div><div class="mt">・<code>chart</code> / <code>chart_dual</code> → plotly の figure JSON にして <code>kind</code> を <code>&quot;chart&quot;</code> に統一。描画に失敗したら <code>kind: &quot;error&quot;</code> に差し替える<br>・<code>report_doc</code> → 節ごとの <code>chart</code> を figure に変換<br>・<code>file</code> → <code>sheets</code> を先頭20行＋総数だけのプレビューに縮める</div><div class="mt">さらに <code>_web_log</code> が、<code>item[&quot;data&quot;]</code> を持つアイテムを <code>_fs_put</code> でサーバに預けて <code>w[&quot;url&quot;] = &quot;/api/file/&lt;token&gt;&quot;</code> に差し替え、<code>kind == &quot;sql&quot;</code> のアイテムに <code>TOOL_LABELS</code> から日本語ラベル（<code>run_sql_query</code> → 「SQL実行 (SELECT)」など）を付ける。</div><div class="mt"><b>切り詰めの表示</b>は llm_content と render の両方に入れる。<code>source_note()</code> が AI向け（<code>source_row_count</code> / <code>source_truncated</code> / <code>source_total_rows</code> / <code>warning</code>）、<code>render_source_note()</code> が画面向け（<code>truncated</code> / <code>source_total_rows</code>）。docstring に、長らく <code>llm_content</code> にしか入っておらず、2,000行を超える明細から作った散布図やピボットが断り書きなしに一部だけを描いていた、と経緯が書かれている。</div></td></tr>
      <tr><td>ユーザー定義ツールの合流と _run_custom</td><td><div class="mt">ユーザー定義ツールは「名前 + 説明 + パラメータ定義 + SQLテンプレート + 出力形式」だけで表す。Pythonコードは書かせない。SQLは <code>db.run_select</code> の SELECT専用ガードを通し、パラメータは SQLite のバインド変数として渡すのでSQLインジェクションは起こらない。保存先は各DBの <code>.meta.yaml</code> の <code>tools:</code>。</div><div class="mt"><b>収集</b> — <code>collect_everywhere(selected=None)</code>:</div><div class="mt">・<code>db.list_db_files()</code> 順に全DBの <code>.meta.yaml</code> を読む。<b>置き場のDBを選んでいなくても拾う</b>（ツールは作るときにDBを意識させないため、組み込みと同じ扱いにする）。<br>・<code>enabled is False</code> は除外。<b>名前の重複は先に見つかった方が勝つ</b>（<code>seen</code> セット）。<br>・<code>selected</code> を渡すと、そのSQLが名指ししている DB が1つも選ばれていないツールを外す。どのDBも名指ししていないSQL（<code>dbs_named_in</code> が空）は置き場のDBのものとして扱う。<br>・各ツールに <code>owner</code>（alias）と <code>owner_file</code>（ファイル名）を足して返す。編集画面が保存先を知るため。</div><div class="mt"><b>検証</b> — <code>validate_custom_tool(tool, existing_names)</code> は問題点のリストを返す（<b>空なら妥当</b>）。<code>build_tools</code> は <code>if not validate_custom_tool(tool, set())</code> で判定するので、二重否定に注意。<code>existing_names</code> に <code>set()</code> を渡しているのは、重複が <code>collect_everywhere</code> の <code>seen</code> で既に落ちているため。検査項目:</div><div class="mt">・名前: <code>^[A-Za-z][A-Za-z0-9_]{0,47}$</code>、<code>builtin_names()</code> と重複しない、<code>existing_names</code> と重複しない<br>・説明・SQL: 必須<br>・パラメータ: 名前が <code>^[A-Za-z_][A-Za-z0-9_]*$</code>、重複なし、型が <code>(&quot;string&quot;,&quot;integer&quot;,&quot;number&quot;,&quot;boolean&quot;)</code> のいずれか<br>・<b>SQL中の <code>:名前</code> とパラメータ定義の対応を双方向で</b>（<code>bind_names()</code> は <code>(?&lt;!:):([A-Za-z_][A-Za-z0-9_]*)</code> で拾う。<code>::</code> は型キャストなので除外）<br>・出力形式が <code>(&quot;table&quot;,&quot;chart&quot;,&quot;chart_dual&quot;,&quot;excel&quot;,&quot;csv&quot;,&quot;none&quot;)</code> のいずれか、<code>chart</code> なら種別ごとの必須項目、<code>chart_dual</code> なら <code>x</code> / <code>bar_y</code> / <code>line_y</code></div><div class="mt"><code>builtin_names()</code> は <code>from tools import BUILTIN_TOOLS</code> を<b>遅延 import</b> して名前集合を作る。以前は4つだけ列挙していて、漏れた名前（<code>forecast</code> など）でツールを作れてしまい、AIに同じ名前の関数が2つ渡って実行されるのは組み込み側だけ、という不整合が起きていた、とコメントにある。</div><div class="mt"><b>実行</b> — <code>_run_custom(tool, args, scope)</code>:</div><div class="mt">・<code>render_sql(tool)</code> = <code>tool[&quot;sql&quot;].strip()</code>。<b><code>:name</code> は置換しない</b>（実行時にバインドするため）。<br>・<code>coerce_params(tool, args)</code> で定義された型に寄せる。<code>None</code> はそのまま <code>None</code>（＝NULLバインド）。変換できなければ <code>ValueError</code> → <code>_err</code>。<br>・<code>db.widen_scope(sql, scope)</code> で SQL が名指ししているDBを繋ぐ。<b>以降の預け先もこの広げた scope</b>。<br>・行数上限: <code>render</code> が <code>excel</code> / <code>csv</code> なら <code>min(config.EXPORT_MAX_ROWS, 1_048_575)</code>（Excelのシート上限）、それ以外は <code>None</code>（＝<code>db.run_select</code> の既定 = <code>MAX_RESULT_ROWS</code> 2,000）。<br>・<code>rows[:MAX_RESULT_ROWS]</code> を <code>_results.put(..., label=f&quot;{name}（ユーザー定義ツール）&quot;)</code> して <code>result_id</code> を返す。コメントに経緯がある — 組み込みツールは前から返しているのにユーザー定義だけ返しておらず、「このツールの結果をグラフにして」と言われてもAIには渡す手段が無かった（SQLはAIに見せていないので取り直せない）。<br>・<code>render</code> の値で分岐: <code>none</code> → <code>render: None</code> / <code>excel</code>・<code>csv</code> → ファイル生成して <code>kind: file</code> / <code>chart</code> → <code>chart.x</code> と <code>chart.y</code> が結果の列にあるか確かめてから <code>kind: chart</code> / <code>chart_dual</code> → <code>x</code> + <code>bar_y</code> + <code>line_y</code> を確かめて <code>kind: chart_dual</code> / それ以外 → <code>kind: table</code>。</div><div class="mt"><b>組み込みの上書き</b> — <code>builtin_overrides(entries)</code> は <code>.meta.yaml</code> の <code>builtin_tools:</code> を合成する。<code>{&quot;ツール名&quot;: {&quot;enabled&quot;: False}}</code> と <code>{&quot;ツール名&quot;: {&quot;description&quot;: &quot;...&quot;}}</code> の2種類だけ。無効化は OR（どれか1つで無効なら無効）、説明は最初に見つかったもの。</div></td></tr>
      <tr><td>主なデータ構造</td><td>・ツール宣言 t = {&quot;type&quot;: &quot;function&quot;, &quot;function&quot;: {&quot;name&quot;: str, &quot;description&quot;: str, &quot;parameters&quot;: {&quot;type&quot;: &quot;object&quot;, &quot;properties&quot;: {引数名: スキーマ}, &quot;required&quot;: [引数名]}}}<br>・dispatch の戻り値 = {&quot;ok&quot;: bool, &quot;llm_content&quot;: str, &quot;render&quot;: dict|None} ＋ 検算が引っかかったときだけ &quot;verify_alerts&quot;: [alert]<br>・render アイテム = {&quot;role&quot;: &quot;assistant&quot;, &quot;kind&quot;: &quot;table&quot;|&quot;chart&quot;|&quot;chart_dual&quot;|&quot;report&quot;|&quot;report_doc&quot;|&quot;file&quot;|&quot;error&quot;|&quot;sources&quot;|&quot;sql&quot;|&quot;text&quot;|&quot;glossary_term&quot;|&quot;mail_draft&quot;, ...kind ごとの追加キー}<br>・scope = [{&quot;path&quot;: str, &quot;alias&quot;: str, &quot;name&quot;: str（DBファイル名）, &quot;tables&quot;: [表名], &quot;meta&quot;: .meta.yaml の中身}]（build_scope が作る。dispatch には entries としても同じものが渡る）<br>・_MODULES = ((HANDLERS_query, SQL_TOOLS_query, ()), (HANDLERS_stats, ...), ... (HANDLERS_knowledge, SQL_TOOLS_knowledge, ADMIN_TOOLS_knowledge)) — (実処理dict, SQLを受け取る名前set, 管理者専用名前set) の3つ組<br>・_REQUIRED = {ツール名: (required の引数名, ...)}（import時に BUILTIN_TOOLS から凍結。_allow_result_id が sql を抜いた後の姿）<br>・_LIST_PARAMS = {ツール名: {&quot;文字列の配列&quot;型の引数名, ...}}（トップレベル properties のみ）<br>・results の1エントリ = {&quot;scope&quot;: str, &quot;columns&quot;: [str], &quot;rows&quot;: [tuple], &quot;truncated&quot;: bool, &quot;sql&quot;: str|None, &quot;norm_sql&quot;: str, &quot;turn&quot;: str, &quot;label&quot;: str|None}。result_id は &quot;r_&quot; + uuid4().hex[:8]、turn は &quot;t_&quot; + uuid4().hex[:8]<br>・fetch の戻り値 = (columns, rows, truncated, result_id, total_rows)。total_rows は切り詰めが起きたときだけ非 None<br>・ユーザー定義ツール = {&quot;name&quot;, &quot;description&quot;, &quot;parameters&quot;: [{&quot;name&quot;, &quot;type&quot;, &quot;description&quot;, &quot;required&quot;}], &quot;sql&quot;, &quot;render&quot;: table|chart|chart_dual|excel|csv|none, &quot;chart&quot;: {...}, &quot;enabled&quot;, &quot;owner&quot;: alias, &quot;owner_file&quot;: ファイル名}<br>・builtin_overrides の戻り値 = {ツール名: {&quot;enabled&quot;: False?, &quot;description&quot;: str?}}（enabled は False のときだけ入る）<br>・_Guard の状態 = {failed: {(name, arguments文字列): 理由}, done: {(name, arguments文字列)}, repeats: int}</td></tr>
      <tr><td>定数・しきい値</td><td>・MAX_ENTRIES = 40 — results に覚えておく結果の数（元 tools/results.py）<br>・MAX_CELLS = 400_000 — results の総セル数（行×列）の上限。超えたら古い順に捨てるが len(_store) &gt; 1 の条件があるため最低1件は残る<br>・config.MAX_RESULT_ROWS = 2000 — 1クエリで取得・表示する最大行数。results に預けるのもこの行数まで<br>・config.SAMPLE_ROWS_FOR_LLM = 40 — llm_content に入れるサンプル行数（トークン節約）<br>・config.EXPORT_MAX_ROWS = 1000000（env で変更可）— ファイル出力の行数上限。_run_custom では min(EXPORT_MAX_ROWS, 1_048_575) でExcelのシート上限に丸める<br>・config.MAX_AGENT_STEPS = 10（env で変更可）— _advance / _stream_advance のループ回数<br>・_HAS_DEFAULT = {&quot;title&quot;, &quot;filename&quot;, &quot;chart_type&quot;, &quot;purpose&quot;} — スキーマ上は必須でも実処理が既定値を持つので _missing_required が見逃す引数<br>・_RETIRED = {&quot;plot_chart&quot;} — 宣言だけ BUILTIN_TOOLS から落とすツール。実処理は _HANDLERS に残る<br>・_DYNAMIC_TOOLS = {&quot;search_knowledge_base&quot;} — build_tools が固定宣言を捨てて組み立て直すツール<br>・ADMIN_TOOLS = {&quot;explore_import_files&quot;, &quot;analyze_usage&quot;} — ADMIN_TOOLS_files ∪ ADMIN_TOOLS_usage<br>・_Guard.LIMIT = 2 — 同じ (ツール名, 引数文字列) が何回来たら質問を打ち切るか<br>・BUILTIN_TOOLS = 43個（静的リテラル37 ＋ _chart_tools() 6 − plot_chart 1 ＋ KNOWLEDGE_TOOLS 1）。_HANDLERS = 44個<br>・SQL_TOOLS = 25個（query 11 / stats 8 / business 6）。うち宣言があり explanation が付くのは24個 — help.html の「24種」と一致<br>・custom_tools._NAME_RE = ^[A-Za-z][A-Za-z0-9_]{0,47}$ — OpenAI の function 名の制約に合わせた48文字以内<br>・custom_tools.RENDER_KINDS = (&quot;table&quot;, &quot;chart&quot;, &quot;chart_dual&quot;, &quot;excel&quot;, &quot;csv&quot;, &quot;none&quot;) / PARAM_TYPES = (&quot;string&quot;, &quot;integer&quot;, &quot;number&quot;, &quot;boolean&quot;)<br>・search_knowledge_base の chunk_top_k 上限 = max(1, min(AIの指定, 利用者設定の2倍, 100))</td></tr>
    </tbody></table></div>
    <div class="card__title mt">落とし穴（18件）</div>
    <div class="tablewrap"><table class="data"><thead><tr><th style="width:60px">#</th><th>内容</th></tr></thead><tbody>
      <tr><td class="mono small">01</td><td>plot_chart の引退には穴が3つ残っている。(1) custom_tools.builtin_names() は引退フィルタ後の BUILTIN_TOOLS から名前を引くので、ユーザーは plot_chart という名前のツールを作れてしまう。(2) その場合 dispatch は _HANDLERS を先に見るので、実行されるのは組み込みの _plot_chart であってユーザーのSQLではない（12574行付近のコメントが「38個に増やして直した」と書いている不整合が、引退ツールにだけ再現する）。(3) plot_chart は SQL_TOOLS と TOOL_LABELS にも残っているので、名前を名指しで呼べばSQLプレビューもラベルも出る。</td></tr>
      <tr><td class="mono small">02</td><td>builtin_tools の enabled: false は「AIに渡さない」だけで、dispatch は一切見ない。過去の会話の履歴からツール名を拾って呼ばれれば無効化したはずのツールが実行される。ADMIN_TOOLS だけが build_tools と dispatch の2箇所で守られている（コメントの「守りは2箇所で持つ」は管理者判定にしか適用されていない）。</td></tr>
      <tr><td class="mono small">03</td><td>_allow_result_id が required から &quot;sql&quot; を消しているので、_missing_required は sql の欠落を絶対に検知しない。sql も result_id も rows も無いときのエラーは fetch() の AnalysisError 側が出す。さらに _HAS_DEFAULT の効果で run_sql_query（required が purpose だけになる）と plot_trend / plot_composition / plot_distribution / plot_relationship（chart_type と title だけになる）は実質必須チェックがゼロになる。</td></tr>
      <tr><td class="mono small">04</td><td>_missing_required と _coerce_lists はどちらも BUILTIN_TOOLS から作った表を引くので、ユーザー定義ツールには一切効かない。ユーザー定義ツールの required: true は to_schema でAIに伝えるだけの飾りで、AIが落としても止まらず、coerce_params が None を入れて SQL に NULL がバインドされる（0件が返って「データがありません」と答える）。</td></tr>
      <tr><td class="mono small">05</td><td>_string_list_params はツールのトップレベル properties しか見ない。export_excel の sheets.items.chart.value_columns のような入れ子の「文字列の配列」は _coerce_lists の対象外で、文字列が1つ来ても直らない。</td></tr>
      <tr><td class="mono small">06</td><td>_INLINE_COLUMNS が付いたツールでは columns が「文字列の配列」型になるので _coerce_lists の対象に入る。pivot_table だけは自前の columns（列に展開する1列名＝文字列）を持つため _allow_result_id が上書きせず、結果として _LIST_PARAMS にも入らない。この2つは連動している — pivot_table の columns を配列宣言に変えると pandas 側で unhashable type: &#x27;list&#x27; になる。</td></tr>
      <tr><td class="mono small">07</td><td>カタログ画面の組み込みツール一覧（builtin=[_builtin_view(t) for t in tools.BUILTIN_TOOLS]）は build_tools を通していない生のリスト。「AIがこのツールをどう理解しているか」を見せるのが目的と書かれているが、実際には explanation 引数も、管理者フィルタも、ナレッジベース名を埋め込んだ動的な description も反映されない。help.html 側（tools_now）は builtin_overrides と ADMIN_TOOLS を反映するので、2つの画面で見えるものが違う。</td></tr>
      <tr><td class="mono small">08</td><td>results の _store はプロセス内グローバルで、利用者もチャットも見ない。get() の照合は scope_key（DBファイルパスの並び）だけ。DBが1つの統合構成では全利用者・全チャットで scope_key が同一なので、result_id（8桁hex）を知っていれば他人の結果を引ける。MAX_ENTRIES = 40 も全利用者で共有なので、同時利用が増えると「会話1本で使う量には十分」という前提が崩れて古い result_id が早く消える。</td></tr>
      <tr><td class="mono small">09</td><td>_gather_sqls はハンドラを呼ぶ前に走る。だからそのツール自身が新しく預ける result_id は当然拾えないし、result_id 経由でSQLを引くときも「実行前の _store」を見る。ユーザー定義ツールだけは例外的にハンドラ呼び出しの直前に sqls.append(render_sql(tool)) で足しており、そのSQLには :name のバインド変数が残ったまま verify に渡る（alerts_for は表名を正規表現で拾うだけで実行しないので害はない）。</td></tr>
      <tr><td class="mono small">10</td><td>_run_custom と fetch は results.put の前に db.widen_scope で scope を広げる。預けたキーは広げた後のもの。DBが複数あってSQLが別DBを名指ししている場合、次のツールが広げる前の scope で同じ result_id を引くと scope_key が一致せず「データが見つかりません」になる。DBが1つの現構成では widen_scope が実質no-opなので表面化しない。</td></tr>
      <tr><td class="mono small">11</td><td>verify_alerts は「戻り値は3キー」という文書化された契約の外にある第4のキーで、_execute だけが読む。ここが res を破壊的に書き換えるので、dispatch の戻り値を再利用する別の経路を足すときは3キー前提で書くと落とす。</td></tr>
      <tr><td class="mono small">12</td><td>_describe_table の llm_content だけは JSON ではなく素の日本語テキスト。_Guard.note が json.loads(res[&quot;llm_content&quot;]) を except (ValueError, TypeError) で囲んでいるのはこのため。llm_content を必ず JSON として読む新しいコードを足すと describe_table で壊れる。</td></tr>
      <tr><td class="mono small">13</td><td>fetch は rows: [] と sql が同時に来たらSQLを採る。LLMが引数の雛形ごと rows:[] を付けてくるのを0行の表として扱うと、データがあるのに「無い」と答えてしまう（実測でCOUNTが常に0行になった）。逆に言えば、意図的に空の表を渡す手段は無い。</td></tr>
      <tr><td class="mono small">14</td><td>knowledge_tool_schemas() は rag_targets() → rag_excluded_ids(None) → _rag_local.user（スレッドローカル）に依存する。_begin_turn の rag.set_current_user(g.user) が効いていないスレッドで build_tools を呼ぶと、除外設定が反映されないKB一覧が出る。ストリーミングの generate() が rag.set_current_user(user) を呼び直しているのはこのため。</td></tr>
      <tr><td class="mono small">15</td><td>build_tools は毎エージェントステップ呼ばれる（llm.chat の第2引数）。collect_everywhere は全DBの .meta.yaml を読み直すので、会話の途中でツールを追加・無効化すると次のステップから効く。逆に、同じ会話の前半で見せた宣言と後半の宣言が食い違い得る。</td></tr>
      <tr><td class="mono small">16</td><td>単一ファイル統合の副作用として、_search_knowledge_base の中で results = rag_retrieve_all(...) がモジュールエイリアスの results（= core モジュール自身）をローカル変数で影にしている。この関数の中では results.put / results.get が呼べない。同じ罠が他の関数にも潜みうる。</td></tr>
      <tr><td class="mono small">17</td><td>dispatch の第4引数 entries には呼び出し側が scope をそのまま渡している。scope の要素に meta（.meta.yaml）が入っている（build_scope が入れている）から builtin_overrides も collect_everywhere も動く。scope を作り直すコードから meta を落とすと、組み込みの無効化・説明上書き・ユーザー定義ツールが静かに全部消える。</td></tr>
      <tr><td class="mono small">18</td><td>カタログへの書き込み系ツール（propose_glossary_term / propose_example）は ADMIN_TOOLS に入っていない。dispatch は誰にでも実行させ、提案カードを画面に出すところまでやる。実際の権限判定は確定ボタンの側（_may_contribute_catalog、既定は管理者のみ・config.CATALOG_OPEN_CONTRIB で全員可に戻せる）にある。dispatch の管理者判定だけを見て「書き込みは止まっている」と読むと誤る。</td></tr>
    </tbody></table></div>
  </div>

  <div class="card mt">
    <div class="card__title" id="impl-catalog">5-6. データカタログ</div>
    <div class="card__desc">DBの隣に置いたサイドカーYAML（<code>&lt;db&gt;.meta.yaml</code>）が唯一のカタログで、表・列の説明、まとまりのメモ、業務用語、関連（ER図の線）、例文、検算、ER配置、ユーザー定義ツールを持つ。これに対して <code>profile_db</code> が実DBを読み取り専用で走査し、列・FK・行数・サンプル行・列統計を JSON キャッシュに落とす。カタログ（人が書いた知識）とプロファイル（機械が読んだ事実）の2枚を突き合わせるのが <code>drift_warnings</code>（腐った記述の検出）と <code>join_suggestions</code>（未登録の結合の発見）で、両者とも「表名は必ず <code>まとまり__名前</code>」という規約を前提にヒューリスティックを組んでいる。関連は <code>parse_endpoint_cols</code> / <code>rel_pairs</code> / <code>format_endpoint</code> の3本で文字列と構造を往復し、複合キーは括弧形式 <code>表.(c1, c2)</code> 1本にまとめて持つ。</div>
    <div class="tablewrap"><table class="data"><thead><tr><th style="width:210px">項目</th><th>内容</th></tr></thead><tbody>
      <tr><td>カタログの置き場所と3つの読み書き関数</td><td><div class="mt">カタログは <code>meta_path(db_path)</code> = <code>str(db_path) + &quot;.meta.yaml&quot;</code>。DBが <code>data/統合.db</code> なら <code>data/統合.db.meta.yaml</code>。<b>カタログは全員で1つ</b>（利用者ごとに分けない）。「DBの中身が何かは人によって変わらないので、定義を分けると同じ質問なのに人によって答えが違うことになる」というのが分けない理由で、書けるのは <code>admin_required</code> のカタログ画面だけ。</div><div class="mt"><b><code>_read_yaml(p)</code> — YAMLの読みとキャッシュ</b></div><div class="mt">モジュール変数 <code>_meta_cache: {パス文字列: (mtime_ns, size, 中身dict)}</code> を持つ。</div><pre class="mono small">st = p.stat()          # 失敗したら _meta_cache から捨てて {} を返す
hit = _meta_cache[str(p)]
if hit and hit[0] == st.st_mtime_ns and hit[1] == st.st_size: return hit[2]
data = yaml.safe_load(...)   # dict でなければ {}
例外なら print して {}（キャッシュには入れない）</pre><div class="mt">キャッシュを入れた動機はコメントに残っている。1画面を描くのにER図の候補・結合の相手先・ユーザー定義ツールの収集がそれぞれ全DBのカタログを見に行き、21DBで1画面66回のパース・2.4秒かかっていた。判定に mtime_ns + size を使っているので、外部エディタで直接直しても次の読みで反映される。</div><div class="mt"><b><code>load_meta</code> / <code>load_meta_for_edit</code> の使い分け</b></div><div class="mt">・<code>load_meta(db_path)</code> … <code>_read_yaml</code> の戻りを<b>そのまま</b>返す。つまりキャッシュの実体。<b>書き換えてはいけない</b>。書き換えると同じファイルを読んだ他の画面・他のリクエストにその変更が漏れる。<br>・<code>load_meta_for_edit(db_path)</code> … <code>copy.deepcopy</code> した複製を返す。画面からの保存は「読む → 一部を書き換える → <code>save_meta</code>」という流れなので、控えをそのまま渡すと保存前の途中状態が漏れる。</div><div class="mt">実際の使い分けは徹底されていて、<code>/api/catalog/table</code>・<code>/glossary</code>・<code>/examples</code>・<code>/checks</code>・<code>/group</code>・<code>/tool</code>・<code>/builtin</code>・<code>/layout</code>・<code>/primary-key</code>・<code>/relationship</code>・<code>/view</code> はすべて <code>load_meta_for_edit</code>。読むだけの <code>_overview</code>・<code>_views_payload</code>・<code>table-info</code>・<code>suggestions</code>・プロンプト生成側はすべて <code>load_meta</code>。<code>cleanup._scrub_meta</code> の呼び出し元は <code>load_meta_for_edit</code> を使わず <code>copy.deepcopy(catalog.load_meta(f))</code> と自前で写しを取っており、そこには「ここを直に触ると、削除前の下見（apply=False）が控えを先に消してしまい、本番の掃除が『消すものが無い』と判断してファイルを書き換えない＝消したテーブルの説明が残り続ける」という事故の記録がコメントで残っている。</div><div class="mt"><b><code>save_meta(db_path, meta)</code> — 全文書き換え</b></div><div class="mt">順序は次のとおり。</div><div class="mt">・<code>_meta_cache.pop(str(target))</code> — 保存したら控えを捨てる。「更新時刻でも気づけるが、同じ秒内に読み書きが続くと取りこぼすことがあるため明示的に消す」。<br>・<code>meta[&quot;caveats&quot;]</code> があれば <code>merge_caveats</code> で <code>description</code> に合流させて <code>caveats</code> を pop（旧2欄形式の吸収）。※ <b>この2つは引数の dict を破壊的に変更する</b>。<br>・<code>_META_KEYS</code> を順に見て、値が <code>None / &quot;&quot; / [] / {}</code> でないものだけ <code>cleaned</code> に詰める。<b><code>_META_KEYS</code> に無いキーは黙って捨てられる</b>。<br>・<code>cleaned</code> が空なら空ファイルを書く。そうでなければ <code>yaml.dump(..., Dumper=_MetaDumper, allow_unicode=True, sort_keys=False, default_flow_style=False)</code>。</div><div class="mt"><code>_MetaDumper</code> は <code>str</code> の representer を差し替えていて、改行を含む文字列（説明・SQL）は行末空白を落としたうえで <code>|</code> ブロックで書く。「手で開いて読める・直せるファイルにしておくため」。PyYAML は行末に空白があると <code>|</code> を使えず引用符に落ちるので、先に <code>rstrip()</code> している。</div><div class="mt"><b><code>forget(db_path)</code></b></div><div class="mt">DBを消した／ビューを作り直したときに呼ぶ。プロファイルのキャッシュファイルを <code>unlink(missing_ok=True)</code> し、プロンプト本文のキャッシュ <code>_TEXT_CACHE</code> からそのDB分を落とす。<code>_meta_cache</code> は mtime で自動的に切り替わるので触らない。</div></td></tr>
      <tr><td>meta.yaml の構造（_META_KEYS）</td><td><pre class="mono small">_META_KEYS = (&quot;tables&quot;, &quot;groups&quot;, &quot;relationships&quot;, &quot;glossary&quot;,
              &quot;examples&quot;, &quot;checks&quot;, &quot;er_layout&quot;, &quot;tools&quot;, &quot;builtin_tools&quot;,
              # 旧形式の読み込み互換のため残す（新規には書かない）
              &quot;title&quot;, &quot;description&quot;)</pre><div class="tablewrap"><table class="data"><thead><tr><th>キー</th><th>中身</th><th>書く場所</th></tr></thead><tbody><tr><td><code>tables</code></td><td><code>{表名: {description, ai_draft, columns, primary_key, glossary}}</code></td><td><code>/api/catalog/table</code>, <code>/primary-key</code>, <code>/glossary</code>, <code>/view</code></td></tr><tr><td><code>groups</code></td><td><code>{接頭辞: {description}}</code> まとまりのメモ</td><td><code>/api/catalog/group</code></td></tr><tr><td><code>relationships</code></td><td><code>[{from, to, cardinality}]</code> ER図の線</td><td><code>/api/catalog/relationship</code></td></tr><tr><td><code>glossary</code></td><td>表をまたぐ用語 <code>{用語: {description, sql}}</code></td><td><code>/api/catalog/glossary</code>（table 指定なし）</td></tr><tr><td><code>examples</code></td><td><code>[{q, description?, sql}]</code></td><td><code>/api/catalog/examples</code></td></tr><tr><td><code>checks</code></td><td>検算 <code>[{name, left, right, drilldown, ...}]</code></td><td><code>/api/catalog/checks</code></td></tr><tr><td><code>er_layout</code></td><td><code>{&quot;alias.表名&quot;: [x, y]}</code></td><td><code>/api/catalog/layout</code></td></tr><tr><td><code>tools</code></td><td>ユーザー定義ツール <code>[{name, description, sql, parameters, ...}]</code></td><td><code>/api/catalog/tool</code></td></tr><tr><td><code>builtin_tools</code></td><td>組み込みツールの上書き <code>{名前: {enabled, description}}</code></td><td><code>/api/catalog/builtin</code></td></tr><tr><td><code>title</code> / <code>description</code></td><td>旧「データ全体の説明」。読むだけ、新規には書かない</td><td>—</td></tr></tbody></table></div><div class="mt"><b><code>tables.&lt;表名&gt;</code> の中身</b></div><div class="mt">・<code>description</code> … 表の説明（1行が何のレコードか）。<code>※</code> で始まる行が注意書きに相当する（旧 <code>caveats</code> 欄は廃止され <code>merge_caveats</code> で合流）。<br>・<code>ai_draft</code> … AIが起こした下書きで人が未確認、の印。プロンプトには <code>（AI推測・未確認）</code> として出る。<code>/api/catalog/table</code> で人が保存すると <code>tm.pop(&quot;ai_draft&quot;)</code> される。<br>・<code>columns</code> … <code>{列名: {description?, values?}}</code>。<code>values</code> はコード値の意味 <code>{&quot;1&quot;: &quot;受付&quot;, &quot;2&quot;: &quot;出荷済&quot;}</code>。説明もコード値も空のエントリは保存時に落とされ、<code>columns</code> が空なら <code>columns</code> キーごと消える。さらに <code>description / columns / primary_key / glossary</code> のどれも無くなったら表のエントリ自体を消す。<br>・<code>primary_key</code> … 人が指定した主キー列のリスト（<code>effective_pk</code> 参照）。<br>・<code>glossary</code> … その表固有の用語。<code>normalize_glossary</code> で <code>{用語: {description, sql}}</code> に揃える。値が文字列だった（手でYAMLを書いた）場合は<b>説明</b>として扱い、警告を print する。以前はSQL式として扱っていたが、説明文が書かれていると「この式をそのまま使う」とAIに渡して構文エラーのSQLを作らせていたため。</div><div class="mt"><b><code>groups</code>（まとまり）</b></div><div class="mt"><code>db_groups(meta)</code> が <code>{接頭辞: {&quot;description&quot;: str}}</code> に正規化する（dict でない値は落とす）。<b>まとまりは表示名を持たない</b>。名前は表名の接頭辞そのもの（<code>人事_勤怠__出勤簿</code> なら <code>人事_勤怠</code>）で、「名前を2つ持つと、どちらを信じるかという問題が生まれるだけ」。また「データ全体の説明」欄も持たない。「全体に書かれた文章は対象の入れ替えに追随できず腐るため、知識は必ず対象物（表・まとまり・用語）に付ける」。まとまりのメモは <code>db_text</code> で、<b>表示中の表の接頭辞に該当するぶんだけ</b> <code>【接頭辞】\nメモ</code> の形でプロンプトに載る。</div><div class="mt"><code>/api/catalog/group</code> の保存は、<code>gkey</code> が空、または「そのまとまりの表が1つも無いのに本文を書こうとした」場合に 400。ただし空文字（＝消す）は表が無くても通す。「表を全部消したあとメモだけ残ると、乖離警告が出るのに直す手段が無くなる」ため。</div></td></tr>
      <tr><td>profile_db — プロファイルの作り方</td><td><div class="mt"><b>キャッシュキーと入口</b></div><pre class="mono small">st = db_path.stat()
key = {&quot;v&quot;: 2, &quot;mtime&quot;: st.st_mtime, &quot;size&quot;: st.st_size}
cache = config.PROFILE_CACHE_DIR / (Path(db_path).name + &quot;.profile.json&quot;)
if not force and cache.exists():
    data = json.loads(cache.read_text())
    if data.get(&quot;key&quot;) == key: return data      # 読めない/壊れていたら黙って作り直す</pre><div class="mt"><code>v</code> は構造バージョン。上げると全キャッシュが無効になる（現在 2）。キャッシュファイル名は DBの<b>ファイル名だけ</b>で、ディレクトリを含まない。</div><div class="mt"><b>走査</b></div><div class="mt"><code>db.connect_ro(db_path)</code>（<code>file:...?mode=ro</code> の URI 接続）を開き、<code>_make_timeout(conn, config.PROFILE_TIMEOUT_SEC)</code> を仕掛ける。これは <code>conn.set_progress_handler(..., 100000)</code> で、100000 VMステップごとに「最後の <code>reset()</code> から30秒を超えていたら 1（中断）」を返す関数を登録し、リセット用のクロージャを返す。中断は <code>sqlite3.OperationalError</code> になり、各所の <code>except sqlite3.Error</code> が拾う。</div><div class="mt">対象は</div><pre class="mono small">SELECT name, type FROM sqlite_master
WHERE type IN (&#x27;table&#x27;,&#x27;view&#x27;) AND name NOT LIKE &#x27;sqlite_%&#x27; ORDER BY name</pre><div class="mt">つまり<b>ビューも表と同じ扱いでプロファイルに入る</b>（<code>t[&quot;type&quot;]</code> が <code>&quot;table&quot;</code> / <code>&quot;view&quot;</code>）。1表の走査が <code>sqlite3.Error</code> で落ちたら、その表は <code>{&quot;type&quot;, &quot;error&quot;: str(e), &quot;columns&quot;: [], &quot;fks&quot;: [], &quot;row_count&quot;: None, ...}</code> という空の枠で登録され、全体は続行する。</div><div class="mt"><b><code>_profile_table(conn, name, reset)</code> — 1表ぶん</b></div><div class="mt"><code>reset()</code> を挟みながら次の順で撃つ。識別子は <code>_qi()</code>（<code>&quot;</code> を <code>&quot;&quot;</code> にエスケープしてダブルクオート）で囲む。</div><div class="mt">・<code>PRAGMA table_info(t)</code> → <code>columns = [{name, type, notnull, pk, pk_seq}]</code>。<code>pk</code> は bool、<code>pk_seq</code> は PRAGMA の pk 値そのもの（0=非キー、1以上=複合主キー内の順番）。「複合キーの構成順は『1行が何を表すか』の手がかりになるので pk_seq に残す」。<br>・<code>PRAGMA foreign_key_list(t)</code> → <code>fks = [{&quot;from&quot;: row[3], &quot;table&quot;: row[2], &quot;to&quot;: row[4] or &quot;id&quot;}]</code>。<br>・<code>SELECT COUNT(*)</code> → <code>row_count</code>。失敗（タイムアウト等）なら <code>None</code> のまま続行。<br>・<code>SELECT * FROM t LIMIT 5</code>（<code>config.PROFILE_SAMPLE_ROWS</code>）→ <code>sample_columns</code>（cursor.description から）と <code>sample_rows</code>。値は <code>_jsonable</code> を通し、<code>bytes</code> は <code>&quot;&lt;BLOB n bytes&gt;&quot;</code> に置き換える。ORDER BY は無いので「先頭5行」であって代表値ではない。<br>・列統計 <code>col_stats</code>。</div><div class="mt"><b><code>col_stats</code> の作り方と distinct 20 の分岐</b></div><div class="mt">条件: <code>row_count is not None and 0 &lt; row_count &lt;= config.PROFILE_STATS_MAX_ROWS</code>(2,000,000)。<b>行数が取れなかった表（3で失敗）は統計をまるごとスキップする</b>。</div><div class="mt">各列について <code>limit = config.PROFILE_LOW_CARDINALITY</code>(20) として</div><pre class="mono small">SELECT &quot;col&quot; AS v, COUNT(*) AS n FROM &quot;t&quot; GROUP BY 1 ORDER BY n DESC LIMIT 21</pre><div class="mt">・<code>len(vals) &lt;= 20</code> → <code>stat[&quot;values&quot;] = [[値, 件数], ...]</code>（件数の多い順）。低カーディナリティ列は実値をそのまま持つ。<br>・<code>21</code> 件返った（＝21種類以上ある）→ 値は諦めて <code>SELECT MIN(col), MAX(col)</code> を撃ち直し、<code>stat[&quot;min&quot;] / stat[&quot;max&quot;]</code> を入れる。<br>・例外は握って <code>stat</code> を空のまま。<code>stat</code> が空でなければ <code>col_stats[列名]</code> に入る。</div><div class="mt">LIMIT を <code>limit + 1</code> にしているのが判定の肝で、「20以下か」を追加のクエリ無しで判別している。NULL は SQLite の GROUP BY で1グループにまとまるので、<code>values</code> に <code>[None, 件数]</code> として入り得る。</div><div class="mt"><b>出力</b></div><pre class="mono small">profile = {&quot;file&quot;: db_path.name, &quot;key&quot;: key,
           &quot;generated_at&quot;: datetime.now().isoformat(timespec=&quot;seconds&quot;),
           &quot;tables&quot;: {表名: 上の dict}}</pre><div class="mt">を <code>json.dumps(..., ensure_ascii=False, default=str)</code> でキャッシュに書いて返す。<code>default=str</code> があるので、JSON にできない値（Decimal など）は文字列化されて保存される＝<b>キャッシュ経由のプロファイルと生成直後のプロファイルで値の型が変わり得る</b>。</div><div class="mt"><b>誰が force するか</b></div><div class="mt"><code>force=True</code> は取り込み系だけ（<code>/api/import/run</code> の手動取り込み、ジョブ登録直後の初回実行、<code>/api/jobs/run</code>）。ビューの作成・削除や表の削除・改名は <code>force</code> ではなく <code>catalog.forget(path)</code> でキャッシュファイルごと消して作り直させている。</div></td></tr>
      <tr><td>effective_pk / declared_pk</td><td><pre class="mono small">def declared_pk(profile, tname) -&gt; list[str]:
    cols = [c for c in profile[&quot;tables&quot;][tname][&quot;columns&quot;] if c.get(&quot;pk&quot;)]
    cols.sort(key=lambda c: c.get(&quot;pk_seq&quot;) or 0)
    return [c[&quot;name&quot;] for c in cols]

def effective_pk(profile, meta, tname) -&gt; tuple[list[str], str]:
    valid = [列名 ...]                                  # profile 側に実在する列
    ov = meta[&quot;tables&quot;][tname][&quot;primary_key&quot;]           # 無ければ None
    if ov:
        cols = [c for c in ov if c in valid]
        if cols: return cols, &quot;override&quot;                # 1つでも残れば採用
    d = declared_pk(profile, tname)
    return (d, &quot;declared&quot;) if d else ([], &quot;none&quot;)</pre><div class="mt">出所は <code>&quot;override&quot; | &quot;declared&quot; | &quot;none&quot;</code> の3値。メタの <code>primary_key</code> が DB宣言より優先されるのは「主キーが宣言されていないテーブル（CSV取込など）に人が指定できるようにするため」。<code>declared_pk</code> が <code>pk_seq</code> で並べ替えるのは、複合キーの構成順を保つため（PRAGMA の返す行順は cid 順で、複合キーの順序とは一致しない）。</div><div class="mt">利用側:</div><div class="mt">・<code>table_text</code> … プロンプトに主キーを載せる。複合キーのときは <code>主キー（人が指定）: (c1, c2) の複合キー → この組み合わせで1行が一意。結合するときは2列すべてを条件にする。</code>、無いときは <code>主キー: なし（宣言が無く、指定もされていない）。重複行があり得るので COUNT(DISTINCT ...) の要否に注意する。</code> と明示する。<br>・<code>_is_sole_pk(profile, meta, table, column)</code> … <code>len(pk) == 1 and pk[0] == column</code>。<code>normalize_direction</code> と <code>child_parent</code>、<code>link_check</code> の「主キー同士を結んでいます」判定が使う。<br>・<code>er_payload</code> … ノードの列に付ける PK バッジ。</div><div class="mt"><code>/api/catalog/primary-key</code> は <code>cols and cols != declared</code> のときだけ <code>primary_key</code> を書き、宣言と同じ並びを指定したときは override を<b>消す</b>（<code>pk_src</code> が <code>declared</code> に戻る）。</div></td></tr>
      <tr><td>drift_warnings — 全検査</td><td><div class="mt"><code>drift_warnings(profile, meta)</code> は文字列のリストを返し、<code>_overview</code> 経由でカタログ画面の上部に <code>alert--warn</code> として並ぶだけ（API は無い）。検査は次の順で走る。</div><div class="mt"><b>1. 表</b> — <code>meta[&quot;tables&quot;]</code> のキーが <code>profile[&quot;tables&quot;]</code> に無い → <code>メタ情報のテーブル &#x27;X&#x27; はDBに存在しません（改名/削除された可能性）。</code> を出して <b>continue</b>（その表の列・主キー検査はしない）。</div><div class="mt"><b>2. 列</b> — <code>tmeta[&quot;columns&quot;]</code> のキーが実在しない → <code>メタ情報の列 &#x27;T.C&#x27; はDBに存在しません。</code></div><div class="mt"><b>3. 指定主キー</b> — <code>tmeta[&quot;primary_key&quot;]</code> の各列が実在しない → <code>指定された主キーの列 &#x27;T.C&#x27; はDBに存在しません。</code>（一意かどうかは見ない）</div><div class="mt"><b>4. 関連の端点</b> — 各 <code>relationship</code> の <code>from</code> / <code>to</code> を <code>parse_endpoint_cols(end, &quot;@own&quot;)</code> で解く。</div><div class="mt">・解けない、または <code>alias != &quot;@own&quot;</code>（＝他DB指定）→ その端点は<b>素通り</b>。<br>・表が profile にある → 列ごとに実在確認、無ければ <code>結合定義の &#x27;X&#x27; に対応する列がありません。</code><br>・表が無い → <code>結合定義の &#x27;X&#x27; に対応するテーブルがありません。</code></div><div class="mt"><b>5. 関連の列数</b> — 両端点が解けて <code>len(from列) != len(to列)</code> → <code>結合定義 &#x27;A → B&#x27; の列数が合っていません。</code>（複合キーの片側だけ列を足した状態）</div><div class="mt"><b>6〜8. SQL の中の亡霊テーブル</b> — 共通の判定が <code>_missing(sql)</code>:</div><pre class="mono small">toks = set(re.findall(r&quot;\w+&quot;, str(sql or &quot;&quot;)))   # \w は日本語のテーブル名も拾う
return sorted(t for t in toks
              if &quot;__&quot; in t and not t.endswith(&quot;__&quot;) and t not in ptables)</pre><div class="mt">「<code>__</code> を含み、<code>__</code> で終わらず、実在しない」トークンだけを表名と見なす。<code>__</code> で終わるものを除くのは、メモの <code>人事_勤怠__*</code> のような「まとまり全体を指す書き方」を拾わないため。これを</div><div class="mt">・<code>meta[&quot;examples&quot;]</code> の <code>sql</code> → <code>例文「q[:30]」が、存在しないテーブル &#x27;T&#x27; を使っています。</code><br>・<code>meta[&quot;checks&quot;]</code> の <code>left</code> / <code>right</code> / <code>drilldown</code> を空白連結したもの → <code>検算「name[:30]」が、…</code><br>・<code>meta[&quot;glossary&quot;]</code>（<b>DB全体の用語だけ</b>）の <code>sql</code> → <code>用語「term」のSQL式が、…</code></div><div class="mt">に掛ける。この検査の目的は「削除の掃除が中断された（アプリ停止・強制終了）ときの取り残し」を見つけること。</div><div class="mt"><b>9〜11. まとまりのメモ</b> — 先に <code>prefixes = {t.split(&quot;__&quot;,1)[0] for t in ptables if &quot;__&quot; in t}</code>（<b>profile の表名から作る。meta の groups キーからではない</b>）を作り、各まとまりについて</div><div class="mt">・そのまとまりの表が1つも無い（<code>t.startswith(gname + &quot;__&quot;)</code> が全滅）→ <code>まとまり「G」のメモが残っていますが、そのまとまりの表がありません。</code><br>・<code>_memo_bad_tables(memo, ptables, prefixes)</code> の各スニペット → <code>まとまり「G」のメモの「snip」は、実在する表の名前ではありません。</code><br>・<code>re.findall(r&quot;まとまり[（(「]([^）)」]+)[）)」]&quot;, memo)</code> で拾った名前が <code>prefixes</code> に無い → <code>まとまり「G」のメモが、存在しないまとまり &#x27;N&#x27; を案内しています。</code></div><div class="mt">まとまりメモを検査する動機はコメントに書かれている。改名すると本文だけ古い名前のまま残る（<code>_rename_in_text</code> は <code>まとまり__表名</code> という完全な表名しか置換しないので、裸のまとまり名は残る）。そしてメモはプロンプトの最上段に無印で入るので、腐ると回答に直に効く。</div><div class="mt"><b><code>_memo_bad_tables</code> — なぜ <code>\w+</code> を使わないか</b></div><div class="mt">例文・検算・用語で使っている <code>_missing</code> はメモに使えない。「メモは散文で、Python の <code>\w</code> は日本語も語構成文字なので『品質__defectsは社内で見つけた不良』が丸ごと1語になり、<b>実在する表を書いたメモほど誤警告が出る（実際に出した）</b>」。そこで逆から見る。</div><pre class="mono small">covered = 実在する表名がメモ中で占める文字位置の集合（全出現・memo.find を i+1 で回す）
for m in re.finditer(r&quot;__&quot;, memo):
    if m.start() in covered: continue                     # 実在表の一部
    head = memo[:m.start()]
    if head が実在の接頭辞のどれかで終わる
       and not memo[m.end():m.end()+1].strip(&quot; *、。」）&quot;):  # &quot;__&quot; の直後が区切り文字か行末
        continue                                          # 「人事_勤怠__*」= まとまり全体を指す言い方
    out.append(memo[m.start()-14 : m.start()+16] の改行を空白に潰したもの)</pre><div class="mt">実在表の位置を先に塗り、そこから外れた <code>__</code> だけを「表名のつもりで書かれた別物」として拾う。警告に出すのは表名ではなく前後14/16文字のスニペット（何が悪いか機械には特定できないので、人が現物を探せる形で見せる）。</div></td></tr>
      <tr><td>_suggest_values — 値の標本の取り方</td><td><div class="mt">結合候補の裏取り用に、実データから2種類の集合を作る。</div><pre class="mono small">_suggest_cache: dict = {}    # {(パス文字列, mtime_ns): (samples, pk_values)}

def _suggest_values(db_path, profile) -&gt; (samples, pk_values):
    key = (str(db_path), Path(db_path).stat().st_mtime_ns)
    if key in _suggest_cache: return それ
    for tname, t in profile[&quot;tables&quot;].items():
        pks = [c[&quot;name&quot;] for c in t[&quot;columns&quot;] if c[&quot;pk&quot;]]     # ← profile の宣言PK
        for c in t[&quot;columns&quot;]:
            if c[&quot;type&quot;] not in (&quot;TEXT&quot;, &quot;INTEGER&quot;): continue  # ← 完全一致
            if len(pks) == 1 and c[&quot;name&quot;] == pks[0]:
                pk_values[(tname, c[&quot;name&quot;])] = {str(r[0]) for r in
                    SELECT DISTINCT col FROM t WHERE col IS NOT NULL LIMIT 20000}
            samples[(tname, c[&quot;name&quot;])] = {str(r[0]) for r in
                    SELECT DISTINCT col FROM t WHERE col IS NOT NULL LIMIT 200}
    _suggest_cache.clear()       # DBは1つ。古い版を抱えない
    _suggest_cache[key] = (samples, pk_values)</pre><div class="mt">・値はすべて <code>str()</code> に揃えてから集合にする。型が違う列（INTEGER の 1 と TEXT の &quot;1&quot;）でも比較が成立する。<br>・標本は列あたり<b>最大200個の distinct 値</b>。主キー側は「照合の分母になるので全部持つ（このアプリの表は大きくても数千行）」として 20000。<br>・<code>pk_values</code> に入るのは<b>単独主キーの列だけ</b>。複合主キーの表は親候補にならない。<br>・判定に使うのは <code>profile</code> の <code>c[&quot;pk&quot;]</code>＝<b>DB宣言の主キー</b>で、<code>effective_pk</code>（人が指定した <code>primary_key</code>）ではない。<br>・キャッシュは DBファイルの mtime_ns。候補APIは関連を触るたびに呼ばれるので、毎回700列を読み直さないための措置。1件だけ持つ（<code>clear()</code> してから入れる）。</div></td></tr>
      <tr><td>join_suggestions — 結合候補の判定</td><td><div class="mt"><code>join_suggestions(profile, meta, db_path=None)</code> は <code>{from, to, cardinality: &quot;N:1&quot;, reason}</code> のリストを返す。<code>db_path</code> を渡すと実データで裏を取る。カタログ画面と <code>/api/catalog/suggestions</code> が呼び、戻りに <code>sqlusage.suggestions_for()</code>（過去に実際に使われたのに未登録の結合、上位8件）を連結して表示する。</div><div class="mt"><b>0. 既存の結合を集める（<code>existing</code>）</b></div><div class="mt">・<code>meta[&quot;relationships&quot;]</code> … <code>rel_pairs(rel, &quot;@own&quot;)</code> が解ければ<b>列ペアごとに</b> <code>(&quot;表.列&quot;.lower(), &quot;表.列&quot;.lower())</code> を入れる（複合キーの片列だけの候補を出さないため）。解けなければ生の <code>from</code>/<code>to</code> 文字列を lower して入れる。<br>・profile の FK … <code>(&quot;表.from&quot;.lower(), &quot;相手表.to&quot;.lower())</code>。</div><div class="mt"><b>1. <code>*_id</code> の命名規約から（<code>列名 &#x27;X&#x27; → テーブル &#x27;T&#x27; の推測</code>）</b></div><pre class="mono small">low = 列名.lower()
if not low.endswith(&quot;_id&quot;) and not low.endswith(&quot;id&quot;): continue
base = low[:-3] if low.endswith(&quot;_id&quot;) else None
if not base: continue                        # ← &quot;id&quot; 止まりはここで落ちる
for cand in (base, base+&quot;s&quot;, base+&quot;es&quot;):     # 表名と大小無視で完全一致
    target = 一致する表名 (自表は除く)
    相手の宣言PK列が2つ以上 → skip（1列だけで結合する候補は誤りになる）
    to_col = 相手の最初のPK列 ?? 相手の列で名前が &quot;id&quot; か low と一致するもの
    existing にあれば skip
    候補を積んで break</pre><div class="mt"><b>2. 同名列が他表の単独主キー（<code>同じ名前の列 &#x27;X&#x27; が &#x27;T&#x27; の主キー</code>）</b></div><div class="mt"><code>_suffix(name)</code> = <code>__</code> の後ろ、<code>_group(name)</code> = <code>__</code> の前。</div><pre class="mono small">pk_owner = {pk列名.lower(): [(表, pk列), ...]}   # 単独主キーの表だけ
for 表, 列:
    cands = pk_owner[列名.lower()] から
            自表と、_suffix が同じ表（＝拠点違いの同型表・兄弟）を除いたもの
    same = cands のうち _group が自表と同じもの
    if not same and len(cands) &gt; 3: continue   # 相手が4つ以上は曖昧すぎる
    for target in (same or cands): 候補を積む</pre><div class="mt"><code>equip_code → equipment.equip_code</code> のようなマスタ参照の型。「<code>*_id</code> の規約が無いデータではこちらが本命になる」。兄弟を除くのは <code>東京__defects.equip_code → 大阪__defects.equip_code</code> のような誤りを出さないため。4つ以上を切るのは「equip の部品コード → 全拠点の部品表、のような総当たり」を避けるため。</div><div class="mt"><b><code>db_path is None</code> ならここで返す。</b></div><div class="mt"><b>3. 名前ベース候補への裏取り</b></div><pre class="mono small">def _overlap(frm, to):
    s_ = samples[(from表, from列)]
    p_ = pk_values[(to表, to列)] or samples[(to表, to列)]
    if not s_ or not p_: return None            # 標本が無い＝判定できない
    return len(s_ &amp; p_) / len(s_)</pre><div class="mt">・<code>None</code>（どちらかの標本が無い）→ 理由に何も足さずそのまま残す。<br>・<code>0</code>（1つも重ならない）→ <b>候補ごと捨てる</b>。「JOINしても1行も繋がらない＝間違い」。<br>・それ以外 → 理由に <code>／値の一致 87%</code> を追記。</div><div class="mt"><b>4. 名前の手がかりが無い発見（<code>列名は違うが値が一致（87%が &#x27;T.C&#x27; に存在）</code>）</b></div><pre class="mono small">for 表, 列:
    s_ = samples[(表, 列)];  if len(s_) &lt; 5: continue     # 小さすぎる集合は偶然一致する
    hits = [(r, 相手表, 相手列)
            for (相手表, 相手列), p_ in pk_values.items()
            if 相手表 != 自表 and _suffix が違う and len(p_) &gt;= 5
               and (frm, to) が existing にも seen にも無い
               and (r := len(s_ &amp; p_) / len(s_)) &gt;= 0.9]
    same = hits のうち _group が自表と同じもの
    if not same and len(hits) &gt; 1: continue   # 相手を1つに絞れないなら出さない
    for h in (same or hits): 候補を積む</pre><div class="mt">しきい値が 0.9 と「両側5種類以上」なのは「名前の手がかりが無いぶん厳しめに見る。小さすぎる集合は偶然一致する（例: 2値のコード）」から。同じまとまりに相手がいなければ複数ヒットを捨てるのは「日付列は全拠点のカレンダーに一致してしまうので、同じまとまりのカレンダーが無ければ『どれと繋ぐべきか』を機械では決められない」から。</div></td></tr>
      <tr><td>関連の端点表記と正規化</td><td><div class="mt">関連1件は YAML 上 <code>{from: &quot;...&quot;, to: &quot;...&quot;, cardinality: &quot;N:1&quot;}</code> の3フィールドだけ。端点は文字列で、4通りの書き方を受ける。</div><div class="mt"><b><code>parse_endpoint(end, default_alias)</code></b></div><div class="mt"><code>.</code> で分割して 3要素 → <code>(alias, table, column)</code>、2要素 → <code>(default_alias, table, column)</code>、それ以外 → <code>None</code>。</div><div class="mt"><b><code>parse_endpoint_cols(end, default_alias)</code> — 複合キー対応</b></div><pre class="mono small">m = re.match(r&quot;^(.+?)\.\(([^()]*)\)$&quot;, raw)      # 括弧形式か
マッチしたら: cols = 括弧内を &quot;,&quot; で分割して strip、空要素は落とす
              cols が空 → None
              head を &quot;.&quot; で分割：1要素 → (default_alias, head, cols)
                                 2要素 → (alias, table, cols)
                                 3要素以上 → None
マッチしなければ parse_endpoint に投げて (alias, table, [col]) に包む</pre><div class="tablewrap"><table class="data"><thead><tr><th>書き方</th><th>結果</th></tr></thead><tbody><tr><td><code>table.col</code></td><td><code>(default_alias, table, [col])</code></td></tr><tr><td><code>alias.table.col</code></td><td><code>(alias, table, [col])</code></td></tr><tr><td><code>table.(c1, c2)</code></td><td><code>(default_alias, table, [c1, c2])</code></td></tr><tr><td><code>alias.table.(c1, c2)</code></td><td><code>(alias, table, [c1, c2])</code></td></tr></tbody></table></div><div class="mt"><b><code>format_endpoint(alias, table, cols, own_alias)</code> — 逆変換</b></div><div class="mt"><code>head = table if alias == own_alias else f&quot;{alias}.{table}&quot;</code>。列が1つなら <code>head.col</code>、複数なら <code>head.(c1, c2)</code>。<b>自DBなら alias は書かない</b>（保存されるYAMLは常に短い形になる）。</div><div class="mt"><b><code>rel_pairs(rel, own_alias)</code></b></div><pre class="mono small">a = parse_endpoint_cols(rel[&quot;from&quot;], own_alias)
b = parse_endpoint_cols(rel[&quot;to&quot;], own_alias)
if not a or not b or len(a[2]) != len(b[2]): return None
return (a[0], a[1]), (b[0], b[1]), list(zip(a[2], b[2]))</pre><div class="mt">戻りは <code>((from別名, from表), (to別名, to表), [(from列, to列), ...])</code>。列は<b>位置で対応</b>する。解けない・列数が合わないときは <code>None</code> を返し、乖離検知が別途知らせる担当。単一列でも列ペア1つのリストになるので、呼び出し側は複合キーかどうかを区別しなくてよい。</div><div class="mt"><b><code>normalize_direction(a, b, cardinality, lookup)</code></b></div><pre class="mono small">card = cardinality or &quot;N:1&quot;
try: pa, ma = lookup(a[0]); pb, mb = lookup(b[0])
except Exception: return a, b, card          # 判断できないときは触らない
if not (pa and pb): return a, b, card
if _is_sole_pk(pa, ma, a[1], a[2]) and not _is_sole_pk(pb, mb, b[1], b[2]):
    return b, a, _CARD_FLIP.get(card, card)  # 片方だけが主キーなら、そちらを親(to)に
return a, b, card</pre><div class="mt"><code>_CARD_FLIP = {&quot;N:1&quot;: &quot;1:N&quot;, &quot;1:N&quot;: &quot;N:1&quot;, &quot;1:1&quot;: &quot;1:1&quot;, &quot;N:M&quot;: &quot;N:M&quot;}</code>。</div><div class="mt">向きを揃える理由はコメントに明示されている。「ER図はIPA表記なので矢印を描かない。見た目に向きが無いぶん、人は好きな方向にドラッグする。ところが from/to は単なる描画順ではなく『どちらが参照している側か』を表しており、参照整合性の検査（親に居ない子を数える）はこの向きに依存する。逆向きに登録されると『入金の無い請求』を異常として数えるような、意味の反転が起きる。」</div><div class="mt"><b>片方だけが単独主キーのときしか入れ替えない。</b> 両方が主キー（1:1候補）／どちらも主キーでないときは人が引いた向きのまま保存される。ただし検査側の <code>child_parent(entries, edge)</code> は保存済みの from/to を鵜呑みにせず、主キーがどちら側にあるかで決め直すので、手で書いた <code>.meta.yaml</code> が逆向きでも検査は正しい向きで走る。</div><div class="mt"><b>ER図への展開（<code>collect_edges</code>）</b></div><div class="mt">FK 由来の線とメタ由来の線を集める。メタ側の端点を<b>列ペア単位</b>で <code>meta_pairs</code> に集めておき、同じペアの FK 線は出さない（重複表示の抑止）。線は列ノード同士を結ぶ（<code>col_node_id(alias, table, column)</code> = <code>alias.table::column</code>、<code>COL_SEP = &quot;::&quot;</code>）。複合キーでも<b>線は1本</b>で、<code>pairs[0]</code> の列ペアに係留し、全ペアは <code>pairs</code> フィールドに持つ。ラベルは <code>edge_label()</code> が <code>_CARD_ENDS</code> から <code>* ─ 1</code> の形で作り、列名は出さない。id は FK が <code>fk||a.t.c||b.t.c</code>、メタが <code>rel||alias||配列位置</code>。</div></td></tr>
      <tr><td>複合キーの合流と分解（/api/catalog/relationship）</td><td><div class="mt">ER図キャンバスから呼ばれる <code>admin_required</code> の1本。<code>load_meta_for_edit</code> → <code>rels = meta.setdefault(&quot;relationships&quot;, [])</code> を直接いじり、最後に <code>save_meta</code> して <code>_er_payload</code> を返す。端点は「ドラッグ直後は <code>from_table</code>/<code>from_column</code>、元に戻す／やり直すは保存済み文字列 <code>from</code>/<code>to</code>」の2通りで来るので <code>_ep(side)</code> が吸収する。</div><div class="mt"><b>action = &quot;add&quot;</b></div><div class="mt">・両端点を <code>parse_endpoint</code> → <code>_endpoint_error</code> で実在確認。同じ列同士は 400。どちらか一方は開いているDBの表でなければ 400。<br>・<code>normalize_direction</code> で子→親に揃える。<br>・<b>同じ表ペアの既存関連（合流できる相手）を探す</b>。</div><pre class="mono small">   for i, r in enumerate(rels):
       pr = rel_pairs(r, alias)
       if (pr[0], pr[1]) == ((a別名,a表),(b別名,b表)):  same.append((i, r))
       elif (pr[0], pr[1]) == ((b別名,b表),(a別名,a表)): # 逆向きの既存
           a, b = b, a; card = _CARD_FLIP[card]; same.append((i, r))</pre><div class="mt">逆向きでも拾って既存の向きに合わせる（1つの関連の中で向きが混ざらないように）。</div><div class="mt">・入れ替えの結果 <code>a</code> が他DBになったら 400（<code>外部キーを持つのは X.T です</code>）。<br>・既存の同じ列ペアがあれば 400（<code>すでに登録されています</code>）。<br>・<code>same</code> があり <code>mode</code> が <code>&quot;merge&quot;</code>/<code>&quot;new&quot;</code> のどちらでもなければ、<b>保存せず</b> <code>{ok: false, ask: &quot;merge_or_new&quot;, existing: [...]}</code> を返して画面に選ばせる。「既存の線に列を足して複合キーにするのか、独立した別の関連なのかは人にしか決められない」。<br>・<code>link_check(a, b, lookup, _path_of)</code> で実データを見る。<code>mode == &quot;merge&quot;</code> のときは補正が入る（下記）。<code>level == &quot;block&quot;</code>、または <code>&quot;warn&quot;</code> で <code>force</code> が無ければ <b>200</b> で <code>{ok: false, check}</code> を返す（「画面の api() は非2xxだと本文を捨てて例外にするため」200 で返している）。<br>・保存。<br>・merge … 合流先は <code>same[0]</code>、ただし <code>merge_from</code>/<code>merge_to</code> が来ていればそれで特定。<code>pairs = 既存のpairs + [(a列, b列)]</code> にして <code>format_endpoint</code> で from/to を書き直す。<b><code>cardinality</code> は書き換えない。</b><br>・それ以外 … <code>{from, to, cardinality}</code> を append。</div><div class="mt"><b>merge のときの警告補正</b></div><pre class="mono small">tgt_pairs = rel_pairs(same[0][1], alias)[2] + [(a[2], b[2])]
parent_cols = [p[1] for p in tgt_pairs]
if tuple_unique(親のパス, 親の表, parent_cols):
    kept = [i for i in check[&quot;issues&quot;] if &quot;一意ではありません&quot; not in i[&quot;title&quot;]]
    落としたものがあれば info「複合キーとして一意です」を足す
    level を kept から再計算</pre><div class="mt"><code>tuple_unique(path, table, cols)</code> は <code>SELECT 1 FROM p.表 GROUP BY c1, c2 HAVING COUNT(*) &gt; 1 LIMIT 1</code> が0行かを見る（数えられなければ False＝安全側）。「複合キーへの合流では『親が単独では一意でない』警告が的外れになり得る」ため。</div><div class="mt"><b>action = &quot;update&quot; / &quot;delete&quot;</b></div><div class="mt">位置（<code>index</code>）でも保存済み <code>from</code>/<code>to</code> 文字列でも指せる。「元に戻す」は index がずれるので from/to で来る。範囲外なら 400。update は <code>cardinality</code> だけを差し替える。</div><div class="mt"><b>action = &quot;remove_pair&quot;</b></div><div class="mt">複合キーから列ペアを1つ外す。<b>探し方が特徴的</b>で、from/to の文字列一致ではなく「表の組が同じで、その列ペアを含む関連」で特定する。</div><pre class="mono small">for k, r in enumerate(rels):
    cand = rel_pairs(r, alias)
    if cand and cand[0] == (fep[0], fep[1]) and cand[1] == (tep[0], tep[1]) \
       and (pair[0], pair[1]) in cand[2]: 見つけた</pre><div class="mt">理由は「from/to の文字列は列を足し引きするたびに変わるので、文字列の完全一致では『元に戻す／やり直す』で見失う（同じ表ペアに複数の関連があっても、列ペアで一意に決まる）」。残りが1ペア以上なら <code>format_endpoint</code> で書き直し（1ペアなら自動的に単独形式に戻る）、0なら関連ごと <code>pop</code>。</div><div class="mt">戻りには <code>add_body</code>（同じ列ペアを <code>add</code> で送り直せる形）を添える。画面の undo/redo が <code>remove_pair</code> ⇄ <code>add</code> を対にして使う。</div></td></tr>
      <tr><td>まとまりメモの点検（POST /api/catalog/group/check）</td><td><div class="mt">「AIに点検させる」ボタン。<code>admin_required</code>。<b>メモは一切書き換えず、指摘のリストを返すだけ</b>。</div><pre class="mono small">llm.is_configured() でなければ 400
findings = llm.review_group_memo(path, group, body[&quot;description&quot;])
→ {ok: true, findings: [{level, line, problem, suggestion}]}</pre><div class="mt"><code>level</code> は <code>err | warn | info</code> に丸められ（それ以外は <code>warn</code>）、画面は <code>err → warn → info</code> の順に並べ替えて <code>alert--&lt;level&gt;</code> で出す。</div><div class="mt"><code>review_group_memo(db_path, group, memo)</code> の中身:</div><div class="mt">・そのまとまりの表（<code>t.startswith(group + &quot;__&quot;)</code>）が無ければ <code>ValueError</code>。<br>・<code>memo</code> が空なら LLM を呼ばず、<code>warn</code>「このまとまりのメモはまだ空です。」を1件返す。「空欄を『点検済み・問題なし』と読ませない（未記入であることを見せる）」ため。<br>・資料は <code>catalog.db_text(&quot;db&quot;, path, tables, full=True)</code> を<b>そのまとまりの表に絞って</b>渡す。<code>db_text</code> は兄弟まとまりの合算指示などの自動生成注記も含むので、AIが「メモに書く必要がないこと」を判断できる。<br>・それに加えて<b>まとまりの外の表を「名前と列だけ」</b>添える。理由がコメントに明記されている。「メモは『複数の表にまたがる前提』を書く欄なので、他のまとまりを指す行が普通にある。絞った資料だけを見せると、実在する表を『存在しません』と誤って指摘する（実際に誤検知した）」。<br>・プロンプトには「上の資料の中にも同じ見出しでメモが載っていることがありますが、それは保存済みの古い版です。点検するのは下の文章です」と明示する。画面から来る <code>description</code> は<b>未保存の編集中テキスト</b>だから。</div><div class="mt">画面側（<code>wireGroupMemo</code>）は点検ボタンを押しても<b>未保存の印（dirty）を付けない</b>（<code>// メモの点検。書き換えないので、未保存の印は付けない</code>）。保存は別の <code>.g-save</code> ボタンで <code>/api/catalog/group</code> を叩き、<code>clearGroupDirty(box)</code> して見出しの「メモあり」バッジを合わせる。まとまりメモは <code>dirty.groups</code> に載っており、右下の一括保存バー・Ctrl+S（<code>saveAllDirty</code>）の対象になる。</div><div class="mt">機械で分かるぶん（存在しない表・まとまりへの参照）は <code>drift_warnings</code> がカタログ画面の上に自動で出しているので、この API は「AIの目に頼るぶんだけ」を返す、という役割分担。</div></td></tr>
      <tr><td>主なデータ構造</td><td>・meta = {tables, groups, relationships, glossary, examples, checks, er_layout, tools, builtin_tools, (title, description)}  ← _META_KEYS の順にYAMLへ書かれる<br>・meta[&quot;tables&quot;][表名] = {description, ai_draft(bool), columns: {列名: {description?, values?}}, primary_key: [列, ...], glossary: {用語: {description, sql}}}<br>・meta[&quot;tables&quot;][表名][&quot;columns&quot;][列名][&quot;values&quot;] = {&quot;1&quot;: &quot;受付&quot;, &quot;2&quot;: &quot;出荷済&quot;}  ← コード値の意味（キーは文字列）<br>・meta[&quot;groups&quot;][接頭辞] = {&quot;description&quot;: str}   ← 接頭辞は表名の &quot;__&quot; の前。表示名は持たない<br>・meta[&quot;relationships&quot;] = [{from: &quot;表.列&quot; | &quot;表.(c1, c2)&quot; | &quot;別名.表.列&quot;, to: 同上, cardinality: &quot;N:1&quot;|&quot;1:N&quot;|&quot;1:1&quot;|&quot;N:M&quot;}]<br>・meta[&quot;glossary&quot;][用語] = {&quot;description&quot;: str, &quot;sql&quot;: str}  ← 表をまたぐ用語。表固有は meta[&quot;tables&quot;][t][&quot;glossary&quot;]<br>・meta[&quot;examples&quot;] = [{q, description?, sql}]（上限 EXAMPLES_MAX=200・dedupe_examples で (q, 正規化SQL) の重複を後勝ちで排除）<br>・meta[&quot;er_layout&quot;] = {&quot;別名.表名&quot;: [x, y]}   ← load_layout が [x,y] 以外の形の項目を読み飛ばす<br>・profile = {file: DBファイル名, key: {v: 2, mtime: float, size: int}, generated_at: ISO文字列, tables: {表名: ...}}<br>・profile[&quot;tables&quot;][表名] = {type: &quot;table&quot;|&quot;view&quot;, columns: [...], fks: [...], row_count: int|None, sample_columns: [列名], sample_rows: [[値]], col_stats: {...}, error?: str}<br>・columns の1要素 = {name, type(宣言型の生文字列), notnull: bool, pk: bool, pk_seq: int(0=非キー、1以上=複合キー内の順)}<br>・fks の1要素 = {from: 子側の列, table: 親の表, to: 親側の列（PRAGMAがNULLなら文字列 &quot;id&quot;）}<br>・col_stats[列名] = {&quot;values&quot;: [[値, 件数], ...]}（distinct 20以下・件数の降順） または {&quot;min&quot;: v, &quot;max&quot;: v}（21種類以上）<br>・結合候補 = {&quot;from&quot;: &quot;表.列&quot;, &quot;to&quot;: &quot;表.列&quot;, &quot;cardinality&quot;: &quot;N:1&quot;, &quot;reason&quot;: 日本語の根拠}<br>・_suggest_values の戻り = (samples: {(表, 列): set[str]}(最大200), pk_values: {(表, 単独PK列): set[str]}(最大20000))<br>・rel_pairs の戻り = ((from別名, from表), (to別名, to表), [(from列, to列), ...]) または None<br>・effective_pk の戻り = ([列名, ...], &quot;override&quot; | &quot;declared&quot; | &quot;none&quot;)<br>・link_check の戻り = {&quot;level&quot;: &quot;ok&quot;|&quot;warn&quot;|&quot;block&quot;, &quot;issues&quot;: [{level, title, detail}]}<br>・collect_edges の1辺 = {id, source, target, from: (別名,表,列), to: 同, pairs: [[from列, to列], ...], from_ref, to_ref, label, cardinality, kind: &quot;fk&quot;|&quot;meta&quot;, owner, index}<br>・drift_warnings の戻り = list[str]（日本語の警告文そのもの。構造化されていない）</td></tr>
      <tr><td>定数・しきい値</td><td>・config.PROFILE_SAMPLE_ROWS = 5 — プロファイルに保存するサンプル行数（SELECT * ... LIMIT 5、ORDER BY なし）<br>・config.PROFILE_LOW_CARDINALITY = 20 — 実値一覧を保持する distinct 数の上限。クエリは LIMIT 21 で撃ち、21件返ったら min/max に切り替える<br>・config.PROFILE_TIMEOUT_SEC = 30 — プロファイリング中の1クエリのタイムアウト（秒）。set_progress_handler(..., 100000) で「最後の reset から」を測る<br>・config.PROFILE_STATS_MAX_ROWS = 2_000_000 — これ以上の行数の表は col_stats をスキップ。row_count が None（COUNT が失敗）でもスキップ<br>・config.PROFILE_CACHE_DIR = DATA_DIR / &quot;.profile_cache&quot; — キャッシュ名は「DBのファイル名 + &quot;.profile.json&quot;」<br>・プロファイル構造バージョン v = 2（profile_db 内の key に埋め込み。上げると全キャッシュが無効）<br>・_suggest_values の標本 = 列あたり DISTINCT 200 件、単独主キー側は DISTINCT 20000 件<br>・join_suggestions: 値の一致率 0% の候補は捨てる（JOINしても0行だから）<br>・join_suggestions: 名前の手がかりが無い発見は一致率 0.9 以上、かつ子・親とも distinct 5 種類以上<br>・join_suggestions: 同名の単独主キーを持つ相手が 4 表以上（len(cands) &gt; 3）で同じまとまりに相手がいなければ候補を出さない<br>・link_check: 親に無い子の値が 30% 以上で warn、それ未満で残があれば info<br>・link_check: 親 distinct &gt;= 10 かつ 子 distinct &lt;= 10 かつ 親カバー率 &lt; 0.5 で「区分値とIDを結んでいる可能性」warn<br>・EXAMPLES_MAX = 200 — 1DBあたりの例文上限（例文は毎回 system prompt に載るため）<br>・_memo_bad_tables のスニペットは &quot;__&quot; の位置から前14文字・後16文字<br>・COL_SEP = &quot;::&quot; — 列ノードIDの区切り（テーブルIDが &quot;別名.表名&quot; なので &quot;.&quot; は使えない）<br>・_CARD_ENDS = {N:1:(*,1), 1:N:(1,*), 1:1:(1,1), N:M:(*,*)} / _CARD_FLIP = {N:1↔1:N, 1:1→1:1, N:M→N:M}<br>・_TEXT_CACHE は 64 件を超えたら丸ごと clear（プロンプト本文のキャッシュ）</td></tr>
    </tbody></table></div>
    <div class="card__title mt">落とし穴（24件）</div>
    <div class="tablewrap"><table class="data"><thead><tr><th style="width:60px">#</th><th>内容</th></tr></thead><tbody>
      <tr><td class="mono small">01</td><td>load_meta はキャッシュの dict 実体をそのまま返す。書き換えると同じファイルを読んだ他の画面・他のリクエストに漏れる。編集するなら必ず load_meta_for_edit（deepcopy）。cleanup 側は load_meta_for_edit を使わず自前で copy.deepcopy しており、そこには「直に触ったせいで削除前の下見が控えを先に消し、本番の掃除が『消すものが無い』と判断してファイルを書かなかった＝消した表の説明が残り続けた」という事故がコメントで残っている。</td></tr>
      <tr><td class="mono small">02</td><td>save_meta は _META_KEYS に無いキーを黙って捨てる。手でYAMLに書き足した独自キーは、画面から1回でも保存すると消える。title / description が _META_KEYS に残っているのは旧形式を読み書きで失わないためだけで、新規には書かれない。</td></tr>
      <tr><td class="mono small">03</td><td>save_meta は引数の dict を破壊的に変更する（caveats を description に合流させて pop する）。呼び出し側が save 後にその dict を再利用すると内容が変わっている。</td></tr>
      <tr><td class="mono small">04</td><td>profile_db のキャッシュ判定は st_mtime（秒精度の float）+ size。_read_yaml が mtime_ns を使い、save_meta がさらに明示的にキャッシュを pop しているのと対照的で、プロファイル側は「サイズが変わらないまま同じ mtime 内に DB が書き換わる」と古い内容を返し得る。取り込み系は force=True、表・ビューの削除／改名は catalog.forget()（キャッシュファイルごと削除）でこれを回避している。</td></tr>
      <tr><td class="mono small">05</td><td>_suggest_values は列の宣言型が厳密に &quot;TEXT&quot; か &quot;INTEGER&quot; の場合しか標本を作らない。&quot;VARCHAR(20)&quot;・&quot;text&quot;・&quot;INT&quot;・型なし（ビューの計算列は空文字になりがち）は全部素通りする。その結果、結合候補の「値の一致 …%」が付かないまま名前だけの推測が表示され、0%で落とすはずのフィルタも効かない。</td></tr>
      <tr><td class="mono small">06</td><td>_suggest_values と join_suggestions が見る主キーは profile の c[&quot;pk&quot;]＝DB宣言の主キーだけで、effective_pk（カタログで人が指定した primary_key）は見ない。CSV取込のように宣言PKが無い表は、カタログで主キーを指定しても結合候補には一切反映されない。</td></tr>
      <tr><td class="mono small">07</td><td>join_suggestions の *_id ヒューリスティックは「表名が base / base+s / base+es と完全一致」を要求する。このアプリの表名は必ず「まとまり__名前」なので、実運用ではまず当たらない。実際に効いているのは (2) 同名列が他表の単独主キー と (4) 値が9割一致 の2本だと理解しておくこと。</td></tr>
      <tr><td class="mono small">08</td><td>join_suggestions 冒頭の <code>if not low.endswith(&quot;_id&quot;) and not low.endswith(&quot;id&quot;)</code> の後半（&quot;id&quot; 止まり）は死に枝。直後の <code>base = low[:-3] if low.endswith(&quot;_id&quot;) else None</code> → <code>if not base: continue</code> で必ず落ちる。</td></tr>
      <tr><td class="mono small">09</td><td>「値の一致 87%」の分母は子側の標本200件（DISTINCT ... LIMIT 200、ORDER BY なし）であって全件ではない。SQLite が返した順の先頭200種に対する率なので、全数の一致率とは一致しない。親側は最大20000件の全値。</td></tr>
      <tr><td class="mono small">10</td><td>drift_warnings が見ていないもの: 表ごとの用語（meta[&quot;tables&quot;][t][&quot;glossary&quot;]）のSQL、ユーザー定義ツール（meta[&quot;tools&quot;]）のSQL、er_layout に残った亡霊キー。表名の亡霊を検査しているのは meta[&quot;glossary&quot;]（DB全体の用語）・examples・checks の3つだけ。</td></tr>
      <tr><td class="mono small">11</td><td>_missing は「&quot;__&quot; を含み、&quot;__&quot; で終わらないトークン」しか表名候補と見なさない。規約から外れた &quot;__&quot; を含まない表名は、消えても例文・検算・用語のどこからも検知されない。</td></tr>
      <tr><td class="mono small">12</td><td>まとまりメモの検査だけ \w+ を使わず「実在表名でメモを塗ってから、残った &quot;__&quot; を拾う」逆引きになっている。Python の \w は日本語も語構成文字なので「品質__defectsは社内で見つけた不良」が丸ごと1語になり、実在表を書いたメモほど誤警告が出た（docstring に実例あり）。</td></tr>
      <tr><td class="mono small">13</td><td>_memo_bad_tables の「まとまり全体を指す書き方」の除外条件は、直前が実在の接頭辞で終わり、かつ &quot;__&quot; の直後の1文字が &quot; *、。」）&quot; のどれか（または行末）であること。「人事_勤怠__の表」のように直後が別の文字だと誤警告になる。prefixes は profile の表名から作られ、meta[&quot;groups&quot;] のキーは使わない。</td></tr>
      <tr><td class="mono small">14</td><td>drift_warnings の関連チェックは parse_endpoint_cols の alias が &quot;@own&quot; のときだけ実表と突き合わせる。他DBを指す端点（alias.table.col）は素通りで、腐っていても警告が出ない。</td></tr>
      <tr><td class="mono small">15</td><td>effective_pk の override は「指定列のうち実在するものだけ残し、1つでも残れば採用」。3列指定して2列が消えても、残った2列が主キー扱いで採用され、消えた1列は別途 drift 警告が出るだけ。一意性はどこでも検証しない。また /api/catalog/primary-key は宣言PKと同じ並びを指定すると override を削除するので、pk_src が declared に戻る。</td></tr>
      <tr><td class="mono small">16</td><td>PRAGMA foreign_key_list の to が NULL（親の主キーを暗黙参照）のとき、コードは literal &quot;id&quot; を入れている。親の主キー名が id でなければ、その FK 線は collect_edges の valid() で列が実在せず黙って消える（エラーも警告も出ない）。</td></tr>
      <tr><td class="mono small">17</td><td>カタログ画面の「実際の値」列（catalog_index）は col_stats の [値, 件数] のペアに str() を掛けているので <code>[&#x27;出荷済&#x27;, 300], [&#x27;受付&#x27;, 120]</code> と表示される。同じ col_stats を使う ER図の table-info は v[0] を取って <code>出荷済, 受付</code> と表示する。同じデータの表示が2箇所で食い違っている。</td></tr>
      <tr><td class="mono small">18</td><td>relationship の add で「逆向きの既存を見つけたら a,b を入れ替える」処理はループ内で行われる。同じ表ペアに順方向と逆方向の関連が両方あると、結果が rels の並び順に依存する。</td></tr>
      <tr><td class="mono small">19</td><td>merge（複合キーへの合流）では合流先の cardinality を書き換えない。新しい列ペアと一緒に送られた多重度は捨てられる。</td></tr>
      <tr><td class="mono small">20</td><td>merge 時の警告の握り潰しは issue の title に &quot;一意ではありません&quot; が含まれるかという部分一致で判定している。link_check の文言を変えると、この補正が黙って効かなくなる。</td></tr>
      <tr><td class="mono small">21</td><td>remove_pair は from/to の文字列一致では関連を探さない。列を足し引きするたびに from/to の文字列が変わるため、文字列一致では undo/redo が対象を見失う。「表ペアが一致し、かつその列ペアを含む」で特定する。</td></tr>
      <tr><td class="mono small">22</td><td>normalize_direction は「片方だけが単独主キー」のときしか向きを直さない。両方が単独主キー（1:1候補）、どちらも主キーでない場合は人が引いた向きのまま保存される。ただし整合性検査側の child_parent が保存後にもう一度主キーで判定し直すので、手書きの .meta.yaml が逆向きでも検査自体は正しい向きで走る。</td></tr>
      <tr><td class="mono small">23</td><td>_make_timeout の30秒は「最後の reset() から」の経過時間。col_stats のループは列ごとに reset するので、1表の走査全体は列数×30秒まで伸び得る（1クエリあたりの上限であって、表あたり・DB全体の上限ではない）。</td></tr>
      <tr><td class="mono small">24</td><td>profile_db のキャッシュ書き込みは json.dumps(..., default=str)。JSON にできない値は文字列化されて保存されるので、生成直後のプロファイルとキャッシュから読んだプロファイルで sample_rows / col_stats の値の型が変わることがある。</td></tr>
    </tbody></table></div>
  </div>

  <div class="card mt">
    <div class="card__title" id="impl-ingest">5-7. 取り込み・改名・削除</div>
    <div class="card__desc">Excel/CSV を唯一の SQLite（data/統合.db）へ書き込む層と、その周辺（形の事前判定、定期実行ジョブ、リアルタイム追随、削除後の後片付け、改名、ビュー）。DB への書き込みは「元 importer.py」セクションだけに閉じ込められており、分析側は読み取り専用接続しか使わない。取り込みの入口は 4 つ（画面の1回きり／ジョブ登録直後の初回／アプリ内スケジューラ／CLI refresh）だが、実処理はすべて import_dataframe に集まり、ジョブ経路はさらに run_job に集約されている。表名は必ず「まとまり__表名」の形を強制し、この接頭辞がカタログ上の「まとまり」になるため、safe_name の table=True フラグと __ の扱いがサブシステム全体の要になっている。</div>
    <div class="tablewrap"><table class="data"><thead><tr><th style="width:210px">項目</th><th>内容</th></tr></thead><tbody>
      <tr><td>全体像とデータの流れ</td><td><pre class="mono small">ファイル（許可フォルダ or アップロード）
  │
  ├─ inspect_file      形だけ見て「そのまま取り込めるか」を判定（読むだけ・止めない）
  │
  ├─ read_table / read_upload      → pandas.DataFrame（dtype=object）
  ├─ plan_columns                  → [{元の列名, 列名, 型}]
  ├─ prepare_frame                 → 全行で型を再検証し、駄目なら TEXT に降格(degraded)
  └─ import_dataframe              → ★唯一の書き込み（CREATE / DROP+CREATE / INSERT）
         └─ prune_runs             → keep_runs を超えた古い「回」を削除</pre><div class="mt">入口は 4 つ。</div><div class="tablewrap"><table class="data"><thead><tr><th>入口</th><th>ルート/関数</th><th>mode</th><th>履歴の kind</th></tr></thead><tbody><tr><td>画面「いま取り込む」</td><td><code>POST /api/import/run</code></td><td>replace のみ（append は 400 で拒否）</td><td><code>manual</code></td></tr><tr><td>ジョブ登録直後の初回</td><td><code>POST /api/jobs/save</code> → <code>run_job</code></td><td>replace のみ</td><td><code>job</code></td></tr><tr><td>アプリ内スケジューラ</td><td><code>scheduler.tick</code> → <code>jobs.run_job</code></td><td>実質 append</td><td><code>auto</code></td></tr><tr><td>CLI</td><td><code>python core.py refresh</code> → <code>refresh_cli</code></td><td>任意</td><td><code>auto</code></td></tr><tr><td>質問のたびの追随</td><td><code>_realtime_refresh</code> → <code>jobs.refresh_realtime</code> → <code>run_job</code></td><td>replace のみ</td><td><code>realtime</code></td></tr></tbody></table></div><div class="mt">画面の UI 上、サーバのフォルダにあるファイルは常に <code>saveJob()</code>（ジョブ登録）へ流れ、<code>/api/import/run</code> を叩くのはアップロード経路だけ。<code>goBtn</code> のハンドラが <code>source.kind === &#x27;upload&#x27;</code> で分岐している。</div><div class="mt">書き込み先の DB はクライアントの指定を一切使わず、<code>db.list_db_files()[0]</code> に固定される（<code>/api/import/run</code>・<code>job_save</code> の両方）。DB は 1 つという設計なので、<code>db_file</code> は実質 <code>統合.db</code> 固定。</div></td></tr>
      <tr><td>取り込み元の許可（どこのファイルを読めるか）</td><td><div class="mt">許可フォルダは <code>config.IMPORT_DIRS</code>（env）＋ 画面から追加した分（<code>data/import_dirs.yaml</code> の <code>dirs:</code>）の和で、<code>allowed_dirs()</code> が <code>resolve()</code> して重複を除いたものを返す。</div><div class="mt">・<code>add_dir</code> は登録の時点で <code>resolve(strict=True)</code> → <code>is_dir()</code> → ルート直下でないこと → <code>iterdir()</code> を 1 件だけ試す、まで実際にやる。本番がネットワークマウントなので「設定はできたが読めない」を後で気づく状況を潰している。<br>・<code>dir_status()</code> は「見つからない（マウントされていない）／フォルダでない／権限なし／利用できます」を切り分けて返す。<br>・<code>is_allowed(path)</code> … 実ファイル＋ノイズでない＋拡張子が <code>IMPORT_EXTENSIONS</code>（小文字比較）＋許可フォルダ配下。<code>resolve(strict=True)</code> を通すので <code>..</code> やシンボリックリンクでの脱出は不可。<br>・<code>is_within_allowed(path)</code> … 拡張子を見ない版。「何が置いてあるか」を一覧する用途（AIツール <code>_listing</code>）で、読めるかどうかは呼び出し側が別に判断する。<br>・<code>is_noise(name)</code> … <code>~$</code>（Excel のロックファイル）、先頭 <code>.</code>、<code>desktop.ini</code> / <code>thumbs.db</code> を除外。<br>・<code>_importer_walk</code> は明示スタックで走査し、<code>resolve()</code> 済みディレクトリを <code>seen_dirs</code> に貯めてリンクの輪を切る。<code>OSError</code> は黙って飛ばす（権限のないフォルダで止まると、その先が全部見えなくなるため）。</div><div class="mt">アップロード（<code>IMPORT_ALLOW_UPLOAD</code>、既定 false）はディスクに置かない。<code>_fs_put</code> でプロセス内の <code>OrderedDict</code>（最大 200 件・古いものから捨てる）に入れ、token を返す。<code>_fs_get</code> は owner が一致しないと None を返す。サーバに残らないので定期取り込みには登録できない（<code>job_save</code> が明示的に 400 を返す）。</div></td></tr>
      <tr><td>形の判定（inspect_file）</td><td><div class="mt">取り込みボタンを押す前に「1行=1レコード / 1列=1項目 の素直な表か」を見る。<b>書き込みは一切しないし、判定が悪くても取り込み API は止めない</b>（助言に徹する設計）。</div><div class="mt">手順:</div><div class="mt">・拡張子が <code>config.IMPORT_EXTENSIONS</code> に無ければ即 <code>対応していない形式</code>。<br>・素の格子として読む。Excel は <code>_grid_excel</code>（<code>read_only=True, data_only=True</code>、先頭 <code>MAX_SCAN_ROWS</code> 行）。テキストは <code>_grid_text</code>（<code>CSV_ENCODINGS</code> を上から試し、<code>.tsv</code> はタブ固定、それ以外は <code>csv.Sniffer</code> で <code>,\t;|</code> から推定、失敗したらタブ数とカンマ数の多い方）。<br>・結合セルは <code>_merged_ranges</code>。read_only では取れないので通常読み込みが要り、<code>MERGE_CHECK_MAX_MB</code> を超えるファイルは調べずに <code>None</code> を返す。<b><code>None</code> は「無かった」ではなく「調べていない」</b>で、後段で「低」の注意として出る。<br>・<code>_guess_header</code> が見出し行（0始まり）を当てる。先頭 <code>HEADER_SEARCH_ROWS</code> 行だけを見て、埋まっているセルが 2 個未満（タイトル行・空行）と、下に中身が無い行を除外し、<code>埋まり具合 + 文字らしさ - 行番号*0.06</code> が最大の行を選ぶ（上の行ほど見出しらしいので優遇）。<br>・<code>_analyze</code> が中身を調べ、<code>_blocks</code> が「空行 2 行以上で切れて再開する塊」を数える。</div><div class="mt">判定項目と深刻度:</div><div class="tablewrap"><table class="data"><thead><tr><th>深刻度</th><th>検出</th><th>条件</th></tr></thead><tbody><tr><td>高</td><td>見出しのセル結合</td><td>横方向の結合で、見出し行またはその1つ上に掛かるもの（最上段1セルの飾りは除外）</td></tr><tr><td>高</td><td>データ部のセル結合</td><td>見出し行より下の結合</td></tr><tr><td>高</td><td>横持ち（クロス表）</td><td><code>_PERIOD_RE</code> に一致する列名が 3 個以上</td></tr><tr><td>高</td><td>見出しが数字</td><td>数値に見える列名が 3 個以上（横持ちの elif 側）</td></tr><tr><td>高</td><td>1シートに複数表</td><td><code>_blocks() &gt; 1</code></td></tr><tr><td>中</td><td>見出しが1行目でない</td><td><code>header_row &gt; 0</code></td></tr><tr><td>中</td><td>合計・小計行</td><td>先頭2セルの文字列に <code>_TOTAL_WORDS</code> を含む行</td></tr><tr><td>中</td><td>列名が空 / 重複 / はみ出し行</td><td>それぞれ検出</td></tr><tr><td>低</td><td>数字と文字の混在列</td><td>非空セルが4個以上で、数値率が 0.6 以上 1.0 未満</td></tr><tr><td>低</td><td>空の列 / 途中の空行 / セル内改行 / 結合未調査</td><td>—</td></tr></tbody></table></div><div class="mt"><code>verdict</code> は issues の level から決まる: 「高」があれば <code>取り込みに向かない</code>、「中」があれば <code>手直しが要る</code>、無ければ <code>そのまま取り込める</code>。<code>summary_line</code> は一覧用の 1 行（先頭 40 文字）。</div><div class="mt">呼び出し元は AI ツール側の <code>_listing</code>（一覧で <code>check=true</code> のとき最大 <code>_MAX_CHECK</code> 件だけ判定）と <code>_preview</code>（1ファイルの詳細）。<code>_preview</code> は <code>inspect_file</code> が当てた <code>header_row</code> をそのまま <code>read_table</code> に渡して読み直す。</div></td></tr>
      <tr><td>読み込み（read_table / read_upload）</td><td><div class="mt">どちらも <code>dtype=object</code> で読む。型は後段で自前に推定するので、pandas に推測させない。</div><div class="mt">・Excel: <code>pd.read_excel(sheet_name=sheet or 0, header=header_row, nrows=..., dtype=object)</code>。<br>・テキスト: <code>sep</code> は明示指定 &gt; <code>.tsv</code> ならタブ &gt; <code>None</code>（pandas の自動判定）。<code>engine=&quot;python&quot;</code>。<code>CSV_ENCODINGS</code> を上から順に試し、<code>UnicodeDecodeError</code> だけを次の候補へ回す。<code>read_table</code> は <code>encoding</code> 引数があればその1つだけを試す。<br>・<code>read_table</code> はファイルサイズ 0 を先に弾く。<code>check_readable</code> が <code>is_allowed</code> と <code>IMPORT_MAX_FILE_MB</code> を確認する。<br>・<code>read_upload</code> は <code>check_upload</code>（<code>IMPORT_ALLOW_UPLOAD</code> / 拡張子 / サイズ）を通してから <code>io.BytesIO</code> で読む。</div><div class="mt"><code>_explain_read_error</code> が pandas / OS の例外を日本語に置き換える。定期取り込みの失敗文はメール・サイドバーの⚠・AI への注記にそのまま載るので、英語のままにしない、というのが理由。扱うのは <code>PermissionError</code>（Excel で開いている）、<code>FileNotFoundError</code>、<code>No columns to parse</code> / <code>EmptyDataError</code>、<code>Worksheet named ...</code>（現存するシート名を並べて出す）、<code>BadZipFile</code>、<code>ParserError</code>。</div></td></tr>
      <tr><td>名前の正規化（safe_name / unique_names）</td><td><pre class="mono small">def safe_name(name, fallback=&quot;col&quot;, *, table=False):
    s = unicodedata.normalize(&quot;NFKC&quot;, str(name)).strip()
    s = re.sub(r&quot;[^\w]&quot;, &quot;_&quot;, s, flags=re.UNICODE)      # \w は日本語も含む＝日本語は残る
    s = re.sub(r&quot;_{2,}&quot;, &quot;__&quot;, s) if table else re.sub(r&quot;_+&quot;, &quot;_&quot;, s)
    s = s.strip(&quot;_&quot;)
    if not s: return fallback
    if s[0].isdigit(): s = &quot;_&quot; + s
    if s.lower() in _RESERVED: s = s + &quot;_&quot;
    return s[:64]</pre><div class="mt"><b><code>table=True</code> が要になる。</b> 既定（列名用）は <code>_+</code> を <code>_</code> 1個に潰すため「まとまり__表名」の <code>__</code> が消え、まとまりに属する表を1つも作れなくなる。表名を扱う箇所はすべて <code>table=True</code> を渡す（<code>import_dataframe</code>・<code>job_save</code>・<code>/api/import/run</code>・<code>prune_runs</code>・<code>run_count</code>・<code>sample_rows</code>・<code>rename_table</code>・<code>view_save</code>・<code>_log_manual</code>）。逆に <code>rename_group</code> の新キーは <code>table=False</code> で呼ぶ（<code>__</code> を含めさせないため。ただし <code>__</code> の検査は safe_name より前に生の入力に対して行う。潰されてしまうと検査が効かない）。</div><div class="mt"><code>unique_names(names)</code> は列名専用。<code>safe_name(n, fallback=f&quot;col{i+1}&quot;)</code> を掛けたうえで、重複には <code>_2</code>, <code>_3</code> … を付ける。表名側には重複解消の仕組みは無い。</div><div class="mt">「まとまり__表名」の強制は 4 か所で行われる: <code>/api/import/run</code>、<code>job_save</code>（<code>safe_name(..., table=True)</code> を掛けたうえで validate）、<code>rename_table</code>、<code>view_save</code>。判定はいずれも <code>&quot;__&quot; not in safe_name(x, table=True).strip(&quot;_&quot;)</code>。</div></td></tr>
      <tr><td>型推定と値の変換</td><td><div class="mt"><code>infer_type(series)</code> の判定順:</div><div class="mt">・NaN と空白だけの値を除く。全部消えたら <code>TEXT</code>。<br>・<code>pd.to_numeric(errors=&quot;coerce&quot;)</code> が全件成功しなければ <code>TEXT</code>。<br>・全部整数で表せて絶対値が <code>2**63</code> 未満なら → <code>_looks_like_code</code> で最終判断。<code>True</code> なら <code>TEXT</code>、そうでなければ <code>INTEGER</code>。<br>・それ以外は <code>REAL</code>。</div><div class="mt"><code>_looks_like_code(values)</code> は「数値にすると元へ戻せない値が1つでもあるか」を見る。</div><div class="mt">・長さ 2 以上で先頭が <code>0</code> かつ 2 文字目が <code>.</code> <code>,</code> でない（郵便番号 <code>0123</code>、製品コード <code>007</code>）<br>・<code>str(int(text)) != text</code>（前後の <code>+</code>、桁区切り、全角数字など）</div><div class="mt"><code>prepare_frame(df, columns)</code> が本番読み込み時にもう一度全行を検証する。型推定はプレビューの先頭 2000 行で行われるので、後ろの行に数値でない値が混ざりうる。「値が入っているのに <code>to_numeric</code> が NaN になる」行が 1 件でもあれば、その列の <code>型</code> を <code>TEXT</code> に書き換えて <code>degraded</code> に積む（黙って NULL にして値を消さないため）。<code>degraded</code> は取り込みメッセージ・ジョブの <code>last_degraded</code>・<code>jobs.problems()</code> の <code>degraded</code> 種別・管理者へのメールまで通る。</div><div class="mt"><code>_cast(series, sqlite_type)</code> は素の Python 値（int / float / str / None）に揃える。numpy の int64 のまま <code>executemany</code> に渡すと sqlite3 がバッファとみなして BLOB で保存してしまい、数値として比較も集計もできなくなるため。</div></td></tr>
      <tr><td>書き込み（import_dataframe）</td><td><pre class="mono small">import_dataframe(db_path, table, df, columns,
                 mode=&quot;create&quot;, timestamp_col=None, timestamp_value=None)
  -&gt; (書き込んだ行数, TEXTに降格した列名のリスト)</pre><div class="mt">事前チェック（すべて <code>ImportError_</code> を投げる = 画面にそのまま出せる日本語）:</div><div class="mt">・<code>db_path.parent.resolve() != config.DATA_DIR.resolve()</code> → 「data/ の直下にしか作れません」<br>・<code>table = safe_name(table, fallback=&quot;&quot;, table=True)</code> が空 → 「テーブル名を入力してください」<br>・<code>len(df) &gt; config.IMPORT_MAX_ROWS</code><br>・<code>columns</code> が空</div><div class="mt">取得日時列:</div><div class="mt">・<code>ts_name = safe_name(timestamp_col, fallback=&quot;取得日時&quot;)</code>。元データの列名とぶつかったらエラー（黙って上書きしない）。<br>・値は <code>timestamp_value</code> があればそれ、無ければ <code>datetime.now().isoformat(timespec=&quot;seconds&quot;)</code>。<b>列全体に同じ1つの値</b>を入れる。これが「1回の取り込み＝取得日時の1つの値」という keep_runs の数え方の土台。<br>・<code>run_job</code> は <code>started</code>（ジョブ開始時刻）を渡す。<code>/api/import/run</code> は渡さないので <code>import_dataframe</code> 内の now になる。</div><div class="mt">モード別:</div><div class="tablewrap"><table class="data"><thead><tr><th>mode</th><th>動き</th></tr></thead><tbody><tr><td><code>create</code></td><td>既にあれば <code>ImportError_</code>。無ければ CREATE TABLE + INSERT</td></tr><tr><td><code>replace</code></td><td><code>DROP TABLE IF EXISTS</code> → CREATE TABLE → INSERT</td></tr><tr><td><code>append</code></td><td>既存の列と照合。無い列があれば <code>ImportError_</code>。ただし取得日時列だけは <code>ALTER TABLE ... ADD COLUMN &lt;ts&gt; TEXT</code> で後から足す。その後 INSERT</td></tr></tbody></table></div><div class="mt">接続は <code>sqlite3.connect(db_path, timeout=30)</code>。裏のスケジューラと画面からの操作が重なっても即エラーにせず順番待ちさせるため。INSERT は <code>executemany</code>、失敗時は <code>rollback()</code> して <code>ImportError_(&quot;書き込みに失敗しました: ...&quot;)</code>。</div><div class="mt">0 件のデータは <code>import_dataframe</code> では弾かない。弾くのは <code>_run_job_locked</code> の側（下記）。</div></td></tr>
      <tr><td>取得日時列と keep_runs（prune_runs）</td><td><div class="mt">「回」＝取得日時列の <b>distinct な値の数</b>。1回の取り込みで入った行はすべて同じ値を持つので、これで回数を数えられる。</div><pre class="mono small">DELETE FROM &lt;table&gt;
 WHERE &lt;ts&gt; IS NOT NULL
   AND &lt;ts&gt; NOT IN (SELECT &lt;ts&gt; FROM &lt;table&gt; WHERE &lt;ts&gt; IS NOT NULL
                     GROUP BY &lt;ts&gt; ORDER BY &lt;ts&gt; DESC LIMIT ?)</pre><div class="mt">・<code>keep &lt; 1</code> または <code>timestamp_col</code> が空なら 0 を返して何もしない。<br>・<code>ts</code> がテーブルに無ければ 0 を返す。<br>・<b><code>&lt;ts&gt; IS NULL</code> の行は消さない。</b> この仕組みを入れる前から入っていた行を守るため。<br>・<code>ORDER BY &lt;ts&gt; DESC</code> は TEXT の辞書順。ISO 8601（<code>2026-09-08T12:34:56</code>）だから時系列と一致する、という前提に乗っている。<br>・戻り値は削除行数（<code>cursor.rowcount</code>）。</div><div class="mt">読み出し系の補助:</div><div class="mt">・<code>run_count(db_path, table, ts)</code> … <code>COUNT(DISTINCT ts)</code>。いま何回分あるか。<br>・<code>table_info(db_path, table, timestamp_col)</code> … 行数、列、<code>runs</code>（distinct 数）、<code>oldest</code> / <code>latest</code>。取得日時列は「ジョブ設定 → <code>config.IMPORT_TIMESTAMP_COLUMN</code>」の順に、実在する列名を探す。<br>・<code>sample_rows(...)</code> … 取得日時列があれば <code>ORDER BY &lt;ts&gt; DESC</code> で取る。「さっきの取り込みが入ったか」を見るのが用途なので、先頭から取ると古い行しか見えない。BLOB は <code>v.hex()[:32]</code> に潰して JSON に載せる。</div></td></tr>
      <tr><td>定期実行ジョブ（jobs）</td><td><div class="mt">定義は <code>data/import_jobs.yaml</code>（<code>{jobs: [...]}</code> または素のリスト）。DB が全ユーザー共通なのでジョブも共通。<code>_jobs_lock</code>（RLock）が定義ファイルの書き換えとジョブ実行を直列化する。</div><div class="mt"><b>検証（validate_job）</b></div><div class="mt">・保存先（db_file・table）と取り込み元（source）が必須。<br>・<code>start_at</code> は ISO 文字列。<code>check_start=True</code>（新規登録）のときだけ、<code>now - START_GRACE_MINUTES</code> より過去を拒否。登録済みジョブの間隔変更・停止/再開は <code>check_start=False</code> で通す。<br>・<b><code>timestamp_column</code> は mode によらず必須。</b> 全件入れ替えでも「いつ時点のデータか」が分からないと分析で断面を説明できないため。<br>・<code>realtime</code> × <code>append</code> は禁止（追記で毎回読み直すと取得日時が質問のたびに増え、保存回数の意味が壊れる）。<br>・<code>append</code> は <code>interval_minutes &gt; 0</code> が必須（いつ溜めるかが決まっていないと意味をなさない）。<br>・<code>append</code> は <code>keep_runs</code> が必須で <code>1 &lt;= keep &lt;= MAX_KEEP_RUNS</code>。</div><div class="mt"><b>job_save が強制する形</b></div><div class="mt">画面もサーバも、取り込み方は 2 通りしか作らせない。API を直接叩かれても同じ形に寄せる。</div><pre class="mono small">mode == &quot;append&quot;  → realtime = False           （interval はクライアント指定）
mode != &quot;append&quot;  → realtime = True, interval_minutes = 0</pre><div class="mt">つまり <b>「定期実行の全件入れ替え」というジョブは画面からは作れない</b>。全件入れ替えは「ファイルの鏡写し」なのでリアルタイム追随に任せ、追記は「時系列で溜める」ので定期実行に任せる、という割り切り。</div><div class="mt"><b>重複防止</b></div><div class="mt">・<code>find_duplicate</code> … 同じ (source, sheet, db_file, table)。パスは <code>os.path.normcase(os.path.normpath(...))</code> で比較。同じ設定が 2 つあると同時刻に 2 回追記され、同じ取得日時なので keep_runs が 1 回分とみなして全行が二重に残る。<br>・<code>find_target_clash</code> … 同じ (db_file, table) を狙う <b>別の取り込み元</b>。許すと、どちらかのファイルが更新されるたびに表の中身が入れ替わる綱引きになる。1テーブル＝取り込み設定1本。</div><div class="mt"><b>実行タイミング</b></div><pre class="mono small">next_run_at(job):
  interval &lt;= 0            → None（手動のみ）
  last_run が無い          → start_at があればその時刻、無ければ now（＝すぐ対象）
  last_run がある          → last_run + interval、start_at があれば max(それ, start_at)
is_due(job, now): enabled かつ next_run_at is not None かつ next_run_at &lt;= now</pre><div class="mt">次回は「前回の<b>実行開始</b>時刻 + 間隔」で決まる。だから手で余計に走らせると予定がずれる。</div><div class="mt"><b>manual_run_blocked</b></div><div class="mt"><code>interval_minutes &gt; 0</code> かつ <code>mode == &quot;append&quot;</code> のときだけ理由文字列を返す。理由は 2 つ:</div><div class="mt">・次回予定が後ろにずれる<br>・保存回数を 1 回ぶん余計に使い、その回だけ間隔の違うデータが混ざる</div><div class="mt">これが効くのは <code>POST /api/jobs/run</code>（400）と <code>/api/import/run</code>（<code>_locked_tables()</code> 経由で 400）と画面のボタン無効化。job_save の強制により append ジョブは必ず interval &gt; 0 なので、<b>実質すべての追記ジョブが手動実行禁止</b>。</div><div class="mt"><b>run_job / _run_job_locked</b></div><div class="mt"><code>run_job</code> は <code>_jobs_lock</code> を取って <code>_run_job_locked</code> を呼ぶだけ。<b>例外は投げず</b>、<code>{&quot;ok&quot;, &quot;rows&quot;, &quot;message&quot;, &quot;degraded&quot;}</code>（append なら <code>removed</code> / <code>kept</code> も）を返す。1 本こけても他を止めないため。</div><div class="mt">・<code>importer.is_allowed(path)</code> を確認（移動・削除・許可フォルダ設定の変更を検出）<br>・<code>read_table(sheet, header_row, delimiter)</code><br>・列の照合。<code>job[&quot;columns&quot;]</code>（登録時のスナップショット）の <code>元の列名</code> がファイル側に無ければ失敗。<b>1列も合わないとき</b>は「区切り文字・見出し行・シートが変わった」という別メッセージにする（列名の変更ではないから）。<br>・<code>len(df) == 0</code> なら失敗させて止める。見出しだけのファイルで全件入れ替えするとテーブルが空になって「成功」で終わるため、前回の内容を残す。<br>・<code>import_dataframe(..., timestamp_value=started.isoformat())</code><br>・append かつ <code>keep_runs</code> があれば <code>prune_runs</code> → <code>run_count</code>。メッセージに <code>保持 N/M回（古い X行を削除）</code> を足す。<br>・結果をジョブ定義に書き戻す（<code>last_run</code>=開始時刻, <code>last_status</code>, <code>last_message</code>, <code>last_rows</code>, <code>last_degraded</code>）。成功時のみ <code>source_stamp</code> を更新。<br>・<code>history.add_import_record(...)</code> に 1 件残す。</div><div class="mt"><b>problems()（設定どおりに更新できていないジョブ）</b></div><div class="mt">有効なジョブだけを見て、先に当たった 1 種類だけを返す（continue で打ち切る）。</div><div class="tablewrap"><table class="data"><thead><tr><th>kind</th><th>条件</th></tr></thead><tbody><tr><td><code>failed</code></td><td><code>last_status == &quot;error&quot;</code></td></tr><tr><td><code>degraded</code></td><td><code>last_degraded</code> が空でない</td></tr><tr><td><code>overdue</code></td><td><code>interval &gt; 0</code> かつ <code>last_run</code> があり、<code>now - last_run &gt; interval * 2</code></td></tr></tbody></table></div><div class="mt">この 1 か所の判定を、チャットのサイドバーの⚠、AI の回答への注記、管理者へのメール（<code>mailer.alert_import_problems</code>）の 3 つが共有する。<code>problems_by_table()</code> は <code>{(db_file, table): [...]}</code> に畳んだ形。</div></td></tr>
      <tr><td>リアルタイム更新（refresh_realtime）</td><td><div class="mt"><code>_begin_turn</code>（/send と /stream の共通前処理）から、スコープ確定後・システムプロンプト構築前に <code>_realtime_refresh(scope)</code> が呼ばれる。<b>質問のたびに走る。</b></div><div class="mt"><code>realtime_jobs()</code> = <code>realtime</code> が真 かつ <code>enabled</code> かつ mode が append でないジョブ。</div><div class="mt">各ジョブについて:</div><div class="mt">・<code>job[&quot;db_file&quot;]</code> が scope の DB 名に無ければスキップ（<b>テーブル単位では絞らない</b>。DB が 1 つの本構成では実質すべての realtime ジョブが毎回対象）。<br>・<code>_source_stamp(job)</code> = <code>f&quot;{st.st_mtime_ns}:{st.st_size}&quot;</code>。中身を読まずに版を判定する。<br>・stamp が空（ファイルが見当たらない）→ 取り込まず、前回の内容のまま答える。<code>_note_realtime_failure</code> でジョブに <code>last_status=&quot;error&quot;</code> を書き、履歴に <code>kind=&quot;realtime&quot;</code> の失敗を 1 件残す。<code>last_run</code> と <code>source_stamp</code> は触らない（実行していないので「最後に動いた時刻」は変わらないし、ファイルが戻ったとき版が違えば取り込み直せるようにするため）。同じ理由で既に記録済みなら何も書かない（質問のたびに呼ばれるので、状態が変わったときだけ書く）。<br>・stamp が <code>job[&quot;source_stamp&quot;]</code> と同じ → 何もしない。ただし直前が <code>error</code> だった場合（ファイルが消えて、同じ内容のまま戻ってきた場合）は <code>last_status=&quot;ok&quot;</code> に戻して⚠を下ろす。下ろさないと次にファイルが変わるまで警告が出続ける。<br>・変わっていれば <code>run_job(job, kind=&quot;realtime&quot;)</code>。版の記録は run_job 側（成功時のみ）なので、失敗したら次の質問で再挑戦する。</div><div class="mt"><code>_realtime_refresh</code> は例外を握って <code>print</code> するだけで質問は止めない（読めなければ前回取り込んだ内容で答える、が決めごと）。</div></td></tr>
      <tr><td>スケジューラと CLI</td><td><div class="mt"><b>アプリ内スケジューラ（元 scheduler.py）</b></div><div class="mt"><code>create_app()</code> から <code>scheduler.start()</code>。<code>config.IMPORT_SCHEDULER</code> が false なら起動しない。二重起動の防止はフラグではなくスレッド名 <code>aiagent-import-scheduler</code> の生存確認（<code>is_running()</code>）で行う。</div><div class="mt"><code>_loop</code>:</div><pre class="mono small">while not _stop.is_set():
    try: tick(); _state[&quot;last_error&quot;] = None
    except Exception as e: _state[&quot;last_error&quot;] = str(e)   # 1周こけても止めない
    _stop.wait(max(5, config.IMPORT_SCHEDULER_TICK_SEC))</pre><div class="mt"><code>sleep</code> ではなく <code>Event.wait</code> なのは、停止の合図で即座に抜けるため。<code>stop()</code> は <code>atexit</code> に登録され、寝ているスレッドを起こして join する（daemon スレッドを寝かせたままプロセスを終えると、後始末中に標準出力を掴んだままになって異常終了することがある）。<code>_scheduler_log</code> は <code>_stop</code> が立っていると何も出さない。</div><div class="mt"><code>tick()</code>:</div><div class="mt">・<code>jobs.due_jobs()</code> を順に <code>jobs.run_job(job)</code>（kind は既定の <code>&quot;auto&quot;</code>）<br>・<code>_state</code> を更新（<code>last_tick</code>, <code>tick_count</code>, <code>last_ran</code> は直近10件）<br>・<code>jobs.problems()</code> を取り、モジュール変数 <code>_prev_problems</code> と比べて <b>変わり目だけ</b> 管理者に通知（<code>mailer.alert_import_problems(cur, prev)</code>）。<code>tick_count &gt; 1</code> から通知するので、起動直後の1周目は送らない。</div><div class="mt"><code>scheduler_status()</code> は <code>_state</code> に <code>running</code> / <code>tick_sec</code> / <code>enabled</code> を足したもの。取り込み画面の「DBの管理」タブに出る。</div><div class="mt"><b>CLI（<code>python core.py refresh</code>）</b></div><pre class="mono small">（引数なし） jobs.due_jobs()                                期限が来たものだけ
--all       enabled なジョブ全部                            期限を無視
--job &lt;ID&gt;  1本だけ
--list      一覧表示のみ</pre><div class="mt">終了コードは 0=全成功または対象なし / 1=1本でも失敗。スケジューラを切って cron 運用する場合の口。</div></td></tr>
      <tr><td>削除と後片付け（drop_table → cleanup.clean_table）</td><td><div class="mt">削除は 2 段。<b>DROP は importer 側、掃除は cleanup 側</b>で、<code>clean_table</code> 単体では表は消えない。</div><div class="mt"><b>drop_table（実物を落とす）</b></div><pre class="mono small">row = conn.execute(&quot;SELECT name, type FROM sqlite_master WHERE name = ? COLLATE NOCASE&quot;, (table,)).fetchone()
if row is None: raise ImportError_(f&quot;&#x27;{table}&#x27; はこのDBにありません。&quot;)
conn.execute(f&quot;DROP {&#x27;VIEW&#x27; if row[1]==&#x27;view&#x27; else &#x27;TABLE&#x27;} IF EXISTS {qi(row[0])}&quot;)
return row[0]      # 実物の綴りを返す</pre><div class="mt">・ビューと表で文が違い、両方撃つのは誤り（SQLite は種類が違うと IF EXISTS でも例外にする）。だから先に種類を見る。<br>・<code>COLLATE NOCASE</code> で探すのは、DROP 側が綴りの大小を吸収するのに探す側が BINARY だと「見つからない→黙って何もしない」になり、呼び出し元は掃除だけ進めて <b>表は残るのに知識だけ消える</b> ため。<br>・戻り値の実物の綴りで掃除するのが呼び出し規約（<code>_w_drop_table</code> は <code>table = importer.drop_table(path, table)</code> と受け直している）。</div><div class="mt"><b>_scrub_meta（メタ 1 ファイルぶんの掃除）</b></div><div class="mt"><code>_scrub_meta(meta, own_alias, alias, table)</code> は <code>meta</code> をその場で書き換え、消したものを <code>{relationships, glossary, examples, checks, tables, er_layout}</code> の形で返す。<code>table=None</code> ならその DB への参照すべて。</div><div class="mt"><b>自分の DB か他所の DB かで消す範囲が変わる</b>（<code>mine = own_alias == alias</code>）:</div><div class="tablewrap"><table class="data"><thead><tr><th>対象</th><th>自分の DB</th><th>他の DB</th></tr></thead><tbody><tr><td><code>relationships</code>（端点が (alias, table) を指す）</td><td>消す</td><td>消す</td></tr><tr><td><code>er_layout</code>（キー <code>&quot;alias.table&quot;</code>）</td><td>消す</td><td>消す</td></tr><tr><td><code>tables</code>（表の説明・列の説明）</td><td>消す</td><td>残す</td></tr><tr><td><code>glossary</code>（<b>SQL式が</b>その表を引くものだけ）</td><td>消す</td><td>残す</td></tr><tr><td><code>examples</code>（SQL がその表を引くもの）</td><td>消す</td><td>残す</td></tr><tr><td><code>checks</code>（left/right/drilldown のどれかが引く）</td><td>消す</td><td>残す</td></tr></tbody></table></div><div class="mt">他所の DB で説明系を残すのは、例文が他 DB の表を引くこともあるから。用語は「SQL式が表名を書いているもの」だけ消す。説明文だけの用語は、文中に表名が出てきても残す（文章だから）。</div><div class="mt">判定は <code>uses_table(sql, table, alias)</code>。構文解析はせず、<code>&quot;orders&quot;</code> と <code>&quot;demo_sales.orders&quot;</code> の両方を境界つき正規表現で探す。取りこぼすより拾いすぎる方がまし、ただし何を消したかは必ず報告する、という方針。</div><div class="mt"><b>_cleanup_walk（全 DB を巡る）</b></div><pre class="mono small">for f in db.list_db_files():
    if f == skip: continue
    meta = copy.deepcopy(catalog.load_meta(f))   # ← deepcopy 必須
    hit = _scrub_meta(meta, db.alias_for(f), alias, table)
    if any(hit.values()):
        _merge(found, own, hit)
        if apply: catalog.save_meta(f, meta)</pre><div class="mt"><code>apply=False</code> が下見（<code>table_impact</code>）、<code>True</code> が本番（<code>clean_table</code>）。</div><div class="mt"><b>clean_table</b></div><div class="mt">・<code>_cleanup_walk(alias, table, apply=True)</code> で全 DB のメタを掃除<br>・<code>drop_jobs</code>（既定 True）なら、その (db_file, table) を狙う定期取り込みを <code>jobs.delete_job</code> で消す。残すと消したテーブルが次の実行で復活する。<br>・<code>catalog.forget(path)</code>（プロファイルキャッシュのファイルとテキストキャッシュを捨てる）<br>・<b>まとまりの最後の表が消えたら、まとまりのメモも片づける。</b> <code>table</code> に <code>__</code> があれば接頭辞を取り、<code>profile_db</code> で <code>pref + &quot;__&quot;</code> で始まる表が 1 つも無ければ <code>meta[&quot;groups&quot;][pref]</code> を pop して保存し、<code>done[&quot;groups&quot;]</code> に記録。残すと「無いデータの前提」だけが AI に渡り続ける。</div><div class="mt"><b>table_impact（下見・何も書き換えない）</b></div><div class="mt"><code>_cleanup_walk(apply=False)</code> に加えて:</div><div class="mt">・<code>jobs</code> … 巻き添えになる定期取り込み（<code>_job_text</code> が <code>名前（表 / 間隔・停止中）</code> を作る）<br>・<code>orphan_terms</code> … <code>_orphan_terms(path, table)</code>。「SQL に表名が書かれていないが、その表の列だけで成立していて、他のどの表でも成立しない」全体用語を列挙する。自動削除は表名の有無で判定するので <code>minutes &gt;= 60</code> のような式はどの表を消しても残る。残った式は検証も整合性の警告も効かなくなるので、削除の確認画面で人に見せて判断を委ねる。<b>数えるだけで消さない。</b></div><div class="mt"><code>summarize(impact)</code> が <code>LABELS</code> の順に <code>[{key, label, items}]</code> に整形する（空は落とす）。</div><div class="mt">入口: <code>GET /api/import/impact</code>（下見）、<code>POST /api/import/drop-table</code>（実行、<code>drop_jobs</code> を body で指定可）。</div></td></tr>
      <tr><td>改名（rename_table / rename_group）</td><td><div class="mt"><b>_rename_in_text</b></div><pre class="mono small">re.sub(r&quot;(?&lt;!\w)&quot; + re.escape(old) + r&quot;(?!\w)&quot;, new, text)</pre><div class="mt">境界を Unicode の語構成文字（<code>\w</code>）で見る。英数字だけの境界では「品質__x」が「高品質__x」の一部に当たる事故が起きる。SQL にも散文にも同じものを使う。</div><div class="mt"><b>rename_table(path, old, new)</b></div><div class="mt">検査（すべて <code>ValueError</code> → API は 400）:</div><div class="mt">・<code>new = safe_name(new, table=True)</code><br>・<code>old</code> が <code>profile_db(path)[&quot;tables&quot;]</code> にあること（views も含む）<br>・<code>&quot;__&quot; in new.strip(&quot;_&quot;)</code>（まとまり必須）<br>・<code>new != old</code>、<code>new</code> が既存でないこと</div><div class="mt">手順:</div><div class="mt">・<code>.meta.yaml</code> の全文を <code>meta_backup</code> に控える<br>・<code>ALTER TABLE old RENAME TO new</code>（<code>sqlite3.connect(timeout=30)</code>）<br>・<b>カタログは YAML 全文への境界つき置換で一括更新</b>。表名は十分に固有なので、説明・SQL・関連の端点・ER 配置キー・ユーザー定義ツールの SQL のどこに現れても同じ置き換えでよい。置換後の文字列を <code>yaml.safe_load</code> し、<code>catalog.save_meta</code> に通して形を正規化して保存する。<br>・<b>まとまり（接頭辞キー）は名前の一部ではないので別扱い。</b> 旧接頭辞 ≠ 新接頭辞 で、旧まとまりに他の表が残っていなければ <code>groups[old_g]</code> を pop し、新キーが未使用なら <code>groups[new_g]</code> に引き継ぐ（<code>moved_memo</code> に旧キーを記録）。削除時と同じ考え方。<br>・定期取り込み: <code>jobs._read()</code> を直接いじり、<code>db_file</code> と <code>table</code> が一致するジョブの <code>table</code> を差し替え、<code>name</code> にも <code>_rename_in_text</code> を掛けて <code>jobs._write()</code>。<br>・利用者ごとの選択: <code>config.USER_META_DIR/*/prefs.yaml</code> を glob し、<code>tables_off</code> リストの中の <code>old</code> を <code>new</code> に置き換えて書き戻す（<code>prefs</code> モジュールを通さず直接書く）。<br>・3〜6 のどこかで例外が出たら <b>実表を元の名前に戻し、<code>.meta.yaml</code> を控えから書き戻し</b>、<code>catalog.forget</code> して再送出。<br>・最後に <code>catalog.forget(path)</code>。</div><div class="mt">戻り値 <code>{old, new, jobs, prefs, memo_moved}</code>。</div><div class="mt"><b>rename_group(path, old_key, new_key)</b></div><div class="mt">・<code>&quot;__&quot; in new_key</code>（<b>生の入力に対して</b>）を先に弾く。safe_name が <code>__</code> を潰すので、後に回すと検査が効かない。<br>・<code>new_key = safe_name(new_key)</code>（table=False）<br>・対象は <code>t.split(&quot;__&quot;, 1)[0] == old_key and &quot;__&quot; in t</code> の全表<br>・<b>先に全部の衝突を確かめてから</b>始める（途中で止まると半端になる）<br>・あとは 1 表ずつ <code>rename_table(path, t, new_key + &quot;__&quot; + rest)</code> を回す</div><div class="mt">入口: <code>POST /api/catalog/rename-table</code> / <code>POST /api/catalog/rename-group</code>。どちらも <code>admin_required</code>。</div></td></tr>
      <tr><td>ビュー（実体を持たない、名前を付けた SELECT）</td><td><div class="mt">表と同じ規約「まとまり__名前」で作るので、登録すると表一覧・ER 図・チャットの表選択にそのまま出る。カタログ側は名前で引くだけなので追加実装が要らない。</div><div class="mt"><b>検査と作成</b></div><div class="mt">・<code>_view_check_sql(sql)</code> … 末尾の <code>;</code> を落とし、<code>db.validate_select</code> を通す（複数文禁止、<code>SELECT</code> / <code>WITH</code> 始まり、書き込み・DDL キーワード禁止）。<br>・<code>_view_run(path, sql, limit)</code> … 実データで動かして <code>{columns, rows, total}</code> を返す。<code>total</code> は <code>SELECT COUNT(*) FROM (&lt;sql&gt;)</code>、失敗しても本体は見せる。<br>・<code>create_view(db_path, name, sql, replace=False)</code> … <code>data/</code> の外は拒否。<code>sqlite_master</code> で同名を引き、<b>表なら拒否</b>（取り違え防止）、ビューで <code>replace=False</code> なら拒否、ビューで replace なら <code>DROP VIEW IF EXISTS</code> してから <code>CREATE VIEW ... AS &lt;sql&gt;</code>。</div><div class="mt"><b>API</b></div><div class="tablewrap"><table class="data"><thead><tr><th>ルート</th><th>内容</th></tr></thead><tbody><tr><td><code>POST /api/catalog/view/preview</code></td><td>保存せず実データで動かす</td></tr><tr><td><code>POST /api/catalog/view/draft</code></td><td>日本語の目的から AI に下書きさせる。実データに当てて失敗したらエラーを添えて <b>1 回だけ</b> 書き直させる（<code>for _attempt in range(2)</code>）。AI が「作らない方がよい」と返したら <code>ok:false</code> + <code>reason</code> を 200 で返す</td></tr><tr><td><code>POST /api/catalog/view</code></td><td>新規・作り直し・改名。説明も同時に保存</td></tr><tr><td><code>POST /api/catalog/view/delete</code></td><td>削除 + 後片付け</td></tr></tbody></table></div><div class="mt"><code>view_save</code> の順序:</div><div class="mt">・<code>name = safe_name(name, table=True)</code>、<code>&quot;__&quot;</code> 必須<br>・<code>_view_check_sql</code><br>・<code>profile_db</code> で同名が「ビュー以外の実体」なら拒否<br>・<b>改名は旧名が本当にビューのときだけ許す</b>（<code>old not in {v[&quot;name&quot;] for v in list_views(path)}</code> なら 400）<br>・<code>_view_run(limit=1)</code> で <b>保存前に必ず動かす</b><br>・<code>create_view(replace = (name == old or bool(existing)))</code><br>・改名なら <code>drop_table(path, old)</code> で旧ビューを落とす<br>・カタログの <code>tables</code> エントリを <code>old</code> から <code>name</code> へ移し替え（説明・列の説明を引き継ぐ）、<code>description</code> を保存、<code>catalog.forget</code></div><div class="mt"><code>view_delete</code> は <code>drop_table</code> → <code>cleanup.clean_table(path, name, drop_jobs=False)</code>。ビューに定期取り込みは付かないので、ジョブは触らない。</div><div class="mt"><code>_views_payload(path)</code> が画面に渡す一覧。<code>view_body</code> は保存済みの <code>CREATE VIEW ... AS</code> の後ろを <code>re.search(r&quot;\bAS\b\s*(.+)$&quot;, sql, re.S|re.I)</code> で切り出す。</div></td></tr>
      <tr><td>更新履歴（history）</td><td><div class="mt"><code>data/import_history.jsonl</code>（1行1件の JSON）。YAML ではなく追記型なのは、実行のたびに全件を書き直したくないため。手動も定期も同じ形で残し、<code>kind</code> で区別する。</div><div class="mt"><code>IMPORT_RECORD_KINDS = {&quot;manual&quot;: &quot;手動&quot;, &quot;auto&quot;: &quot;定期&quot;, &quot;job&quot;: &quot;定期（手動実行）&quot;, &quot;realtime&quot;: &quot;リアルタイム&quot;}</code></div><div class="mt"><code>add_import_record</code> は <code>_history_lock</code> の下で 1 行追記し、行数カウンタ <code>_count</code> を進めて <code>_trim_if_needed</code>。カウンタはプロセス内変数で、初回は <code>_line_count</code> で数え直す。上限 <code>config.IMPORT_HISTORY_MAX</code> の 1.1 倍を超えてから、新しい方だけを残してまとめて間引く（毎回書き直すと重い）。<b>記録に失敗しても取り込み自体は止めない</b>（print して続行）。</div><div class="mt">読み出し: <code>for_table(db_file, table, limit)</code>、<code>recent_import_records(limit)</code>、<code>counts()</code>、<code>latest_by_source()</code>（AI ツールの「取り込み状況」列が使う）。<code>_newest_first</code> は「先に並びを逆にしてから安定ソート」する。<code>at</code> が秒までしか無いので、同じ秒の中は「後に書いた方が新しい」で決めるため。</div></td></tr>
      <tr><td>HTTP API 一覧（すべて admin_required）</td><td><div class="tablewrap"><table class="data"><thead><tr><th>メソッド・パス</th><th>関数</th><th>内容</th></tr></thead><tbody><tr><td>GET <code>/import</code></td><td><code>import_index</code></td><td>取り込み画面。<code>dir_status</code> / <code>existing_tables</code> / <code>_group_choices</code> / <code>_manage_view</code> を渡す</td></tr><tr><td>GET/POST <code>/api/import/dirs</code></td><td><code>dirs_list</code> / <code>dirs_edit</code></td><td>取り込み元フォルダの一覧・追加・削除</td></tr><tr><td>POST <code>/api/import/browse</code></td><td><code>_w_browse</code></td><td>フォルダを1階層開く（許可フォルダの外は開かない）</td></tr><tr><td>POST <code>/api/import/upload</code></td><td><code>upload</code></td><td>アップロード受け取り（メモリ、token 返却）</td></tr><tr><td>POST <code>/api/import/preview</code></td><td><code>_w_preview</code></td><td>先頭 2000 行を読んで列プラン・サンプル行・推奨表名を返す</td></tr><tr><td>POST <code>/api/import/run</code></td><td><code>run</code></td><td>1回きりの取り込み（append は 400。<code>_locked_tables</code> も見る）</td></tr><tr><td>GET <code>/api/import/manage</code></td><td><code>manage_view</code></td><td>「DBの管理」タブの中身</td></tr><tr><td>GET <code>/api/import/table</code></td><td><code>table_detail</code></td><td>開いたテーブルのサンプル行と更新履歴</td></tr><tr><td>GET <code>/api/import/impact</code></td><td><code>impact</code></td><td>削除の下見</td></tr><tr><td>POST <code>/api/import/drop-table</code></td><td><code>_w_drop_table</code></td><td>削除＋後片付け</td></tr><tr><td>POST <code>/api/jobs/save</code></td><td><code>job_save</code></td><td>ジョブ登録。replace なら直後に 1 回実行</td></tr><tr><td>POST <code>/api/jobs/run</code></td><td><code>job_run</code></td><td>「▶ 今すぐ更新」。<code>manual_run_blocked</code> を見る</td></tr><tr><td>POST <code>/api/jobs/update</code></td><td><code>job_update</code></td><td>enabled / interval / realtime の変更（<code>check_start=False</code>）</td></tr><tr><td>POST <code>/api/jobs/delete</code></td><td><code>job_delete</code></td><td>ジョブ削除</td></tr><tr><td>POST <code>/api/catalog/rename-table</code></td><td><code>api_rename_table</code></td><td>表の改名（まとまりの移動も同じ口）</td></tr><tr><td>POST <code>/api/catalog/rename-group</code></td><td><code>api_rename_group</code></td><td>まとまりキーの一括改名</td></tr><tr><td>POST <code>/api/catalog/view*</code></td><td><code>view_preview</code> / <code>view_draft</code> / <code>view_save</code> / <code>view_delete</code></td><td>ビュー</td></tr></tbody></table></div><div class="mt">取り込みが成功したら呼び出し側が <code>catalog.profile_db(db_path, force=True)</code> でプロファイルを取り直す（<code>/api/import/run</code>、<code>job_save</code> の初回、<code>job_run</code>）。</div></td></tr>
      <tr><td>主なデータ構造</td><td>・job = {id: 12桁hex, name, source(絶対パス), sheet|None, header_row(int,0始まり), delimiter|None, db_file, table, mode(&#x27;replace&#x27;|&#x27;append&#x27;), timestamp_column|None, keep_runs|None, start_at(&#x27;YYYY-MM-DDTHH:MM&#x27;), interval_minutes(int), realtime(bool), enabled(bool), columns[], created_at, last_run, last_status(&#x27;ok&#x27;|&#x27;error&#x27;), last_message, last_rows, last_degraded[], source_stamp(&#x27;&lt;mtime_ns&gt;:&lt;size&gt;&#x27;)}<br>・columns（列プラン）= [{&quot;元の列名&quot;: 元ファイルの見出し, &quot;列名&quot;: safe_name後, &quot;型&quot;: &quot;TEXT&quot;|&quot;INTEGER&quot;|&quot;REAL&quot;}] ※prepare_frame が「型」をその場で TEXT に書き換えることがある<br>・write_cols（import_dataframe 内部）= [{&quot;列名&quot;, &quot;型&quot;}] … columns から作り、取得日時列を末尾に足したもの。CREATE TABLE と INSERT の列順はこれ<br>・inspect_file の戻り = {file, sheet, sheets[], header_row(0始まり), verdict, issues[], shape{列数,読んだ行数,見出し行}, columns[], encoding?, delimiter?}<br>・issue = {level: &quot;高&quot;|&quot;中&quot;|&quot;低&quot;, text: 何が起きているか, fix: 直し方}<br>・import_dataframe の戻り = (書き込んだ行数:int, TEXTに降格した列名:list[str])<br>・run_job の戻り = {ok: bool, rows: int, message: str, degraded: [列名], removed?: int, kept?: int}<br>・problems() の要素 = {id, name, db_file, table, kind: &quot;failed&quot;|&quot;degraded&quot;|&quot;overdue&quot;, since(last_run), message}<br>・履歴レコード = {at, db_file, table, ok, kind, mode, rows, removed, kept, keep, source, sheet, job_id, job_name, user, message, seconds}<br>・_scrub_meta の hit / clean_table・table_impact の戻り = {relationships[], glossary[], examples[], checks[], tables[], er_layout[], jobs[], groups[], orphan_terms[]}（各要素は {db, text}。ただし jobs は table_impact のとき {id, name, text}）<br>・table_info の戻り = {name, columns[], column_count, rows, timestamp_column, runs(distinct数), latest, oldest, error?}<br>・_manage_view の戻り = {dbs: [{name, size, mtime, tables: [{...table_info, jobs: [_job_row]}]}], orphans: [_job_row], locked: {db_file: {table: 理由}}, sched: scheduler_status()}<br>・scope（realtime のフィルタに使う）= [{path, alias, name(=DBファイル名), tables?}]<br>・アップロード預かり物 = {data: bytes, filename, mime, owner} を token をキーに OrderedDict で保持</td></tr>
      <tr><td>定数・しきい値</td><td>・MAX_SCAN_ROWS = 200（core.py 冒頭 filecheck セクション）… 形を見るために読む最大行数<br>・HEADER_SEARCH_ROWS = 12 … 見出し行を探す範囲。これより下に見出しがある表は当てられない<br>・MERGE_CHECK_MAX_MB = 20 … これを超えるExcelは結合セルを調べず None（＝「調べていない」）を返す<br>・_TOTAL_WORDS = (&quot;合計&quot;,&quot;総計&quot;,&quot;小計&quot;,&quot;計&quot;,&quot;累計&quot;,&quot;total&quot;,&quot;subtotal&quot;,&quot;sum&quot;) … 行頭2セルにあると合計行とみなす<br>・CSV_ENCODINGS = [&quot;utf-8-sig&quot;, &quot;cp932&quot;, &quot;utf-8&quot;, &quot;shift_jis&quot;, &quot;euc_jp&quot;] … 上から順に試す<br>・config.IMPORT_EXTENSIONS = (&quot;.csv&quot;, &quot;.tsv&quot;, &quot;.txt&quot;, &quot;.xlsx&quot;, &quot;.xlsm&quot;)（config.py・env では変えられない定数）<br>・config.IMPORT_MAX_FILE_MB = 100（env IMPORT_MAX_FILE_MB）<br>・config.IMPORT_MAX_ROWS = 1_000_000（env IMPORT_MAX_ROWS）… import_dataframe が超過を拒否<br>・config.IMPORT_PREVIEW_ROWS = 30 … 画面に見せる行数。ただしプレビューが読むのは nrows=2000（/api/import/preview のハードコード）<br>・config.IMPORT_SCAN_DEPTH = 0（env）… 0 は「無制限」という意味のある値。未指定は None で区別する<br>・config.IMPORT_MAX_FILES = 2000（env）… list_all_files の打ち切り<br>・config.IMPORT_SAMPLE_ROWS = 20（env）… sample_rows の既定<br>・config.IMPORT_TIMESTAMP_COLUMN = &quot;取得日時&quot;（env）… ジョブに設定が無いときの既定列名<br>・config.IMPORT_SCHEDULER = true / IMPORT_SCHEDULER_TICK_SEC = 60（env）… ただし実際の待ちは max(5, tick) 秒<br>・config.IMPORT_HISTORY_MAX = 5000（env）… 1.1倍を超えてから間引く<br>・config.IMPORT_ALLOW_UPLOAD = false（env、既定 false）/ IMPORT_DIRS_EDITABLE = true（env）<br>・jobs.MAX_KEEP_RUNS = 800 … 保存回数の上限。決めておかないと日次で回すだけで表が際限なく膨らむ<br>・jobs.DEFAULT_KEEP_RUNS = None … 既定値をあえて置かない（業務ごとに違うので必ず自分で決めさせる）<br>・jobs.START_GRACE_MINUTES = 2 … 開始日時が「過去」かの判定の許容。送信のタイムラグ対策<br>・jobs.INTERVALS = {手動のみ:0, 15分ごと:15, 1時間ごと:60, 3時間ごと:180, 6時間ごと:360, 1日ごと:1440, 1週間ごと:10080}<br>・importer.DELIMITERS = {自動判定:None, カンマ:&quot;,&quot;, タブ:&quot;\t&quot;, パイプ:&quot;|&quot;, セミコロン:&quot;;&quot;, 空白（連続もまとめる）:&quot;\\s+&quot;}<br>・safe_name の切り詰め = 64文字（return s[:64]）<br>・INTEGER 判定の上限 = abs(値) &lt; 2**63（infer_type）<br>・sqlite3.connect(..., timeout=30) … import_dataframe / prune_runs / rename_table の書き込み接続<br>・scheduler の tick_count &gt; 1 から通知（起動直後の1周目は「変化」とみなさない）<br>・AIツール側: _MAX_ROWS=300（一覧件数）、_MAX_PREVIEW_ROWS=20、_MAX_CHECK=20（1件ずつ開くので形の判定はここまで）<br>・VIEW_PREVIEW_ROWS = 20 / view_draft の再試行は 1 回だけ（for _attempt in range(2)）<br>・_fs（アップロード預かり）_MAX_ITEMS = 200、LRU で古いものから破棄</td></tr>
    </tbody></table></div>
    <div class="card__title mt">落とし穴（36件）</div>
    <div class="tablewrap"><table class="data"><thead><tr><th style="width:60px">#</th><th>内容</th></tr></thead><tbody>
      <tr><td class="mono small">01</td><td>safe_name の table=True を落とすと『まとまり』が壊れる。既定（列名用）は <code>_+</code> を <code>_</code> 1個に潰すので「まとまり__表名」の __ が消える。表名を扱う全箇所（import_dataframe / job_save / /api/import/run / prune_runs / run_count / sample_rows / rename_table / view_save / _log_manual）が table=True を渡している。逆に列名側は table=False なので、元ファイルの列名に __ が含まれると _ 1個に潰れて列名が変わる。</td></tr>
      <tr><td class="mono small">02</td><td>safe_name は最後に s[:64] で切る。表名の切り詰めによる衝突を解消する仕組みは無い（unique_names があるのは列名だけ）。65文字以上の表名を 2 つ作ると、先頭64文字が同じなら import_dataframe が「既にあります」または既存表への追記になる。</td></tr>
      <tr><td class="mono small">03</td><td>existing_tables は type=&#x27;table&#x27; しか見ない。同名のビューがあると have=False になり、mode=&#x27;create&#x27;/&#x27;append&#x27; は CREATE TABLE が『view X already exists』で、mode=&#x27;replace&#x27; は DROP TABLE IF EXISTS が『use DROP VIEW to delete view X』で落ちる。どちらも「書き込みに失敗しました: ...」という一般的な文言になり、原因（ビューと衝突している）が読み取れない。取り込み画面の existing 一覧にもビューは出ない。</td></tr>
      <tr><td class="mono small">04</td><td>append で対象テーブルが存在しないと、エラーにならず黙って CREATE TABLE する（have=False の分岐）。表名の打ち間違いは「新しい表が1つできる」という形で現れる。</td></tr>
      <tr><td class="mono small">05</td><td>append は『追記先に無い列』は弾くが、『追記先にあって今回無い列』は素通りする（INSERT が列名を明示するので NULL が入る）。列が減ったファイルは、警告なく NULL 行が積み上がる。</td></tr>
      <tr><td class="mono small">06</td><td>prepare_frame の TEXT 降格（degraded）が効くのは write_cols の「型」だけで、CREATE TABLE のときしか使われない。append で既存列が INTEGER のまま今回だけ降格した場合、テーブル定義は変わらず、SQLite の型親和性に任されることになる。</td></tr>
      <tr><td class="mono small">07</td><td>prune_runs の『回』は取得日時列の distinct 値。ORDER BY は TEXT の辞書順なので ISO 8601（YYYY-MM-DDTHH:MM:SS）前提。列名だけ合わせて別形式の日時（&#x27;2026/9/8 12:34&#x27; など）を手で入れると、古い回が新しいと判定されて残り、新しい回が消える。</td></tr>
      <tr><td class="mono small">08</td><td>prune_runs は &lt;ts&gt; IS NULL の行を絶対に消さない。取得日時の仕組みを入れる前の行を守るためだが、裏返すと、いくら keep_runs を絞っても NULL 行は永久に残り、行数が減らない原因になる。</td></tr>
      <tr><td class="mono small">09</td><td>run_job は終了時に <code>saved = get_job(job.id) or dict(job)</code> → <code>save_job(saved)</code> する。実行中に画面からそのジョブを削除すると、実行完了時に定義ファイルへ書き戻されて復活する。</td></tr>
      <tr><td class="mono small">10</td><td>validate_job は mode によらず timestamp_column を必須にする。全件入れ替えでも必須なのは『いつ時点のデータか』が分からないと分析で断面を説明できないから。API を直接叩いても通らない。</td></tr>
      <tr><td class="mono small">11</td><td>job_save は mode から realtime と interval を強制的に決める（append→realtime=False、それ以外→realtime=True かつ interval_minutes=0）。クライアントが何を送っても上書きされるので、画面からもAPIからも『定期実行の全件入れ替え』ジョブは作れない。</td></tr>
      <tr><td class="mono small">12</td><td>この強制の結果、append ジョブは必ず interval&gt;0 になり、manual_run_blocked が必ず真になる。つまり実質すべての追記ジョブは画面から手動実行できない。</td></tr>
      <tr><td class="mono small">13</td><td>ところが CLI の <code>python core.py refresh --all</code> は manual_run_blocked を通らない。追記ジョブを予定外に1回走らせて保存回数を1つ消費し、次回予定もずらす（ヘルプにも注記あり）。cron に --all を仕込むと追記の間隔設計が黙って崩れる。</td></tr>
      <tr><td class="mono small">14</td><td>next_run_at は last_run（＝実行の開始時刻）＋interval で決まるので、手で走らせるたびに以後の予定が後ろへずれていく。これが manual_run_blocked の存在理由そのもの。</td></tr>
      <tr><td class="mono small">15</td><td>refresh_realtime は scope の DB 名でしか絞らない（テーブル単位では絞らない）。DB が1つしかない本構成では、質問のたびに全 realtime ジョブの元ファイルを stat しに行く。</td></tr>
      <tr><td class="mono small">16</td><td>_source_stamt は mtime_ns:size のみ。ファイルサイズも更新時刻も変わらない書き換え（同じバイト数の上書き）は検出できない。逆にネットワーク共有で mtime の精度が落ちると取りこぼす。</td></tr>
      <tr><td class="mono small">17</td><td>realtime の失敗記録（_note_realtime_failure）は last_run を更新しない。したがって problems() の overdue 判定にも影響しない。復旧の検出は『stamp が source_stamp と一致した』経路でしか起きないので、ファイルが別内容で戻ってきたときは run_job 側で、同内容で戻ってきたときは警告解除だけ、という2経路になっている。</td></tr>
      <tr><td class="mono small">18</td><td>_cleanup_walk が copy.deepcopy(catalog.load_meta(f)) するのは必須。load_meta はキャッシュそのものを返すので、下見（apply=False）が直に触るとキャッシュ側を先に消してしまい、本番の掃除が「消すものが無い」と判断してファイルを書き換えず、削除した表の説明が残り続ける。</td></tr>
      <tr><td class="mono small">19</td><td>_scrub_meta は tools（ユーザー定義ツール）と builtin_tools を見ない。表を消してもツールの SQL は残り、table_impact にも出ないので、消した表を引くツールが黙って残る。一方 rename_table は YAML 全文置換なのでツールの SQL も追随する。削除と改名で扱いが非対称。</td></tr>
      <tr><td class="mono small">20</td><td>clean_table は DROP TABLE をしない（呼び出し側が importer.drop_table 済みである前提）。逆に drop_table は掃除をしない。片方だけ呼ぶと『知識だけ残る』か『表だけ残る』になる。drop_table が実物の綴りを返すのは、その戻り値で掃除を呼ばせるため。</td></tr>
      <tr><td class="mono small">21</td><td>rename_table は catalog.save_meta を通すので、_META_KEYS（tables, groups, relationships, glossary, examples, checks, er_layout, tools, builtin_tools, title, description）に無いキーは改名のたびに消える。手で足した独自キーは残らない。</td></tr>
      <tr><td class="mono small">22</td><td>_rename_in_text が置き換えるのは『まとまり__表名』という完全な表名だけ。まとまりメモの本文に書かれた裸のまとまり名は置換されず古いまま残る。これを拾うために drift_warnings 側にまとまりメモの検査（_memo_bad_tables と「存在しないまとまりを案内している」）が入っている。</td></tr>
      <tr><td class="mono small">23</td><td>rename_table をビュー名に対して呼ぶと ALTER TABLE が OperationalError（view v may not be altered）になる。この例外は ALTER の try/finally（except 無し）を素通りしてルートの except Exception に落ちるため、画面には『改名に失敗しました（元に戻しました）』と出るが、実際にはロールバック処理に入る前なので何も戻していない（何も変わっていない）。</td></tr>
      <tr><td class="mono small">24</td><td>SQLite は ALTER TABLE ... RENAME TO のときに依存するビューの定義SQLを自動で書き換える。だから表を改名してもビューは壊れないが、それはアプリ側が何かしているのではなく SQLite の挙動。rename_table のロールバック（新→旧の再 ALTER）でも同じ仕組みで戻る。</td></tr>
      <tr><td class="mono small">25</td><td>rename_group は先に全メンバーの衝突を確認してから 1 表ずつ rename_table する。衝突以外の理由（ビューが混ざっている、権限など）で途中失敗すると、前半だけ改名された中途半端な状態が残る。</td></tr>
      <tr><td class="mono small">26</td><td>create_view の同名チェックは <code>WHERE name = ?</code>（COLLATE NOCASE なし）だが、drop_table は COLLATE NOCASE。綴りの大小だけが違う名前を渡すと、create_view は「無い」と判断して CREATE VIEW を撃ち、SQLite 側で衝突エラーになる。</td></tr>
      <tr><td class="mono small">27</td><td>view_save の 21570 行付近のコメントは『drop_table は DROP VIEW のあとに DROP TABLE も撃つので』と書いてあるが、drop_table は sqlite_master で種類を判定してから1文だけ撃つ実装に変わっている。コメントが実装より古い。ただし『old が本当にビューか』の検査自体は今も必要（実テーブル名を old に入れられると中身ごと消えるため）。</td></tr>
      <tr><td class="mono small">28</td><td>filecheck の関数が inspect ではなく inspect_file なのは、1ファイル化でモジュールスコープが1つになった結果、標準ライブラリの inspect を import している後ろのセクションに名前を食われて機能が死ぬため。同じ理由で _importer_walk / _importer_qi のように接頭辞つきの名前がある。</td></tr>
      <tr><td class="mono small">29</td><td>_grid_text の中に <code>from importer import CSV_ENCODINGS</code> が残っているが、core.py 冒頭で sys.modules[&quot;importer&quot;] = 自分自身 に張り替えているので、これは自己インポートになる。CSV_ENCODINGS の定義（10028行あたり）は _grid_text の定義（2523行）より後ろだが、関数内 import なので呼び出し時に解決されて動く。</td></tr>
      <tr><td class="mono small">30</td><td>inspect_file の verdict が『取り込みに向かない』でも、取り込み API は一切止めない。判定はあくまで人が押す前の助言で、最終判断は人に委ねる設計。</td></tr>
      <tr><td class="mono small">31</td><td>/api/import/run と job_save は body の db_file を無視して db.list_db_files()[0] を使う。DB を1つだけ持つ設計の帰結で、API を直接叩いても保存先は選べない。</td></tr>
      <tr><td class="mono small">32</td><td>/api/import/run は mode=&#x27;append&#x27; を無条件で 400 にする。追記の入口はジョブ登録だけ。画面のボタンも upload×append を無効化しているが、これは二重の防御。</td></tr>
      <tr><td class="mono small">33</td><td>import 画面のプレビューは nrows=2000 でしか読まない。型はこの 2000 行から推定され、本番読み込みで prepare_frame が全行を見て降格する。だから「プレビューでは INTEGER だったのに TEXT で入った」は正常動作（degraded として警告が出る）。</td></tr>
      <tr><td class="mono small">34</td><td>_merged_ranges が返す None は「結合セルが無かった」ではなく「大きすぎて調べていない」。inspect_file はこれを『低』の注意として出すが、verdict には影響しないので、20MB超のExcelは多段見出しでも『そのまま取り込める』と表示されうる。</td></tr>
      <tr><td class="mono small">35</td><td>rename_table の prefs.yaml 書き換えは prefs モジュールを通さず直接 yaml で読み書きする。_prefs_lock を取らないうえ、prefs._save が行う KEYS フィルタも掛からない（＝ KEYS 外のキーも保存される）。</td></tr>
      <tr><td class="mono small">36</td><td>history の行数カウンタ _count はプロセス内変数。cron の <code>python core.py refresh</code> が別プロセスで書くとずれるが、間引きは後追いで効けばよいという割り切り。</td></tr>
    </tbody></table></div>
  </div>

  <div class="card mt">
    <div class="card__title" id="impl-rag">5-8. 文書検索（LightRAG）</div>
    <div class="card__desc">社内文書はアプリ本体ではなく、別に立てた LightRAG サーバ群（1台＝1ナレッジベース、以下KB）にHTTPで問い合わせる。1回の <code>search_knowledge_base</code> 呼び出しで、その利用者が選んでいる全KBへ ThreadPoolExecutor で並列 fan-out し（<code>rag_retrieve_all</code>）、返ってきたチャンクを KB 横断のラウンドロビンで文字数予算内に詰め直して（<code>rag_merge_context</code>）、本文＋出典リストをツール戻り値として Agent に返す。LightRAG 側の回答生成（<code>/query</code> の bypass）は一切使わず <code>/query/data</code> の「検索だけ」に限定しており、文章を書くのは常にこのアプリの Agent 側である（SQL集計結果やExcelの中身と突き合わせた回答を書かせるため）。KB の登録は管理者（<code>data/knowledge_bases.json</code>）、そのうちどれを検索するか・検索の効き方は利用者ごとの prefs（<code>rag_off</code> / <code>rag_settings</code>）で決まる。</div>
    <div class="tablewrap"><table class="data"><thead><tr><th style="width:210px">項目</th><th>内容</th></tr></thead><tbody>
      <tr><td>全体の流れ（1回の検索で何が起きるか）</td><td><pre class="mono small">LLM が search_knowledge_base を tool_call
  → dispatch()  … _coerce_lists / _missing_required を通す
  → _search_knowledge_base(args, scope)   ※ scope は未使用
      1. query の空チェック
      2. rag_targets()          … kb_enabled() − rag_excluded_ids()（スレッドローカルの利用者）
      3. args.knowledge_bases があれば名前で絞る（未知の名前は即エラー）
      4. rag_user_settings()    … prefs の rag_settings を rag_defaults() に重ねる
      5. args.chunk_top_k があれば上書き（上限あり）
      6. rag_retrieve_all()     … 全KBへ並列 POST /query/data
      7. 全滅なら rag_all_failed_message() で _err
      8. rag_merge_context()    … ラウンドロビン＋文字数予算
      9. llm_content(JSON) と render(kind=&quot;sources&quot;) を返す</pre><div class="mt">呼ばれるまでの前提が2つある。</div><div class="mt">・<b>ツール宣言そのものが動的</b>。<code>build_tools</code> は <code>BUILTIN_TOOLS</code> を回すとき <code>_DYNAMIC_TOOLS = {&quot;search_knowledge_base&quot;}</code> に入っている名前を飛ばし、代わりに <code>knowledge_tool_schemas()</code> が返したものを足す。KB が0件なら空リストが返るので、宣言ごと LLM に渡らない（存在しない情報源を探させても往復と費用が増えるだけ、という判断）。<br>・<b>システムプロンプト側にも同じ一覧が入る</b>。<code>build_system_prompt</code> が <code>rag_targets()</code> を引いて「社内文書（ナレッジベース）」の節を組み立てる。0件ならこの節ごと出さない。出典番号の付け方・推測禁止・食い違いは両論併記、というルールはここと、ツール戻り値の <code>note</code> の二重で言い聞かせている。</div></td></tr>
      <tr><td>RagClient — LightRAG 1台へのHTTPクライアント</td><td><div class="mt">LightRAG はライブラリとして抱き込まず、必ず HTTP API 経由で触る（索引作成が重く別サーバ・別GPUで動かしたい／IT部門からは「URLとAPIキー」の形でしか払い出されない）。公開しているのは <code>health()</code> と <code>retrieve()</code> の2つだけ。</div><div class="mt"><b>認証</b>: <code>_headers()</code> は <code>Content-Type: application/json</code>。<code>api_key</code> が空でなければ <code>X-API-Key</code> を足す（LightRAG の認証ヘッダ）。</div><div class="mt"><b>retrieve() が送る payload</b>（<code>POST {base_url}/query/data</code>）:</div><div class="tablewrap"><table class="data"><thead><tr><th>キー</th><th>値</th></tr></thead><tbody><tr><td><code>query</code></td><td>質問文字列（AIが組み立てた検索語）</td></tr><tr><td><code>mode</code></td><td><code>settings[&quot;retrieve_mode&quot;]</code>（mix / hybrid / local / global / naive）</td></tr><tr><td><code>chunk_top_k</code></td><td><code>settings[&quot;chunk_top_k&quot;]</code></td></tr><tr><td><code>include_chunk_content</code></td><td>常に <code>True</code>（本文が要るので固定）</td></tr><tr><td><code>top_k</code></td><td><code>top_k is not None</code> のときだけ足す</td></tr></tbody></table></div><div class="mt">応答は <code>body[&quot;status&quot;]</code> が <code>None</code> でも <code>&quot;success&quot;</code> でもなければ <code>RagError(body[&quot;message&quot;])</code>。つまり <b>status キーが無い応答は成功扱い</b>。本文は <code>body[&quot;data&quot;][&quot;chunks&quot;]</code>。</div><div class="mt"><b>_post() のエラー分岐（この順）</b>:</div><div class="mt">・<code>requests</code> 未インストール → <code>_REQUESTS_MISSING</code><br>・<code>_requests.Timeout</code> → 「タイムアウトしました（N秒）: URL」（秒数を文面に入れるため、ここだけ <code>_rag_describe</code> を通さない）<br>・<code>_requests.RequestException</code> → <code>_rag_describe(exc, url)</code><br>・<code>status_code in (401, 403)</code> → 「APIキーが拒否されました」<br>・<code>status_code &gt;= 400</code> → <code>HTTP {code}: {_rag_error_message(resp)}</code><br>・JSON パース失敗 → 「応答をJSONとして解釈できませんでした。」</div><div class="mt"><b>health() は2本叩く</b>。LightRAG の <code>/health</code> は認証不要で、APIキーが誤っていても 200 を返す（構成の詳細が伏せられるだけ）。これだけで済ませると「接続成功」と出たのに検索は全部403、を見逃す。そこで <code>health()</code> は <code>/health</code> の後に <code>_verify_credentials()</code> を呼び、保護された <code>/documents/pipeline_status</code> を GET して 401/403 を確かめる。APIキー未設定で 401/403 のときだけ文面が「この環境はAPIキーを要求します」に変わる。</div></td></tr>
      <tr><td>_rag_describe — 接続エラーの切り分け</td><td><div class="mt"><code>requests</code> の例外文字列をそのまま出すと読めないうえ、綴り違い・FW・プロトコル取り違えがどれも同じ見た目になる。管理画面で環境を登録するのはこの機能の主要操作なので、ここで「何を直せばよいか」まで日本語にする。</div><div class="mt"><b>判定順が重要</b>。<code>SSLError</code> / <code>ProxyError</code> / <code>ConnectTimeout</code> はいずれも <code>ConnectionError</code> のサブクラスなので、先に見ないと握り潰される。</div><div class="tablewrap"><table class="data"><thead><tr><th>判定</th><th>出す文面の主旨</th></tr></thead><tbody><tr><td><code>SSLError</code></td><td>http/https の取り違え、社内CA証明書が信頼済みか</td></tr><tr><td><code>ProxyError</code></td><td><code>HTTP_PROXY</code> / <code>NO_PROXY</code> の設定</td></tr><tr><td><code>Timeout</code></td><td>ネットワーク経路とファイアウォール</td></tr><tr><td><code>ConnectionError</code> かつ本文に <code>NameResolutionError</code> / <code>getaddrinfo failed</code> / <code>Name or service not known</code> / <code>nodename nor servname</code> を含む</td><td>ホスト名を解決できない。URLの綴りと社内DNS</td></tr><tr><td>上記以外の <code>ConnectionError</code></td><td>接続拒否。ポート番号とサーバ起動状態</td></tr><tr><td>それ以外</td><td><code>接続に失敗しました: URL（例外クラス名）</code></td></tr></tbody></table></div><div class="mt">エラー本文の整形は2段。<code>_rag_error_message(resp, limit=300)</code> は LightRAG の失敗応答 <code>{&quot;status&quot;,&quot;message&quot;,&quot;data&quot;,&quot;metadata&quot;}</code> から <code>message</code> → <code>detail</code> → <code>error</code> の順に文字列を拾い、無ければ <code>_rag_safe_body</code>。<code>_rag_safe_body(resp, limit=300)</code> は本文の改行を空白に潰して300文字で切り、超過分は <code>…</code> を足す。生JSONをそのまま画面に出すと環境の数だけ同じ塊が並んで読めなくなるため。</div></td></tr>
      <tr><td>登録簿（管理者側）と接続テスト</td><td><div class="mt"><code>data/knowledge_bases.json</code>（<code>config.KNOWLEDGE_BASES_FILE</code>）に JSON の配列で持つ。<code>_kb_write</code> は <code>.json.tmp</code> に書いて <code>os.replace</code> で差し替え、そのあと <code>os.chmod(0o600)</code> を試みる（APIキーが平文で入るため。失敗は握り潰す＝Windows等で落ちない）。読み書きは <code>_kb_lock</code>（<code>threading.Lock</code>）で直列化。</div><div class="mt">・<code>kb_add</code> … <code>base_url</code> は <code>_kb_normalize_url</code> で末尾スラッシュ除去＋スキーム無しなら <code>http://</code> を付与。<b>URL重複と名前重複の両方を弾く</b>。名前を一意にするのは、名前がそのまま AI に見せるツールの選択肢（enum）になるから — 重なると AI も人もどちらを指しているか決められない。id は <code>uuid4().hex[:12]</code>。<br>・<code>kb_update</code> … <b>空文字の <code>api_key</code> は「変更なし」</b>。画面はキーを伏せて表示するので未入力＝据え置きが自然、という判断。<br>・<code>kb_list</code> / <code>kb_get</code> は既定で <code>_kb_redact</code>（<code>api_key</code> を落として <code>has_api_key: bool</code> を足す）。実値は <code>GET /api/knowledge/&lt;id&gt;/key</code>（admin_required）を押したときだけ返す — 一覧に埋め込むと管理画面を開くたびにキーがHTMLとして流れ、キャッシュやソース表示に残るため。<br>・<code>kb_test</code> … <code>health()</code> を呼び、<code>{ok, status, detail}</code> を返す。<code>detail</code> は <code>status / core_version / api_version / pipeline_busy</code> だけに絞る。</div><div class="mt">Webエンドポイント（すべて <code>admin_required</code>、<code>bp_knowledge</code>）: <code>GET /knowledge</code>, <code>POST /api/knowledge</code>, <code>POST /api/knowledge/&lt;id&gt;</code>, <code>POST /api/knowledge/&lt;id&gt;/delete</code>, <code>POST /api/knowledge/&lt;id&gt;/test</code>, <code>GET /api/knowledge/&lt;id&gt;/key</code>。</div><div class="mt">接続テストだけ <b>失敗しても 200 に <code>ok:false</code> を載せて返す</b>（<code>RegistryError</code> は 404）。つながらないのは「この画面で確かめたい結果」であってAPIの失敗ではなく、500 にすると画面側がネットワーク不調と区別できず原因の文面も出せないため。</div></td></tr>
      <tr><td>利用者ごとの選択（rag_excluded_ids）</td><td><div class="mt">prefs（<code>data/users/&lt;ユーザー&gt;/prefs.yaml</code>、キーは <code>KEYS = (&quot;model&quot;, &quot;rag_off&quot;, &quot;rag_settings&quot;, &quot;tables_off&quot;)</code>）に <b>「外したもの」を保存する</b>。</div><div class="mt">選択リスト方式（選んだものを保存）にすると、管理者が新しいKBを足したとき既存の利用者全員にそれが見えないままになる。除外方式なら新しいものは既定で検索対象に入る。まったく同じ理由で表の選択も <code>excluded_tables</code> / <code>tables_off</code> が除外方式になっている。</div><pre class="mono small">rag_targets(user) = [e for e in kb_enabled() if e[&quot;id&quot;] not in set(rag_excluded_ids(user))]
rag_available(user) = bool(rag_targets(user))</pre><div class="mt"><code>kb_enabled()</code> は <code>enabled</code> が真のものだけ（管理者が無効にした環境はチャット側の一覧にそもそも出ない。逆に利用者が外しただけの環境は他人の検索対象には残る）。</div><div class="mt"><b>利用者をどう渡しているか</b>: <code>dispatch</code> は引数に利用者を持たない（35個のツールすべての形が変わるため）。代わりに <code>_rag_local = threading.local()</code> に置き、<code>rag.set_current_user(user)</code> で入れる。<code>rag_user_settings</code> / <code>rag_excluded_ids</code> / <code>excluded_tables</code> は <code>user or _current_user()</code> で引く。呼んでいるのは3か所。</div><div class="tablewrap"><table class="data"><thead><tr><th>場所</th><th>理由</th></tr></thead><tbody><tr><td><code>_begin_turn</code>（<code>/api/chat/send</code> と <code>/api/chat/stream</code> の共通前処理）</td><td>リクエストを処理しているスレッドに入れる</td></tr><tr><td><code>/api/chat/stream</code> の <code>generate()</code> の冒頭</td><td>応答を流す処理が別スレッドで回る構成でも引けるように（<code>_begin_turn</code> で入れたものはそのスレッドには無い）</td></tr><tr><td><code>/api/chat/rewind</code>（発言の書き直し）</td><td>書き直しも1回のターン。送信と同じ下ごしらえをする（ここが抜けていて、前の質問で同じスレッドを使った別の利用者の設定で検索していた）</td></tr></tbody></table></div><div class="mt"><code>rag_retrieve_all</code> が <code>environments</code> と <code>settings</code> を <b>引数で受け取る</b>のはこれと表裏。ワーカースレッドにはスレッドローカルが伝播しないので、fan-out する前に呼び出し元が解決しておく必要がある。</div><div class="mt">チャット開始の門番: <code>_begin_turn</code> と <code>/api/chat/rewind</code> はどちらも <code>if not scope and not rag.rag_available(g.user)</code> で止める。DBが1つも無くてもKBがあれば文書には答えられ、両方無いときだけ止める。rewind 側にも同じ条件を置いてあるのは、ここだけ厳しいと「書き直しだけ通らない」になるため。</div></td></tr>
      <tr><td>検索設定（RAG_SPECS）</td><td><div class="mt"><code>RAG_SPECS</code> が唯一の正本で、画面のフォーム定義・入力検証・初期値・保存がすべてこの1つのタプルから作られる。項目を増やすときはここに1行足すだけでよい。</div><div class="tablewrap"><table class="data"><thead><tr><th>キー</th><th>種類</th><th>範囲</th><th>既定（config）</th></tr></thead><tbody><tr><td><code>retrieve_mode</code></td><td>choice</td><td><code>_RAG_MODES</code> の5つ</td><td><code>RAG_RETRIEVE_MODE</code>=<code>mix</code></td></tr><tr><td><code>chunk_top_k</code></td><td>int</td><td>1〜100</td><td><code>RAG_CHUNK_TOP_K</code>=10</td></tr><tr><td><code>top_k</code></td><td>int</td><td>1〜200</td><td><code>RAG_TOP_K</code>=40</td></tr><tr><td><code>max_context_chars</code></td><td>int</td><td>1000〜20000</td><td><code>RAG_MAX_CONTEXT_CHARS</code>=12000</td></tr></tbody></table></div><div class="mt">上限は LightRAG 側の制約（<code>MAX_QUERY_TOP_K=1000</code>）より <b>わざと狭く</b>取ってある。実用外の値を入れられると、検索が返らないだけで理由が分からなくなるため。</div><div class="mt">・<code>_rag_default(key)</code> は <b>config を毎回引き直す遅延評価</b>。値を二重に持たないためで、管理者が env の既定を変えれば「初期値に戻す」の戻り先も一緒に変わる。<br>・<code>rag_merge_settings(stored)</code> … <code>rag_defaults()</code> に保存値を重ねる。<code>RAG_SPEC_BY_KEY</code> に無いキーは無視（項目を削除したあとも古い保存値がファイルに残るため）、<code>_rag_coerce</code> が <code>ValueError</code> を投げた値も無視して初期値のまま。<b>壊れた保存値で質問が止まることはない</b>。<br>・<code>rag_validate_settings(payload)</code> … 画面から来た値。payload に入っているキーだけを検証し、1つでも不正なら <code>ValueError</code>（400）。<br>・<code>rag_form_fields()</code> … <code>{key, label, kind, help, min, max, choices:[{value,label}]}</code> を返す。<code>chat.js</code> の <code>renderKbFields</code> が kind を見て <code>&lt;select&gt;</code> か <code>&lt;input type=number&gt;</code> を出し分ける。</div><div class="mt">保存時（<code>POST /api/knowledge/prefs</code>）に <b>初期値と同じ項目は保存しない</b>（<code>{k: v for k, v in cleaned.items() if v != base.get(k)}</code>）。明示的に設定を変えていない利用者は、管理者が env の既定を変えたとき新しい既定に自動で追随する。</div><div class="mt"><code>off</code>（除外id）の保存側は <code>rag.kb_list()</code>（無効なものも含む全件）に実在する id だけ残す。消えた環境の id を持ち続けても意味がなく、同じ id が再利用されることもないため。</div></td></tr>
      <tr><td>rag_retrieve_all — 並列実行と部分失敗</td><td><pre class="mono small">workers = max(1, min(config.RAG_FANOUT_WORKERS, len(environments)))
with ThreadPoolExecutor(max_workers=workers) as pool:
    return list(pool.map(_one, environments))</pre><div class="mt">・<code>environments</code> が空なら即 <code>[]</code>。<br>・<code>pool.map</code> なので <b>戻り値の順序は environments の順（＝登録簿の並び）を保つ</b>。この順序がそのまま <code>rag_merge_context</code> の第2周以降のラウンドロビン順になる。<br>・<code>list(...)</code> を <code>with</code> の中で評価しているので、ここで全KBの完了を待つ。1KBあたりのタイムアウトは <code>config.RAG_RETRIEVE_TIMEOUT</code>（既定180秒）。KB数がワーカー数を超えると最悪 <code>ceil(n/8) × 180秒</code> ぶんチャットが待つ。</div><div class="mt"><code>_one(env)</code> の中は <b>二段の except で「1つ落ちても残りで続行」を保証する</b>。</div><pre class="mono small">try:    body = client.retrieve(question, mode=..., chunk_top_k=..., top_k=...)
except RagError as exc:   print(...); return {..., &quot;chunks&quot;: [], &quot;error&quot;: str(exc)}
except Exception as exc:  print(...); return {..., &quot;chunks&quot;: [], &quot;error&quot;: f&quot;検索でエラー: {exc}&quot;}</pre><div class="mt">想定外の例外まで拾うのは、1台の不調で他のKBの結果まで巻き添えにしないため。失敗は例外として上に投げず、<b>結果レコードの <code>error</code> フィールドに畳んで返す</b>（呼び出し側が「成功したKBだけで続ける」と「全滅なら諦める」を素直に書けるようにするため）。失敗は <code>print(&quot;[rag] 検索失敗 kb=...&quot;)</code> でサーバログにも出す。</div><div class="mt">呼び出し側（<code>_search_knowledge_base</code>）での部分失敗の扱い:</div><pre class="mono small">failures = [{&quot;knowledge_base&quot;: r[&quot;name&quot;], &quot;error&quot;: r[&quot;error&quot;]} for r in results if r.get(&quot;error&quot;)]
if failures and len(failures) == len(results):
    return _err(rag_all_failed_message(failures))</pre><div class="mt"><b>全滅のときだけエラーで返す</b>。一部失敗なら残りの結果で回答を作り、<code>failures</code> を llm_content にも render にも載せる。UI（<code>sourcesCard</code>）は末尾に「次のナレッジベースは検索できませんでした: 名前（エラー1行目）」を出す — 黙って減らすと「無かった」と誤解されるため。<code>searched</code> に載るのは <code>error</code> が無いKBだけ（0件でも載る）。</div><div class="mt"><code>rag_all_failed_message(failures)</code> は <b>同一のエラー文言でグルーピングする</b>。キーがまとめて期限切れ・サーバが止まっている等、原因が全部同じことが多く、素直に連結すると同じ文章がKBの数だけ並ぶ。1種類なら「すべての〜に失敗しました。{error}」、複数なら <code>・名前A、名前B: エラー</code> の行を並べる。</div></td></tr>
      <tr><td>_rag_normalize_chunks — 形の揺れの吸収</td><td><div class="mt">LightRAG の実装差でチャンクの形が揺れても壊れないようにする、防御的な正規化。</div><div class="tablewrap"><table class="data"><thead><tr><th>入力</th><th>content</th><th>file_path</th><th>score</th></tr></thead><tbody><tr><td><code>str</code></td><td>その文字列</td><td><code>&quot;&quot;</code></td><td><code>None</code></td></tr><tr><td><code>dict</code></td><td><code>content</code> → <code>text</code> → <code>chunk</code> の順で最初に見つかった真値</td><td><code>file_path</code> → <code>source</code></td><td><code>item.get(&quot;score&quot;)</code>（無ければ <code>None</code>）</td></tr><tr><td>それ以外</td><td>スキップ（<code>continue</code>）</td><td></td><td></td></tr></tbody></table></div><div class="mt"><code>content</code> は <code>str()</code> して <code>strip()</code>。<b>空になったものは捨てる</b>（出典番号だけ消費して中身が無い、を作らない）。<code>file_path</code> は <code>str()</code> するので <code>None</code> は <code>&quot;None&quot;</code> ではなく — <code>item.get(...) or item.get(...) or &quot;&quot;</code> を経ているので空文字になる。<code>score</code> は型変換も範囲チェックもせず素通し（表示と JSON 化にしか使わない）。</div><div class="mt"><b>スコア順の並べ替えはしない</b>。LightRAG が返した順をそのまま保つので、<code>chunks[0]</code> が「そのKBの一番良い1件」という前提が <code>rag_merge_context</code> の第1周で効く。</div></td></tr>
      <tr><td>rag_merge_context — ラウンドロビンと文字数予算</td><td><div class="mt">入力は <code>rag_retrieve_all</code> の結果、出力は <code>(参考情報テキスト, 出典リスト)</code>。</div><div class="mt"><b>なぜスコア順の単純な足切りにしないか</b>: スコアで切ると1つのKBが枠を埋め尽くすことがあり、質問に関係するのに別のKBが締め出される。どのKBにも必ず枠が回るようにしておくと、KBへの振り分けを多少誤っても効く。</div><pre class="mono small">live = [r for r in results if not r.get(&quot;error&quot;) and r.get(&quot;chunks&quot;)]
if not live: return &quot;&quot;, []</pre><div class="mt"><b>take(result, chunk) の判定順</b>:</div><div class="mt">・<code>sha256(content)</code> が <code>seen</code> にあれば False（同じ文章が複数のKBに入っていることがある）<br>・<code>index = state[&quot;index&quot;] + 1</code> を仮採番し、ラベル <code>[出典{index}] {KB名}</code> を作る。<code>file_path</code> があれば <code> / {file_path}</code> を足す<br>・<code>block = f&quot;{label}\n{content}\n&quot;</code><br>・<code>state[&quot;used&quot;] + len(block) &gt; char_budget</code> なら False。<b>その場で捨てるだけで打ち切らない</b><br>・通れば <code>seen</code> に digest を足し、<code>blocks</code> / <code>sources</code> に積み、<code>used</code> と <code>index</code> を確定</div><div class="mt"><b>第1周（どのKBからも最低1件）</b></div><pre class="mono small">first = [(r, r[&quot;chunks&quot;][0]) for r in live if r[&quot;chunks&quot;]]
for result, chunk in sorted(first, key=lambda rc: len(rc[1][&quot;content&quot;])):
    take(result, chunk)</pre><div class="mt">短いチャンクから順に入れるのは、予算内に入る「KBの数」を最大にするため。ここを素通りさせると、先に登録されたKBが予算を食い切り、後ろのKBが正常に応答しているのに1件も回答に出ない（無言の脱落）ことになる。</div><div class="mt"><b>第2周以降（残りをラウンドロビン）</b></div><pre class="mono small">max_depth = max(len(r[&quot;chunks&quot;]) for r in live)
for depth in range(1, max_depth):
    for result in live:
        if depth &lt; len(result[&quot;chunks&quot;]):
            take(result, result[&quot;chunks&quot;][depth])</pre><div class="mt">内側は <code>live</code> の順（＝登録簿の順）で、第1周のような長さソートはしない。入らないチャンクがあっても break しない（次のKBのもっと短いチャンクなら入るかもしれない）。</div><div class="mt">戻りは <code>&quot;\n&quot;.join(blocks)</code> と <code>sources</code>。</div><div class="mt"><b>出典番号の付け方</b>: <code>state[&quot;index&quot;]</code> は「採用された順」に 1 から連番。捨てられたチャンクは番号を消費しない（<code>index</code> は take が成功したときだけ確定する）ので、<code>sources</code> の <code>index</code> は 1..N の欠番なしになる。この番号は3か所で同じものが使われる — (a) <code>context</code> 本文中の <code>[出典N]</code> ラベル、(b) <code>sources[i][&quot;index&quot;]</code>、(c) UI の <code>src__no</code>。システムプロンプトとツール戻り値の <code>note</code> の両方で「番号は検索結果のものをそのまま使う」と指示している。</div></td></tr>
      <tr><td>ツール _search_knowledge_base の引数と戻り値</td><td><div class="mt"><b>knowledge_bases（KB名で絞る）</b>: 文字列1つで来ても <code>_coerce_lists</code> が配列に直す（<code>_LIST_PARAMS</code> は <code>BUILTIN_TOOLS</code> の「array of string」な引数を機械的に集めた表で、<code>KNOWLEDGE_TOOLS</code> を <code>BUILTIN_TOOLS</code> に合流させてあるので自動で効く）。<code>{name: target}</code> の辞書で照合し、<b>知らない名前が1つでもあれば黙って全件検索にせずエラーを返す</b>。「そのKBが無いのに『調べたが無かった』と結論される」のを防ぐためで、文面には検索できるKB名の一覧を並べる。</div><div class="mt"><b>chunk_top_k（AIによる件数の上書き）</b>:</div><pre class="mono small">if want_k:
    settings = {**settings, &quot;chunk_top_k&quot;: max(1, min(int(want_k), settings[&quot;chunk_top_k&quot;] * 2, 100))}</pre><div class="mt">「もっと広く探して」に応えるためAI指定を優先するが、<b>利用者設定の2倍かつ100件が天井</b>。青天井にすると1回の検索でAIの読める量を使い切る。<code>int()</code> に失敗したら黙って無視（元の設定のまま）。<code>top_k</code> と <code>retrieve_mode</code> はAIからは触れない。</div><div class="mt"><b>戻り値（2分岐）</b>。どちらも <code>render</code> は <code>{&quot;role&quot;:&quot;assistant&quot;, &quot;kind&quot;:&quot;sources&quot;, query, sources, failures, searched}</code>。</div><div class="tablewrap"><table class="data"><thead><tr><th></th><th><code>sources</code> が空</th><th><code>sources</code> あり</th></tr></thead><tbody><tr><td><code>found</code></td><td>0</td><td><code>len(sources)</code></td></tr><tr><td><code>context</code></td><td>無し</td><td>統合した本文</td></tr><tr><td><code>sources</code>(llm)</td><td>無し</td><td><code>excerpt</code> を落としたもの</td></tr><tr><td><code>note</code></td><td>言い回しを変えて<b>もう一度だけ</b>試すか、見つからなかったとそのまま伝えよ。推測禁止</td><td>context だけを根拠に。<code>[出典1]</code> を必ず添える。食い違いは両論併記</td></tr></tbody></table></div><div class="mt">LLM に渡す <code>sources</code> から <code>excerpt</code> を落としているのは、同じ本文が <code>context</code> にもう入っているため（トークンの二重払いを避ける）。逆に UI 用の <code>render</code> には <code>excerpt</code>（先頭200文字）が残り、<code>sourcesCard</code> はクリックで全文表示をトグルする。</div><div class="mt">このツールは <code>SQL_TOOLS_knowledge = set()</code>（SQLを受け取らないので <code>_with_explanation</code> の解説引数は付かず、実行前SQLプレビューの対象にもならない）、<code>ADMIN_TOOLS_knowledge = set()</code>（社内文書を調べるのは一般利用者の主目的そのものなので全員に渡す）。</div></td></tr>
      <tr><td>knowledge_tool_schemas — 動的 enum</td><td><pre class="mono small">envs = rag_targets()
if not envs: return []
schema = json.loads(json.dumps(KNOWLEDGE_TOOLS[0]))   # 原本を壊さない深いコピー
fn[&quot;description&quot;] += &quot;\n\n登録されているナレッジベース:\n&quot; + &quot;\n&quot;.join(f&quot;- {name}: {desc}&quot;)
fn[&quot;parameters&quot;][&quot;properties&quot;][&quot;knowledge_bases&quot;][&quot;items&quot;][&quot;enum&quot;] = names</pre><div class="mt">・<b>KBは運用中に増減するので、選択肢を起動時には決められない</b>。だから <code>_DYNAMIC_TOOLS</code> に入れて毎回組み立て直す。<code>BUILTIN_TOOLS</code> に固定の宣言も残してあるのは、<code>_missing_required</code> と <code>_coerce_lists</code> がそこから表を作るから（宣言を1つに保つより、必須引数検査を無料で効かせる方を採った）。<br>・<code>json.loads(json.dumps(...))</code> で深いコピーを取るのは、<code>description</code> への <code>+=</code> と <code>enum</code> の代入がモジュールグローバルの <code>KNOWLEDGE_TOOLS</code> を破壊しないため（浅いコピーだと <code>properties</code> が共有され、2回目以降の呼び出しで description が積み上がる）。<br>・<b>見せるのは、その利用者がサイドバーで選んでいるものだけ</b>（<code>rag_targets()</code> であって <code>kb_enabled()</code> ではない）。外したものまで並べると、AIはあると思って呼び、そのたびに <code>_search_knowledge_base</code> の未知名チェックに断られて往復を1回損する。<br>・説明文は管理画面で管理者が書いた <code>description</code> がそのまま入る。AIがツール／KBを選ぶ材料は名前と説明しかないので、<b>ここが検索の当たり外れをいちばん左右する</b>。</div><div class="mt"><code>build_tools</code> 側では、動的に組み立てた宣言に対しても <code>.meta.yaml</code> の <code>builtin_tools:</code> による無効化（<code>enabled: False</code>）と説明の上書きが効く。</div></td></tr>
      <tr><td>画面（サイドバーと管理画面）</td><td><div class="mt"><b>チャットのサイドバー</b>（<code>#kbSection</code>、ラベルは「LightRAG」）。初期値は <code>chat.html</code> に渡る <code>knowledge_prefs_payload()</code> → <code>window.CHAT_INIT.knowledge</code>。</div><pre class="mono small">{ bases: [{id, name, description, on}], settings, defaults, fields }</pre><div class="mt"><code>bases</code> は <code>kb_enabled()</code> から作り、<code>on = id not in rag_excluded_ids(g.user)</code>。</div><div class="mt">・KBが0件なら <code>renderKnowledge</code> が節ごと <code>display:none</code>（この状態ではAIにツール自体を渡していない）。<br>・<b>チェックは押した時点で保存する</b>。「保存」を押させると、押し忘れたまま質問して「なぜあの文書が出ないのか」になるため。送るのは <code>off</code>＝チェックの外れているものの id。<br>・見出しのバッジは <code>4 / 22</code> の形。全部選んでいるときも分母を出す（数字だけだと選択数なのか総数なのか読めない）。<br>・「検索設定」だけは <code>#kbSave</code> ボタンで明示保存、<code>#kbReset</code> は <code>settings: kb.defaults</code> を送る（＝サーバ側で「初期値と同じ項目は保存しない」に当たり、<code>rag_settings</code> が空になる）。</div><div class="mt"><b>管理画面</b> <code>/knowledge</code>（admin_required）は <code>bases=kb_list()</code>（キー伏せ）、<code>defaults=rag_defaults()</code>、<code>fields=rag_form_fields()</code> を渡す。ヘルプ画面（<code>/help</code>）は <code>bases=kb_list() if g.user.is_admin else []</code> — 一般利用者にはKBの一覧を出さない。</div></td></tr>
      <tr><td>主なデータ構造</td><td>・登録簿の1件 = {id: 12桁hex, name, base_url, api_key, description, enabled: bool, created_at: ISO8601(UTC)}  ← data/knowledge_bases.json の配列要素<br>・伏せた写し（_kb_redact） = 上記から api_key を除き has_api_key: bool を足したもの<br>・rag_targets() = [登録簿の1件（api_key入り）, ...]  ※ kb_enabled() から rag_off を引いたもの<br>・settings（rag_user_settings） = {retrieve_mode: str, chunk_top_k: int, top_k: int, max_context_chars: int}<br>・RAG_SPECS の1行 = (key, label, kind(&quot;int&quot;|&quot;choice&quot;), help, lo, hi, choices)  choices = ((値, 表示名), ...)<br>・rag_form_fields() の1要素 = {key, label, kind, help, min, max, choices: [{value, label}]}<br>・retrieve() の payload = {query, mode, chunk_top_k, include_chunk_content: True, (top_k)}<br>・rag_retrieve_all() の1要素 = {id, name, chunks: [chunk], error: str|None}  ※ environments と同じ順<br>・chunk（_rag_normalize_chunks 後） = {content: 非空str, file_path: str, score: 任意|None}<br>・source = {index: 1始まりの連番, knowledge_base: KB名, kb_id, file_path, score, excerpt: content[:200]}<br>・context = &quot;[出典N] KB名 / file_path\n本文\n&quot; を &quot;\n&quot; で連結した文字列<br>・failures = [{knowledge_base: KB名, error: エラー文言}]<br>・render アイテム = {role:&quot;assistant&quot;, kind:&quot;sources&quot;, query, sources, failures, searched: [成功したKB名]}<br>・prefs.yaml = {model, rag_off: [kb_id], rag_settings: {初期値と違う項目だけ}, tables_off: [表名]}<br>・サイドバー払い出し = {bases: [{id, name, description, on: bool}], settings, defaults, fields}</td></tr>
      <tr><td>定数・しきい値</td><td>・config.RAG_RETRIEVE_TIMEOUT = 180秒（env <code>RAG_RETRIEVE_TIMEOUT</code>）… 1KBへの検索タイムアウト。文書の取り込み中はLightRAG側が抽出処理で埋まり応答が遅くなるため、わざと長く取ってある<br>・config.RAG_FANOUT_WORKERS = 8（env <code>RAG_FANOUT_WORKERS</code>）… 同時に投げるKB数。実際は max(1, min(8, KB数))<br>・config.RAG_RETRIEVE_MODE = &quot;mix&quot;（env）… retrieve_mode の初期値<br>・config.RAG_CHUNK_TOP_K = 10（env）… chunk_top_k の初期値<br>・config.RAG_TOP_K = 40（env）… top_k の初期値。naive モードでは使われない<br>・config.RAG_MAX_CONTEXT_CHARS = 12000（env）… 統合後にAIへ渡す上限。1つの質問でナレッジ検索を何度も呼ぶことがあり、そのたびに積み上がるので控えめにしてある<br>・RAG_SPECS の許容範囲: chunk_top_k 1〜100 / top_k 1〜200 / max_context_chars 1000〜20000。LightRAG の MAX_QUERY_TOP_K=1000 より意図的に狭い<br>・AIによる chunk_top_k 上書きの天井 = min(AI指定, 利用者設定×2, 100)、下限 1<br>・health() と _verify_credentials() の HTTP タイムアウト = 15秒（ハードコード。RagClient の timeout は使わない）<br>・_rag_error_message / _rag_safe_body の本文切り出し = 300文字（超過は「…」）<br>・source の excerpt = content[:200]<br>・config.KNOWLEDGE_BASES_FILE = data/knowledge_bases.json（env で変更可）、書き込み後に chmod 0o600 を試行<br>・prefs.KEYS = (&quot;model&quot;, &quot;rag_off&quot;, &quot;rag_settings&quot;, &quot;tables_off&quot;)。これ以外のキーは読み書きしない<br>・認証ヘッダ名 = X-API-Key（LightRAG）。エンドポイントは POST /query/data, GET /health, GET /documents/pipeline_status<br>・_DYNAMIC_TOOLS = {&quot;search_knowledge_base&quot;}</td></tr>
    </tbody></table></div>
    <div class="card__title mt">落とし穴（15件）</div>
    <div class="tablewrap"><table class="data"><thead><tr><th style="width:60px">#</th><th>内容</th></tr></thead><tbody>
      <tr><td class="mono small">01</td><td><code>/api/chat/rewind</code>（発言の書き直し）は <code>_begin_turn</code> を通らないので、<b>送信と同じ下ごしらえを自分でやる必要がある</b>。具体的には <code>rag.set_current_user(g.user)</code> と <code>results.new_turn()</code>。以前これが抜けていて、書き直しのときだけ <code>_current_user()</code> がそのワーカースレッドに前回の質問で残った値（別の利用者のこともある）か None を返していた。None のときは <code>prefs.load(None)</code> が <code>{}</code> を返すので、その利用者の除外設定と検索設定が黙って無視され、全KB・env既定で検索されていた。門番の <code>rag.rag_available(g.user)</code> は明示的に g.user を渡していたため、「入口は正しいのに中身が違う人の設定で走る」という形になっていた。<b>いまは両方呼んでいる</b>（検証: 巻き戻しの確認スクリプト）。ターンの外に持ち出す状態を足すときは、ここにも同じ入れ直しが要る。</td></tr>
      <tr><td class="mono small">02</td><td><code>_one</code> の中で <code>RagClient(env[&quot;base_url&quot;], ...)</code> を組み立てているのは try の<b>外</b>。knowledge_bases.json を手で編集して base_url を欠いたエントリを作ると KeyError が <code>pool.map</code> を突き抜け、<code>rag_retrieve_all</code> ごと例外になって「1つ落ちても残りで続行」が成立しない（dispatch の包括 except に拾われて質問全体が「ツール実行でエラー」になる）。</td></tr>
      <tr><td class="mono small">03</td><td><code>RagClient.health()</code> は <code>self.timeout</code> を使わない。<code>kb_test</code> は <code>timeout=config.RAG_RETRIEVE_TIMEOUT</code>(180) を渡して構築するが、実際に効くのは health/_verify_credentials にハードコードされた 15 秒。接続テストが 15 秒で切れるのに検索は 180 秒待つ、という非対称がある。</td></tr>
      <tr><td class="mono small">04</td><td><code>_post</code> は <code>_requests.Timeout</code> を <code>RequestException</code> より<b>先</b>に捕まえて独自の文面（秒数入り）を作るので、POST 経路のタイムアウトは <code>_rag_describe</code> を通らない。一方 <code>health</code> / <code>_verify_credentials</code> は <code>RequestException</code> しか見ないので、そこのタイムアウトだけ <code>_rag_describe</code> の「応答がありません（タイムアウト）」文面になる。同じ事象で2種類の文面が出る。</td></tr>
      <tr><td class="mono small">05</td><td><code>_rag_describe</code> の分岐は継承関係を前提に順序が決まっている。requests では SSLError・ProxyError・ConnectTimeout がすべて ConnectionError のサブクラス（ConnectTimeout は Timeout でもある）。ConnectionError の判定を上に動かすと、証明書エラーもプロキシエラーも「接続を拒否されました。ポート番号を確認してください」に化ける。</td></tr>
      <tr><td class="mono small">06</td><td><code>retrieve()</code> は <code>body.get(&quot;status&quot;) not in (None, &quot;success&quot;)</code> で判定する。status キーごと欠けた応答は<b>成功扱い</b>になり、<code>data.chunks</code> が無ければ 0 件として静かに通る。LightRAG 以外のものが同じURLで200を返している場合、エラーにならず「見つかりませんでした」になる。</td></tr>
      <tr><td class="mono small">07</td><td><code>rag_merge_context</code> の第1周で捨てられたチャンク（重複 or 予算オーバー）は、第2周以降で拾い直されない。第2周は <code>depth in range(1, max_depth)</code> で必ず index 1 から始まるので、そのKBの最良チャンク（index 0）は永久に落ちる。</td></tr>
      <tr><td class="mono small">08</td><td>重複判定の <code>seen</code> に digest を足すのは take が<b>成功したときだけ</b>。予算オーバーで落ちた本文は seen に入らないので、同じ本文が別KBから来たときに（そのときは入るなら）採用され得る。重複排除は「採用済みとの重複」だけを見ている。</td></tr>
      <tr><td class="mono small">09</td><td>文字数予算 <code>char_budget</code> は <code>len(block)</code> の合計しか数えない。最後に <code>&quot;\n&quot;.join(blocks)</code> するので、実際の context は予算より (ブロック数−1) 文字だけ長くなる。</td></tr>
      <tr><td class="mono small">10</td><td><code>.meta.yaml</code> の <code>builtin_tools:</code> で <code>search_knowledge_base</code> の description を上書きすると、<code>build_tools</code> が <code>{**t[&quot;function&quot;], &quot;description&quot;: o[&quot;description&quot;]}</code> で丸ごと差し替えるため、<code>knowledge_tool_schemas</code> が追記した「登録されているナレッジベース:」の一覧が消える。<code>knowledge_bases</code> の enum は残るので、AIには選択肢だけあって各KBが何の文書なのかの手掛かりが無い状態になる。</td></tr>
      <tr><td class="mono small">11</td><td><code>search_knowledge_base</code> は <code>ADMIN_TOOLS</code> にも <code>_HANDLERS</code> の門番にも引っかからないので、KBを1件も選んでいない利用者のAIが（宣言を渡していないのに）名前を推測して呼ぶと dispatch を通って <code>_search_knowledge_base</code> まで届く。そこで初めて「検索できるナレッジベースがありません」という _err が返る（守りは宣言側と実処理側の2枚）。</td></tr>
      <tr><td class="mono small">12</td><td>サイドバーの <code>bases</code> は <code>kb_enabled()</code> から作られる。管理者がKBを無効化すると、それを除外していた利用者の画面からその行が消え、次にどれかのチェックを触った瞬間に <code>off</code> が「いま見えているものの中で外れているid」だけで上書き保存され、無効KBの除外が prefs から落ちる。あとで管理者が再度有効化すると、その利用者では黙って検索対象に復活する。</td></tr>
      <tr><td class="mono small">13</td><td><code>_search_knowledge_base(args, scope)</code> は第2引数の <code>scope</code>（DB/表の選択）を完全に無視する。文書検索はDB選択と独立で、表を1つも選んでいなくても動く。</td></tr>
      <tr><td class="mono small">14</td><td><code>_rag_normalize_chunks</code> は score でも何でも並べ替えない。<code>chunks[0]</code> が「そのKBの最良1件」という前提は LightRAG の返す順序に全面的に依存している。</td></tr>
      <tr><td class="mono small">15</td><td><code>_rag_default</code> が config を毎回参照する遅延評価なので、<code>rag_defaults()</code> の戻り値は env（＝プロセス起動時に読んだ config の値）に追随する。かつ「初期値と同じ値は prefs に保存しない」ので、既定を変えると明示設定していない利用者は次回から新しい既定で動く（保存済みの利用者は動かない）。</td></tr>
    </tbody></table></div>
  </div>

  <div class="card mt">
    <div class="card__title" id="impl-chart">5-9. グラフ・分析・ファイル出力</div>
    <div class="card__desc">SELECT結果（columns, rows）を受け取り、Plotlyの図・統計分析・Excel/CSV/テキスト/Word/PowerPointを組み立てる層。グラフは54種の chart_type を CHART_SPECS 1本の台帳で管理し、用途別の6ツール（plot_comparison など）と plot_dual_axis の宣言をそこから機械生成する。図は「画面へPlotly JSON」「Word/PowerPointへPNG（kaleido）」「Excel/PowerPointのネイティブグラフ」の3経路に分かれ、統計は表＋日本語の所見という共通形で返す。生成ファイルはディスクに書かず、メモリ上のバイト列をトークン付きで預けて /api/file/&lt;token&gt; から配る。</div>
    <div class="tablewrap"><table class="data"><thead><tr><th style="width:210px">項目</th><th>内容</th></tr></thead><tbody>
      <tr><td>全体の流れとデータの受け渡し</td><td><div class="mt">LLMのツール呼び出しは <code>tools.dispatch(name, arguments_json, scope, entries, admin)</code> に入る。dispatch は (1) 引数JSONの解析、(2) 管理者専用ツールの遮断、(3) <code>_coerce_lists</code>（配列で受ける引数に文字列が1つ来たら要素1つの配列に直す）、(4) <code>_missing_required</code>（必須引数の欠落を機械的に止める）、(5) <code>_gather_sqls</code>（入れ子も含めてSQLを収集し、実行後 <code>verify.alerts_for</code> に渡す）を通してからハンドラを呼ぶ。</div><div class="mt">どのツールも戻り値は <code>{&quot;ok&quot;: bool, &quot;llm_content&quot;: str(JSON), &quot;render&quot;: dict|None}</code> の3点セット。<code>llm_content</code> はトークン節約のため要約（先頭 <code>config.SAMPLE_ROWS_FOR_LLM</code>＝40行まで）で、<code>render</code> が画面に積まれるアイテムになる。</div><div class="mt">データの用意は <code>fetch(spec, scope, label=..., max_rows=...)</code> に一本化されている。優先順は次のとおり。</div><div class="mt">・<code>spec[&quot;rows&quot;]</code> があり、中身が空でないか sql/result_id が無い → <code>_inline_table</code>（DBを介さない表）<br>・<code>spec[&quot;result_id&quot;]</code> があればその預かりを使う。無い場合でも <code>results.find_by_sql</code> で「同じ質問・同じDBの組み合わせ・同じSQL」の既存結果を探し、あればそれを使い回す<br>・どちらも無ければ <code>db.run_select(sql, db.widen_scope(sql, scope), max_rows=...)</code></div><div class="mt">戻り値は <code>(columns, rows, truncated, result_id, total_rows)</code> の5要素。<code>max_rows</code> は道具ごとに違い、画面向け（表・グラフ・レポート）は <code>MAX_RESULT_ROWS</code>＝2,000、ファイル出力は <code>EXPORT_MAX_ROWS</code>＝1,000,000 を渡す。result_id で受け取った結果が2,000行で切られていて、かつ呼び出し側がそれより大きい上限を要求した場合は、預けたときのSQLで取り直す（「集計→CSV」の流れでCSVだけ2,000行に欠ける事故を防ぐ）。</div><div class="mt">切り詰めが起きたときは <code>source_note()</code> がLLM向けの警告を、<code>render_source_note()</code> が画面向けの <code>truncated</code> / <code>source_total_rows</code> を付ける。後者は元々表にしか渡っておらず、グラフとレポートが断りなしに一部だけを描いていたのを直した経緯がコメントに残っている。</div></td></tr>
      <tr><td>グラフ種別の台帳（CHART_SPECS / required_fields / validate）</td><td><div class="mt">グラフ種別は <code>CHART_SPECS: dict[str, tuple[str, tuple, str]]</code> の1本だけが正。値は <code>(日本語の説明, 必要な指定, 分類)</code>。分類は「比較 / 推移 / 構成 / 分布 / 関係 / 指標」の6つ。内訳は 比較12・推移11・構成8・分布8・関係12・指標3 の計54種で、<code>CHART_TYPES = tuple(CHART_SPECS)</code> がその順序付き一覧になる。</div><div class="mt">・比較: bar, hbar, stacked_bar, percent_bar, lollipop, dumbbell, pareto, pyramid, marimekko, radar, polar_bar, bump<br>・推移: line, step, area, area_percent, range_area, slope, candlestick, ohlc, gantt, calendar, control_chart<br>・構成: pie, donut, treemap, sunburst, icicle, funnel, waterfall, sankey<br>・分布: histogram, density, ecdf, box, violin, strip, ridgeline, qq<br>・関係: scatter, bubble, histogram2d, contour, heatmap, matrix, scatter_matrix, parallel_coordinates, parallel_categories, scatter3d, surface, network<br>・指標: indicator, gauge, bullet</div><div class="mt">台帳から派生する関数は3つ。<code>type_help(category)</code> は enum の説明文とツール説明文に埋め込む文字列を作り、<code>types_in(category)</code> はその分類の種別名リスト、<code>required_fields(chart_type)</code> は必要な指定のタプルを返す（未知の種別には <code>(&quot;x&quot;, &quot;y&quot;)</code>）。</div><div class="mt"><code>validate(item, columns)</code> の判定順は、(1) 未知の chart_type なら使える種別を全列挙して終了、(2) <code>LIST_FIELDS = (&quot;path&quot;, &quot;dimensions&quot;)</code> はリストとして扱い空・不在を個別に指摘、(3) それ以外の必須は未指定か列に無ければエラー、(4) 任意指定（color, size, text, y2, z, lower, upper, target, facet）は指定されていれば存在チェックのみ。ただし <code>target</code> は列名ではなく目標値（数値）で来ることがあるため、int/float なら飛ばす。</div><div class="mt"><code>matrix</code> と <code>surface</code> は required_fields が空タプルで、集計済みのクロス表をそのまま塗る前提。<code>required_fields</code> は画面（カタログのツール定義UI）にも <code>chart_fields</code> として渡され、AI・UI・検証の3者が同じ台帳を見る。</div></td></tr>
      <tr><td>用途別グラフツールの機械生成と振り分け</td><td><div class="mt">LLMに見せるグラフツールは6つで、<code>_CHART_TOOLS</code> に <code>ツール名 -&gt; (分類, 説明, 使う指定, 必須)</code> として定義されている。</div><div class="tablewrap"><table class="data"><thead><tr><th>ツール</th><th>分類</th><th>宣言上の必須</th></tr></thead><tbody><tr><td>plot_comparison</td><td>比較</td><td>sql, chart_type, x, y, title</td></tr><tr><td>plot_trend</td><td>推移</td><td>sql, chart_type, title</td></tr><tr><td>plot_composition</td><td>構成</td><td>sql, chart_type, title</td></tr><tr><td>plot_distribution</td><td>分布</td><td>sql, chart_type, title</td></tr><tr><td>plot_relationship</td><td>関係</td><td>sql, chart_type, title</td></tr><tr><td>plot_kpi</td><td>指標</td><td>sql, chart_type, value, title</td></tr></tbody></table></div><div class="mt"><code>_chart_tools()</code> は各エントリについて、共通の <code>sql / chart_type / title / purpose</code> を土台に、<code>chart_type</code> の enum を <code>charts.types_in(cat)</code>、説明を <code>charts.type_help(cat)</code> から埋める。個別の指定は <code>_CHART_ARGS</code>（x,y,y2,z,color,size,text,facet,path,dimensions,lower,upper,source,target,start,end,open,high,low,close,value,agg,max,suffix,nbins,orientation,barmode,marginal,trendline,colorscale の説明カタログ）から引く。<b>54種の振り分けは「分類ごとにenumを切る」だけ</b>なので、種別を1つ足しても宣言側は自動で追従する。</div><div class="mt">生成された定義は <code>BUILTIN_TOOLS</code> に展開され、その後 <code>_allow_result_id(BUILTIN_TOOLS)</code> が木をたどって、<code>properties</code> に <code>sql</code> を持つ節すべてに <code>result_id</code> と <code>rows</code> を足し、<b>required から &quot;sql&quot; を外す</b>。</div><div class="mt">実処理はすべて <code>_plot_chart</code> 1本で、<code>HANDLERS_query</code> に <code><b>{name: _plot_chart for name in _CHART_TOOLS}</code> として登録される。<code>_plot_chart</code> は fetch → <code>_CHART_FIELDS</code>（30個の指定名）を args から拾って item を作る → <code>chart_type</code> 未指定なら &quot;bar&quot; → <code>charts.validate</code> → 通れば <code>render = {&quot;kind&quot;: &quot;chart&quot;, columns, rows, </b>item, title, ...}</code> を返す。<b>この時点では図を作らず、素材だけを積む。</b></div><div class="mt">旧 <code>plot_chart</code>（全54種を1つのenumで持つ汎用ツール）は <code>_RETIRED</code> により BUILTIN_TOOLS から除かれる。実処理とハンドラ登録は残っているので、過去の会話やユーザー定義ツールの上書きは壊れない。<code>plot_dual_axis</code> だけは別ツール・別ハンドラ <code>_plot_dual_axis</code> で、x / bar_y[] / line_y[] を自前で検証し <code>kind: &quot;chart_dual&quot;</code> を返す。</div></td></tr>
      <tr><td>figure の組み立て（_Ctx と _BUILDERS）</td><td><div class="mt"><code>build_figure(item)</code> が render アイテム（kind=&quot;chart&quot;）から Plotly の figure を作る。<code>_BUILDERS[chart_type]</code> を引き、無ければ使える種別を全列挙した ValueError を投げ、あれば <code>builder(_Ctx(item))</code> を呼び、最後に <code>margin=dict(l=55, r=20, t=50, b=50)</code> を当てる。<code>_BUILDERS</code> は54キー（donut は <code>_pie</code> を共有）。</div><div class="mt"><code>_Ctx.__init__</code> の下ごしらえが要点。</div><div class="mt">・<code>self.df = pd.DataFrame(item[&quot;rows&quot;], columns=item[&quot;columns&quot;])</code><br>・color, size, text, y2, z, lower, upper, target, facet, source, start, end, open, high, low, close, value の17個は <b>df.columns に無ければ None に落とす</b><br>・<code>target</code> だけは列名でなく数値のこともあるので <code>self.target_value</code> に生のまま保持<br>・<code>path</code> / <code>dimensions</code> は df に実在する列だけに絞る<br>・<code>_numeric(...)</code> で数値化。<code>pd.to_numeric(errors=&quot;coerce&quot;).fillna(元の値)</code> なので、数値にならなかったセルは元の値のまま残る</div><div class="mt">代表的な builder:</div><div class="mt">・<code>_hbar</code>: y の昇順に並べ替えてから x/y を入れ替えて orientation=&quot;h&quot;（値が大きいものが上に来る）<br>・<code>_percent_bar</code> / <code>_area_percent</code>: x でグループ化した合計を分母に構成比(%)を作り、y軸を 0〜100 に固定<br>・<code>_pareto</code>: y 降順、累積構成比を第2軸、<code>add_hline(y=80)</code> に「80%」注記<br>・<code>_pyramid</code>: color 列の値2種類を左右に振り分け、左側は値を負にする。2種類無ければ ValueError<br>・<code>_marimekko</code>: 幅 = size の x ごとの最大値を合計100に正規化し、<code>go.Bar(width=...)</code> で幅可変の積み上げ<br>・<code>_control_chart</code>: 平均と ±3σ（std ddof=1）を引き、外れた点だけマーカーを <code>#B02A2A</code> にする<br>・<code>_calendar</code>: x を日付化し、ISO週×曜日の行列に集計して <code>px.imshow</code><br>・<code>_waterfall</code>: x の値が「合計 / 計 / total」の行だけ measure を &quot;total&quot; にする<br>・<code>_sankey</code> / <code>_network</code>: source と target を通し番号のラベル表に畳んでから描く<br>・<code>_density</code> / <code>_qq</code>: scipy を遅延importし、3行未満なら ValueError<br>・<code>_indicator</code> / <code>_gauge</code> / <code>_bullet</code>: <code>_indicator_value</code> が <code>agg</code>（sum/mean/max/min/last、既定 sum）で1つの数にし、<code>_target_of</code> が target 列の合計、無ければ <code>target_value</code> を float 化。目標があるときだけ delta が付き、gauge/bullet の上限は <code>max</code> 指定か <code>max(v, t)*1.25</code></div><div class="mt"><code>build_dual_figure(item)</code> は <code>make_subplots(specs=[[{&quot;secondary_y&quot;: True}]])</code> に bar_y を棒（左軸）、line_y を折れ線（右軸）で積む。</div></td></tr>
      <tr><td>図の3つの出口（画面 / 画像 / ネイティブ）</td><td><div class="mt">同じ図でも、行き先によって作り方がまったく違う。</div><div class="mt"><b>(A) 画面 — Plotly JSON。</b> <code>render_item_for_web(item)</code> が kind を見て分岐し、<code>out[&quot;figure&quot;] = json.loads(fig.to_json())</code> を入れる。失敗したら kind を &quot;error&quot; に差し替える（例外で画面全体を落とさない）。ブラウザ側は <code>Plotly.newPlot</code> で描く。</div><div class="mt">重要なのは、<b>figure は保存されず毎回作り直される</b>点。会話履歴には columns / rows / chart_type などの素材だけが残り、履歴を開くたびに再構築される。JSONに載らない値は <code>jsonable()</code> が処理し、bytes は <code>&lt;N bytes&gt;</code>、NaN と ±inf は None（不正なJSONを出さないため）になる。</div><div class="mt"><b>(B) Word / PowerPoint — PNG。</b> <code>_chart_image(chart)</code> が <code>figures.for_print(charts.build_figure(chart))</code> を呼ぶ。図そのものは同じ <code>build_figure</code> を通るので、画面と紙で見た目の元は一致する。失敗しても None を返すだけで、文書作成は止めない。</div><div class="mt"><b>(C) Excel / PowerPoint — ネイティブグラフ。</b> 画像ではなく、受け取った側が範囲や種類を変えられる本物のグラフを埋める。Plotly の54種はそのままでは表現できないので、対応表で近いものに寄せる。</div><div class="mt">・<code>_XLSX_CHART_MAP</code>（17件）→ <code>EXCEL_CHART_TYPES</code> の11種へ。lollipop と pareto は bar、step/bump/slope は line、donut は pie、funnel は hbar、bubble は scatter に落ちる<br>・<code>_PPTX_CHART_MAP</code>（19件）→ 上に加えて radar と polar_bar→radar、donut→doughnut が使える</div><div class="mt">地図に無い種別（sankey・箱ひげ・treemap など）は、PowerPoint では画像に落として貼り、それも作れなければ表スライドに退避する。Excel では単にグラフを付けず表だけになる。</div></td></tr>
      <tr><td>画像化（kaleido・キャッシュ・一度死んだら諦める設計）</td><td><div class="mt"><code>figures.render(fig, width, height, scale)</code> が Plotly figure を PNG のバイト列にする。既定は <code>REPORT_IMAGE_WIDTH</code>=1200px、<code>REPORT_IMAGE_HEIGHT</code>=650px、<code>REPORT_IMAGE_SCALE</code>=2。</div><div class="mt">処理順は、(1) モジュール変数 <code>_broken</code> が空でなければ即 None、(2) キャッシュキー = <code>sha1(fig.to_json() + &quot;|WxH@S&quot;)</code>、(3) <code>_lock</code> 下で <code>_cache</code> を引く、(4) <code>fig.to_image(format=&quot;png&quot;, ...)</code>、(5) 例外が出たら理由を <code>_broken</code> に積んで None、(6) 成功したらキャッシュ（<code>_MAX_CACHE</code>=40 を超えたら古いものから捨てる）。</div><div class="mt">Plotly の画像化は裏で Chrome を動かす（kaleido）。社内サーバに Chrome が入っていないことがあるので、失敗を「画像は諦めるが文書は作る」に倒している。<code>_broken</code> はプロセス寿命の間ずっと残り、1枚あたり数秒待たされる再挑戦を止める。理由は <code>why_unavailable()</code> で取り出せ、<code>_export_docx</code> が「chart を指定したのに図が0枚だった」ときにだけ添える。</div><div class="mt"><code>for_print(fig)</code> は <code>_polish(fig)</code> を通してから render する。<code>_polish</code> は <code>copy.deepcopy</code> で元を壊さずに、template=&quot;plotly_white&quot;、font=<code>REPORT_FONT_JA</code>（既定 Meiryo）、本文15pt・タイトル17pt、margin l=70/r=30/t=50/b=60、凡例は横並びで上、背景は白、colorway は Excel/PowerPoint と同じ10色、y軸はグリッド #E8E8E8・桁区切り、を当てる。画面はマウスで拡大できるが紙とスライドはできない、という理由がコメントに書かれている。</div></td></tr>
      <tr><td>集計ツール（pivot_table と analyze_stats）</td><td><div class="mt"><b>pivot_table</b>。SQLite に PIVOT 構文が無く、CASE WHEN を列の数だけ手書きさせないための道具。<code>columns</code>（列に展開する1列名・文字列）が要素1つの配列で来た場合は中身を取り出し、2つ以上ならエラーにする。</div><div class="mt"><code>analysis.pivot(...)</code> の処理順は、(1) index / values 必須・<code>aggfunc</code> は <code>AGG_FUNCS</code>（sum/mean/count/median/min/max/std/nunique、既定 sum）・<code>percent</code> は row/column/total に限る、(2) 指定列が結果に無ければ利用可能な列を添えて ValueError、(3) count/nunique 以外は values を数値化、(4) <code>pd.pivot_table(fill_value=0, margins=margins and not percent, margins_name=&quot;合計&quot;, dropna=False)</code>、(5) <code>rank_by</code> があれば先に並べ替え（<b>%にする前</b>。%にすると行内の大小が消えるため）、(6) <code>percent</code> があれば <code>_as_percent</code>、(7) reset_index・順位列の挿入・MultiIndex の平坦化（<code>&quot; / &quot;</code> 連結）。</div><div class="mt">結果は <code>results.put</code> で預け直して新しい result_id を返すので、集計後の表をそのままグラフやレポートに渡せる。</div><div class="mt"><b>analyze_stats</b> は method で3方向に分かれる。</div><div class="mt">・<code>describe</code> → 対象列は指定が無ければ <code>numeric_columns</code>（<b>8割以上が数値として読める列</b>）を自動判定。<code>group_by</code> があれば群ごとに describe。列名は「件数/平均/標準偏差/最小/25%/中央値/75%/最大」に和訳し小数3桁<br>・<code>correlation</code> → 既定は pearson/spearman。1列目が「列」なので matrix グラフにそのまま渡せる。llm_content には上位8組と「相関は因果ではありません」の注意。<code>partial=true</code> なら偏相関、<code>lag&gt;0</code> なら時差相関に分岐<br>・<code>outliers</code> → <code>advanced.outliers_ext</code>。target 必須</div></td></tr>
      <tr><td>統計・予測のアルゴリズムとしきい値</td><td><div class="mt">分析関数はすべて <code>{&quot;title&quot;, &quot;tables&quot;, &quot;notes&quot;, &quot;meta&quot;}</code> を返し、画面用アイテム（kind=&quot;report&quot;）とLLM用の要約に変換される。有意水準は <code>ALPHA = 0.05</code> 固定。</div><div class="mt"><b>外れ値 <code>outliers_ext</code></b></div><div class="tablewrap"><table class="data"><thead><tr><th>方法</th><th>正常範囲</th><th>既定しきい値</th></tr></thead><tbody><tr><td>iqr</td><td>Q1−t·IQR 〜 Q3+t·IQR</td><td>1.5</td></tr><tr><td>zscore</td><td>mean ± t·std(ddof=1)</td><td>3.0</td></tr><tr><td>modified_zscore</td><td>median ± t·1.4826·MAD</td><td>3.5</td></tr><tr><td>percentile</td><td>下位t% 〜 上位t%</td><td>1.0</td></tr><tr><td>mahalanobis</td><td>距離 ≤ cut</td><td>sqrt(chi2.ppf(0.975, 列数))</td></tr></tbody></table></div><div class="mt">MAD が0（同じ値ばかり）なら判定不能。結果は500件で打ち切り、「外れ値＝誤りとは限らない」旨を必ず添える。</div><div class="mt"><b>時系列の異常検知 <code>detect_anomalies</code></b>。最低8点。window は既定7で <code>max(3, min(window, max(3, len//3)))</code> に丸める。<code>season_length</code> があり2周期以上あれば季節分解の seasonal を引いてから判定。移動中央値と移動MADで <code>scale = MAD × 1.4826</code>、<code>score = (値 − 移動中央値) / scale</code>。<code>|score| ≥ threshold</code>（既定3.0）を異常とし、上位100件を表にする。12点以上なら変化点検出も走る（<code>max_cuts=3</code>, <code>min_seg=4</code>、残差平方和の減りが区間全体の10%以下なら採らない）。</div><div class="mt"><b>予測 <code>forecast</code></b>。最低4点、periods は 1〜120。<code>method=&quot;auto&quot;</code> は「season_length があり2周期以上 → holt_winters / 8点以上 → holt / それ以外 → linear」。exog を渡すと arima 固定。ARIMA の次数は p∈0..2, d∈0..1, q∈0..2（p=q=0を除く）を総当たりし AIC 最小を採る。区間は残差SDの ±1.96 倍。</div><div class="mt">当てはまりの目安は <code>_backtest_note</code> が出す。8点以上・exog無しのときだけ、原点をずらして再帰的に forecast を呼び MAE と MAPE を出す。実績が平均×1%未満の期は誤差率から外す。MAPE の言い換えは &lt;10%「かなり当たります」、&lt;20%「実用的な精度」、それ以上「参考程度」。</div><div class="mt"><b>回帰 <code>regression</code></b>（ols / logistic / poisson）。説明変数は8割以上が数値なら数値、そうでなければダミー化。VIF <b>10超</b>を警告、Durbin-Watson が <b>1.5未満/2.5超</b>で残差の並びを警告、R²&lt;0.3 で注意。30行以上なら <b>seed=0 で7:3に分けたホールドアウト</b>の R² を別表で出す。</div><div class="mt"><b>クラスタリング <code>clustering</code></b>。標準化してから <code>kmeans2(minit=&quot;++&quot;, seed=0)</code>。<code>k=&quot;auto&quot;</code> は 2〜<code>min(8, len//2)</code> を試し、自前実装のシルエットが最大のものを採る（800点超は標本化）。最良値が <b>0.25未満</b>なら「たまたまの区切りに近い」と警告。群の特徴は<b>群間平均から0.8標準偏差以上離れた項目</b>を最大3つ拾って一言にする。</div><div class="mt"><b>ABC分析 <code>abc_analysis</code></b>。降順に並べて累計構成比を出し、<code>thresholds</code>（既定 <code>[70, 90]</code>）で A/B/C に分ける。要約表の見出しは値の列名から作る（「金額」と決め打つと停止時間や工数を渡したときに嘘になるため）。</div></td></tr>
      <tr><td>ファイル出力（Excel / CSV / テキスト）</td><td><div class="mt">いずれもディスクには書かず、メモリ上のバイト列を <code>render</code> の <code>data</code> に載せて返す。</div><div class="mt"><b>export_excel</b>。シートごとに fetch し、上限は <code>min(EXPORT_MAX_ROWS, 1_048_575)</code>（Excelのシート上限から見出し1行を引いた値）。<code>build_excel</code> はシート名を <code>safe_sheet_name</code> で整え（禁止文字を <code>_</code> に、31文字で切り、重複は <code>_2</code>）、note があれば1行目に斜体グレー、データは3行目から。見出しは濃紺地に白太字、偶数行に縞、数値セルは <code>#,##0.####</code>。見出しの下でウィンドウ枠を固定しオートフィルタを掛ける。列幅は<b>見出しと先頭200行</b>から <code>min(最大+2, 60)</code>。</div><div class="mt"><code>_add_chart</code> はシート上のデータ範囲を参照するネイティブグラフを作る。category_column の既定は1列目、value_columns の既定は残り全部。<b>scatter だけは vals[0] を x にし、残りを y にする</b>。系列色は10色を巡回。data_labels は <b>pie だけ「false と書かない限りオン」</b>。<code>x_axis.delete = False</code> の明示は「これが無いとExcelで軸が消えることがある」ため。アンカー既定は複数のグラフが21行ずつ下にずれて並ぶ。</div><div class="mt"><b>export_csv</b>。<code>csv.writer(lineterminator=&quot;\r\n&quot;, quoting=QUOTE_MINIMAL)</code>、None は空文字。区切りは comma/tab/semicolon（既定 comma）。文字コードは utf-8-sig（既定）/ utf-8 / cp932 で、<b>cp932 のときだけ <code>errors=&quot;replace&quot;</code></b>（絵文字などで落とさない）。2つ以上なら ZIP でまとめる。</div><div class="mt"><b>export_text</b>。<code>format</code> は md か txt。<code>{{見出し}}</code> というプレースホルダが body にあればそこへ差し込み、無ければ末尾に追記する。<code>table_to_text</code> は markdown / tsv / 等幅の3スタイル。</div></td></tr>
      <tr><td>文書出力（Word / PowerPoint / build_report）</td><td><div class="mt"><b>export_docx</b>。節ごとに fetch し、<code>chart</code> があれば validate を通してから PNG にする。<b>画像化できなければ図を落として先へ進む</b>（表は根拠として残る）。表は既定で載り、行数は <code>max_rows</code>（既定40）で切る。</div><div class="mt"><code>build_docx</code> の並びは 表紙 → 目次 → 要約 → 本編 → 結論 → 推奨する打ち手 → 前提・注意 → 付録。日本語フォントは <code>_jp_font</code> が <code>w:rFonts</code> の ascii/hAnsi/eastAsia/cs を全部書き換えて当てる（python-docx は latin しか設定せず、当てないと英字フォントが混じる）。目次とページ番号は Word のフィールドで入れるため、開いた後に F9 で更新する旨を添える。表は <code>DOCX_MAX_TABLE_ROWS = 40</code> で<b>再度</b>切る。</div><div class="mt"><b>export_pptx</b>。16:9（13.333×7.5インチ）。title 引数があって1枚目が表紙でなければ表紙を差し込み、<b>中扉が2枚以上あって目次が無ければ目次を自動生成</b>する。1スライド1メッセージが方針で、<code>_header</code> が見出しと「キーメッセージ帯」を描く。グラフは <code>PPTX_CHART_TYPES</code>（12種）のネイティブが既定。カテゴリは <code>MAX_CATEGORIES = 24</code> で切る。表は既定 <code>PPTX_MAX_TABLE_ROWS = 12</code> 行。値ラベルは「pie/doughnut、またはカテゴリ8以下かつ系列2以下」のときだけ。</div><div class="mt"><b>build_report</b> は画面表示とファイルを同時に作る。節ごとに fetch → 表は <code>max_rows</code>（既定20）で切り、<b>グラフは全行を使う</b>。chart の検証に失敗しても <code>dropped</code> に積むだけでレポート全体は作り切り、LLMには「同じ引数で呼び直さない」よう指示する。<code>format</code> は md / docx / pptx / xlsx / none。</div></td></tr>
      <tr><td>ファイル名の規則と、効く出力・効かない出力</td><td><div class="mt">ファイル名を作る関数は3つあり、規則が違う。</div><div class="mt"><b><code>exports.safe_filename(name, ext)</code></b> は、(1) Windowsで使えない文字と制御文字を <code>_</code> に置換、(2) 前後の空白とピリオドを除去、(3) 末尾の拡張子を落とす（対象は xlsx/csv/txt/md/zip の5つだけ。<b>docx と pptx は落ちない</b>）、(4) 空なら default、(5) <b>先頭80文字に切る</b>、(6) <code>_YYYYMMDD_HHMM</code> と拡張子を付ける。切り詰めは常に「日時より前」に効くので、日時が消えることはない。</div><div class="mt"><b><code>docx_safe_filename</code> / <code>pptx_safe_filename</code></b> は禁止文字を置換するだけで、<b>日時を付けず、長さも切らず、制御文字も落とさない</b>。同じ題名で2回作ると同じファイル名になる。</div><div class="tablewrap"><table class="data"><thead><tr><th>出力</th><th>日時</th><th>80文字切り</th></tr></thead><tbody><tr><td>export_excel / export_csv / export_text</td><td>あり</td><td>あり</td></tr><tr><td>build_report（md / xlsx）</td><td>あり</td><td>あり</td></tr><tr><td>export_docx / export_pptx</td><td><b>なし</b></td><td><b>なし</b></td></tr><tr><td>build_report（docx / pptx）</td><td><b>なし</b></td><td><b>なし</b></td></tr><tr><td>ユーザー定義ツール・利用状況の書き出し</td><td>あり</td><td>あり</td></tr></tbody></table></div><div class="mt">つまり <b>Office文書だけが別系統</b>。なお Excel の<b>シート名</b>はファイル名とは無関係で、<code>safe_sheet_name</code> が別に31文字・禁止文字を処理する。</div></td></tr>
      <tr><td>トークン方式のダウンロード</td><td><div class="mt">ツールが作るのはバイト列なので、ブラウザに渡すには一度サーバ側に置いてURLを発行する必要がある。ここでもディスクには書かない。</div><pre class="mono small">_MAX_ITEMS = 200
_fs_lock  = threading.Lock()
_files: OrderedDict[str, dict] = OrderedDict()

def _fs_put(data, filename, mime, owner) -&gt; str:
    token = secrets.token_urlsafe(16)
    with _fs_lock:
        _files[token] = {&quot;data&quot;: …, &quot;filename&quot;: …, &quot;mime&quot;: …, &quot;owner&quot;: …}
        while len(_files) &gt; _MAX_ITEMS:
            _files.popitem(last=False)      # 古いものから捨てる
    return token</pre><div class="mt">配布口は <code>/api/file/&lt;token&gt;</code> + <code>login_required</code> で、<code>_fs_get(token, g.user.username)</code> が None なら 404。<b>URLを推測されても他人のファイルは渡さない</b>のが owner 一致チェックの役目。</div><div class="mt">預ける側は <code>_web_log(render_log, start)</code>。表示用の変換を通した後、<b><code>item[&quot;data&quot;]</code> を持つアイテムなら種類を問わず</b> <code>_fs_put</code> してから <code>url</code> を足す。ブラウザ側は、作られた直後（replay でない）かつ自動保存が有効なら保存を始める。</div><div class="mt">同じ仕組みを画像アップロードとデータ取り込みも共有している。</div><div class="mt">生成ファイルは会話履歴にも残る。<code>_encode_item</code> が <b><code>CHAT_EMBED_FILE_MAX_BYTES</code> = 2MiB 以下なら base64 で埋め込み、超えていれば中身を捨てて <code>_no_data</code> を立てる</b>。したがって、プロセスを再起動すると <code>_files</code> は空になるが、2MiB以下のファイルは履歴を開き直した時点でリンクが復活する。2MiB を超えたファイルは再ダウンロードできない。</div><div class="mt">結果データ側の置き場は別物で、<code>results</code> が <code>MAX_ENTRIES = 40</code> 件・<code>MAX_CELLS = 400_000</code> の二重上限で古いものから捨てる。取り出しには「預けたときと同じDBの組み合わせ」の一致が要る。</div></td></tr>
      <tr><td>主なデータ構造</td><td>・chart アイテム: {kind:&quot;chart&quot;, columns:[...], rows:[(...)], chart_type:str, x,y,color,size,text,path[],dimensions[],nbins,orientation,barmode,y2,z,lower,upper,facet,source,target,start,end,open,high,low,close,value,agg,max,suffix,colorscale,marginal,trendline, title, truncated?, source_total_rows?}<br>・chart_dual アイテム: {kind:&quot;chart_dual&quot;, columns, rows, x, bar_y:[列名], line_y:[列名], left_title, right_title, title}<br>・CHART_SPECS の1件: chart_type -&gt; (日本語の説明:str, 必要な指定:tuple, 分類:&quot;比較|推移|構成|分布|関係|指標&quot;)<br>・_CHART_TOOLS の1件: ツール名 -&gt; (分類:str, 説明:str, 使う指定:tuple, 必須:tuple)<br>・_Ctx: {item, df:DataFrame, x, y, title, 17個の任意フィールド（df に無ければ None）, target_value（生の値）, path:[実在列], dimensions:[実在列]}<br>・fetch の戻り値: (columns:list, rows:list[tuple], truncated:bool, result_id:str, total_rows:int|None)<br>・分析結果: {&quot;title&quot;:str, &quot;tables&quot;:[{&quot;name&quot;,&quot;columns&quot;,&quot;rows&quot;}], &quot;notes&quot;:[str], &quot;meta&quot;:dict}<br>・results の預かり: rid -&gt; {scope:str, columns, rows, truncated, sql, norm_sql, turn, label}<br>・excel の1シート: {&quot;name&quot;, &quot;columns&quot;, &quot;rows&quot;, &quot;note&quot;?, &quot;charts&quot;?:[{type, category_column, value_columns[], title, y_title, x_title, number_format, data_labels, anchor, width, height}]}<br>・docx の1セクション: {heading, body, bullets[], table:{columns,rows,note}, table_caption, image:bytes, caption, note, callout, level, page_break}<br>・pptx の1スライド: {kind:title|agenda|section|message|table|chart|kpi|compare|closing, title, subtitle, message, comment, callout, source, notes, chart, categories[], series:[{name, values[], x[]}], image:bytes, columns, rows, max_rows, highlight_rows[], items[], panes[2], summary[], actions[]}<br>・filestore の1件: token -&gt; {&quot;data&quot;: bytes, &quot;filename&quot;: str, &quot;mime&quot;: str, &quot;owner&quot;: ユーザー名}<br>・会話に保存される file アイテム: {kind:&quot;file&quot;, filename, mime, data(base64 + _b64:true) または _no_data:true, sheets[], note, outline[]}</td></tr>
      <tr><td>定数・しきい値</td><td>・CHART_SPECS / CHART_TYPES: 54種（比較12・推移11・構成8・分布8・関係12・指標3）<br>・LIST_FIELDS = (&quot;path&quot;, &quot;dimensions&quot;) — validate でリストとして扱う指定<br>・build_figure の余白 = margin(l=55, r=20, t=50, b=50)／印刷用は margin(l=70, r=30, t=50, b=60)<br>・印刷用 colorway ＝ Excel の _SERIES_COLORS ＝ pptx の SERIES = 1F4E79, F4B183, 70AD47, C55A11, 7F7F7F, 2E75B6, A9D18E, FFD966, 9DC3E6, BFBFBF の10色<br>・REPORT_IMAGE_WIDTH=1200 / REPORT_IMAGE_HEIGHT=650 / REPORT_IMAGE_SCALE=2 / REPORT_FONT_JA=&quot;Meiryo&quot;<br>・figures._MAX_CACHE = 40（PNGキャッシュ、FIFO）。キーは sha1(fig.to_json() + &quot;|WxH@S&quot;)<br>・MAX_RESULT_ROWS = 2000（画面・LLM向け）／ SAMPLE_ROWS_FOR_LLM = 40（LLMに返す行数）<br>・EXPORT_MAX_ROWS = 1_000_000（ファイル出力）。Excel は min(EXPORT_MAX_ROWS, 1_048_575) に丸める<br>・results.MAX_ENTRIES = 40 / results.MAX_CELLS = 400_000（行×列の合計）<br>・filestore._MAX_ITEMS = 200、token = secrets.token_urlsafe(16)<br>・CHAT_EMBED_FILE_MAX_BYTES = 2 MiB（これを超えるファイルは履歴に中身を残さない）<br>・exports.ENCODINGS = utf-8-sig（既定）/ utf-8 / cp932。cp932 のみ errors=&quot;replace&quot;<br>・safe_filename: 禁止文字 [&lt;&gt;:&quot;/\|?*\x00-\x1f]、末尾拡張子の除去対象は xlsx|csv|txt|md|zip、ステム80文字、末尾に _%Y%m%d_%H%M<br>・docx_safe_filename / pptx_safe_filename: 禁止文字 [\/:*?&quot;&lt;&gt;|]、日時なし・長さ制限なし<br>・excel: シート名31文字・列幅上限60（先頭200行から算出）・グラフ20cm×10cm・アンカーは 21行おき<br>・EXCEL_CHART_TYPES = 11種 / PPTX_CHART_TYPES = 12種（+doughnut, radar）<br>・_XLSX_CHART_MAP = 17件 / _PPTX_CHART_MAP = 19件（Plotly種別 → ネイティブ種別）<br>・DOCX_MAX_TABLE_ROWS = 40、画像幅16cm / PPTX_MAX_TABLE_ROWS = 12、MAX_CATEGORIES = 24、KPIカード最大4枚<br>・export_docx の表 max_rows 既定40 / build_report の表 max_rows 既定20 / pptx table は既定12<br>・advanced.ALPHA = 0.05（有意水準）<br>・外れ値のしきい値: iqr=1.5、zscore=3.0、modified_zscore=3.5（1.4826×MAD）、percentile=1.0、mahalanobis=sqrt(chi2.ppf(0.975, 列数))。結果は500件で打ち切り<br>・detect_anomalies: 最低8点、window 既定7、threshold 既定3.0、変化点は12点以上のとき（max_cuts=3, min_seg=4、減りが10%以下なら採らない）<br>・forecast: 最低4点、periods 1〜120、区間は残差SDの ±1.96 倍、ARIMA は p∈0..2 / d∈0..1 / q∈0..2（p=q=0除く）でAIC最小<br>・backtest: 8点以上・exogなしのみ。MAPE &lt;10%「かなり当たります」、&lt;20%「実用的」、以上「参考程度」。実績が平均×1%未満の期は除外<br>・regression: 数値列判定は8割以上、VIF&gt;10 を警告、Durbin-Watson 1.5未満/2.5超で警告、R²&lt;0.3 で注意、ホールドアウトは30行以上・seed=0・7:3<br>・clustering: k=&quot;auto&quot; は 2〜min(8, len//2)、シルエット 0.25 未満で警告、ダミーは種類2〜20のみ、800点で標本化、割り当て表500件<br>・abc_analysis: thresholds 既定 [70, 90]（累計構成比%）<br>・analysis.AGG_FUNCS = sum/mean/count/median/min/max/std/nunique（既定 sum）、PERCENT_MODES = row/column/total<br>・numeric_columns の判定 = 数値として読める比率 0.8 以上</td></tr>
    </tbody></table></div>
    <div class="card__title mt">落とし穴（33件）</div>
    <div class="tablewrap"><table class="data"><thead><tr><th style="width:60px">#</th><th>内容</th></tr></thead><tbody>
      <tr><td class="mono small">01</td><td>plot_* ツールは図を作らない。_plot_chart は validate を通した素材（columns/rows と指定）を render に積むだけで、Plotly の figure は画面表示のたびに作り直す。履歴に figure は保存されていない。</td></tr>
      <tr><td class="mono small">02</td><td>_allow_result_id が required から &quot;sql&quot; を機械的に外すので、宣言上「sql 必須」でも実際には止められない。さらに _HAS_DEFAULT = {title, filename, chart_type, purpose} は欠落チェックを免除される。実際に強制されるのは plot_comparison なら x と y、plot_kpi なら value だけ。</td></tr>
      <tr><td class="mono small">03</td><td>plot_chart（全54種を1つの enum で持つ旧ツール）は _RETIRED で宣言だけ消してある。実処理とハンドラは残っているので、過去の会話やユーザー定義ツールの上書きは壊れない。「同じことが2通りでできるとAIが毎回迷う」ための判断。</td></tr>
      <tr><td class="mono small">04</td><td>_Ctx は df.columns に無い任意フィールドを黙って None にする。validate を通さない経路（pivot_table の heatmap 描画など）では、指定ミスがエラーにならず「その指定が無かったこと」になる。</td></tr>
      <tr><td class="mono small">05</td><td>figures._broken はモジュール変数で、一度でも画像化に失敗するとプロセスが生きている間ずっと全ての画像化が None を返す。1枚あたり数秒待たされる再挑戦を避けるための意図的な設計で、リセット手段は再起動しかない。</td></tr>
      <tr><td class="mono small">06</td><td>余白は3回上書きされる。build_figure が (55,20,50,50)、印刷経路では _polish が (70,30,50,60)、ブラウザは newPlot 時に (55,20,40,50) と透明背景でさらに上書きする。個別 builder で margin を凝っても印刷と画面では消える。</td></tr>
      <tr><td class="mono small">07</td><td>export_docx で max_rows に40より大きい値を渡しても意味がない。ハンドラが切った後、docx 側が DOCX_MAX_TABLE_ROWS=40 で再度切るため、上限は常に40行。</td></tr>
      <tr><td class="mono small">08</td><td>build_report は表とグラフでデータ量が違う。表は max_rows（既定20）で切るが、グラフには全行を渡す。「表は読みやすさのために切っている」という但し書きが実装コメントにある。</td></tr>
      <tr><td class="mono small">09</td><td>Office文書（docx / pptx）のファイル名だけ規則が違う。日時も長さ制限も付かないので、同じ題名で2回作ると同名ファイルになる。</td></tr>
      <tr><td class="mono small">10</td><td>pivot_table の columns だけ意味が違う（配列ではなく「列に展開する1列名」の文字列）。_allow_result_id はこれを検知して上書きしないようにしており、上書きすると _coerce_lists が文字列を配列にして pandas 側で unhashable type: &#x27;list&#x27; になる。</td></tr>
      <tr><td class="mono small">11</td><td>pivot の percent と margins は併用できない。構成比を指定すると総計行・列が黙って消える。並べ替え（rank_by）は %化の前に行う（%にすると行内の大小が消えるため）。</td></tr>
      <tr><td class="mono small">12</td><td>fetch は rows と sql/result_id が同時に来たときSQLを優先する。LLMが引数の雛形ごと rows:[] を付けてくることがあり、それを0行の表として返すと「データがあるのに無い」と答えてしまう（COUNTが常に0行になる実測がコメントに残っている）。</td></tr>
      <tr><td class="mono small">13</td><td>result_id を渡さず同じSQLを書き直してきた呼び出しは、results.find_by_sql が機械的に使い回しに変える。条件は「同じ質問・同じDBの組み合わせ・空白を潰して一致するSQL」の3つ全部。SQLの大文字小文字は揃えない（&#x27;A装置&#x27; と &#x27;a装置&#x27; の違いが意味を持つため）。</td></tr>
      <tr><td class="mono small">14</td><td>result_id 経由のデータは2,000行に切られていることがある。ファイル出力のように大きな上限を要求する呼び出しでは、預けたときのSQLで取り直す分岐が fetch にある。これが無いと「集計→CSV」でCSVだけ2,000行で欠ける。</td></tr>
      <tr><td class="mono small">15</td><td>切り詰めの警告は長らく llm_content にしか無く、画面には出ていなかった。グラフとレポートが断りなしに一部だけを描いていたのを直した経緯がある。</td></tr>
      <tr><td class="mono small">16</td><td>Excel の散布図だけ列の意味がずれる。value_columns の先頭を x 軸に使い、残りを y にする。他の種類は category_column が横軸。</td></tr>
      <tr><td class="mono small">17</td><td>Excel のグラフで x_axis.delete / y_axis.delete を明示的に False にしているのは、これが無いとExcelで軸が消えることがあるため。data_labels は pie だけ「明示的に false と書かない限りオン」という非対称な既定を持つ。</td></tr>
      <tr><td class="mono small">18</td><td>_export_excel と build_excel の中でローカル変数 charts がモジュール charts を覆い隠している。その関数内で charts モジュールを使っていないので現状は動くが、追記するときは名前が衝突する。</td></tr>
      <tr><td class="mono small">19</td><td>detect_anomalies と analyze_stats の outliers は用途が違う。静的な外れ値は右肩上がりのデータだと直近を全部外れ値と判定するため、時系列には移動中央値＋MAD を使う。</td></tr>
      <tr><td class="mono small">20</td><td>外れ値判定に平均と標準偏差ではなく中央値とMADを使うのは、平均・標準偏差が異常値自身に引っ張られるため。1.4826 は正規分布で標準偏差の尺度に合わせる係数。</td></tr>
      <tr><td class="mono small">21</td><td>ARIMA の次数は以前 (1,1,1) 固定だった。当てはまらないのに「ARIMAで予測した」とだけ言うことになるため、AIC で総当たり選択に変えた。選ばれた次数は notes に出る。</td></tr>
      <tr><td class="mono small">22</td><td>予測の検証は再帰的に forecast を呼ぶ。無限再帰を止めているのは _backtest=False の引数だけで、exog つきのときはそもそも走らない。</td></tr>
      <tr><td class="mono small">23</td><td>MAPE は実績が0に近い期があると跳ね上がるので、平均の1%未満の期を割り算から外し、外した回数を注記して「誤差率より外れた幅で見てほしい」と促す。</td></tr>
      <tr><td class="mono small">24</td><td>R² は学習に使ったデータで測ると必ず良く出る。30行以上のとき seed=0 で7:3に分けたホールドアウトを別表で出し、そちらの数字で「予測に使えるか」を語らせる。</td></tr>
      <tr><td class="mono small">25</td><td>clustering の k=&quot;auto&quot; は max(scored) を採るため、シルエット係数が同点なら分割数の大きい方が勝つ（タプルの2番目で比較されるため）。空クラスタが出た候補は最初から除外される。</td></tr>
      <tr><td class="mono small">26</td><td>abc_analysis の要約表の見出しは値の列名から動的に作る。「金額」と決め打つと停止時間や工数を渡したときに単位の違う見出しのままExcel・PowerPointへ出て行くため。</td></tr>
      <tr><td class="mono small">27</td><td>ファイルはディスクに書かない。_files は200件のFIFOなので、古いチャットを大量に開くと先に発行したURLが失効する。</td></tr>
      <tr><td class="mono small">28</td><td>会話に保存されるファイルは2MiBまで。それを超えると中身を捨てるので、履歴からは再ダウンロードできない。メール添付も render_log の data を直接読むため同じ制限を受ける。</td></tr>
      <tr><td class="mono small">29</td><td>/api/file/&lt;token&gt; は login_required に加えて owner 一致を確かめる。トークンを推測されても他人のファイルは渡らないが、逆に言えば同一トークンでも別ユーザーからは404になる。</td></tr>
      <tr><td class="mono small">30</td><td>jsonable が NaN と ±inf を None に変換しているのは、そのまま json.dumps すると &quot;NaN&quot; という不正なJSONになりブラウザ側で読めなくなるため（Excel の空セルは pandas で NaN になる）。</td></tr>
      <tr><td class="mono small">31</td><td>_scale が色スケール名を色のリストに直すのは、名前のまま渡すと周辺分布つきのグラフで plotly が文字列を1文字ずつ色として読み、&quot;Blues&quot; が &#x27;B&#x27; 扱いになって落ちるため。</td></tr>
      <tr><td class="mono small">32</td><td>_pie は donut と共有の builder で、hole を出すかどうかを item[&quot;chart_type&quot;] == &quot;donut&quot; で判定する。item を手で組む場合、chart_type を消すとドーナツが円になる。</td></tr>
      <tr><td class="mono small">33</td><td>funnel だけ plotly と引数の向きが逆（plotly は x=値 / y=段階）。このアプリの仕様は「x に段階、y に値」なので _funnel が入れ替えている。</td></tr>
    </tbody></table></div>
  </div>

  <div class="card mt">
    <div class="card__title" id="impl-auth">5-10. 認証・権限・保存レイアウト</div>
    <div class="card__desc">ログインは auth.py 1ファイルに閉じてあり、<code>authenticate()</code> が「常設管理者 → 常設一般ユーザー（BUILTIN_USERS）→ プロバイダ（local / http）」の順に判定する。認証結果は <code>User</code> データクラスの4項目だけを Flask のセッション Cookie に写し、毎リクエストの <code>load_user_into_context</code>（<code>app.before_request</code>）で <code>g.user</code> に復元する。権限は <code>login_required</code> / <code>admin_required</code> の2段だけで、両者とも <code>request.path.startswith(&quot;/api/&quot;)</code> を見て JSON(401/403) と 画面(リダイレクト/403テンプレ) を切り替える。ユーザーごとの状態（チャット履歴・prefs）は <code>data/users/&lt;User.safe_key&gt;/</code> にファイルで置き、カタログ・ナレッジベース登録簿・モデル設定・メール設定・各種履歴は全員共通で <code>data/</code> 直下に置く。</div>
    <div class="tablewrap"><table class="data"><thead><tr><th style="width:210px">項目</th><th>内容</th></tr></thead><tbody>
      <tr><td>ファイルの分かれ方と、なぜ auth.py だけ別なのか</td><td><div class="mt">ソースは <code>core.py</code>（約37,000行・アプリ本体）/ <code>config.py</code>（env から読む設定）/ <code>auth.py</code>（ログイン）の3本。</div><div class="mt"><code>auth.py</code> は「LDAP連携APIに差し替えるときに触るファイルを1本に閉じる」ことを目的に分離されている。そのため<b>ログイン関係の設定は env にも config.py にも一切無く、すべて auth.py の冒頭定数</b>にある（<code>AUTH_PROVIDER</code> / <code>AUTH_USERS_FILE</code> / <code>AUTH_ADMIN_GROUP</code> / <code>ADMIN_USER</code> / <code>ADMIN_PASS</code> / <code>BUILTIN_USERS</code> / <code>AUTH_API_*</code>）。config.py の「--- 認証 ---」節にもその旨だけが書いてあり、置いてあるのは <code>USER_META_DIR</code>（＝<code>DATA_DIR / &quot;users&quot;</code>）だけ。</div><div class="mt">core.py 側は <code>auth.User</code> / <code>auth.authenticate</code> / <code>auth.get_provider</code> / <code>auth.AuthError</code> / <code>auth.admin_enabled</code> / <code>auth.load_users_file</code> / <code>auth.save_users_file</code> / <code>auth.hash_password</code> / <code>auth.AUTH_ADMIN_GROUP</code> しか触らない。</div><div class="mt">なお core.py は冒頭で、統合前のモジュール名（<code>db</code> <code>catalog</code> <code>chats</code> <code>prefs</code> <code>models</code> <code>rag</code> <code>tools</code> <code>llm</code> …）を全部 <code>_sys.modules</code> に自分自身として登録している。したがって core.py 内の <code>import prefs</code> / <code>import rag</code> は<b>すべて自分自身を指す</b>。<code>auth</code> と <code>config</code> だけが本物の別ファイル。</div></td></tr>
      <tr><td>authenticate() — 3段の判定順と、その順序の理由</td><td><div class="mt"><code>auth.authenticate(username, password)</code> が画面から呼ばれる唯一の入口。処理は次の順で、途中で確定したらプロバイダには渡さない。</div><div class="mt">・<code>_try_builtin_admin(username, password)</code><br>・<code>admin_enabled()</code>（＝<code>ADMIN_USER</code> と <code>ADMIN_PASS</code> の両方が真）が偽なら即 None。<b><code>ADMIN_PASS</code> を空文字にするとこのアカウントごと無効</b>になる（空パスワードで入れてしまう事故を防ぐため）。<br>・ID は <code>strip().lower()</code> と <code>ADMIN_USER.lower()</code> の比較（大文字小文字を無視）。<br>・パスワードは <code>hmac.compare_digest(str(password).encode(&quot;utf-8&quot;), str(ADMIN_PASS).encode(&quot;utf-8&quot;))</code>。<b>bytes に落としてから比べているのは、<code>compare_digest</code> が非ASCIIの str を受け付けず TypeError になるため</b>（日本語パスワードを設定した瞬間に落ちる）。<br>・成功時は <code>User(username=ADMIN_USER, display_name=&quot;管理者&quot;, groups=[AUTH_ADMIN_GROUP], is_admin=True)</code>。<br>・常設管理者と同じIDだったが 1 で失敗した場合、<b>ここで None を返してプロバイダには渡さない</b>。LDAP側に同名の <code>admin</code> が居ても取り違えないため。<br>・<code>BUILTIN_USERS</code> のどれかとIDが一致したら <code>_try_builtin_user</code> の結果で確定（一致・不一致どちらでもプロバイダへは行かない）。<code>_try_builtin_user</code> は <b>IDとパスワードが同じ文字列</b>なら成功（<code>hmac.compare_digest</code> で比較）。返るのは <code>User(username=&lt;リストの綴り&gt;, display_name=&quot;&quot;, groups=[], is_admin=False)</code>。<br>・どれにも当たらなければ <code>get_provider().authenticate(username, password)</code>。</div><div class="mt">この「先に常設アカウントを見る」構造が、LDAPが落ちていても設定画面に入れる非常口になっている。逆に LDAP へ完全移行したら <code>BUILTIN_USERS = []</code> にし、<code>ADMIN_PASS</code> を強いものへ変えるのが前提。</div></td></tr>
      <tr><td>プロバイダ（local / http）</td><td><div class="mt"><code>AuthProvider</code>（ABC）の実装は2つで、<code>_PROVIDERS = {&quot;local&quot;: LocalAuthProvider, &quot;http&quot;: HttpApiAuthProvider}</code>。<code>get_provider(name)</code> は <code>AUTH_PROVIDER</code> を小文字化して引き、未知なら <code>AuthError</code> を投げる。</div><div class="mt"><b>LocalAuthProvider</b>（既定）</div><div class="mt">・<code>AUTH_USERS_FILE</code>（＝プロジェクト直下の <code>auth_users.yaml</code>）を毎回読む。キャッシュしない。<br>・ファイルが無い／<code>users</code> が空でも <code>AuthError</code> にはせず <b>None（＝普通の認証失敗）</b>を返す。常設 admin と BUILTIN_USERS だけで運用できるため。<br>・YAMLの読み込み自体が失敗したときだけ <code>AuthError</code>。<br>・ID照合は <code>lower()</code> 同士。パスワードは <code>verify_password</code>。<br>・<code>is_admin</code> は <code>AUTH_ADMIN_GROUP in groups</code> の完全一致（部分一致しない）。<br>・返す <code>username</code> は<b>YAMLに書かれた綴りそのもの</b>（入力の綴りではない）。これが保存先フォルダ名の安定に効いている。</div><div class="mt"><b>HttpApiAuthProvider</b></div><div class="mt">・<code>AUTH_API_URL</code> が空なら <code>AuthError</code>。<br>・<code>{AUTH_API_USER_FIELD: username, AUTH_API_PASS_FIELD: password}</code> を JSON で POST（<code>urllib.request</code>、タイムアウト <code>AUTH_API_TIMEOUT</code>＝10秒）。<br>・HTTPError の <b>400/401/403 は「認証失敗」で None</b>、それ以外は <code>AuthError</code>。接続不能も <code>AuthError</code>。<br>・応答が JSON でなければ <code>AuthError</code>。<br>・成功判定は <code>AUTH_API_SUCCESS_FIELD</code> が設定されていればその値の真偽、空なら <code>status == 200</code>。<br>・<code>_dig(data, &quot;user.displayName&quot;)</code> のドット区切りで入れ子から値を取る。<br>・<b><code>AUTH_API_GROUPS_FIELD</code> が空なら groups は必ず空 → 全員が一般ユーザー</b>。「応答に無いものを推測して管理者にするのは危険」という判断で、迷ったら一般に倒している。この構成では管理者は <code>ADMIN_PASS</code> で入る admin だけになる。</div><div class="mt"><code>AuthError</code> は「認証以前の失敗（設定不備・通信不可）」専用で、ログイン画面は None（＝ID/パスワード違い）とは違う文面を出す。</div></td></tr>
      <tr><td>パスワードのハッシュ（local プロバイダ用）</td><td><div class="mt"><code>hash_password(password)</code> は <code>secrets.token_bytes(16)</code> のソルトと <code>hashlib.pbkdf2_hmac(&quot;sha256&quot;, …, _ITER)</code>（<code>_ITER = 200_000</code>）で、<code>pbkdf2_sha256$&lt;反復数&gt;$&lt;salt hex&gt;$&lt;hash hex&gt;</code> の1行に詰める。</div><div class="mt"><code>verify_password(password, stored)</code> は <code>$</code> で4分割し、アルゴリズム名が違えば False、保存されている反復数で計算し直して <code>hmac.compare_digest(dk.hex(), hash_hex)</code> で比較。<code>ValueError</code> / <code>AttributeError</code> は握って False（形式が壊れた行で例外を出さない）。反復数を stored 側から読むので、<code>_ITER</code> を将来上げても既存ユーザーはそのままログインできる。</div><div class="mt"><code>save_users_file</code> は書いた後 <code>os.chmod(p, 0o600)</code> を試み、<code>OSError</code> は無視（Windowsでは事実上効かない）。</div></td></tr>
      <tr><td>セッション（Cookie に入るもの・入らないもの）</td><td><div class="mt"><code>_USER_KEY = &quot;user&quot;</code>。</div><div class="mt">・<code>login_user(user)</code> … <code>session[&quot;user&quot;] = {&quot;username&quot;, &quot;display_name&quot;, &quot;groups&quot;(list), &quot;is_admin&quot;}</code> を書き、<code>session.permanent = False</code>。permanent=False なので <b>ブラウザを閉じるとログアウト</b>（<code>PERMANENT_SESSION_LIFETIME</code> は設定していない）。<br>・<code>load_user_into_context()</code> … <code>app.before_request</code> に登録。<code>session.get(&quot;user&quot;)</code> があれば <code>g.user = auth.User(**data)</code>、無ければ <code>g.user = None</code>。<b>ここで再検証は一切しない</b>（YAMLもLDAPも見に行かない）。<br>・<code>logout_user()</code> … <code>session.clear()</code>。<code>chat_id</code> も一緒に消える。</div><div class="mt">Cookie の設定は <code>create_app()</code> の <code>app.config.update</code> にある。</div><div class="tablewrap"><table class="data"><thead><tr><th>キー</th><th>値</th><th>備考</th></tr></thead><tbody><tr><td><code>SECRET_KEY</code></td><td><code>_secret_key()</code></td><td>下記</td></tr><tr><td><code>SESSION_COOKIE_HTTPONLY</code></td><td>True</td><td></td></tr><tr><td><code>SESSION_COOKIE_SAMESITE</code></td><td>&quot;Lax&quot;</td><td></td></tr><tr><td><code>SESSION_COOKIE_SECURE</code></td><td><b>未設定</b></td><td>社内HTTP前提</td></tr><tr><td><code>MAX_CONTENT_LENGTH</code></td><td>64MB</td><td></td></tr><tr><td><code>JSON_AS_ASCII</code></td><td>False</td><td></td></tr></tbody></table></div><div class="mt"><code>_secret_key()</code> の決まり方は <code>FLASK_SECRET_KEY</code>（環境変数）&gt; プロジェクト直下の <code>.flask_secret</code> の中身 &gt; 新規に <code>secrets.token_urlsafe(48)</code> を生成してそのファイルへ書き込み（<code>chmod 0o600</code> を試行）。<b>ファイルに残すのは「再起動でログアウトさせないため」</b>という明示の設計判断。逆に言えば、鍵を捨てる＝全員を強制ログアウトさせる唯一の手段になっている。</div><div class="mt">セッションに入るもう1つの値は <code>session[&quot;chat_id&quot;]</code>（いま開いている会話のID）だけ。会話の実体・モデル選択・RAG設定はすべてファイル側にある。</div></td></tr>
      <tr><td>ログイン画面（bp_auth）</td><td><div class="mt"><code>bp_auth = Blueprint(&quot;auth&quot;, __name__)</code>。ルートは <code>/login</code>（GET/POST）と <code>/logout</code>（POST）の2本で、<b>どちらにも権限デコレータは付かない</b>（アプリ全体で唯一の無防備ルートは他に <code>/vendor/plotly.min.js</code> のみ）。</div><div class="mt"><code>login()</code> の流れ:</div><div class="mt">・<code>g.get(&quot;user&quot;)</code> が既にあれば <code>chat.index</code> へリダイレクト。<br>・<code>auth.get_provider()</code>。ここで <code>AuthError</code> が出たら <code>login.html</code> に <code>fatal=&lt;文言&gt;</code> を渡してフォームごと出さない。<br>・<code>provider.name == &quot;local&quot;</code> かつ <code>not auth.admin_enabled()</code> かつ <code>auth_users.yaml</code> にユーザーが1人も居ない場合だけ <code>setup_needed = True</code>（画面に <code>python core.py users add &lt;名前&gt; --admin</code> を案内する）。<b><code>ADMIN_PASS</code> が設定されていればこの案内は出ない</b>（常設 admin で入れるため）。<br>・POST 時、ID か パスワードが空なら flash(warning)。<code>auth.authenticate</code> が <code>AuthError</code> なら flash(error)、None なら「ユーザー名またはパスワードが違います。」、成功なら <code>login_user(user)</code> して <code>next</code> へリダイレクト。<br>・<code>next</code> の検査は <code>nxt.startswith(&quot;/&quot;)</code> だけ。</div><div class="mt"><code>AuthProvider.hint</code>（<code>LocalAuthProvider</code> は「社内LDAP導入までの暫定アカウントです。」）は定義されているが、<code>login.html</code> は provider を受け取っておらず<b>どこにも表示されない</b>。</div></td></tr>
      <tr><td>login_required と admin_required</td><td><div class="mt">どちらも <code>functools.wraps</code> で包む素朴なデコレータで、判断材料は <code>g.get(&quot;user&quot;)</code> だけ。</div><pre class="mono small">login_required:
  user is None → path が &quot;/api/&quot; 始まり ? jsonify({&quot;error&quot;:&quot;ログインしてください。&quot;}),401
                                        : redirect(url_for(&quot;auth.login&quot;, next=request.path))

admin_required:
  user is None      → 上と同じ（401 or ログイン画面へ）
  not user.is_admin → &quot;/api/&quot; 始まり ? jsonify({&quot;error&quot;:&quot;この操作は管理者のみです。&quot;}),403
                                     : render_template_string(_TPL_403), 403</pre><div class="mt"><code>_TPL_403</code> は「元 templates/403.html」を core.py 内の文字列として持っているもので、<code>base.html</code> を継承し <code>user.display_name or user.username</code> を出す（<code>user</code> は <code>inject_globals</code> が全テンプレートへ注入）。<code>render_template_string</code> は helpers 節より前で個別に import されている。</div><div class="mt"><b>実際の分布（全84ルート）</b></div><div class="tablewrap"><table class="data"><thead><tr><th>Blueprint</th><th>admin_required</th><th>login_required</th><th>無防備</th></tr></thead><tbody><tr><td>bp_auth</td><td>0</td><td>0</td><td>2（/login, /logout）</td></tr><tr><td>bp_chat</td><td>1（/api/mail/test）</td><td>14</td><td>0</td></tr><tr><td>bp_catalog</td><td>28</td><td>1（/api/catalog/table-info）</td><td>0</td></tr><tr><td>bp_import</td><td>15</td><td>0</td><td>0</td></tr><tr><td>bp_mail</td><td>3</td><td>0</td><td>0</td></tr><tr><td>bp_models</td><td>3</td><td>0</td><td>0</td></tr><tr><td>bp_knowledge</td><td>6</td><td>1（/api/knowledge/prefs）</td><td>0</td></tr><tr><td>bp_usage</td><td>4</td><td>0</td><td>0</td></tr><tr><td>bp_help</td><td>0</td><td>1</td><td>0</td></tr><tr><td>bp_table</td><td>0</td><td>3</td><td>0</td></tr><tr><td>bp_api</td><td>0</td><td>1（/api/file/&lt;token&gt;）</td><td>1（/vendor/plotly.min.js）</td></tr></tbody></table></div><div class="mt">設計の線引き:</div><div class="mt">・<b>カタログ・取り込み・モデル設定・メール設定・ナレッジベース登録・利用状況は「閲覧も含めて」管理者のみ</b>。理由は <code>admin_required</code> の docstring に明記されている（AIの回答の土台・DBの中身・送信先が変わるため）。画面側でメニューを隠すだけでは URL 直打ちで抜けられる。<br>・例外は <code>/api/catalog/table-info</code>（ER図のテーブル詳細）。チャットの読み取り専用ER図からも使い、返す内容は <code>describe_table</code> でAIに渡している範囲と同じなのでログイン済みなら見せる、と docstring で明示している。<br>・<code>/api/knowledge/prefs</code> と <code>/api/tables/prefs</code> は「自分の除外設定」なので login_required。<br>・<code>base.html</code> は非管理者に対して<b>管理メニューのセクションごと（チャットのリンクも含めて）非表示</b>にする。理由はコメントにあるとおり「行き先が1つだけのメニューは出さない」で、守りは <code>admin_required</code> 側にある。</div></td></tr>
      <tr><td>AI経路での権限（画面と同じ線を引く）</td><td><div class="mt">チャットは <code>_is_admin()</code>（＝<code>bool(getattr(g.get(&quot;user&quot;), &quot;is_admin&quot;, False))</code>）を <code>llm.build_system_prompt</code> / <code>tools.build_tools</code> / <code>tools.dispatch</code> に渡している。</div><div class="mt">・<code>build_tools(entries, admin=False)</code> は <code>name in ADMIN_TOOLS and not admin</code> のツールを<b>そもそも宣言に載せない</b>（AIは存在を知らないので呼ばれない）。<br>・<code>dispatch(..., admin=False)</code> は名指しで呼ばれても <code>&#x27;&lt;名前&gt;&#x27; は管理者だけが使えます。</code> を返す。コメントどおり<b>守りを2箇所で持つ</b>。<br>・<code>ADMIN_TOOLS</code> は各モジュールの申告を合わせたもので、実体は <code>explore_import_files</code>（取り込み元フォルダの調査＝<code>ADMIN_TOOLS_files</code>）と <code>analyze_usage</code>（他人の質問・失敗まで見える＝<code>ADMIN_TOOLS_usage</code>）の2つ。<code>search_knowledge_base</code> は <code>ADMIN_TOOLS_knowledge = set()</code> で全員に渡す。<br>・ヘルプ画面のツール一覧も <code>if name in tools.ADMIN_TOOLS and not g.user.is_admin: continue</code> で同じ線を引き、<code>bases=rag.kb_list() if g.user.is_admin else []</code> としている。</div></td></tr>
      <tr><td>_may_contribute_catalog（チャットからのカタログ書き込み）</td><td><pre class="mono small">def _may_contribute_catalog() -&gt; bool:
    return config.CATALOG_OPEN_CONTRIB or _is_admin()</pre><div class="mt"><code>config.CATALOG_OPEN_CONTRIB</code> は env <code>CATALOG_OPEN_CONTRIB</code>（既定 <b>false</b>）。</div><div class="mt">効くのは <code>POST /api/chat/glossary-save</code> と <code>POST /api/chat/save-example</code> の2本だけ。どちらも <code>login_required</code> の直後に <code>if not _may_contribute_catalog(): return jsonify({&quot;error&quot;: _CATALOG_CONTRIB_DENIED}), 403</code>。</div><div class="mt">既定を管理者のみにした理由は config.py と両関数の docstring に揃えて書かれている：カタログは全利用者のシステムプロンプトに毎回そのまま載り、用語の定義は「必ずその定義に従う」、用語のSQL式は「そのまま使う」とAIに指示しているので、ここを開けると<b>権限の低い利用者が管理者を含む全員の回答を左右できる</b>（書けるのは読み取り専用のSELECTだけだが、答えの中身は歪められる）。</div><div class="mt">どちらの設定でも、書き込みは <code>catalog_history.add_catalog_change(..., user=g.user.username, source=&quot;chat&quot;)</code> で必ず記録される。</div></td></tr>
      <tr><td>data/ 配下の保存レイアウト</td><td><div class="mt">パスはすべて <code>config.py</code> で決まり、env で個別に差し替えられる。<code>config.DATA_DIR</code>（既定 <code>&lt;プロジェクト&gt;/data</code>）は import 時に <code>mkdir(parents=True, exist_ok=True)</code> される。</div><div class="mt"><b>全員共通（data/ 直下）</b></div><div class="tablewrap"><table class="data"><thead><tr><th>パス</th><th>定数</th><th>中身</th><th>書けるのは</th><th>chmod</th></tr></thead><tbody><tr><td><code>統合.db</code></td><td>—</td><td>唯一のSQLite。<code>db.list_db_files()</code> は <code>DATA_DIR/*.db</code> を名前順で列挙</td><td>取り込み（管理者）</td><td>—</td></tr><tr><td><code>統合.db.meta.yaml</code></td><td><code>catalog.meta_path()</code></td><td>データカタログ（表/列の説明・用語集・例文・検算・関連・ビュー・ユーザー定義ツール・まとまりメモ）</td><td>管理者</td><td>—</td></tr><tr><td><code>.profile_cache/&lt;DB名&gt;.profile.json</code></td><td><code>PROFILE_CACHE_DIR</code></td><td>自動プロファイルの控え</td><td>自動生成</td><td>—</td></tr><tr><td><code>knowledge_bases.json</code></td><td><code>KNOWLEDGE_BASES_FILE</code></td><td>LightRAG接続先の登録簿（<b>APIキーを平文で持つ</b>）</td><td>管理者</td><td><b>0600 を試行</b></td></tr><tr><td><code>model_settings.yaml</code></td><td><code>MODEL_SETTINGS_FILE</code></td><td>候補モデル・既定・vision判定・文脈量上書き・<b>APIキー</b>・chat_url・models_url</td><td>管理者</td><td>しない</td></tr><tr><td><code>mail_settings.yaml</code></td><td><code>SMTP_SETTINGS_FILE</code></td><td>ホスト/ポート/タイムアウト・差出人・宛先許可リスト・通知先など（<b>秘密は入れない約束</b>。SMTP認証情報は env のみ）</td><td>管理者</td><td>しない</td></tr><tr><td><code>import_jobs.yaml</code></td><td><code>IMPORT_JOBS_FILE</code></td><td>定期取り込みジョブ</td><td>管理者</td><td>しない</td></tr><tr><td><code>import_dirs.yaml</code></td><td><code>IMPORT_DIRS_FILE</code></td><td>画面から足した取り込み元フォルダ（env の <code>IMPORT_DIRS</code> は画面から消せない土台）</td><td>管理者</td><td>しない</td></tr><tr><td><code>import_history.jsonl</code></td><td><code>IMPORT_HISTORY_FILE</code></td><td>取り込み1回=1行。上限 <code>IMPORT_HISTORY_MAX</code>(5000)</td><td>追記</td><td>—</td></tr><tr><td><code>catalog_history.jsonl</code></td><td><code>CATALOG_HISTORY_FILE</code></td><td>用語集・例文の変更1件=1行。上限 <code>CATALOG_HISTORY_MAX</code>(2000)</td><td>追記</td><td>—</td></tr></tbody></table></div><div class="mt"><b>利用者ごと（<code>config.USER_META_DIR</code> ＝ <code>data/users/</code>）</b></div><pre class="mono small">data/users/&lt;User.safe_key&gt;/
  prefs.yaml                 model / rag_off / rag_settings / tables_off の4キーのみ
  chats/index.json           一覧（id, title, created_at, updated_at, db_names, n_turns）
  chats/&lt;会話ID&gt;.json        会話の実体（messages と render_log）</pre><div class="mt"><b>プロジェクト直下</b></div><div class="mt">・<code>auth_users.yaml</code>（local プロバイダのユーザー定義。既定では<b>存在しない</b>）<br>・<code>.flask_secret</code>（セッション署名鍵）<br>・<code>env</code>（LLMキー・SMTP・取り込み先など。認証設定は入らない）</div><div class="mt"><code>.gitignore</code> は <code>data/*</code>・<code>data/users/</code>・<code>auth_users.yaml</code>・<code>.flask_secret</code>・<code>env*</code>(<code>env.example</code> を除く) を除外し、<code>data/*.meta.yaml</code> だけは全員共通の資産として git 管理する方針になっている。</div></td></tr>
      <tr><td>User.safe_key と、ユーザーごとのファイル入出力</td><td><pre class="mono small">@property
def safe_key(self) -&gt; str:
    return &quot;&quot;.join(c if (c.isalnum() or c in &quot;-_.@&quot;) else &quot;_&quot; for c in self.username)[:64]</pre><div class="mt"><code>str.isalnum()</code> は Unicode 準拠なので<b>日本語のユーザー名はそのまま残る</b>（<code>山田太郎</code> → <code>山田太郎</code>）。長さは64文字で切る。</div><div class="mt">・<code>chats.chats_dir(user)</code> = <code>USER_META_DIR / (user.safe_key or str(user)) / &quot;chats&quot;</code><br>・<code>prefs._prefs_path(user)</code> = <code>USER_META_DIR / _key(user) / &quot;prefs.yaml&quot;</code>（<code>_key</code> は safe_key と同じ決め方）</div><div class="mt">会話ファイル名は <code>chats._safe_id(chat_id)</code> で <code>[^0-9a-zA-Z_-]</code> を落として64文字に切るので、<code>..</code> や <code>/</code> は混ざらない。<code>new_id()</code> は <code>%Y%m%d-%H%M%S-</code> + uuid4の6桁で、ファイル名だけで新しい順に並ぶ。</div><div class="mt"><b>掃除は「一覧を読むついで」に行う</b>（常駐の掃除役を置かない）。<code>list_chats</code> → <code>_drop_expired</code>（<code>CHAT_HISTORY_DAYS</code>=90日、<code>updated_at</code> 起点。0で無期限）、<code>_upsert_index</code> → <code>CHAT_HISTORY_LIMIT</code>=100本を超えた古いものを実体ごと削除。<code>index.json</code> が壊れた/消えた場合は <code>_rebuild_index</code> が <code>chats/*.json</code> から作り直す。</div><div class="mt">生成ファイル（Excel等）は <code>render_log</code> に base64 で埋め込むが、<code>CHAT_EMBED_FILE_MAX_BYTES</code>(2MB) を超えるものは本体を捨てて <code>_no_data: True</code> だけ残す。</div><div class="mt"><code>prefs</code> は <code>KEYS = (&quot;model&quot;, &quot;rag_off&quot;, &quot;rag_settings&quot;, &quot;tables_off&quot;)</code> に無いキーを読み書きとも捨てる。<code>_save</code> は <code>_prefs_lock</code>（<code>threading.Lock</code>）で直列化。</div><div class="mt"><b>除外方式の理由</b>（<code>rag_excluded_ids</code> / <code>excluded_tables</code> の docstring）: 「選んだもの」ではなく「外したもの」を保存する。選択リスト方式だと、管理者が新しいナレッジベースや表を足したとき既存の利用者全員に見えないままになるため。</div></td></tr>
      <tr><td>検算（verify）とアラート</td><td><div class="mt"><b>検算ルール</b> は <code>data/&lt;DB&gt;.db.meta.yaml</code> の <code>checks:</code> に置く（＝管理者だけが編集できる場所）。<code>normalize()</code> が壊れた項目を落として揃え、<code>tolerance_pct</code> の既定は <code>DEFAULT_TOLERANCE_PCT = 0.5</code>（%）。左右のSQLは1行1列のスカラを返す約束で、<code>_scalar</code> は NULL を 0.0 として扱う。</div><div class="mt">実行の流れ:</div><div class="mt">・<code>tools.dispatch</code> が成功したら <code>_attach_verification(res, sqls, scope)</code> が <code>verify.alerts_for(sqls, scope)</code> を呼ぶ。ここで例外が出ても回答は止めない（<code>print</code> して素通り）。<br>・<code>alerts_for</code> は、実行されたSQLが触れた <code>(alias, table)</code> 集合と交わる検算だけを走らせ、<b>不一致だけ</b>返す（一致・実行不能は何も言わない。毎回「問題ありません」と言われると読まれなくなるため）。<br>・<code>run_check</code> の結果は <code>_verify_cache[(_fingerprint(check), _data_version(check, scope))]</code> にキャッシュ。<code>_data_version</code> は関係するDBファイルの <code>st_mtime_ns</code>。<b>データが変わった後の最初の1回しか実際には実行されない</b>。<code>_CACHE_MAX = 300</code> を超えたら丸ごと clear。<br>・不一致で <code>drilldown</code> があれば <code>DRILL_ROWS = 8</code> 行だけ内訳を取る。<br>・チャット側は <code>_fresh_alerts(chat, alerts)</code> で、<code>render_log</code> に既にある <code>verify_key</code> を除く。<code>key</code> は <code>verify||owner||name||md5(指紋)[:8]||version</code> という形で、<b><code>hash()</code> を使わない</b>（プロセスごとに変わって再起動のたびに同じ警告が出直すため）。<br>・残った警告は <code>_merge_alerts</code> でツール結果JSONの <code>verification_warnings</code> に混ぜてLLMへ渡し、同時に <code>verify.render_item(a)</code> を画面カードとして積む。</div><div class="mt"><b>取り込み失敗のメール通知</b>（<code>mailer.alert_import_problems</code>）は <code>SmtpSettings.alert_to</code> が空か <code>alert_enabled=False</code> なら送らない。<code>ALERT_KINDS = (&quot;failed&quot;, &quot;degraded&quot;, &quot;overdue&quot;)</code> のうち <code>alert_kinds</code> に選ばれた種類だけを見て、<b>「健全→失敗」「失敗→復旧」の変わり目でのみ1通</b>送る（15分間隔なら1日96通になるのを避けるため）。スケジューラの <code>tick()</code> から呼ばれ、<code>_state[&quot;tick_count&quot;] &gt; 1</code> の周回からしか送らない（起動直後の1周目は「変化」ではない）。</div><div class="mt"><b>起動時の警告</b> <code>_warn_if_no_admin()</code> は <code>create_app()</code> の中で1回だけ走る。<code>auth.admin_enabled()</code> が真なら何もしない。偽で local プロバイダなら <code>auth_users.yaml</code> に <code>AUTH_ADMIN_GROUP</code> を持つユーザーが居るかを見て、居なければ標準出力に「管理者が1人も居ません」と出す。http プロバイダなら（グループを返さない前提で）無条件に警告する。気づけるのが「設定を直したいとき」になってしまうので起動時に言う、という判断が docstring に書いてある。同じく <code>_ensure_default_db()</code> が <code>.db</code> ゼロなら <code>data/データ.db</code> を作る。</div></td></tr>
      <tr><td>同時実行（waitress のスレッドと threading.local）</td><td><div class="mt">起動は <code>python core.py</code>（引数なし）で <code>create_app()</code> → <code>waitress.serve(app, host=HOST, port=PORT, threads=THREADS)</code>。<code>HOST=&quot;0.0.0.0&quot;</code> / <code>PORT=8000</code> / <code>THREADS=8</code> / <code>DEBUG=False</code> は<b>末尾のコード内定数で、env も環境変数も読まない</b>（<code>PORT</code> を他のソフトが環境変数で持っていると別ポートで起動する事故があるため、と明記）。waitress が無ければ Flask 開発サーバ（<code>threaded=True, use_reloader=False</code>）に落ちる。</div><div class="mt"><b>ワーカー（プロセス）は必ず1</b>。理由は <code>scheduler.start()</code> が立てる定期取り込みスレッドがワーカーの数だけ立ち、同じジョブを多重実行してしまうから。同時アクセス数はスレッド数で稼ぐ。<code>scheduler</code> は <code>_THREAD_NAME = &quot;aiagent-import-scheduler&quot;</code> の生存をスレッド名で確認して二重起動を防ぎ、<code>_stop</code>（<code>threading.Event</code>）で <code>wait</code> するので終了の合図で即抜ける。このスレッドには <b>リクエスト文脈が無いので <code>g</code> / <code>request</code> を使わない</b>（状態は <code>_state</code> に置いて画面が読む）。</div><div class="mt"><b><code>threading.local</code> は2つだけ</b>。どちらも「リクエストを処理しているスレッドに置いて、web 側が質問のたびに入れ直す」方式。</div><div class="tablewrap"><table class="data"><thead><tr><th>変数</th><th>置くもの</th><th>入れる場所</th><th>読む場所</th></tr></thead><tbody><tr><td><code>_rag_local</code>（元 rag/retriever.py）</td><td>いまの利用者</td><td><code>_begin_turn</code> の <code>rag.set_current_user(g.user)</code>、SSEの <code>generate()</code> 冒頭</td><td><code>rag_user_settings</code> / <code>rag_excluded_ids</code> / <code>excluded_tables</code> / <code>rag_targets</code> の引数省略時</td></tr><tr><td><code>_turn_local</code>（元 tools/results.py）</td><td>いまの質問の識別子</td><td><code>_begin_turn</code> の <code>results.new_turn()</code>、SSEの <code>generate()</code> で <code>results.set_turn(turn_id)</code></td><td><code>results.put</code> / <code>find_by_sql</code></td></tr></tbody></table></div><div class="mt"><code>_rag_local</code> が要るのは「<code>dispatch</code> が引数に利用者を持たない（35個のツールすべての形が変わるため）」から、<code>_turn_local</code> が要るのは「同じ質問の中でだけSQLの結果を使い回す」ため（質問をまたぐと、間にリアルタイム取り込みが走って古い数字を返しかねない）。</div><div class="mt">SSE (<code>POST /api/chat/stream</code>) は <code>stream_with_context</code> で流すが、<b><code>generate()</code> の冒頭で <code>rag.set_current_user(user)</code> と <code>results.set_turn(turn_id)</code> をやり直している</b>。Flask の <code>g</code> / <code>session</code> は ContextVar ベースの文脈に乗るので流し込み先のスレッドでも見えるが、<code>threading.local</code> は乗らないため。また <code>session[&quot;chat_id&quot;]</code> は<b>応答を流し始める前に</b>確定させる（流し始めた後に書いても Cookie に載らず、次の質問が別の会話として始まってしまう）。</div><div class="mt"><b>プロセス内共有の入れ物とロック</b></div><div class="tablewrap"><table class="data"><thead><tr><th>入れ物</th><th>ロック</th><th>上限</th></tr></thead><tbody><tr><td><code>_files</code>（生成ファイル、元 web/filestore.py）</td><td><code>_fs_lock</code></td><td><code>_MAX_ITEMS = 200</code></td></tr><tr><td><code>_store</code>（SELECT結果、元 tools/results.py）</td><td><b>無し</b></td><td><code>MAX_ENTRIES = 40</code> / <code>MAX_CELLS = 400_000</code></td></tr><tr><td><code>_meta_cache</code>（カタログYAML）</td><td>無し（mtime_ns+size で判定）</td><td>無し</td></tr><tr><td><code>_verify_cache</code></td><td>無し</td><td><code>_CACHE_MAX = 300</code></td></tr><tr><td><code>_models_cache</code></td><td><code>_models_lock</code>（無効化時のみ）</td><td><code>_CACHE_SEC = 300</code></td></tr><tr><td><code>_sent_log</code>（メール送信記録）</td><td><code>_mailer_lock</code></td><td><code>_MAX_LOG = 200</code></td></tr><tr><td><code>_prefs_lock</code> / <code>_kb_lock</code> / <code>_history_lock</code> / <code>_catalog_history_lock</code></td><td>各ファイル書き込みを直列化</td><td>—</td></tr></tbody></table></div><div class="mt">SQLite は接続を都度作って都度閉じる（<code>connect_ro</code> / <code>connect_scope</code>）ので、<code>check_same_thread</code> の既定のままでスレッドをまたがない。</div></td></tr>
      <tr><td>生成ファイルの持ち主チェック</td><td><div class="mt">ツールが作るバイト列は <code>_fs_put(data, filename, mime, owner=g.user.username)</code> でプロセス内 <code>OrderedDict</code> に預け、トークン（<code>secrets.token_urlsafe(16)</code>）だけを画面に渡す。ディスクには書かない。</div><div class="mt"><code>_fs_get(token, owner)</code> は <code>item[&quot;owner&quot;] != owner</code> なら None を返す。<code>GET /api/file/&lt;token&gt;</code> は <code>login_required</code> の上で <code>_fs_get(token, g.user.username)</code> を通し、外れれば <code>abort(404)</code>（403ではなく404で存在も隠す）。画像アップロード・取り込みアップロード・利用状況Excelもすべて同じ仕組みを通る。</div><div class="mt"><b>持ち主の識別子は <code>safe_key</code> ではなく生の <code>username</code></b>。</div></td></tr>
      <tr><td>ユーザー管理CLI（python core.py users …）</td><td><div class="mt"><code>users_cli</code> は <code>argparse</code> で <code>list</code> / <code>add</code> / <code>passwd</code> / <code>remove</code> を持つ。</div><div class="mt">・<code>add &lt;名前&gt; [--display-name] [--groups a,b] [--admin] [--password]</code>。<code>--admin</code> は <code>AUTH_ADMIN_GROUP</code> を groups に足す。同名（大文字小文字無視）が居れば <code>sys.exit</code>。<br>・パスワードは既定で <code>getpass</code> の2回入力。<code>--password</code> を使うと「コマンドラインで渡したパスワードは履歴に残ります。」と stderr に警告する。<br>・<code>remove</code> は「※ 個人カタログ（data/users/配下）は残ります。不要なら手動で削除してください。」と明示的に案内する（<b>退職者のデータは自動では消えない</b>）。</div><div class="mt">CLIは <code>if __name__ == &quot;__main__&quot;</code> の中で <code>sys.argv[1]</code> を見て分岐し、<code>users</code> / <code>refresh</code> / <code>selftest</code> 以外は使い方を出して終了する。CLI経路ではサーバもスケジューラも起動しない。直起動時は <code>_sys.modules.setdefault(&quot;core&quot;, _sys.modules[__name__])</code> で <code>__main__</code> と <code>core</code> を同じ実体に向け、後から <code>import core</code> が走ってスケジューラが二重に立つのを防いでいる。</div></td></tr>
      <tr><td>主なデータ構造</td><td>・auth.User = dataclass(username: str, display_name: str = &quot;&quot;, groups: list = [], is_admin: bool = False) / __post_init__ で display_name を username で埋める / .safe_key プロパティ<br>・session[&quot;user&quot;] = {&quot;username&quot;: str, &quot;display_name&quot;: str, &quot;groups&quot;: [str], &quot;is_admin&quot;: bool}  ← login_user が書く4キーだけ<br>・session[&quot;chat_id&quot;] = str | 未設定  ← セッションに入るもう1つの値<br>・g.user = auth.User | None  ← load_user_into_context が毎リクエスト作り直す<br>・auth_users.yaml = {&quot;users&quot;: [{&quot;username&quot;, &quot;display_name&quot;, &quot;password_hash&quot;, &quot;groups&quot;: [str]}]}<br>・password_hash = &quot;pbkdf2_sha256$200000$&lt;salt hex 32桁&gt;$&lt;dk hex&gt;&quot;<br>・data/users/&lt;safe_key&gt;/prefs.yaml = {model: str, rag_off: [kb_id], rag_settings: {...}, tables_off: [表名]}（KEYS 以外は読み書きとも捨てる）<br>・data/users/&lt;safe_key&gt;/chats/index.json = {&quot;chats&quot;: [{id, title, created_at, updated_at, db_names: [str], n_turns: int}]}<br>・data/users/&lt;safe_key&gt;/chats/&lt;ID&gt;.json = {id, title, created_at, updated_at, db_names, table_names: [&quot;DB名.表名&quot;], tables: {}, messages: [LLM用・systemは保存しない], render_log: [{role, kind, at, ...}]}<br>・render_log の作成ファイル項目 = {kind:&quot;file&quot;, filename, mime, data(base64), _b64: True} または {..., _no_data: True}（2MB超）<br>・knowledge_bases.json = [{id: uuid4hex[:12], name, base_url, api_key, description, enabled, created_at}] ／ 画面へ出すときは _kb_redact で api_key を落として has_api_key: bool に置換<br>・model_settings.yaml = {models: [str], default: str, vision: [str], context_overrides: {モデル名小文字: int}, api_key: str, chat_url: str, models_url: str}（ADMIN_KEYS 以外は捨てる）<br>・mail_settings.yaml = EDITABLE_KEYS のみ = host, port, timeout, sender, sender_name, senders, allow_addresses, max_recipients, dry_run, alert_to, alert_enabled, alert_kinds, ok_domains<br>・catalog_history.jsonl の1行 = {at, kind: &quot;glossary&quot;|&quot;example&quot;, op: &quot;add&quot;|&quot;update&quot;|&quot;remove&quot;, db, table, name, user, source: &quot;chat&quot;|..., before, after}<br>・_files[token] = {&quot;data&quot;: bytes, &quot;filename&quot;: str, &quot;mime&quot;: str, &quot;owner&quot;: username}（プロセス内 OrderedDict・最大200）<br>・_store[result_id] = {scope: scope_key, columns, rows, truncated, sql, norm_sql, turn, label}（プロセス内 OrderedDict・ユーザー別ではない）<br>・verify の検算ルール（meta.yaml の checks:）= {name, left:{label,sql}, right:{label,sql}, tolerance_pct, drilldown, enabled}<br>・verify のアラート = {key: &quot;verify||owner||name||md5指紋8桁||version&quot;, name, left_label, left, right_label, right, diff, pct, tolerance_pct, drill}</td></tr>
      <tr><td>定数・しきい値</td><td>・AUTH_PROVIDER = &quot;local&quot;（auth.py 冒頭。&quot;http&quot; にすると社内認証APIへ）<br>・AUTH_USERS_FILE = &lt;auth.py と同じフォルダ&gt;/auth_users.yaml（既定の配布物には存在しない）<br>・AUTH_ADMIN_GROUP = &quot;admin&quot;（完全一致。部分一致はしない）<br>・ADMIN_USER / ADMIN_PASS（常設の管理者。実際の値は auth.py 冒頭を参照。ADMIN_PASS が空文字ならアカウントごと無効）<br>・BUILTIN_USERS（動作確認用の一般利用者。IDとパスワードが同じなので、本番では空リストにして仕組みごと止める。値は auth.py 冒頭を参照）<br>・AUTH_API_TIMEOUT = 10（秒）／AUTH_API_SUCCESS_FIELD が空なら HTTP 200 で成功扱い／AUTH_API_GROUPS_FIELD が空なら全員一般ユーザー<br>・_ITER = 200_000（PBKDF2-SHA256 の反復数。検証は保存側の値を使うので後から上げられる）<br>・User.safe_key の許可文字 = isalnum() または &quot;-_.@&quot;、最大64文字<br>・SECRET_KEY = FLASK_SECRET_KEY &gt; .flask_secret の中身 &gt; secrets.token_urlsafe(48) を生成して保存（0600 を試行）<br>・SESSION_COOKIE_HTTPONLY = True / SESSION_COOKIE_SAMESITE = &quot;Lax&quot; / SESSION_COOKIE_SECURE は未設定 / session.permanent = False<br>・MAX_CONTENT_LENGTH = 64 * 1024 * 1024（Flask 側の上限。IMPORT_MAX_FILE_MB=100 より先に効く）<br>・config.USER_META_DIR = DATA_DIR / &quot;users&quot;<br>・config.CATALOG_OPEN_CONTRIB = env CATALOG_OPEN_CONTRIB（既定 false ＝ カタログ書き込みは管理者のみ）<br>・CHAT_HISTORY_LIMIT = 100（本） / CHAT_HISTORY_DAYS = env 既定90（0で無期限） / CHAT_EMBED_FILE_MAX_BYTES = 2MB<br>・CATALOG_HISTORY_MAX = 2000（1.2倍を超えたら間引く） / IMPORT_HISTORY_MAX = 5000<br>・filestore: _MAX_ITEMS = 200 / トークンは secrets.token_urlsafe(16)<br>・results: MAX_ENTRIES = 40 / MAX_CELLS = 400_000<br>・verify: DEFAULT_TOLERANCE_PCT = 0.5(%) / DRILL_ROWS = 8 / _CACHE_MAX = 300<br>・mailer: ALERT_KINDS = (&quot;failed&quot;, &quot;degraded&quot;, &quot;overdue&quot;) / _MAX_LOG = 200 / SMTP_MAX_RECIPIENTS = 20 / SMTP_DRY_RUN 既定 true<br>・IMAGE_MAX_MB = 8 / IMAGE_MAX_COUNT = 4<br>・起動: HOST = &quot;0.0.0.0&quot; / PORT = 8000 / THREADS = 8 / DEBUG = False（core.py 末尾の定数。env も環境変数も読まない）<br>・IMPORT_SCHEDULER_TICK_SEC = 60（実際の待ちは max(5, tick_sec)）</td></tr>
    </tbody></table></div>
    <div class="card__title mt">落とし穴（20件）</div>
    <div class="tablewrap"><table class="data"><thead><tr><th style="width:60px">#</th><th>内容</th></tr></thead><tbody>
      <tr><td class="mono small">01</td><td>権限はログイン時点の写しであって、リクエストごとに再検証しない。load_user_into_context は session の辞書を auth.User(**data) に戻すだけで、auth_users.yaml も LDAP も見に行かない。したがって管理者グループから外しても・ユーザーを remove しても、その人のブラウザを閉じるまで管理者のまま操作できる。強制的に無効化する手段は .flask_secret（または FLASK_SECRET_KEY）を差し替えて全員をログアウトさせることだけ。</td></tr>
      <tr><td class="mono small">02</td><td>auth.User にフィールドを1つ足すと、既にログイン中の全員が 500 になる。session に入っているのは古い4キーの辞書で、load_user_into_context の auth.User(**data) は before_request なので全ルートで落ちる。逆にフィールドを消した場合も TypeError。User の形を変えるときは Cookie の互換を考えるか、鍵を差し替えて全員を追い出すこと。</td></tr>
      <tr><td class="mono small">03</td><td>/login の next 検査は nxt.startswith(&quot;/&quot;) だけなので、//evil.example.com のようなプロトコル相対URLを通してしまう（オープンリダイレクト）。login_required が付ける next は request.path なので通常は問題にならないが、URLは外から作れる。</td></tr>
      <tr><td class="mono small">04</td><td>CSRF対策が一切ない（トークンもOrigin検査も無い）。守りは SESSION_COOKIE_SAMESITE=&quot;Lax&quot; だけで、POST /logout も含めて全POSTが同じ状況。SESSION_COOKIE_SECURE も設定していないので、HTTPS 前段を置く場合はそこで補うことになる。</td></tr>
      <tr><td class="mono small">05</td><td>safe_key はパス区切りを潰すが &quot;.&quot; は許可文字に入っている。username が &quot;..&quot; のプロバイダを繋ぐと data/users/../chats/ すなわち data/chats/ に書きに行ける。BUILTIN/常設adminは定数なので安全、auth_users.yaml は管理者が書くので実害は薄いが、HTTP認証APIの応答を素通しする経路では成立しうる。</td></tr>
      <tr><td class="mono small">06</td><td>HttpApiAuthProvider は応答から username を読むのに AUTH_API_USER_FIELD（＝リクエスト側のキー名）を使い回す。認証APIがそのキーを返さないと、フォールバックで「利用者が打った文字列」がそのまま username になる。すると Yamada と yamada で data/users/ のフォルダが2つに割れ、チャット履歴とモデル選択が別物になる。local プロバイダは YAML の綴りを返すのでこの問題が無い（照合は lower で行い、返す値は正本を使う、という対比になっている）。</td></tr>
      <tr><td class="mono small">07</td><td>auth_users.yaml は配布物に存在しない。したがって既定構成では LocalAuthProvider は常に None を返し、実際に通るのは常設 admin と BUILTIN_USERS の4人だけ。それでも「ユーザーが1人も居ません」の案内（setup_needed）は ADMIN_PASS が設定されていると出ないので、画面からは local プロバイダが空であることに気づけない。</td></tr>
      <tr><td class="mono small">08</td><td>AuthProvider.hint（LocalAuthProvider は「社内LDAP導入までの暫定アカウントです。」）は login.html に渡されておらず、どこにも表示されない死んだ属性。</td></tr>
      <tr><td class="mono small">09</td><td>base.html は非管理者に対して管理メニューのセクションをまるごと隠すが、その中には「チャット」のリンクも入っている。一般利用者のサイドバー上部は「ヘルプ」だけになる。仕様であってバグではない（コメントに「行き先が1つだけのメニューは出さない」とある）が、初見では権限バグに見える。</td></tr>
      <tr><td class="mono small">10</td><td>results の _store（result_id → SELECT結果）はプロセス内で全ユーザー共有で、get() が確かめるのは scope（DBファイルのパス集合）だけ。このアプリはDBが1つなので scope は誰でも同じ文字列になり、実質「result_id を知っていれば誰でも読める」。ID は LLM にしか渡らないので現実の露出は小さいが、ユーザー境界ではない。さらに _store には一切ロックが無く、waitress の8スレッドから put/_evict/find_by_sql が同時に走ると「dictionary changed size during iteration」を踏み得る（_files には _fs_lock がある）。</td></tr>
      <tr><td class="mono small">11</td><td>knowledge_bases.json は APIキーを平文で持つため os.chmod 0600 を試すが、同じくキーを平文で持つ model_settings.yaml（_write_admin）は chmod していない。加えて Windows では chmod は事実上効かないので、どちらも「data/ を直接読める人には無防備」。auth.py の docstring が「OSレベルのアクセス制御ではない」と断っているのはこの点。</td></tr>
      <tr><td class="mono small">12</td><td>rag_targets / rag_user_settings / excluded_tables を引数なしで呼ぶ経路が4つある（knowledge_tool_schemas / build_system_prompt のKB一覧 / ナレッジ検索ツールの実処理2箇所）。ここは threading.local の _rag_local を読む。set_current_user を通るのは _begin_turn と SSE の generate() だけなので、モデル設定画面の llm.budget → build_tools のようにチャット以外から build_tools が呼ばれると、そのスレッドに残っていた「前の人」の除外設定が使われる。表示上の見積もりにしか効かないが、スレッド使い回しに由来する取り違えなので原因が追いにくい。</td></tr>
      <tr><td class="mono small">13</td><td>SSE の /api/chat/stream は generate() の中で rag.set_current_user と results.set_turn をやり直す。g と session は ContextVar ベースの Flask 文脈なのでスレッドをまたいでも見えるが、threading.local は見えないため。この2行を消すと「同じ質問なのに前の人の設定で検索する」「同じSQLを2回実行する」が起きる。</td></tr>
      <tr><td class="mono small">14</td><td>session[&quot;chat_id&quot;] は応答を流し始める前に必ず書く必要がある。stream() が chat[&quot;id&quot;] をその場で確定させてセッションに入れているのはこのため。流し始めた後に session を書いても Set-Cookie に載らず、次の質問が別の会話として始まる。</td></tr>
      <tr><td class="mono small">15</td><td>/api/import/upload は importer.check_upload で IMPORT_MAX_FILE_MB（既定100MB）を見るが、その前に Flask の MAX_CONTENT_LENGTH（64MB）が効く。64〜100MB のファイルは日本語のエラーではなく素の 413 で弾かれる。</td></tr>
      <tr><td class="mono small">16</td><td>dirs_edit（POST /api/import/dirs）は @admin_required が付いているのに、関数の中でもう一度 if not g.user.is_admin: 403 を書いている。到達不能な二重チェックで、直せば消せる冗長。</td></tr>
      <tr><td class="mono small">17</td><td>config.py は load_dotenv(&quot;./env&quot;) → load_dotenv(BASE_DIR/&quot;env&quot;) の順で読む。python-dotenv の既定は override=False なので、先に読んだ ./env（＝カレントディレクトリ）が勝ち、さらに本物の環境変数が両方に勝つ。別ディレクトリから起動すると意図しない env が効く。ただし認証設定は env に無いので、この影響は認証には及ばない。</td></tr>
      <tr><td class="mono small">18</td><td>起動用の HOST / PORT / THREADS / DEBUG は core.py 末尾のコード内定数で、env も環境変数も読まない（PORT を他ソフトが環境変数で持っていた事故への対処と明記されている）。「env に PORT を書いたのに変わらない」は仕様。</td></tr>
      <tr><td class="mono small">19</td><td>ワーカー（プロセス）は必ず1にすること。scheduler.start() の定期取り込みスレッドがワーカーごとに立ち、同じジョブを多重実行する。gunicorn を使うなら -w 1、同時接続はスレッド数で増やす。</td></tr>
      <tr><td class="mono small">20</td><td>python core.py users remove はログイン情報を消すだけで、data/users/&lt;safe_key&gt;/ 配下のチャット履歴と prefs は残る（CLI 自身が最後にそう案内する）。退職者対応では手で消す必要がある。</td></tr>
    </tbody></table></div>
  </div>
{% endraw %}
{% endif %}

  <div class="small muted mt mb">
    解決しないときは、システム管理者に連絡してください。エラーが出た場合は、
    エラーメッセージの文面と、直前の質問文を添えると調査が早くなります。
  </div>
</div>
{% endblock %}
""",

# --- import.html ---
"import.html": r"""{% extends "base.html" %}
{% from "_icons.html" import icon %}
{% block title %}データカタログ（取り込み） — {{ app_title }}{% endblock %}
{# 見出しは置かない。画面の説明はサイドバーの項目にマウスを乗せると出る #}

{% block body %}
<div class="content content--wide">
  {# データカタログの一機能。同じタブバーを出して、行き来が同じ画面の中に見えるようにする。
     他のタブはカタログ画面へ。 #}
  <div class="tabs tabs--bar">
    <a class="tab" href="{{ url_for('catalog.index') }}#tab=tables">テーブル</a>
    <a class="tab" href="{{ url_for('catalog.index') }}#tab=er">結合・ER図</a>
    <a class="tab" href="{{ url_for('catalog.index') }}#tab=glossary">用語集・例文</a>
    <a class="tab" href="{{ url_for('catalog.index') }}#tab=tools">ツール</a>
    <button class="tab is-active">取り込み</button>
  </div>

  <!-- ================= 取り込み ================= -->
  <div id="pane-file">
    <details class="acc" {{ 'open' if dirs|selectattr('ok', 'equalto', false)|list }}>
      <summary>取り込み元フォルダ
        <span class="badge">{{ dirs|length }}</span>
        {% set ng = dirs|selectattr('ok', 'equalto', false)|list %}
        {% if ng %}<span class="badge badge--err">{{ ng|length }}件に問題あり</span>{% endif %}
      </summary>
      <div class="acc__body">
        <div id="dirList"></div>
        {% if user.is_admin and dirs_editable %}
        <div class="row mt">
          <input type="text" id="newDir" class="grow"
                 placeholder="追加するフォルダのパス（例: /mnt/real/real2 や \\\\server\\share\\取込）">
          <button class="btn btn--sm" id="addDir">＋ フォルダを追加</button>
        </div>
        <div class="small muted mt">
          ここに追加したフォルダは <code>data/import_dirs.yaml</code> に保存され、再起動後も残ります。
          <code>env</code> の <code>IMPORT_DIRS</code> で指定した分は画面からは消せません。
          <b>追加したフォルダ配下のファイルは全ユーザーが読めるようになります。</b>
        </div>
        {% else %}
        <div class="small muted mt">
          フォルダの追加・削除は管理者のみです。
          （<code>env</code> の <code>IMPORT_DIRS</code> でも設定できます）
        </div>
        {% endif %}
      </div>
    </details>

    <div class="card">
      <div class="row" style="align-items:center">
        <div class="card__title" style="margin:0">取り込むファイル</div>
        <div class="spacer"></div>
        <button class="btn btn--sm" id="pickServer">サーバのフォルダから選ぶ</button>
        {% if allow_upload %}
          <button class="btn btn--sm" id="pickLocal">自分のPCから選ぶ</button>
          <input type="file" id="localFile" class="hidden"
                 accept=".csv,.tsv,.txt,.xlsx,.xlsm">
        {% endif %}
      </div>
      <div id="chosen" class="mt">
        <div class="small muted">まだ選ばれていません。右上のボタンからファイルを選んでください。</div>
      </div>
      <div id="readOpts" class="row mt hidden">
        <div id="sheetWrap" class="hidden" style="width:190px">
          <label class="field">シート</label><select id="sheet"></select>
        </div>
        <div id="sepWrap" style="width:190px">
          <label class="field">区切り文字</label>
          <select id="delimiter">
            {% for d in delimiters %}<option>{{ d }}</option>{% endfor %}
          </select>
        </div>
        <div style="width:110px">
          <label class="field">見出しの行</label>
          <input type="number" id="headerRow" value="1" min="1" max="50">
        </div>
        <button class="btn btn--sm" id="reload">読み直す</button>
      </div>
    </div>

    <div id="previewArea"></div>
  </div>
{# content--wide の閉じ。これが無いと、この画面だけ div が1つ開いたままになり、
   DOMの入れ子が他の画面とずれる（実測: 描いた画面の深さが +1 だった） #}
</div>

{% endblock %}

{% block scripts %}
<!-- サーバのフォルダを辿って選ぶダイアログ -->
<div class="modal hidden" id="browser">
  <div class="modal__box">
    <div class="modal__head">
      <b>ファイルを選ぶ</b>
      <div class="spacer"></div>
      <button class="btn btn--sm btn--ghost" id="browserClose" title="閉じる" aria-label="閉じる">{{ icon('x', 'icon--sm') }}</button>
    </div>
    <div class="modal__crumbs" id="crumbs"></div>
    <div class="modal__body" id="browserList"></div>
    <div class="modal__foot small muted">
      表示されるのは許可された取り込み元フォルダの中だけです（{{ extensions }}）。
    </div>
  </div>
</div>

<script>
window.IMP = {
  allowUpload: {{ allow_upload|tojson }},
  dbFiles: {{ db_files|tojson }},
  existing: {{ existing|tojson }},
  groups: {{ groups|tojson }},
  manage: {{ manage|tojson }},
  intervals: {{ intervals|tojson }},
  modes: {{ modes|tojson }},
  defaultTs: {{ default_ts|tojson }},
  maxKeep: {{ max_keep|tojson }},
  defaultKeep: {{ default_keep|tojson }}
};
</script>
{% endblock %}
""",

# --- knowledge.html ---
"knowledge.html": r"""{% extends "base.html" %}
{% block title %}ナレッジベース — {{ app_title }}{% endblock %}
{# 見出しは置かない。画面の説明はサイドバーの項目にマウスを乗せると出る #}

{% block body %}
<div class="content">
  <div id="banner"></div>

  <details class="card" id="howto">
    <summary class="card__title" style="cursor:pointer">この画面の使い方</summary>
    <div class="card__desc" style="margin-top:8px">
      社内文書の検索は、別に立てた <b>LightRAG サーバ</b>へHTTPで問い合わせます。
      このアプリは文書の索引を持ちません（索引作成は重く、別のサーバで動かすため）。
      <ol style="margin:8px 0 0 18px;padding:0;line-height:1.9">
        <li>LightRAG サーバの <b>URL</b> と <b>APIキー</b> を「ナレッジベースを追加」に入れる</li>
        <li>「接続テスト」でつながることを確かめる</li>
        <li><b>説明</b>に「何が入っているか・どんなときに使うか」を書く</li>
      </ol>
      <div class="mt">
        追加した瞬間から、チャットのAIがそのナレッジベースを検索できるようになります。
        <b>説明はAIがそのまま読みます</b>。AIがどのナレッジベースを調べるか決める材料は
        名前と説明しかないので、ここの書き方で検索の当たり外れが変わります。
      </div>
      <div class="mt">
        URLは次のどの形でも受け付けます（末尾スラッシュ・前後の空白は自動で除去）。
        スキームを省略すると <code>http://</code> を補うので、
        <b>HTTPSの環境では必ず https:// から書いてください</b>。
        <pre class="mono" style="margin:6px 0 0">https://rag.example.co.jp
https://rag.example.co.jp/lightrag     ← リバースプロキシ配下(--api-prefix)
http://10.20.30.40:9621</pre>
      </div>
    </div>
  </details>

  <div class="card">
    <div class="card__title">登録されているナレッジベース</div>
    <div class="card__desc">
      「検索対象にする」を外すと、その環境は全利用者の検索から外れます
      （チャット画面の一覧にも出なくなります）。
      APIキーは伏せ字で表示され、「表示」を押したときだけ実値を取りに行きます。
    </div>
    <div id="kbList"></div>
  </div>

  <div class="card">
    <div class="card__title">ナレッジベースを追加</div>
    <div class="row">
      <div style="width:220px">
        <label class="field">名前</label>
        <input type="text" id="newName" placeholder="例: 設備マニュアル">
      </div>
      <div class="grow" style="min-width:260px">
        <label class="field">URL</label>
        <input type="text" id="newUrl" placeholder="例: http://10.20.30.40:9621">
      </div>
      <div style="width:200px">
        <label class="field">APIキー</label>
        <input type="password" id="newKey" placeholder="払い出されたキー" autocomplete="new-password">
      </div>
    </div>
    <div class="row mt">
      <div class="grow">
        <label class="field">説明（AIがこれを読んで、どのナレッジベースを調べるか決めます）</label>
        <input type="text" id="newDesc"
               placeholder="例: 装置の取扱説明書・保全手順・図面。復旧手順や仕様を調べるときに使う。">
      </div>
      <button class="btn btn--primary" id="add">＋ 追加</button>
    </div>
  </div>

  <div class="card">
    <div class="card__title">検索の効き方の初期値</div>
    <div class="card__desc">
      利用者はチャット画面のサイドバーから個別に変えられます。ここに出ているのは
      <b>まだ自分で変えていない人が使う値</b>で、<code>env</code>（{{ 'RAG_RETRIEVE_MODE / RAG_CHUNK_TOP_K / RAG_TOP_K / RAG_MAX_CONTEXT_CHARS' }}）
      で決まります。env を変えれば、設定を触っていない利用者はその新しい値に追随します。
    </div>
    <div id="defaults"></div>
  </div>
</div>
{% endblock %}

{% block scripts %}
<script>
window.KB_INIT = {
  bases: {{ bases|tojson }},
  defaults: {{ defaults|tojson }},
  fields: {{ fields|tojson }}
};
</script>
{% endblock %}
""",

# --- login.html ---
"login.html": r"""{% from "_icons.html" import icon %}<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ログイン — {{ app_title }}</title>
<link rel="stylesheet" href="{{ url_for('static', filename='css/app.css') }}">
</head>
<body>
{% include "_icons.html" %}
<div class="loginpage">
  <div class="loginbox">
    <div class="brand">
      {{ icon('spark') }}
      <h1>{{ app_title }}</h1>
    </div>

    {% if fatal %}
      <div class="alert alert--err">{{ fatal }}</div>
    {% else %}
      {% for category, message in get_flashed_messages(with_categories=true) %}
        <div class="alert alert--{{ 'err' if category == 'error' else 'warn' if category == 'warning' else category }}">{{ message }}</div>
      {% endfor %}

      <div class="card">
        <form method="post">
          <label class="field" for="u">ユーザー名</label>
          <input id="u" name="username" type="text" autocomplete="username" autofocus required>
          <div style="height:12px"></div>
          <label class="field" for="p">パスワード</label>
          <input id="p" name="password" type="password" autocomplete="current-password" required>
          <div style="height:16px"></div>
          <button class="btn btn--primary" style="width:100%">ログイン</button>
        </form>
      </div>

      {% if setup_needed %}
        <div class="alert alert--warn">
          まだユーザーが登録されていません。次のコマンドで作成してください。
          <pre class="mono" style="margin:8px 0 0;white-space:pre-wrap">python core.py users add &lt;ユーザー名&gt; --admin</pre>
        </div>
      {% endif %}
    {% endif %}
  </div>
</div>
</body>
</html>
""",

# --- mail.html ---
"mail.html": r"""{% extends "base.html" %}
{% block title %}メール設定 — {{ app_title }}{% endblock %}
{# 見出しは置かない。画面の説明はサイドバーの項目にマウスを乗せると出る #}

{% block body %}
<div class="content">
  <div id="banner"></div>

  <div class="card">
    <div class="card__title">送信サーバ</div>
    <div class="card__desc">
      社内リレー宛にそのまま送ります（暗号化・認証なし）。
      分からない場合は情報システム部門に確認してください。
      保存するとすぐ反映されます（再起動は不要）。
    </div>
    <div class="row mb">
      <div class="grow" style="max-width:360px">
        <label class="field">ホスト名</label>
        <input type="text" id="host" placeholder="例: relay.example.co.jp">
      </div>
      <div style="width:120px">
        <label class="field">ポート</label>
        <input type="number" id="port" min="1" max="65535" placeholder="25">
      </div>
      <div style="width:140px">
        <label class="field">タイムアウト（秒）</label>
        <input type="number" id="timeout" min="1" max="300" placeholder="20">
      </div>
    </div>
    <div id="serverInfo"></div>
  </div>

  <div class="card">
    <div class="card__title">差出人</div>
    <div class="card__desc">
      メールの From になるアドレスです。複数を登録しておき、使うものを1つ選びます。
      SMTPサーバによっては、認証したアカウント以外のアドレスでは送信を拒否されます。
    </div>
    <div class="row mb">
      <div style="width:280px">
        <label class="field">使用する差出人</label>
        <select id="sender"></select>
      </div>
      <div style="width:280px">
        <label class="field">差出人の表示名</label>
        <input type="text" id="senderName" placeholder="例: 営業企画部 BIレポート">
      </div>
    </div>
    <label class="field">差出人アドレスの候補</label>
    <div id="senderList"></div>
    <div class="row mt">
      <input type="text" id="newSender" class="grow" style="max-width:360px"
             placeholder="例: bi-report@example.co.jp">
      <button class="btn btn--sm" id="addSender">＋ 追加</button>
    </div>
  </div>

  <div class="card">
    <div class="card__title">送信できる宛先</div>
    <div class="card__desc">
      ここに登録したアドレスにだけ送れます。<b>1件も登録していないあいだは、どこにも送れません。</b>
      登録できるドメインは、下の「登録してよいドメイン」で決まります。
    </div>
    <div id="allowState"></div>

    <div class="mt" style="max-width:520px">
      <label class="field">登録してよいドメイン</label>
      <input type="text" id="okDomains"
             placeholder="例: @example.co.jp（複数は ; 区切り。空欄なら制限なし）">
      <div class="small muted mt">
        宛先・通知先に登録できるアドレスを、このドメイン（サブドメイン含む）に限定します。
      </div>
    </div>

    <div class="mt" style="max-width:520px">
      <label class="field">送信を許可するアドレス</label>
      <div id="addrList"></div>
      <div class="row mt">
        <input type="text" id="newAddr" class="grow" placeholder="例: tanaka@example.co.jp">
        <button class="btn btn--sm" id="addAddr">追加</button>
      </div>
      <div class="small muted mt" id="domainNote"></div>
    </div>
  </div>

  <div class="card">
    <div class="card__title">取り込みの警告を知らせる先（管理者）</div>
    <div class="card__desc">
      取り込みが<b>設定どおりにできなくなったとき</b>（取り込み元のファイルが無い・
      シート名や列が変わった・自動実行が止まっている等）に、ここへメールで知らせます。<br>
      送るのは状態が変わった瞬間の1回だけです（失敗が続く間は繰り返しません）。直ったら「復旧」を1回送ります。
      登録できるドメインは宛先と同じ縛りです。空のままなら通知しません。
    </div>

    <div class="mt">
      <label class="row" style="align-items:center;gap:8px;cursor:pointer">
        <input type="checkbox" id="alertEnabled">
        <b>警告をメールで知らせる</b>
      </label>
      <div class="small muted" style="margin-left:26px">
        外すと、通知先を消さずに通知だけ止められます（棚卸しや長期メンテのあいだなど）。
        止めているあいだも、画面の⚠とAIへの注記はこれまでどおり出ます。
      </div>
    </div>

    <div class="mt" id="alertKindsWrap">
      <label class="field">知らせる警告の種類</label>
      <div id="alertKinds"></div>
      <div class="small muted mt">
        緊急度が違うので、種類ごとに選べます。
        「取り込みが失敗した」は前回の内容のまま止まっている状態なので、通常は入れておいてください。
      </div>
    </div>

    <div class="mt" style="max-width:520px">
      <label class="field">通知先のアドレス</label>
      <div id="alertList"></div>
      <div class="row mt">
        <input type="text" id="newAlert" class="grow" placeholder="例: admin@example.co.jp">
        <button class="btn btn--sm" id="addAlert">追加</button>
      </div>
    </div>
  </div>

  <div class="card">
    <div class="card__title">送信のしかた</div>
    <div class="row mb">
      <div style="width:240px">
        <label class="field">一度に送れる宛先の数</label>
        <input type="number" id="maxRecipients" min="1" max="500">
      </div>
      <div class="grow">
        <label class="field">動作</label>
        <label class="check">
          <input type="checkbox" id="dryRun">
          <span>テスト送信モード（実際には送らず、内容の確認だけ）</span>
        </label>
      </div>
    </div>
    <div id="dryNote"></div>
  </div>

  <div class="row mb">
    <button class="btn btn--primary" id="save">設定を保存</button>
    <button class="btn" id="test">送信サーバへの接続を確認</button>
    <div class="spacer"></div>
    <button class="btn btn--ghost btn--sm" id="reload">読み直す</button>
  </div>

  <details class="acc">
    <summary>送信の記録<span class="badge" id="logCount">0</span></summary>
    <div class="acc__body" id="logList"></div>
  </details>
</div>
{% endblock %}

{% block scripts %}
<script>
window.MAIL = {{ status|tojson }};
window.MAIL_LOG = {{ log|tojson }};
window.IS_ADMIN = {{ user.is_admin|tojson }};
</script>
{% endblock %}
""",

# --- models.html ---
"models.html": r"""{% extends "base.html" %}
{% block title %}モデル設定 — {{ app_title }}{% endblock %}
{# 見出しは置かない。画面の説明はサイドバーの項目にマウスを乗せると出る #}

{% block body %}
<div class="content">
  <div id="banner"></div>

  <details class="card" id="howto">
    <summary class="card__title" style="cursor:pointer">この画面の使い方</summary>
    <div class="card__desc" style="margin-top:8px">
      APIが返すモデルは100件を超えることもあり、その中には旧世代のものや
      チャットに使えないものが混ざっています。そのまま利用者に見せると選び間違えるので、
      <b>ここで「使ってよいモデル」を決めます</b>。
      <ol style="margin:8px 0 0 18px;padding:0;line-height:1.9">
        <li>「一覧から選ぶ」で、使わせたいモデルにチェックを入れる</li>
        <li>「既定のモデル」で、まだ自分で選んでいない利用者が使うものを決める</li>
        <li>下の「設定を保存」を押す</li>
      </ol>
      <div class="mt">
        保存すると、チャット画面のプルダウンは<b>ここで選んだモデルだけ</b>になります。
        候補から外したモデルを選んでいた利用者は、次の質問から既定のモデルに変わります。
      </div>
    </div>
  </details>

  <div class="card">
    <div class="card__title">選択できるモデル</div>
    <div class="card__desc">
      ここに登録したモデルだけが、チャット画面のプルダウンに出ます。
      候補から外すと、既にそのモデルを選んでいた利用者も既定のモデルに戻ります。
    </div>
    <div id="modelList"></div>
    <div class="row mt">
      <button class="btn btn--sm btn--primary" id="pickModel">一覧から選ぶ</button>
      <input type="text" id="newModel" class="grow" style="max-width:300px"
             placeholder="一覧に無い名前を直接入力" list="catalogList">
      <datalist id="catalogList"></datalist>
      <button class="btn btn--sm" id="addModel">＋ 追加</button>
      <div class="spacer"></div>
      <button class="btn btn--ghost btn--sm" id="refresh"
              title="APIに問い合わせて、使えるモデルの一覧を取り直します">一覧を取得</button>
    </div>
    <div id="catalogHint" class="small muted mt"></div>
  </div>

  <div class="card">
    <div class="card__title">既定のモデル</div>
    <div class="card__desc">
      まだ自分で選んでいない利用者が使うモデルです。上の候補から選びます。
    </div>
    <div style="max-width:320px">
      <select id="defaultModel"></select>
    </div>
  </div>

  <div class="card">
    <div class="card__title">接続先URL</div>
    <div class="card__desc">
      AIサービス（OpenAI互換API）のエンドポイントを、用途ごとに<b>フルパス</b>で指定します。
      ここで保存したURLが <code>env</code>（OPENAI_BASE_URL）より優先され、
      保存すると次の呼び出しから反映されます（再起動不要）。
      <b>空欄にして保存すると env の値に戻ります。</b>
    </div>
    <div class="mb" style="max-width:640px">
      <label class="field">チャット（AI呼び出し）のURL</label>
      <input type="text" id="chatUrl" placeholder="例: https://api.openai.com/v1/chat/completions">
      <div class="small muted mt" id="chatUrlNote"></div>
    </div>
    <div style="max-width:640px">
      <label class="field">モデル一覧の取得URL（この画面の「一覧を取得」が使います）</label>
      <input type="text" id="modelsUrl" placeholder="例: https://api.openai.com/v1/models">
      <div class="small muted mt" id="modelsUrlNote"></div>
    </div>
  </div>

  <div class="card">
    <div class="card__title">APIキー</div>
    <div class="card__desc">
      AIサービス（OpenAI互換API）への接続に使うキーです。ここで保存したキーが
      <code>env</code> のキーより優先されます。<b>保存済みのキーは画面に表示されません</b>
      （変更するときだけ入力します）。
    </div>
    <div id="apiKeyState" class="mb"></div>
    <div class="row" style="gap:8px;max-width:560px">
      <input type="password" id="apiKeyInput" class="grow" autocomplete="new-password"
             placeholder="変更する場合だけ入力し、「設定を保存」で反映">
      <button class="btn btn--sm" id="apiKeyClear"
              title="画面で保存したキーを消して、env のキーに戻します">envのキーに戻す</button>
    </div>
    <div class="small muted mt">
      保存すると次のAI呼び出しから新しいキーが使われます（再起動不要）。
    </div>
  </div>

  <div class="card">
    <div class="card__title">画像を扱えるモデルの判定</div>
    <div class="card__desc">
      モデル名にこの文字列が含まれていれば「画像を送れる」と判断します
      （部分一致・大文字小文字は区別しません）。
      判定を誤ると、画像を送れないモデルに画像を渡して失敗します。
    </div>
    <div id="visionList"></div>
    <div class="row mt">
      <input type="text" id="newVision" class="grow" style="max-width:280px"
             placeholder="例: gpt-4o">
      <button class="btn btn--sm" id="addVision">＋ 追加</button>
    </div>
    <div id="visionPreview" class="mt"></div>
  </div>

  <div class="card">
    <div class="card__title">モデルが一度に読める量と、AIに渡すカタログの上限</div>
    <div class="card__desc">
      カタログ（テーブル・列の説明、コード値、サンプル行）をどこまで<b>そのまま</b>AIに渡すかは、
      <b>選ばれたモデルの文脈量から自動で決まります</b>（文脈の半分をカタログに、残りを
      会話の履歴と回答に使う配分）。設定する上限はありません。<br>
      カタログ全体が上限に収まらないモデルでは、質問ごとに関係するデータだけへ自動で絞ります
      （列名は失われません）。<br>
      文脈量は OpenAI 公式リファレンスの値を持っています。<b>「推定」と出ているモデル</b>は
      表に無いので、下の欄で正しいトークン数を登録してください（ゲートウェイ独自の名前や
      他社モデルなど）。
    </div>
    <div id="ctxTable" class="mt"></div>
    <div class="row mt" style="align-items:flex-end;gap:8px">
      <div style="width:260px">
        <label class="field">文脈量を登録するモデル名</label>
        <input type="text" id="ctxName" placeholder="例: my-gateway-model">
      </div>
      <div style="width:160px">
        <label class="field">文脈量（トークン）</label>
        <input type="number" id="ctxTokens" step="1000" placeholder="例: 128000">
      </div>
      <button class="btn btn--sm" id="ctxAdd">登録</button>
    </div>
    <div class="small muted mt">
      名前は部分一致です（<code>my-gateway</code> と登録すれば <code>my-gateway-model-v2</code> にも効きます）。
      「設定を保存」で確定します。
    </div>
  </div>

  <div class="row mb">
    <button class="btn btn--primary" id="save">設定を保存</button>
    <div class="spacer"></div>
    <button class="btn btn--ghost btn--sm" id="reload">読み直す</button>
  </div>
</div>
{% endblock %}

{% block scripts %}
<script>window.MODELS = {{ status|tojson }};</script>
{% endblock %}
""",

# --- table.html ---
"table.html": r"""{% extends "base.html" %}
{% block title %}{{ table }} — {{ app_title }}{% endblock %}
{# 別タブで開く読み取り専用のビューア。表そのものに場所を使いたいので、
   見出しは小さく持ち、画面の幅と高さをいっぱいに使う（CSSの .is-table 参照）。 #}
{% block body_class %}is-table{% endblock %}

{% block sidebar %}
<div class="sidebar__section">
  <div class="sidebar__label">開いているテーブル</div>
  <div style="font-weight:600">{{ table }}</div>
  {% if db_title %}<div class="small muted">{{ db_title }}</div>{% endif %}
  {% if description %}<div class="small mt">{{ description }}</div>{% endif %}
  <a class="btn btn--sm mt" style="width:100%"
     href="{{ url_for('catalog.index') }}?db={{ db_file|urlencode }}#tables">カタログで開く</a>
</div>
{% endblock %}

{% block body %}
<div class="content">
  {% if error %}
    <div class="alert alert--err">{{ error }}</div>
  {% else %}
  <div class="card">
    <div class="row" style="align-items:center;gap:10px;flex-wrap:wrap">
      <div>
        <div style="font-weight:650;font-size:16px">{{ table }}</div>
        <div class="small muted" id="countLabel">読み込み中…</div>
      </div>
      <div class="spacer"></div>
      <input type="text" id="q" placeholder="値で絞り込み（全列を対象）" style="width:260px">
      <select id="size" style="width:auto" title="1ページの行数">
        {% for n in page_sizes %}<option value="{{ n }}" {{ 'selected' if n == 100 }}>{{ n }}行</option>{% endfor %}
      </select>
    </div>

    {# いま効いている絞り込み。1つずつ外せる（中身は table.js が描く） #}
    <div class="chips mt hidden" id="chips"></div>

    <div class="tablewrap mt" id="tableBox">
      <div class="small muted" style="padding:10px"><span class="spinner"></span> 読み込み中…</div>
    </div>

    <div class="row mt" style="align-items:center;gap:8px">
      <button class="btn btn--sm" id="first" title="最初のページ">≪ 先頭</button>
      <button class="btn btn--sm" id="prev">前へ</button>
      <span class="small muted" id="pageLabel">—</span>
      <button class="btn btn--sm" id="next">次へ</button>
      <button class="btn btn--sm" id="last" title="最後のページ">末尾 ≫</button>
      <div class="spacer"></div>
      <span class="small muted">列名をクリックすると並べ替え</span>
    </div>
  </div>
  {% endif %}
</div>
{% endblock %}

{% block scripts %}
<script>
window.TABLE_INIT = {
  db: {{ db_file|tojson }},
  table: {{ table|tojson }},
  error: {{ (error or '')|tojson }}
};
</script>
{% endblock %}
""",

# --- usage.html ---
"usage.html": r"""{% extends "base.html" %}
{% block title %}利用状況 — {{ app_title }}{% endblock %}
{# 見出しは置かない。画面の説明はサイドバーの項目にマウスを乗せると出る #}

{% block body %}
<div class="content content--wide">

  {# 条件は1本の帯にまとめる。タブを切り替えても条件はそのまま持ち回る #}
  <div class="tabs tabs--bar">
    {% for v in views if not v.merged %}
    <button class="tab {{ 'is-active' if loop.first }}" data-view="{{ v.key }}">{{ v.label }}</button>
    {% endfor %}
    <button class="tab" data-view="chats">質問・履歴</button>

    <div class="tabs__end">
      <div class="row" style="align-items:center;gap:8px">
        <select id="uRange" title="集計する期間">
          {% for r in ranges %}
          <option value="{{ r.days }}" {{ 'selected' if r.days == 30 }}>{{ r.label }}</option>
          {% endfor %}
        </select>
        <select id="uUser" title="利用者で絞る">
          <option value="">全員</option>
          {% for u in users %}<option value="{{ u }}">{{ u }}</option>{% endfor %}
        </select>
        <button class="btn btn--sm btn--primary" id="uExport"
                title="いまの条件のまま、集計をExcelにします">Excel出力</button>
      </div>
    </div>
  </div>

  {# 集計タブ（全体像・利用者・推移…）。中身は app.js が描く #}
  <div class="tabpane is-active" id="pane-report">
    <div id="uNotes"></div>
    <div id="uBody"></div>
  </div>

  {# チャット履歴。左に一覧、右に中身 #}
  <div class="tabpane" id="pane-chats">
    <div id="uQNotes"></div>
    <div class="row mb" style="align-items:center">
      <input type="text" id="uChatFilter" style="max-width:320px"
             placeholder="質問の文言で絞り込み">
      <span class="small muted" id="uChatCount"></span>
      <div class="spacer"></div>
      <span class="small muted">他の利用者の質問がそのまま見えます。取り扱いに注意してください。</span>
    </div>
    {# 1行 = 1つの質問と、その回答。会話の列にはタイトルと会話IDを出す
       （同じ会話IDの行が、同じ会話ルームのやり取り） #}
    <div class="tablewrap"><table class="data qa"><thead><tr>
      <th style="width:130px">日時</th>
      <th style="width:90px">利用者</th>
      <th style="width:210px">会話</th>
      <th style="width:28%">質問</th>
      <th>回答</th>
    </tr></thead><tbody id="uQaBody"></tbody></table></div>
  </div>
</div>
{% endblock %}

{% block scripts %}
<script src="/vendor/plotly.min.js"></script>
<script>
/* この画面のJSを動かすための目印。中身は使っていない（タブや選択肢はサーバ描画） */
window.USAGE = {};
</script>
{% endblock %}
""",

}

STATIC_FILES = {

# --- css/app.css ---
"css/app.css": r"""/* =============================================================================
   DB分析アシスタント — 画面全体のスタイル

   落ち着いた紙のような暖色グレーを基調にする。彩度の高い色は、
   本当に目を向けてほしいところ（エラー・注意・実行中）にだけ使う。
   ライト/ダークはOSの設定に追従。色は変数だけを触れば揃う。
   ========================================================================== */

:root {
    --bg:        #faf9f7;
    --surface:   #ffffff;
    --surface-2: #f3f2ef;
    --border:    #e8e6e1;
    --border-2:  #d9d6cf;
    --text:      #1f1e1d;
    --muted:     #7d7a73;
    --accent:    #b8552f;
    --accent-weak:#f5ece7;
    --ok:        #4a7c59;
    --ok-weak:   #eef3ef;
    --warn:      #9a6b1f;
    --warn-weak: #f8f2e6;
    --err:       #a63d33;
    --err-weak:  #faedeb;
    /* 影はほとんど使わない。境界は線で示す方が静かに見える */
    --shadow:    0 1px 2px rgba(31,30,29,.04);
    --shadow-lg: 0 4px 24px rgba(31,30,29,.10);
    --radius:    10px;
    --radius-sm: 7px;
    --sidebar:   244px;
    --sidebar-bg:#f5f3ef;
    --nav-hover: #e9e6df;
    /* 和文が混ざるので明朝は使わない。欧文と和文で別の書体に割れて揃わないため、
       字面の素直なゴシック1本にして、大きさと太さと字間で階層を作る。 */
    --sans: "Inter", "Segoe UI", "Hiragino Sans", "Yu Gothic UI", "Noto Sans JP",
            system-ui, sans-serif;
    --mono: ui-monospace, "SFMono-Regular", Menlo, Consolas, "Noto Sans Mono", monospace;
}

@media (prefers-color-scheme: dark) {
    :root {
        --bg:        #1a1917;
        --surface:   #232220;
        --surface-2: #2b2926;
        --border:    #35332f;
        --border-2:  #45423d;
        --text:      #edeae4;
        --muted:     #a39e94;
        --accent:    #d97757;
        --accent-weak:#3a2620;
        --ok:        #7fa98a;
        --ok-weak:   #232e26;
        --warn:      #c9a05e;
        --warn-weak: #322a1c;
        --err:       #d98376;
        --err-weak:  #38241f;
        --sidebar-bg:#1f1e1c;
        --nav-hover: #322f2b;
        --shadow:    0 1px 2px rgba(0,0,0,.30);
        --shadow-lg: 0 4px 24px rgba(0,0,0,.45);
    }
}

* { box-sizing: border-box; }

body {
    margin: 0;
    background: var(--bg);
    color: var(--text);
    font-family: var(--sans);
    font-size: 14.5px;
    line-height: 1.65;
    letter-spacing: .005em;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; text-underline-offset: 2px; }
code, pre, .mono { font-family: var(--mono); }
code { font-size: .92em; }

::selection { background: var(--accent-weak); }

/* 線画アイコン。絵文字は使わず、太さ1.5の輪郭で統一する */
.icon {
    width: 17px; height: 17px; flex: 0 0 auto;
    stroke: currentColor; stroke-width: 1.6; fill: none;
    stroke-linecap: round; stroke-linejoin: round;
    vertical-align: -3px;
}
.icon--sm { width: 14px; height: 14px; }
.icon--lg { width: 22px; height: 22px; }

/* --- レイアウト ------------------------------------------------------------ */

.layout { display: flex; min-height: 100vh; }

.sidebar {
    width: var(--sidebar);
    flex: 0 0 var(--sidebar);
    background: var(--sidebar-bg);
    border-right: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    position: sticky;
    top: 0;
    height: 100vh;
    overflow-y: auto;
    overflow-x: hidden;
    padding-top: 8px;
}
/* 折りたたみ中。幅を0にするだけで、中身はそのまま残す（開けば元の状態に戻る） */
.is-collapsed .sidebar { padding: 0; border-right-color: transparent; }
.is-collapsed .sidebar > * { visibility: hidden; }

/* --- サイドバーの境目（ドラッグで幅変更・クリックで折りたたみ）--------------------- */

.resizer {
    position: fixed; top: 0; bottom: 0; left: var(--sidebar);
    width: 11px; margin-left: -5px; z-index: 60;
    cursor: col-resize; touch-action: none;
}
/* 掴める線。ふだんは見えず、近づいたときだけ出す */
.resizer::before {
    content: ""; position: absolute; top: 0; bottom: 0; left: 4px;
    width: 3px; border-radius: 2px; background: transparent;
    transition: background .12s;
}
.resizer:hover::before, .resizer:focus-visible::before,
.resizer.is-dragging::before { background: var(--accent); }
.resizer:focus-visible { outline: none; }

/* --- 説明の吹き出し --------------------------------------------------------------
   data-tip を付けた要素にマウスを乗せると出る。少し待ってから出すので、
   通りすがりでは邪魔にならない。見た目はここ1箇所、位置だけ個別に決める。 */

.hastip { position: relative; }

.hastip::after, .resizer::after {
    content: attr(data-tip);
    position: absolute; z-index: 80; pointer-events: none;
    background: var(--text); color: var(--bg);
    padding: 8px 12px; border-radius: var(--radius-sm);
    font-size: 12px; font-weight: 450; line-height: 1.65; letter-spacing: .01em;
    box-shadow: var(--shadow-lg);
    opacity: 0; visibility: hidden;
    transition: opacity .12s .3s, visibility 0s .3s;
}
.hastip:hover::after, .hastip:focus-visible::after,
.resizer:hover::after, .resizer:focus-visible::after { opacity: 1; visibility: visible; }

/* 要素の下・右揃え。長い説明を入れるので折り返しと改行(&#10;)を許す */
.hastip::after {
    top: calc(100% + 8px); right: 0;
    width: max-content; max-width: 330px;
    white-space: pre-line; text-align: left;
}
/* 画面左端に近いボタンは左揃えで出す（右揃えだと左にはみ出す） */
.hastip--l::after { right: auto; left: 0; }
/* サイドバーの境目は横に出す。1行なので折り返さない */
.resizer::after {
    left: 15px; top: 50%; transform: translateY(-50%);
    white-space: nowrap;
}
.resizer.is-dragging::after { opacity: 0; visibility: hidden; transition: none; }
.is-collapsed .resizer::after { content: attr(data-tip-open); }
/* 折りたたみ中は掴む所が分かるように、線を薄く出しておく */
.is-collapsed .resizer::before { background: var(--border-2); }

/* ドラッグ中は文字が選択されないようにする */
body.is-resizing { user-select: none; cursor: col-resize; }
.sidebar__section { padding: 12px; }
.sidebar__section + .sidebar__section { border-top: 1px solid var(--border); }
.sidebar__label {
    font-size: 11px; font-weight: 600; letter-spacing: .08em;
    color: var(--muted); text-transform: uppercase; margin: 2px 4px 8px;
}

/* サイドバーの折りたたみ節。DBもナレッジベースも数が多く、全部開いたままだと
   履歴に届くまで延々スクロールすることになるので、節ごとに畳めるようにする。
   開閉は <details> そのもの（JSなしで動く）。状態は common.js が覚える。 */
details.sbsec > summary {
    display: flex; align-items: center; gap: 6px;
    cursor: pointer; list-style: none;
}
details.sbsec > summary::-webkit-details-marker { display: none; }
details.sbsec > summary .sidebar__label { margin: 0; flex: 1; }
/* ▼は最後。閉じているときは右向きに倒す */
details.sbsec > summary::after {
    content: "▼"; font-size: 9px; color: var(--muted);
    transition: transform .15s ease; flex: none;
}
details.sbsec:not([open]) > summary::after { transform: rotate(-90deg); }
details.sbsec > summary:hover::after,
details.sbsec > summary:hover .sidebar__label { color: var(--fg); }
details.sbsec > summary:focus-visible {
    outline: 2px solid var(--accent); outline-offset: 2px; border-radius: var(--radius-sm);
}
/* 節の中身は、見出しとの間だけ空ける */
details.sbsec > .sbsec__body { margin-top: 8px; }
/* 見出しに置くボタン（＋新規・全選択）。畳んでいても押せる */
details.sbsec > summary .sbsec__act { flex: none; }
.sidebar__user {
    display: flex; align-items: center; gap: 7px; font-weight: 500;
}
.navlink {
    display: flex; align-items: center; gap: 10px;
    padding: 7px 9px; border-radius: 8px; font-size: 13.5px;
    color: var(--text); font-weight: 450; margin-bottom: 1px;
    transition: background .12s, color .12s;
}
.navlink .icon { color: var(--muted); }
.navlink:hover { background: var(--nav-hover); text-decoration: none; }
.navlink.is-active { background: var(--nav-hover); font-weight: 550; }
.navlink.is-active .icon { color: var(--accent); }

/* ふつうの画面は中身の高さだけ伸びて、ページ全体がスクロールする。
   チャットだけは画面に固定して、ログの中だけをスクロールさせたいので
   body に .is-chat を付けて切り替える（下の .is-chat .main を参照）。 */
.main { flex: 1; min-width: 0; display: flex; flex-direction: column; }
/* flexの既定で縮められると中身がはみ出して読めなくなるので、縮小を止める */
.content { flex: none; }

.is-chat .main { height: 100vh; overflow: hidden; }

/* 表だけを見る画面（テーブル全体のビューア）。読むのは中身だけなので、
   幅の上限を外し、高さも画面いっぱいに使う。ページ自体はスクロールさせず、
   表の中だけを縦横にスクロールさせる（見出し行と操作列を画面に残すため）。 */
.is-table .main { height: 100vh; overflow: hidden; }
.is-table .content {
    max-width: none; padding: 12px 14px; height: 100%;
    display: flex; flex-direction: column; min-height: 0;
}
.is-table .card {
    flex: 1; min-height: 0; display: flex; flex-direction: column; margin: 0;
}
.is-table .tablewrap { flex: 1; min-height: 0; max-height: none; }
/* 行が縦に詰まっている方が一度に読める。ビューアだけ少し詰める */
.is-table table.data th, .is-table table.data td { padding: 5px 10px; }
/* 行番号の列は横スクロールしても残す。列の多い表で「いま何行目か」を見失わないため */
.is-table table.data th:first-child,
.is-table table.data td:first-child {
    position: sticky; left: 0; z-index: 2; background: var(--surface);
    border-right: 1px solid var(--border);
}
.is-table table.data thead th:first-child { z-index: 3; background: var(--surface-2); }
.is-table table.data tbody tr:hover td:first-child { background: var(--surface-2); }
/* 見出しも操作部も無い画面では、そもそも header ごと出していない（base.html）。
   以前ここでチャットだけ display:none にしていたが、同じことをする画面が
   増えたのでテンプレート側にまとめた。 */
.topbar {
    display: flex; align-items: center; justify-content: space-between;
    gap: 10px 16px; flex-wrap: wrap;
    padding: 20px 32px 16px; background: var(--bg);
    border-bottom: 1px solid var(--border); position: sticky; top: 0; z-index: 20;
}
/* 右側（操作部）は縮めない。既定では左右が同じ割合で縮むので、
   場所が足りているのに操作部だけが折り返して見出しが2段になる。
   見出しのほうを縮ませて、説明文を折り返させる。 */
/* 操作部は縮めない。縮ませると、場所が足りているのに中で折り返したり、
   見出しの文字が削られたりする。狭いときは topbar ごと2段に折り返す。
   見出しが無い画面では操作部が唯一の子になり、space-between で左に寄る。 */
.topbar > div:last-child { flex: 0 0 auto; }
.topbar h1 {
    margin: 0; font-size: 19px; font-weight: 600; letter-spacing: -.015em;
    white-space: nowrap;
}
.topbar .sub { color: var(--muted); font-size: 13px; margin-top: 2px; }
.content { padding: 24px 28px 72px; max-width: 1400px; width: 100%; }
.content--wide { max-width: none; }

/* --- 部品 ------------------------------------------------------------------ */

.card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 20px; margin-bottom: 18px;
}
.card__title {
    font-weight: 600; font-size: 14.5px; margin: 0 0 6px; letter-spacing: -.005em;
}
.card__desc { color: var(--muted); font-size: 13px; margin: 0 0 14px; }
.row { display: flex; gap: 12px; flex-wrap: wrap; align-items: flex-end; }
.row > * { min-width: 0; }
.grow { flex: 1; }
.spacer { flex: 1; }
.muted { color: var(--muted); }
.small { font-size: 12.5px; }
.mt { margin-top: 12px; }
.mb { margin-bottom: 12px; }
.hidden { display: none !important; }

.btn {
    display: inline-flex; align-items: center; justify-content: center; gap: 7px;
    padding: 7px 14px; border-radius: var(--radius-sm);
    border: 1px solid var(--border-2); background: var(--surface); color: var(--text);
    font: inherit; font-weight: 500; font-size: 13.5px; cursor: pointer;
    white-space: nowrap; transition: background .12s, border-color .12s;
}
.btn:hover { background: var(--surface-2); border-color: var(--muted); }
.btn:disabled { opacity: .45; cursor: not-allowed; }
.btn--primary { background: var(--accent); border-color: var(--accent); color: #fff; }
.btn--primary:hover { background: var(--accent); border-color: var(--accent); filter: brightness(1.08); }
.btn--danger { color: var(--err); border-color: var(--border-2); }
.btn--danger:hover { background: var(--err-weak); border-color: var(--err); }
.btn--sm { padding: 4px 10px; font-size: 12.5px; }
.btn--ghost { border-color: transparent; background: transparent; color: var(--muted); }
.btn--ghost:hover { background: var(--surface-2); color: var(--text); }
/* アイコンだけのボタン（ER図の保存・元に戻す・やり直す など） */
.btn--icon { padding: 4px 7px; }
.btn--icon .icon { width: 16px; height: 16px; }

label.field { display: block; font-size: 13px; font-weight: 500; margin-bottom: 6px;
              color: var(--muted); }
input[type=text], input[type=password], input[type=number], select, textarea {
    width: 100%; padding: 8px 11px; font: inherit; font-size: 13.5px;
    color: var(--text); background: var(--surface);
    border: 1px solid var(--border-2); border-radius: var(--radius-sm);
    transition: border-color .12s, box-shadow .12s;
}
input:focus, select:focus, textarea:focus {
    outline: none; border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-weak);
}
textarea { resize: vertical; min-height: 68px; }
input[type=checkbox] { accent-color: var(--accent); width: 15px; height: 15px; }

.badge {
    display: inline-block; padding: 1px 8px; border-radius: 999px;
    font-size: 11.5px; font-weight: 500; background: var(--surface-2); color: var(--muted);
}
.badge--ok { background: var(--ok-weak); color: var(--ok); }
.badge--warn { background: var(--warn-weak); color: var(--warn); }
.badge--err { background: var(--err-weak); color: var(--err); }
.badge--accent { background: var(--accent-weak); color: var(--accent); }

/* 帯で塗らず、左の縦線だけで色を示す。並んでも画面が騒がしくならない */
.alert {
    padding: 10px 14px; border-radius: var(--radius-sm); font-size: 13.5px;
    background: var(--surface-2); color: var(--text);
    border: 1px solid var(--border); border-left: 3px solid var(--border-2);
    margin-bottom: 12px;
}
.alert--ok { background: var(--ok-weak); border-color: var(--border); border-left-color: var(--ok); }
.alert--warn { background: var(--warn-weak); border-color: var(--border); border-left-color: var(--warn); }
.alert--err { background: var(--err-weak); border-color: var(--border); border-left-color: var(--err); }
.alert--info { background: var(--surface-2); border-color: var(--border); border-left-color: var(--muted); }

.metrics { display: flex; gap: 10px; flex-wrap: wrap; }
.metric {
    background: var(--surface-2); border-radius: var(--radius-sm);
    padding: 10px 15px; min-width: 92px;
}
.metric__label { font-size: 12px; color: var(--muted); font-weight: 450; }
.metric__value { font-size: 21px; font-weight: 500; line-height: 1.25;
                 font-variant-numeric: tabular-nums; }
/* クリックでそのタブへ飛べる充実度（カタログ画面） */
.metric--link {
    font: inherit; text-align: left; cursor: pointer; color: var(--text);
    border: 1px solid transparent;
    transition: border-color .12s, background .12s;
}
.metric--link:hover { border-color: var(--border-2); background: var(--surface); }

.metrics--inline { gap: 6px; }
.metrics--inline .metric { padding: 5px 10px; min-width: 66px; }
.metrics--inline .metric__label { font-size: 10.5px; }
.metrics--inline .metric__value { font-size: 15px; line-height: 1.2; }

/* ユーザー定義ツールのパラメータ。1行1つで、名前・型・説明・必須を並べる。
   以前は「名前:型*:説明」というテキスト1行に書かせていて、書き方を知らないと
   何も作れなかった。 */
.prow { display: flex; align-items: center; gap: 6px; margin-bottom: 5px; }
.prow .p-name { width: 150px; }
.prow .p-type { width: 110px; }

/* 絞り込みで当たった列の行 */
table.data tr.is-hit > td { background: var(--accent-weak); }

/* --- 用語集・例文（カタログ画面） -----------------------------------------------
   左が見渡すための一覧、右がいま選んだ1件のエディタ。
   一覧はページと一緒に流れ、エディタは追いかけてくる。 */

.md { display: flex; gap: 16px; align-items: flex-start; }
.md__side { flex: 0 0 300px; min-width: 0; }
.md__main { flex: 1; min-width: 340px; position: sticky; top: 72px;
            max-height: calc(100vh - 96px); overflow-y: auto; }
@media (max-width: 1100px) {
    .md { flex-wrap: wrap; }
    .md__side { flex: 1 1 100%; }
    .md__main { position: static; max-height: none; }
}

/* 用語集⇄例文の切り替え。上のタブと紛れないよう、丸い錠剤型にする */
.seg { display: inline-flex; padding: 3px; gap: 2px; background: var(--surface);
       border: 1px solid var(--border-2); border-radius: 999px; }
.seg__btn { border: none; background: none; font: inherit; font-size: 13px;
            font-weight: 550; color: var(--muted); padding: 5px 14px;
            border-radius: 999px; cursor: pointer;
            transition: background .12s, color .12s; }
.seg__btn:hover { color: var(--text); }
.seg__btn.is-active { background: var(--accent-weak); color: var(--accent); }
.seg__count { font-weight: 400; opacity: .8; }

.mlist { margin-top: 8px; }
.mlist__group { font-size: 11px; font-weight: 600; letter-spacing: .05em;
                color: var(--muted); margin: 12px 4px 4px; }
.mlist__item { display: flex; align-items: center; gap: 8px; width: 100%;
               text-align: left; padding: 6px 9px; border: none;
               border-radius: var(--radius-sm); background: none; font: inherit;
               font-size: 13px; color: var(--text); cursor: pointer; }
.mlist__item:hover { background: var(--surface-2); }
.mlist__item.is-active { background: var(--accent-weak); color: var(--accent); }
.mlist__term { flex: 0 1 auto; min-width: 44px; font-weight: 550;
               overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.mlist__desc { flex: 1 1 0; min-width: 0; color: var(--muted); font-size: 12px;
               overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.mlist__item.is-active .mlist__desc { color: inherit; opacity: .75; }
/* 例文の一覧は質問が主役。説明があれば右に添える（質問側を広く取る） */
.mlist__q { flex: 2 1 0; min-width: 0; overflow: hidden;
            text-overflow: ellipsis; white-space: nowrap; }
.mlist__empty { padding: 10px 6px; color: var(--muted); font-size: 12.5px; }

/* 一覧の行頭の点 = 検証結果（無色の輪 = 未検証）。行末の点 = 未保存 */
.dot { flex: none; width: 8px; height: 8px; border-radius: 50%;
       border: 1.5px solid var(--border-2); background: transparent; }
.dot--ok { background: var(--ok); border-color: var(--ok); }
.dot--warn { background: var(--warn); border-color: var(--warn); }
.dot--err { background: var(--err); border-color: var(--err); }
.dot--dirty { width: 7px; height: 7px; background: var(--accent); border-color: var(--accent); }

.editcard { border: 1px solid var(--border); border-radius: var(--radius);
            background: var(--surface); padding: 16px; }
.editcard--empty { border-style: dashed; display: grid; place-items: center;
                   min-height: 180px; text-align: center; }
.editcard textarea { resize: none; overflow: hidden; min-height: 34px; }
.ed-dup { color: var(--err); margin-top: 6px; }

/* 検証結果。空のときは場所を取らない */
.vstatus:empty { display: none; }
.vstatus:not(:empty) {
    margin-top: 8px; display: flex; align-items: baseline; gap: 8px;
}

/* エディタ下の参照。列名クリックでSQLに挿し込める */
.refbox { margin-top: 14px; padding-top: 12px; border-top: 1px dashed var(--border-2); }
.refbox .tablewrap { max-height: 240px; }
.reflink { border: none; background: none; padding: 0; cursor: pointer;
           font-family: var(--mono); font-size: 12px; color: var(--accent); }
.reflink:hover { text-decoration: underline; }

/* 未保存の変更をまとめて保存するバー（カタログ画面） */
.savebar {
    position: fixed; right: 28px; bottom: 24px; z-index: 90;
    display: flex; align-items: center; gap: 12px;
    padding: 9px 12px 9px 16px; border-radius: 999px;
    background: var(--surface); border: 1px solid var(--border-2);
    box-shadow: var(--shadow-lg);
}

/* --- 表 -------------------------------------------------------------------- */

.tablewrap { overflow: auto; max-height: 460px; border: 1px solid var(--border); border-radius: var(--radius-sm); }
table.data { border-collapse: separate; border-spacing: 0; width: 100%; font-size: 12.5px; }
table.data th, table.data td {
    padding: 6px 10px; text-align: left;
    /* 列の間にも線を引く。数字が並ぶ表では、横線だけだと目が隣の列へ滑る */
    border-bottom: 1px solid var(--border); border-right: 1px solid var(--border);
    white-space: nowrap; max-width: 380px; overflow: hidden; text-overflow: ellipsis;
}
table.data th:last-child, table.data td:last-child { border-right: none; }
table.data thead th {
    position: sticky; top: 0; z-index: 1; background: var(--surface-2);
    font-weight: 550; color: var(--muted); border-bottom: 1px solid var(--border-2);
}
table.data tbody tr:hover { background: var(--surface-2); }
table.data td.num { text-align: right; font-variant-numeric: tabular-nums; }

/* ヘルプは同じ table.data に長い説明文を入れる。データ格子用の
   「1行に収めて溢れたら … で切る」が効くと、どのセルも1行目の途中で
   切れて読めなくなるので、ここだけ折り返す側に戻す。 */
.help table.data th, .help table.data td {
    white-space: normal; max-width: none; overflow: visible;
    text-overflow: clip; vertical-align: top; line-height: 1.75;
    /* 関数名のような長い英字1語も折り返す。これが無いと、その1語の幅より
       列を狭くできず、表が画面からはみ出す */
    overflow-wrap: anywhere;
}
/* セルの中のコード例。列の幅を決めるときは幅0として数えさせ（width:0）、
   実際にはセル幅いっぱいに置く（min-width:100%）。
   横に長いコードは <pre> の中だけで横スクロールする */
.help table.data td pre { width: 0; min-width: 100%; }
/* 見出し（thead）は上に貼り付かなくてよい。文章の途中で浮くと読みにくい */
.help table.data thead th { position: static; }
/* ヘルプでは表そのものが本文。高さ460pxの窓に閉じ込めると、
   中をもう一度スクロールしないと続きが読めず、読み飛ばしが起きる。
   縦の制限だけ外す（横に長いときのスクロールは残す） */
.help .tablewrap { max-height: none; }
/* 説明の中に入るコード。横に長いものはその場で横スクロールさせる
   （ページ全体が横に伸びると本文が読めなくなる） */
.help pre {
    margin: 6px 0; padding: 9px 11px; overflow-x: auto;
    background: var(--surface-2); border: 1px solid var(--border);
    border-radius: var(--radius-sm); font-size: 12px; line-height: 1.6;
}

/* --- タブ ------------------------------------------------------------------ */

.tabs { display: flex; gap: 2px; border-bottom: 1px solid var(--border); margin-bottom: 16px; }
.tab {
    padding: 8px 14px; border: none; background: none; color: var(--muted);
    font: inherit; font-weight: 600; font-size: 13.5px; cursor: pointer;
    border-bottom: 2px solid transparent; margin-bottom: -1px;
}
.tab:hover { color: var(--text); }
.tab.is-active { color: var(--text); border-bottom-color: var(--accent); }
/* 定期取り込みが設定どおりに動いていないDB・テーブルに付ける印（チャットのサイドバー） */
.warnmark { color: var(--warn, #c77700); display: inline-flex; align-items: center; margin-left: 4px; }
.warnmark .icon { width: 14px; height: 14px; }

/* 別画面へ渡すタブ（データカタログ⇄取り込み）はリンクだが、見た目はボタンのタブと揃える */
a.tab { text-decoration: none; display: inline-block; line-height: normal; }

/* タブと一緒に、右端へ充実度やDB選択を載せる帯（データカタログ）。
   別々の段にすると、それだけで縦を60px以上使ってしまう。
   タブは伸びた高さいっぱいに広がるので、下線は帯の境界線の位置に来る。 */
.tabs--bar { align-items: stretch; flex-wrap: wrap; row-gap: 4px; }
.tabs--bar .tab { display: flex; align-items: center; }
.tabs__end {
    margin-left: auto; align-self: center;
    display: flex; align-items: center; gap: 8px; flex-wrap: wrap;
    justify-content: flex-end; padding: 4px 0 6px;
}
.tabpane { display: none; }
.tabpane.is-active { display: block; }

details.acc { border: 1px solid var(--border); border-radius: var(--radius-sm); margin-bottom: 10px; background: var(--surface); }
details.acc > summary {
    padding: 9px 13px; cursor: pointer; font-weight: 600; font-size: 13px;
    list-style: none; display: flex; align-items: center; gap: 8px;
}
details.acc > summary::-webkit-details-marker { display: none; }
details.acc > summary::before { content: "▸"; color: var(--muted); }
details.acc[open] > summary::before { content: "▾"; }
details.acc > .acc__body { padding: 0 13px 13px; }
/* 行の右端に置く削除。ふだんは目立たせず、その行に近づいたときだけ出す。
   常に赤いボタンが並ぶと、一覧が「消す画面」に見えてしまうため。 */
details.acc > summary .t-drop {
    flex: none; opacity: 0; color: var(--muted);
    border-color: transparent; background: none;
    transition: opacity .12s, color .12s;
}
details.acc > summary:hover .t-drop,
details.acc > summary .t-drop:focus-visible { opacity: 1; }
details.acc > summary .t-drop:hover { color: var(--err); opacity: 1; }
/* テーブル一覧の元DBグループ（表名「元DB名__表名」の規約があるときの折りたたみ）。
   個々のテーブルと見分けがつくよう、見出しをひと回り強くして地の色を変える */
details.acc--group { background: var(--surface-2); }
details.acc--group > summary { font-size: 14px; padding: 11px 13px; }
details.acc--group > .acc__body { padding: 0 10px 10px; }
details.acc--group > .acc__body > details.acc { background: var(--surface); }

/* チャットから飛んできたテーブル。どれを開いたのかが一目で分かるように光らせる */
details.acc.is-target {
    border-color: var(--accent);
    box-shadow: 0 0 0 3px var(--accent-weak);
    transition: box-shadow .4s, border-color .4s;
}

/* --- チャット --------------------------------------------------------------- */

/* 上のヘッダを除いた残り全部。ヘッダの高さが変わってもここは追従する */
.chat { display: flex; flex-direction: column; flex: 1; min-height: 0;
        position: relative; }
/* 上を読んでいるあいだ出る「最新へ」。入力欄のすぐ上に小さく浮かせる。
   読んでいる内容を隠さないよう、丸ボタン1つぶんに留める。 */
.jumpdown {
    position: absolute; left: 50%; bottom: 100%; z-index: 5;
    margin-bottom: 12px; cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    width: 32px; height: 32px; padding: 0; border-radius: 999px;
    border: 1px solid var(--border-2); background: var(--surface);
    color: var(--muted); box-shadow: var(--shadow-lg);
    transform: translate(-50%, 6px);
    opacity: 0; visibility: hidden;
    transition: opacity .15s, transform .15s, visibility 0s .15s,
                color .12s, border-color .12s;
}
.jumpdown.is-on {
    opacity: 1; visibility: visible; transform: translate(-50%, 0);
    transition: opacity .15s, transform .15s, visibility 0s, color .12s, border-color .12s;
}
.jumpdown:hover { color: var(--accent); border-color: var(--accent); }
.jumpdown .icon { width: 18px; height: 18px; stroke-width: 2; vertical-align: 0; }
.chat__log { flex: 1; overflow-y: auto; padding: 20px 24px 8px; }
.chat__inner { max-width: 980px; margin: 0 auto; }
.chat__composer {
    border-top: 1px solid var(--border); background: var(--surface); padding: 12px 24px 16px;
    position: relative;          /* 「最新へ」ボタンの位置の基準 */
}
.composer__inner { max-width: 980px; margin: 0 auto; display: flex; gap: 10px; align-items: flex-end; }
.composer__inner textarea {
    min-height: 44px; max-height: 200px; border-radius: var(--radius); padding: 11px 13px;
}

/* 質問は右、回答は左。どちらの発言か、位置だけで分かるようにする */
.msg { display: flex; margin-bottom: 18px; }
.msg--user { justify-content: flex-end; }
.msg__body { min-width: 0; padding-top: 3px; }
.msg--assistant .msg__body { flex: 1; }
.msg--user .msg__body {
    max-width: min(78%, 620px);
    background: var(--surface-2); border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 11px 15px;
}
/* 到着中の回答。末尾にカーソルを出して、まだ続きがあることを示す */
.streaming::after {
    content: ""; display: inline-block; width: 7px; height: 15px;
    margin-left: 2px; vertical-align: -2px; background: var(--accent);
    border-radius: 1px; animation: blink 1.1s steps(2, start) infinite;
}
.streaming.is-done::after { content: none; }
@keyframes blink { to { visibility: hidden; } }

.msg__body > *:first-child { margin-top: 0; }
.msg__body > *:last-child { margin-bottom: 0; }
.msg__body p { margin: 0 0 8px; }
/* 回答の中のリンクは、押せると分かるよう最初から下線を引く
   （本文と同じ色の並びだと、リンクだと気づかれない） */
.msg__body a { text-decoration: underline; text-underline-offset: 2px; }
.msg__body ul, .msg__body ol { margin: 0 0 8px; padding-left: 22px; }

/* 回答待ちの表示。経過時間だけが動くので、数字が揺れて目立ちすぎないよう
   等幅の数字にして、色は本文より落とす。 */
.thinking {
    display: flex; align-items: center; gap: 8px;
    color: var(--muted); font-size: 13.5px;
}
.thinking__label:empty { display: none; }
.thinking__time { font-variant-numeric: tabular-nums; }

.toolblock {
    border: 1px solid var(--border); border-radius: var(--radius-sm);
    background: var(--surface); margin-bottom: 10px; overflow: hidden;
}
.toolblock__head {
    display: flex; align-items: center; gap: 8px; padding: 8px 12px;
    background: var(--surface-2); font-size: 13px; font-weight: 500;
    color: var(--muted);
}
.toolblock__note {
    padding: 9px 13px; border-top: 1px solid var(--border);
    font-size: 12.5px; line-height: 1.75; color: var(--muted);
}
.toolblock__note b { color: var(--text); font-weight: 500; }
.toolblock pre {
    margin: 0; padding: 11px 13px; overflow-x: auto;
    font-size: 12.2px; line-height: 1.55; background: var(--surface);
}
.toolblock__foot { padding: 6px 11px; border-top: 1px solid var(--border);
                   display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }

/* 触れているテーブルから、カタログの該当テーブルへ飛ぶリンク（チャット画面） */
.catlinks { display: flex; align-items: center; gap: 8px; flex-wrap: wrap;
            font-size: 12px; }
.catlinks a { font-family: var(--mono); font-size: 11.5px; }

.plot { width: 100%; min-height: 340px; }
/* --- 社内文書の出典 -----------------------------------------------------------
   回答の [出典n] と突き合わせるための一覧。抜粋は2行に畳み、
   行を押すと全文が出る（長い抜粋が並ぶと、回答本文が埋もれるため）。 */

.srcs { padding: 8px 11px; display: flex; flex-direction: column; gap: 8px; }
.src { cursor: pointer; border-left: 2px solid var(--border); padding-left: 9px; }
.src:hover { border-left-color: var(--accent); }
.src__where { font-size: 12.5px; display: flex; gap: 6px; flex-wrap: wrap; align-items: baseline; }
.src__no { color: var(--accent); font-weight: 600; }
.src__text {
    color: var(--muted); font-size: 12.5px; line-height: 1.7; margin-top: 2px;
    display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 2;
    overflow: hidden;
}
.src.is-open .src__text { -webkit-line-clamp: unset; overflow: visible; }

.filecard {
    display: flex; align-items: center; gap: 12px; padding: 13px 15px;
    border: 1px solid var(--border-2); background: var(--surface);
    border-radius: var(--radius-sm); margin-bottom: 10px;
}
.filecard .icon { color: var(--muted); }
.filecard .name { font-weight: 500; }

/* --- 画像のドロップ先 ------------------------------------------------------------
   ふだんは出さず、ファイルをドラッグしてきたときだけチャット全体を覆う。
   落とす場所を探させないよう、狙いは「画面のどこでもよい」にしている。 */

.dropzone {
    position: absolute; inset: 0; z-index: 40;
    display: none; align-items: center; justify-content: center;
    background: color-mix(in srgb, var(--bg) 82%, transparent);
    backdrop-filter: blur(1.5px);
}
.dropzone.is-on { display: flex; }
.dropzone__box {
    display: flex; align-items: center; gap: 12px;
    padding: 22px 32px; border-radius: var(--radius);
    border: 2px dashed var(--accent); background: var(--surface);
    color: var(--accent); font-weight: 550; font-size: 15px;
    box-shadow: var(--shadow-lg);
}
.dropzone.is-warn .dropzone__box { border-color: var(--warn); color: var(--warn); }

/* --- 画像の添付 ---------------------------------------------------------------- */
.attachlist { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 8px; }
.attach {
    display: flex; align-items: center; gap: 6px; padding: 4px 8px 4px 4px;
    border: 1px solid var(--border-2); border-radius: var(--radius-sm);
    background: var(--surface-2); font-size: 12px; max-width: 220px;
}
.attach img { width: 34px; height: 34px; object-fit: cover; border-radius: 4px; }
.attach__name { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.attach__x {
    border: 0; background: none; cursor: pointer; color: var(--muted);
    font-size: 15px; line-height: 1; padding: 0 2px;
}
.attach__x:hover { color: var(--err); }

/* 送信済みの画像（吹き出しの中） */
.sentimgs { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 6px; }
.sentimgs img {
    max-width: 220px; max-height: 180px; border-radius: var(--radius-sm);
    border: 1px solid var(--border-2); display: block;
}

/* --- 発言の巻き戻し・編集 ------------------------------------------------------- */
.turn { position: relative; }
.turn__tools {
    position: absolute; top: -6px; right: -4px; display: flex; gap: 2px;
    opacity: 0; transition: opacity .12s;
    background: var(--surface); border: 1px solid var(--border-2);
    border-radius: 999px; padding: 2px; box-shadow: var(--shadow);
}
/* 触れるまで隠す。キーボード操作でも出るように :focus-within を入れる */
.msg:hover .turn__tools, .turn:focus-within .turn__tools { opacity: 1; }
.turn__btn {
    border: 0; background: none; cursor: pointer; padding: 3px 8px;
    border-radius: 999px; font-size: 13px; line-height: 1;
    display: inline-flex; align-items: center; gap: 4px;
}
.turn__btn:hover { background: var(--surface-2); }
/* アイコンに添える一言。押す前に何が起こるか分かるように */
.turn__btn__t { font-size: 11px; color: var(--muted); }
.turn__btn:hover .turn__btn__t { color: var(--text); }
.turn__edit {
    width: 100%; min-height: 64px; padding: 10px 12px; font: inherit; font-size: 14px;
    border: 1px solid var(--accent); border-radius: var(--radius-sm);
    background: var(--surface); color: var(--text); resize: none;
}

/* --- メール設定 --------------------------------------------------------------- */
.chips { display: flex; flex-wrap: wrap; gap: 6px; }
.chip {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 4px 10px; border-radius: 999px; font-size: 12.5px;
    border: 1px solid var(--border-2); background: var(--surface-2);
}
.chip__x {
    border: 0; background: none; cursor: pointer; color: var(--muted);
    font-size: 15px; line-height: 1; padding: 0 2px;
}
.chip__x:hover { color: var(--err); }

/* 文脈の使用量。いま（濃い）と、上限まで育ったとき（薄い）を重ねて見せる */

.kvrow { display: flex; gap: 10px; padding: 3px 0; font-size: 13px; }
.kvrow__k { width: 130px; flex: 0 0 130px; color: var(--muted); }

.check { display: inline-flex; align-items: center; gap: 8px; cursor: pointer; }
.check input { width: 16px; height: 16px; }

/* --- 分析結果（表＋所見） ----------------------------------------------------- */
.report { margin-bottom: 10px; }
.report__title {
    font-weight: 600; font-size: 15.5px; letter-spacing: -.005em;
    margin-bottom: 8px; padding-bottom: 6px; border-bottom: 1px solid var(--border);
}
.report__notes {
    margin: 10px 0 0; padding: 11px 14px 11px 28px;
    background: var(--surface-2); border-left: 2px solid var(--border-2);
    border-radius: var(--radius-sm); font-size: 13.5px; line-height: 1.75;
}
.report__notes li { margin: 3px 0; }

/* --- まとまったレポート ------------------------------------------------------- */
.doc {
    border: 1px solid var(--border-2); border-radius: var(--radius);
    background: var(--surface); margin-bottom: 12px; overflow: hidden;
}
.doc__head {
    display: flex; align-items: center; gap: 12px; padding: 16px 20px;
    border-bottom: 1px solid var(--border); background: var(--surface-2);
}
.doc__title { font-size: 17px; font-weight: 600; letter-spacing: -.01em; }
.doc__summary { padding: 14px 20px; background: var(--surface-2);
                border-bottom: 1px solid var(--border); }
.doc__label {
    font-size: 11px; font-weight: 600; color: var(--muted);
    letter-spacing: .1em; text-transform: uppercase; margin-bottom: 6px;
}
.doc__summary ul { margin: 0; padding-left: 20px; line-height: 1.8; }
.doc__section { padding: 16px 20px; border-top: 1px solid var(--border); }
.doc__h {
    margin: 0 0 10px; font-size: 15px; font-weight: 600;
    padding-left: 10px; border-left: 2px solid var(--border-2);
}
.doc__note {
    margin-top: 8px; padding: 8px 12px; font-size: 13px;
    background: var(--surface-2); border-left: 3px solid var(--border-2);
    border-radius: var(--radius-sm);
}
.doc__actions { margin: 0; padding-left: 22px; line-height: 1.9; }

/* --- メールの下書き ---------------------------------------------------------- */
.mailcard {
    border: 1px solid var(--border-2); border-radius: var(--radius-sm);
    background: var(--surface); margin-bottom: 10px; overflow: hidden;
}
.mailcard__head {
    display: flex; align-items: center; gap: 8px; padding: 10px 14px;
    background: var(--surface-2); border-bottom: 1px solid var(--border);
}
.mailcard__row {
    display: flex; gap: 10px; padding: 5px 14px; font-size: 13px;
    border-bottom: 1px dashed var(--border);
}
.mailcard__label { width: 64px; flex: 0 0 64px; color: var(--muted); }
.mailcard__body {
    margin: 0; padding: 14px; white-space: pre-wrap; word-break: break-word;
    font: inherit; font-size: 13.5px; line-height: 1.8; max-height: 340px; overflow: auto;
}
.mailcard__foot {
    display: flex; align-items: center; gap: 10px; padding: 10px 14px;
    border-top: 1px solid var(--border); background: var(--surface-2);
}

.examples { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 16px; }
.example {
    padding: 7px 12px; border: 1px solid var(--border-2); border-radius: 999px;
    background: var(--surface); cursor: pointer; font: inherit; font-size: 12.5px;
}
.example:hover { border-color: var(--accent); color: var(--accent); }

.empty { text-align: center; color: var(--muted); padding: 72px 20px; }
.empty__icon { margin-bottom: 14px; color: var(--border-2); }
.empty__icon .icon { width: 40px; height: 40px; stroke-width: 1.1; }

/* 説明の吹き出し（JS版・common.js）。body直下に置くので親に切られない */
.desctip {
    position: fixed; z-index: 400; display: none; pointer-events: none;
    max-width: 340px; padding: 9px 12px; border-radius: var(--radius-sm);
    background: var(--text); color: var(--bg);
    font-size: 12px; line-height: 1.7; letter-spacing: .01em;
    box-shadow: var(--shadow-lg); white-space: pre-line;
}
.desctip__title { font-weight: 700; margin-bottom: 3px; }
.desctip__body--none { opacity: .7; font-style: normal; }
.desctip__meta { margin-top: 5px; opacity: .65; font-size: 11px; }

/* --- 対象データの選択 -------------------------------------------------------- */

.dbpick { border: 1px solid var(--border); border-radius: var(--radius-sm); margin-bottom: 6px; }
.dbpick__head {
    display: flex; align-items: center; gap: 8px; padding: 7px 10px; cursor: pointer;
}
.dbpick__head:hover { background: var(--surface-2); }
.dbpick__name { font-weight: 600; font-size: 12.5px; flex: 1; min-width: 0;
                overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.dbpick__tables { padding: 2px 10px 9px 30px; display: none; }
.dbpick.is-open .dbpick__tables { display: block; }
/* テーブル名は「押すと中身が開く」リンク。ふだんは一覧として静かに見せ、
   マウスを乗せたときだけ下線を出す（サイドバーが青いリンクだらけにならないように） */
.dbpick__table {
    display: flex; gap: 7px; align-items: center; font-size: 12px; padding: 2px 0;
}
.dbpick__tname {
    color: var(--muted); text-decoration: none; min-width: 0;
    overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.dbpick__tname:hover { color: var(--text); text-decoration: underline; text-underline-offset: 2px; }
/* 対象にする表の選択。外したものは薄くして、消さずに残す（また戻せることを示す） */
.tblpick, .grppick { flex: none; margin: 0; cursor: pointer; }
.dbpick__table:has(.tblpick:not(:checked)) .dbpick__tname { opacity: .45; }
/* 一覧はチェックの分だけ左を詰める（インデントが二重にならないように） */
.dbpick__tables { padding-left: 22px; }

/* --- 社内文書の検索先 ---------------------------------------------------------
   外したものは薄く見せる。消さずに残すのは、また戻せることを示すため。 */

.kbpick {
    display: flex; align-items: center; gap: 8px; padding: 5px 8px;
    border-radius: var(--radius-sm); cursor: pointer; font-size: 12.5px;
}
.kbpick:hover { background: var(--surface-2); }
.kbpick__name { min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.kbpick.is-off { opacity: .45; }

.histitem {
    display: flex; align-items: center; gap: 6px; padding: 6px 9px;
    border-radius: var(--radius-sm); cursor: pointer; font-size: 12.5px;
}
.histitem:hover { background: var(--surface-2); }
.histitem.is-active { background: var(--accent-weak); color: var(--accent); font-weight: 600; }
.histitem__title { flex: 1; min-width: 0; overflow: hidden;
                   text-overflow: ellipsis; white-space: nowrap; }
.histitem__del { opacity: 0; border: none; background: none; cursor: pointer;
                 color: var(--muted); padding: 0 3px; font-size: 13px; }
.histitem:hover .histitem__del { opacity: 1; }
.histitem__del:hover { color: var(--err); }

/* --- ER図キャンバス --------------------------------------------------------- */

.er { position: relative; border: 1px solid var(--border); border-radius: var(--radius);
      background: var(--surface); overflow: hidden; height: 620px; }
/* チャットのモーダル内での高さ。インラインstyleにすると .er--full の100vhが
   上書きできず「全画面なのに下が欠ける」ことになるため、必ずクラスで与える */
.er--chat { height: 72vh; }
.er--full { position: fixed; inset: 0; z-index: 200; height: 100vh; border-radius: 0; }
.er__toolbar {
    position: absolute; top: 10px; left: 10px; z-index: 6; display: flex; gap: 6px;
    flex-wrap: wrap; align-items: center; background: var(--surface); padding: 6px;
    border: 1px solid var(--border); border-radius: var(--radius-sm); box-shadow: var(--shadow);
}
/* 保存・元に戻す・やり直す のまとまり。区切り線で他のボタンと分ける */
.er__tools { display: inline-flex; gap: 2px; padding-right: 8px; margin-right: 2px;
             border-right: 1px solid var(--border); }
.er__viewport { position: absolute; inset: 0; overflow: hidden; cursor: grab;
    background-image: radial-gradient(var(--border) 1px, transparent 1px);
    background-size: 22px 22px; }
.er__viewport.is-panning { cursor: grabbing; }
/* ノードとSVGには同じ transform を当てるので、変形の基準点も必ず揃えること。
   SVG側だけ既定(50% 50%)のままだと、拡大縮小した瞬間に線とテーブルがずれる。 */
.er__world, .er__svg { position: absolute; top: 0; left: 0; transform-origin: 0 0; }
.er__svg { overflow: visible; pointer-events: none; }
.er__svg path { pointer-events: stroke; cursor: pointer; }

.ertable {
    position: absolute; width: 232px; background: var(--surface);
    border: 1.5px solid var(--border-2); border-radius: 4px;
    box-shadow: var(--shadow); font-size: 11.5px; user-select: none;
}
.ertable:hover { border-color: var(--accent); box-shadow: var(--shadow-lg); }
.ertable.is-selected { border-color: var(--accent); box-shadow: 0 0 0 2px var(--accent-weak); }
.ertable__head {
    padding: 5px 8px; text-align: center; font-weight: 700; cursor: move;
    background: var(--surface-2); border-bottom: 1px solid var(--border);
    border-radius: 3px 3px 0 0;
}
.ertable__head .rows { font-weight: 400; opacity: .6; font-size: 10px; }
.ercol {
    display: flex; align-items: center; gap: 6px; padding: 2px 8px;
    position: relative; white-space: nowrap;
}
.ercol:hover { background: var(--accent-weak); }
.ercol__name { flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; }
.ercol__type { opacity: .45; font-size: 10px; }
.ercol.pk > .ercol__name { text-decoration: underline; text-decoration-thickness: 1.5px; }
.ercol.fk > .ercol__name { text-decoration: underline; text-decoration-style: dashed; }
.ercol.pk.fk > .ercol__name { text-decoration: underline; text-decoration-style: double; }
/* 接続点は列の左右どちらにも置く。相手テーブルが左にあるときは左から引く。 */
.erhandle {
    position: absolute; top: 50%; transform: translateY(-50%);
    width: 11px; height: 11px; border-radius: 50%;
    background: var(--border-2); border: 2px solid var(--surface);
    cursor: crosshair; opacity: 0; transition: opacity .12s, background .12s;
}
.erhandle--l { left: -6px; }
.erhandle--r { right: -6px; }
.ercol:hover .erhandle, .ertable:hover .erhandle { opacity: 1; }
.erhandle:hover { background: var(--accent); transform: translateY(-50%) scale(1.4); }
/* 多重度（1 / *）。細い線の上に乗るので、背景色で縁取って読めるようにする */
.er__edgelabel {
    font-size: 14px; font-weight: 800; fill: var(--text);
    paint-order: stroke; stroke: var(--surface); stroke-width: 4px; stroke-linejoin: round;
}
.er__edgelabel.is-selected { fill: var(--accent); }
/* 線の上に置く累積使用回数。座布団を敷かないと線と重なって読めない */
.er__countbg { fill: var(--surface); stroke: var(--border); stroke-width: 1px; }
.er__countbg.is-zero { fill: var(--surface-2); stroke-dasharray: 3 2; }
.er__count { font-size: 10px; font-weight: 700; fill: var(--text); }
.er__count.is-zero { font-weight: 600; fill: var(--muted); }
.er__panel {
    position: absolute; right: 10px; bottom: 10px; z-index: 6; width: 320px;
    background: var(--surface); border: 1px solid var(--border);
    border-radius: var(--radius); box-shadow: var(--shadow-lg); padding: 12px;
    max-height: calc(100% - 20px); overflow: auto;
}
/* テーブルの中身（列・サンプル行）を出すときは広げる。キャンバスからはみ出さない幅に */
.er__panel--wide { width: min(560px, calc(100% - 20px)); }
/* 最大化: キャンバスいっぱいに広げる（ドラッグで決めた大きさは無視） */
.er__panel--max { left: 10px !important; top: 10px !important; right: 10px; bottom: 10px;
                  width: auto !important; height: auto !important; max-height: none; }
/* 境目をつまんで大きさを変えるための取っ手。パネルは右下に付いているので、
   左辺・上辺・左上の角の3つ。見た目は出さず、カーソルだけで分からせる */
.er__grip { position: absolute; z-index: 7; }
.er__grip--l  { left: -4px; top: 12px; bottom: 12px; width: 8px; cursor: ew-resize; }
.er__grip--t  { top: -4px; left: 12px; right: 12px; height: 8px; cursor: ns-resize; }
.er__grip--tl { left: -5px; top: -5px; width: 14px; height: 14px; cursor: nwse-resize; }
.er__panel--max .er__grip { display: none; }
/* 中身がパネルの高さを超えたら本文だけスクロール（見出しは残す） */
.er__panel { display: flex; flex-direction: column; }
.er__panel__body { overflow: auto; min-height: 0; }
.er__legend {
    position: absolute; left: 10px; bottom: 10px; z-index: 5; font-size: 11px;
    color: var(--muted); background: var(--surface); padding: 5px 9px;
    border: 1px solid var(--border); border-radius: var(--radius-sm);
}

/* --- ダイアログ（ファイル選択） ------------------------------------------------ */

.modal { position: fixed; inset: 0; z-index: 300; display: grid; place-items: center;
         background: rgba(16,24,40,.45); padding: 20px; }
.modal__box {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: var(--radius); box-shadow: var(--shadow-lg);
    width: 100%; max-width: 720px; max-height: 80vh; display: flex; flex-direction: column;
}
.modal__head { display: flex; align-items: center; gap: 10px;
               padding: 12px 14px; border-bottom: 1px solid var(--border); }
.modal__crumbs { display: flex; flex-wrap: wrap; gap: 4px; align-items: center;
                 padding: 8px 14px; border-bottom: 1px solid var(--border);
                 font-size: 12.5px; background: var(--surface-2); }
.modal__crumbs button { border: none; background: none; color: var(--accent);
                        font: inherit; cursor: pointer; padding: 1px 3px; }
.modal__crumbs button:hover { text-decoration: underline; }
.modal__body { flex: 1; overflow-y: auto; padding: 6px 8px; }
.modal__foot { padding: 8px 14px; border-top: 1px solid var(--border); }

.fsrow { display: flex; align-items: center; gap: 9px; padding: 7px 10px;
         border-radius: var(--radius-sm); cursor: pointer; font-size: 13px; }
.fsrow:hover { background: var(--surface-2); }
.fsrow .name { flex: 1; min-width: 0; overflow: hidden;
               text-overflow: ellipsis; white-space: nowrap; }
.fsrow .meta { color: var(--muted); font-size: 11.5px; white-space: nowrap; }

.chosenfile { display: flex; align-items: center; gap: 10px; padding: 9px 12px;
              border: 1px solid var(--accent); background: var(--accent-weak);
              border-radius: var(--radius-sm); }

/* --- トースト --------------------------------------------------------------- */

/* 画面右上に出す（右下は「未保存バー」と送信ボタンの居場所なので、そこには重ねない）。
   新しいものほど下に積まれ、上から順に消えていく。 */
.toasts { position: fixed; right: 18px; top: 18px; z-index: 500;
          display: flex; flex-direction: column; gap: 10px; }
.toast {
    padding: 14px 20px; border-radius: var(--radius-sm); background: var(--surface);
    border: 1px solid var(--border); box-shadow: var(--shadow-lg);
    font-size: 13.5px; font-weight: 500; line-height: 1.55;
    min-height: 48px; display: flex; align-items: center;
    max-width: 440px; min-width: 240px;
    animation: toastin .18s ease-out;
}
.toast--ok { border-left: 3px solid var(--ok); }
.toast--err { border-left: 3px solid var(--err); }
.toast--warn { border-left: 3px solid var(--warn); }
@keyframes toastin { from { opacity: 0; transform: translateY(-8px); } }

/* AIの回答の中の注意書き（※ ⚠ で始まる行）。データの信頼性にかかわるので目立たせる */
.caveat { color: var(--err); font-weight: 600; }

/* --- テーブルビューアの列フィルター（Excelのフィルター相当）------------------- */

.th__inner { display: flex; align-items: center; gap: 4px; }
.th__name { cursor: pointer; user-select: none; flex: 1; min-width: 0; }
.th__name:hover { color: var(--text); }
.th__filter {
    border: none; background: none; padding: 0 2px; cursor: pointer;
    color: var(--border-2); display: inline-flex; align-items: center; border-radius: 4px;
}
.th__filter:hover { color: var(--text); background: var(--surface); }
.th__filter.is-on { color: var(--accent); }

/* 絞り込みの一覧（いま何で絞っているか） */
/* .chip / .chips / .chip__x の定義はこの上（メール設定・モデル設定の節）に1組だけ。
   ここにもう1組あったため、後に書いたこちらが常に勝ち、
   先に書いた方が丸ごと効いていなかった。重複を消して1か所に戻す。 */

/* 列の見出しから開くフィルターの小窓 */
.colfilter {
    position: fixed; z-index: 400; width: 300px; padding: 10px;
    background: var(--surface); border: 1px solid var(--border-2);
    border-radius: var(--radius-sm); box-shadow: var(--shadow-lg);
    display: flex; flex-direction: column; gap: 6px;
}
.colfilter__head { display: flex; align-items: center; gap: 6px; }
.colfilter__list { max-height: 260px; overflow: auto; border: 1px solid var(--border);
                   border-radius: var(--radius-sm); padding: 6px; }
.colfilter__row { display: flex; align-items: center; gap: 6px; font-size: 12.5px;
                  padding: 2px 0; cursor: pointer; }
.colfilter__row:hover { background: var(--surface-2); }

.spinner {
    width: 15px; height: 15px; border: 2px solid var(--border-2);
    border-top-color: var(--accent); border-radius: 50%;
    animation: spin .7s linear infinite; display: inline-block; vertical-align: -2px;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* --- ログイン --------------------------------------------------------------- */

.loginpage { min-height: 100vh; display: grid; place-items: center; padding: 24px; }
.loginbox { width: 100%; max-width: 380px; }
.loginbox .brand { text-align: center; margin-bottom: 26px; }
.loginbox .brand .icon { width: 34px; height: 34px; color: var(--accent); stroke-width: 1.3; }
.loginbox .brand h1 {
    margin: 14px 0 4px; font-size: 22px; font-weight: 600; letter-spacing: -.02em;
}

@media (max-width: 860px) {
    .sidebar { position: fixed; left: -100%; z-index: 100; transition: left .2s; }
    .sidebar.is-open { left: 0; box-shadow: var(--shadow-lg); }
    .resizer { display: none; }          /* 狭い画面では幅を触らせない */
    .content { padding: 16px; }
    .chat__log, .chat__composer { padding-left: 14px; padding-right: 14px; }
}

/* 利用状況の質問・回答の表。長い本文は2行で切る（1行1問を見渡せるように）。
   列幅は見出しの指定どおりに固定する。fixed にしないと、長い本文の列が
   幅を取り合って、短い列が1文字ぶんまで潰れる。 */
table.qa { table-layout: fixed; }
table.qa td { vertical-align: top; }
/* 2行で切るのはセルの中の div。td 自体の display を変えると、
   セルが表の列構造から外れて、回答が質問の下に落ちる。 */
table.qa .qa__clamp {
    display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;
    overflow: hidden; white-space: normal; line-height: 1.5;
    overflow-wrap: anywhere;
}
table.qa td.qa__a { color: var(--muted); }

/* 利用状況: 見出しの並び替えボタンと、列フィルターの小窓（Excel風） */
table.qa th { white-space: nowrap; }
.qa__sort { background: none; border: none; padding: 0; font: inherit;
            font-weight: inherit; color: inherit; cursor: pointer; }
.qa__sort:hover { color: var(--accent); }
.qa__arrow { margin-left: 2px; font-size: 10px; }
.qa__flt { background: none; border: 1px solid transparent; border-radius: 4px;
           padding: 0 4px; margin-left: 4px; cursor: pointer;
           color: var(--muted); font-size: 10px; }
.qa__flt:hover { color: var(--text); border-color: var(--border-2); }
.qa__flt.is-on { color: var(--accent); border-color: var(--accent); }
.qa-pop { position: fixed; z-index: 300; /* ER図の全画面(200)より上 */
          width: 280px; padding: 10px;
          background: var(--surface); border: 1px solid var(--border-2);
          border-radius: 8px; box-shadow: 0 8px 24px rgba(0, 0, 0, .18); }
.qa-pop input[type="text"] { width: 100%; }
.qa-pop__list { max-height: 240px; overflow-y: auto; margin-top: 8px; }
.qa-pop__item { display: flex; gap: 6px; align-items: center;
                padding: 2px 0; font-size: 12px; cursor: pointer; }
.qa-pop__item input { flex: none; }
.qa-pop__item span { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

/* SQLの日本語解説（用語・例文のエディタ）。SQLを読めない人への読み下し */
.sqlnote { margin-top: 6px; line-height: 1.6; }
.sqlnote:empty { display: none; }
.sqlnote__head { font-weight: 600; color: var(--text); opacity: .75; }

/* ER図: まとまり表示中に、関連で繋がっている「隣のまとまりの表」を破線で出す */
.ertable--other { outline: 2px dashed var(--border-2); outline-offset: 2px; opacity: .92; }

/* ER図: 結合候補の相手として画面に出している表（候補線と同じ赤系） */
.ertable--sug { outline: 2px dashed var(--err); outline-offset: 2px; opacity: .95; }
/* 候補線の多重度の文字も赤系に */
.er__edgelabel--sug { fill: var(--err); }

/* まとまりのメモ行。右列（表示名・キー）が縦に長いので、.row 既定の下揃えだと
   左のメモが押し下げられて上に空白ができる。ここは上揃えで固定する */
.gmemo { align-items: flex-start; }
""",

# --- js/app.js ---
"js/app.js": r"""// 統合スクリプト。元は static/js の10ファイル。
// 共通部（common / er / manage）は素のまま、画面別の7本は
// 「その画面のときだけ動く」即時関数で包んである（window.XXX が画面の目印）。

// ===== 元 common.js =====
/* 画面共通の小道具: 通信・トースト・DOM生成 */

const $  = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];

/* 線画アイコン。実体は _icons.html のスプライト（絵文字は使わない）。
   el() に渡せるよう DOM ノードで返す。 */
function icon(name, cls = '') {
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('class', `icon ${cls}`.trim());
    svg.setAttribute('viewBox', '0 0 24 24');
    svg.setAttribute('aria-hidden', 'true');
    const use = document.createElementNS('http://www.w3.org/2000/svg', 'use');
    use.setAttribute('href', `#i-${name}`);
    svg.append(use);
    return svg;
}

function el(tag, attrs = {}, ...children) {
    const node = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
        if (v === null || v === undefined || v === false) continue;
        if (k === 'class') node.className = v;
        else if (k === 'html') node.innerHTML = v;
        else if (k.startsWith('on') && typeof v === 'function') node.addEventListener(k.slice(2), v);
        else node.setAttribute(k, v);
    }
    for (const c of children.flat()) {
        if (c === null || c === undefined || c === false) continue;
        node.append(c.nodeType ? c : document.createTextNode(String(c)));
    }
    return node;
}

/* 「テーブル全体を閲覧」ボタン。サンプル行を出している所には必ずこれを添える。
   先頭数行だけでは「本当にこのテーブルでよいか」は決められないので、
   別タブ（読み取り専用のビューア）で中身を辿れるようにする。
   db はファイル名（sales.db）でもエイリアス（sales）でもよい。 */
function tableViewLink(dbName, table, cls = 'btn btn--sm btn--ghost') {
    if (!dbName || !table) return null;
    const href = `/table?db=${encodeURIComponent(dbName)}&table=${encodeURIComponent(table)}`;
    return el('a', {
        class: cls, href, target: '_blank', rel: 'noopener',
        title: `${table} の全行を別タブで開きます（読み取り専用）`,
    }, icon('table', 'icon--sm'), 'テーブル全体を閲覧');
}

function toast(message, kind = 'ok', ms = 4200) {
    const box = $('#toasts');
    if (!box) return;
    const node = el('div', { class: `toast toast--${kind}` }, message);
    box.append(node);
    setTimeout(() => { node.style.opacity = '0'; setTimeout(() => node.remove(), 250); }, ms);
}

async function api(url, body, method = 'POST') {
    const opt = { method, headers: { 'Content-Type': 'application/json' } };
    if (body !== undefined) opt.body = JSON.stringify(body);
    if (method === 'GET') { delete opt.body; delete opt.headers; }
    const res = await fetch(url, opt);
    let data = {};
    try { data = await res.json(); } catch (e) { /* 本文なし */ }
    if (!res.ok) {
        // 呼び出し側が状況で分岐できるように、状態番号と本文も持たせる
        const err = new Error(data.error || `通信に失敗しました (${res.status})`);
        err.status = res.status;
        err.data = data;
        throw err;
    }
    return data;
}

/* 最低限のMarkdown。AIの回答は見出し・箇条書き・強調・コードくらいしか使わない */
/* Markdownの表（| a | b | の並び）を <table> にする。
   AIは一覧を表で返すことが多く、生の | と --- が並ぶと読めない。
   セル内の <br>（AIが改行の意図で書く）は改行として扱う。行の | が揃っていなくても
   ある分だけ描く（崩れた表を全部捨てるより、読める形で出す方がよい）。 */
function mdTables(html) {
    const lines = html.split('\n');
    const out = [];
    let i = 0;
    const isRow = l => /^\s*\|.*\|\s*$/.test(l);
    const isSep = l => /^\s*\|(\s*:?-{2,}:?\s*\|)+\s*$/.test(l);
    const cells = l => l.trim().replace(/^\||\|$/g, '').split('|')
        .map(c => c.trim().replace(/&lt;br\s*\/?&gt;/gi, '<br>'));
    while (i < lines.length) {
        if (isRow(lines[i]) && i + 1 < lines.length && isSep(lines[i + 1])) {
            const head = cells(lines[i]);
            const body = [];
            i += 2;
            while (i < lines.length && isRow(lines[i]) && !isSep(lines[i])) {
                body.push(cells(lines[i])); i += 1;
            }
            out.push('<div class="tablewrap"><table class="data"><thead><tr>'
                + head.map(h => `<th>${h}</th>`).join('') + '</tr></thead><tbody>'
                + body.map(r => '<tr>' + r.map(c => `<td>${c}</td>`).join('') + '</tr>').join('')
                + '</tbody></table></div>');
            continue;
        }
        out.push(lines[i]); i += 1;
    }
    return out.join('\n');
}

function mdToHtml(src) {
    const esc = s => s.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
    const blocks = esc(src || '').split(/```/);
    return blocks.map((chunk, i) => {
        if (i % 2 === 1) return `<pre class="mono" style="background:var(--surface-2);padding:10px;border-radius:6px;overflow:auto">${chunk.replace(/^\w*\n/, '')}</pre>`;
        // リンクは先に <a> にして目印へ逃がす。あとの行単位の置換で
        // URLの中の記号（*・-・_ など）が別の意味に取られるのを防ぐ。
        // 開けるのは http/https だけ（javascript: などは文字のまま出す）。
        const links = [];
        const stash = html => `\u0000L${links.push(html) - 1}\u0000`;
        const anchor = (url, text) =>
            stash(`<a href="${url}" target="_blank" rel="noopener noreferrer">${text}</a>`);
        // 表を先に確定してから行単位の置換にかける（表の中の * や - を箇条書きと誤認しないため）
        return mdTables(chunk)
            // `コード` はそのまま見せる場所なので、先に確保して以降の置換から外す
            // （中に書かれたURLをリンクにしない・記号を装飾に取られない）
            .replace(/`([^`\n]+)`/g, (m, t) => stash(`<code>${t}</code>`))
            // [表示文](URL)
            .replace(/\[([^\]\n]+)\]\((https?:\/\/[^\s)]+)\)/g, (m, t, u) => anchor(u, t))
            // 素のURL。文末の句読点や閉じ括弧は URL に含めない
            .replace(/https?:\/\/[^\s<>"'`）)\]]+/g, u => {
                const tail = u.match(/[.,、。!?！？:;]+$/);
                const url = tail ? u.slice(0, -tail[0].length) : u;
                return anchor(url, url) + (tail ? tail[0] : '');
            })
            .replace(/^### (.*)$/gm, '<h4>$1</h4>')
            .replace(/^## (.*)$/gm, '<h3>$1</h3>')
            .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
            // データの信頼性にかかわる注意書き（※ ⚠ で始まる行）は赤で出す。
            // 「更新できていない」「値の型が違う」は数字の読み方を左右するので、
            // 本文と同じ色で流すと読み飛ばされる。箇条書きの中の ※ も拾う。
            .replace(/^(\s*(?:[-*]\s*)?)([※⚠].*)$/gm, '$1<span class="caveat">$2</span>')
            .replace(/^\s*[-*] (.*)$/gm, '<li>$1</li>')
            .replace(/(<li>[\s\S]*?<\/li>)(?!\s*<li>)/g, '<ul>$1</ul>')
            // 表の直前後の改行は <br> にしない（表の周りに余白が二重に入る）
            .replace(/\n*(<div class="tablewrap">)/g, '$1')
            .replace(/(<\/div>)\n*/g, '$1')
            .replace(/\n{2,}/g, '</p><p>')
            .replace(/\n/g, '<br>')
            // 逃がしておいたリンクを戻す
            .replace(/\u0000L(\d+)\u0000/g, (m, n) => links[n]);
    }).join('');
}

/* 値の見た目。数値は右寄せにしたいので型も返す */
function cellInfo(v) {
    if (v === null || v === undefined) return { text: '', num: false };
    if (typeof v === 'number') return { text: v.toLocaleString(undefined, { maximumFractionDigits: 6 }), num: true };
    return { text: String(v), num: false };
}

function dataTable(columns, rows, opts = {}) {
    const thead = el('thead', {}, el('tr', {}, columns.map(c => el('th', {}, c))));
    const tbody = el('tbody', {}, rows.map(r => el('tr', {},
        r.map(v => { const i = cellInfo(v); return el('td', { class: i.num ? 'num' : null, title: i.text }, i.text); })
    )));
    const wrap = el('div', { class: 'tablewrap' }, el('table', { class: 'data' }, thead, tbody));
    if (opts.caption) {
        return el('div', {}, wrap, el('div', { class: 'small muted', style: 'margin-top:4px' }, opts.caption));
    }
    return wrap;
}

/* --- 説明の吹き出し（はみ出さない版） --------------------------------------------
   CSSだけで作る .hastip は、要素の中に ::after を置くので、横を切り落とす親
   （サイドバーは overflow-x: hidden）の中では見えなくなる。こちらは body の直下に
   1つだけ作って画面座標で置くので、どこに置いた要素でも切れずに出せる。

   使い方: data-desc-title（見出し）/ data-desc（説明）/ data-desc-meta（右下の補足）
   説明が空でも、未登録であること自体を伝えたいので出す。 */

(function describeTip() {
    const DELAY = 260;                 // 通りすがりでは出さない
    let box = null, timer = null, current = null;

    function ensure() {
        if (box) return box;
        box = el('div', { class: 'desctip' });
        document.body.append(box);
        return box;
    }

    function place(target) {
        const b = ensure();
        const r = target.getBoundingClientRect();
        b.style.visibility = 'hidden';
        b.style.display = 'block';
        const w = b.offsetWidth, h = b.offsetHeight;
        // 基本は右側。入らなければ左に回す
        let x = r.right + 10;
        if (x + w > window.innerWidth - 8) x = Math.max(8, r.left - w - 10);
        let y = r.top + r.height / 2 - h / 2;
        y = Math.min(Math.max(8, y), window.innerHeight - h - 8);
        b.style.left = `${Math.round(x)}px`;
        b.style.top = `${Math.round(y)}px`;
        b.style.visibility = 'visible';
    }

    function show(target) {
        const title = target.dataset.descTitle || '';
        const desc = (target.dataset.desc || '').trim();
        const meta = target.dataset.descMeta || '';
        const b = ensure();
        // null は落としてから渡す。replaceChildren はNode以外を文字列にするので、
        // 見出しや補足が無いときに "null" という文字がそのまま吹き出しに出る。
        b.replaceChildren(...[
            title ? el('div', { class: 'desctip__title' }, title) : null,
            el('div', { class: desc ? 'desctip__body' : 'desctip__body desctip__body--none' },
                desc || '説明が未登録です。データカタログで書くと、AIの理解もここの表示も良くなります。'),
            meta ? el('div', { class: 'desctip__meta' }, meta) : null,
        ].filter(Boolean));
        place(target);
        current = target;
    }

    function hide() {
        clearTimeout(timer);
        current = null;
        if (box) box.style.display = 'none';
    }

    document.addEventListener('mouseover', ev => {
        const t = ev.target.closest?.('[data-desc]');
        if (!t || t === current) return;
        clearTimeout(timer);
        timer = setTimeout(() => show(t), DELAY);
    });
    document.addEventListener('mouseout', ev => {
        const t = ev.target.closest?.('[data-desc]');
        if (t && t === current && !t.contains(ev.relatedTarget)) hide();
        else if (t) clearTimeout(timer);
    });
    // キーボードで辿る人にも出す。スクロールしたら位置がずれるので消す
    document.addEventListener('focusin', ev => {
        const t = ev.target.closest?.('[data-desc]') || ev.target.querySelector?.('[data-desc]');
        if (t) show(t);
    });
    document.addEventListener('focusout', hide);
    window.addEventListener('scroll', hide, true);
    window.addEventListener('resize', hide);
})();

/* --- サイドバーの幅と開閉 ------------------------------------------------------
   境目をドラッグすると幅が変わり、クリックすると折りたたむ。
   「動かさずに離した」ときだけクリック扱いにしたいので、移動量で見分ける。 */

/* サイドバーの節（details.sbsec）の開閉。
   開閉そのものは <details> がやるので、ここでするのは2つだけ。
     ・前回の状態を覚えて復元する（節ごと）
     ・見出しに置いたボタン（＋新規・全選択）で開閉が起きないようにする
   localStorage は使えない環境（プライベートウィンドウ等）があるので、
   読み書きとも失敗しても既定の状態で動くようにしておく。 */
(function sidebarSections() {
    const key = (id) => 'sbsec:' + id;

    document.addEventListener('DOMContentLoaded', () => {
        $$('details.sbsec').forEach(sec => {
            if (sec.id) {
                try {
                    const saved = localStorage.getItem(key(sec.id));
                    if (saved !== null) sec.open = saved === '1';
                } catch (e) { /* 読めなければテンプレートの既定のまま */ }
                sec.addEventListener('toggle', () => {
                    try { localStorage.setItem(key(sec.id), sec.open ? '1' : '0'); } catch (e) { }
                });
            }
            // 見出しの中のボタンは、その機能だけ働かせる（節は開閉しない）。
            // 同じ要素に付いた本来のハンドラは stopPropagation では止まらないので、
            // ボタンの動作はそのまま生きる。
            $$('button', sec.querySelector(':scope > summary') || sec).forEach(btn => {
                btn.addEventListener('click', (ev) => {
                    ev.preventDefault();
                    ev.stopPropagation();
                });
            });
        });
    });
})();

(function sidebarHandle() {
    const MIN = 180, MAX = 460, DEFAULT = 244;
    const root = document.documentElement;
    const store = {
        get width() { return parseInt(localStorage.getItem('sidebarWidth') || '', 10) || DEFAULT; },
        set width(v) { localStorage.setItem('sidebarWidth', String(v)); },
        get collapsed() { return localStorage.getItem('sidebarCollapsed') === '1'; },
        set collapsed(v) { localStorage.setItem('sidebarCollapsed', v ? '1' : '0'); },
    };
    const clamp = (v) => Math.min(MAX, Math.max(MIN, Math.round(v)));

    function apply(width, collapsed) {
        root.style.setProperty('--sidebar', (collapsed ? 0 : width) + 'px');
        document.body.classList.toggle('is-collapsed', collapsed);
    }

    // 読み込み直後に反映（前回の状態を覚えている）
    let width = clamp(store.width), collapsed = store.collapsed;
    apply(width, collapsed);

    document.addEventListener('DOMContentLoaded', () => {
        const handle = $('#sidebarResizer');
        if (!handle) return;

        let startX = 0, startW = width, moved = false, dragging = false;

        const onMove = (ev) => {
            if (!dragging) return;
            const dx = ev.clientX - startX;
            if (Math.abs(dx) > 3) moved = true;
            if (!moved) return;
            // 畳んだ状態から右へ引いたら、その場で開く
            if (collapsed && dx > 0) { collapsed = false; store.collapsed = false; }
            width = clamp((collapsed ? 0 : startW) + dx);
            apply(width, false);
        };

        const onUp = () => {
            if (!dragging) return;
            dragging = false;
            handle.classList.remove('is-dragging');
            document.body.classList.remove('is-resizing');
            document.removeEventListener('pointermove', onMove);
            document.removeEventListener('pointerup', onUp);
            if (moved) {
                store.width = width;
            } else {                      // 動かさなかった = クリック
                collapsed = !collapsed;
                store.collapsed = collapsed;
                apply(width, collapsed);
            }
        };

        handle.addEventListener('pointerdown', ev => {
            if (ev.button !== 0) return;
            ev.preventDefault();
            dragging = true; moved = false;
            startX = ev.clientX;
            startW = collapsed ? 0 : width;
            handle.classList.add('is-dragging');
            document.body.classList.add('is-resizing');
            document.addEventListener('pointermove', onMove);
            document.addEventListener('pointerup', onUp);
        });

        // キーボードでも操作できるようにする
        handle.addEventListener('keydown', ev => {
            const step = ev.shiftKey ? 40 : 16;
            if (ev.key === 'ArrowLeft' || ev.key === 'ArrowRight') {
                ev.preventDefault();
                collapsed = false; store.collapsed = false;
                width = clamp(width + (ev.key === 'ArrowRight' ? step : -step));
                store.width = width;
                apply(width, false);
            } else if (ev.key === 'Enter' || ev.key === ' ') {
                ev.preventDefault();
                collapsed = !collapsed; store.collapsed = collapsed;
                apply(width, collapsed);
            }
        });

        handle.addEventListener('dblclick', () => {   // 既定の幅に戻す
            width = DEFAULT; collapsed = false;
            store.width = width; store.collapsed = false;
            apply(width, false);
        });
    });
})();

// ===== 元 er.js =====
/* ER図キャンバス。ライブラリなしで、テーブル移動・関連のドラッグ作成・
   多重度の変更・削除・元に戻す／やり直す・拡大縮小をまかなう。

   座標系は2つ。
     world  … ノードが持つ論理座標（.meta.yaml の er_layout と同じ）
     screen … 画面のピクセル。world に translate(tx,ty) scale(k) をかけたもの */

const ER = (() => {
    let data = { nodes: [], edges: [], alias: '' };
    let view = { tx: 40, ty: 40, k: 1 };
    let selected = null;          // {type:'edge'|'table', ...}
    // 履歴（元に戻す／やり直す）。ER図上のすべての操作を1手ずつ戻せる。
    // 操作ごとに「戻す手順」「やり直す手順」を関数で積む（コマンド方式）。
    //   移動                       … 画面の中だけ動かす（保存は 💾）
    //   関連の追加・削除・多重度 /
    //   主キー / 他DBテーブルの出し入れ … サーバに保存済みなので、逆の操作をサーバに送って戻す
    let past = [], future = [];
    const HIST_MAX = 50;
    let savedLayout = '';         // 最後に保存（または読み込み）した配置。💾 の活性判定に使う
    let root, viewport, world, svg, panel;
    // 読み取り専用（チャットからの表示）。編集の入口だけを閉じ、
    // 移動・パン・ズーム・全画面はそのまま使えるようにする。
    let ro = false;
    let docWired = false;         // documentへのキーハンドラは1回だけ張る
    // 過去の分析で実際に使われた結合の回数（{ "a.t.c||a.t.c": n }）。
    // 宣言された関連の上に「本当に通っている道」を重ねるためのもの。
    let usage = null;

    const NS = 'http://www.w3.org/2000/svg';
    const CARDS = ['N:1', '1:N', '1:1', 'N:M'];
    //: 多重度の読み方。N は「多」、N:M は両側とも多（多対多）
    const CARD_JA = { 'N:1': '多対1', '1:N': '1対多', '1:1': '1対1', 'N:M': '多対多' };

    /* --- 描画 ---------------------------------------------------------------- */

    function applyView() {
        world.style.transform = `translate(${view.tx}px, ${view.ty}px) scale(${view.k})`;
        svg.style.transform = world.style.transform;
    }

    function tableEl(n) {
        const box = el('div', {
            class: 'ertable',
            'data-id': n.id, style: `left:${n.x}px; top:${n.y}px`,
        },
            el('div', { class: 'ertable__head' },
                el('div', {}, n.table),
                el('div', { class: 'rows' },
                    n.rows === null || n.rows === undefined ? '行数不明' : `${n.rows.toLocaleString()}行`)));
        n.columns.forEach(c => {
            box.append(el('div', {
                class: 'ercol' + (c.pk ? ' pk' : '') + (c.fk ? ' fk' : ''),
                'data-col': c.name,
            },
                // 接続点は左右どちらにも置く。相手が左にあるときは左から引けたほうが自然なため。
                el('div', { class: 'erhandle erhandle--l', 'data-handle': c.name, 'data-side': 'left' }),
                el('span', { class: 'ercol__name' }, c.name),
                el('span', { class: 'ercol__type' }, c.type),
                el('div', { class: 'erhandle erhandle--r', 'data-handle': c.name, 'data-side': 'right' })));
        });
        return box;
    }

    /** 列の接続点（world座標）。DOMの実寸から取るのでフォント差に強い。 */
    function anchor(tableId, colName, side) {
        const box = world.querySelector(`.ertable[data-id="${CSS.escape(tableId)}"]`);
        if (!box) return null;
        const node = data.nodes.find(n => n.id === tableId);
        const col = box.querySelector(`.ercol[data-col="${CSS.escape(colName)}"]`);
        const y = node.y + (col ? col.offsetTop + col.offsetHeight / 2 : 14);
        const x = side === 'left' ? node.x : node.x + box.offsetWidth;
        return { x, y, w: box.offsetWidth };
    }

    function edgePath(e) {
        const [fa, ft] = e.from, [ta, tt] = e.to;
        const fid = `${fa}.${ft}`, tid = `${ta}.${tt}`;
        const fn = data.nodes.find(n => n.id === fid), tn = data.nodes.find(n => n.id === tid);
        if (!fn || !tn) return null;
        const fromRight = fn.x <= tn.x;
        const fSide = fromRight ? 'right' : 'left', tSide = fromRight ? 'left' : 'right';
        // 複合キーは列の数だけ端点がある。単一列の関連も同じ形で扱う
        const pairs = (e.pairs && e.pairs.length) ? e.pairs : [[e.from[2], e.to[2]]];
        const as = [], bs = [];
        pairs.forEach(([fc, tc]) => {
            const a = anchor(fid, fc, fSide), b = anchor(tid, tc, tSide);
            if (a && b) { as.push(a); bs.push(b); }
        });
        if (!as.length) return null;

        const dir = fromRight ? 1 : -1;
        const curve = (p, q, k) => {          // p → q を横向きの3次ベジェで
            // 制御点は距離の半分まで。超えると線が行き過ぎて膨らむ
            const len = Math.abs(q.x - p.x);
            const d2 = Math.max(6, Math.min(len * k, len / 2));
            return `M ${p.x} ${p.y} C ${p.x + dir * d2} ${p.y}, ${q.x - dir * d2} ${q.y}, ${q.x} ${q.y}`;
        };
        const midOf = (p, q, k) => {          // その曲線の中点（t=0.5）
            const len = Math.abs(q.x - p.x);
            const d2 = Math.max(6, Math.min(len * k, len / 2));
            const c1 = p.x + dir * d2, c2 = q.x - dir * d2;
            return { x: (p.x + 3 * c1 + 3 * c2 + q.x) / 8, y: (p.y + 3 * p.y + 3 * q.y + q.y) / 8 };
        };

        if (as.length === 1) {                // 単一列: 従来どおり1本の曲線
            const a = as[0], b = bs[0];
            return { d: curve(a, b, 0.45), a, b, mid: midOf(a, b, 0.45) };
        }

        // 複合キー: 各列から出た線をいったん合流させ、1本の幹で相手側へ渡し、
        // 相手側でまた各列へ分かれる。どの列の組で結んでいるかが目で追える
        const avgY = arr => arr.reduce((t, p) => t + p.y, 0) / arr.length;
        const gap = Math.abs(bs[0].x - as[0].x);
        const stub = Math.max(12, Math.min(46, gap * 0.22));
        const ja = { x: as[0].x + dir * stub, y: avgY(as) };
        const jb = { x: bs[0].x - dir * stub, y: avgY(bs) };
        const d = [
            ...as.map(p => curve(p, ja, 0.6)),
            curve(ja, jb, 0.45),
            ...bs.map(p => curve(jb, p, 0.6)),
        ].join(' ');
        return { d, a: ja, b: jb, mid: midOf(ja, jb, 0.45), fan: true };
    }

    /* 利用状況のキー。端点の並び順に依らないよう、文字列順で正規化する。
       複合キーの線は列ペアごとにキーを作り、いちばん使われたペアの回数で塗る */
    function usageKeys(e) {
        const [fa, ft] = e.from, [ta, tt] = e.to;
        return (e.pairs || [[e.from[2], e.to[2]]]).map(([fc, tc]) => {
            const a = `${fa}.${ft}.${fc}`, b = `${ta}.${tt}.${tc}`;
            return a <= b ? `${a}||${b}` : `${b}||${a}`;
        });
    }

    function usageCount(e) {
        return Math.max(...usageKeys(e).map(k => usage[k] || 0));
    }

    /* --- 利用回数の色（濃さ）------------------------------------------------------
       回数は片寄る（よく使う1本が何十回、残りは0〜数回）ので、対数で段を作る。
       いちばん多い線を濃さ1として、その中での位置で色を決める。 */

    function rgb(varName) {
        const v = getComputedStyle(document.documentElement)
            .getPropertyValue(varName).trim();
        const m = v.match(/^#?([0-9a-f]{6})$/i);
        if (m) {
            const n = parseInt(m[1], 16);
            return [n >> 16 & 255, n >> 8 & 255, n & 255];
        }
        const p = v.match(/\d+/g);
        return p ? p.slice(0, 3).map(Number) : [128, 128, 128];
    }

    /** 未使用（薄い）→ よく使う（濃い）の間を、0〜1の位置で混ぜる。 */
    function ramp(t, hot) {
        const a = rgb('--border-2'), b = rgb(hot);
        const c = a.map((v, i) => Math.round(v + (b[i] - v) * Math.min(1, Math.max(0, t))));
        return `rgb(${c[0]},${c[1]},${c[2]})`;
    }

    /** その図の中で、いちばん多く使われた回数（濃さの基準）。 */
    function usageMax() {
        if (!usage) return 0;
        return data.edges.reduce((m, e) => Math.max(m, usageCount(e)), 0);
    }

    function drawEdges() {
        svg.replaceChildren();
        const marks = [], counts = [];
        const top = usageMax();
        data.edges.forEach(e => {
            const p = edgePath(e);
            if (!p) return;
            const on = selected?.type === 'edge' && selected.id === e.id;
            // 実際に使われた回数。null は「重ね表示オフ or 未取得」
            const count = usage ? usageCount(e) : null;

            // 当たり判定用の太い透明な線。見える線は細いので、
            // これが無いと1px幅を狙わされて実質クリックできない。
            const hit = document.createElementNS(NS, 'path');
            hit.setAttribute('d', p.d);
            hit.setAttribute('fill', 'none');
            hit.setAttribute('stroke', 'transparent');
            hit.setAttribute('stroke-width', '16');
            hit.style.cursor = 'pointer';
            const tipLines = [];
            if ((e.pairs || []).length > 1) {
                tipLines.push('複合キー: ' + e.pairs.map(pp => `${pp[0]} = ${pp[1]}`).join(' AND '));
            }
            if (count !== null) {
                tipLines.push(count
                    ? `過去の分析で ${count} 回使われた結合`
                    : '過去の分析では一度も使われていない結合（検算されていない経路）');
            }
            if (tipLines.length) {
                const tip = document.createElementNS(NS, 'title');
                tip.textContent = tipLines.join('\n');
                hit.append(tip);
            }
            // pointerdown を止めるのが肝。止めないとキャンバスのパン処理が走り、
            // その中の再描画でこのパス自体が差し替わって click が発火しなくなる。
            hit.addEventListener('pointerdown', ev => ev.stopPropagation());
            hit.addEventListener('click', ev => { ev.stopPropagation(); if (!ro) selectEdge(e); });
            svg.append(hit);

            const path = document.createElementNS(NS, 'path');
            path.setAttribute('d', p.d);
            path.setAttribute('fill', 'none');
            // 太さは使わず、色の濃さで回数を表す。太さを変えると、
            // 線が重なったときにどれが太いのか分からなくなるため。
            // DBまたぎは線の刻み方（破線の長さ）で見分ける。
            path.setAttribute('stroke-width', on ? 2.6 : 1.6);
            if (on) {
                path.setAttribute('stroke', 'var(--accent)');
            } else if (count === null) {
                path.setAttribute('stroke', e.kind === 'fk' ? 'var(--muted)' : 'var(--text)');
            } else {
                // 対数で位置を出す。1回でもはっきり色が付くよう下駄を履かせる
                const t = top > 0 && count > 0
                    ? 0.25 + 0.75 * (Math.log(1 + count) / Math.log(1 + top))
                    : 0;
                path.setAttribute('stroke', ramp(t, '--accent'));
            }
            if (e.kind === 'fk') path.setAttribute('stroke-dasharray', '5 4');
            path.setAttribute('pointer-events', 'none');   // 当たり判定は hit に任せる
            svg.append(path);

            // 多重度は線の両端に置く（IPA表記なので矢印は使わない）
            // 多重度は cardinality（"N:1" など）から組み立てる。
            // ラベル文字列（"* ─ 1"）を切り分ける形だと、区切りが罫線（─ U+2500）
            // なのに ASCII の "-" で切っていて必ず失敗し、
            // どの関連も既定の「* ─ 1」に見えていた（1:N も 1:1 も N:M も同じ形）。
            const [l, r] = String(e.cardinality || 'N:1').split(':')
                .map(x => (x.trim() === '1' ? '1' : '*'));
            marks.push([p.a, l, p.a.x < p.b.x ? 14 : -14, on],
                       [p.b, r, p.b.x > p.a.x ? -14 : 14, on]);

            // 複合キーの線は、列の組で1つの結合だと分かる印を中ほどに置く
            if ((e.pairs || []).length > 1) {
                const bg = document.createElementNS(NS, 'text');
                bg.setAttribute('x', p.mid.x);
                bg.setAttribute('y', p.mid.y - 8);
                bg.setAttribute('text-anchor', 'middle');
                bg.setAttribute('class', 'er__edgelabel' + (on ? ' is-selected' : ''));
                bg.setAttribute('pointer-events', 'none');
                bg.textContent = `複合キー(${e.pairs.length}列)`;
                svg.append(bg);
            }

            // 累積の使用回数を線の中ほどに置く。0 は「一度も検算されていない経路」
            if (count !== null) counts.push([p.mid, count]);
        });

        // 結合候補（未登録）。赤い点線で重ね、クリックで登録カードを開く。
        // 画面に両端が出ている候補だけが描かれる（edgePath が null を返すため）
        if (showSug) suggestions.forEach((sg, i) => {
            const p = edgePath(sg.edge);
            if (!p) return;
            const on = selected?.type === 'sug' && selected.idx === i;
            const hit = document.createElementNS(NS, 'path');
            hit.setAttribute('d', p.d);
            hit.setAttribute('fill', 'none');
            hit.setAttribute('stroke', 'transparent');
            hit.setAttribute('stroke-width', '16');
            hit.style.cursor = 'pointer';
            const tip = document.createElementNS(NS, 'title');
            tip.textContent = `結合の候補（未登録）: ${sg.from} = ${sg.to}`;
            hit.append(tip);
            hit.addEventListener('pointerdown', ev => ev.stopPropagation());
            hit.addEventListener('click', ev => { ev.stopPropagation(); if (!ro) selectSuggestion(i); });
            svg.append(hit);
            const path = document.createElementNS(NS, 'path');
            path.setAttribute('d', p.d);
            path.setAttribute('fill', 'none');
            path.setAttribute('stroke', 'var(--err)');
            path.setAttribute('stroke-width', on ? 2.6 : 1.6);
            path.setAttribute('stroke-dasharray', '3 3');
            path.setAttribute('pointer-events', 'none');
            svg.append(path);
            // 実線と同じIPA表記で多重度を描く（N・Mは「*」）
            const [cl, cr] = String(sg.cardinality || 'N:1').split(':')
                .map(x => (x === '1' ? '1' : '*'));
            marks.push([p.a, cl, p.a.x < p.b.x ? 14 : -14, on, true],
                       [p.b, cr, p.b.x > p.a.x ? -14 : 14, on, true]);
        });
        marks.forEach(([pt, text, dx, on, sug]) => {
            if (!text) return;
            const t = document.createElementNS(NS, 'text');
            t.setAttribute('x', pt.x + dx);
            t.setAttribute('y', pt.y + 4);
            t.setAttribute('text-anchor', 'middle');
            t.setAttribute('class', 'er__edgelabel' + (on ? ' is-selected' : '')
                + (sug ? ' er__edgelabel--sug' : ''));
            t.textContent = text;
            svg.append(t);
        });

        // 使用回数は最後にまとめて描く。線の上に重なるので、
        // 白抜きの座布団を敷いてから数字を置く（細い線の上でも読めるように）
        counts.forEach(([pt, n]) => {
            const label = n ? `${n.toLocaleString()}回` : '未使用';
            // 和文と数字で字幅が倍ほど違うので、文字種ごとに足す
            const w = [...label].reduce((s, c) => s + (/[　-鿿]/.test(c) ? 10.5 : 6), 0) + 10;
            const h = 15;
            const box = document.createElementNS(NS, 'rect');
            box.setAttribute('x', pt.x - w / 2); box.setAttribute('y', pt.y - h / 2);
            box.setAttribute('width', w); box.setAttribute('height', h);
            box.setAttribute('rx', 7);
            box.setAttribute('class', 'er__countbg' + (n ? '' : ' is-zero'));
            svg.append(box);

            const t = document.createElementNS(NS, 'text');
            t.setAttribute('x', pt.x);
            t.setAttribute('y', pt.y + 4);
            t.setAttribute('text-anchor', 'middle');
            t.setAttribute('class', 'er__count' + (n ? '' : ' is-zero'));
            t.textContent = label;
            svg.append(t);
        });
    }

    /** 画面に出すノード。隠したノードへ向かう線は anchor() が null を返すので
        自動的に描かれない（edgePath 側で特別扱いしなくてよい）。 */
    let groupFilter = null;   // 元DBグループ（表名の「__」より前）での絞り込み。null=全部
    let extraShown = new Set(); // まとまり表示に手で足した表（またぎ関連を引くため）
    let suggestions = [];       // 結合候補（列名からの推測）。setSuggestions で受け取る
    let showSug = false;        // 候補の赤線を重ねるか
    let sugOnlyIds = new Set(); // 候補のためだけに画面へ出している表（赤枠で描く）
    function shownNodes() {
        if (!groupFilter) return data.nodes;
        const ids = new Set(data.nodes
            .filter(n => String(n.table || '').split('__')[0] === groupFilter)
            .map(n => n.id));
        // 関連で繋がっている「隣のまとまりの表」も一緒に出す。
        // 出さないと、まとまりをまたぐ関連が見えず、この表示からは消せも引けもしない
        const extra = new Set();
        (data.edges || []).forEach(e => {
            const f = `${e.from[0]}.${e.from[1]}`, t = `${e.to[0]}.${e.to[1]}`;
            if (ids.has(f) && !ids.has(t)) extra.add(t);
            if (ids.has(t) && !ids.has(f)) extra.add(f);
        });
        // 候補を表示中は、候補の相手（まだ画面に居ない表）も赤枠で出す。
        // 出さないと、またぎの候補が1本も見えない
        sugOnlyIds = new Set();
        if (showSug) {
            const base = new Set([...ids, ...extra, ...extraShown]);
            suggestions.forEach(sg2 => {
                const f = `${sg2.edge.from[0]}.${sg2.edge.from[1]}`;
                const t = `${sg2.edge.to[0]}.${sg2.edge.to[1]}`;
                if (base.has(f) && !base.has(t)) sugOnlyIds.add(t);
                if (base.has(t) && !base.has(f)) sugOnlyIds.add(f);
            });
        }
        return data.nodes.filter(n => ids.has(n.id) || extra.has(n.id)
                                      || extraShown.has(n.id) || sugOnlyIds.has(n.id));
    }

    function render() {
        world.replaceChildren(...shownNodes().map(tableEl));
        // 隣のまとまりから来ている表は、見た目で区別する（枠を破線に）
        if (groupFilter) {
            $$('.ertable', world).forEach(b => {
                if (sugOnlyIds.has(b.dataset.id)) {
                    b.classList.add('ertable--sug');
                    b.title = '結合候補の相手（候補を隠すと消えます）';
                    return;
                }
                const n = data.nodes.find(x => x.id === b.dataset.id);
                if (n && String(n.table || '').split('__')[0] !== groupFilter) {
                    b.classList.add('ertable--other');
                    b.title = '別のまとまりの表（関連で繋がっているため表示）';
                }
            });
        }
        wireNodes();
        drawEdges();
        applyView();
    }

    /* --- 選択パネル ------------------------------------------------------------ */

    function closePanel() {
        selected = null; panel.classList.add('hidden');
        panel.classList.remove('er__panel--wide', 'er__panel--max');
        drawEdges(); syncSelection();
    }

    /* パネルの見出し（タイトル・最大化・閉じる）。3種類のパネルで同じ形にする。 */
    function panelHead(title, extra) {
        const maxBtn = el('button', { class: 'btn btn--sm btn--ghost', title: '最大化' });
        const syncMax = () => {
            const on = panel.classList.contains('er__panel--max');
            maxBtn.replaceChildren(icon(on ? 'minimize' : 'maximize', 'icon--sm'));
            maxBtn.title = on ? '元の大きさに戻す' : '最大化';
        };
        maxBtn.addEventListener('click', () => {
            panel.classList.toggle('er__panel--max');
            syncMax();
        });
        syncMax();
        return el('div', { class: 'row', style: 'align-items:center;flex:0 0 auto' },
            el('b', { class: 'grow' }, title),
            extra || null,
            maxBtn,
            el('button', { class: 'btn btn--sm btn--ghost', title: '閉じる',
                           onclick: closePanel }, icon('x', 'icon--sm')));
    }

    /* パネルを出す。中身は本文コンテナに入れ、境目に取っ手を付ける。
       ドラッグで決めた大きさ（width/height）は次に開くときも保つ。 */
    function showPanel(title, bodyChildren, opts) {
        panel.classList.remove('hidden');
        panel.classList.toggle('er__panel--wide', !!(opts && opts.wide));
        panel.classList.remove('er__panel--max');
        const body = el('div', { class: 'er__panel__body' }, ...(bodyChildren || []));
        panel.replaceChildren(
            el('div', { class: 'er__grip er__grip--l' }),
            el('div', { class: 'er__grip er__grip--t' }),
            el('div', { class: 'er__grip er__grip--tl' }),
            panelHead(title, opts && opts.extra),
            body);
        wirePanelResize();
        return body;
    }

    /* 左辺・上辺・左上の角をつまんで大きさを変える。パネルは右下に付いているので、
       左へ引けば広く、上へ引けば高くなる。 */
    function wirePanelResize() {
        panel.querySelectorAll('.er__grip').forEach(g => {
            g.addEventListener('pointerdown', ev => {
                ev.preventDefault(); ev.stopPropagation();
                const dirL = g.classList.contains('er__grip--l') || g.classList.contains('er__grip--tl');
                const dirT = g.classList.contains('er__grip--t') || g.classList.contains('er__grip--tl');
                const r = panel.getBoundingClientRect();
                const sx = ev.clientX, sy = ev.clientY, w0 = r.width, h0 = r.height;
                const vp = viewport.getBoundingClientRect();
                const move = e2 => {
                    if (dirL) {
                        const w = Math.max(280, Math.min(vp.width - 20, w0 + (sx - e2.clientX)));
                        panel.style.width = `${w}px`;
                    }
                    if (dirT) {
                        const h = Math.max(160, Math.min(vp.height - 20, h0 + (sy - e2.clientY)));
                        panel.style.height = `${h}px`;
                        panel.style.maxHeight = 'none';
                    }
                };
                const up = () => {
                    document.removeEventListener('pointermove', move);
                    document.removeEventListener('pointerup', up);
                };
                document.addEventListener('pointermove', move);
                document.addEventListener('pointerup', up);
            });
        });
    }

    function syncSelection() {
        world.querySelectorAll('.ertable').forEach(b =>
            b.classList.toggle('is-selected', selected?.type === 'table' && selected.id === b.dataset.id));
    }

    function selectSuggestion(i) {
        const sg = suggestions[i];
        selected = { type: 'sug', idx: i };
        drawEdges(); syncSelection();
        const [ft, fc] = sg.from.split('.');
        const [tt, tc] = sg.to.split('.');
        showPanel('結合の候補（未登録）', [
            el('div', { class: 'small mono mb' }, `${sg.from}\n${sg.to}`),
            el('div', { class: 'small muted mb' }, `推測の根拠: ${sg.reason || ''}`),
            el('div', { class: 'small muted mb' },
                `多重度: ${sg.cardinality}（${CARD_JA[sg.cardinality] || ''}。登録後に変更できます）`),
            el('div', { class: 'alert alert--info small mb' },
                'まだ登録されていない推測です。登録すると実データで妥当性を確かめたうえで、'
                + 'AIがJOINに使う関連になります。'),
            el('div', { class: 'row' },
                el('button', { class: 'btn btn--sm btn--primary', onclick: async () => {
                    await mutate({ action: 'add', from_table: ft, from_column: fc,
                                   to_table: tt, to_column: tc, cardinality: sg.cardinality });
                    // 登録できたか（実データ検証で止まらなかったか）は edges で確かめる
                    const okNow = data.edges.some(e2 =>
                        e2.from[1] === ft && e2.from[2] === fc
                        && e2.to[1] === tt && e2.to[2] === tc);
                    if (okNow) {
                        suggestions.splice(i, 1);
                        syncSugBtn();
                        toast('関連を登録しました。');
                        closePanel();
                    }
                } }, 'この結合を登録'),
                el('button', { class: 'btn btn--sm btn--ghost', onclick: () => {
                    suggestions.splice(i, 1);
                    syncSugBtn();
                    closePanel();
                    toast('この候補を隠しました（次にカタログを開くとまた提案されます）。');
                } }, '候補から外す'),
                el('div', { class: 'spacer' }),
                el('button', { class: 'btn btn--sm btn--ghost', onclick: closePanel }, '閉じる')),
        ]);
    }

    function selectEdge(e) {
        selected = { type: 'edge', id: e.id, edge: e };
        drawEdges(); syncSelection();
        const comp = (e.pairs || []).length > 1;
        showPanel(comp ? '関連（複合キー）' : '関連', [
            el('div', { class: 'small mono mb' },
                `${e.from_ref || e.from.join('.')}\n${e.to_ref || e.to.join('.')}`),
            comp ? el('div', { class: 'alert alert--info small mb' },
                `${e.pairs.length}列の組で1つの結合です。JOINでは全列を同時に条件にします: `
                + e.pairs.map(pp => `${pp[0]} = ${pp[1]}`).join(' AND ')) : null,
            e.kind === 'fk'
                ? el('div', { class: 'alert alert--info small' },
                    'DBに FOREIGN KEY として宣言された関連です。ここからは変更・削除できません。')
                : !e.editable
                ? el('div', { class: 'alert alert--info small' },
                    `この関連は ${e.owner} 側で管理されています。`
                    + `変更するには、右上のプルダウンで ${e.owner} に切り替えてください。`)
                : el('div', {},
                    el('div', { class: 'small muted mb' },
                        `多重度（現在 ${e.cardinality}＝${CARD_JA[e.cardinality] || ''}）`),
                    el('div', { class: 'row mb' }, CARDS.map(c =>
                        el('button', {
                            class: 'btn btn--sm' + (c === e.cardinality ? ' btn--primary' : ''),
                            title: CARD_JA[c],
                            // index ではなく from/to で指す。表やビューを消すと
                            // 関連の配列が詰まり、index は別の関連を指してしまう
                            onclick: () => mutate({ action: 'update', index: e.index,
                                                    from: e.from_ref, to: e.to_ref,
                                                    cardinality: c }),
                        }, `${c}（${CARD_JA[c]}）`))),
                    comp ? el('div', { class: 'mb' },
                        el('div', { class: 'small muted mb' },
                            '列の組（「外す」でその列だけ複合キーから抜けます）'),
                        ...e.pairs.map(pp => el('div', { class: 'row mb', style: 'gap:6px;align-items:center' },
                            el('span', { class: 'small mono grow' }, `${pp[0]} = ${pp[1]}`),
                            el('button', { class: 'btn btn--sm btn--ghost',
                                onclick: () => mutate({ action: 'remove_pair',
                                                        from: e.from_ref, to: e.to_ref,
                                                        pair: pp }) }, '外す')))) : null,
                    el('button', {
                        class: 'btn btn--sm btn--danger',
                        onclick: () => { if (confirm(comp ? 'この関連を（全列まとめて）削除しますか？'
                                                          : 'この関連を削除しますか？'))
                            // index は配列が詰まるとずれる。保存済みの from/to を添えて、
                            // サーバ側でそちらを優先して探させる
                            mutate({ action: 'delete', index: e.index,
                                     from: e.from_ref, to: e.to_ref }); },
                    }, comp ? '関連ごと削除' : '削除'))]);
    }

    function selectTable(id) {
        const n = data.nodes.find(x => x.id === id);
        if (!n) return;
        selected = { type: 'table', id };
        drawEdges(); syncSelection();
        // 概要・列の説明・実値・サンプル行を取りに行く（描画用の図には入れていない）。
        // 主キーの編集はカタログ画面だけ（読み取り専用のチャットでは出さない）。
        const rowsBadge = (n.rows !== null && n.rows !== undefined)
            ? el('span', { class: 'muted small', style: 'margin-right:6px' },
                 `${Number(n.rows).toLocaleString()}行`) : null;
        const body = el('div', { class: 'small muted' }, el('span', { class: 'spinner' }), ' 読み込み中...');
        showPanel(`${n.table}`, [body], { wide: true, extra: rowsBadge });

        api(`/api/catalog/table-info?db=${encodeURIComponent(n.alias)}&table=${encodeURIComponent(n.table)}`,
            undefined, 'GET').then(info => {
            if (selected?.id !== id) return;          // 読んでいる間に別のものを選んだ
            body.replaceChildren(...describeParts(info, n));
        }).catch(e => {
            body.replaceChildren(el('div', { class: 'alert alert--err small' }, e.message));
        });
    }

    /** テーブルの中身（概要・列・サンプル行・主キー編集）。パネルの中身を作る。 */
    function describeParts(info, n) {
        const parts = [];
        parts.push(el('div', { class: 'small', style: 'margin:6px 0 8px' },
            info.description
                ? el('span', {}, info.description,
                    info.ai_draft ? el('span', { class: 'badge badge--accent', style: 'margin-left:6px' }, 'AI下書き') : null)
                : el('span', { class: 'muted' }, '説明はまだ書かれていません。')));

        // 列（型・PK・説明・実際の値）
        const rows = (info.columns || []).map(c => el('tr', {},
            el('td', {}, c.name, c.pk ? el('span', { class: 'badge', style: 'margin-left:4px' }, 'PK') : null),
            el('td', { class: 'muted' }, c.type),
            el('td', {}, c.description || el('span', { class: 'muted' }, '—')),
            el('td', { class: 'muted', title: c.actual }, c.actual || '')));
        parts.push(el('div', { class: 'tablewrap', style: 'max-height:200px' },
            el('table', { class: 'data' },
                el('thead', {}, el('tr', {}, ['列', '型', '説明', '実際の値'].map(h => el('th', {}, h)))),
                el('tbody', {}, rows))));

        // 用語（このテーブル固有）
        const gl = Object.entries(info.glossary || {});
        if (gl.length) {
            parts.push(el('div', { class: 'small', style: 'margin-top:8px' },
                el('b', {}, '業務用語: '),
                gl.map(([t, e]) => `${t}（${e.description || e.sql || ''}）`).join('、')));
        }

        // サンプル行（全体は別タブのビューアで見る）
        if ((info.sample_rows || []).length) {
            parts.push(el('div', { class: 'row', style: 'align-items:center;margin:8px 0 2px' },
                el('span', { class: 'small muted' }, 'サンプル行'),
                el('div', { class: 'spacer' }),
                tableViewLink(info.alias || info.db, info.table)));
            parts.push(el('div', { class: 'tablewrap', style: 'max-height:160px' },
                dataTable(info.sample_columns || [], info.sample_rows || [])));
        }

        // 主キーの編集（カタログ画面だけ。読み取り専用では出さない）
        if (!ro) {
            const checks = n.columns.map(c => el('label',
                { style: 'display:flex;gap:6px;align-items:center;font-size:12px' },
                el('input', { type: 'checkbox', 'data-pk': c.name, ...(c.pk ? { checked: 'checked' } : {}) }),
                c.name));
            parts.push(el('details', { class: 'mt' },
                el('summary', { class: 'small muted', style: 'cursor:pointer' }, '主キーを直す（鍵＝実線の下線）'),
                el('div', { style: 'max-height:150px;overflow:auto;margin:6px 0' }, checks),
                el('button', {
                    class: 'btn btn--primary btn--sm',
                    onclick: async () => {
                        const cols = [...panel.querySelectorAll('[data-pk]')]
                            .filter(c => c.checked).map(c => c.dataset.pk);
                        const before = n.columns.filter(c => c.pk).map(c => c.name);
                        try {
                            await pkApi(n.table, cols);
                            closePanel(); toast('主キーを保存しました。');
                            record({ label: `${n.table} の主キーを変更`,
                                     undo: () => pkApi(n.table, before),
                                     redo: () => pkApi(n.table, cols) });
                        } catch (e) { toast(e.message, 'err'); }
                    },
                }, '主キーを保存')));
        }
        return parts;
    }

    /* --- 変更（サーバに保存して描き直す） ---------------------------------------- */

    /* --- 履歴 ---------------------------------------------------------------- */

    function record(entry) {
        past.push(entry);
        if (past.length > HIST_MAX) past.shift();
        future = [];                      // 新しい操作をしたら「やり直す」先は消える
        syncHistoryUi();
    }

    async function undo() {
        const e = past.pop();
        if (!e) return;
        try { await e.undo(); future.push(e); toast(`元に戻しました: ${e.label}`); }
        catch (err) { toast(`元に戻せませんでした: ${err.message}`, 'err'); }
        syncHistoryUi();
    }

    async function redo() {
        const e = future.pop();
        if (!e) return;
        try { await e.redo(); past.push(e); toast(`やり直しました: ${e.label}`); }
        catch (err) { toast(`やり直せませんでした: ${err.message}`, 'err'); }
        syncHistoryUi();
    }

    function layoutSnapshot() {
        return JSON.stringify(data.nodes.map(n => [n.id, Math.round(n.x), Math.round(n.y)]).sort());
    }

    /* ボタンの活性と、次に戻す／やり直す操作名をツールチップに出す */
    function syncHistoryUi() {
        const u = $('#erUndo'), r = $('#erRedo'), sv = $('#erSave');
        if (u) {
            u.disabled = !past.length;
            u.dataset.tip = past.length ? `元に戻す（Ctrl+Z）: ${past[past.length - 1].label}`
                                        : '元に戻す（Ctrl+Z）\nまだ操作していません。';
        }
        if (r) {
            r.disabled = !future.length;
            r.dataset.tip = future.length ? `やり直す（Ctrl+Y）: ${future[future.length - 1].label}`
                                          : 'やり直す（Ctrl+Y）\n戻した操作はありません。';
        }
        if (sv) {
            const dirty = layoutSnapshot() !== savedLayout;
            sv.disabled = !dirty;
            sv.dataset.tip = dirty ? '配置を保存（Ctrl+S）\nテーブルの位置に、保存していない変更があります。'
                                   : '配置を保存（Ctrl+S）\nテーブルの位置は保存済みです。関連・主キーなどは操作した時点で保存されています。';
        }
    }

    function setPos(id, pos) {
        const n = data.nodes.find(x => x.id === id);
        if (n) { n.x = pos.x; n.y = pos.y; }
        render(); syncHistoryUi();
    }

    /** サーバから返ってきた図を反映する。画面上の位置は動かさない
        （まだ保存していない配置を、関連を1本足しただけで捨てないため）。 */
    function applyEr(er) {
        if (!er || !er.nodes) return;   // 図データを伴わない応答では触らない
        const positions = Object.fromEntries(data.nodes.map(n => [n.id, [n.x, n.y]]));
        data = er;
        data.nodes.forEach(n => { if (positions[n.id]) [n.x, n.y] = positions[n.id]; });
        render(); syncHistoryUi();
        refreshSuggestions();
    }

    /** 候補を取り直す。関連の追加・削除・主キー変更のたびに呼ぶ。
        消した関連はすぐ候補に戻り、引いた関連の候補線はすぐ消える。 */
    async function refreshSuggestions() {
        if (typeof CAT === 'undefined' || ro) return;
        try {
            const r = await api(`/api/catalog/suggestions?db=${encodeURIComponent(CAT.db)}`,
                                undefined, 'GET');
            if (selected?.type === 'sug') closePanel();   // 番号がずれるので開き直してもらう
            setSuggestions(r.suggestions || []);
            render();                        // 候補の相手テーブルが出入りする
        } catch (e) { /* 取れなくても既存の表示で困らない */ }
    }

    /* 関連API を1回叩いて図を反映する（履歴には積まない。undo/redo からも使う） */
    async function relApi(body) {
        const r = await api('/api/catalog/relationship', { db: CAT.db, ...body });
        // 保存せずに聞き返す応答（実データ判定で停止／複合キーの合流確認）には
        // 図データが入らない。ここで返さないと図を空で置き換えて壊してしまう
        if (r.check || r.ask) return r;
        applyEr(r.er); closePanel();
        return r;
    }

    /* 人の操作から呼ぶ。サーバに保存したうえで、逆の操作を履歴に積む */
    async function mutate(body) {
        try {
            const r = await relApi(body);
            // 同じ表ペアに既存の関連がある。複合キーに合流するか、別の関連かを人に選ばせる
            if (r.ask === 'merge_or_new') { showMergeAsk(r, body); return; }
            // 実データを見て「結ぶべきでない／要確認」と判定されたら、理由を出して止める
            if (r.check) { showLinkCheck(r, body); return; }
            if (body.action === 'add' && r.added) {
                const a = r.added;
                record({ label: `関連を追加（${a.from} → ${a.to}）`,
                         undo: () => relApi({ action: 'delete', from: a.from, to: a.to }),
                         // 一度通した線なので、やり直しでは確認（warn）を飛ばす。block は元々通らない
                         redo: () => relApi({ action: 'add', from: a.from, to: a.to,
                                              cardinality: a.cardinality, force: true }) });
            } else if (r.merged) {
                const m = r.merged;
                record({ label: `複合キーに列を追加（${m.pair[0]} = ${m.pair[1]}）`,
                         undo: () => relApi({ action: 'remove_pair', from: m.from, to: m.to, pair: m.pair }),
                         redo: () => relApi({ action: 'add', ...m.add_body, mode: 'merge', force: true }) });
            } else if (r.pair_removed) {
                const m = r.pair_removed;
                record({ label: `複合キーから列を外す（${m.pair[0]} = ${m.pair[1]}）`,
                         undo: () => relApi({ action: 'add', ...m.add_body, mode: 'merge', force: true }),
                         redo: () => relApi({ action: 'remove_pair', from: m.from, to: m.to, pair: m.pair }) });
            } else if ((body.action === 'delete' || body.action === 'remove_pair') && r.removed) {
                const a = r.removed;
                record({ label: `関連を削除（${a.from} → ${a.to}）`,
                         undo: () => relApi({ action: 'add', from: a.from, to: a.to,
                                              cardinality: a.cardinality, force: true }),
                         redo: () => relApi({ action: 'delete', from: a.from, to: a.to }) });
            } else if (body.action === 'update' && r.updated) {
                const a = r.updated;
                record({ label: `多重度を ${a.previous} → ${a.cardinality}（${a.from}）`,
                         undo: () => relApi({ action: 'update', from: a.from, to: a.to, cardinality: a.previous }),
                         redo: () => relApi({ action: 'update', from: a.from, to: a.to, cardinality: a.cardinality }) });
            }
        } catch (e) { toast(e.message, 'err'); }
    }

    async function pkApi(table, columns) {
        const r = await api('/api/catalog/primary-key', { db: CAT.db, table, columns });
        applyEr(r.er);
        return r;
    }

    /* 線を引いた先が結べない／結ぶべきでないときのパネル。
       なぜだめかを実データの数字つきで並べる。警告どまりなら「それでも登録する」を出す。
       ER図の線は「この列で JOIN してよい」というAIへの指示なので、成立しない線を
       黙って登録させない。 */
    function showMergeAsk(r, body) {
        const ex = (r.existing || [])[0] || {};
        showPanel('複合キーにしますか？', [
            el('div', { class: 'small mono mb' }, `${r.from}\n${r.to}`),
            el('div', { class: 'small muted mb' },
                'この2つのテーブルの間には、すでに関連があります: '
                + (ex.pairs || []).map(pp => `${pp[0]} = ${pp[1]}`).join(' AND ')),
            el('div', { class: 'alert alert--info small mb' },
                '複合キー（複数列の組で1つの結合。JOINで全列を同時に条件にする）なら'
                + '「列を追加」を、意味の異なる独立した結合なら「別の関連」を選んでください。'),
            el('div', { class: 'row', style: 'gap:8px;flex-wrap:wrap' },
                el('button', { class: 'btn btn--sm btn--primary',
                    onclick: () => mutate({ ...body, mode: 'merge' }) }, '複合キーとして列を追加'),
                el('button', { class: 'btn btn--sm',
                    onclick: () => mutate({ ...body, mode: 'new' }) }, '別の関連として登録'),
                el('div', { class: 'spacer' }),
                el('button', { class: 'btn btn--sm btn--ghost', onclick: closePanel }, 'やめる')),
        ]);
    }

    function showLinkCheck(r, body) {
        const check = r.check;
        const blocked = check.level === 'block';
        const LV = { block: ['alert--err', '結べません'],
                     warn:  ['alert--warn', '確認してください'],
                     info:  ['alert--info', '参考'] };
        const items = check.issues.map(i => {
            const [cls, label] = LV[i.level] || LV.info;
            return el('div', { class: `alert ${cls} small`, style: 'margin:6px 0' },
                el('div', {}, el('b', {}, i.title), ' ', el('span', { class: 'muted' }, `（${label}）`)),
                el('div', { style: 'margin-top:3px' }, i.detail));
        });
        const buttons = el('div', { class: 'row mt', style: 'gap:8px;justify-content:flex-end' },
            el('button', { class: 'btn btn--sm', onclick: closePanel }, blocked ? '閉じる' : 'やめる'),
            blocked ? null
                    : el('button', { class: 'btn btn--sm btn--primary',
                                     onclick: () => mutate({ ...body, force: true }) },
                         'それでも登録する'));
        showPanel(blocked ? 'この線は結べません' : 'この線でよいですか？', [
            el('div', { class: 'small mono mb' }, `${r.from} → ${r.to}（${r.cardinality}）`),
            el('div', { class: 'small muted' },
                blocked
                    ? '実データを見ると、この2列で JOIN しても結果が出ません。列の選び間違いです。'
                    : '実データを見ると気になる点があります。意味を確かめてから登録してください。'),
            ...items,
            el('div', { class: 'small muted mt' },
                'ER図の線は「この列で結合してよい」というAIへの指示です。' +
                '成立しない線を引くと、AIが自信を持って間違った結合を書くようになります。'),
            buttons,
        ], { wide: true });
    }

    /* --- 操作 ------------------------------------------------------------------ */

    function wireNodes() {
        world.querySelectorAll('.ertable').forEach(box => {
            const node = data.nodes.find(n => n.id === box.dataset.id);

            $('.ertable__head', box).addEventListener('pointerdown', ev => {
                ev.stopPropagation();
                const sx = ev.clientX, sy = ev.clientY, ox = node.x, oy = node.y;
                let moved = false;
                const move = e2 => {
                    node.x = ox + (e2.clientX - sx) / view.k;
                    node.y = oy + (e2.clientY - sy) / view.k;
                    box.style.left = `${node.x}px`; box.style.top = `${node.y}px`;
                    moved = true; drawEdges();
                };
                const up = () => {
                    document.removeEventListener('pointermove', move);
                    document.removeEventListener('pointerup', up);
                    if (!moved) { selectTable(node.id); return; }   // 読み取り専用でも中身は見られる
                    // 動かし終わった位置を1手として積む（クリックだけなら積まない）
                    const before = { x: ox, y: oy }, after = { x: node.x, y: node.y };
                    record({ label: `${node.table} を移動`,
                             undo: () => setPos(node.id, before),
                             redo: () => setPos(node.id, after) });
                };
                document.addEventListener('pointermove', move);
                document.addEventListener('pointerup', up);
            });

            if (!ro) box.querySelectorAll('.erhandle').forEach(h => {
                h.addEventListener('pointerdown', ev => {
                    ev.stopPropagation(); ev.preventDefault();
                    startLink(node, h.dataset.handle, h.dataset.side, ev);
                });
            });
        });
    }

    function startLink(fromNode, fromCol, side, ev) {
        const ghost = document.createElementNS(NS, 'path');
        ghost.setAttribute('fill', 'none');
        ghost.setAttribute('stroke', 'var(--accent)');
        ghost.setAttribute('stroke-width', '2');
        ghost.setAttribute('stroke-dasharray', '5 4');
        svg.append(ghost);
        const a = anchor(fromNode.id, fromCol, side || 'right');
        const out = (side === 'left') ? -60 : 60;

        const toWorld = e => {
            const r = viewport.getBoundingClientRect();
            return { x: (e.clientX - r.left - view.tx) / view.k, y: (e.clientY - r.top - view.ty) / view.k };
        };
        const move = e2 => {
            const p = toWorld(e2);
            ghost.setAttribute('d',
                `M ${a.x} ${a.y} C ${a.x + out} ${a.y}, ${p.x - out} ${p.y}, ${p.x} ${p.y}`);
        };
        const up = e2 => {
            document.removeEventListener('pointermove', move);
            document.removeEventListener('pointerup', up);
            ghost.remove();
            const target = document.elementFromPoint(e2.clientX, e2.clientY)?.closest('.ercol');
            const box = target?.closest('.ertable');
            if (!target || !box) return;
            const toNode = data.nodes.find(n => n.id === box.dataset.id);
            if (toNode.id === fromNode.id && target.dataset.col === fromCol) return;
            mutate({
                action: 'add',
                from_table: fromNode.table, from_column: fromCol,
                to_table: toNode.table, to_column: target.dataset.col,
                cardinality: guessCardinality(fromNode, fromCol, toNode, target.dataset.col),
            });
        };
        document.addEventListener('pointermove', move);
        document.addEventListener('pointerup', up);
    }

    /** 「その列がそのテーブルの主キー全体なら 1 側」という規則で多重度を推定する。 */
    function guessCardinality(fromNode, fromCol, toNode, toCol) {
        const solePk = (node, col) => {
            const pks = node.columns.filter(c => c.pk).map(c => c.name);
            return pks.length === 1 && pks[0] === col;
        };
        const a = solePk(fromNode, fromCol), b = solePk(toNode, toCol);
        if (a && b) return '1:1';
        if (b) return 'N:1';
        if (a) return '1:N';
        return 'N:M';
    }


    function wireViewport() {
        // init は表の削除などで何度も呼ばれる。要素に印を付けて1回だけ張る
        // （フラグ1本にすると、要素ごと作り直すチャット側で張られなくなる）
        if (viewport.dataset.wired) return;
        viewport.dataset.wired = '1';
        viewport.addEventListener('pointerdown', ev => {
            if (ev.target.closest('.ertable') || ev.target.closest('.er__panel')) return;
            closePanel();
            const sx = ev.clientX, sy = ev.clientY, ox = view.tx, oy = view.ty;
            viewport.classList.add('is-panning');
            const move = e2 => { view.tx = ox + (e2.clientX - sx); view.ty = oy + (e2.clientY - sy); applyView(); };
            const up = () => {
                viewport.classList.remove('is-panning');
                document.removeEventListener('pointermove', move);
                document.removeEventListener('pointerup', up);
            };
            document.addEventListener('pointermove', move);
            document.addEventListener('pointerup', up);
        });

        viewport.addEventListener('wheel', ev => {
            ev.preventDefault();
            const r = viewport.getBoundingClientRect();
            const mx = ev.clientX - r.left, my = ev.clientY - r.top;
            const k2 = Math.min(2.5, Math.max(0.2, view.k * (ev.deltaY < 0 ? 1.12 : 0.89)));
            view.tx = mx - (mx - view.tx) * (k2 / view.k);
            view.ty = my - (my - view.ty) * (k2 / view.k);
            view.k = k2;
            applyView();
        }, { passive: false });
    }

    function fit() {
        const nodes = shownNodes();
        if (!nodes.length) return;
        const boxes = nodes.map(n => {
            const b = world.querySelector(`.ertable[data-id="${CSS.escape(n.id)}"]`);
            return { x: n.x, y: n.y, w: b?.offsetWidth || 232, h: b?.offsetHeight || 120 };
        });
        const minX = Math.min(...boxes.map(b => b.x)), minY = Math.min(...boxes.map(b => b.y));
        const maxX = Math.max(...boxes.map(b => b.x + b.w)), maxY = Math.max(...boxes.map(b => b.y + b.h));
        const r = viewport.getBoundingClientRect();
        // 下限0.05: 100表を超える全体表示でも一応ひと目で収まるように
        view.k = Math.min(1.2, Math.max(0.05,
            Math.min((r.width - 80) / (maxX - minX), (r.height - 80) / (maxY - minY))));
        view.tx = 40 - minX * view.k;
        view.ty = 40 - minY * view.k;
        applyView();
    }

    async function saveLayout() {
        if (ro) return;
        const snap = layoutSnapshot();
        if (snap === savedLayout) { toast('配置は保存済みです。'); return; }
        const layout = Object.fromEntries(data.nodes.map(n => [n.id, [Math.round(n.x), Math.round(n.y)]]));
        try {
            await api('/api/catalog/layout', { db: CAT.db, layout });
            savedLayout = snap; syncHistoryUi();
            toast('配置を保存しました。');
        } catch (e) { toast(e.message, 'err'); }
    }

    function init(opts) {
        root = $('#erRoot'); viewport = $('#erViewport');
        world = $('#erWorld'); svg = $('#erSvg'); panel = $('#erPanel');
        if (!root) return;
        ro = !!(opts && opts.readonly);
        data = (opts && opts.data) || (typeof CAT !== 'undefined' ? CAT.er : null);
        if (!data) return;
        // チャットでは開くたびに init し直すので、前回の状態を持ち越さない
        view = { tx: 40, ty: 40, k: 1 };
        selected = null; past = []; future = []; groupFilter = null;
        // 元DBグループの絞り込み（カタログ画面のみ。表が多いときは最初の
        // グループを初期表示にして「114表の壁」を避ける）
        const gsel = $('#erGroup');
        if (gsel && !ro) {
            if (!gsel.dataset.wired) {
                gsel.dataset.wired = '1';
                gsel.addEventListener('change', () => {
                    groupFilter = gsel.value || null;
                    extraShown.clear();          // 足した表はまとまりごとの一時的なもの
                    syncAddBtn();
                    render(); setTimeout(fit, 20);
                });
            }
            if (data.nodes.length > 30 && gsel.options.length > 1) {
                gsel.selectedIndex = 1;
            }
            groupFilter = gsel.value || null;
        }
        extraShown.clear();
        syncAddBtn();
        svg.setAttribute('width', '100%'); svg.setAttribute('height', '100%');
        render();
        savedLayout = layoutSnapshot();      // 読み込んだ配置＝保存済みとみなす
        syncHistoryUi();
        wireViewport();
        setTimeout(fit, 30);

        // ツールバーも1回だけ張る。init は表の削除のたびに走るので、
        // 素直に addEventListener すると同じ操作が2回ずつ動く
        // （結合候補は2回反転して元に戻り、保存は2回POSTされる）
        const once = (sel, fn) => {
            const b = $(sel);
            if (!b || b.dataset.wired) return;
            b.dataset.wired = '1';
            b.addEventListener('click', fn);
        };
        once('#erSave', saveLayout);
        once('#erAddTable', ev => { ev.stopPropagation(); openAddTable(); });
        once('#erSuggest', () => {
            showSug = !showSug;
            if (selected?.type === 'sug') closePanel();
            syncSugBtn();
            render();                       // 候補の相手テーブルが出入りする
            setTimeout(fit, 20);
        });
        once('#erUndo', undo);
        once('#erRedo', redo);
        once('#erFull', () => {
            root.classList.toggle('er--full');
            $('#erFull').textContent = root.classList.contains('er--full') ? '全画面を終了' : '全画面';
            setTimeout(fit, 60);
        });
        if (!docWired) {
            docWired = true;
            // root は init のたびに差し替わるので、この1本のハンドラで常に最新を見る
            document.addEventListener('keydown', ev => {
                if (ev.key === 'Escape' && root && root.classList.contains('er--full')) {
                    $('#erFull')?.click();
                    return;
                }
                // Ctrl+Z / Ctrl+Y(Ctrl+Shift+Z) / Ctrl+S は、ER図が見えていて
                // 入力欄にいないときだけ受ける（他のタブやチャットでは横取りしない）
                if (ro || !root || !(ev.ctrlKey || ev.metaKey)) return;
                if (!root.getClientRects().length) return;                    // 別タブで隠れている
                if (/INPUT|TEXTAREA|SELECT/.test(ev.target.tagName) || ev.target.isContentEditable) return;
                const k = ev.key.toLowerCase();
                if (k === 'z' && !ev.shiftKey) { ev.preventDefault(); undo(); }
                else if (k === 'y' || (k === 'z' && ev.shiftKey)) { ev.preventDefault(); redo(); }
                else if (k === 's') { ev.preventDefault(); saveLayout(); }
            });
        }
    }

    function syncSugBtn() {
        const b = $('#erSuggest');
        if (!b) return;
        b.textContent = suggestions.length ? `結合候補(${suggestions.length})` : '結合候補';
        b.disabled = !suggestions.length;
        b.classList.toggle('btn--primary', showSug && suggestions.length > 0);
    }

    /** 結合候補を受け取る（カタログ画面が読み込み時に呼ぶ）。 */
    function setSuggestions(list) {
        const alias = data?.nodes?.[0]?.alias;
        suggestions = (list || []).map(sg => {
            const [ft, fc] = String(sg.from).split('.');
            const [tt, tc] = String(sg.to).split('.');
            return { ...sg, edge: { from: [alias, ft, fc], to: [alias, tt, tc] } };
        });
        syncSugBtn();
    }

    /** まとまり表示では意味があるが、「すべて」表示では足す必要が無い。 */
    function syncAddBtn() {
        const b = $('#erAddTable');
        if (b) b.style.display = groupFilter ? '' : 'none';
    }

    /* 「＋ 別のまとまりの表」。104表を全部出さずに、相手の表だけを1つずつ
       画面に足して、またぎの関連を引けるようにする。 */
    let addPop = null;

    function closeAddPop() {
        addPop?.remove(); addPop = null;
        document.removeEventListener('click', closeAddPop);
    }

    function openAddTable() {
        closeAddPop();
        const shown = new Set(shownNodes().map(n => n.id));
        const cands = data.nodes.filter(n => !shown.has(n.id))
            .sort((a, b) => String(a.table).localeCompare(String(b.table), 'ja'));
        const list = el('div', { class: 'qa-pop__list' });
        const renderList = (needle = '') => {
            list.replaceChildren(...cands
                .filter(n => !needle || String(n.table).toLowerCase().includes(needle))
                .map(n => el('button', { class: 'mlist__item', onclick: () => {
                    extraShown.add(n.id);
                    render(); setTimeout(fit, 20);
                    closeAddPop();
                } }, el('span', { class: 'mlist__desc' }, n.table))));
            if (!list.children.length) {
                list.append(el('div', { class: 'small muted' }, '一致する表がありません。'));
            }
        };
        const search = el('input', { type: 'text', placeholder: '表の名前で絞り込み',
            oninput: () => renderList(search.value.trim().toLowerCase()) });
        renderList();
        const added = [...extraShown].map(id => data.nodes.find(n => n.id === id)).filter(Boolean);
        addPop = el('div', { class: 'qa-pop', onclick: ev => ev.stopPropagation() },
            search,
            ...(added.length ? [
                el('div', { class: 'small muted mt' }, '足した表（クリックで外す）'),
                el('div', {}, ...added.map(n => el('button', {
                    class: 'btn btn--sm btn--ghost',
                    onclick: () => { extraShown.delete(n.id); render(); closeAddPop(); },
                }, `✕ ${n.table}`))),
            ] : []),
            list);
        document.body.append(addPop);
        const r = $('#erAddTable').getBoundingClientRect();
        addPop.style.top = `${Math.round(r.bottom + 4)}px`;
        addPop.style.left = `${Math.round(Math.min(r.left, window.innerWidth - 300))}px`;
        setTimeout(() => document.addEventListener('click', closeAddPop), 0);
    }

    /** 利用状況を受け取って重ねる（カタログ画面が読み込み後に呼ぶ）。
        常時表示（切替ボタンは無い）。凡例もこのタイミングで出す。 */
    function setUsage(map) {
        usage = map || {};
        $('#erUsageLegend')?.classList.remove('hidden');
        drawEdges();
    }

    /** 表を1つだけ図から外す（削除したとき用）。

        init を呼び直すと図が開いた時点まで巻き戻る（拡大率・履歴・
        保存済みの印・まとまりの絞り込みが全部初期化される）ので、
        消えた分だけを落として描き直す。 */
    function dropTable(name) {
        if (!data || !data.nodes) return;
        const gone = data.nodes.filter(n => n.table === name).map(n => n.id);
        if (!gone.length) return;
        data.nodes = data.nodes.filter(n => n.table !== name);
        data.edges = (data.edges || []).filter(
            e => !gone.includes(`${e.from[0]}.${e.from[1]}`)
              && !gone.includes(`${e.to[0]}.${e.to[1]}`));
        if (selected && (selected.table === name
                         || gone.includes(selected.id))) closePanel();
        extraShown.delete(name);
        render();
        syncHistoryUi();
    }

    return { init, refit: fit, mutate, setUsage, setSuggestions, dropTable };
})();

// ===== 元 manage.js =====
/* DBとテーブルの管理（取り込み画面とカタログ画面で共有）。
   中身の確認・定期取り込みの状態と操作・テーブル/DBの削除。

   もともと取り込み画面の「DBの管理」タブにあったが、「中身を見る場所」
   （カタログ）と「管理する場所」が分かれていると使いにくいので、
   同じ部品を両方から使えるようにここへ切り出した。

   使う側は window.MANAGE = { intervals: [...], refresh: fn } を用意する。
     intervals … 更新の頻度の選択肢（ラベル）
     refresh   … 削除や設定変更のあとに一覧を描き直す関数 */

const MANAGE = window.MANAGE || { intervals: [], refresh: () => location.reload() };
const openTables = new Set();      // 描き直しても開いていたテーブルは開いたまま

/* スケジューラの状態。正常なときは何も出さない（"問題なし"の報告は読む理由がない）。
   止まっているときだけ帯を出す。設定どおりに更新できていない個々のジョブは、
   ⚠マーク・AIの注記・管理者メールで別に届く。 */
function renderSched(s) {
    const box = $('#schedBanner');
    if (!box) return;
    if (!s.enabled) {
        box.replaceChildren(el('div', { class: 'alert alert--warn' },
            '自動実行は停止しています（env の IMPORT_SCHEDULER=false）。手動更新はできます。'));
    } else if (!s.running) {
        box.replaceChildren(el('div', { class: 'alert alert--err' },
            '自動実行のスレッドが動いていません。アプリを再起動してください。'));
    } else {
        box.replaceChildren();
    }
}

/** 定期取り込みの操作ボタン（頻度の変更・手動実行・停止・削除）。 */

function jobControls(j) {
    return [
        // リアルタイム更新の切替。追記のジョブは対象外（サーバ側でも弾かれる）
        j.mode_label === '追記' ? null : el('button', {
            class: 'btn btn--sm',
            title: j.realtime
                ? '質問のたびに元ファイルの更新を確認して取り込み直しています。押すとやめます。'
                : '質問のたびに元ファイルの更新を確認し、変わっていれば取り込み直してから答えるようにします。'
                  + 'ファイルが読めないときは前回取り込んだ内容で答えます。',
            onclick: async () => {
                await api('/api/jobs/update', { id: j.id, realtime: !j.realtime });
                toast(j.realtime
                    ? `「${j.name}」のリアルタイム更新を止めました。`
                    : `「${j.name}」をリアルタイム更新にしました。質問のたびに元ファイルへ追随します。`);
                MANAGE.refresh();
            },
        }, j.realtime ? 'リアルタイム中' : 'リアルタイムにする'),
        el('select', {
            style: 'width:130px',
            title: '更新の頻度',
            onchange: async ev => {
                await api('/api/jobs/update', { id: j.id, interval: ev.target.value });
                toast(`「${j.name}」を ${ev.target.value} に変更しました。`);
                MANAGE.refresh();
            },
        }, MANAGE.intervals.map(i => el('option',
            { ...(i === j.interval_label ? { selected: 'selected' } : {}) }, i))),
        // 定期実行＋追記は手で走らせると間隔が崩れるので押せなくする
        j.manual_blocked
            ? el('button', { class: 'btn btn--sm', disabled: 'disabled',
                             title: j.manual_blocked }, '今すぐ更新（不可）')
            : el('button', {
                class: 'btn btn--sm',
                onclick: async ev => {
                    ev.target.innerHTML = '<span class="spinner"></span>';
                    try {
                        const r = await api('/api/jobs/run', { id: j.id });
                        r.results.forEach(x =>
                            toast(`${x.name}: ${x.message}`, x.ok ? 'ok' : 'err', 7000));
                    } catch (e) { toast(e.message, 'err', 9000); }
                    MANAGE.refresh();
                },
            }, '今すぐ更新'),
        el('button', {
            class: 'btn btn--sm',
            title: j.enabled === false
                ? '自動更新を再開します（次回予定の時刻から動きます）。'
                : '自動更新を一時的に止めます。設定は残るので、いつでも再開できます。'
                  + '止めている間は「更新できていない」警告も出ません。',
            onclick: async () => {
                await api('/api/jobs/update', { id: j.id, enabled: j.enabled === false });
                toast(j.enabled === false
                    ? `「${j.name}」の自動更新を再開しました。`
                    : `「${j.name}」の自動更新を止めました。「再開」でいつでも戻せます。`);
                MANAGE.refresh();
            },
        }, j.enabled === false ? '再開' : '停止'),
        el('button', {
            class: 'btn btn--sm btn--danger',
            title: '定期取り込みの設定だけを消します（テーブルと中のデータは残ります）。'
                   + 'このテーブルは自動更新されなくなります。',
            onclick: async () => {
                if (!confirm(`定期取り込み「${j.name}」の設定を削除しますか？\n`
                    + '（テーブルと中のデータは残ります）')) return;
                await api('/api/jobs/delete', { id: j.id });
                toast('定期取り込みの設定を削除しました。');
                MANAGE.refresh();
            },
        }, '設定を削除'),
    ];
}

/** 1件ぶんの定期取り込みの中身（取り込み元と更新のしかた）。 */

function jobDetail(j, withName) {
    const box = el('div', { style: 'margin-top:6px' });
    if (withName) {
        box.append(el('div', { style: 'font-weight:600;font-size:12.5px;margin-bottom:2px' },
            `${j.name}`,
            j.enabled === false ? el('span', { class: 'badge badge--warn' }, '停止中') : null));
    }
    box.append(
        kv('ファイル名', j.source_label ? j.source_label.split(/[\\/]/).pop() : '―', true),
        kv('フルパス', j.source),
        kv('シート', j.sheet || '（Excel以外）'),
        kv('区切り文字', j.delimiter === null || j.delimiter === undefined
            ? '自動判定' : JSON.stringify(j.delimiter)),
        kv('見出しの行', (Number(j.header_row || 0) + 1) + ' 行目'),
        kv('更新の方法', j.mode_label, true),
        kv('更新の頻度', j.interval_label, true),
        kv('リアルタイム更新', j.realtime ? 'ON（質問のたびに元ファイルへ追随）' : 'OFF', true),
        kv('開始日時', (j.start_at || '').replace('T', ' ') || '（すぐ対象）'),
        kv('次回予定', j.next_label, true),
        kv('前回実行', (j.last_run || '').replace('T', ' ')),
        kv('状態', j.enabled === false ? '停止中' : '有効'));
    // 前回の結果。失敗（赤）と要確認（黄＝数値列が文字に落ちた）は、文章を読まなくても
    // 分かるように色を付ける。成功はそのまま小さく出す。
    if (j.last_status === 'error') {
        box.append(el('div', { class: 'alert alert--err small', style: 'margin-top:6px' },
            el('b', {}, '前回の更新に失敗しています'),
            el('div', { style: 'margin-top:2px' }, j.last_message || '')));
    } else if ((j.last_degraded || []).length) {
        box.append(el('div', { class: 'alert alert--warn small', style: 'margin-top:6px' },
            el('b', {}, `数値にできない値がありました（${j.last_degraded.join('、')}）`),
            el('div', { style: 'margin-top:2px' },
                '文字として保存したので、合計や平均がずれる可能性があります。元ファイルの値を確認してください。')));
    } else {
        box.append(kv('前回結果', j.last_message || '―'));
    }
    if (j.mode === 'append') box.append(kv('保存回数', `${j.keep_runs} 回まで`, true));
    if (j.manual_blocked) {
        box.append(el('div', { class: 'small muted mt' }, ''+ j.manual_blocked));
    }
    box.append(el('div', { class: 'row mt', style: 'gap:6px' }, ...jobControls(j)));
    return box;
}

function kv(label, value, strong) {
    return el('div', { style: 'display:flex;gap:8px;font-size:12.5px;padding:1px 0' },
        el('span', { class: 'muted', style: 'width:120px;flex:0 0 120px' }, label),
        el('span', { class: strong ? '': 'mono', style: strong ? 'font-weight:600': '' },
            value === null || value === undefined || value === '' ? '―' : String(value)));
}

/* --- 削除（テーブル / DB） --------------------------------------------------------
   消す前に「何が巻き添えになるか」を必ず見せる。カタログの説明・関連・例文・
   検算ルールはあちこちのDBに散っていて、画面を見ているだけでは分からないため。 */

function impactList(groups) {
    if (!groups.length) {
        return el('div', { class: 'small muted' }, '巻き添えになるものはありません。');
    }
    return el('div', {}, groups.map(g => el('details', { class: 'acc' },
        el('summary', {},
            el('strong', {}, g.label),
            el('span', { class: 'muted small' }, `${g.items.length}件`)),
        el('div', { class: 'acc__body' },
            g.items.map(it => el('div', { class: 'small', style: 'padding:1px 0' },
                el('span', { class: 'muted mono', style: 'margin-right:6px' }, it.db),
                it.text))))));
}

/** 削除の確認ダイアログ。opts で文言と実行内容を差し替える。 */

async function confirmDelete(opts) {
    let groups;
    try {
        groups = (await api(opts.impactUrl, undefined, 'GET')).groups;
    } catch (e) { return toast(e.message, 'err'); }

    // この画面には「ファイルを選ぶ」の .modal が最初から置いてある。
    // 取り違えないよう、こちらには id を付けておく
    const back = el('div', { class: 'modal', id: 'delModal' });
    const close = () => back.remove();
    back.addEventListener('click', ev => { if (ev.target === back) close(); });

    const dropJobs = el('input', { type: 'checkbox', checked: 'checked' });
    const jobCount = (groups.find(g => g.key === 'jobs')?.items || []).length;
    // 合言葉。DB削除のときだけ、ファイル名をそのまま打ってもらう
    const phrase = opts.phrase
        ? el('input', { type: 'text', style: 'width:100%',
                        placeholder: opts.phrase, autocomplete: 'off' })
        : null;

    const go = el('button', {
        class: 'btn btn--sm btn--danger',
        ...(phrase ? { disabled: 'disabled' } : {}),
        onclick: async () => {
            go.disabled = true;
            try {
                const r = await api(opts.url, {
                    ...opts.body,
                    ...(phrase ? { confirm: phrase.value.trim() } : {}),
                    drop_jobs: dropJobs.checked,
                });
                close();
                toast(opts.done(r));
                MANAGE.refresh();
                opts.after?.(r);
            } catch (e) { toast(e.message, 'err', 9000); go.disabled = false; }
        },
    }, opts.action);
    phrase?.addEventListener('input',
        () => { go.disabled = phrase.value.trim() !== opts.phrase; });

    back.append(el('div', { class: 'modal__box' },
        el('div', { class: 'modal__head' },
            el('b', { class: 'grow' }, opts.title),
            el('button', { class: 'btn btn--sm btn--ghost', onclick: close },
                icon('x', 'icon--sm'))),
        el('div', { class: 'modal__body', style: 'padding:12px 14px' },
            el('div', { class: 'alert alert--err' }, opts.warning),
            el('div', { class: 'small muted', style: 'margin:10px 0 4px' },
                '一緒に片づけるもの'),
            impactList(groups),
            jobCount
                ? el('label', { class: 'row mt', style: 'align-items:center;gap:6px' },
                    dropJobs,
                    el('span', { class: 'small' },
                        `定期取り込みの設定 ${jobCount} 件も削除する`
                        + '（外すと、次の実行でまた取り込まれます）'))
                : null,
            phrase
                ? el('div', { class: 'mt' },
                    el('div', { class: 'small', style: 'margin-bottom:4px' },
                        `確認のため、`, el('b', { class: 'mono' }, opts.phrase),
                        ` をそのまま入力してください。`),
                    phrase)
                : null),
        el('div', { class: 'modal__foot row', style: 'align-items:center' },
            el('div', { class: 'spacer' }),
            el('button', { class: 'btn btn--sm', onclick: close }, 'やめる'),
            go)));
    document.body.append(back);
    (phrase || go).focus();
}


/** 消したテーブルを画面から取り除く。
 *
 *  一覧はサーバが描いたHTMLなので、消しただけでは残り続ける
 *  （別の画面へ行って戻ると消える、という分かりにくい挙動になっていた）。
 *  一覧・上部の数字・ER図・カタログの控えを、その場で揃える。
 */
function dropTableFromView(name, stamps) {
    if (typeof CAT === 'undefined') return;      // カタログ画面以外では何もしない
    const acc = $(`#pane-tables details.acc[data-table="${CSS.escape(name)}"]:not(.t-manage)`);
    const group = acc?.closest('details.acc--group');
    acc?.remove();
    let groupGone = null;
    if (group) {
        const left = $$('details.acc[data-table]:not(.t-manage)', group).length;
        if (!left) {
            groupGone = group.dataset.group || null;
            group.remove();                      // 中身が空になったまとまりは畳んで消す
        } else {
            $('summary .muted', group).textContent = `${left}テーブル`;
        }
    }
    // カタログの控えとER図からも取り除く（用語の置き場所・参照・図に残らないように）
    CAT.tables = (CAT.tables || []).filter(x => x.name !== name);
    if (CAT.er) {
        const gone = (CAT.er.nodes || []).filter(n => n.table === name).map(n => n.id);
        CAT.er.nodes = (CAT.er.nodes || []).filter(n => n.table !== name);
        CAT.er.edges = (CAT.er.edges || []).filter(
            e => !gone.includes(`${e.from[0]}.${e.from[1]}`)
              && !gone.includes(`${e.to[0]}.${e.to[1]}`));
        // init だと図が開いた時点まで巻き戻る（拡大率・元に戻す履歴・
        // 保存済みの印・まとまりの絞り込みが初期化される）。消えた分だけ落とす
        if (typeof ER !== 'undefined') ER.dropTable(name);
    }
    // ビューでもあり得る。ビュータブに残すと、そこから「保存」を押したときに
    // 消したはずのビューが黙って作り直される
    if (Array.isArray(CAT.views)) {
        const before = CAT.views.length;
        CAT.views = CAT.views.filter(v => v.name !== name);
        if (CAT.views.length !== before) MANAGE.refreshViews?.();
    }
    // サーバ側の掃除で用語集・例文・検算が変わっているので、画面が持つ「印」も
    // 差し替える。しないと次の保存が「別の場所で変わりました」で拒まれ、
    // 読み直しで書きかけが失われる
    if (stamps && typeof CAT !== 'undefined' && CAT.stamps) Object.assign(CAT.stamps, stamps);
    MANAGE.scrubTable?.(name);     // 例文・検算・用語の画面からも、この表のぶんを下ろす
    // 書きかけのまま消した場合の「未保存」も下ろす（保存する相手がもういない）。
    // まとまりごと消えたときは、そのメモの未保存も一緒に下ろす
    MANAGE.clearDirty?.(name, groupGone);
    MANAGE.recompute?.();          // 上部の数字（テーブル説明・列の説明）を数え直す
}


/** テーブルの改名（まとまりの移動も同じ口）。カタログの記述は全部ついてくる。 */
function openRenameTable(dbName, table) {
    const i = table.indexOf('__');
    const curGroup = i > 0 ? table.slice(0, i) : '';
    const curName = i > 0 ? table.slice(i + 2) : table;
    // いま存在するまとまりを、表の一覧から拾う
    const groups = [...new Set((window.CAT?.tables || [])
        .map(t => t.name).filter(n => n.includes('__')).map(n => n.split('__')[0]))].sort();

    const back = el('div', { class: 'modal', id: 'renModal' });
    const close = () => back.remove();
    back.addEventListener('click', ev => { if (ev.target === back) close(); });

    const pick = el('select', {},
        ...groups.map(g2 => el('option', { value: g2,
            ...(g2 === curGroup ? { selected: 'selected' } : {}) }, g2)),
        el('option', { value: '__new__' }, '＋ 新しいまとまりを作る'));
    const newGroup = el('input', { type: 'text', placeholder: '新しいまとまり名', class: 'hidden' });
    const name = el('input', { type: 'text', value: curName });
    const hint = el('div', { class: 'small muted mt' });
    const sync = () => {
        newGroup.classList.toggle('hidden', pick.value !== '__new__');
        const g2 = pick.value === '__new__' ? newGroup.value.trim() : pick.value;
        const full = g2 && name.value.trim() ? `${g2}__${name.value.trim()}` : '';
        hint.textContent = !full ? 'まとまりと名前を決めてください。'
            : full === table ? 'いまの名前と同じです。'
            : `新しい名前: ${full}（説明・関連・用語・例文・検算はすべて引き継がれます）`;
        return full;
    };
    pick.addEventListener('change', sync);
    newGroup.addEventListener('input', sync);
    name.addEventListener('input', sync);

    const go = el('button', { class: 'btn btn--sm btn--primary', onclick: async () => {
        const full = sync();
        if (!full || full === table) return;
        go.disabled = true;
        try {
            const r = await api('/api/catalog/rename-table',
                { db: dbName, table, new_table: full });
            toast(`${table} を ${r.new} に変更しました。ページを読み直します。`);
            // reloadClean で読み直す。素の reload だと、書きかけの説明や
            // メモが残っているせいで離脱警告が出て止まり、改名は済んでいるのに
            // 画面だけ旧名のまま残る（保存も 400 で弾かれる）
            setTimeout(reloadClean, 800);
        } catch (e) { toast(e.message, 'err'); go.disabled = false; }
    } }, '変更する');

    back.append(el('div', { class: 'modal__box' },
        el('div', { class: 'modal__head' },
            el('b', {}, `名前・まとまりを変更: ${table}`),
            el('div', { class: 'spacer' }),
            el('button', { class: 'btn btn--sm btn--ghost', 'aria-label': '閉じる',
                onclick: close }, icon('x', 'icon--sm'))),
        el('div', { style: 'padding:14px' },
            el('div', { class: 'row', style: 'align-items:flex-end;gap:8px' },
                el('div', {},
                    el('label', { class: 'field' }, 'まとまり'), pick),
                el('div', {},
                    el('label', { class: 'field hidden' }, ''), newGroup),
                el('div', { class: 'grow' },
                    el('label', { class: 'field' }, 'テーブル名'), name)),
            hint,
            el('div', { class: 'row mt' },
                el('div', { class: 'spacer' }),
                el('button', { class: 'btn btn--sm btn--ghost', onclick: close }, 'やめる'),
                go))));
    document.body.append(back);
    sync();
}


/** テーブル削除の確認。一覧の行の削除ボタンから呼ぶ。 */
function askDeleteTable(dbName, name, rows, isView) {
    // ビューに実体は無い。消えるのは定義だけなので、
    // 「中のN行を削除します」と言うと実際と食い違う
    confirmDelete({
        title: `${isView ? 'ビュー' : 'テーブル'}を削除: ${name}`,
        warning: isView
            ? `${name}（ビュー）の定義を削除します。`
              + '元のテーブルとデータはそのまま残ります。'
              + 'この操作は元に戻せません。'
            : `${name} と、その中の ${(rows || 0).toLocaleString()}行 を削除します。`
              + 'この操作は元に戻せません。',
        impactUrl: `/api/import/impact?db=${encodeURIComponent(dbName)}`
                   + `&table=${encodeURIComponent(name)}`,
        url: '/api/import/drop-table',
        body: { db: dbName, table: name },
        action: isView ? 'ビューを削除する' : 'テーブルを削除する',
        done: () => `${name} を削除し、カタログの記述も片づけました。`,
        after: (res) => dropTableFromView(name, res && res.stamps),
    });
}


function tableCard(dbName, t) {
    const js = t.jobs || [];
    const j = js[0];
    const head = el('summary', {},
        el('strong', {}, t.name),
        el('span', { class: 'muted small' },
            `${(t.rows || 0).toLocaleString()}行 / ${t.column_count}列`),
        js.length
            ? el('span', { class: j.enabled === false ? 'badge badge--warn': 'badge badge--ok' },
                js.length > 1 ? `定期取り込み ${js.length}件`
                    : (j.enabled === false ? '定期取り込み（停止中）' : `定期取り込み ${j.interval_label}`))
            : el('span', { class: 'badge' }, '定期取り込みなし'),
        js.some(x => x.last_status === 'error')
            ? el('span', { class: 'badge badge--err' }, '前回失敗') : null);

    const body = el('div', { class: 'acc__body' });

    // 定期取り込み（取り込み元と更新のしかた）
    body.append(el('div', { style: 'font-weight:700;margin-bottom:4px' }, '定期取り込み'));
    if (js.length) {
        js.forEach(x => body.append(jobDetail(x, js.length >1)));
    } else {
        body.append(el('div', { class: 'small muted' },
            '設定されていません。取り込み元も分かりません'
            + '（手動で取り込んだか、外部で作られたテーブルです）。'
            + '「ファイルから取り込む」で取り込むときに登録できます。'));
    }

    // いま入っているデータ
    body.append(el('div', { class: 'row', style: 'margin-top:10px' },
        el('button', { class: 'btn btn--sm',
            onclick: () => openRenameTable(dbName, t.name) }, '名前・まとまりを変更')));
    body.append(el('div', { style: 'font-weight:700;margin:10px 0 4px' }, '中身'),
        kv('行数', (t.rows || 0).toLocaleString(), true),
        kv('列数', t.column_count),
        kv('取得日時列', t.timestamp_column || '（なし）'),
        kv('保持している回数', t.runs === null ? '―' : `${t.runs} 回分`, true),
        kv('最新の取り込み', (t.latest || '').replace('T', ' ')),
        kv('最古の取り込み', (t.oldest || '').replace('T', ' ')),
        kv('列', t.columns.join(', ')));

    // サンプル行と更新履歴は開いたときに取りに行く（全テーブル分を先読みすると重い）
    const sampleBox = el('div', { class: 'mt' }, el('div', { class: 'small muted' }, '—'));
    const histBox = el('div', { class: 'mt' }, el('div', { class: 'small muted' }, '—'));
    body.append(
        el('div', { class: 'row mt', style: 'align-items:center;gap:6px' },
            el('div', { style: 'font-weight:700' }, 'サンプル行'),
            el('div', { class: 'spacer' }),
            tableViewLink(dbName, t.name),
            el('button', {
                class: 'btn btn--sm btn--ghost',
                onclick: () => loadTableDetail(dbName, t.name, sampleBox, histBox, true),
            }, '読み直す')),
        sampleBox,
        el('div', { style: 'font-weight:700;margin-top:10px' }, '更新履歴'),
        histBox);


    // 「今すぐ更新」を押すと一覧を描き直すので、開いていた表は開いたままにする
    const key = `${dbName}/${t.name}`;
    const acc = el('details', {
        class: 'acc',
        ...(openTables.has(key) ? { open: 'open' } : {}),
        ontoggle: ev => {
            if (!ev.target.open) { openTables.delete(key); return; }
            openTables.add(key);
            loadTableDetail(dbName, t.name, sampleBox, histBox);
        },
    }, head, body);
    // 最初から開いている場合は toggle が飛ばないので、こちらから読みに行く
    if (openTables.has(key)) loadTableDetail(dbName, t.name, sampleBox, histBox);
    // 中身だけを別の入れ物に載せ替える使い方（カタログ画面）のために、
    // サンプル行と更新履歴の置き場を外から辿れるようにしておく
    body.__sampleBox = sampleBox;
    body.__histBox = histBox;
    return acc;
}

/** テーブルのサンプル行と更新履歴を取ってきて流し込む。 */

async function loadTableDetail(dbName, table, sampleBox, histBox, force) {
    if (sampleBox.dataset.loaded && !force) return;
    sampleBox.dataset.loaded = '1';
    const wait = () => el('div', { class: 'small muted' },
        el('span', { class: 'spinner' }), '読み込み中...');
    sampleBox.replaceChildren(wait());
    histBox.replaceChildren(wait());
    let r;
    try {
        r = await api(`/api/import/table?db=${encodeURIComponent(dbName)}`
            + `&table=${encodeURIComponent(table)}`, undefined, 'GET');
    } catch (e) {
        sampleBox.dataset.loaded = '';
        sampleBox.replaceChildren(el('div', { class: 'alert alert--err' }, e.message));
        histBox.replaceChildren();
        return;
    }
    renderSample(sampleBox, r.sample);
    renderHistory(histBox, r.history, r.kinds);
}

function renderSample(box, s) {
    if (s.error) {
        box.replaceChildren(el('div', { class: 'alert alert--warn' }, s.error));
        return;
    }
    if (!s.rows.length) {
        box.replaceChildren(el('div', { class: 'small muted' }, 'まだ1行も入っていません。'));
        return;
    }
    box.replaceChildren(
        el('div', { class: 'small muted', style: 'margin-bottom:4px' },
            s.order_by
                ? `最大 ${s.limit} 行 ・ 「${s.order_by}」の新しい順（直近の取り込み分が上）`
                : `先頭 ${s.limit} 行 ・ 取得日時の列がないので入っている順`),
        dataTable(s.columns, s.rows));
}

function renderHistory(box, list, kinds) {
    if (!list || !list.length) {
        box.replaceChildren(el('div', { class: 'small muted' },
            'まだありません。この画面から取り込むと、ここに1回ぶんずつ残ります。'));
        return;
    }
    const ok = list.filter(h => h.ok).length;
    const rows = list.map(h => el('tr', {},
        el('td', { class: 'mono' }, (h.at || '').replace('T', ' ')),
        el('td', {}, h.ok
            ? el('span', { style: 'color:var(--ok)' }, '成功')
            : el('span', { style: 'color:var(--err)' }, '失敗')),
        el('td', {}, (kinds || {})[h.kind] || h.kind),
        el('td', {}, h.mode === 'append' ? '追記' : '全件入れ替え'),
        el('td', { class: 'num' }, h.ok ? (h.rows || 0).toLocaleString() : '―'),
        el('td', { class: 'num' }, h.removed ? `-${h.removed.toLocaleString()}` : ''),
        el('td', {}, h.kept === null || h.kept === undefined ? ''
            : `${h.kept}${h.keep ? '/'+ h.keep : '' }`),
        el('td', {}, h.seconds === null || h.seconds === undefined ? '' : `${h.seconds}秒`),
        el('td', {}, h.user || (h.kind === 'auto' ? '（自動）' : '')),
        el('td', { title: h.message }, h.message || '')));

    box.replaceChildren(
        el('div', { class: 'small muted', style: 'margin-bottom:4px' },
            `直近 ${list.length} 件（成功 ${ok} / 失敗 ${list.length - ok}）`),
        el('div', { class: 'tablewrap', style: 'max-height:320px' },
            el('table', { class: 'data' },
                el('thead', {}, el('tr', {},
                    ['日時', '結果', 'きっかけ', '方法', '行数', '削除', '保持', '所要', '実行者', 'メッセージ']
                        .map(h => el('th', {}, h)))),
                el('tbody', {}, rows))));
}

/** 対象のテーブルがまだ無い（または消された）定期取り込み。 */

function renderOrphans(list) {
    const box = $('#orphanJobs');
    box.replaceChildren();
    if (!list.length) return;
    const card = el('div', { class: 'card' },
        el('div', { class: 'card__title' }, '対象のテーブルがない定期取り込み'),
        el('div', { class: 'card__desc' },
            'まだ一度も実行されていないか、テーブルが削除された設定です。'
            + '実行すればテーブルが作られます。'));
    list.forEach(j => card.append(el('div', { class: 'acc__body' },
        el('div', { class: 'small mono muted' }, `${j.db_file} / ${j.table}`),
        jobDetail(j, true))));
    box.append(card);
}

// ===== 元 chat.js（window.CHAT_INIT がある画面だけ動く） =====
(() => {
if (!window.CHAT_INIT) return;
/* チャット画面。描画アイテム（text/sql/table/chart/file/error）を組み立てて流す。 */

let currentChatId = window.CHAT_INIT.chatId || null;
let busy = false;
// 表示中のビューの世代。チャットを切り替える（＝ログを描き直す）たびに進める。
// 送信処理は開始時の世代を覚えておき、届いた回答は世代が一致するときだけ描く。
// これが無いと、送信中に別のチャットへ切り替えたとき、後から届いた回答が
// 関係ないチャットの画面に紛れ込む。
let viewToken = 0;
// 過去の会話を開き直したときに、作成済みファイルの保存が走らないようにする
let replaying = false;
// 次に送るユーザー発言の番号。巻き戻しでどこまで戻すかの目印になる。
let turnCount = 0;

/* --- モデルの選択と画像 --------------------------------------------------------- */

let modelInfo = { current: '', vision: false, image_max_count: 4, image_max_mb: 8 };
let pendingImages = [];        // 送信待ちの画像（サーバに預けたトークン）
// テンプレートが入れた素の文言。モデルに応じて画像の案内を足すため、先に控えておく。
const basePlaceholder = document.getElementById('input')?.placeholder || '';

function renderModel() {
    const sel = $('#modelPick');
    const list = modelInfo.models || [];
    sel.replaceChildren(...(list.length
        ? list.map(m => el('option', {
            value: m.id, ...(m.id === modelInfo.current ? { selected: 'selected' } : {}),
            // カタログ全体が収まらないモデルは選ぶ前から分かるようにする
            ...(m.catalog_fits === false ? { title: 'カタログ全体は入りません（自動で絞ります）' } : {}),
        }, m.id + (m.vision ? ' ' : '') + (m.catalog_fits === false ? ' ⚠' : '')))
        : [el('option', { value: modelInfo.current }, modelInfo.current || '（未設定）')]));

    // カタログ全体がこのモデルに収まらないときの警告（文面はサーバが状況に合わせて作る）
    const warn = $('#modelWarn');
    const scope = modelInfo.scope || {};
    warn.style.display = scope.note ? '' : 'none';
    warn.textContent = scope.note || '';

    const badge = $('#modelBadge');
    // 画像の添付はドラッグ＆ドロップと貼り付けで行う（ボタンは置かない）
    badge.textContent = modelInfo.vision
        ? `画像OK（最大${modelInfo.image_max_count}枚・${modelInfo.image_max_mb}MB）`
        : '文字のみ';
    badge.className = 'badge' + (modelInfo.vision ? ' badge--ok' : '');

    /* 添付ボタンを置いていないので、画像の入れ方は入力欄の薄字で伝える。
       画像を扱えないモデルのときに書くと嘘になるので、そのときは出さない。 */
    const input = $('#input');
    input.placeholder = modelInfo.vision
        ? `${basePlaceholder}（画像は Ctrl+V で貼り付け、ドラッグ＆ドロップでも添付できます）`
        : basePlaceholder;

    if (!modelInfo.vision && pendingImages.length) {
        pendingImages = [];
        renderAttachments();
    }
}

async function loadModels(refresh) {
    try {
        modelInfo = await api('/api/models' + (refresh ? '?refresh=1' : ''),
                              undefined, 'GET');
        renderModel();
    } catch (e) { /* 未設定でも画面は動かす */ }
}

function renderAttachments() {
    const row = $('#attachRow');
    const box = $('#attachList');
    row.style.display = pendingImages.length ? '' : 'none';
    box.replaceChildren(...pendingImages.map((im, i) =>
        el('div', { class: 'attach' },
            el('img', { src: im.url, alt: im.filename }),
            el('span', { class: 'attach__name', title: im.filename }, im.filename),
            el('button', {
                class: 'attach__x', title: '外す',
                onclick: () => { pendingImages.splice(i, 1); renderAttachments(); },
            }, '×'))));
}

async function attachImages(files) {
    if (!modelInfo.vision) {
        toast('いま選ばれているモデルは画像を扱えません。', 'warn');
        return;
    }
    for (const f of files) {
        if (pendingImages.length >= modelInfo.image_max_count) {
            toast(`画像は一度に${modelInfo.image_max_count}枚までです。`, 'warn');
            break;
        }
        const fd = new FormData();
        fd.append('file', f);
        try {
            const res = await fetch('/api/chat/image', { method: 'POST', body: fd });
            const data = await res.json();
            if (!res.ok) throw new Error(data.error || '添付できませんでした');
            pendingImages.push(data);
            renderAttachments();
        } catch (e) { toast(e.message, 'err', 8000); }
    }
}

/* --- 対象データ（一覧表示のみ） ------------------------------------------------
   選択UIは無い。どのDBを使うかは質問ごとにアプリが自動で決める。
   一覧はクリックで開閉でき、中身（テーブルと説明）を確かめられる。 */

function wireScope() {
    $$('.dbpick').forEach(box => {
        // まとまりに入っていない表の枠には見出しが無い（開閉するものが無い）。
        // ここで落ちると、この後のモデル選択や送信ボタンの配線まで全部止まる
        $('.dbpick__head', box)?.addEventListener('click', () => {
            box.classList.toggle('is-open');
        });
    });
    // 対象にする表の選択。ナレッジベースと同じく、押した時点で保存する
    // （「保存」を押させると、押し忘れたまま質問して「なぜあの表を見ないのか」になる）
    const picks = () => $$('.tblpick');
    if (!picks().length) return;

    const saveTables = async () => {
        syncTableUi();
        const off = picks().filter(c => !c.checked).map(c => c.dataset.table);
        try {
            await api('/api/tables/prefs', { off });
        } catch (e) { toast(e.message, 'err', 8000); }
    };

    // 見出しの数と、まとまりのチェック状態を実際の選択に合わせる
    function syncTableUi() {
        const all = picks();
        const on = all.filter(c => c.checked).length;
        const count = $('#tblCount');
        if (count) count.textContent = `${on} / ${all.length}`;
        $$('.grppick').forEach(g => {
            const box = g.closest('.dbpick');
            const kids = $$('.tblpick', box);
            const hit = kids.filter(c => c.checked).length;
            g.checked = hit > 0;
            g.indeterminate = hit > 0 && hit < kids.length;   // 一部だけ選んでいる印
        });
        const btn = $('#tblAll');
        if (btn) btn.textContent = on === all.length ? '全解除' : '全選択';
    }

    picks().forEach(c => c.addEventListener('change', saveTables));
    $$('.grppick').forEach(g => g.addEventListener('change', () => {
        $$('.tblpick', g.closest('.dbpick')).forEach(c => { c.checked = g.checked; });
        saveTables();
    }));
    $('#tblAll')?.addEventListener('click', () => {
        const all = picks();
        const turnOn = all.some(c => !c.checked);
        all.forEach(c => { c.checked = turnOn; });
        saveTables();
    });
    syncTableUi();
}

/* --- 社内文書の検索先（利用者ごと） ---------------------------------------------
   チェックは押した時点で保存する。「保存」を押させると、押し忘れたまま質問して
   「なぜあの文書が出ないのか」になるため。

   サーバに保存しているのは「外したもの」で、選んだものではない。選択リスト方式に
   すると、管理者が新しいナレッジベースを足したとき、既存の利用者全員にそれが
   見えないままになる（rag/retriever.py の rag_excluded_ids を参照）。 */

let kb = { bases: [], settings: {}, defaults: {}, fields: [] };

async function saveKnowledge(body) {
    try {
        kb = { ...kb, ...(await api('/api/knowledge/prefs', body)) };
    } catch (e) { toast(e.message, 'err', 8000); }
    renderKnowledge();
}

function renderKbFields() {
    const box = $('#kbFields');
    if (!box) return;
    box.replaceChildren(...(kb.fields || []).map(f => {
        const v = (kb.settings || {})[f.key];
        const input = f.kind === 'choice'
            ? el('select', { id: `kbf-${f.key}`, style: 'width:100%' },
                f.choices.map(c => el('option',
                    { value: c.value, ...(c.value === v ? { selected: 'selected' } : {}) },
                    c.label)))
            : el('input', {
                type: 'number', id: `kbf-${f.key}`, value: v,
                min: f.min, max: f.max, style: 'width:100%',
            });
        return el('div', { class: 'mt' },
            el('label', {
                class: 'field', for: `kbf-${f.key}`,
                'data-desc-title': f.label, 'data-desc': f.help,
            }, f.label),
            input);
    }));
}

function renderKnowledge() {
    const section = $('#kbSection');
    if (!section) return;
    const bases = kb.bases || [];
    // 1件も無ければ節ごと隠す。この状態ではAIに検索ツール自体を渡していない。
    if (!bases.length) { section.style.display = 'none'; return; }
    section.style.display = '';
    // 節を畳んでいても件数は見出しに出す。全部選んでいるときも
    // 「22 / 22」と出す（数字だけだと、選択数なのか総数なのか読めないため）
    const count = $('#kbCount');
    if (count) count.textContent = `${bases.filter(b => b.on).length} / ${bases.length}`;

    $('#kbList').replaceChildren(...bases.map(b => {
        const cb = el('input', {
            type: 'checkbox', ...(b.on ? { checked: 'checked' } : {}),
            onchange: () => {
                b.on = cb.checked;
                saveKnowledge({ off: bases.filter(x => !x.on).map(x => x.id) });
            },
        });
        return el('label', {
            class: `kbpick${b.on ? '' : ' is-off'}`,
            'data-desc-title': b.name,
            'data-desc': b.description || '',
        }, cb, el('span', { class: 'kbpick__name' }, b.name));
    }));
    $('#kbAll').textContent = bases.every(b => b.on) ? '全解除' : '全選択';
    renderKbFields();
}

function wireKnowledge() {
    if (!$('#kbSection')) return;
    kb = window.CHAT_INIT.knowledge || kb;
    renderKnowledge();

    $('#kbAll').addEventListener('click', () => {
        const on = !(kb.bases || []).every(b => b.on);
        kb.bases.forEach(b => { b.on = on; });
        saveKnowledge({ off: kb.bases.filter(x => !x.on).map(x => x.id) });
    });

    $('#kbSave').addEventListener('click', async ev => {
        const settings = {};
        (kb.fields || []).forEach(f => {
            const node = $(`#kbf-${f.key}`);
            if (node) settings[f.key] = f.kind === 'choice' ? node.value : Number(node.value);
        });
        ev.target.disabled = true;
        await saveKnowledge({ settings });
        ev.target.disabled = false;
        toast('検索設定を保存しました。', 'ok');
    });

    $('#kbReset').addEventListener('click', async () => {
        await saveKnowledge({ settings: kb.defaults || {} });
        toast('検索設定を初期値に戻しました。', 'ok');
    });
}

/* --- 履歴 ------------------------------------------------------------------- */

function renderHistory(items) {
    const box = $('#historyList');
    box.replaceChildren();
    if (!items.length) {
        box.append(el('div', { class: 'small muted' }, 'まだ履歴はありません。'));
        return;
    }
    items.forEach(c => {
        const stamp = (c.updated_at || '').slice(5, 16).replace('T', ' ');
        box.append(el('div', {
            class: 'histitem' + (c.id === currentChatId ? ' is-active' : ''),
            onclick: ev => { if (!ev.target.closest('.histitem__del')) openChat(c.id); },
        },
            el('div', { class: 'histitem__title', title: `${c.title}（${stamp}）` }, c.title || '（無題）'),
            el('span', { class: 'small muted' }, stamp),
            el('button', {
                class: 'histitem__del', title: '削除',
                onclick: async () => {
                    if (!confirm(`「${c.title}」を削除しますか？`)) return;
                    await api('/api/chat/delete', { id: c.id });
                    if (c.id === currentChatId) { currentChatId = null; clearLog(); }
                    refreshHistory();
                },
            }, icon('trash', 'icon--sm'))));
    });
}

async function refreshHistory() {
    const r = await api('/api/history', undefined, 'GET');
    currentChatId = r.current || currentChatId;
    renderHistory(r.chats);
}

async function openChat(id) {
    const r = await api('/api/chat/open', { id });
    currentChatId = id;
    clearLog();
    replaying = true;
    lastRole = null;
    // finally で必ず戻す。1件でも描画に失敗すると true のまま固定され、
    // 以降ずっと「再描画中」扱いになってファイルの自動保存が止まる
    try { r.items.forEach(addItem); } finally { replaying = false; }
    // このチャットの質問を送信中なら「考えています…」を出し直す
    // （開始時刻は busyStart から続き）。clearLog で表示ごと消えるため、
    // これが無いと切替後は待ち秒数が見えない。よそのチャットの質問のときは
    // 出さない（無関係な画面にカウントが出るのは紛らわしいだけのため）。
    if (busy && busyChatId === id) setBusy(true);
    refreshHistory();
    scrollDown(true);
}

/* --- 描画 ------------------------------------------------------------------- */

/* まだ何も話していないときの画面。例文は全DBのカタログ（examples）から来る。 */
let starters = { examples: [], tables: [] };

function renderEmpty() {
    const box = el('div', { class: 'empty', id: 'emptyState' },
        el('div', { class: 'empty__icon' }, icon('chat')));

    if (!window.CHAT_INIT.llmReady) {
        box.append(el('div', { class: 'alert alert--warn', style: 'display:inline-block;text-align:left' },
            'LLMが未設定です。管理者に「モデル設定」画面で接続先URLとAPIキーの設定を依頼してください。'));
        return box;
    }

    const kbNames = (kb.bases || []).filter(b => b.on).map(b => b.name);

    if (!(starters.tables || []).length) {
        // data/ にDBが1つも無い。ただしナレッジベースがあれば文書には答えられるので、
        // 「何もできません」とは言わない（DBだけを前提にした案内は誤りになる）。
        if (kbNames.length) {
            box.append(el('div', {}, '社内文書について質問してください。'),
                el('div', { class: 'small muted mt' },
                    `調べられる文書: ${kbNames.join('、')}`),
                el('div', { class: 'small muted mt' },
                    '分析できるデータがまだ取り込まれていないので、数値の集計はできません。'
                    + (window.CHAT_INIT.isAdmin
                        ? '「データ取り込み」からExcel/CSVを取り込めます。' : '')));
        } else {
            box.append(el('div', {}, '分析できるデータがまだありません。'),
                el('div', { class: 'small muted mt' },
                    '管理者は「データ取り込み」からExcel/CSVを取り込めます。'));
        }
        return box;
    }

    box.append(el('div', {}, '下の欄から質問してください。'));
    if (kbNames.length) {
        // 登録が多いとき、全部並べると初見の人には文字の壁になる。
        // 代表2つ＋件数だけ伝えて、一覧はサイドバーに任せる。
        const brief = kbNames.length > 3
            ? `データに加えて、社内文書（${kbNames.slice(0, 2).join('・')} など`
              + `${kbNames.length}件）も調べられます。`
              + '一覧はサイドバーの「社内文書の検索先」にあります。'
            : `データに加えて、社内文書も調べられます: ${kbNames.join('、')}`;
        box.append(el('div', { class: 'small muted mt' }, brief));
    }

    if ((starters.examples || []).length) {
        box.append(el('div', { class: 'small muted mt' }, '質問例:'),
            el('div', { class: 'examples', style: 'justify-content:center;margin-top:10px' },
                starters.examples.map(q =>
                    el('button', { class: 'example', onclick: () => send(q) }, q))));
    } else {
        // 例文が未登録のDB。何について聞けるかだけでも見せる
        box.append(el('div', { class: 'small muted mt' },
            `使えるテーブル: ${starters.tables.join('、')}`));
        if (window.CHAT_INIT.isAdmin) {
            box.append(el('div', { class: 'small muted mt' },
                'データカタログの「質問とSQLの例文」に登録すると、ここに出ます。'
                + '回答が正しかったときに出る「この質問とSQLを例文として保存」からも増やせます。'));
        }
    }
    return box;
}

function showEmpty() {
    if ($('#logInner').querySelector('.msg, .toolblock, .report, .doc')) return;
    $('#emptyState')?.remove();
    $('#logInner').append(renderEmpty());
}

function clearLog() {
    viewToken++;                 // 進行中の送信からの描き込みを、ここで無効にする
    turnCount = 0;
    $('#logInner').replaceChildren(renderEmpty());
}

function bubble(role) {
    const wrap = el('div', { class: `msg msg--${role}` },
        el('div', { class: 'msg__body' }));
    $('#emptyState')?.remove();
    $('#logInner').append(wrap);
    return $('.msg__body', wrap);
}

let lastRole = null;
function slot(role) {
    const last = $('#logInner').lastElementChild;
    if (lastRole === role && last && last.classList.contains('msg')) return $('.msg__body', last);
    lastRole = role;
    return bubble(role);
}

/* このSQLが触れているテーブルを、カタログの該当テーブルへのリンクにする。
   AIが「この列が何か分からない」と言ったその場から、説明を書きに行けるようにする。
   カタログは管理者専用なので、リンクも管理者にだけ出す。 */
function catalogLinks(tables) {
    if (!window.CHAT_INIT.isAdmin || !(tables || []).length) return null;
    return el('div', { class: 'catlinks' },
        el('span', { class: 'muted' }, 'カタログで説明を書く:'),
        ...tables.map(t => el('a', {
            href: `/catalog?db=${encodeURIComponent(t.db)}`
                  + `#tab=tables&table=${encodeURIComponent(t.table)}`,
            target: '_blank', rel: 'noopener',
            title: `${t.db} の ${t.table} を開く（列の説明はここで書けます）`,
        }, t.table)));
}

/* ER図のカード。図はその場に埋めず、開いたときにキャンバスを組み立てる。
   （er.js は一度に1つの図しか持てないので、開いている間だけ実体を作る） */
/* 「テーブルを見せて」で出るカード。全行のビューアへのリンクを出すだけで、
   勝手には開かない。開くかどうかは人が「テーブル全体を開く」を押して決める
   （見たいタイミングは人の側にあり、送るたびにタブが増えるのは邪魔なため）。 */
function tableCardLink(item) {
    const href = `/table?db=${encodeURIComponent(item.db)}&table=${encodeURIComponent(item.table)}`;
    const meta = [
        item.rows === null || item.rows === undefined ? null : `${Number(item.rows).toLocaleString()}行`,
        (item.columns || []).length ? `${item.columns.length}列` : null,
        item.description || null,
    ].filter(Boolean).join(' ・ ');
    return el('div', { class: 'filecard' },
        icon('table', 'icon--lg'),
        el('div', { class: 'grow' },
            el('div', { class: 'name' }, item.title || `${item.table}（${item.db}）`),
            el('div', { class: 'small muted' }, meta || 'テーブルの中身を別タブで開きます')),
        el('a', { class: 'btn btn--primary btn--sm', href, target: '_blank', rel: 'noopener',
                  title: `${item.table} の全行を別タブで開きます（読み取り専用）` },
           'テーブル全体を開く'));
}

function erCard(item) {
    return el('div', { class: 'filecard' },
        icon('table', 'icon--lg'),
        el('div', { class: 'grow' },
            el('div', { class: 'name' }, item.title || (item.db + ' のER図')),
            el('div', { class: 'small muted' },
                'テーブルの関係図（読み取り専用・拡大縮小と全画面ができます）')),
        el('button', { class: 'btn btn--primary btn--sm',
                       onclick: () => openErModal(item) }, '表示'));
}

function openErModal(item) {
    const back = el('div', { class: 'modal' });
    const close = () => { back.remove(); };
    back.addEventListener('click', ev => { if (ev.target === back) close(); });

    const svgEl = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svgEl.setAttribute('class', 'er__svg');
    svgEl.id = 'erSvg';

    // er.js が期待するIDでキャンバスの骨組みを作る（カタログ画面と同じ構造）
    const box = el('div', { class: 'modal__box', style: 'max-width:96vw;width:1200px' },
        el('div', { class: 'modal__head' },
            el('b', { class: 'grow' }, item.title || (item.db + ' のER図')),
            el('button', { class: 'btn btn--sm btn--ghost', onclick: close }, icon('x', 'icon--sm'))),
        el('div', { class: 'modal__body', style: 'padding:10px' },
            el('div', { class: 'er er--chat', id: 'erRoot' },
                el('div', { class: 'er__toolbar' },
                    el('button', { class: 'btn btn--sm', id: 'erFull' }, '全画面')),
                el('div', { class: 'er__viewport', id: 'erViewport' },
                    svgEl,
                    el('div', { class: 'er__world', id: 'erWorld' })),
                el('div', { class: 'er__legend' },
                    el('b', {}, 'IPA表記'), '　下線＝主キー　線の両端の 1・*＝多重度　',
                    '実線＝登録済み／短い破線＝FOREIGN KEY　長い破線＝DBをまたぐ関連'),
                el('div', { class: 'er__panel hidden', id: 'erPanel' }))));
    back.append(box);
    document.body.append(back);
    ER.init({ data: item.er, readonly: true });
    // Escは段階的に効かせる: 全画面中なら解除だけ(er.jsに任せる)、通常表示なら閉じる。
    // capture=true で er.js より先に状態を見る（同じイベントで両方起きるのを防ぐ）
    document.addEventListener('keydown', function esc(ev) {
        if (ev.key !== 'Escape') return;
        const root = document.getElementById('erRoot');
        if (root && root.classList.contains('er--full')) return;   // 解除はer.js側
        document.removeEventListener('keydown', esc, true);
        close();
    }, true);
}

/* 用語の登録カード。AIは提案まで。書き込みはボタンを押したときだけ。
   SQLや置き場所は出さない。代わりに「どう数えるか」の日本語と実データの件数で、
   SQLを読めない人でも正しさを判断できるようにする。 */
function glossaryCard(item) {
    const card = el('div', { class: 'mailcard' });
    const row = (label, value) => value ? el('div', { class: 'mailcard__row' },
        el('span', { class: 'mailcard__label' }, label),
        el('span', { class: 'grow' }, value)) : null;

    card.append(el('div', { class: 'mailcard__head' },
        icon('catalog', 'icon--sm'), el('b', {}, '用語集への登録の提案'),
        el('div', { class: 'spacer' }),
        el('span', { class: 'badge' + (item.exists ? ' badge--warn' : ' badge--ok') },
            item.exists ? '既存の定義を変更' : '新規登録')));
    [row('用語', item.term),
     row('意味', item.description),
     row('どう数えるか', item.how),
     item.detail ? row('実データで確認', item.detail) : null,
     item.exists && item.old ? el('div', { class: 'mailcard__row' },
         el('span', { class: 'mailcard__label' }, '変更前'),
         el('span', { class: 'grow small muted' },
             item.old.description || '', item.old.sql ? '（式あり）' : '')) : null,
    ].filter(Boolean).forEach(x => card.append(x));

    const btn = el('button', { class: 'btn btn--primary btn--sm', onclick: async () => {
        btn.disabled = true;
        try {
            const r = await api('/api/chat/glossary-save', {
                db: item.db, table: item.table, term: item.term,
                description: item.description, sql: item.sql });
            toast(r.message, 'ok', 8000);
            btn.textContent = '登録済み';
        } catch (e) { toast(e.message, 'err', 8000); btn.disabled = false; }
    } }, '用語集に登録');
    card.append(el('div', { class: 'mailcard__row', style: 'justify-content:flex-end' },
        el('span', { class: 'small muted grow' },
            '登録すると全員のAIがこの定義に従います。登録した人と変更の記録は残ります。'),
        btn));
    return card;
}

/* 例文の登録カード。SQLは出さず、「何をどう集計したか」と実データの先頭数行を見せる。 */
function exampleCard(item) {
    const card = el('div', { class: 'mailcard' });
    const row = (label, value) => value ? el('div', { class: 'mailcard__row' },
        el('span', { class: 'mailcard__label' }, label),
        el('span', { class: 'grow' }, value)) : null;

    card.append(el('div', { class: 'mailcard__head' },
        icon('catalog', 'icon--sm'), el('b', {}, '例文への登録の提案'),
        el('div', { class: 'spacer' }),
        el('span', { class: 'badge' + (item.exists ? ' badge--warn' : ' badge--ok') },
            item.exists ? '既存の例文を更新' : '新規登録')));
    [row('質問', item.question),
     row('何をしたか', item.summary),
     item.exists && item.old_q && item.old_q !== item.question
         ? row('変更前の質問', item.old_q) : null,
    ].filter(Boolean).forEach(x => card.append(x));

    if ((item.rows || []).length) {
        card.append(el('div', { class: 'mailcard__row' },
            el('span', { class: 'mailcard__label' }, '実データ'),
            el('div', { class: 'grow' },
                dataTable(item.columns || [], item.rows || [],
                    { caption: `全 ${Number(item.total || 0).toLocaleString()} 件中 先頭 ${item.rows.length} 行` }))));
    }

    const btn = el('button', { class: 'btn btn--primary btn--sm', onclick: async () => {
        btn.disabled = true;
        try {
            const r = await api('/api/chat/save-example', {
                db: item.db, question: item.question, sql: item.sql, description: item.summary });
            toast(r.message, 'ok', 8000);
            btn.textContent = '登録済み';
        } catch (e) { toast(e.message, 'err', 8000); btn.disabled = false; }
    } }, '例文として登録');
    card.append(el('div', { class: 'mailcard__row', style: 'justify-content:flex-end' },
        el('span', { class: 'small muted grow' },
            '登録すると似た質問へのAIのお手本になります。登録した人と変更の記録は残ります。'),
        btn));
    return card;
}

/* --- 社内文書の検索結果（出典） -------------------------------------------------
   回答の中の [出典n] と突き合わせられるように、番号・ナレッジベース名・
   ファイル名・本文の抜粋を並べる。AIの回答を人が検証できることが目的なので、
   折りたたんで隠さず、行の抜粋だけを畳んでおく（クリックで全文）。 */

function sourcesCard(item) {
    const sources = item.sources || [];
    const head = el('div', { class: 'toolblock__head' },
        icon('book', 'icon--sm'),
        el('span', {}, '社内文書の検索'),
        el('span', { class: 'muted small' }, `— 「${item.query}」`),
        el('div', { class: 'spacer' }),
        el('span', { class: 'badge' }, `${sources.length}件`));

    const block = el('div', { class: 'toolblock' }, head);

    if (!sources.length) {
        // 「渡せる文字数に入らなかった」と「本当に無かった」は別のこと。
        // 一緒にすると、設定を上げれば読めるのに諦めてしまう
        block.append(el('div', { class: 'srcs' },
            el('div', { class: 'small muted' }, item.dropped
                ? `文章は ${item.dropped} 件見つかりましたが、1件あたりが長く、`
                  + '参考情報に渡せる文字数の上限に入りませんでした。'
                  + 'サイドバーの検索設定で「参考情報の文字数上限」を上げると読めます。'
                : `該当する文章は見つかりませんでした（探した先: ${(item.searched || []).join('、') || 'なし'}）。`)));
    } else {
        block.append(el('div', { class: 'srcs' }, sources.map(s => {
            // サーバが送ってくるのは先頭だけ（全文ではない）。
            // 「全文」と書くと、ここに無い＝文書に無い、と読まれてしまう
            const cut = s.excerpt_cut;
            const row = el('div', {
                class: 'src',
                title: cut ? `クリックで抜粋（先頭${s.excerpt_chars || 200}字）の全体を表示します`
                           : 'クリックで抜粋の全体を表示します',
                onclick: () => row.classList.toggle('is-open'),
            },
                el('div', { class: 'src__where' },
                    el('span', { class: 'src__no' }, `[出典${s.index}]`),
                    el('span', {}, s.knowledge_base),
                    s.file_path ? el('span', { class: 'muted' }, ` / ${s.file_path}`) : null,
                    cut ? el('span', { class: 'small muted' },
                            ` （先頭${s.excerpt_chars || 200}字）`) : null),
                el('div', { class: 'src__text' }, (s.excerpt || '') + (cut ? '…' : '')));
            return row;
        })));
    }

    // 一部のナレッジベースだけ落ちた場合。黙って減らすと「無かった」と誤解される
    if ((item.failures || []).length) {
        block.append(el('div', { class: 'toolblock__foot' },
            el('span', { class: 'small' },
                '次のナレッジベースは検索できませんでした: '
                + item.failures.map(f => `${f.knowledge_base}（${f.error.split('\n')[0]}）`).join(' / '))));
    }
    return block;
}

function addItem(item) {
    const body = slot(item.role === 'user' ? 'user' : 'assistant');
    if (item.kind === 'text' && item.role === 'user' && item.turn !== undefined) {
        turnCount = item.turn + 1;           // 次に送る発言の番号
        body.append(userTurn(item));
    } else if (item.kind === 'text') {
        body.append(el('div', { html: `<p>${mdToHtml(item.content)}</p>` },
                      catalogLinks(item.tables)));
    } else if (item.kind === 'sql') {
        const block = el('div', { class: 'toolblock' },
            el('div', { class: 'toolblock__head' },
                icon('table', 'icon--sm'), el('span', {}, item.label || item.tool),
                item.purpose ? el('span', { class: 'muted small' }, `— ${item.purpose}`) : null),
            el('pre', { class: 'mono' }, item.sql),
            // SQLを読めない人向けの解説。AIが書いたものなので、根拠はSQL本体で確かめられる
            item.explanation
                ? el('div', { class: 'toolblock__note' },
                    el('b', {}, 'このSQLがしていること'),
                    el('div', { style: 'white-space:pre-wrap;margin-top:3px' }, item.explanation))
                : null);
        const links = catalogLinks(item.tables);
        if (item.question || links) {
            const foot = el('div', { class: 'toolblock__foot' });
            if (item.question) {
                // 直接保存ではなくAIに頼む。AIが内容の日本語説明と実データ付きの
                // 登録カードを出し、そこで確定する（何が登録されるか見えるように）
                foot.append(el('button', {
                    class: 'btn btn--sm',
                    onclick: ev => {
                        ev.target.disabled = true;
                        send(`「${item.question}」の回答に使ったSQLを、そのまま例文として登録してください。`);
                    },
                }, 'この質問と答え方を例文にする'));
            }
            if (links) foot.append(links);
            block.append(foot);
        }
        body.append(block);
    } else if (item.kind === 'table') {
        const cap = `${(item.rows || []).length} 行`
            + (item.truncated ? '（上限で切り詰め）' : '');
        body.append(dataTable(item.columns || [], item.rows || [], { caption: cap }));
    } else if (item.kind === 'chart') {
        // 元データが上限で切られていると、グラフは「一部だけ」を描くことになる。
        // 断りが無いと全体を表したものに見えてしまうので、図の上に必ず出す。
        const warn = truncationNote(item);
        if (warn) body.append(warn);
        const div = el('div', { class: 'plot' });
        body.append(div);
        if (item.figure) {
            Plotly.newPlot(div, item.figure.data, {
                ...item.figure.layout, autosize: true,
                margin: { l: 55, r: 20, t: 40, b: 50 },
                paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)',
            }, { responsive: true, displaylogo: false });
        }
    } else if (item.kind === 'file') {
        const card = el('div', { class: 'filecard' },
            icon('file', 'icon--lg'),
            el('div', { class: 'grow' },
                el('div', { class: 'name' }, item.filename),
                el('div', { class: 'small muted' },
                    item.note || (item.sheets || []).map(s => `${s.name}: ${s.total}行`).join('/ '))),
            item.url ? el('a', { class: 'btn btn--primary btn--sm', href: item.url }, 'ダウンロード') : null);
        body.append(card);
        // 作られた直後だけ自動で保存を始める（履歴を開き直したときは出さない）
        if (item.url && !replaying && window.CHAT_INIT.autoDownload) window.location.href = item.url;
        (item.sheets || []).forEach(s => {
            if (!s.rows || !s.rows.length) return;
            body.append(el('details', { class: 'acc' },
                el('summary', {}, `「${s.name}」の内容を確認（先頭${s.rows.length}行）`),
                el('div', { class: 'acc__body' }, dataTable(s.columns, s.rows))));
        });
    } else if (item.kind === 'glossary_term') {
        body.append(glossaryCard(item));
    } else if (item.kind === 'example_proposal') {
        body.append(exampleCard(item));
    } else if (item.kind === 'sources') {
        body.append(sourcesCard(item));
    } else if (item.kind === 'table_link') {
        body.append(tableCardLink(item));
    } else if (item.kind === 'er') {
        body.append(erCard(item));
    } else if (item.kind === 'report') {
        const warn = truncationNote(item);
        if (warn) body.append(warn);
        body.append(reportBlock(item));
    } else if (item.kind === 'report_doc') {
        body.append(reportDoc(item));
    } else if (item.kind === 'mail_draft') {
        body.append(mailCard(item));
    } else if (item.kind === 'error') {
        body.append(el('div', { class: 'alert alert--err' }, item.message));
    }
}

/* --- 発言の巻き戻し・編集 --------------------------------------------------------- */

/** ユーザーの発言。マウスを乗せると編集アイコンが出る。 */
function userTurn(item) {
    const wrap = el('div', { class: 'turn' });
    const text = el('div', {});
    if ((item.images || []).length) {
        text.append(el('div', { class: 'sentimgs' },
            item.images.map(im => el('a', { href: im.url, target: '_blank',
                                            title: im.filename },
                el('img', { src: im.url, alt: im.filename })))));
    }
    text.append(el('div', { html: `<p>${mdToHtml(item.content)}</p>` }));
    // 操作は「書き直す」の1本だけ。以前は「消すだけ」のボタンも並べていたが、
    // 目的はどちらも結局「その地点からやり直す」なので、2本あると違いの説明の
    // ほうが難しくなる。純粋に消したいだけの稀なケースは、書き直し画面で
    // 本文を空にして送信すれば同じことができる（確認の上で以降を消すだけになる）。
    const tools = el('div', { class: 'turn__tools' },
        el('button', {
            class: 'turn__btn', title: 'この発言を書き直して、聞き直します（以降のやり取りは新しい回答に置き換わります）',
            onclick: () => editTurn(wrap, item),
        }, icon('tool', 'icon--sm'), el('span', { class: 'turn__btn__t' }, '書き直す')));
    wrap.append(text, tools);
    return wrap;
}

/** 発言を編集する形に差し替える。 */
function editTurn(wrap, item) {
    if (busy) return;
    const area = el('textarea', { class: 'turn__edit', rows: '3' });
    area.value = item.content;
    const cancel = () => {
        const fresh = userTurn(item);
        wrap.replaceWith(fresh);
    };
    const box = el('div', {},
        area,
        el('div', { class: 'row mt' },
            el('button', { class: 'btn btn--primary btn--sm',
                           onclick: () => rewindTo(item, area.value, wrap) }, '書き直して送信'),
            el('button', { class: 'btn btn--sm', onclick: cancel }, 'キャンセル'),
            el('div', { class: 'spacer' }),
            el('span', { class: 'small muted' }, '送信すると、これ以降のやり取りは新しい回答に置き換わります')));
    wrap.replaceChildren(box);
    area.focus();
    area.setSelectionRange(area.value.length, area.value.length);
    area.style.height = 'auto';
    area.style.height = Math.min(240, area.scrollHeight) + 'px';
    area.addEventListener('input', () => {
        area.style.height = 'auto';
        area.style.height = Math.min(240, area.scrollHeight) + 'px';
    });
    area.addEventListener('keydown', ev => {
        if (ev.key === 'Enter' && !ev.shiftKey) { ev.preventDefault(); rewindTo(item, area.value, wrap); }
        if (ev.key === 'Escape') cancel();
    });
    scrollDown();
}

/** 巻き戻して、必要ならその内容で会話をやり直す。 */
/** 画面上の、この発言より後ろをすべて消す（サーバの返事を待たずに見た目を合わせる）。
 *
 *  待っている間ずっと古いやり取りが残っていると、「押せていないのか、
 *  やり直し中なのか」が見た目で分からない。押した時点で消えれば、
 *  残っているのが新しい質問だけになり、待ち表示の意味も伝わる。
 */
function truncateLogAt(wrap) {
    const msg = wrap.closest('.msg');
    if (!msg) return;
    while (msg.nextElementSibling) msg.nextElementSibling.remove();
    while (wrap.nextElementSibling) wrap.nextElementSibling.remove();
}

async function rewindTo(item, text, wrap) {
    if (busy) return;
    const send = (text || '').trim();
    if (!send && !confirm('この発言と、それ以降のやり取りを消します。'
                          + '聞き直しはしません。よろしいですか？')) {
        return;
    }
    if (wrap) {
        truncateLogAt(wrap);
        if (send) {
            // 書き直した内容を、いま送った質問として見せる
            wrap.replaceWith(userTurn({ ...item, content: send }));
        } else {
            const msg = wrap.closest('.msg');
            wrap.remove();
            if (msg && !$('.msg__body', msg)?.childElementCount) msg.remove();
        }
        lastRole = null;
    }
    setBusy(true, send ? 'やり直し中' : '巻き戻し中');
    try {
        const r = await api('/api/chat/rewind', { turn: item.turn, text: send });
        clearLog();
        lastRole = null;
        replaying = true;                    // 再描画なのでファイルの自動保存は走らせない
        // finally で必ず戻す（1件でも描画に失敗すると true のまま固定される）
        try { (r.items || []).forEach(addItem); } finally { replaying = false; }
        if (!send) {
            // 巻き戻しだけのときは、消した発言を入力欄に戻す
            $('#input').value = r.restored || '';
            $('#input').style.height = 'auto';
            $('#input').style.height = Math.min(200, $('#input').scrollHeight) + 'px';
            $('#input').focus();
            toast(`${r.dropped}件のやり取りを取り消しました。入力欄から続けられます。`, 'ok');
        }
        currentChatId = r.chat_id || currentChatId;
        refreshHistory();
    } catch (e) {
        toast(e.message, 'err', 8000);
    }
    setBusy(false);
    scrollDown(true);
}

/* --- 分析結果（表＋所見） ------------------------------------------------------- */

/** 元データを上限で切り詰めたときの断り書き。切られていなければ null。
 *
 *  表は行数キャプションで分かるが、グラフとレポートは見た目に手がかりが無い。
 *  一部だけを描いたものを全体と読み違えるのがいちばん困るので、目立つ形で出す。 */
function truncationNote(item) {
    if (!item || !item.truncated) return null;
    const total = item.source_total_rows;
    return el('div', { class: 'alert alert--warn small' },
        '元データは上限で切り詰められています'
        + (total ? `（実際は ${Number(total).toLocaleString()} 行）` : '')
        + '。この結果は全体の一部です。'
        + '全体を見るには、SQLで集計してから作り直してください。');
}

function reportBlock(item) {
    const box = el('div', { class: 'report' });
    if (item.title) box.append(el('div', { class: 'report__title' }, item.title));
    (item.tables || []).forEach((t, i) => {
        const cap = `${(t.rows || []).length} 行`;
        const table = dataTable(t.columns || [], t.rows || [], { caption: cap });
        // 表が多いときは1つ目だけ開いておく（結論はたいてい先頭にある）
        if ((item.tables || []).length > 1) {
            box.append(el('details', { class: 'acc', ...(i === 0 ? { open: 'open' } : {}) },
                el('summary', {}, t.name || `表${i + 1}`),
                el('div', { class: 'acc__body' }, table)));
        } else {
            if (t.name) box.append(el('div', { class: 'small muted mt' }, t.name));
            box.append(table);
        }
    });
    if ((item.notes || []).length) {
        box.append(el('ul', { class: 'report__notes' },
            item.notes.map(n => el('li', {}, n))));
    }
    return box;
}

/* --- まとまったレポート --------------------------------------------------------- */

function reportDoc(item) {
    const doc = el('div', { class: 'doc' });
    doc.append(el('div', { class: 'doc__head' },
        el('div', { class: 'grow' },
            el('div', { class: 'doc__title' }, item.title),
            item.subtitle ? el('div', { class: 'small muted' }, item.subtitle) : null),
        item.url ? el('a', { class: 'btn btn--sm', href: item.url },
                      `${item.filename}`) : null));

    if ((item.summary || []).length) {
        doc.append(el('div', { class: 'doc__summary' },
            el('div', { class: 'doc__label' }, '要点'),
            el('ul', {}, item.summary.map(s => el('li', {}, s)))));
    }

    (item.sections || []).forEach((s, i) => {
        const sec = el('div', { class: 'doc__section' },
            el('h4', { class: 'doc__h' }, `${i + 1}. ${s.heading}`));
        if (s.body) sec.append(el('div', { html: mdToHtml(s.body) }));
        if (s.figure) {
            const div = el('div', { class: 'plot' });
            sec.append(div);
            Plotly.newPlot(div, s.figure.data, {
                ...s.figure.layout, autosize: true,
                margin: { l: 55, r: 20, t: 40, b: 50 },
                paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)',
            }, { responsive: true, displaylogo: false });
        }
        if (s.chart_error) sec.append(el('div', { class: 'alert alert--warn' }, s.chart_error));
        if (s.table) {
            const cap = s.table.truncated
                ? `全 ${(s.table.total || 0).toLocaleString()} 行のうち上位 ${s.table.rows.length} 行`
                : `${s.table.rows.length} 行`;
            sec.append(dataTable(s.table.columns, s.table.rows, { caption: cap }));
        }
        if (s.note) sec.append(el('div', { class: 'doc__note' }, s.note));
        doc.append(sec);
    });

    if (item.conclusion) {
        doc.append(el('div', { class: 'doc__section' },
            el('h4', { class: 'doc__h' }, '結論'),
            el('div', { html: mdToHtml(item.conclusion) })));
    }
    if ((item.recommendations || []).length) {
        doc.append(el('div', { class: 'doc__section' },
            el('h4', { class: 'doc__h' }, '推奨する打ち手'),
            el('ol', { class: 'doc__actions' },
                item.recommendations.map(r => el('li', {}, r)))));
    }
    if ((item.caveats || []).length) {
        doc.append(el('details', { class: 'acc' },
            el('summary', {}, '前提・注意'),
            el('div', { class: 'acc__body' },
                el('ul', {}, item.caveats.map(c => el('li', {}, c))))));
    }
    return doc;
}

/* --- メールの下書き ------------------------------------------------------------- */

function mailCard(item) {
    const p = item.preview || {};
    const draft = item.draft || {};
    const card = el('div', { class: 'mailcard' });
    const row = (label, value) => el('div', { class: 'mailcard__row' },
        el('span', { class: 'mailcard__label' }, label),
        el('span', { class: 'grow' }, value));

    card.append(el('div', { class: 'mailcard__head' },
        icon('mail', 'icon--sm'), el('b', {}, 'メールの下書き'),
        el('div', { class: 'spacer' }),
        el('span', { class: 'badge' }, p.dry_run ? 'テスト送信モード': '本番送信')));
    card.append(
        row('From', p.from || '（未設定）'),
        row('To', (p.to || []).join(', ') || '（なし）'));
    if ((p.cc || []).length) card.append(row('Cc', p.cc.join(', ')));
    if ((p.bcc || []).length) card.append(row('Bcc', `${p.bcc.length}件（非表示）`));
    card.append(row('件名', p.subject || '（なし）'));
    if ((draft.attach_filenames || []).length) {
        card.append(row('添付', draft.attach_filenames.join(', ')));
    }
    card.append(el('pre', { class: 'mailcard__body' }, p.body || ''));

    const foot = el('div', { class: 'mailcard__foot' });
    if ((p.errors || []).length) {
        card.append(el('div', { class: 'alert alert--err' },
            el('div', {}, 'このままでは送信できません:'),
            el('ul', {}, p.errors.map(e => el('li', {}, e)))));
    } else {
        if (p.dry_run) {
            card.append(el('div', { class: 'alert alert--warn' },
                'いまはテスト送信モードです（env の SMTP_DRY_RUN=true）。'
                + '「送信」を押しても実際には送られず、内容の確認だけ行います。'));
        }
        // テスト送信モードかどうかで文言が変わる。初期・成功・失敗の3か所で
        // 使い回して、途中で本番送信の文言に化けないようにする
        const label = p.dry_run ? '送信（テスト）' : 'このまま送信する';
        const doneLabel = p.dry_run ? '確認しました（未送信）' : '送信済み';
        const send = el('button', { class: 'btn btn--primary btn--sm' }, label);
        send.addEventListener('click', async () => {
            const to = (p.to || []).join(', ');
            if (!confirm(`次の宛先に送信します。よろしいですか？\n\n`
                + `宛先: ${to}\n件名: ${p.subject}`
                + ((draft.attach_filenames || []).length
                    ? `\n添付: ${draft.attach_filenames.join(', ')}` : ''))) return;
            send.disabled = true;
            send.innerHTML = '<span class="spinner"></span> 送信中';
            try {
                const r = await api('/api/mail/send', { draft, confirm: true });
                toast(r.record.message, 'ok', 8000);
                send.textContent = doneLabel;
                foot.append(el('span', { class: 'small muted' },
                    `${r.record.at.replace('T', ' ')} に送信`));
            } catch (e) {
                toast(e.message, 'err', 9000);
                send.disabled = false;
                send.textContent = label;
            }
        });
        foot.append(send);
    }
    foot.append(el('div', { class: 'spacer' }),
        el('span', { class: 'small muted' }, `送信サーバ: ${p.smtp || '未設定' }`));
    card.append(foot);
    return card;
}

/** いちばん下の近くを見ているか（読んでいる途中で飛ばさないための判定）。 */
function atBottom(slack = 120) {
    const log = $('#log');
    return log.scrollHeight - log.scrollTop - log.clientHeight < slack;
}

/**
 * 下までスクロールする。
 * force を付けない限り、ユーザーが上の方を読んでいるときは動かさない。
 * 回答が届くたびに勝手に飛ばされると、途中の表やグラフを読めないため。
 */
function scrollDown(force = false) {
    if (!force && !atBottom()) {
        showJump(true);
        return;
    }
    const log = $('#log');
    log.scrollTop = log.scrollHeight;
    showJump(false);
}

/** 「最新へ」ボタンの出し入れ。上を読んでいるあいだだけ出す。 */
function showJump(on) {
    $('#jumpDown')?.classList.toggle('is-on', !!on);
}

/** スクロール位置を見てボタンを出し入れする。 */
function watchScroll() {
    const log = $('#log');
    if (!log) return;
    // 位置を読んでクラスを付け替えるだけなので、間引かずにそのまま呼ぶ
    const update = () => showJump(!atBottom());
    log.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
    update();
}

/* --- 送信 ------------------------------------------------------------------- */

/* 待ち時間の表示。
   何をしているか言えないときは経過秒だけを出す。時間が見えていれば
   「止まっているのか動いているのか」が分かる。
   ツール実行中はその名前も添える。計測は送信から通しで、途中で戻さない。 */
let thinkTimer = null;

const elapsedText = (sec) =>
    sec < 60 ? `${sec}s` : `${Math.floor(sec / 60)}m ${String(sec % 60).padStart(2, '0')}s`;

// 「考えています…」の開始時刻とラベル。表示要素の中に閉じ込めず外に持つのは、
// チャット切替でログを描き直すと要素ごと消えるため。戻ってきたときに
// この値から表示を作り直せば、経過秒数は数え直しにならず続きから出る。
let busyStart = null;
let busyLabel = '';
let busyChatId = null;   // いま回答を待っている質問が、どのチャットのものか

function setBusy(on, label = '') {
    busy = on;
    $('#send').disabled = on;
    $('#send').innerHTML = on ? `<span class="spinner"></span>` : '送信';

    if (!on) {
        clearInterval(thinkTimer);
        thinkTimer = null;
        busyStart = null;
        busyLabel = '';
        busyChatId = null;
        $('#thinking')?.remove();
        return;
    }

    if (busyStart === null) busyStart = Date.now();
    if (label) busyLabel = label;

    let ind = $('#thinking');
    if (!ind) {
        ind = el('div', { class: 'msg msg--assistant', id: 'thinking' },
            el('div', { class: 'msg__body thinking' },
                el('span', { class: 'spinner' }),
                el('span', { class: 'thinking__label' }),
                el('span', { class: 'thinking__time' })));
        $('#logInner').append(ind);
        const tick = () => {
            const sec = Math.floor((Date.now() - busyStart) / 1000);
            $('.thinking__time', ind).textContent = elapsedText(sec);
        };
        tick();
        clearInterval(thinkTimer);       // 描き直し前の古いタイマーを残さない
        thinkTimer = setInterval(tick, 1000);
        scrollDown(true);
    }
    $('.thinking__label', ind).textContent = label || busyLabel;
}

async function send(text) {
    if (busy) return;
    text = (text || $('#input').value).trim();
    if (!text) return;
    $('#input').value = '';
    $('#input').style.height = 'auto';
    lastRole = null;
    // 添付は送信の時点で確定させる（送信中に足しても混ざらないように）
    const images = pendingImages.slice();
    pendingImages = [];
    renderAttachments();
    addItem({ role: 'user', kind: 'text', content: text, turn: turnCount,
              images: images.length ? images : undefined });
    scrollDown(true);                       // 自分の発言のときは必ず下へ
    busyChatId = currentChatId;             // この質問が属するチャット（新規なら null）
    setBusy(true, '考えています');
    const tokens = images.map(i => i.token);
    const ok = await sendStreaming(text, tokens);
    if (!ok) await sendAtOnce(text, tokens);   // 逐次表示が使えない環境では従来方式へ
    setBusy(false);
}

/** 従来方式。最後にまとめて受け取る。 */
async function sendAtOnce(text, imageTokens) {
    const myView = viewToken;               // この送信が属するビュー
    try {
        const r = await api('/api/chat/send', { text, images: imageTokens });
        if (viewToken === myView) {
            lastRole = null;
            r.items.slice(1).forEach(addItem);  // 先頭は今出したユーザー発言
            currentChatId = r.chat_id || currentChatId;
            scrollDown();
        } else if (r.chat_id && currentChatId === r.chat_id) {
            // 途中で他のチャットを見て戻ってきた。完成形を読み直して揃える
            openChat(r.chat_id);
        }
        refreshHistory();
    } catch (e) {
        if (viewToken === myView) {
            addItem({ role: 'assistant', kind: 'error', message: e.message });
            scrollDown();
        }
    }
    return true;
}

/**
 * 逐次表示。届いた文字からすぐ出す。
 * 戻り値 false は「この方式が使えなかった」の意味で、呼び出し側が従来方式に切り替える。
 */
async function sendStreaming(text, imageTokens) {
    const myView = viewToken;               // この送信が属するビュー
    let missed = false;                     // 別画面表示中に描けなかった分があるか
    let res;
    try {
        res = await fetch('/api/chat/stream', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, images: imageTokens }),
        });
    } catch (e) {
        return false;
    }
    if (!res.ok || !res.body) return false;

    let node = null;          // いま書き込んでいる回答の入れ物
    let buf = '';             // 表示中の本文
    const openText = () => {
        if (node) return;
        $('#thinking')?.remove();
        lastRole = null;
        node = el('div', { class: 'streaming' });
        slot('assistant').append(node);
    };
    const closeText = () => {
        if (node && !buf.trim()) node.remove();   // 中身が無ければ跡を残さない
        else if (node) node.classList.add('is-done');   // 点滅カーソルを消す
        node = null; buf = '';
    };

    const handle = (event, data) => {
        if (event === 'end') {
            if (viewToken === myView) {
                // 送信したときの画面のまま。ライブで全部描けているので何もしない
                currentChatId = data.chat_id || currentChatId;
            } else if (missed && data.chat_id && currentChatId === data.chat_id) {
                // 途中で他のチャットを見て戻ってきた。描き逃した分があるので、
                // 保存済みの完成形（サーバは end を送る前に保存している）を読み直す
                openChat(data.chat_id);
            }
            refreshHistory();
            return;
        }
        if (viewToken !== myView) {         // 別の画面を表示中。ここには描かない
            if (event === 'delta' || event === 'item') missed = true;
            return;
        }
        if (event === 'delta') {
            openText();
            buf += data.text;
            node.innerHTML = mdToHtml(buf);
            scrollDown();
        } else if (event === 'text_end') {
            closeText();
        } else if (event === 'running') {
            setBusy(true, `${data.label}`);
        } else if (event === 'item') {
            closeText();
            lastRole = null;
            addItem(data);
            // 結果が出た＝そのツールは終わっている。ラベルを戻さないと
            // 表が出ているのに「SQL実行…」が回り続けているように見える
            setBusy(true, '考えています');
            scrollDown();
        }
    };

    // SSE を1行ずつ組み立てる（EventSource は POST を使えないので自前で読む）
    const reader = res.body.getReader();
    const dec = new TextDecoder();
    let rest = '';
    try {
        for (;;) {
            const { value, done } = await reader.read();
            if (done) break;
            rest += dec.decode(value, { stream: true });
            const blocks = rest.split('\n\n');
            rest = blocks.pop();
            for (const block of blocks) {
                let ev = 'message', payload = '';
                for (const line of block.split('\n')) {
                    if (line.startsWith('event: ')) ev = line.slice(7).trim();
                    else if (line.startsWith('data: ')) payload += line.slice(6);
                }
                if (!payload) continue;
                // 捨ててよいのは「行が壊れていて読めない」ときだけ。描画側で起きた
                // 例外まで飲み込むと、画面が黙って欠けて原因も残らない
                let data;
                try { data = JSON.parse(payload); }
                catch (e) { continue; }      // 壊れた行は捨てる
                handle(ev, data);
            }
        }
    } catch (e) {
        if (viewToken === myView) {
            addItem({ role: 'assistant', kind: 'error', message: `通信が途切れました: ${e.message}` });
        }
    }
    if (viewToken === myView) closeText();
    return true;
}

/* --- 起動 ------------------------------------------------------------------- */

document.addEventListener('DOMContentLoaded', () => {
    starters = window.CHAT_INIT.starters || { examples: [], tables: [] };
    // 最初の画面は「何を聞けるか」を出す。ナレッジベースの一覧もその材料なので、
    // showEmpty より先に読み込む。
    wireKnowledge();
    showEmpty();
    wireScope();
    renderHistory(window.CHAT_INIT.history || []);
    if (currentChatId) openChat(currentChatId);

    watchScroll();
    $('#jumpDown').addEventListener('click', () => scrollDown(true));

    $('#send').addEventListener('click', () => send());
    $('#input').addEventListener('keydown', ev => {
        if (ev.key === 'Enter' && !ev.shiftKey) { ev.preventDefault(); send(); }
    });
    $('#input').addEventListener('input', ev => {
        ev.target.style.height = 'auto';
        ev.target.style.height = Math.min(200, ev.target.scrollHeight) + 'px';
    });
    $('#newChat').addEventListener('click', async () => {
        await api('/api/chat/open', { id: null });
        currentChatId = null; lastRole = null;
        clearLog(); refreshHistory();
    });
    // --- モデルの選択 ---
    loadModels();
    $('#modelPick').addEventListener('change', async ev => {
        const chosen = ev.target.value;
        try {
            modelInfo = await api('/api/models', { model: chosen });
            renderModel();
            toast(`モデルを ${modelInfo.current} にしました。`
                  + (modelInfo.vision ? '（画像も送れます）' : ''), 'ok');
        } catch (e) {
            toast(e.message, 'err');
            renderModel();               // 選択を元に戻す
        }
    });

    // --- 画像の添付（貼り付け・ドラッグ＆ドロップ）---
    $('#input').addEventListener('paste', ev => {
        const files = [...(ev.clipboardData?.files || [])]
            .filter(f => f.type.startsWith('image/'));
        if (files.length) { ev.preventDefault(); attachImages(files); }
    });

    /* ドラッグ中の判定。子要素をまたぐたびに dragleave が飛ぶので、
       enter と leave の数を数えて「本当に外へ出た」ときだけ消す。 */
    const zone = $('#dropzone');
    const hasFiles = (ev) => [...(ev.dataTransfer?.types || [])].includes('Files');
    let depth = 0;

    const show = () => {
        $('#dropzoneText').textContent = modelInfo.vision
            ? '画像をドロップして添付'
            : 'いま選ばれているモデルは画像を扱えません';
        zone.classList.toggle('is-warn', !modelInfo.vision);
        zone.classList.add('is-on');
    };
    const hide = () => { depth = 0; zone.classList.remove('is-on'); };

    document.addEventListener('dragenter', ev => {
        if (!hasFiles(ev)) return;
        depth++; show();
    });
    document.addEventListener('dragover', ev => {
        if (hasFiles(ev)) ev.preventDefault();      // これが無いと drop が飛ばない
    });
    document.addEventListener('dragleave', ev => {
        if (!hasFiles(ev)) return;
        if (--depth <= 0) hide();
    });
    document.addEventListener('drop', ev => {
        if (!hasFiles(ev)) return;
        ev.preventDefault();
        hide();
        attachImages([...(ev.dataTransfer?.files || [])]
            .filter(f => f.type.startsWith('image/')));
    });
});
})();

// ===== 元 catalog.js（window.CAT がある画面だけ動く） =====
(() => {
if (!window.CAT) return;
/* データカタログ画面。タブ・テーブル編集・用語集・例文・ツール。 */

/* --- タブ ------------------------------------------------------------------- */

/* いま見ているタブはURLのハッシュに残す。ツール保存などでページを
   読み直しても、同じタブに戻ってこられる。 */
function activateTab(pane) {
    // 「DB情報」タブは「DB・テーブル」に統合した。古いブックマークや、
    // DBを切り替えたときの持ち越しで来ても迷子にせず、その場所を開いて見せる。
    if (pane === 'info') {
        pane = 'tables';
    }
    const tab = $(`.tab[data-pane="${pane}"]`);
    if (!tab) return;
    $$('.tab[data-pane]').forEach(t => t.classList.toggle('is-active', t === tab));
    $$('.tabpane').forEach(p => p.classList.toggle('is-active', p.id === `pane-${pane}`));
    // ツールはDBに属さない（全DB共通）。DBの切替と充実度メーターを見せたままだと
    // 「選択中のDBのツール」と読めてしまうので、このタブでは隠す。
    const end = $('.tabs__end');
    if (end) end.style.display = (pane === 'tools') ? 'none' : '';
    if (pane === 'er') ER.refit();
    // 隠れているタブでは高さを測れないので、表示された瞬間に伸びる欄を測り直す
    if (pane === 'glossary') $$('#pane-glossary textarea').forEach(autoGrow);
    history.replaceState(null, '',
        pane === 'glossary' ? `#tab=glossary&sec=${glSec}` : `#tab=${pane}`);
}

/* チャットから「カタログで説明を書く」で来たとき、そのテーブルを開いて光らせる。
   一覧の途中にあると、開いても自分で探すことになるので、位置まで運ぶ。 */
function revealTable(name) {
    const acc = $(`#pane-tables details.acc[data-table="${CSS.escape(name)}"]:not(.t-manage)`);
    if (!acc) {
        toast(`テーブル「${name}」が見つかりません。`, 'warn');
        return;
    }
    acc.classList.remove('hidden');
    // 元DBグループで畳まれていたら、先に親を開かないと位置へ運べない
    const grp = acc.closest('details.acc--group');
    if (grp) { grp.classList.remove('hidden'); grp.open = true; }
    acc.open = true;
    acc.classList.add('is-target');
    acc.scrollIntoView({ block: 'center', behavior: 'smooth' });
    // 光らせるのは合図なので、見つけてもらえたら消す
    setTimeout(() => acc.classList.remove('is-target'), 2600);
}


function wireTabs() {
    $$('.tab[data-pane]').forEach(tab => tab.addEventListener('click', () => activateTab(tab.dataset.pane)));
    // activateTab はハッシュを書き換えるので、必要な値は先に全部読んでおく
    const hash = location.hash;
    const sec = hash.match(/sec=(\w+)/);
    const tab = hash.match(/tab=(\w+)/);
    const table = hash.match(/table=([^&]+)/);

    if (sec && ['gl', 'ex', 'ck'].includes(sec[1])) switchSec(sec[1]);
    if (table) {
        activateTab('tables');
        // 描画が終わってから運ぶ（開いた直後は高さが確定していない）
        requestAnimationFrame(() => revealTable(decodeURIComponent(table[1])));
    } else if (tab) {
        activateTab(tab[1]);
    }
}

/* --- 未保存の変更 --------------------------------------------------------------
   書きかけの内容を黙って失わせない。編集した場所に「未保存」の印を付け、
   画面右下のバーからまとめて保存できるようにする。ページを離れるときは警告。 */

const dirty = { tables: new Set(), groups: new Set(),
                glossary: false, examples: false, checks: false };

function dirtyLabel() {
    const parts = [];
    if (dirty.tables.size) parts.push(`テーブル${dirty.tables.size}件`);
    if (dirty.groups.size) parts.push(`まとまり${dirty.groups.size}件`);
    if (dirty.glossary) parts.push('用語集');
    if (dirty.examples) parts.push('例文');
    if (dirty.checks) parts.push('検算');
    return parts.join('・');
}

function updateSavebar() {
    const label = dirtyLabel();
    $('#savebar')?.classList.toggle('hidden', !label);
    if (label) $('#savebarText').textContent = `未保存: ${label}`;
}

function markTableDirty(acc) {
    dirty.tables.add(acc.dataset.table);
    const summary = $('summary', acc);
    if (!$('.js-dirty', summary)) {
        summary.append(el('span', { class: 'badge badge--accent js-dirty' }, '未保存'));
    }
    updateSavebar();
}

function clearTableDirty(acc) {
    dirty.tables.delete(acc.dataset.table);
    $('.js-dirty', acc)?.remove();
    updateSavebar();
}

/* まとまりのメモ。表と同じく summary に「未保存」の印を出す。
   印を付ける先が details.acc--group[data-group] である点だけが表と違う。 */
function groupBox(el_) { return el_.closest('details.acc--group'); }

function markGroupDirty(box) {
    const acc = groupBox(box);
    if (!acc) return;
    dirty.groups.add(acc.dataset.group);
    const summary = $('summary', acc);
    if (!$('.js-dirty', summary)) {
        summary.append(el('span', { class: 'badge badge--accent js-dirty' }, '未保存'));
    }
    updateSavebar();
}

function clearGroupDirty(box) {
    const acc = groupBox(box);
    if (!acc) return;
    dirty.groups.delete(acc.dataset.group);
    // 探す先は「まとまり自身の summary」に限る。acc の中には配下テーブルの
    // 未保存の印も入っているので、acc 全体から探すとそちらを消してしまう
    $('.js-dirty', $('summary', acc))?.remove();
    updateSavebar();
}

function setDirty(key, on = true) {
    dirty[key] = on;
    updateSavebar();
}

// アプリ都合の遷移（DB切替・再プロファイル・保存後の再読込）では警告を出さない
let leavingOnPurpose = false;
window.addEventListener('beforeunload', ev => {
    if (dirtyLabel() && !leavingOnPurpose) { ev.preventDefault(); ev.returnValue = ''; }
});
function reloadClean() { leavingOnPurpose = true; window.location.reload(); }

/** 読み直してよいか確かめる。書きかけがあれば聞く。

    reloadClean は「わざと離れる」印を立てるので、離脱時の警告も出ない。
    確かめずに読み直すと、他のタブに書きかけていた用語・例文・検算・説明が
    警告なしに全部消える。 */
function reloadCleanIfSaved() {
    const left = dirtyLabel();
    if (left && !confirm(`保存していない変更があります（${left}）。\n`
                         + 'このまま画面を読み直すと、その内容は失われます。よろしいですか？')) {
        toast('読み直しをやめました。先に保存してください。', 'err', 7000);
        return false;
    }
    reloadClean();
    return true;
}

/* --- 充実度（上部の数字） -------------------------------------------------------
   保存のたびに数え直す。ページを読み直さなくても数字が現実に追いつくように。 */

function recomputeMetrics() {
    const tabs = CAT.tables;
    const td = tabs.filter(t => t.description).length;
    const cd = tabs.reduce((n, t) => n + t.columns.filter(c => c.description).length, 0);
    const ct = tabs.reduce((n, t) => n + t.columns.length, 0);
    $('#mTables').textContent = `${td}/${tabs.length}`;
    $('#mCols').textContent = `${cd}/${ct}`;
    $('#mGloss').textContent = Object.keys(CAT.dbGlossary || {}).length
        + tabs.reduce((n, t) => n + Object.keys(t.glossary || {}).length, 0);
    $('#mEx').textContent = (CAT.examples || []).length;
}

/* --- テーブル説明 ------------------------------------------------------------ */

function parseValues(text) {
    const out = {};
    String(text || '').split(/[;\n]/).forEach(part => {
        const i = part.indexOf('=');
        if (i > 0) out[part.slice(0, i).trim()] = part.slice(i + 1).trim();
    });
    return out;
}

/** 1テーブル分を保存する。成功したら画面内の控え（CAT.tables）とバッジも合わせる。 */
async function saveTable(acc) {
    const table = acc.dataset.table;
    const desc = $('.t-desc', acc).value;
    const columns = {};
    $$('tr[data-col]', acc).forEach(tr => {
        columns[tr.dataset.col] = {
            description: $('.c-desc', tr).value,
            values: parseValues($('.c-vals', tr).value),
        };
    });
    await api('/api/catalog/table', { db: CAT.db, table, description: desc, columns });

    // 絞り込みと充実度は CAT.tables を見るので、保存内容をそちらへも反映する
    const t = CAT.tables.find(x => x.name === table);
    if (t) {
        t.description = desc.trim();
        t.ai_draft = false;
        t.columns.forEach(c => {
            const tr = acc.querySelector(`tr[data-col="${CSS.escape(c.name)}"]`);
            if (tr) c.description = $('.c-desc', tr).value.trim();
        });
    }
    const summary = $('summary', acc);
    // 消してよいのは「説明あり/なし」と「AI下書き」だけ。まとめて消すと、
    // サーバが描いた「ビュー」バッジ（実体のある表との唯一の見分け）まで落ちる
    $$('.badge', summary).forEach(b => {
        if (['説明あり', '説明なし', 'AI下書き・未確認', 'AI下書き'].includes(b.textContent)) b.remove();
    });
    summary.append(el('span', { class: `badge ${desc.trim() ? 'badge--ok' : 'badge--warn'}` },
        desc.trim() ? '説明あり' : '説明なし'));
    clearTableDirty(acc);
    recomputeMetrics();
}

/** まとまりのメモを1件保存する。保存できたら未保存の印と見出しのバッジを直す。 */
async function saveGroupMemo(box) {
    const memo = $('.g-memo', box).value;
    await api('/api/catalog/group',
        { db: CAT.db, group: box.dataset.group, description: memo });
    clearGroupDirty(box);
    // 「メモあり」はサーバ側で描いているので、保存後の見た目はここで合わせる
    const summary = $('summary', groupBox(box));
    $$('.badge--ok', summary).forEach(b => b.remove());
    if (memo.trim()) {
        summary.append(el('span', { class: 'badge badge--ok' }, 'メモあり'));
    }
}


/** 未保存のものを全部保存する（右下のバーと Ctrl+S から）。 */
async function saveAllDirty() {
    // :not(.t-manage) が要る。テーブルの中の「管理」ブロックは同じ data-table を
    // 持つが説明の入力欄が無いので、保存しようとすると英語のエラーが出る
    for (const acc of $$('#pane-tables details.acc[data-table]:not(.t-manage)')) {
        if (!dirty.tables.has(acc.dataset.table)) continue;
        try { await saveTable(acc); }
        catch (e) { toast(`${acc.dataset.table}: ${e.message}`, 'err', 8000); }
    }
    for (const box of $$('#pane-tables .gmemo')) {
        if (!dirty.groups.has(box.dataset.group)) continue;
        try { await saveGroupMemo(box); }
        catch (e) { toast(`${box.dataset.group}: ${e.message}`, 'err', 8000); }
    }
    if (dirty.glossary) await saveGlossary();
    if (dirty.examples) await saveExamples();
    if (dirty.checks) await saveChecks();
    if (!dirtyLabel()) toast('すべて保存しました。');
}

/* --- 管理（取り込み元・定期取り込み・更新履歴・削除） -----------------------------
   取り込み画面の「DBの管理」タブにあったものを、DBを見ているこの画面に集約した。
   描画は manage.js（両画面で共有）。ここでは /api/import/manage から
   このDBの分だけを取り出して、各テーブルの「管理」とDB情報の行に流し込む。 */
let manageData = null;

async function loadManage(force) {
    if (manageData && !force) return manageData;
    try {
        const m = await api('/api/import/manage', undefined, 'GET');
        manageData = m;
    } catch (e) {
        $('#dbManageInfo') && ($('#dbManageInfo').textContent = e.message);
        return null;
    }
    // 定期取り込みの全体状態（スケジューラ・宙に浮いた設定）
    renderSched(manageData.sched);
    renderOrphans(manageData.orphans || []);

    const d = (manageData.dbs || []).find(x => x.name === CAT.db);
    // DB情報の行: サイズ・更新日・削除ボタン
    const info = $('#dbManageInfo');
    if (info && d) {
        info.textContent = `${d.tables.length}テーブル ・ `
            + `${((d.size || 0) / 1024).toLocaleString(undefined, { maximumFractionDigits: 0 })} KB`
            + ` ・ 更新 ${d.mtime || '―'}`;
    }
    // 各テーブルの「管理」: 開いているものだけ描く（未開封は開いたときに描く）
    $$('.t-manage').forEach(acc => {
        if (acc.open) renderTableManage(acc);
    });
    return manageData;
}

/** テーブル1つぶんの管理欄を描く（manage.js の tableCard の中身を流用）。 */
function renderTableManage(acc) {
    const body = $('.t-manage__body', acc);
    const d = (manageData?.dbs || []).find(x => x.name === CAT.db);
    const t = d?.tables.find(x => x.name === acc.dataset.table);
    if (!t) {
        body.replaceChildren(el('div', { class: 'small muted' }, '管理情報を取得できませんでした。'));
        return;
    }
    // tableCard は <details> を返す。中身の acc__body だけをここに載せる
    const card = tableCard(CAT.db, t);
    const inner = card.querySelector('.acc__body');
    body.replaceChildren(...(inner ? [...inner.childNodes] : []));
    // 中身のサンプル行と更新履歴は、tableCard 側が toggle 時に読む設計なので手で呼ぶ
    const sampleBox = inner?.__sampleBox, histBox = inner?.__histBox;
    if (sampleBox && histBox) loadTableDetail(CAT.db, t.name, sampleBox, histBox);
}

function wireManage() {
    $$('.t-manage').forEach(acc => acc.addEventListener('toggle', async () => {
        if (!acc.open) return;
        await loadManage();
        renderTableManage(acc);
    }));
    // 定期取り込みの全体状態は開いてすぐ見えるようにする
    loadManage();
}

/* 一覧の行にある削除ボタン。summary の中なので、押しても開閉しないよう止める。 */
/* テーブルの説明・まとまりのメモは、中身に合わせて高さを伸ばす。
   2行固定だと3行目から見切れて、書いてあることに気づけない。
   閉じた折りたたみの中では高さを測れないので、開いた瞬間にも測り直す。 */
function wireGrowingNotes() {
    const all = $$('#pane-tables textarea.t-desc, #pane-tables textarea.g-memo');
    all.forEach(ta => ta.addEventListener('input', () => autoGrow(ta)));
    $$('#pane-tables details').forEach(d => d.addEventListener('toggle', () => {
        if (d.open) $$('textarea.t-desc, textarea.g-memo', d).forEach(ta => autoGrow(ta));
    }));
    all.forEach(ta => { if (ta.offsetParent) autoGrow(ta); });
}


function wireRowDelete() {
    $$('#pane-tables .t-drop').forEach(btn => {
        btn.addEventListener('click', ev => {
            ev.preventDefault();          // summary の既定動作（開閉）を止める
            ev.stopPropagation();
            askDeleteTable(CAT.db, btn.dataset.table, Number(btn.dataset.rows || 0),
                           btn.dataset.isView === '1');
        });
    });
}


function wireTables() {
    // どの入力欄をいじっても、そのテーブルに「未保存」の印を付ける
    $('#pane-tables').addEventListener('input', ev => {
        // :not(.t-manage) が要る。「管理」は同じ data-table を持つ入れ子なので、
        // 付けないと未保存の印がテーブル本体ではなく管理の見出しに付く
        const acc = ev.target.closest('details.acc[data-table]:not(.t-manage)');
        if (acc && ev.target.matches('.t-desc, .c-desc, .c-vals')) markTableDirty(acc);
        // まとまりのメモは表の外（acc--group 直下）にあるので別に拾う
        if (ev.target.matches('.g-memo')) markGroupDirty(ev.target);
    });

    // 同上。素で探すと1つのテーブルが本体と「管理」の2回当たる
    $$('details.acc[data-table]:not(.t-manage)').forEach(acc => {
        const table = acc.dataset.table;

        $('.t-save', acc)?.addEventListener('click', async ev => {
            ev.target.disabled = true;
            try {
                await saveTable(acc);
                toast(`${table} を保存しました。`);
            } catch (e) { toast(e.message, 'err'); }
            ev.target.disabled = false;
        });

        $('.t-draft', acc)?.addEventListener('click', async ev => {
            ev.target.disabled = true;
            ev.target.innerHTML = '<span class="spinner"></span> 生成中';
            try {
                const r = await api('/api/catalog/draft-table', { db: CAT.db, table });
                const d = r.draft || {};
                let filled = false;
                if (d.description && !$('.t-desc', acc).value.trim()) {
                    $('.t-desc', acc).value = d.description; filled = true;
                }
                Object.entries(d.columns || {}).forEach(([name, cd]) => {
                    const tr = acc.querySelector(`tr[data-col="${CSS.escape(name)}"]`);
                    if (!tr) return;
                    if (cd.description && !$('.c-desc', tr).value.trim()) {
                        $('.c-desc', tr).value = cd.description; filled = true;
                    }
                    if (cd.values && !$('.c-vals', tr).value.trim()) {
                        $('.c-vals', tr).value =
                            Object.entries(cd.values).map(([k, v]) => `${k}=${v}`).join('; ');
                        filled = true;
                    }
                });
                // スクリプトからの書き込みは input が飛ばないので、印は自分で付ける
                if (filled) markTableDirty(acc);
                toast('AIの下書きを入れました。内容を確認して保存してください。');
            } catch (e) { toast(e.message, 'err'); }
            ev.target.disabled = false;
            ev.target.textContent = 'AIに下書きさせる';
        });
    });
}

/* --- テーブルの絞り込み ---------------------------------------------------------
   検索対象は名前だけでなく、説明・コード値・実際の値も含める。
   「単価はどのテーブル？」「'出荷済' はどこに入っている？」に答えるため。 */

let missingOnly = false;

function applyTableFilter() {
    const q = $('#tblFilter').value.trim().toLowerCase();
    // :not(.t-manage) — 各テーブル内の管理アコーディオンも data-table を持つため除外
    const accs = $$('#pane-tables details.acc[data-table]:not(.t-manage)');
    let shown = 0;
    const matched = [];
    accs.forEach(acc => {
        const descNow = $('.t-desc', acc).value.trim();
        let hay = `${acc.dataset.table} ${descNow}`.toLowerCase();
        $$('tr[data-col]', acc).forEach(tr => {
            const rowText = [tr.dataset.col, $('.c-desc', tr).value, $('.c-vals', tr).value,
                             tr.cells[4]?.getAttribute('title') || ''].join(' ').toLowerCase();
            const hit = !!q && rowText.includes(q);
            tr.classList.toggle('is-hit', hit);     // 当たった列は行ごと着色
            hay += ' ' + rowText;
        });
        const show = (!q || hay.includes(q)) && (!missingOnly || !descNow);
        acc.classList.toggle('hidden', !show);
        if (show) { shown++; matched.push(acc); }
    });
    // 数件まで絞れたら開いて見せる（開いて回る手間を省く）
    if (q && shown && shown <= 4) matched.forEach(a => { a.open = true; });
    // 元DBグループ: 中身が全部消えたグループは隠し、絞り込み中はヒットを含む
    // グループを開いて見せる（閉じたままだとヒットが見えない）
    $$('#pane-tables details.acc--group').forEach(g => {
        const vis = $$('details.acc[data-table]:not(.t-manage):not(.hidden)', g);
        g.classList.toggle('hidden', !vis.length);
        if ((q || missingOnly) && vis.length) g.open = true;
    });
    const info = $('#tblFilterInfo');
    if (q || missingOnly) {
        info.classList.remove('hidden');
        info.textContent = `${accs.length}テーブル中 ${shown}件を表示`;
    } else {
        info.classList.add('hidden');
    }
}

function wireTableFilter() {
    $('#tblFilter').addEventListener('input', applyTableFilter);
    $('#tblMissing').addEventListener('click', ev => {
        missingOnly = !missingOnly;
        ev.target.classList.toggle('btn--primary', missingOnly);
        applyTableFilter();
    });
    $('#tblOpenAll').addEventListener('click', () => {
        $$('#pane-tables details.acc--group:not(.hidden)').forEach(g => { g.open = true; });
        $$('#pane-tables details.acc[data-table]:not(.t-manage):not(.hidden)')
            .forEach(a => { a.open = true; });
    });
    $('#tblCloseAll').addEventListener('click', () => {
        $$('#pane-tables details.acc[data-table]:not(.t-manage)').forEach(a => { a.open = false; });
        $$('#pane-tables details.acc--group').forEach(g => { g.open = false; });
    });
    // 元DBグループの開閉を覚える（クリック操作だけ保存。絞り込みによる自動開は保存しない）
    $$('#pane-tables details.acc--group').forEach(g => {
        const key = 'catGroup:' + CAT.db + ':' + g.dataset.group;
        try { if (localStorage.getItem(key) === '1') g.open = true; } catch (e) { /* 読めなければ既定のまま */ }
        $('summary', g)?.addEventListener('click', () => {
            setTimeout(() => { try { localStorage.setItem(key, g.open ? '1' : '0'); } catch (e) {} }, 0);
        });
    });
}

/* --- 用語集・例文（一覧＋エディタの2ペイン） ------------------------------------
   以前は全行が常に編集フォームで並び、件数が増えると走査も編集もつらかった。
   左に見渡すための一覧、右にいま選んだ1件だけのエディタ、という構成に分け、
   SQLを書く手が止まらないよう、列名を1クリックで式に挿せる参照を
   SQL欄のすぐ下に置く。行の実体は glItems / exItems（JSの配列）に持ち、
   画面はそこから描き直す。 */

const SCOPE_DB = '';                 // 「DB全体」を表す値
let glInitialScopes = new Set();     // 保存時に「空になった場所」も書き戻して消すため
let glItems = [], glSelId = null;    // 用語: {id, term, scope, description, sql, verdict, detail, dirty}
let exItems = [], exSelId = null;    // 例文: {id, q, description, sql, verdict, detail, dirty}
let idSeq = 0;
let glSec = 'gl';                    // いま開いている側（gl=用語集 / ex=例文）

/* SQLは1行に収まらないことが多いので、書いたぶんだけ伸びる欄にする */
function autoGrow(ta) {
    ta.style.height = 'auto';
    ta.style.height = Math.min(220, Math.max(34, ta.scrollHeight)) + 'px';
}

function growingSql(cls, value, placeholder) {
    const ta = el('textarea', { class: `${cls} mono`, rows: '1', placeholder }, value || '');
    ta.addEventListener('input', () => autoGrow(ta));
    // 一度でも触ったかどうか。参照からの挿入位置の判断に使う
    ta.addEventListener('focus', () => { ta.dataset.touched = '1'; });
    requestAnimationFrame(() => autoGrow(ta));
    return ta;
}

/* 検証結果の色。OK系は緑、0行は注意、エラーは赤 */
function verdictClass(verdict) {
    if (['エラー', '不一致'].includes(verdict)) return 'err';
    if (verdict === '0行') return 'warn';
    if (['条件式', '計算式', 'OK', '一致'].includes(verdict)) return 'ok';
    return '';
}

/* エディタ内の検証結果（バッジ＋説明文） */
function setStatus(box, it) {
    if (!it.verdict) { box.replaceChildren(); return; }
    const cls = verdictClass(it.verdict);
    box.replaceChildren(
        el('span', { class: `badge${cls ? ' badge--' + cls : ''}` }, it.verdict),
        el('span', { class: 'small muted' }, it.detail || ''));
    // 検証がデータを返してきたら、そのまま見せる（判定の根拠を目で確かめられる）
    if (it.columns && it.rows && it.rows.length) {
        box.append(el('div', { class: 'tablewrap mt', style: 'max-height:200px;overflow:auto' },
            el('table', { class: 'data' },
                el('thead', {}, el('tr', {}, ...it.columns.map(c => el('th', {}, String(c))))),
                el('tbody', {}, ...it.rows.map(r => el('tr', {},
                    ...r.map(v => el('td', {}, v === null || v === undefined ? '' : String(v)))))))));
    }
}

/* --- SQLの日本語解説 ----------------------------------------------------------
   よくある形（SELECT〜FROM〜JOIN〜WHERE〜GROUP BY〜ORDER BY）を機械的に読み下す。
   AIは使わない（費用ゼロ・即時・書き換えるたびに追随）。読めない形なら黙る。 */

function sqlToJapanese(sql) {
    let t = String(sql || '').replace(/\s+/g, ' ').trim().replace(/;$/, '');
    if (!t) return null;
    const out = [];

    const cte = t.match(/^WITH\s+(.+?)\s+(SELECT\s.+)$/i);
    if (cte) {
        const names = [...cte[1].matchAll(/([\w一-鿿々〇ぁ-ゖァ-ヺー]+)\s+AS\s*\(/gi)].map(m => m[1]);
        if (names.length) out.push(`前処理（WITH句）: ${names.join('、')} を先に作る`);
        t = cte[2];
    }
    const parts = t.split(/\bUNION\s+ALL\b/i);
    if (parts.length > 1) out.push(`${parts.length}個のSELECTを縦につなげる（UNION ALL）。以下は1つ目:`);
    t = parts[0].trim();

    const m = t.match(/^SELECT\s+(.+?)\s+FROM\s+(.+)$/i);
    if (!m) {
        // 用語のSQL式は「rank = 'A'」のような素の条件・計算式が多い
        if (/[=<>]|\bLIKE\b|\bIN\s*\(|\bIS\b|\bBETWEEN\b/i.test(t)) {
            return [...out, `条件: ${jaCond(t)} の行`];
        }
        if (/^[\w一-鿿々〇ぁ-ゖァ-ヺー.()*/+\-,'" %]+$/.test(t)) {
            return [...out, `計算式: ${jaCol(t)}`];
        }
        return out.length ? out : null;
    }
    let [, cols, rest] = m;

    // 後ろから順に切り出す
    const take = (re) => { const x = rest.match(re); if (x) rest = rest.slice(0, x.index).trim(); return x; };
    const limit = take(/\bLIMIT\s+(\d+)\s*$/i);
    const order = take(/\bORDER\s+BY\s+(.+)$/i);
    const group = take(/\bGROUP\s+BY\s+(.+)$/i);
    const where = take(/\bWHERE\s+(.+)$/i);

    // FROM と JOIN
    const joins = [];
    rest = rest.replace(/\b(?:LEFT\s+|INNER\s+)?JOIN\s+([\w一-鿿々〇ぁ-ゖァ-ヺー._]+)(?:\s+(?:AS\s+)?([\w一-鿿々〇ぁ-ゖァ-ヺー]+))?\s+ON\s+(.+?)(?=\b(?:LEFT\s+|INNER\s+)?JOIN\b|$)/gi,
        (_, tbl, ali, on) => { joins.push({ tbl, ali, on: on.trim() }); return ''; });
    const base = rest.trim().match(/^([\w一-鿿々〇ぁ-ゖァ-ヺー._()]+)(?:\s+(?:AS\s+)?([\w一-鿿々〇ぁ-ゖァ-ヺー]+))?/);

    const alias = x => (x ? `（略称 ${x}）` : '');
    if (base) out.push(`対象: ${base[1]}${alias(base[2])}`
        + joins.map(j => ` に ${j.tbl}${alias(j.ali)} を「${j.on}」でつなぐ`).join(''));
    if (where) out.push(`絞り込み: ${jaCond(where[1])}`);
    if (group) out.push(`まとめ方: ${group[1].trim()} ごとに集計`);
    out.push(`出すもの: ${splitCols(cols).map(jaCol).join('、 ')}`);
    if (order) out.push(`並び順: ${order[1].split(',').map(o => {
        const d = /\bDESC\b/i.test(o);
        return `${o.replace(/\b(DESC|ASC)\b/gi, '').trim()} の${d ? '大きい順' : '小さい順'}`;
    }).join('、 ')}`);
    if (limit) out.push(`先頭 ${limit[1]} 行だけ`);
    return out;
}

/** カンマで列を割る（関数の中のカンマは割らない） */
function splitCols(text) {
    const out = []; let depth = 0, cur = '';
    for (const ch of text) {
        if (ch === '(') depth++;
        if (ch === ')') depth--;
        if (ch === ',' && !depth) { out.push(cur.trim()); cur = ''; continue; }
        cur += ch;
    }
    if (cur.trim()) out.push(cur.trim());
    return out;
}

function jaCol(c) {
    const as = c.match(/\s+AS\s+([\w一-鿿々〇ぁ-ゖァ-ヺー"']+)\s*$/i);
    const name = as ? as[1].replace(/["']/g, '') : null;
    let body = as ? c.slice(0, as.index).trim() : c.trim();
    const fn = {
        'COUNT(*)': '件数', 'COUNT(1)': '件数',
    }[body.toUpperCase()];
    if (fn) body = fn;
    else body = body
        .replace(/^ROUND\((.+),\s*(\d+)\)$/i, (_, x, n) => `${x}（小数${n}桁で丸め）`)
        .replace(/^SUM\((.+)\)$/i, '$1 の合計')
        .replace(/^AVG\((.+)\)$/i, '$1 の平均')
        .replace(/^MIN\((.+)\)$/i, '$1 の最小')
        .replace(/^MAX\((.+)\)$/i, '$1 の最大')
        .replace(/^COUNT\(DISTINCT\s+(.+)\)$/i, '$1 の種類数')
        .replace(/^COUNT\((.+)\)$/i, '$1 の件数')
        .replace(/^CASE\s+WHEN[\s\S]+END$/i, '条件による値');
    return name && name !== body ? `${name}（= ${body}）` : body;
}

function jaCond(c) {
    return c
        .replace(/\s+AND\s+/gi, '、かつ ')
        .replace(/\s+OR\s+/gi, '、または ')
        .replace(/([\w一-鿿々〇ぁ-ゖァ-ヺー._]+)\s+LIKE\s+'([^']*)'/gi, (_, col, v) =>
            `${col} が「${v.replace(/%/g, '…')}」に一致`)
        .replace(/([\w一-鿿々〇ぁ-ゖァ-ヺー._]+)\s*=\s*'([^']*)'/g, '$1 が「$2」')
        .replace(/([\w一-鿿々〇ぁ-ゖァ-ヺー._]+)\s*!=\s*'([^']*)'/g, '$1 が「$2」以外')
        .replace(/([\w一-鿿々〇ぁ-ゖァ-ヺー._]+)\s*>=\s*([\w.']+)/g, '$1 が $2 以上')
        .replace(/([\w一-鿿々〇ぁ-ゖァ-ヺー._]+)\s*<=\s*([\w.']+)/g, '$1 が $2 以下')
        .replace(/\bBETWEEN\s+'([^']*)'\s+AND\s+'([^']*)'/gi, ' が「$1」〜「$2」の範囲')
        .replace(/\bIS\s+NULL\b/gi, ' が空')
        .replace(/\bIS\s+NOT\s+NULL\b/gi, ' が入っている');
}

/** SQL入力欄の下に置く解説。入力のたびに読み直す。 */
function sqlNote(ta) {
    const box = el('div', { class: 'sqlnote small muted' });
    const update = () => {
        const lines = ta.value.trim() ? sqlToJapanese(ta.value) : null;
        box.replaceChildren(...(lines ? [
            el('div', { class: 'sqlnote__head' }, 'このSQLがやっていること'),
            ...lines.map(l => el('div', {}, `・${l}`)),
        ] : []));
    };
    ta.addEventListener('input', update);
    update();
    return box;
}

/* 一覧の行頭の点。検証結果がひと目で分かるように */
function statusDot(it) {
    const cls = verdictClass(it.verdict);
    return el('span', { class: `dot${cls ? ' dot--' + cls : ''}`,
                        title: it.verdict ? `検証: ${it.verdict}${it.detail ? ' — ' + it.detail : ''}` : '未検証' });
}

const dirtyDot = it => it.dirty
    ? el('span', { class: 'dot dot--dirty', title: '未保存の変更' }) : null;

/* カーソル位置に文字列を挿し込む。参照の列名クリックから使う */
function insertIntoTa(ta, text) {
    let s = ta.selectionStart ?? ta.value.length;
    let e = ta.selectionEnd ?? s;
    // まだ一度も触っていない欄はカーソルが先頭にあるだけなので、末尾に足す
    if (!ta.dataset.touched) {
        s = e = ta.value.length;
        if (s && !/[\s(.,]$/.test(ta.value)) text = ' ' + text;
    }
    ta.value = ta.value.slice(0, s) + text + ta.value.slice(e);
    ta.selectionStart = ta.selectionEnd = s + text.length;
    ta.focus();
    // input を流して、未保存の印と欄の高さを通常の入力と同じ経路で更新する
    ta.dispatchEvent(new Event('input', { bubbles: true }));
}

/* --- 参照（エディタ内に出す、テーブルの中身） ------------------------------------ */

function fmtCodes(c) {
    return Object.entries(c.codes || {}).map(([k, v]) => `${k}=${v}`).join('; ');
}

function refTable(t, qualify, ta) {
    const head = el('thead', {}, el('tr', {},
        ['列', '型', '説明・コード値', '実際の値'].map(c => el('th', {}, c))));
    const body = el('tbody', {}, t.columns.map(c => {
        const ins = qualify ? `${t.name}.${c.name}` : c.name;
        const desc = [c.description, fmtCodes(c)].filter(Boolean).join(' ／ ');
        return el('tr', {},
            el('td', {}, el('button', { class: 'reflink', type: 'button',
                title: `クリックで「${ins}」をSQLに挿入`,
                onclick: () => insertIntoTa(ta, ins) }, c.name + (c.pk ? ' (PK)' : ''))),
            el('td', { class: 'muted' }, c.type),
            el('td', { class: 'muted', title: desc }, desc),
            el('td', { class: 'muted', title: c.actual }, c.actual));
    }));
    return el('div', { class: 'tablewrap' }, el('table', { class: 'data' }, head, body));
}

function sampleAcc(t) {
    if (!t.sample_rows?.length) return null;
    return el('details', { class: 'acc mt' },
        el('summary', {}, 'サンプル行を見る'),
        el('div', { class: 'acc__body' },
            el('div', { class: 'row mb', style: 'align-items:center' },
                el('span', { class: 'small muted' },
                    `先頭 ${t.sample_rows.length} 行のみ`),
                el('div', { class: 'spacer' }),
                tableViewLink(CAT.db, t.name)),
            dataTable(t.sample_columns, t.sample_rows)));
}

function rowsLabel(t) {
    return t.rows === null || t.rows === undefined ? '行数不明'
        : t.rows.toLocaleString() + '行';
}

/** テーブルを1つ選んでいればそれを開いて、DB全体なら全テーブルを畳んで見せる。 */
function refPanel(scope, ta) {
    const single = scope ? CAT.tables.find(x => x.name === scope) : null;
    const box = el('div', { class: 'refbox' });
    if (single) {
        box.append(
            el('div', { class: 'small muted mb' },
                `参照: ${single.name}（${rowsLabel(single)}）。列名をクリックするとSQLに入ります。`),
            refTable(single, false, ta), sampleAcc(single));
    } else if (CAT.tables.length) {
        box.append(el('div', { class: 'small muted mb' },
            '参照: テーブルを開いて列名をクリックすると「テーブル名.列名」の形でSQLに入ります。'));
        // 表が多いDB（統合後は114表）では、選ぶたびに全表のDOMを作ると固まる。
        // 一覧は名前だけ先に出し、中身は開いた瞬間に作る。探すための絞り込みも置く
        const flt = el('input', { type: 'text', class: 'mb',
            placeholder: 'テーブル名で絞り込み', style: 'max-width:260px' });
        box.append(flt);
        const rows = CAT.tables.map(t => {
            const body = el('div', { class: 'acc__body' });
            const acc = el('details', { class: 'acc', 'data-ref': t.name },
                el('summary', {}, el('strong', {}, t.name),
                    el('span', { class: 'muted small' }, `${rowsLabel(t)} / ${t.columns.length}列`)),
                body);
            acc.addEventListener('toggle', () => {
                if (acc.open && !body.childElementCount) {
                    body.append(refTable(t, true, ta), sampleAcc(t));
                }
            }, { once: false });
            box.append(acc);
            return acc;
        });
        flt.addEventListener('input', () => {
            const q = flt.value.trim().toLowerCase();
            rows.forEach(a => a.classList.toggle('hidden',
                !!q && !a.dataset.ref.toLowerCase().includes(q)));
        });
    }
    return box;
}

/* --- 用語集⇄例文の切り替え ----------------------------------------------------- */

function switchSec(sec) {
    glSec = sec;
    $('#sec-gl').classList.toggle('hidden', sec !== 'gl');
    $('#sec-ex').classList.toggle('hidden', sec !== 'ex');
    $('#sec-ck').classList.toggle('hidden', sec !== 'ck');
    $$('.seg__btn').forEach(b => b.classList.toggle('is-active', b.dataset.sec === sec));
    // 隠れている間は高さを測れないので、表示された側の伸びる欄を測り直す
    $$(`#sec-${sec} textarea`).forEach(autoGrow);
    if ($('#pane-glossary')?.classList.contains('is-active')) {
        history.replaceState(null, '', `#tab=glossary&sec=${sec}`);
    }
}

/* ↑↓キーで一覧を移動できるようにする（一覧にフォーカスがあるとき） */
function listArrowNav(ev, listSel, pick) {
    if (ev.key !== 'ArrowDown' && ev.key !== 'ArrowUp') return;
    ev.preventDefault();
    const btns = $$(`${listSel} .mlist__item`);
    if (!btns.length) return;
    const i = btns.findIndex(b => b.classList.contains('is-active'));
    const next = i === -1 ? btns[0] : btns[i + (ev.key === 'ArrowDown' ? 1 : -1)];
    if (next) pick(Number(next.dataset.id), true);
}

/* --- 用語集 ------------------------------------------------------------------- */

const glById = id => glItems.find(x => x.id === id);
const glScopeLabel = scope => scope || '全体（複数テーブル）';

/* 置き場所セレクトの選択肢。表名が「元DB名__表名」の規約なら optgroup でまとめる
   （統合後は114表がフラットに並んで選べないため）。value は生の表名のまま */
function scopeOptionGroups(selected) {
    const groups = new Map();
    CAT.tables.forEach(t => {
        const g = t.name.includes('__') ? t.name.split('__')[0] : '';
        if (!groups.has(g)) groups.set(g, []);
        groups.get(g).push(t.name);
    });
    const opt = name => el('option',
        { value: name, ...(selected === name ? { selected: 'selected' } : {}) }, name);
    if (groups.size <= 1) return CAT.tables.map(t => opt(t.name));
    return [...groups.entries()].flatMap(([g, names]) =>
        g ? [el('optgroup', { label: g }, ...names.map(opt))] : names.map(opt));
}

function markGlDirty(it) { it.dirty = true; setDirty('glossary'); }

/** 同じ置き場所に同じ用語が他にもあるか。保存すると片方しか残らないので警告する。 */
function glDupOf(it) {
    return glItems.some(x => x !== it && x.scope === it.scope
        && x.term.trim() && x.term.trim() === it.term.trim());
}

function loadGlossaryAll() {
    glItems = [];
    Object.entries(CAT.dbGlossary || {}).forEach(([term, v]) => glItems.push({
        id: ++idSeq, term, scope: SCOPE_DB,
        description: v.description || '', sql: v.sql || '',
        verdict: null, detail: '', dirty: false }));
    CAT.tables.forEach(t => Object.entries(t.glossary || {}).forEach(([term, v]) => glItems.push({
        id: ++idSeq, term, scope: t.name,
        description: v.description || '', sql: v.sql || '',
        verdict: null, detail: '', dirty: false })));
    glInitialScopes = new Set(glItems.map(r => r.scope));
    glSelId = glItems[0]?.id ?? null;
    glRenderList();
    glRenderEditor();
}

function glRenderList() {
    const q = ($('#glFilter')?.value || '').trim().toLowerCase();
    const groups = [[SCOPE_DB, glScopeLabel(SCOPE_DB)],
                    ...CAT.tables.map(t => [t.name, t.name])];
    const nodes = [];
    let shown = 0;
    for (const [scope, label] of groups) {
        const items = glItems.filter(it => it.scope === scope && (!q ||
            `${it.term} ${it.description} ${it.sql} ${label}`.toLowerCase().includes(q)));
        if (!items.length) continue;
        nodes.push(el('div', { class: 'mlist__group' }, `${label}（${items.length}）`));
        items.forEach(it => {
            shown++;
            nodes.push(el('button', {
                class: `mlist__item${it.id === glSelId ? ' is-active' : ''}`,
                type: 'button', 'data-id': it.id,
                onclick: () => glSelect(it.id),
            },
                statusDot(it),
                el('span', { class: 'mlist__term' }, it.term || '（無題）'),
                el('span', { class: 'mlist__desc' }, it.description || it.sql || ''),
                dirtyDot(it)));
        });
    }
    if (!nodes.length) {
        nodes.push(el('div', { class: 'mlist__empty' },
            glItems.length ? '絞り込みに当たる用語がありません。'
                           : 'まだ用語がありません。「＋ 用語を追加」から登録してください。'));
    }
    $('#glList').replaceChildren(...nodes);
    $('#glCount').textContent = q ? `${glItems.length}件中 ${shown}件` : `${glItems.length}件`;
    $('#segGlN').textContent = glItems.length;
}

function glSelect(id, focusList = false) {
    glSelId = id;
    glRenderList();
    glRenderEditor();
    const btn = $(`#glList .mlist__item[data-id="${id}"]`);
    btn?.scrollIntoView({ block: 'nearest' });
    if (focusList) btn?.focus();
}

function glAdd() {
    // 置き場所は、いま見ている用語と同じ所を最初の候補にする
    const cur = glById(glSelId);
    const it = { id: ++idSeq, term: '',
                 scope: cur ? cur.scope : (CAT.tables[0]?.name ?? SCOPE_DB),
                 description: '', sql: '', verdict: null, detail: '', dirty: true };
    glItems.push(it);
    glSelect(it.id);
    $('#glEditor .ed-term')?.focus();
}

/** AIの下書きの結果（式の解説／書けなかった理由）。人が式を直したら下ろす。 */
function glDraftNote(it) {
    const n = it.draftNote;
    if (!n || !n.text) return null;
    return el('div', { class: n.kind === 'ok' ? 'alert alert--info mt' : 'alert alert--warn mt' },
        el('div', { class: 'mb' }, el('b', {},
            n.kind === 'ok' ? 'この式がしていること' : 'SQL式にできませんでした')),
        el('div', { style: 'white-space:pre-wrap' }, n.text));
}


function glRenderEditor() {
    const box = $('#glEditor');
    const it = glById(glSelId);
    if (!it) {
        box.replaceChildren(el('div', { class: 'editcard editcard--empty' },
            el('div', {},
                el('div', { class: 'muted mb' }, glItems.length
                    ? '左の一覧から用語を選んでください。'
                    : 'まだ用語がありません。最初の用語を登録しましょう。'),
                el('button', { class: 'btn btn--sm', type: 'button', onclick: glAdd },
                    '＋ 用語を追加'))));
        return;
    }

    const term = el('input', { type: 'text', class: 'ed-term', value: it.term,
        placeholder: '用語（例: 有効な受注）' });
    const scopeSel = el('select', { title: 'この用語の置き場所' },
        el('option', { value: SCOPE_DB, ...(it.scope === SCOPE_DB ? { selected: 'selected' } : {}) },
            '全体（複数テーブル）'),
        ...scopeOptionGroups(it.scope));
    const desc = el('input', { type: 'text', value: it.description,
        placeholder: '説明（自然言語でOK。例: キャンセル以外の、実際に売上になる受注）' });
    const sql = growingSql('ed-sql', it.sql, "SQL条件・計算式（任意。例: status != '9'）");
    const dup = el('div', { class: 'small ed-dup hidden' });
    const status = el('div', { class: 'vstatus' });
    setStatus(status, it);

    const showDup = () => {
        const bad = !!it.term.trim() && glDupOf(it);
        dup.classList.toggle('hidden', !bad);
        if (bad) dup.textContent = `「${it.term.trim()}」は「${glScopeLabel(it.scope)}」に`
            + '既にあります。保存する前に1つにまとめてください。';
    };
    showDup();

    term.addEventListener('input', () => {
        it.term = term.value; markGlDirty(it); glRenderList(); showDup();
    });
    desc.addEventListener('input', () => {
        it.description = desc.value; markGlDirty(it); glRenderList();
    });
    sql.addEventListener('input', () => {
        if (it.sql === sql.value) return;
        // 式が変わったら前の検証結果もAIの解説もあてにならないので消す
        it.sql = sql.value; it.verdict = null; it.detail = '';
        if (it.draftNote) { it.draftNote = null; glRenderEditor(); return; }
        setStatus(status, it); markGlDirty(it); glRenderList();
    });
    scopeSel.addEventListener('change', () => {
        it.scope = scopeSel.value;
        it.verdict = null; it.detail = '';
        markGlDirty(it);
        glRenderList();
        glRenderEditor();          // 参照パネルを新しい置き場所に合わせて作り直す
    });

    const draftBtn = el('button', {
        class: 'btn btn--sm', type: 'button',
        ...(CAT.llmReady ? {} : { disabled: 'disabled' }),
        title: '説明をもとに、AIがこの用語のSQL式を下書きします',
        onclick: async () => {
            if (!it.term.trim() || !it.description.trim()) {
                toast('先に用語と説明を書いてください。', 'warn'); return;
            }
            draftBtn.disabled = true;
            draftBtn.innerHTML = '<span class="spinner"></span> 生成中';
            try {
                const key = it.term.trim();
                const r = await api('/api/catalog/glossary/draft',
                    { db: CAT.db, table: it.scope || null,
                      terms: [{ term: key, description: it.description.trim() }] });
                const drafted = (r.drafted || {})[key];
                if (drafted) {
                    it.sql = drafted; it.verdict = null; it.detail = '';
                    // AIの解説は、この式が何をしているかの説明。編集すると当てはまらなくなる
                    it.draftNote = { kind: 'ok', text: (r.explanations || {})[key] || '' };
                    markGlDirty(it);
                    glRenderList(); glRenderEditor();
                    toast('SQL式を下書きしました。「検証」で確かめてから保存してください。');
                    return;        // エディタは作り直したので、このボタンはもう無い
                }
                // 書けなかった理由をその場に出す（定型文で終わらせない）
                it.draftNote = { kind: 'ng', text: (r.reasons || {})[key]
                    || 'この説明からはSQL式を決められませんでした。' };
                glRenderEditor();
                toast('SQL式にできませんでした。理由を確かめてください。', 'warn', 8000);
                return;            // エディタを作り直したので、このボタンはもう無い
            } catch (e) { toast(e.message, 'err'); }
            draftBtn.disabled = !CAT.llmReady;
            draftBtn.textContent = 'AIで下書き';
        },
    }, 'AIで下書き');

    const verifyBtn = el('button', { class: 'btn btn--sm', type: 'button',
        title: 'SQL式を実データに当てて確かめる',
        onclick: () => glVerify([it]) }, '検証');

    const delBtn = el('button', { class: 'btn btn--sm btn--danger', type: 'button',
        onclick: () => {
            if (!confirm(`用語「${it.term || '（無題）'}」を削除しますか？（「保存」までは確定しません）`)) return;
            const i = glItems.indexOf(it);
            glItems.splice(i, 1);
            glSelId = (glItems[i] || glItems[i - 1])?.id ?? null;
            setDirty('glossary');
            glRenderList(); glRenderEditor();
        } }, '削除');

    box.replaceChildren(el('div', { class: 'editcard' },
        el('div', { class: 'row' },
            el('div', { class: 'grow' }, el('label', { class: 'field' }, '用語'), term),
            el('div', { style: 'width:230px' },
                el('label', { class: 'field' }, '置き場所'), scopeSel),
            delBtn),
        dup,
        el('div', { class: 'mt' },
            el('label', { class: 'field' }, '説明（自然言語で構いません）'), desc),
        el('div', { class: 'mt' },
            el('div', { class: 'row', style: 'align-items:center;margin-bottom:6px' },
                el('label', { class: 'field', style: 'margin:0' },
                    'SQL条件・計算式（任意。空欄なら説明からAIが組み立てます）'),
                el('div', { class: 'spacer' }), draftBtn, verifyBtn),
            sql,
            sqlNote(sql)),
        glDraftNote(it),
        status,
        refPanel(it.scope, sql)));
}

async function glVerify(items, btn) {
    const rows = items.filter(r => r.term.trim());
    if (!rows.length) { toast('検証する用語がありません。', 'warn'); return; }
    let orig;
    if (btn) {
        orig = btn.textContent;
        btn.disabled = true;
        btn.innerHTML = '<span class="spinner"></span> 検証中';
    }
    // 検証APIは置き場所ごとなので、まとめて呼んで結果を各行へ戻す
    const byScope = new Map();
    rows.forEach(r => {
        if (!byScope.has(r.scope)) byScope.set(r.scope, []);
        byScope.get(r.scope).push(r);
    });
    for (const [scope, list] of byScope) {
        try {
            const res = await api('/api/catalog/glossary/verify',
                { db: CAT.db, table: scope || null,
                  terms: list.map(r => ({ term: r.term, sql: r.sql })) });
            res.results.forEach((x, i) => { list[i].verdict = x.verdict; list[i].detail = x.detail;
                                            list[i].columns = x.columns; list[i].rows = x.rows; });
        } catch (e) { toast(e.message, 'err'); }
    }
    if (btn) { btn.disabled = false; btn.textContent = orig; }
    glRenderList();
    glRenderEditor();
}

/** 用語集を保存する。行を場所ごとにまとめ、空になった場所も書き戻して消す。 */
async function saveGlossary() {
    const rows = glItems.filter(r => r.term.trim());

    // 同じ場所に同じ用語が2つあると後の1つしか残らないので、先に止める
    for (const r of rows) {
        if (glDupOf(r)) {
            toast(`「${r.term.trim()}」が同じ場所（${glScopeLabel(r.scope)}）に2回あります。`
                  + '1つにまとめてください。', 'err', 8000);
            glSelect(r.id);
            return;
        }
    }

    const byScope = new Map();
    rows.forEach(r => {
        if (!byScope.has(r.scope)) byScope.set(r.scope, []);
        byScope.get(r.scope).push(r);
    });
    try {
        for (const scope of new Set([...glInitialScopes, ...byScope.keys()])) {
            const terms = (byScope.get(scope) || []).map(r =>
                ({ term: r.term.trim(), description: r.description.trim(), sql: r.sql.trim() }));
            // 印は「用語集ぜんぶ」に対して1つ。1件目で通れば以降は自分の書き込みで
            // 変わるので、応答で受け取った新しい印に差し替えながら続ける
            const gr = await api('/api/catalog/glossary',
                { db: CAT.db, table: scope || null, terms, stamp: CAT.stamps?.glossary });
            if (gr.stamp) CAT.stamps.glossary = gr.stamp;
            const obj = {};
            terms.forEach(t => { obj[t.term] = { description: t.description, sql: t.sql }; });
            if (scope) {
                const t = CAT.tables.find(x => x.name === scope);
                if (t) t.glossary = obj;
            } else {
                CAT.dbGlossary = obj;
            }
        }
    } catch (e) { toast(e.message, 'err'); return; }
    glInitialScopes = new Set(byScope.keys());

    // まっさらな行は片付ける。用語名が無くて保存されなかった行は消さずに知らせる
    glItems = glItems.filter(r => r.term.trim() || r.description.trim() || r.sql.trim());
    const nameless = glItems.filter(r => !r.term.trim());
    glItems.forEach(r => { if (r.term.trim()) r.dirty = false; });
    if (!glById(glSelId)) glSelId = glItems[0]?.id ?? null;
    setDirty('glossary', !!nameless.length);
    recomputeMetrics();
    glRenderList();
    glRenderEditor();
    toast(nameless.length
        ? '用語集を保存しました（用語名が空の行は保存されていません）。'
        : '用語集を保存しました。');
}

/** 説明だけ書かれた用語すべてに、AIでSQL式を一括下書きする。 */
async function draftGlossary(btn) {
    const targets = glItems.filter(r => r.term.trim() && r.description.trim() && !r.sql.trim());
    if (!targets.length) {
        toast('SQL式が空で、説明が書かれている用語がありません。', 'warn');
        return;
    }
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner"></span> 変換中';
    const byScope = new Map();
    targets.forEach(r => {
        if (!byScope.has(r.scope)) byScope.set(r.scope, []);
        byScope.get(r.scope).push(r);
    });
    let n = 0;
    for (const [scope, list] of byScope) {
        try {
            const r = await api('/api/catalog/glossary/draft',
                { db: CAT.db, table: scope || null,
                  terms: list.map(x => ({ term: x.term.trim(), description: x.description.trim() })) });
            list.forEach(x => {
                const sql = (r.drafted || {})[x.term.trim()];
                if (sql) { x.sql = sql; x.verdict = null; x.detail = ''; x.dirty = true; n++; }
            });
        } catch (e) { toast(e.message, 'err'); }
    }
    if (n) setDirty('glossary');
    glRenderList();
    glRenderEditor();
    toast(n ? `${n}件のSQL式を下書きしました。「すべて検証」で確かめてから保存してください。`
            : 'AIが判断できませんでした。説明をもう少し具体的に書いてみてください。',
          n ? 'ok' : 'warn');
    btn.disabled = false;
    btn.textContent = '説明からSQL式を下書き';
}

function wireGlossary() {
    $('#glFilter').addEventListener('input', glRenderList);
    $('#glAdd').addEventListener('click', glAdd);
    $('#glDraft').addEventListener('click', ev => draftGlossary(ev.currentTarget));
    $('#glVerifyAll').addEventListener('click', ev => glVerify(glItems, ev.currentTarget));
    $('#glSave').addEventListener('click', saveGlossary);
    $('#glList').addEventListener('keydown', ev => listArrowNav(ev, '#glList', glSelect));
    $$('.seg__btn').forEach(b => b.addEventListener('click', () => switchSec(b.dataset.sec)));
}

/* --- 例文 --------------------------------------------------------------------- */

const exById = id => exItems.find(x => x.id === id);

function markExDirty(it) { it.dirty = true; setDirty('examples'); }

function loadExamples() {
    exItems = (CAT.examples || []).map(e => ({ id: ++idSeq, q: e.q || '',
        description: e.description || '', sql: e.sql || '',
        verdict: null, detail: '', dirty: false }));
    exSelId = exItems[0]?.id ?? null;
    exRenderList();
    exRenderEditor();
}

function exRenderList() {
    const q = ($('#exFilter')?.value || '').trim().toLowerCase();
    const nodes = [];
    let shown = 0;
    exItems.forEach(it => {
        if (q && !`${it.q} ${it.description} ${it.sql}`.toLowerCase().includes(q)) return;
        shown++;
        nodes.push(el('button', {
            class: `mlist__item${it.id === exSelId ? ' is-active' : ''}`,
            type: 'button', 'data-id': it.id,
            onclick: () => exSelect(it.id),
        },
            statusDot(it),
            el('span', { class: 'mlist__q' }, it.q || '（質問未入力）'),
            it.description ? el('span', { class: 'mlist__desc' }, it.description) : null,
            dirtyDot(it)));
    });
    if (!nodes.length) {
        nodes.push(el('div', { class: 'mlist__empty' },
            exItems.length ? '絞り込みに当たる例文がありません。'
                           : 'まだ例文がありません。「＋ 例文を追加」から登録してください。'));
    }
    $('#exList').replaceChildren(...nodes);
    const exMax = CAT.examplesMax || 200;
    $('#exCount').textContent = q ? `${exItems.length}件中 ${shown}件`
                                  : `${exItems.length}件 / 上限${exMax}件`;
    $('#segExN').textContent = exItems.length;
    const add = $('#exAdd');
    add.disabled = exItems.length >= exMax;
    add.title = add.disabled ? `例文は${exMax}件までです。使わないものを削除してください。` : '';
}

function exSelect(id, focusList = false) {
    exSelId = id;
    exRenderList();
    exRenderEditor();
    const btn = $(`#exList .mlist__item[data-id="${id}"]`);
    btn?.scrollIntoView({ block: 'nearest' });
    if (focusList) btn?.focus();
}

function exAdd() {
    const exMax = CAT.examplesMax || 200;
    if (exItems.length >= exMax) { toast(`例文は${exMax}件までです。`, 'warn'); return; }
    const it = { id: ++idSeq, q: '', description: '', sql: '',
                 verdict: null, detail: '', dirty: true };
    exItems.push(it);
    exSelect(it.id);
    $('#exEditor .ed-q')?.focus();
}

function exRenderEditor() {
    const box = $('#exEditor');
    const it = exById(exSelId);
    if (!it) {
        box.replaceChildren(el('div', { class: 'editcard editcard--empty' },
            el('div', {},
                el('div', { class: 'muted mb' }, exItems.length
                    ? '左の一覧から例文を選んでください。'
                    : 'まだ例文がありません。最初の例文を登録しましょう。'),
                el('button', { class: 'btn btn--sm', type: 'button', onclick: exAdd },
                    '＋ 例文を追加'))));
        return;
    }

    const q = el('input', { type: 'text', class: 'ed-q', value: it.q,
        placeholder: '質問（例: 部門別の平均残業時間を教えて）' });
    const desc = el('input', { type: 'text', value: it.description,
        placeholder: '説明（任意。例: 残業は分で入っているので60で割る。休職者は含めない）' });
    const sql = growingSql('ed-sql', it.sql, 'SELECT ...');
    const status = el('div', { class: 'vstatus' });
    setStatus(status, it);

    q.addEventListener('input', () => {
        it.q = q.value; markExDirty(it); exRenderList();
    });
    desc.addEventListener('input', () => {
        it.description = desc.value; markExDirty(it); exRenderList();
    });
    sql.addEventListener('input', () => {
        if (it.sql === sql.value) return;
        it.sql = sql.value; it.verdict = null; it.detail = '';
        setStatus(status, it); markExDirty(it); exRenderList();
    });

    const verifyBtn = el('button', { class: 'btn btn--sm', type: 'button',
        title: 'このSQLが実際に通るか確かめる',
        onclick: () => exVerify([it]) }, '検証');

    // 例文は「日本語の質問＋確認済みのSQL」なので、そのままツールの中身になる。
    // よく聞かれる質問はツールにしておくと、AIが毎回書き起こさずに済む。
    const toolBtn = el('button', { class: 'btn btn--sm', type: 'button',
        title: 'この例文をもとに、AIが呼び出せるツールを作る',
        onclick: () => {
            if (!it.q.trim() || !it.sql.trim()) {
                toast('質問とSQLの両方が要ります。', 'warn');
                return;
            }
            openToolWizard({ purpose: it.description
                ? `${it.q}（${it.description}）` : it.q, sql: it.sql });
        } }, 'ツールにする');

    const delBtn = el('button', { class: 'btn btn--sm btn--danger', type: 'button',
        onclick: () => {
            if (!confirm('この例文を削除しますか？（「保存」までは確定しません）')) return;
            const i = exItems.indexOf(it);
            exItems.splice(i, 1);
            exSelId = (exItems[i] || exItems[i - 1])?.id ?? null;
            setDirty('examples');
            exRenderList(); exRenderEditor();
        } }, '削除');

    box.replaceChildren(el('div', { class: 'editcard' },
        el('div', { class: 'row' },
            el('div', { class: 'grow' }, el('label', { class: 'field' }, '質問'), q),
            delBtn),
        el('div', { class: 'mt' },
            el('label', { class: 'field' },
                '説明（任意。この例をどう読めばよいかをAIに伝える）'), desc),
        el('div', { class: 'mt' },
            el('div', { class: 'row', style: 'align-items:center;margin-bottom:6px' },
                el('label', { class: 'field', style: 'margin:0' },
                    'SQL（この質問への正しい答えを返すSELECT）'),
                el('div', { class: 'spacer' }), toolBtn, verifyBtn),
            sql,
            sqlNote(sql)),
        status,
        refPanel(SCOPE_DB, sql)));
}

// 例文はAIに「正しい例」として渡すので、通らないSQLが混ざると害になる
async function exVerify(items, btn) {
    const rows = items.filter(r => r.q.trim() || r.sql.trim());
    if (!rows.length) { toast('検証する例文がありません。', 'warn'); return; }
    let orig;
    if (btn) {
        orig = btn.textContent;
        btn.disabled = true;
        btn.innerHTML = '<span class="spinner"></span> 検証中';
    }
    try {
        const r = await api('/api/catalog/examples/verify',
            { db: CAT.db, examples: rows.map(x => ({ q: x.q, sql: x.sql })) });
        r.results.forEach((x, i) => { rows[i].verdict = x.verdict; rows[i].detail = x.detail;
                                      rows[i].columns = x.columns; rows[i].rows = x.rows; });
    } catch (e) { toast(e.message, 'err'); }
    if (btn) { btn.disabled = false; btn.textContent = orig; }
    exRenderList();
    exRenderEditor();
}

/** 例文を保存する。サーバ側で重複がまとめられたら、その結果に画面も揃える。 */
async function saveExamples() {
    let r;
    try {
        r = await api('/api/catalog/examples',
            { db: CAT.db, stamp: CAT.stamps?.examples,
              examples: exItems.map(x => ({ q: x.q.trim(),
                description: x.description.trim(), sql: x.sql.trim() })) });
    } catch (e) { toast(e.message, 'err', e.data?.stale ? 12000 : 5000); return; }
    CAT.examples = r.examples || [];
    if (r.stamp) CAT.stamps.examples = r.stamp;   // 続けて保存できるように

    // サーバの確定結果で作り直す。検証結果は内容が同じ行へ引き継ぐ
    const key = x => `${x.q.trim()}\u0000${x.sql.trim()}`;
    const old = new Map(exItems.map(x => [key(x), x]));
    const selKey = exById(exSelId) ? key(exById(exSelId)) : null;
    const kept = CAT.examples.map(e => {
        const o = old.get(`${e.q}\u0000${e.sql}`);
        return { id: ++idSeq, q: e.q, description: e.description || '', sql: e.sql,
                 verdict: o?.verdict ?? null, detail: o?.detail ?? '', dirty: false };
    });
    // 質問とSQLが揃っていない行は保存されないので、書きかけを消さずに残す
    const partial = exItems.filter(x =>
        (x.q.trim() || x.sql.trim() || x.description.trim()) && !(x.q.trim() && x.sql.trim()));
    exItems = [...kept, ...partial];
    exSelId = (exItems.find(x => key(x) === selKey) || exItems[0])?.id ?? null;
    setDirty('examples', !!partial.length);
    recomputeMetrics();
    exRenderList();
    exRenderEditor();
    if (r.warning) {
        toast(`例文を保存しました。${r.warning}`, 'warn', 10000);
    } else if (r.dropped) {
        toast(`例文を保存しました。質問とSQLが同じ重複 ${r.dropped} 件をまとめました。`, 'ok', 7000);
    } else {
        toast(partial.length
            ? '例文を保存しました（質問とSQLが揃っていない行は保存されていません）。'
            : '例文を保存しました。');
    }
}

function wireExamples() {
    loadExamples();
    $('#exFilter').addEventListener('input', exRenderList);
    $('#exAdd').addEventListener('click', exAdd);
    $('#exVerifyAll').addEventListener('click', ev => exVerify(exItems, ev.currentTarget));
    $('#exSave').addEventListener('click', saveExamples);
    $('#exList').addEventListener('keydown', ev => listArrowNav(ev, '#exList', exSelect));
}

/* --- 検算（一致するはずの2つの数字） --------------------------------------------
   登録しておくと、AIが関係するテーブルに触れるたびに自動で突き合わせ、
   食い違っていればチャットに警告が出る（verify.py）。ここはその管理画面。 */

let ckItems = [], ckSelId = null;

const ckById = id => ckItems.find(x => x.id === id);

function markCkDirty(it) { it.dirty = true; setDirty('checks'); }

function loadChecks() {
    ckItems = (CAT.checks || []).map(c => ({
        id: ++idSeq, name: c.name || '',
        left_label: (c.left || {}).label || '', left_sql: (c.left || {}).sql || '',
        right_label: (c.right || {}).label || '', right_sql: (c.right || {}).sql || '',
        tolerance_pct: c.tolerance_pct ?? 0.5,
        drilldown: c.drilldown || '', enabled: c.enabled !== false,
        verdict: null, detail: '', dirty: false }));
    ckSelId = ckItems[0]?.id ?? null;
    ckRenderList();
    ckRenderEditor();
}

function ckPayload(it) {
    return { name: it.name.trim(),
             left: { label: it.left_label.trim(), sql: it.left_sql.trim() },
             right: { label: it.right_label.trim(), sql: it.right_sql.trim() },
             tolerance_pct: Number(it.tolerance_pct) || 0,
             drilldown: it.drilldown.trim(), enabled: !!it.enabled };
}

function ckRenderList() {
    const nodes = [];
    ckItems.forEach(it => {
        nodes.push(el('button', {
            class: `mlist__item${it.id === ckSelId ? ' is-active' : ''}`,
            type: 'button', 'data-id': it.id,
            onclick: () => ckSelect(it.id),
        },
            statusDot(it),
            el('span', { class: 'mlist__term' }, it.name || '（無題）'),
            el('span', { class: 'mlist__desc' },
                it.enabled ? `${it.left_label || '左'} = ${it.right_label || '右'}` : '無効'),
            dirtyDot(it)));
    });
    if (!nodes.length) {
        nodes.push(el('div', { class: 'mlist__empty' },
            'まだ検算ルールがありません。「＋ ルールを追加」から登録してください。'));
    }
    $('#ckList').replaceChildren(...nodes);
    $('#ckCount').textContent = `${ckItems.length}件`;
    $('#segCkN').textContent = ckItems.length;
}

function ckSelect(id, focusList = false) {
    ckSelId = id;
    ckRenderList();
    ckRenderEditor();
    const btn = $(`#ckList .mlist__item[data-id="${id}"]`);
    btn?.scrollIntoView({ block: 'nearest' });
    if (focusList) btn?.focus();
}

function ckAdd() {
    const it = { id: ++idSeq, name: '', left_label: '', left_sql: '',
                 right_label: '', right_sql: '', tolerance_pct: 0.5,
                 drilldown: '', enabled: true,
                 verdict: null, detail: '', dirty: true };
    ckItems.push(it);
    ckSelect(it.id);
    $('#ckEditor .ed-name')?.focus();
}

function ckSetStatus(box, it) {
    if (!it.verdict) { box.replaceChildren(); return; }
    const cls = verdictClass(it.verdict);
    box.replaceChildren(
        el('span', { class: `badge${cls ? ' badge--' + cls : ''}` }, it.verdict),
        el('span', { class: 'small muted' }, it.detail || ''));
}

function ckRenderEditor() {
    const box = $('#ckEditor');
    const it = ckById(ckSelId);
    if (!it) {
        box.replaceChildren(el('div', { class: 'editcard editcard--empty' },
            el('div', {},
                el('div', { class: 'muted mb' },
                    '一致するはずの2つの数字を、左右のSQLで登録します。'),
                el('button', { class: 'btn btn--sm', type: 'button', onclick: ckAdd },
                    '＋ ルールを追加'))));
        return;
    }

    const bind = (input, key, opts = {}) => {
        input.addEventListener('input', () => {
            it[key] = opts.number ? input.value : input.value;
            if (opts.resetVerdict !== false) { it.verdict = null; it.detail = ''; }
            markCkDirty(it); ckRenderList();
        });
        return input;
    };

    const name = bind(el('input', { type: 'text', class: 'ed-name', value: it.name,
        placeholder: '名前（例: 入金と請求の一致）' }), 'name');
    const enabled = el('input', { type: 'checkbox',
        ...(it.enabled ? { checked: 'checked' } : {}) });
    enabled.addEventListener('change', () => {
        it.enabled = enabled.checked; markCkDirty(it); ckRenderList();
    });
    const llabel = bind(el('input', { type: 'text', value: it.left_label,
        placeholder: '左の名前（例: 入金の合計）' }), 'left_label');
    const lsql = bind(growingSql('ed-lsql', it.left_sql,
        'SELECT SUM(...) FROM ...（1行1列を返すこと）'), 'left_sql');
    const rlabel = bind(el('input', { type: 'text', value: it.right_label,
        placeholder: '右の名前（例: 請求のうち入金済み）' }), 'right_label');
    const rsql = bind(growingSql('ed-rsql', it.right_sql,
        'SELECT SUM(...) FROM ...（1行1列を返すこと）'), 'right_sql');
    const tol = bind(el('input', { type: 'number', value: it.tolerance_pct,
        min: '0', step: '0.1', style: 'width:110px' }), 'tolerance_pct',
        { number: true });
    const drill = bind(growingSql('ed-drill', it.drilldown,
        '差の内訳を出すSELECT（任意。不一致のとき警告と一緒に表示されます）'),
        'drilldown');
    const status = el('div', { class: 'vstatus' });
    ckSetStatus(status, it);

    const verifyBtn = el('button', { class: 'btn btn--sm', type: 'button',
        title: '左右のSQLをいま実行して、値と差を確かめる',
        onclick: () => ckVerify([it]) }, '検算');

    const delBtn = el('button', { class: 'btn btn--sm btn--danger', type: 'button',
        onclick: () => {
            if (!confirm(`検算ルール「${it.name || '（無題）'}」を削除しますか？（「保存」までは確定しません）`)) return;
            const i = ckItems.indexOf(it);
            ckItems.splice(i, 1);
            ckSelId = (ckItems[i] || ckItems[i - 1])?.id ?? null;
            setDirty('checks');
            ckRenderList(); ckRenderEditor();
        } }, '削除');

    box.replaceChildren(el('div', { class: 'editcard' },
        el('div', { class: 'row' },
            el('div', { class: 'grow' }, el('label', { class: 'field' }, '名前'), name),
            el('label', { class: 'check', style: 'align-self:flex-end;padding-bottom:8px' },
                enabled, el('span', {}, '有効')),
            delBtn),
        el('div', { class: 'mt' },
            el('label', { class: 'field' }, '左の数字（名前とSQL。1行1列のSELECT）'),
            llabel, el('div', { style: 'height:6px' }), lsql),
        el('div', { class: 'mt' },
            el('label', { class: 'field' }, '右の数字（左と一致するはずのもの）'),
            rlabel, el('div', { style: 'height:6px' }), rsql),
        el('div', { class: 'row mt', style: 'align-items:center' },
            el('label', { class: 'field', style: 'margin:0' }, '許容差(%)'), tol,
            el('div', { class: 'spacer' }), verifyBtn),
        el('div', { class: 'mt' },
            el('label', { class: 'field' }, '差の内訳SQL（任意）'), drill),
        status));
}

async function ckVerify(items, btn) {
    const targets = items.filter(it => it.left_sql.trim() && it.right_sql.trim());
    if (!targets.length) { toast('左右のSQLが入っているルールがありません。', 'warn'); return; }
    let orig;
    if (btn) {
        orig = btn.textContent;
        btn.disabled = true;
        btn.innerHTML = '<span class="spinner"></span> 検算中';
    }
    try {
        const r = await api('/api/catalog/checks/verify',
            { db: CAT.db, checks: targets.map(ckPayload) });
        r.results.forEach((x, i) => {
            const it = targets[i];
            if (!x.ok_run) {
                it.verdict = 'エラー';
                it.detail = x.error || '実行できませんでした。';
            } else {
                it.verdict = x.match ? '一致' : '不一致';
                const fmt = v => Number(v).toLocaleString(undefined,
                    { maximumFractionDigits: 2 });
                it.detail = `左 ${fmt(x.left)} / 右 ${fmt(x.right)}`
                    + `（差 ${fmt(x.diff)}・${x.pct}%）`;
                if (!x.match && (x.drill || {}).rows) {
                    it.detail += ` 内訳 ${x.drill.rows.length}行${x.drill.truncated ? '以上' : ''}`;
                }
            }
        });
    } catch (e) { toast(e.message, 'err'); }
    if (btn) { btn.disabled = false; btn.textContent = orig; }
    ckRenderList();
    ckRenderEditor();
}

/** 検算ルールを保存する。 */
async function saveChecks() {
    // 「何か書かれているのに左右のSQLが揃っていない」行を止める。
    // 名前と左右のSQLだけを見ていたので、左右の"名前"や内訳SQLだけ書いた
    // 書きかけの行が素通りし、サーバで落とされて黙って消えていた
    const written = it => (it.name || '').trim() || (it.left_sql || '').trim()
        || (it.right_sql || '').trim() || (it.left_label || '').trim()
        || (it.right_label || '').trim() || (it.drilldown || '').trim();
    const bad = ckItems.find(it =>
        written(it) && !((it.left_sql || '').trim() && (it.right_sql || '').trim()));
    if (bad) {
        toast(`「${bad.name || '（無題）'}」は左右の両方にSQLが必要です。`, 'err', 7000);
        ckSelect(bad.id);
        return;
    }
    let r;
    try {
        r = await api('/api/catalog/checks',
            { db: CAT.db, stamp: CAT.stamps?.checks,
              checks: ckItems.map(ckPayload) });
    } catch (e) { toast(e.message, 'err', e.data?.stale ? 12000 : 8000); return; }
    CAT.checks = r.checks || [];
    if (r.stamp) CAT.stamps.checks = r.stamp;
    // サーバの確定結果で作り直す（空のルールはここで消える）
    const results = new Map(ckItems.map(it => [it.name.trim(), it]));
    const wasSel = ckItems.find(it => it.id === ckSelId)?.name?.trim();
    loadChecks();
    // 作り直すと1件目が選ばれる。編集していたルールに戻す
    if (wasSel) {
        const back = ckItems.find(it => (it.name || '').trim() === wasSel);
        if (back) ckSelId = back.id;
    }
    ckItems.forEach(it => {
        const o = results.get(it.name);
        if (o) { it.verdict = o.verdict; it.detail = o.detail; }
    });
    setDirty('checks', false);
    ckRenderList(); ckRenderEditor();
    toast(r.dropped
        ? `検算ルールを保存しました。中身がまったく同じ ${r.dropped} 件はまとめました。`
        : '検算ルールを保存しました。次の質問から自動で突き合わせます。',
        'ok', r.dropped ? 7000 : undefined);
}

function wireChecks() {
    loadChecks();
    $('#ckAdd').addEventListener('click', ckAdd);
    $('#ckVerifyAll').addEventListener('click', ev => ckVerify(ckItems, ev.currentTarget));
    $('#ckSave').addEventListener('click', saveChecks);
    $('#ckList').addEventListener('keydown', ev => listArrowNav(ev, '#ckList', ckSelect));
}

/* --- ツール ------------------------------------------------------------------ */

/* 結果の見せ方。値はサーバの render と同じ。表示だけ日本語にする。 */
const RENDER_KINDS = [
    ['table', '表'], ['chart', 'グラフ'], ['chart_dual', '2軸グラフ（棒＋折れ線）'],
    ['excel', 'Excelファイル'], ['csv', 'CSVファイル'], ['none', '出さない（AIにだけ渡す）'],
];
const PARAM_TYPES = [['string', '文字'], ['integer', '整数'],
                     ['number', '小数'], ['boolean', 'はい/いいえ']];

/* 日本語の説明から、英数字のツール名を作る。
   AIのfunction名は英数字しか使えないが、それを人に考えさせない。 */
function toolNameFrom(desc, taken) {
    const ascii = String(desc || '').toLowerCase()
        .replace(/[^a-z0-9]+/g, '_').replace(/^_+|_+$/g, '');
    let base = /^[a-z]/.test(ascii) ? ascii.slice(0, 40) : '';
    if (!base) base = 'tool';                 // 日本語だけの説明はここに来る
    let name = base, n = 2;
    while ((taken || []).includes(name)) name = `${base}_${n++}`;
    return name;
}

/* パラメータ1行ぶんの入力欄。 */
function paramRow(p) {
    const v = p || { name: '', type: 'string', description: '', required: true };
    const row = el('div', { class: 'prow' },
        el('input', { type: 'text', class: 'p-name', placeholder: '名前（英数字）', value: v.name }),
        el('select', { class: 'p-type' }, PARAM_TYPES.map(([k, label]) =>
            el('option', { value: k, ...(k === (v.type || 'string') ? { selected: 'selected' } : {}) }, label))),
        el('input', { type: 'text', class: 'p-desc grow',
                      placeholder: '説明（AIがここを読んで値を決めます）', value: v.description || '' }),
        el('label', { class: 'small', style: 'display:flex;gap:4px;align-items:center' },
            el('input', { type: 'checkbox', class: 'p-req',
                          ...(v.required !== false ? { checked: 'checked' } : {}) }), '必須'),
        el('button', { class: 'btn btn--sm btn--ghost', title: 'この行を消す',
                       onclick: () => row.remove() }, icon('x', 'icon--sm')));
    return row;
}

function readParams(card) {
    return $$('.prow', card).map(r => ({
        name: $('.p-name', r).value.trim(),
        type: $('.p-type', r).value,
        description: $('.p-desc', r).value.trim(),
        required: $('.p-req', r).checked,
    })).filter(p => p.name);
}

/* グラフの設定欄。種別ごとに要る項目が違うので、選ばれた種別に合わせて出し直す。
   ここが無かったせいで、見せ方に「グラフ」を選ぶと必ず保存に失敗していた。 */
function chartFields(box, kind, chart) {
    const c = chart || {};
    box.replaceChildren();
    if (kind === 'chart_dual') {
        box.append(
            el('div', { class: 'row mb' },
                el('div', { class: 'grow' },
                    el('label', { class: 'field' }, '横軸にする列'),
                    el('input', { type: 'text', class: 'ch-x', value: c.x || '' })),
                el('div', { class: 'grow' },
                    el('label', { class: 'field' }, '棒にする列（カンマ区切り）'),
                    el('input', { type: 'text', class: 'ch-bar', value: (c.bar_y || []).join(', ') })),
                el('div', { class: 'grow' },
                    el('label', { class: 'field' }, '折れ線にする列（カンマ区切り）'),
                    el('input', { type: 'text', class: 'ch-line', value: (c.line_y || []).join(', ') }))));
        return;
    }
    if (kind !== 'chart') return;
    const type = c.chart_type || 'bar';
    const sel = el('select', { class: 'ch-type' },
        Object.keys(CAT.chartFields || {}).map(k =>
            el('option', { value: k, ...(k === type ? { selected: 'selected' } : {}) }, k)));
    sel.addEventListener('change', () => chartFields(box, kind, { ...readChart(box, kind), chart_type: sel.value }));
    const need = (CAT.chartFields || {})[type] || ['x', 'y'];
    box.append(
        el('div', { class: 'row mb', style: 'align-items:flex-end' },
            el('div', { style: 'width:180px' }, el('label', { class: 'field' }, 'グラフの種類'), sel),
            ...need.map(k => el('div', { class: 'grow' },
                el('label', { class: 'field' }, `${k} にする列`),
                el('input', { type: 'text', class: 'ch-f', 'data-key': k,
                              value: Array.isArray(c[k]) ? c[k].join(', ') : (c[k] || '') }))),
            el('div', { class: 'grow' },
                el('label', { class: 'field' }, 'グラフの表題（任意）'),
                el('input', { type: 'text', class: 'ch-title', value: c.title || '' }))));
}

function readChart(box, kind) {
    if (kind === 'chart_dual') {
        const list = s => (s || '').split(',').map(x => x.trim()).filter(Boolean);
        return { x: $('.ch-x', box)?.value.trim() || '',
                 bar_y: list($('.ch-bar', box)?.value),
                 line_y: list($('.ch-line', box)?.value) };
    }
    if (kind !== 'chart') return {};
    const out = { chart_type: $('.ch-type', box)?.value || 'bar',
                  title: $('.ch-title', box)?.value.trim() || '' };
    $$('.ch-f', box).forEach(inp => {
        const k = inp.dataset.key, v = inp.value.trim();
        // path / dimensions は列を並べて渡す種別（treemap や散布図行列）
        out[k] = (k === 'path' || k === 'dimensions')
            ? v.split(',').map(x => x.trim()).filter(Boolean) : v;
    });
    return out;
}

function toolCard(tool) {
    const t = tool || { name: '', description: '', sql: '', parameters: [],
                        render: 'table', chart: {}, enabled: true };
    const original = t.name;
    // 定義が置かれているDB。一覧は全DBぶん出すので、開いているDBとは限らない
    const ownerFile = t.owner_file || CAT.db;

    const params = el('div', {}, (t.parameters || []).map(paramRow));
    const chartBox = el('div', { class: 'mt' });
    const renderSel = el('select', { class: 'tl-render' }, RENDER_KINDS.map(([k, label]) =>
        el('option', { value: k, ...(k === t.render ? { selected: 'selected' } : {}) }, label)));
    renderSel.addEventListener('change', () => chartFields(chartBox, renderSel.value, t.chart));

    const card = el('details', { class: 'acc', ...(tool ? {} : { open: 'open' }) },
        el('summary', {},
            el('strong', {}, t.name || '（新しいツール）'),
            t.enabled === false ? el('span', { class: 'badge badge--warn' }, '無効') : null),
        el('div', { class: 'acc__body' },
            el('div', { class: 'row mb' },
                el('div', { class: 'grow' },
                    el('label', { class: 'field' }, '説明（AIが使うかどうかの判断材料）'),
                    el('input', { type: 'text', class: 'tl-desc', value: t.description })),
                el('div', { style: 'width:200px' },
                    el('label', { class: 'field' }, '結果の見せ方'), renderSel)),
            chartBox,
            el('div', { class: 'row mt', style: 'align-items:center' },
                el('label', { class: 'field', style: 'margin:0' }, 'パラメータ（毎回変えられる値）'),
                el('div', { class: 'spacer' }),
                el('button', { class: 'btn btn--sm',
                               onclick: () => params.append(paramRow(null)) }, '＋ 追加')),
            params,
            el('details', { class: 'mt' },
                el('summary', { class: 'small muted', style: 'cursor:pointer' }, '詳しい設定（SQL・ツール名）'),
                el('div', { class: 'mt' },
                    el('label', { class: 'field' }, 'SQL（パラメータは :名前 で書く）'),
                    el('textarea', { class: 'tl-sql mono', rows: '5' }, t.sql || ''),
                    el('label', { class: 'field mt' }, 'ツール名（英数字と_。空なら自動で付けます）'),
                    el('input', { type: 'text', class: 'tl-name', value: t.name }))),
            el('div', { class: 'row mt' },
                el('label', { style: 'display:flex;gap:6px;align-items:center;font-size:12.5px' },
                    el('input', { type: 'checkbox', class: 'tl-enabled',
                        ...(t.enabled !== false ? { checked: 'checked' } : {}) }), '有効'),
                el('div', { class: 'spacer' }),
                el('button', {
                    class: 'btn btn--sm',
                    title: '実際のデータで動かして、結果を確かめます',
                    onclick: ev => tryTool(readTool(card, original), ev.target, null, ownerFile),
                }, '試す'),
                tool ? el('button', {
                    class: 'btn btn--sm btn--danger',
                    onclick: async () => {
                        if (!confirm(`${t.name} を削除しますか？`)) return;
                        // ここだけ try が無く、失敗しても何も出ないまま無反応だった
                        try {
                            await api('/api/catalog/tool',
                                { db: ownerFile, action: 'delete', name: t.name });
                        } catch (e) { toast(e.message, 'err', 9000); return; }
                        toast('削除しました。'); reloadCleanIfSaved();
                    },
                }, '削除') : null,
                el('button', {
                    class: 'btn btn--primary btn--sm',
                    onclick: async () => {
                        const payload = readTool(card, original);
                        try {
                            await api('/api/catalog/tool',
                                { db: ownerFile, tool: payload, name: payload.name, original });
                            toast('保存しました。'); reloadCleanIfSaved();
                        } catch (e) { toast(e.message, 'err'); }
                    },
                }, '保存'))));

    chartFields(chartBox, t.render, t.chart);
    return card;
}

/** 編集欄の中身を、保存できる形にまとめる。 */
function readTool(card, original) {
    const render = $('.tl-render', card).value;
    const desc = $('.tl-desc', card).value.trim();
    const typed = $('.tl-name', card).value.trim();
    const taken = (CAT.custom || []).map(x => x.name).filter(n => n !== original);
    const out = {
        name: typed || toolNameFrom(desc, taken),
        description: desc,
        sql: $('.tl-sql', card).value,
        parameters: readParams(card),
        render,
        enabled: $('.tl-enabled', card).checked,
    };
    if (render === 'chart' || render === 'chart_dual') out.chart = readChart(card, render);
    return out;
}

/* --- 試し実行 ------------------------------------------------------------------
   SQLを読めない人に「合っているか」を判断してもらうには、実際に出てくる表を
   見せるのがいちばん早い。結果はその場に出す。 */

function resultTable(res) {
    if (!res.ok) {
        return el('div', { class: 'alert alert--err small' },
            'うまく動きませんでした: ' + (res.error || '原因不明'));
    }
    const box = el('div', {});
    if (res.note) box.append(el('div', { class: 'alert alert--warn small' }, res.note));
    if ((res.problems || []).length) {
        box.append(el('div', { class: 'alert alert--warn small' },
            '保存の前に直すところ: ' + res.problems.join(' / ')));
    }
    if (res.columns?.length) {
        box.append(dataTable(res.columns, res.rows || []));
        box.append(el('div', { class: 'small muted mt' },
            res.rows?.length ? `先頭 ${res.rows.length} 行です。` : '行はありませんでした。'));
    }
    return box;
}

async function tryTool(payload, btn, into, dbFile) {
    const target = into || (() => {
        // 押したボタンの近くに結果を出す。無ければ作る
        const card = btn.closest('.acc__body') || btn.parentElement;
        let box = $('.tl-result', card);
        if (!box) { box = el('div', { class: 'tl-result mt' }); card.append(box); }
        return box;
    })();
    target.replaceChildren(el('div', { class: 'small muted' }, '試しています…'));
    if (btn) btn.disabled = true;
    try {
        const res = await api('/api/catalog/tool/try', { db: dbFile || CAT.db, tool: payload });
        target.replaceChildren(resultTable(res));
        return res;
    } catch (e) {
        target.replaceChildren(el('div', { class: 'alert alert--err small' }, e.message));
        return { ok: false, error: e.message };
    } finally {
        if (btn) btn.disabled = false;
    }
}

/* --- 日本語だけで作る ------------------------------------------------------------
   SQLを書かずにツールを作るための入口。日本語で目的を書いてもらい、
   AIにSQLを起こさせ、その場で実データに当てて結果を見せてから保存する。 */

function openToolWizard(seed) {
    const back = el('div', { class: 'modal', id: 'toolWiz' });
    const close = () => back.remove();
    back.addEventListener('click', ev => { if (ev.target === back) close(); });

    const purpose = el('textarea', { rows: '3', style: 'width:100%',
        placeholder: '例: 指定した年の月別売上を、部署ごとに出す' }, seed?.purpose || '');

    const out = el('div', { class: 'mt' });
    let drafted = null;
    // 保存先の .meta.yaml。SQLが主に見ているDBをサーバが決める（作る人は選ばない）
    let homeDb = CAT.db;

    const saveBtn = el('button', { class: 'btn btn--primary btn--sm', disabled: 'disabled',
        onclick: async () => {
            try {
                await api('/api/catalog/tool',
                    { db: homeDb, tool: drafted, name: drafted.name, original: '' });
                close(); toast('ツールを作りました。'); reloadCleanIfSaved();
            } catch (e) { toast(e.message, 'err', 9000); }
        } }, 'この内容で作る');

    const makeBtn = el('button', { class: 'btn btn--primary btn--sm', onclick: async () => {
        const text = purpose.value.trim();
        if (!text) return toast('何をするツールかを書いてください。', 'warn');
        makeBtn.disabled = true; saveBtn.disabled = true;
        out.replaceChildren(el('div', { class: 'small muted' },
            'AIがSQLを起こして、実際のデータで確かめています…'));
        try {
            // db は送らない。全DBのカタログを見て、AIがどのDBを使うか決める
            const res = await api('/api/catalog/tool/draft', {
                purpose: text, render: 'table' });
            out.replaceChildren();
            if (res.refused) {
                // AIが「このツールは作れない・作らない方がよい」と判断した。
                // SQLは書かせず、理由だけを見せる
                out.append(el('div', { class: 'alert alert--warn small' },
                    el('div', { class: 'mb' }, el('b', {}, 'この指示ではツールを作りませんでした')),
                    el('div', { style: 'white-space:pre-wrap' }, res.reason || ''),
                    el('div', { class: 'small muted mt' },
                        'やりたいことを書き直してもう一度お試しください。')));
                makeBtn.disabled = false;
                return;
            }
            drafted = res.tool;
            if (res.home_db) homeDb = res.home_db;
            if (!res.ok) {
                out.append(el('div', { class: 'alert alert--err small' },
                    'うまく作れませんでした: ' + (res.error || '原因不明')
                    + '　やりたいことをもう少し具体的に書き直して、もう一度お試しください。'));
            } else {
                out.append(el('div', { class: 'alert alert--ok small' },
                    'できました。下の内容で作ります。'));
                if (drafted && drafted.explanation) {
                    out.append(el('div', { class: 'alert alert--info small mt' },
                        el('div', { class: 'mb' }, el('b', {}, 'このSQLがしていること')),
                        el('div', { style: 'white-space:pre-wrap' }, drafted.explanation)));
                }
                // 何ができたかを先に見せる。SQLを読めなくても、決まった内容と
                // 実際に出た行を見れば「これでいい」と判断できる。
                out.append(draftSummary(drafted));
                out.append(el('div', { class: 'small muted mt' },
                    '実際のデータで動かした結果（先頭のみ）:'));
                out.append(resultTable({ ok: true, columns: res.columns, rows: res.rows }));
                if (!(res.rows || []).length) {
                    out.append(el('div', { class: 'alert alert--warn small mt' },
                        '動きましたが0行でした。条件が厳しいだけかもしれません。'
                        + '中身を確かめてから保存してください。'));
                }
                saveBtn.disabled = false;
            }
            // 起こした中身は必ず見せる。保存前に人が直せるようにする
            if (drafted) out.append(draftDetail(drafted, res.ok ? null : out));
        } catch (e) {
            out.replaceChildren(el('div', { class: 'alert alert--err small' }, e.message));
        }
        makeBtn.disabled = false;
    } }, 'AIに作ってもらう');

    /* AIが決めたことを、SQLを読まなくても確かめられる形で見せる。 */
    function draftSummary(t) {
        const ps = t.parameters || [];
        return el('div', { class: 'card mt', style: 'padding:10px 12px' },
            el('div', { class: 'small' },
                el('b', {}, 'このツールがすること: '), t.description || ''),
            ps.length
                ? el('div', { class: 'small mt' },
                    el('b', {}, '毎回変えられる値: '),
                    ps.map(p => `${p.description || p.name}`).join('、'),
                    el('div', { class: 'small muted', style: 'margin-top:2px' },
                        '下の結果は ' + ps.map(p =>
                            `${p.description || p.name}=「${p.example ?? ''}」`).join('、')
                        + ' で試した結果です。AIが呼ぶときは質問に合わせて値を入れます。'))
                : el('div', { class: 'small muted mt' },
                    '毎回変える値はありません（いつも同じ条件で返します）。'),
            null);
    }

    /* 起こした中身をその場で直せるようにする。ふつうは開かなくてよい。 */
    function draftDetail(t, retryInto) {
        const sql = el('textarea', { class: 'mono', rows: '6', style: 'width:100%' }, t.sql || '');
        const desc = el('input', { type: 'text', style: 'width:100%', value: t.description || '' });
        sql.addEventListener('input', () => { drafted.sql = sql.value; });
        desc.addEventListener('input', () => { drafted.description = desc.value; });
        return el('details', { class: 'mt', ...(retryInto ? { open: 'open' } : {}) },
            el('summary', { class: 'small muted', style: 'cursor:pointer' },
                '中身を見る・直す（ふつうは不要）'),
            el('div', { class: 'mt' },
                el('label', { class: 'field' }, 'AIに渡す説明'), desc,
                el('label', { class: 'field mt' }, 'SQL'), sql,
                el('div', { class: 'row mt' },
                    el('button', { class: 'btn btn--sm', onclick: async ev => {
                        const res = await tryTool(drafted, ev.target, retryBox, homeDb);
                        saveBtn.disabled = !res.ok;
                    } }, 'この内容で試す')),
                retryBox));
    }
    const retryBox = el('div', { class: 'mt' });

    back.append(el('div', { class: 'modal__box' },
        el('div', { class: 'modal__head' },
            el('b', { class: 'grow' }, '日本語でツールを作る'),
            el('button', { class: 'btn btn--sm btn--ghost', onclick: close }, icon('x', 'icon--sm'))),
        el('div', { class: 'modal__body', style: 'padding:12px 14px' },
            el('div', { class: 'small muted mb' },
                'やりたいことを日本語で書くだけです。SQLも設定も要りません。'
                + 'AIがSQLを組み立て、毎回変える値があればそれも自分で見つけ、'
                + '実際のデータで動くところまで確かめてから作ります。'),
            el('label', { class: 'field' }, 'このツールは何をする？'),
            purpose,
            el('div', { class: 'small muted', style: 'margin-top:4px' },
                '例:「指定した年の月別売上を出す」「ある部署の残業時間の多い順に社員を並べる」。'
                + '「指定した」「ある〇〇の」と書けば、そこが毎回変えられる値になります。'),
            el('div', { class: 'row mt' }, el('div', { class: 'spacer' }), makeBtn),
            out),
        el('div', { class: 'modal__foot row', style: 'align-items:center' },
            el('div', { class: 'spacer' }),
            el('button', { class: 'btn btn--sm', onclick: close }, 'やめる'),
            saveBtn)));
    document.body.append(back);
    purpose.focus();
    // 例文から来たときは、検証済みのSQLをそのまま使う。AIに書き直させると
    // 通っていたSQLが別物になりかねないし、LLMの呼び出しも無駄になる。
    // いまのデータで通らなくなっていたときだけ、「AIに作ってもらう」に切り替えてもらう。
    if (seed?.sql) {
        drafted = {
            name: toolNameFrom(seed.purpose,
                (CAT.custom || []).map(x => x.name)
                    .concat((CAT.builtin || []).map(b => b.name))),
            description: seed.purpose, sql: seed.sql,
            parameters: [], render: 'table', enabled: true,
        };
        out.replaceChildren(el('div', { class: 'small muted' },
            '例文のSQLを実際のデータで確かめています…'));
        (async () => {
            try {
                const res = await api('/api/catalog/tool/try', { db: CAT.db, tool: drafted });
                out.replaceChildren();
                if (res.ok) {
                    out.append(el('div', { class: 'alert alert--ok small' },
                        '例文の検証済みSQLをそのまま使います。実際のデータで動かした結果です。'));
                    out.append(resultTable(res));
                    saveBtn.disabled = false;
                } else {
                    out.append(el('div', { class: 'alert alert--warn small' },
                        '例文のSQLが、いまのデータでは通りませんでした: '
                        + (res.error || '') + '　「AIに作ってもらう」で作り直せます。'));
                }
                out.append(draftDetail(drafted, res.ok ? null : out));
            } catch (e) {
                out.replaceChildren(el('div', { class: 'alert alert--err small' }, e.message));
            }
        })();
    } else if (seed?.purpose) {
        makeBtn.click();
    }
}

function wireTools() {
    const list = $('#toolList');
    list.replaceChildren(...CAT.custom.map(toolCard));
    if (!CAT.custom.length) list.append(el('div', { class: 'small muted' }, 'まだありません。'));
    $('#toolWizard')?.addEventListener('click', () => openToolWizard(null));

    renderBuiltins();
    $('#btFilter').addEventListener('input', renderBuiltins);
}

/* --- 組み込みツール（中身を見る） -------------------------------------------------
   AIに渡している JSON Schema をそのまま読める形にして出す。
   説明が長いものが多く、パラメータは今まで一切見えていなかった。 */

function builtinCard(b) {
    const ov = CAT.builtinOverrides[b.name] || {};
    const off = ov.enabled === false;

    const head = el('summary', {},
        el('code', {}, b.name),
        off ? el('span', { class: 'badge badge--warn' }, '無効') : null,
        b.is_sql ? el('span', { class: 'badge' }, 'SQL') : null,
        ov.description ? el('span', { class: 'badge badge--accent' }, '説明を上書き中') : null);

    // AIが読んでいる説明。上書きがあればそちらが実際に使われる
    const body = el('div', { class: 'acc__body' },
        el('div', { class: 'small muted' }, 'AIに渡している説明'),
        el('div', { class: 'toolblock mt' },
            el('pre', { class: 'mono', style: 'white-space:pre-wrap' },
                ov.description || b.description)),
        ov.description
            ? el('div', { class: 'small muted mt' },
                `元の説明: ${b.description}`)
            : null);

    if (b.params.length) {
        body.append(el('div', { class: 'small muted mt' }, 'パラメータ'),
            dataTable(['名前', '型', '必須', '説明'],
                b.params.map(p => [
                    p.name,
                    p.type + (p.enum.length ? `（${p.enum.join(' / ')}）` : ''),
                    p.required ? '必須' : '',
                    p.description,
                ])));
    } else {
        body.append(el('div', { class: 'small muted mt' }, 'パラメータはありません。'));
    }

    // 実装コード。重いので開いたときに初めて取りに行く
    const srcAcc = el('details', { class: 'acc mt' },
        el('summary', {}, '実装コードを見る（このツールが実際に何をするか）'),
        el('div', { class: 'acc__body', 'data-src-body': '1' },
            el('div', { class: 'small muted' },
                el('span', { class: 'spinner' }), ' 読み込み中...')));
    srcAcc.addEventListener('toggle', async () => {
        if (!srcAcc.open || srcAcc.dataset.loaded) return;
        srcAcc.dataset.loaded = '1';
        const box = $('[data-src-body]', srcAcc);
        try {
            const r = await api(`/api/catalog/builtin/source?name=${encodeURIComponent(b.name)}`,
                                undefined, 'GET');
            box.replaceChildren(...r.parts.map(p =>
                el('div', { class: 'toolblock mt' },
                    el('div', { class: 'toolblock__head' },
                        el('span', {}, p.label),
                        el('span', { class: 'muted small' }, `— ${p.where}`)),
                    el('pre', { class: 'mono' }, p.code))));
            if (!r.parts.length) {
                box.replaceChildren(el('div', { class: 'small muted' }, 'コードを取得できませんでした。'));
            }
        } catch (e) {
            srcAcc.dataset.loaded = '';
            box.replaceChildren(el('div', { class: 'alert alert--err' }, e.message));
        }
    });
    body.append(srcAcc);

    // 編集は補助。まず中身が読めることを優先し、操作は下にまとめる
    body.append(el('div', { class: 'row mt', style: 'align-items:center' },
        el('label', { class: 'check' },
            el('input', { type: 'checkbox', class: 'bt-en', ...(off ? {} : { checked: 'checked' }) }),
            el('span', {}, 'このツールをAIに渡す')),
        el('div', { class: 'grow' },
            el('input', { type: 'text', class: 'bt-desc',
                value: ov.description || '',
                placeholder: '説明を上書きする（空欄なら上の元の説明を使う）' })),
        el('button', {
            class: 'btn btn--sm',
            onclick: async ev => {
                const card = ev.target.closest('details');
                try {
                    await api('/api/catalog/builtin', {
                        db: CAT.db, name: b.name,
                        enabled: $('.bt-en', card).checked,
                        description: $('.bt-desc', card).value,
                    });
                    // 画面内の控えも合わせる（開き直さずにバッジを正しくする）
                    CAT.builtinOverrides[b.name] = {
                        enabled: $('.bt-en', card).checked,
                        description: $('.bt-desc', card).value.trim(),
                    };
                    const open = card.open;
                    card.replaceWith(builtinCard(b));
                    $(`#builtinList details[data-tool="${b.name}"]`).open = open;
                    toast(`${b.name} を保存しました。`);
                } catch (e) { toast(e.message, 'err'); }
            },
        }, '保存')));

    return el('details', { class: 'acc', 'data-tool': b.name }, head, body);
}

function renderBuiltins() {
    const q = ($('#btFilter')?.value || '').trim().toLowerCase();
    const hit = CAT.builtin.filter(b =>
        !q || `${b.name} ${b.description}`.toLowerCase().includes(q));
    $('#builtinList').replaceChildren(...hit.map(builtinCard));
    $('#btCount').textContent = q
        ? `${CAT.builtin.length}件中 ${hit.length}件`
        : `${CAT.builtin.length}件`;
}

/* --- DB情報・その他 ---------------------------------------------------------- */

/* まとまり（表名の接頭辞）のメモと名前。全体説明の欄は廃止した:
   全体に書いた文章は表の入れ替えに追随できず腐る。まとまりに付ければ、
   その表を選んでいるときだけAIに渡り、まとまりごと消えれば一緒に消える。
   名前は接頭辞そのもの（別の表示名は持たない）。 */
/* 点検の結果。指摘は「原文の引用 → 何が問題か → どうするとよいか」の順に出す。
   直すのは人なので、どの行のことかが一目で分かることを優先する。 */
const MEMO_CHECK_LABEL = {
    err: 'データと合っていません',
    warn: '裏が取れません',
    info: 'ここに書かなくても伝わります',
};

function renderMemoCheck(out, findings) {
    out.classList.remove('hidden');
    if (!findings.length) {
        out.replaceChildren(el('div', { class: 'alert alert--ok' },
            '気になるところはありませんでした。'));
        return;
    }
    const order = { err: 0, warn: 1, info: 2 };
    const sorted = [...findings].sort((a, b) => order[a.level] - order[b.level]);
    out.replaceChildren(...sorted.map(f => el('div', { class: `alert alert--${f.level}` },
        el('div', { class: 'small muted' }, MEMO_CHECK_LABEL[f.level] || ''),
        f.line ? el('div', { class: 'mono small', style: 'margin:3px 0' }, f.line) : null,
        el('div', {}, f.problem),
        f.suggestion ? el('div', { class: 'small muted', style: 'margin-top:3px' },
            '→ ' + f.suggestion) : null)));
}


function wireGroupMemo() {
    $$('#pane-tables .gmemo .g-save').forEach(btn => {
        btn.addEventListener('click', async () => {
            const box = btn.closest('.gmemo');
            try { await saveGroupMemo(box); }
            catch (e) { toast(e.message, 'err'); return; }
            toast('保存しました。');
        });
    });
    // メモの点検。書き換えないので、未保存の印は付けない
    $$('#pane-tables .gmemo .g-check').forEach(btn => {
        btn.addEventListener('click', async () => {
            const box = btn.closest('.gmemo');
            const out = $('.gcheck', box);
            const label = btn.textContent;
            btn.disabled = true;
            btn.innerHTML = '<span class="spinner"></span> 点検中';
            try {
                const r = await api('/api/catalog/group/check', {
                    db: CAT.db, group: box.dataset.group,
                    description: $('.g-memo', box).value,
                });
                renderMemoCheck(out, r.findings || []);
            } catch (e) { toast(e.message, 'err', 8000); }
            btn.disabled = false;
            btn.textContent = label;
        });
    });

    // まとまりの名前の一括改名（配下の全テーブルの接頭辞を変える）
    $$('#pane-tables .gmemo .g-rename').forEach(btn => {
        btn.addEventListener('click', async () => {
            const box = btn.closest('.gmemo');
            const oldKey = box.dataset.group;
            const n = ($('.g-key', box).value || '').trim();
            if (!n || n === oldKey) { toast('新しい名前を入力してください。', 'warn'); return; }
            const count = $$(`details.acc[data-table^="${CSS.escape(oldKey)}__"]`).length;
            if (!confirm(`まとまり「${oldKey}」の ${count} テーブルすべてを「${n}__…」に改名します。
`
                       + 'カタログの記述・関連・例文・検算はすべて引き継がれます。よろしいですか？')) return;
            btn.disabled = true;
            try {
                const r = await api('/api/catalog/rename-group',
                    { db: CAT.db, group: oldKey, new_group: n });
                toast(`${r.count} テーブルを改名しました。ページを読み直します。`);
                // 同上（reloadClean でないと、未保存のメモがあるときに止まる）
                setTimeout(reloadClean, 800);
            } catch (e) { toast(e.message, 'err'); btn.disabled = false; }
        });
    });
}

function wireMisc() {

    // 充実度の数字から該当タブへ飛ぶ。「テーブル説明」は未記入だけに絞って開く
    $$('.metric[data-jump]').forEach(m => m.addEventListener('click', () => {
        activateTab(m.dataset.jump);
        if (m.dataset.sec) switchSec(m.dataset.sec);
        if (m.dataset.filter === 'missing' && !missingOnly) {
            missingOnly = true;
            $('#tblMissing').classList.add('btn--primary');
            applyTableFilter();
        }
    }));

    $('#saveAll')?.addEventListener('click', saveAllDirty);

    // Ctrl+S = いま見ているタブの内容を保存（ブラウザの保存ダイアログは出さない）
    document.addEventListener('keydown', ev => {
        if (!(ev.ctrlKey || ev.metaKey) || ev.key.toLowerCase() !== 's') return;
        ev.preventDefault();
        if (dirtyLabel()) saveAllDirty();
        else toast('未保存の変更はありません。');
    });
}


/* --- ビュー（実体を持たない、名前を付けたSELECT）-------------------------------
   よく使う結合や絞り込みに名前を付けて置いておく。保存すると表と同じ扱いになる。
   作り方は「日本語で書く → AIがSQLを組み立てる → 実データで動かして見せる → 登録」。 */

let viewEditing = null;      // 編集中のビュー名（新規なら null）

function renderViews() {
    const box = $('#viewList');
    if (!box) return;
    const list = CAT.views || [];
    if (!list.length) {
        box.replaceChildren(el('div', { class: 'small muted' },
            'まだありません。よく使う結合や絞り込みを登録しておくと、'
            + 'AIが毎回SQLを組み立てずに済み、答えのぶれもなくなります。'));
        return;
    }
    box.replaceChildren(...list.map(v => {
        const out = el('div', { class: 'mt' });
        return el('details', { class: 'acc' },
            el('summary', {},
                el('strong', {}, v.name),
                el('span', { class: 'badge' }, 'ビュー'),
                v.error ? el('span', { class: 'badge badge--warn' }, '動きません') : null,
                el('span', { class: 'small muted', style: 'margin-left:8px' },
                    v.description || '説明が未記入です')),
            el('div', { class: 'acc__body' },
                v.error ? el('div', { class: 'alert alert--err small mb' },
                    `いまは動きません（元のテーブルが変わった可能性があります）: ${v.error}`) : null,
                el('div', { class: 'small muted mb' },
                    `${(v.columns || []).length}列`
                    + (v.rows === null || v.rows === undefined ? '' : `・${Number(v.rows).toLocaleString()}行`)
                    + '　列の説明や用語は「テーブル」タブから付けられます'),
                el('div', { class: 'toolblock mb' },
                    el('pre', { class: 'mono', style: 'white-space:pre-wrap' }, v.sql || '')),
                el('div', { class: 'row' },
                    el('button', { class: 'btn btn--sm', onclick: ev => previewView(v, out, ev.target) }, 'プレビュー'),
                    el('button', { class: 'btn btn--sm', onclick: () => editView(v) }, '編集'),
                    el('div', { class: 'spacer' }),
                    el('button', { class: 'btn btn--sm btn--danger', onclick: () => deleteView(v) }, '削除')),
                out));
    }));
}

function viewPreviewBox(r) {
    const cols = r.columns || [], rows = r.rows || [];
    if (!cols.length) return el('div', { class: 'small muted' }, '列がありません。');
    const head = el('tr', {}, ...cols.map(c => el('th', {}, c)));
    const body = rows.slice(0, 10).map(row => el('tr', {}, ...row.map(x =>
        el('td', {}, x === null || x === undefined ? '' : String(x)))));
    return el('div', {},
        el('div', { class: 'alert alert--ok small mb' },
            r.total === null || r.total === undefined
                ? `${rows.length}行 取得できました`
                : `${Number(r.total).toLocaleString()}行 取得できました（先頭${Math.min(rows.length, 10)}行を表示）`),
        el('div', { class: 'tablewrap' },
            el('table', { class: 'data' }, el('thead', {}, head), el('tbody', {}, ...body))));
}

async function previewView(v, out, btn) {
    btn.disabled = true;
    try {
        const r = await api('/api/catalog/view/preview', { db: CAT.db, sql: v.sql });
        out.replaceChildren(viewPreviewBox(r));
    } catch (e) {
        out.replaceChildren(el('div', { class: 'alert alert--err small' }, e.message));
    }
    btn.disabled = false;
}

function renderViewExplain(text) {
    const box = $('#viewExplain');
    if (!box) return;
    if (!text) { box.replaceChildren(); return; }
    box.replaceChildren(el('div', { class: 'alert alert--info mt' },
        el('div', { class: 'mb' }, el('b', {}, 'このSQLがしていること')),
        el('div', { style: 'white-space:pre-wrap' }, text)));
}


function openViewEditor(title) {
    $('#viewEditor').classList.remove('hidden');
    $('#viewEditorTitle').textContent = title;
    $('#viewEditor').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function editView(v) {
    viewEditing = v.name;
    openViewEditor(`ビューを編集（${v.name}）`);
    $('#viewNote').replaceChildren();
    renderViewExplain('');
    $('#viewPurpose').value = '';
    $('#viewSqlWrap').classList.remove('hidden');
    $('#viewSql').value = v.sql || '';
    $('#viewName').value = v.name;
    $('#viewDesc').value = v.description || '';
    $('#viewPreview').replaceChildren();
}

async function deleteView(v) {
    if (!confirm(`ビュー「${v.name}」を削除しますか？\n`
        + '（元のテーブルとデータはそのまま残ります）')) return;
    try {
        const r = await api('/api/catalog/view/delete', { db: CAT.db, name: v.name });
        CAT.views = r.views || [];
        renderViews();
        // 「テーブル」タブとER図からも下ろす。ここを scrubTableFromPanes だけに
        // していたので、消したビューが一覧に残り、そこに説明を書いて保存すると
        // 存在しないビューの説明がカタログに戻っていた
        dropTableFromView(v.name, r.stamps);
        toast('ビューを削除しました。');
    } catch (e) { toast(e.message, 'err', 9000); }
}

function wireViews() {
    if (!$('#viewList')) return;
    renderViews();

    $('#viewNew').addEventListener('click', () => {
        viewEditing = null;
        openViewEditor('ビューを作る');
        $('#viewPurpose').value = '';
        $('#viewSql').value = '';
        $('#viewName').value = '';
        $('#viewDesc').value = '';
        $('#viewPreview').replaceChildren();
        $('#viewNote').replaceChildren();
        renderViewExplain('');
        $('#viewSqlWrap').classList.add('hidden');
    });

    $('#viewManual').addEventListener('click', () => {
        $('#viewNote').replaceChildren();
        $('#viewSqlWrap').classList.remove('hidden');
        $('#viewSql').focus();
    });

    // 人がSQLを直したら、AIの解説は当てはまらなくなるので下ろす
    $('#viewSql').addEventListener('input', () => renderViewExplain(''));

    $('#viewDraft').addEventListener('click', async ev => {
        const purpose = $('#viewPurpose').value.trim();
        if (!purpose) { toast('どんな一覧が欲しいかを書いてください。', 'warn'); return; }
        ev.target.disabled = true;
        const old = ev.target.textContent;
        ev.target.textContent = 'AIが考えています...';
        // 前回の理由・解説・結果は先に下ろす（考えている間、古い内容が残らないように）
        $('#viewNote').replaceChildren();
        renderViewExplain('');
        $('#viewPreview').replaceChildren();
        try {
            const r = await api('/api/catalog/view/draft', { db: CAT.db, purpose });
            if (r.ok === false) {
                // 作らない方がよい、とAIが判断した。理由だけを出してSQLは書かない
                $('#viewSqlWrap').classList.add('hidden');
                $('#viewNote').replaceChildren(
                    el('div', { class: 'alert alert--warn' },
                        el('div', { class: 'mb' },
                            el('b', {}, 'この指示ではビューを作りませんでした')),
                        el('div', { style: 'white-space:pre-wrap' }, r.reason || ''),
                        el('div', { class: 'small muted mt' },
                            '書き方を変えてもう一度試すか、「SQLを自分で書く」で直接作れます。')));
                return;
            }
            $('#viewNote').replaceChildren();
            $('#viewSqlWrap').classList.remove('hidden');
            $('#viewSql').value = r.sql || '';
            if (!$('#viewName').value) $('#viewName').value = r.name || '';
            if (!$('#viewDesc').value) $('#viewDesc').value = r.description || '';
            renderViewExplain(r.explanation);
            $('#viewPreview').replaceChildren(viewPreviewBox(r));
            toast('下書きができました。中身を確かめて保存してください。');
        } catch (e) {
            toast(e.message, 'err', 12000);
        } finally {
            // 途中で return しても必ずボタンを戻す（「AIが考えています...」で固まらせない）
            ev.target.disabled = false;
            ev.target.textContent = old;
        }
    });

    $('#viewRun').addEventListener('click', async ev => {
        const sql = $('#viewSql').value.trim();
        if (!sql) { toast('SQLを書いてください。', 'warn'); return; }
        ev.target.disabled = true;
        try {
            const r = await api('/api/catalog/view/preview', { db: CAT.db, sql });
            $('#viewPreview').replaceChildren(viewPreviewBox(r));
        } catch (e) {
            $('#viewPreview').replaceChildren(
                el('div', { class: 'alert alert--err small' }, e.message));
        }
        ev.target.disabled = false;
    });

    $('#viewSave').addEventListener('click', async ev => {
        const name = $('#viewName').value.trim();
        const sql = $('#viewSql').value.trim();
        if (!name) { toast('名前を入れてください。', 'warn'); return; }
        if (!sql) { toast('SQLを書いてください。', 'warn'); return; }
        ev.target.disabled = true;
        try {
            const payload = {
                db: CAT.db, name, sql,
                description: $('#viewDesc').value.trim(),
                old_name: viewEditing || '',
            };
            let r;
            try {
                r = await api('/api/catalog/view', payload);
            } catch (e) {
                // 同名のビューが既にある。黙って差し替えず、一度確かめる
                if (e.status !== 409 || !e.data?.exists) throw e;
                if (!confirm(`ビュー「${name}」は既にあります。定義を上書きしますか？
`
                           + '（元の定義は元に戻せません）')) { ev.target.disabled = false; return; }
                r = await api('/api/catalog/view', { ...payload, overwrite: true });
            }
            CAT.views = r.views || [];
            renderViews();
            $('#viewEditor').classList.add('hidden');
            viewEditing = null;
            toast('保存しました。テーブル一覧やチャットからも使えます。');
        } catch (e) { toast(e.message, 'err', 12000); }
        ev.target.disabled = false;
    });

    $('#viewCancel').addEventListener('click', () => {
        $('#viewEditor').classList.add('hidden');
        viewEditing = null;
    });
}

document.addEventListener('DOMContentLoaded', () => {
    wireTables();
    wireRowDelete();
    wireGrowingNotes();
    wireManage();
    wireTableFilter();
    loadGlossaryAll();
    wireGlossary();
    wireExamples();
    wireChecks();
    ER.init();
    wireTabs();          // ハッシュのタブ復元は ER.init の後（er タブ復元時に refit するため）
    wireTools();
    wireViews();
    wireMisc();
    wireGroupMemo();

    // 過去の分析で実際に使われた結合を、ER図に重ねる（読み込みはページと非同期）
    api(`/api/catalog/usage?db=${encodeURIComponent(CAT.db)}`, undefined, 'GET')
        .then(r => ER.setUsage(r.edges || {}))
        .catch(() => {});          // 取れなくてもER図自体は使える
    ER.setSuggestions(CAT.suggestions || []);
});
// 画面インラインの window.MANAGE.refresh はグローバルの loadManage を
// 参照していたので、この関数スコープ版に繋ぎ直す。
// 上部の数字の計算はこの画面の中にあるので、共通部から呼べるよう一緒に渡す
function scrubTableFromPanes(name) {
    // 表名の単語一致（前後が識別子文字でも「.」修飾でもない）。
    // サーバ側の掃除（clean_table）と同じ範囲を、開きっぱなしの画面からも下ろす。
    // これをしないと、古い一覧のまま「検証」や「保存」をして、
    // 消えたはずの記述が検証エラーになったり書き戻されたりする。
    // Python の \w と同じ範囲にする。英数字だけで見ると、
    // 「生産__実績」を消したときに 生産__実績明細 の「明」が
    // 識別子の文字と見なされず、別の表の例文まで一致してしまう
    const w = ch => !!ch && /[\p{L}\p{N}\p{M}_]/u.test(ch);
    const uses = txt => {
        txt = String(txt || '');
        let i = -1;
        while ((i = txt.indexOf(name, i + 1)) !== -1) {
            const before = txt[i - 1];
            if (!w(before) && before !== '.' && !w(txt[i + name.length])) return true;
        }
        return false;
    };
    const before = { ex: exItems.length, ck: ckItems.length, gl: glItems.length };
    CAT.examples = (CAT.examples || []).filter(e => !uses(e.sql));
    exItems = exItems.filter(it => !uses(it.sql));
    if (!exItems.some(it => it.id === exSelId)) exSelId = exItems[0]?.id ?? null;
    exRenderList(); exRenderEditor();

    CAT.checks = (CAT.checks || []).filter(c =>
        !uses((c.left || {}).sql) && !uses((c.right || {}).sql) && !uses(c.drilldown));
    ckItems = ckItems.filter(it =>
        !uses(it.left_sql) && !uses(it.right_sql) && !uses(it.drilldown));
    if (!ckItems.some(it => it.id === ckSelId)) ckSelId = ckItems[0]?.id ?? null;
    ckRenderList(); ckRenderEditor();

    // 用語は「その表専用の用語」と「SQL式がその表を引くもの」を消す
    // （説明文だけの全体用語は残る — サーバ側の掃除と同じ）
    glItems = glItems.filter(it => it.scope !== name && !uses(it.sql));
    if (!glItems.some(it => it.id === glSelId)) glSelId = glItems[0]?.id ?? null;
    glRenderList(); glRenderEditor();
    recomputeMetrics();

    // この表を引いていた記述も一緒に下ろしている。黙って消すと、
    // あとで「書いたはずの例文が無い」となって原因が分からなくなる
    const lost = [
        [before.ex - exItems.length, '例文'],
        [before.ck - ckItems.length, '検算'],
        [before.gl - glItems.length, '用語'],
    ].filter(([n]) => n > 0).map(([n, label]) => `${label}${n}件`);
    if (lost.length) toast(`${name} を使っていた ${lost.join('・')} も一覧から外しました。`);
}

if (window.MANAGE) {
    window.MANAGE.refresh = () => loadManage(true);
    window.MANAGE.recompute = recomputeMetrics;
    window.MANAGE.scrubTable = scrubTableFromPanes;
    window.MANAGE.refreshViews = renderViews;   // 「ビュー」タブの一覧を描き直す
    // 消したテーブル（と空になったまとまり）の「未保存」も下ろす。
    // 残したままだと保存する相手がいないのに未保存バーが出続け、
    // Ctrl+S も効かず、ページを離れるたびに警告が出る
    window.MANAGE.clearDirty = (name, group) => {
        dirty.tables.delete(name);
        if (group) dirty.groups.delete(group);
        updateSavebar();
    };
}
})();

// ===== 利用状況（window.USAGE がある画面だけ動く） =====
(() => {
if (!window.USAGE) return;

let view = 'summary';            // いま見ているタブ
let chats = [];

const days = () => Number($('#uRange').value || 0);
const who = () => $('#uUser').value || '';

/* --- 集計タブ ----------------------------------------------------------------
   表は集計がそのまま返す形（columns/rows）で描き、グラフは「見て意味がある
   ものだけ」出す。全部にグラフを付けると、2列しかない表にまで棒が並んで
   かえって読みにくい。 */

/** その表をグラフにするなら何が向くか。向かなければ null。 */
function chartSpec(table) {
    const cols = table.columns || [], rows = table.rows || [];
    if (rows.length < 2 || cols.length < 2) return null;
    // 数値の列を探す（先頭列は見出しとして使う）
    const numIdx = cols.map((c, i) => i).slice(1)
        .filter(i => rows.every(r => typeof r[i] === 'number'));
    if (!numIdx.length) return null;
    const labels = rows.map(r => String(r[0]));
    // 日付が並ぶなら折れ線、それ以外は棒
    const isDate = labels.every(v => /^\d{4}-\d{2}-\d{2}$/.test(v));
    return {
        type: isDate ? 'scatter' : 'bar',
        labels,
        series: numIdx.slice(0, 3).map(i => ({ name: cols[i], values: rows.map(r => r[i]) })),
    };
}

function drawChart(box, spec) {
    const dark = document.documentElement.dataset.theme === 'dark'
        || (!document.documentElement.dataset.theme
            && matchMedia('(prefers-color-scheme: dark)').matches);
    const data = spec.series.map(s => ({
        type: spec.type, mode: spec.type === 'scatter' ? 'lines+markers' : undefined,
        name: s.name, x: spec.labels, y: s.values,
    }));
    Plotly.newPlot(box, data, {
        margin: { l: 48, r: 16, t: 8, b: 72 },
        height: 260,
        showlegend: spec.series.length > 1,
        paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)',
        font: { color: dark ? '#d7d3cc' : '#3c3a36', size: 11 },
        xaxis: { automargin: true }, yaxis: { automargin: true },
    }, { displayModeBar: false, responsive: true });
}

function renderTable(t) {
    const wrap = el('div', { class: 'card' });
    if (t.title) wrap.append(el('div', { class: 'card__title' }, t.title));
    const table = el('table', { class: 'data' },
        el('thead', {}, el('tr', {}, ...(t.columns || []).map(c => el('th', {}, String(c))))),
        el('tbody', {}, ...(t.rows || []).map(r =>
            el('tr', {}, ...r.map(v => el('td', {}, v === null || v === undefined ? '' : String(v)))))));
    wrap.append(el('div', { class: 'tablewrap' }, table));
    const spec = chartSpec(t);
    if (spec) {
        const box = el('div', { style: 'margin-top:10px' });
        wrap.append(box);
        setTimeout(() => drawChart(box, spec), 0);   // DOMに入ってから描く
    }
    return wrap;
}

async function loadReport() {
    const body = $('#uBody'), notes = $('#uNotes');
    body.replaceChildren(el('div', { class: 'small muted' }, '集計しています…'));
    notes.replaceChildren();
    let r;
    try {
        r = await api(`/api/usage/report?method=${encodeURIComponent(view)}`
                      + `&days=${days()}&user=${encodeURIComponent(who())}`,
                      undefined, 'GET');
    } catch (e) {
        body.replaceChildren(el('div', { class: 'alert alert--warn' }, e.message));
        return;
    }
    notes.replaceChildren(...(r.notes || []).map(n =>
        el('div', { class: 'small muted', style: 'margin-bottom:4px' }, n)));
    body.replaceChildren(...(r.tables || []).length
        ? (r.tables || []).map(renderTable)
        : [el('div', { class: 'empty' }, 'この条件では、集計できる記録がありません。')]);
}

/* --- チャット履歴 ------------------------------------------------------------
   一覧は「誰の・いつ・何を聞いたか」だけ。本文は選んだ1本だけ読みに行く。 */

/* 1行 = 1つの質問と、その回答。純粋な表で、行を押して開くものは無い。
   見出しはExcel風: クリックで並び替え（昇順→降順→解除）、▾で値を選んで絞り込む。 */

let qaSortCol = null, qaSortDir = 1;
const qaColFilters = [null, null, null, null, null];   // Set なら「その値の行だけ」

/** 並び替え・絞り込みに使う、1行ぶんの列の値。表示と同じ内容にする。 */
function qaRowValues({ c, x }) {
    return [x.at, c.user,
            `${c.title || '（無題）'}　${c.id}`,
            x.text,
            [...(x.marks || []), x.answer].filter(Boolean).join(' ')];
}

function qaRows() {
    const q = ($('#uChatFilter').value || '').trim().toLowerCase();
    const all = chats.flatMap(c => (c.questions || []).map(x => ({ c, x })));
    const hit = all
        .filter(({ c, x }) => !q
            || `${c.user} ${c.id} ${c.title} ${x.text} ${x.answer}`.toLowerCase().includes(q))
        .filter(r => qaRowValues(r).every((v, i) => !qaColFilters[i] || qaColFilters[i].has(v)));
    if (qaSortCol !== null) {
        hit.sort((a, b) => qaRowValues(a)[qaSortCol]
            .localeCompare(qaRowValues(b)[qaSortCol], 'ja') * qaSortDir);
    }
    return { all, hit };
}

/* --- 見出しの配線 ------------------------------------------------------------ */

function qaUpdateHeader() {
    $$('#pane-chats thead th').forEach((th, i) => {
        const arrow = th.querySelector('.qa__arrow');
        if (arrow) arrow.textContent = qaSortCol === i ? (qaSortDir === 1 ? '▲' : '▼') : '';
        th.querySelector('.qa__flt')?.classList.toggle('is-on', !!qaColFilters[i]);
    });
}

function wireQaHeader() {
    $$('#pane-chats thead th').forEach((th, i) => {
        const label = th.textContent;
        th.replaceChildren(
            el('button', { class: 'qa__sort', title: 'クリックで並び替え',
                onclick: () => {
                    if (qaSortCol !== i) { qaSortCol = i; qaSortDir = 1; }
                    else if (qaSortDir === 1) { qaSortDir = -1; }
                    else { qaSortCol = null; }        // 3回目で元の並びに戻す
                    qaUpdateHeader(); renderChatList();
                } }, label, el('span', { class: 'qa__arrow' })),
            el('button', { class: 'qa__flt', title: 'この列の値で絞り込む',
                onclick: ev => { ev.stopPropagation(); qaOpenFilter(i, th); } }, '▾'));
    });
}

/* --- 列フィルターの小窓 -------------------------------------------------------
   Excelのオートフィルターと同じ考え方: 値の一覧は「他の列の絞り込みを
   適用した後」に残る値から作り、チェックした値の行だけを表示する。 */

let qaPop = null;

function qaCloseFilter() {
    qaPop?.remove(); qaPop = null;
    document.removeEventListener('click', qaCloseFilter);
}

function qaOpenFilter(col, th) {
    qaCloseFilter();
    const q = ($('#uChatFilter').value || '').trim().toLowerCase();
    const rows = chats.flatMap(c => (c.questions || []).map(x => ({ c, x })))
        .filter(({ c, x }) => !q
            || `${c.user} ${c.id} ${c.title} ${x.text} ${x.answer}`.toLowerCase().includes(q))
        .filter(r => qaRowValues(r).every((v, i) =>
            i === col || !qaColFilters[i] || qaColFilters[i].has(v)));
    const counts = new Map();
    rows.forEach(r => {
        const v = qaRowValues(r)[col];
        counts.set(v, (counts.get(v) || 0) + 1);
    });
    const values = [...counts.keys()].sort((a, b) => a.localeCompare(b, 'ja'));
    const picked = new Set(qaColFilters[col] || values);

    const apply = () => {
        // 全部チェック＝絞り込み無しに戻す（見出しの印も消える）
        qaColFilters[col] = picked.size >= values.length ? null : new Set(picked);
        qaUpdateHeader(); renderChatList();
    };

    const list = el('div', { class: 'qa-pop__list' });
    const renderList = (needle = '') => {
        list.replaceChildren(...values
            .filter(v => !needle || v.toLowerCase().includes(needle))
            .map(v => {
                const cb = el('input', { type: 'checkbox',
                    ...(picked.has(v) ? { checked: 'checked' } : {}),
                    onchange: () => { cb.checked ? picked.add(v) : picked.delete(v); apply(); } });
                return el('label', { class: 'qa-pop__item', title: v },
                          cb, el('span', {}, `${v}（${counts.get(v)}）`));
            }));
    };
    const search = el('input', { type: 'text', placeholder: '値を検索',
        oninput: () => renderList(search.value.trim().toLowerCase()) });
    renderList();

    qaPop = el('div', { class: 'qa-pop', onclick: ev => ev.stopPropagation() },
        search,
        el('div', { class: 'row mt', style: 'gap:6px' },
            el('button', { class: 'btn btn--sm', onclick: () => {
                values.forEach(v => picked.add(v)); apply();
                list.querySelectorAll('input').forEach(cb => { cb.checked = true; });
            } }, 'すべて選択'),
            el('button', { class: 'btn btn--sm btn--ghost', onclick: () => {
                picked.clear(); apply();
                list.querySelectorAll('input').forEach(cb => { cb.checked = false; });
            } }, 'すべて解除'),
            el('div', { class: 'spacer' }),
            el('button', { class: 'btn btn--sm btn--ghost', onclick: qaCloseFilter }, '閉じる')),
        list);
    document.body.append(qaPop);
    const r = th.getBoundingClientRect();
    qaPop.style.top = `${Math.round(r.bottom + 4)}px`;
    qaPop.style.left = `${Math.round(Math.min(r.left, window.innerWidth - 280))}px`;
    setTimeout(() => document.addEventListener('click', qaCloseFilter), 0);
}

function renderChatList() {
    const { all, hit } = qaRows();
    const body = $('#uQaBody');
    body.replaceChildren(...hit.slice(0, 500).map(({ c, x }) => {
        const answer = [...(x.marks || []), x.answer].filter(Boolean).join(' ');
        return el('tr', {},
            el('td', { class: 'muted small' }, x.at),
            el('td', {}, c.user),
            el('td', {},
                el('div', { class: 'qa__clamp', title: c.title || '' }, c.title || '（無題）'),
                el('div', { class: 'small muted' }, c.id,
                    ...(c.errors ? [' ', el('span', { class: 'badge badge--warn' }, `失敗${c.errors}`)] : []))),
            el('td', { title: x.text },
                el('div', { class: 'qa__clamp' }, x.text)),
            el('td', { class: 'qa__a', title: answer },
                el('div', { class: 'qa__clamp' }, answer || '（回答なし）')));
    }));
    if (!hit.length) {
        body.replaceChildren(el('tr', {},
            el('td', { colspan: '5', class: 'muted' }, '一致する質問がありません。')));
    }
    $('#uChatCount').textContent = hit.length === all.length
        ? `${all.length}質問` : `${all.length}質問中 ${hit.length}件`;
    if (hit.length > 500) {
        $('#uChatCount').textContent += '（表示は先頭500件）';
    }
}

async function loadChats() {
    $('#uQaBody').replaceChildren(el('tr', {},
        el('td', { colspan: '5', class: 'muted' }, '読み込み中…')));
    // 所見は集計から。表は「質問と回答」だけを出す（会話に紐づいたものを使う）
    api(`/api/usage/report?method=questions&days=${days()}`
        + `&user=${encodeURIComponent(who())}`, undefined, 'GET')
        .then(r => $('#uQNotes').replaceChildren(
            ...(r.notes || []).map(n => el('div', { class: 'small muted' }, n))))
        .catch(() => {});
    try {
        const r = await api(`/api/usage/chats?days=${days()}&user=${encodeURIComponent(who())}`,
                            undefined, 'GET');
        chats = r.chats || [];
    } catch (e) {
        $('#uQaBody').replaceChildren(el('tr', {},
            el('td', { colspan: '5' }, el('div', { class: 'alert alert--warn' }, e.message))));
        return;
    }
    renderChatList();
}

/* --- タブ・条件・Excel ------------------------------------------------------- */

function showTab(key) {
    $$('.tab').forEach(t => t.classList.toggle('is-active', t.dataset.view === key));
    const isChats = key === 'chats';
    $('#pane-report').classList.toggle('is-active', !isChats);
    $('#pane-chats').classList.toggle('is-active', isChats);
    if (isChats) { loadChats(); } else { view = key; loadReport(); }
}

async function exportExcel() {
    const btn = $('#uExport');
    // いま見ているタブのぶんだけ出す。質問・履歴タブは「質問」の集計になる
    const methods = [$('#pane-chats').classList.contains('is-active') ? 'questions' : view];
    btn.disabled = true;
    const label = btn.textContent;
    btn.textContent = '作成中…';
    try {
        const r = await api('/api/usage/export',
                            { methods, days: days(), user: who() });
        toast(`${r.filename} を作りました（${r.sheets}シート）。`);
        location.href = r.url;
    } catch (e) {
        toast(e.message, 'err');
    } finally {
        btn.disabled = false;
        btn.textContent = label;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    $$('.tab').forEach(t => t.addEventListener('click', () => showTab(t.dataset.view)));
    $('#uRange').addEventListener('change', () =>
        $('#pane-chats').classList.contains('is-active') ? loadChats() : loadReport());
    $('#uUser').addEventListener('change', () =>
        $('#pane-chats').classList.contains('is-active') ? loadChats() : loadReport());
    $('#uChatFilter').addEventListener('input', renderChatList);
    wireQaHeader();
    $('#uExport').addEventListener('click', exportExcel);
    loadReport();
});
})();

// ===== 元 import.js（window.IMP がある画面だけ動く） =====
(() => {
if (!window.IMP) return;
/* データ取り込み画面。プレビュー 列の設定 取り込み先 実行 / 定期登録。 */

let plan = [];          // 列の設定
let previewInfo = null;
// いま選ばれている取り込み元。サーバのファイル（path）か、アップロード（upload）のどちらか。
let source = null;      // {kind:'server'|'upload', path?, upload?, name}

function readOptions() {
    return {
        path: source?.kind === 'server' ? source.path : '',
        upload: source?.kind === 'upload' ? source.upload : null,
        sheet: $('#sheetWrap').classList.contains('hidden') ? null : $('#sheet').value,
        header_row: Math.max(0, parseInt($('#headerRow').value || '1', 10) - 1),
        delimiter: $('#delimiter').value,
    };
}

/* --- 取り込み元フォルダの管理 --------------------------------------------------- */

async function loadDirs() {
    const r = await api('/api/import/dirs', undefined, 'GET');
    const box = $('#dirList');
    box.replaceChildren(...r.dirs.map(d => el('div', {
        class: 'row', style: 'align-items:center;gap:8px;padding:5px 0;'
            + 'border-bottom:1px solid var(--border)',
    },
        el('span', { class: d.ok ? 'badge badge--ok': 'badge badge--err' }, d['状態']),
        el('code', { class: 'grow', title: d['実際のパス'] }, d['設定値']),
        el('span', { class: 'badge' }, d.source === 'env'? '.env': '画面から追加'),
        (r.editable && d.removable) ? el('button', {
            class: 'btn btn--sm btn--danger',
            onclick: async () => {
                if (!confirm(`${d['設定値']} を取り込み元から外しますか？\n（フォルダ自体は削除されません）`)) return;
                await api('/api/import/dirs', { action: 'remove', path: d['設定値'] });
                toast('取り込み元から外しました。');
                loadDirs();
            },
        }, '外す') : null)));
    if (!r.dirs.length) box.append(el('div', { class: 'small muted' }, '登録がありません。'));
}

function wireDirs() {
    const add = $('#addDir');
    if (!add) return;
    const submit = async () => {
        const v = $('#newDir').value.trim();
        if (!v) return;
        add.disabled = true;
        try {
            await api('/api/import/dirs', { action: 'add', path: v });
            $('#newDir').value = '';
            toast('取り込み元フォルダを追加しました。');
            loadDirs();
        } catch (e) { toast(e.message, 'err', 8000); }
        add.disabled = false;
    };
    add.addEventListener('click', submit);
    $('#newDir').addEventListener('keydown', ev => { if (ev.key === 'Enter') submit(); });
}

/* --- サーバのフォルダを辿るダイアログ -------------------------------------------- */

async function openBrowser(path) {
    $('#browser').classList.remove('hidden');
    const list = $('#browserList');
    list.replaceChildren(el('div', { class: 'fsrow' }, el('span', { class: 'spinner' }), '読み込み中...'));
    let r;
    try {
        r = await api('/api/import/browse', { path: path || null });
    } catch (e) {
        list.replaceChildren(el('div', { class: 'alert alert--err' }, e.message));
        return;
    }

    $('#crumbs').replaceChildren(...r.crumbs.flatMap((c, i) => [
        i ? el('span', { class: 'muted' }, '/') : null,
        el('button', { onclick: () => openBrowser(c.path) }, c.name),
    ]).filter(Boolean));
    if (!r.crumbs.length) $('#crumbs').replaceChildren(el('span', { class: 'muted' }, '取り込み元フォルダ'));

    const rows = [];
    if (r.parent) {
        rows.push(el('div', { class: 'fsrow', onclick: () => openBrowser(r.parent) },
            icon('back', 'icon--sm'), el('span', { class: 'name' }, '上のフォルダへ')));
    }
    r.dirs.forEach(d => rows.push(el('div', { class: 'fsrow', onclick: () => openBrowser(d.path) },
        icon('folder', 'icon--sm'), el('span', { class: 'name' }, d.name))));
    r.files.forEach(f => rows.push(el('div', {
        class: 'fsrow',
        onclick: () => { chooseServerFile(f.path, f.name); closeBrowser(); },
    },
        icon('file', 'icon--sm'), el('span', { class: 'name' }, f.name),
        el('span', { class: 'meta' }, `${(f.size / 1024).toFixed(0)} KB ・ ${f.mtime}`))));
    if (!rows.length) rows.push(el('div', { class: 'small muted', style: 'padding:12px' },
        'このフォルダには取り込めるファイルがありません。'));
    list.replaceChildren(...rows);
}

function closeBrowser() { $('#browser').classList.add('hidden'); }

/* --- 選択の確定 ----------------------------------------------------------------- */

function showChosen(icon, label, note) {
    $('#chosen').replaceChildren(el('div', { class: 'chosenfile' },
        el('span', {}, icon),
        el('div', { class: 'grow' },
            el('div', { style: 'font-weight:700' }, label),
            note ? el('div', { class: 'small muted' }, note) : null)));
    $('#readOpts').classList.remove('hidden');
}

function chooseServerFile(path, name) {
    source = { kind: 'server', path, name };
    showChosen('', name, path);
    loadPreview();
}

async function chooseLocalFile(file) {
    const fd = new FormData();
    fd.append('file', file);
    showChosen('', file.name, 'アップロード中...');
    try {
        const res = await fetch('/api/import/upload', { method: 'POST', body: fd });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || 'アップロードに失敗しました');
        source = { kind: 'upload', upload: data.upload, name: data.name };
        showChosen('', data.name,
            `自分のPCから（${(data.size / 1024).toFixed(0)} KB）・定期取り込みには登録できません`);
        loadPreview();
    } catch (e) {
        toast(e.message, 'err', 8000);
        $('#chosen').replaceChildren(el('div', { class: 'alert alert--err' }, e.message));
    }
}

/* --- プレビュー --------------------------------------------------------------- */

async function loadPreview() {
    if (!source) return;
    const area = $('#previewArea');
    area.replaceChildren(el('div', { class: 'card' },
        el('span', { class: 'spinner' }), '読み込み中...'));
    try {
        const r = await api('/api/import/preview', readOptions());
        previewInfo = r;
        plan = r.plan.map(p => ({
            source: p['元の列名'], name: p['列名'], type: p['型'], include: true,
        }));
        // Excel ならシート欄を出す
        const has = (r.sheets || []).length > 0;
        $('#sheetWrap').classList.toggle('hidden', !has);
        $('#sepWrap').classList.toggle('hidden', has);
        if (has && $('#sheet').options.length !== r.sheets.length) {
            $('#sheet').replaceChildren(...r.sheets.map(s => el('option', {}, s)));
        }
        renderPreview(r);
    } catch (e) {
        area.replaceChildren(el('div', { class: 'alert alert--err' }, e.message));
    }
}

function renderPreview(r) {

    const area = $('#previewArea');
    area.replaceChildren(
        el('div', { class: 'card' },
            el('div', { class: 'card__title' }, 'プレビュー'),
            el('div', { class: 'card__desc' },
                `先頭 ${Math.min(30, r.rows.length)} 行 / 読み込んだ ${r.scanned.toLocaleString()} 行から型を推定しています。`
                + '　いちばん右の取得日時は取り込み時に自動で追加される列です。'),
            el('div', { id: 'previewTable' })),

        el('div', { class: 'card' },
            el('div', { class: 'card__title' }, '列の設定'),
            el('div', { id: 'planTable' })),

        el('div', { class: 'card' },
            el('div', { class: 'card__title' }, '取り込み先'),
            el('div', { class: 'row mb', style: 'align-items:flex-end' },
                el('div', { style: 'width:260px' },
                    el('label', { class: 'field' }, 'まとまり'),
                    el('select', { id: 'groupPick', onchange: syncTableName },
                        el('option', { value: '' }, '（選んでください）'),
                        ...(IMP.groups || []).map(g =>
                            el('option', { value: g.key }, g.key)),
                        el('option', { value: '__new__' }, '＋ 新しいまとまりを作る'))),
                el('div', { id: 'newGroupWrap', class: 'hidden', style: 'width:200px' },
                    el('label', { class: 'field' }, '新しいまとまりの名前'),
                    el('input', { type: 'text', id: 'newGroup', placeholder: '例）購買管理（日本語OK）',
                        oninput: syncTableName })),
                el('div', { style: 'width:240px' },
                    el('label', { class: 'field' }, 'テーブル名'),
                    el('input', { type: 'text', id: 'tableName',
                        value: splitGroup(r.suggest_table).name,
                        oninput: syncTableName }))),
            el('div', { class: 'small muted mb', id: 'tableNameHint' }),
            el('div', { class: 'row mb' },
                el('div', { style: 'width:320px' },
                    el('label', { class: 'field' }, '更新のしかた'),
                    el('select', { id: 'mode', onchange: syncMode },
                        Object.entries(IMP.modes).map(([k, v]) =>
                            el('option', { value: k }, v)))),
                el('div', { style: 'width:240px' },
                    el('label', { class: 'field' },
                        '取得日時の列名 ', el('span', { class: 'badge badge--err' }, '必須')),
                    el('input', { type: 'text', id: 'tsCol', value: IMP.defaultTs,
                        oninput: renderColumnPlan })),
                el('div', { id: 'keepWrap', class: 'hidden', style: 'width:220px' },
                    el('label', { class: 'field' },
                        '保存回数 ', el('span', { class: 'badge badge--err' }, '必須')),
                    el('input', { type: 'number', id: 'keepRuns', value: '',
                        placeholder: `1〜${IMP.maxKeep}`,
                        min: '1', max: String(IMP.maxKeep) }))),
            el('div', { class: 'small muted mb' },
                '取得日時の列は更新の仕方によらず必ず追加され、取り込んだ日時が入ります。'),
            el('div', { id: 'appendNote', class: 'hidden small muted mb' },
                `追記では、取り込み1回ぶんを「1回」と数え、新しい方から最大 ${IMP.maxKeep} 回分まで保持できます。`
                + '上限を超えた古い回は取り込みのたびに自動で削除されます'
                + '（取得日時が入っていない既存の行は消しません）。'),
            el('div', { id: 'destNote' }),

            // 登録の欄は別カードに分けない。更新のしかたを選んだ時点で
            // 「何を聞くか・ボタンが何をするか」まで決まるので、離れた場所に
            // もう1つ設定の塊があると、そちらを見落として片手落ちの登録になる。
            el('div', { class: 'row mt' },
                el('div', { id: 'jobNameWrap', class: 'grow', style: 'max-width:480px' },
                    el('label', { class: 'field' }, '設定の名前'),
                    el('input', { type: 'text', id: 'jobName',
                        value: `${r.suggest_table} の取り込み` })),
                el('div', { id: 'jobStartWrap', class: 'hidden', style: 'width:210px' },
                    el('label', { class: 'field' }, '開始日時'),
                    el('input', { type: 'datetime-local', id: 'jobStart' })),
                el('div', { id: 'jobIntervalWrap', class: 'hidden', style: 'width:170px' },
                    el('label', { class: 'field' },
                        '更新間隔 ', el('span', { class: 'badge badge--err' }, '必須')),
                    el('select', { id: 'jobInterval' },
                        IMP.intervals
                            // 追記でしか出さない欄なので「手動のみ」は候補から外す
                            .filter(i => i !== '手動のみ')
                            .map(i => el('option',
                                { ...(i === '1日ごと' ? { selected: 'selected' } : {}) }, i))))),
            el('div', { id: 'jobNote', class: 'small muted mt' }),
            el('div', { class: 'row mt' },
                el('button', { class: 'btn btn--primary', id: 'goBtn' }, '登録して取り込む'),
                el('div', { class: 'spacer' }))));

    $('#tableName').addEventListener('input', syncDest);
    // ボタンは1つだけ。何が起こるかはモードと取り込み元で決まり、ラベルがそれを言う
    $('#goBtn').addEventListener('click', ev => {
        if (source?.kind === 'upload') runImport(ev);
        else saveJob();
    });
    // 開始日時は過去を選べないようにする（分単位で今から）
    const jobStart = $('#jobStart');
    if (jobStart) jobStart.min = localNow();
    renderColumnPlan();
    // ファイル名が「まとまり__表名」の形なら、そのまとまりを初期選択する
    const guess = splitGroup(r.suggest_table).group;
    const pick = $('#groupPick');
    if (guess && pick) {
        if ([...pick.options].some(o => o.value === guess)) {
            pick.value = guess;
        } else {
            pick.value = '__new__';
            $('#newGroup').value = guess;
        }
    }
    syncMode(); syncDest(); syncTableName();
}

/** datetime-local に入れる「今」。ローカル時刻の YYYY-MM-DDTHH:MM。 */
function localNow(offsetMinutes = 0) {
    const d = new Date(Date.now() + offsetMinutes * 60000);
    const p = n => String(n).padStart(2, '0');
    return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`
         + `T${p(d.getHours())}:${p(d.getMinutes())}`;
}

/** 取得日時の列名。空なら既定値。 */
function tsName() {
    return ($('#tsCol')?.value || '').trim();
}

/** プレビューと「列の設定」を描き直す。取得日時の列も混ぜて見せる。 */
function renderColumnPlan() {
    const ts = tsName();
    const stamp = localNow().replace('T', ' ') + ':00';

    const pv = $('#previewTable');
    if (pv && previewInfo) {
        const cols = [...previewInfo.columns, ts ? `${ts}（自動追加）` : '（取得日時：列名が未入力）'];
        const rows = previewInfo.rows.slice(0, 30).map(r => [...r, ts ? stamp : '—']);
        pv.replaceChildren(dataTable(cols, rows));
    }

    const box = $('#planTable');
    if (!box) return;
    const rows = plan.map((c, i) => el('tr', {},
        el('td', {}, el('input', {
            type: 'checkbox', ...(c.include ? { checked: 'checked' } : {}),
            onchange: ev => { plan[i].include = ev.target.checked; },
        })),
        el('td', { class: 'muted' }, c.source),
        el('td', {}, el('input', {
            type: 'text', value: c.name,
            onchange: ev => { plan[i].name = ev.target.value; },
        })),
        el('td', {}, el('select', {
            onchange: ev => { plan[i].type = ev.target.value; },
        }, ['TEXT', 'INTEGER', 'REAL'].map(t =>
            el('option', { value: t, ...(t === c.type ? { selected: 'selected' } : {}) }, t))))));

    // 自動で足される取得日時の行。外せないので操作欄は出さない。
    rows.push(el('tr', { style: 'background:var(--accent-weak)' },
        el('td', {}, '自動'),
        el('td', { class: 'muted' }, '（取り込み日時）'),
        el('td', {}, ts
            ? el('b', {}, ts)
            : el('span', { style: 'color:var(--err)' }, '列名を入力してください')),
        el('td', {}, 'TEXT')));

    box.replaceChildren(el('div', { class: 'tablewrap', style: 'max-height:340px' },
        el('table', { class: 'data' },
            el('thead', {}, el('tr', {},
                el('th', { style: 'width:52px' }, '取込'), el('th', {}, '元の列名'),
                el('th', {}, '列名（保存側）'), el('th', { style: 'width:120px' }, '型'))),
            el('tbody', {}, rows))));
}

/* 取り込み方は2通りしかない。更新のしかたを選んだ時点で、その後に聞くことが決まる。
 *
 *   全件入れ替え … 元ファイルの鏡写し。登録した時点で1回取り込み、以降は
 *                  質問のたびに元ファイルを見て、変わっていれば取り込み直す。
 *                  定期実行は使わない（間隔を聞かない）。
 *   追記         … 時系列で溜める。いつ溜めるかが決まらないと意味をなさないので
 *                  更新間隔が必須。逆に「いま取り込む」は使わせない
 *                  （手で押すと1回ぶん余計に増えて、保存回数の数え方が崩れる）。 */
/* --- 取り込み先の「まとまり」 -------------------------------------------------
   まとまりは表名の接頭辞（まとまり__表名）で決まる。利用者に規約を手入力
   させないよう、ここで選ばせて名前を組み立てる。 */

function splitGroup(name) {
    const i = String(name || '').indexOf('__');
    return i > 0 ? { group: name.slice(0, i), name: name.slice(i + 2) }
                 : { group: '', name: String(name || '') };
}

function chosenGroup() {
    const pick = $('#groupPick');
    if (!pick) return '';
    return pick.value === '__new__' ? ($('#newGroup')?.value || '').trim() : pick.value;
}

function finalTableName() {
    const base = ($('#tableName')?.value || '').trim();
    const g = chosenGroup();
    return (g && base) ? `${g}__${base}` : '';     // どちらか欠けたら取り込ませない
}

function syncTableName() {
    const wrap = $('#newGroupWrap');
    if (wrap) wrap.classList.toggle('hidden', $('#groupPick').value !== '__new__');
    const hint = $('#tableNameHint');
    if (!hint) return;
    const g = chosenGroup(), base = ($('#tableName')?.value || '').trim();
    hint.textContent = !g ? 'まとまりを選んでください。'
        : !base ? 'テーブル名を入れてください。'
        : `できるテーブル: ${finalTableName()}（カタログでは「${g}」のまとまりに入ります）`;
    syncDest();          // 取り込み先が変わる＝重複の判定もやり直す
}

function syncMode() {
    const append = $('#mode').value === 'append';
    const upload = source?.kind === 'upload';
    ['#keepWrap', '#appendNote'].forEach(s => $(s)?.classList.toggle('hidden', !append));
    $('#jobIntervalWrap')?.classList.toggle('hidden', !append || upload);
    $('#jobStartWrap')?.classList.toggle('hidden', !append || upload);
    // アップロードは登録できない（サーバに残らず読み直せない）ので、名前も聞かない
    $('#jobNameWrap')?.classList.toggle('hidden', upload);

    const go = $('#goBtn');
    if (go) {
        go.textContent = upload
            ? 'いま取り込む（この1回だけ）'
            : (append ? '登録する' : '登録して取り込む');
        go.disabled = upload && append;    // 追記×アップロードは成立しない（下の説明参照）
    }

    const note = $('#jobNote');
    if (note) {
        let text;
        if (upload && append) {
            text = 'アップロードしたファイルは追記に使えません。'
                + 'サーバに残らないため定期実行に登録できず、手で1回だけ追記すると'
                + '保存回数の数え方が崩れるためです。'
                + '追記で溜めるなら、取り込み元フォルダに置いてから選び直してください。';
        } else if (upload) {
            text = 'アップロードしたファイルはサーバに残らないため、登録して追随はできません。'
                + 'この1回だけ取り込みます。以降も自動で追随させたいときは、'
                + '取り込み元フォルダに置いてから選び直してください。';
        } else if (append) {
            text = '決めた間隔で自動的に取り込み、1回ぶんずつ溜めます。'
                + '開始日時を入れると、その時刻を過ぎるまで動きません（空なら登録後すぐ対象）。'
                + '手動で1回だけ取り込むことはできません'
                + '（1回ぶん余計に増えて、保存回数の数え方が崩れるため）。';
        } else {
            text = '登録した時点で1回取り込みます。以降は、チャットで質問を受けるたびに'
                + '元ファイルの更新を確認し、変わっていればその場で取り込み直してから答えます。'
                + '定期実行の設定は要りません。'
                + 'ファイルが読めないときは、最後に取り込んだ内容で答えます'
                + '（そのときはカタログに警告が出ます）。';
        }
        note.replaceChildren(el('div', {}, text));
    }
    syncDest();
}

/** 保存前の必須チェック。足りなければ理由を配列で返す。 */
function formProblems(forJob = false) {
    const out = [];
    if (!tsName()) out.push('取得日時の列名を入力してください（必須）。');
    if ($('#mode').value === 'append') {
        const raw = ($('#keepRuns')?.value || '').trim();
        const keep = parseInt(raw, 10);
        if (!raw) out.push('保存回数を入力してください（必須）。');
        else if (!Number.isInteger(keep) || keep < 1 || keep > IMP.maxKeep) {
            out.push(`保存回数は 1〜${IMP.maxKeep} で指定してください。`);
        }
    }
    if (forJob) {
        const raw = ($('#jobStart')?.value || '').trim();
        // input の min だけでは手入力を防げないので、送る前にもう一度見る
        if (raw && raw < localNow(-2)) {
            out.push(`開始日時に過去の時刻は指定できません（指定: ${raw.replace('T', ' ')}）。`);
        }
    }
    return out;
}

function syncDest() {
    const dbFile = IMP.dbFiles[0];   // 保存先は常に唯一のDB（画面では見せない）
    const note = $('#destNote');
    note.replaceChildren();
    const go = $('#goBtn');
    // ボタンの土台（ラベルと「追記×アップロード」の禁止）は syncMode が決める。
    // ここでは取り込み先に固有の理由（管理中のテーブル）だけを重ねる。
    const baseDisabled = (source?.kind === 'upload') && $('#mode').value === 'append';
    if (go) { go.disabled = baseDisabled; go.title = ''; }
    const tables = IMP.existing[dbFile] || [];
    // 判定は「実際にできる表名（まとまり__表名）」で行う。素の表名で見ると、
    // まとまりを切り替えたときに既存の表を黙って上書きしてしまう。
    const t = finalTableName();
    // 表が100個を超えると、全部並べても読めない。狙っている先がどうなのかだけ言う
    note.append(el('div', { class: 'small muted' },
        tables.length ? `いま ${tables.length} テーブルあります。`
                      : 'まだテーブルはありません。'));

    if (!t) {
        note.append(el('div', { class: 'small muted mt' },
            'まとまりとテーブル名を決めると、ここに取り込み先の状態が出ます。'));
        if (go) { go.disabled = true; go.title = 'まとまりとテーブル名を決めてください。'; }
        return;
    }

    // 定期実行＋追記で管理中のテーブルには、上書きも二重登録もさせない
    const locked = (lockedTables[dbFile] || {})[t];
    if (locked) {
        note.append(el('div', { class: 'alert alert--warn mt' }, ''+ locked));
        if (go) { go.disabled = true; go.title = '' + locked; }
        return;
    }
    if (tables.includes(t)) {
        // 追記でも「同じ表に足す」ことは伝える。黙って混ざるのがいちばん困る
        note.append(el('div', { class: 'alert alert--warn mt' },
            $('#mode').value === 'replace'
                ? `${t} は既にあります。全件入れ替えなので、いま入っている行はすべて削除されて入れ直されます。`
                : `${t} は既にあります。追記なので、いまの行を残したまま下に足します。`));
    } else {
        note.append(el('div', { class: 'small muted mt' }, `${t} は新しく作られます。`));
    }
}

function importPayload() {
    return {
        ...readOptions(),
        table: finalTableName(), mode: $('#mode').value,
        timestamp_column: $('#tsCol')?.value || null,
        keep_runs: $('#mode').value === 'append' ? $('#keepRuns')?.value : null,
        columns: plan,
    };
}

async function runImport(ev) {
    const bad = formProblems();
    if (bad.length) { bad.forEach(m => toast(m, 'warn')); return; }
    ev.target.disabled = true;
    ev.target.innerHTML = '<span class="spinner"></span> 取り込み中';
    try {
        const r = await api('/api/import/run', importPayload());
        let msg = `${r.table} に ${r.rows.toLocaleString()}行を取り込みました。`;
        if (r.timestamp_column) msg += ` 取得日時列「${r.timestamp_column}」つき。`;
        if (r.keep) msg += ` 保持 ${r.kept}/${r.keep}回`;
        if (r.removed) msg += `（古い ${r.removed.toLocaleString()}行を削除）`;
        toast(msg, 'ok', 8000);
        if (r.degraded?.length) {
            toast(`数値にできない値があったため TEXT で取り込んだ列: ${r.degraded.join(', ')}`, 'warn', 9000);
        }
        setTimeout(() => window.location.reload(), 1500);
    } catch (e) { toast(e.message, 'err', 9000); }
    ev.target.disabled = false;
    syncMode();                        // ラベルと有効/無効を元の状態に戻す
}

async function saveJob() {
    const bad = formProblems(true);
    if (bad.length) { bad.forEach(m => toast(m, 'warn')); return; }
    // 送信中はボタンを止める。二重クリックで同じ設定が2件できるのを防ぐ
    // （サーバ側でも同じ取り込み元→同じテーブルは弾く）
    const append = $('#mode').value === 'append';
    const btn = $('#goBtn');
    if (btn) {
        btn.disabled = true;
        btn.innerHTML = append
            ? '登録中…'
            : '<span class="spinner"></span> 登録して取り込み中';
    }
    try {
        // 送る形はモードで決まる。全件入れ替えは「間隔なし＋リアルタイム」、
        // 追記は「間隔あり＋リアルタイムなし」。サーバ側でも同じ形に寄せている。
        const r = await api('/api/jobs/save', {
            ...importPayload(), name: $('#jobName').value,
            interval: append ? $('#jobInterval').value : '手動のみ',
            start_at: append ? ($('#jobStart')?.value || '') : '',
            realtime: !append,
        });
        if (append) {
            toast('定期取り込みに登録しました。'
                + 'データカタログの各テーブルの「管理」で確認できます。', 'ok', 8000);
        } else if (r.first_run?.ok) {
            toast(`登録しました。${(r.first_run.rows || 0).toLocaleString()}行を取り込みました。`
                + '以降は質問のたびに元ファイルへ追随します。', 'ok', 8000);
        } else {
            // 登録自体は済んでいる。取り込みだけ失敗したことを取り違えないよう分けて出す
            toast('登録しましたが、最初の取り込みに失敗しました: '
                + (r.first_run?.message || '原因不明'), 'warn', 12000);
        }
        refreshLocked();
        if (!append && r.first_run?.ok) setTimeout(() => window.location.reload(), 1800);
    } catch (e) { toast(e.message, 'err', 9000); }
    if (btn) btn.disabled = false;
    syncMode();                        // ラベルと有効/無効を元の状態に戻す
}

/* --- 手で更新してはいけないテーブル ---------------------------------------------
   定期実行＋追記のテーブルは、手で足すと取得日時が1回ぶん余計に増えて間隔が崩れる。
   取り込み先を選ぶ欄でそのテーブルに鍵をかけるため、状態だけ取っておく。
   定期取り込みの一覧・操作・スケジューラの状態は「データカタログ > DB・テーブル」にある。 */
let lockedTables = {};

async function refreshLocked() {
    try {
        const m = await api('/api/import/manage', undefined, 'GET');
        lockedTables = m.locked || {};
        if ($('#tableName')) syncDest();
    } catch (e) { /* 鍵が取れなくても取り込みはできる */ }
}

/* --- 起動 ------------------------------------------------------------------- */

document.addEventListener('DOMContentLoaded', () => {
    loadDirs();
    wireDirs();
    $('#pickServer')?.addEventListener('click', () => openBrowser(null));
    $('#browserClose')?.addEventListener('click', closeBrowser);
    $('#browser')?.addEventListener('click', ev => {
        if (ev.target.id === 'browser') closeBrowser();   // 背景をクリックで閉じる
    });
    document.addEventListener('keydown', ev => {
        if (ev.key === 'Escape') closeBrowser();
    });
    $('#pickLocal')?.addEventListener('click', () => $('#localFile')?.click());
    $('#localFile')?.addEventListener('change', ev => {
        if (ev.target.files?.[0]) chooseLocalFile(ev.target.files[0]);
        ev.target.value = '';        // 同じファイルを選び直せるように
    });
    ['#sheet', '#delimiter', '#headerRow'].forEach(sel =>
        $(sel)?.addEventListener('change', loadPreview));
    $('#reload')?.addEventListener('click', loadPreview);

    lockedTables = (IMP.manage || {}).locked || {};
    if ($('#tableName')) syncDest();
});
})();

// ===== 元 knowledge.js（window.KB_INIT がある画面だけ動く） =====
(() => {
if (!window.KB_INIT) return;
/* ナレッジベース設定（管理者のみ）。
   LightRAG サーバの接続先を登録し、接続テストで疎通を確かめる。

   キーは一覧に埋め込まない。管理画面を開くたびにHTMLとして流れると、
   キャッシュやソース表示に残るため、「表示」を押したときだけ取りに行く。 */

let state = {};

/* 1件ぶんの行。編集はその場で行い、「保存」で確定する。 */
function baseRow(b) {
    const name = el('input', { type: 'text', value: b.name, style: 'width:100%' });
    const url = el('input', { type: 'text', value: b.base_url, style: 'width:100%' });
    const desc = el('input', {
        type: 'text', value: b.description || '', style: 'width:100%',
        placeholder: '何が入っているか・どんなときに使うか（AIがこれを読みます）',
    });
    const key = el('input', {
        type: 'password', value: '', style: 'width:100%', autocomplete: 'new-password',
        placeholder: b.has_api_key ? '••••（変えるときだけ入力）' : '未設定',
    });
    const on = el('input', { type: 'checkbox', ...(b.enabled ? { checked: 'checked' } : {}) });
    const result = el('div', { class: 'small muted mt' });

    const save = el('button', {
        class: 'btn btn--sm btn--primary',
        onclick: async ev => {
            ev.target.disabled = true;
            try {
                const r = await api(`/api/knowledge/${b.id}`, {
                    name: name.value, base_url: url.value, description: desc.value,
                    enabled: on.checked, api_key: key.value,
                });
                state.bases = r.bases;
                toast('保存しました。', 'ok');
                render();
            } catch (e) { toast(e.message, 'err', 9000); ev.target.disabled = false; }
        },
    }, '保存');

    const test = el('button', {
        class: 'btn btn--sm',
        onclick: async ev => {
            ev.target.disabled = true;
            ev.target.innerHTML = '<span class="spinner"></span> 確認中';
            result.replaceChildren();
            try {
                const r = await api(`/api/knowledge/${b.id}/test`, {});
                result.replaceChildren(el('div', {
                    class: `alert alert--${r.ok ? 'ok' : 'err'}`,
                    style: 'white-space:pre-wrap',
                }, r.ok ? `つながりました（${r.status}）。` : r.error));
            } catch (e) {
                result.replaceChildren(el('div', { class: 'alert alert--err' }, e.message));
            }
            ev.target.disabled = false;
            ev.target.textContent = '接続テスト';
        },
    }, '接続テスト');

    const reveal = el('button', {
        class: 'btn btn--sm btn--ghost',
        title: 'APIキーの実値を表示します',
        onclick: async ev => {
            ev.target.disabled = true;
            try {
                const r = await api(`/api/knowledge/${b.id}/key`, undefined, 'GET');
                key.type = 'text';
                key.value = r.api_key;
                key.placeholder = '';
            } catch (e) { toast(e.message, 'err', 9000); }
            ev.target.disabled = false;
        },
    }, '表示');

    const del = el('button', {
        class: 'btn btn--sm btn--ghost',
        onclick: async ev => {
            if (!confirm(`「${b.name}」を削除します。`
                + 'このナレッジベースはAIの検索対象から外れます。よろしいですか？')) return;
            ev.target.disabled = true;
            try {
                const r = await api(`/api/knowledge/${b.id}/delete`, {});
                state.bases = r.bases;
                toast('削除しました。', 'ok');
                render();
            } catch (e) { toast(e.message, 'err', 9000); ev.target.disabled = false; }
        },
    }, '削除');

    return el('div', { class: 'card', style: 'margin-bottom:10px' },
        el('div', { class: 'row' },
            el('div', { style: 'width:220px' },
                el('label', { class: 'field' }, '名前'), name),
            el('div', { class: 'grow', style: 'min-width:240px' },
                el('label', { class: 'field' }, 'URL'), url),
            el('div', { style: 'width:200px' },
                el('label', { class: 'field' }, 'APIキー'), key),
            b.has_api_key ? reveal : null),
        el('div', { class: 'row mt' },
            el('div', { class: 'grow' },
                el('label', { class: 'field' }, '説明（AIが読みます）'), desc)),
        el('div', { class: 'row mt', style: 'align-items:center' },
            el('label', { class: 'small', style: 'display:flex;gap:6px;align-items:center' },
                on, '検索対象にする（全利用者に効きます）'),
            el('div', { class: 'spacer' }),
            test, save, del),
        result);
}

function render() {
    const list = $('#kbList');
    const bases = state.bases || [];
    list.replaceChildren();
    if (!bases.length) {
        list.append(el('div', { class: 'small muted' },
            'まだ登録がありません。下の「ナレッジベースを追加」から登録してください。'));
    } else {
        bases.forEach(b => list.append(baseRow(b)));
    }

    // 上部のまとめ。0件のときは「AIに何が起きるか」まで書く
    const box = $('#banner');
    const live = bases.filter(b => b.enabled).length;
    box.replaceChildren(bases.length && live
        ? el('div', { class: 'alert alert--ok' },
            `${live} 件のナレッジベースを検索できます。`
            + 'チャットのAIは、質問の内容に応じてこの中から調べ先を選びます。')
        : el('div', { class: 'alert alert--info' },
            '検索できるナレッジベースがありません。'
            + 'この状態では、AIに社内文書の検索ツールを渡しません'
            + '（データの分析やファイル出力はこれまで通り使えます）。'));

    // 検索の効き方の初期値。ここは表示だけ（変えるのは env）
    const d = state.defaults || {};
    $('#defaults').replaceChildren(...(state.fields || []).map(f => {
        const v = d[f.key];
        const label = f.kind === 'choice'
            ? ((f.choices.find(c => c.value === v) || {}).label || v)
            : v;
        return el('div', { class: 'kvrow' },
            el('div', { class: 'kvrow__k' }, f.label),
            el('div', { class: 'grow' }, String(label),
                el('div', { class: 'small muted' }, f.help)));
    }));
}

document.addEventListener('DOMContentLoaded', () => {
    state = window.KB_INIT || {};
    render();

    $('#add').addEventListener('click', async ev => {
        ev.target.disabled = true;
        try {
            const r = await api('/api/knowledge', {
                name: $('#newName').value,
                base_url: $('#newUrl').value,
                api_key: $('#newKey').value,
                description: $('#newDesc').value,
            });
            state.bases = r.bases;
            ['#newName', '#newUrl', '#newKey', '#newDesc'].forEach(x => { $(x).value = ''; });
            toast('追加しました。「接続テスト」で疎通を確かめてください。', 'ok', 8000);
            render();
        } catch (e) { toast(e.message, 'err', 9000); }
        ev.target.disabled = false;
    });
});
})();

// ===== 元 mail.js（window.MAIL がある画面だけ動く） =====
(() => {
if (!window.MAIL) return;
/* メール設定。送信サーバ・差出人・送ってよい宛先を決める。

   送信は社内リレー宛（暗号化なし・認証なし）を前提にしている。
   外部SMTPを使う環境では env の SMTP_SECURITY / SMTP_USER / SMTP_PASSWORD を使う。 */

let state = {};                 // 画面で編集中の設定
const editable = () => !!window.IS_ADMIN;

function chipList(box, items, onRemove, empty) {
    box.replaceChildren();
    if (!items.length) {
        box.append(el('div', { class: 'small muted' }, empty));
        return;
    }
    box.append(el('div', { class: 'chips' }, items.map((v, i) =>
        el('span', { class: 'chip' }, v,
            editable() ? el('button', {
                class: 'chip__x', title: '削除',
                onclick: () => { onRemove(i); render(); },
            }, '×') : null))));
}

function render() {
    const s = state;

    // 送信サーバ
    $('#host').value = s.host || '';
    $('#port').value = s.port ?? 25;
    $('#timeout').value = s.timeout ?? 20;
    ['#host', '#port', '#timeout'].forEach(x => { $(x).disabled = !editable(); });

    const kv = (k, v) => el('div', { class: 'kvrow' },
        el('span', { class: 'kvrow__k' }, k), el('span', { class: 'mono' }, v));
    $('#serverInfo').replaceChildren(kv('設定ファイル', s.settings_file || ''));

    // 差出人
    const sel = $('#sender');
    const opts = [...new Set([...(s.senders || []), s.sender].filter(Boolean))];
    sel.replaceChildren(...(opts.length
        ? opts.map(v => el('option', { value: v, ...(v === s.sender ? { selected: 'selected' } : {}) }, v))
        : [el('option', { value: '' }, '（候補を追加してください）')]));
    sel.disabled = !editable();
    $('#senderName').value = s.sender_name || '';
    $('#senderName').disabled = !editable();
    chipList($('#senderList'), s.senders || [], i => {
        const removed = s.senders.splice(i, 1)[0];
        if (s.sender === removed) s.sender = s.senders[0] || '';
    }, '候補がありません。下の欄から追加してください。');

    // 宛先
    chipList($('#addrList'), s.allow_addresses || [],
        i => s.allow_addresses.splice(i, 1), '登録なし');
    // 取り込みの警告の通知先（管理者）
    chipList($('#alertList'), s.alert_to || [],
        i => s.alert_to.splice(i, 1), '登録なし（通知しません）');

    // 警告メールの ON/OFF と、知らせる種類
    const on = s.alert_enabled !== false;
    $('#alertEnabled').checked = on;
    $('#alertEnabled').disabled = !editable();
    $('#alertEnabled').onchange = () => { s.alert_enabled = $('#alertEnabled').checked; render(); };
    // 止めているあいだは種類を触らせない（何を選んでも送られないため）
    $('#alertKindsWrap').classList.toggle('muted', !on);
    const labels = s.alert_kind_labels || {};
    const picked = s.alert_kinds || [];
    $('#alertKinds').replaceChildren(...Object.keys(labels).map(kind => {
        const cb = el('input', {
            type: 'checkbox', ...(picked.includes(kind) ? { checked: 'checked' } : {}),
            ...((!on || !editable()) ? { disabled: 'disabled' } : {}),
            onchange: () => {
                const next = new Set(s.alert_kinds || []);
                cb.checked ? next.add(kind) : next.delete(kind);
                s.alert_kinds = Object.keys(labels).filter(k => next.has(k));
            },
        });
        return el('label', { class: 'row', style: 'align-items:center;gap:8px;cursor:pointer' },
            cb, el('span', {}, labels[kind]));
    }));
    const n = (s.allow_addresses || []).length;
    $('#allowState').replaceChildren(n
        ? el('div', { class: 'alert alert--ok' },
            `登録した ${n} 件のアドレスにだけ送信できます。`)
        : el('div', { class: 'alert alert--warn' },
            '宛先が1件も登録されていません。いまの状態ではどこにも送信できません。'));
    if (document.activeElement !== $('#okDomains')) {
        $('#okDomains').value = (s.allowed_domains || []).map(d => '@' + d).join('; ');
    }
    $('#okDomains').disabled = !editable();
    $('#domainNote').textContent = (s.allowed_domains || []).length
        ? `登録できるのは ${s.allowed_domains_label} のアドレスだけです。`
        : 'ドメインの制限はかかっていません（上の「登録してよいドメイン」で設定できます）。';

    $('#maxRecipients').value = s.max_recipients ?? 20;
    $('#dryRun').checked = !!s.dry_run;
    ['#maxRecipients', '#dryRun'].forEach(x => { $(x).disabled = !editable(); });
    $('#dryNote').replaceChildren(s.dry_run
        ? el('div', { class: 'alert alert--info' },
            'テスト送信モードです。チャットの「送信」を押しても外にはメールが出ず、'
            + '組み立てた内容の確認だけを行います。動作を確かめてから外してください。')
        : el('div', { class: 'alert alert--warn' },
            '本番送信モードです。チャットの「送信」を押すと実際にメールが送られます。'));

    // 上部のまとめ
    const box = $('#banner');
    box.replaceChildren();
    if ((s.problems || []).length) {
        box.append(el('div', { class: 'alert alert--err' },
            el('div', {}, 'このままではメールを送れません:'),
            el('ul', {}, s.problems.map(p => el('li', {}, p)))));
    } else {
        box.append(el('div', { class: 'alert alert--ok' },
            `送信できる状態です（${s.sender_name ? s.sender_name + ' <' + s.sender + '>' : s.sender}`
            + ` ${s.host}:${s.port}）。`));
    }
    if (!editable()) {
        box.append(el('div', { class: 'alert alert--info' },
            '設定の変更は管理者のみです。内容の確認だけできます。'));
    }
    ['#save', '#test', '#addSender', '#addAddr']
        .forEach(x => { const b = $(x); if (b) b.disabled = !editable(); });
}

function renderLog(list) {
    $('#logCount').textContent = list.length;
    const box = $('#logList');
    if (!list.length) {
        box.replaceChildren(el('div', { class: 'small muted' }, 'まだ送信していません。'));
        return;
    }
    box.replaceChildren(dataTable(
        ['日時', '結果', '宛先', '件名', '添付', 'モード', '実行者'],
        list.map(r => [
            (r.at || '').replace('T', ' '),
            r.ok ? '成功' : '失敗',
            (r.to || []).join(', ') + (r.bcc_count ? `（+Bcc ${r.bcc_count}）` : ''),
            r.subject || '',
            (r.attachments || []).join(', '),
            r.dry_run ? 'テスト' : '本番',
            r.user || '',
        ])));
}

function addTo(key, input, normalize) {
    const v = (input.value || '').trim();
    if (!v) return;
    const value = normalize ? normalize(v) : v;
    state[key] = state[key] || [];
    if (state[key].some(x => x.toLowerCase() === value.toLowerCase())) {
        toast('すでに登録されています。', 'warn');
        return;
    }
    state[key].push(value);
    input.value = '';
    if (key === 'senders' && !state.sender) state.sender = value;
    render();
}

async function load() {
    const r = await api('/api/mail/settings', undefined, 'GET');
    state = r;
    render();
    renderLog(r.log || []);
}

document.addEventListener('DOMContentLoaded', () => {
    state = window.MAIL || {};
    render();
    renderLog(window.MAIL_LOG || []);

    // 送信サーバ
    $('#host').addEventListener('input', ev => { state.host = ev.target.value.trim(); });
    $('#timeout').addEventListener('input',
        ev => { state.timeout = parseInt(ev.target.value || '20', 10); });
    $('#port').addEventListener('input',
        ev => { state.port = parseInt(ev.target.value || '25', 10); });

    $('#sender').addEventListener('change', ev => { state.sender = ev.target.value; });
    $('#senderName').addEventListener('input', ev => { state.sender_name = ev.target.value; });
    $('#maxRecipients').addEventListener('input',
        ev => { state.max_recipients = parseInt(ev.target.value || '20', 10); });
    $('#dryRun').addEventListener('change', ev => {
        state.dry_run = ev.target.checked;
        render();
    });

    $('#addSender').addEventListener('click', () => addTo('senders', $('#newSender')));
    $('#addAddr').addEventListener('click', () => {
        // 保存時にも弾かれるが、その場で言った方が直しやすい
        const v = ($('#newAddr').value || '').trim();
        const doms = state.allowed_domains || [];
        const dom = v.toLowerCase().split('@').pop();
        if (v && doms.length && !doms.some(d => dom === d || dom.endsWith('.' + d))) {
            toast(`${state.allowed_domains_label} のアドレスだけ登録できます。`, 'warn', 7000);
            return;
        }
        addTo('allow_addresses', $('#newAddr'));
    });
    $('#addAlert').addEventListener('click', () => {
        const v = ($('#newAlert').value || '').trim();
        const doms = state.allowed_domains || [];
        const dom = v.toLowerCase().split('@').pop();
        if (v && doms.length && !doms.some(d => dom === d || dom.endsWith('.' + d))) {
            toast(`${state.allowed_domains_label} のアドレスだけ登録できます。`, 'warn', 7000);
            return;
        }
        addTo('alert_to', $('#newAlert'));
    });
    [['#newSender', '#addSender'], ['#newAddr', '#addAddr'], ['#newAlert', '#addAlert']].forEach(([i, b]) =>
        $(i).addEventListener('keydown', ev => { if (ev.key === 'Enter') $(b).click(); }));

    $('#save').addEventListener('click', async ev => {
        ev.target.disabled = true;
        try {
            const r = await api('/api/mail/settings', {
                host: state.host, port: state.port, timeout: state.timeout,
                sender: state.sender, sender_name: state.sender_name,
                senders: state.senders || [],
                allow_addresses: state.allow_addresses || [],
                alert_to: state.alert_to || [],
                alert_enabled: state.alert_enabled !== false,
                alert_kinds: state.alert_kinds || [],
                max_recipients: state.max_recipients,
                dry_run: state.dry_run,
                ok_domains: $('#okDomains').value,
            });
            state = { ...state, ...r };
            toast('保存しました。', 'ok');
            render();
        } catch (e) { toast(e.message, 'err', 9000); }
        ev.target.disabled = false;
    });

    $('#test').addEventListener('click', async ev => {
        ev.target.disabled = true;
        ev.target.innerHTML = '<span class="spinner"></span> 確認中';
        try {
            const r = await api('/api/mail/test', {});
            toast(r.message, r.ok ? 'ok' : 'err', 9000);
        } catch (e) { toast(e.message, 'err', 9000); }
        ev.target.disabled = false;
        ev.target.textContent = '送信サーバへの接続を確認';
    });

    $('#reload').addEventListener('click', load);
});
})();

// ===== 元 models.js（window.MODELS がある画面だけ動く） =====
(() => {
if (!window.MODELS) return;
/* モデル設定（管理者のみ）。
   チャットのプルダウンに出す候補・既定・画像判定キーワードを決める。 */

let state = {};

function chips(box, items, onRemove, empty, decorate) {
    box.replaceChildren();
    if (!items.length) {
        box.append(el('div', { class: 'small muted' }, empty));
        return;
    }
    box.append(el('div', { class: 'chips' }, items.map((v, i) =>
        el('span', { class: 'chip' }, decorate ? decorate(v) : v,
            el('button', {
                class: 'chip__x', title: '削除',
                onclick: () => { onRemove(i); render(); },
            }, '×')))));
}

/* サーバ側の is_vision と同じ判定。保存前に結果を見せるため。 */
const isVision = (name) =>
    (state.vision || []).some(k => String(name).toLowerCase().includes(k));

/* そのモデルを選んでいる利用者の数。候補から外す前に見せる。 */
const usersOf = (name) => ((state.in_use || {})[name] || []).length;

function render() {
    const models = state.models || [];

    chips($('#modelList'), models, i => {
        const removed = models[i];
        const n = usersOf(removed);
        if (n && !confirm(`${removed} は ${n} 人が選んでいます。`
            + '候補から外すと、その人たちは既定のモデルに戻ります。よろしいですか？')) return;
        models.splice(i, 1);
        if (state.default === removed) state.default = models[0] || '';
    }, '候補がありません。「一覧から選ぶ」で使わせたいモデルを選んでください。',
        v => `${v}${isVision(v) ? '　': '' }${usersOf(v) ? `（利用者${usersOf(v)}人）` : ''}`);

    // 既定は候補の中からしか選べない
    const sel = $('#defaultModel');
    sel.replaceChildren(...(models.length
        ? models.map(v => el('option',
            { value: v, ...(v === state.default ? { selected: 'selected' } : {}) }, v))
        : [el('option', { value: '' }, '（候補を追加してください）')]));

    chips($('#visionList'), state.vision || [],
        i => state.vision.splice(i, 1),
        '未設定です。画像はどのモデルでも送れない扱いになります。');

    // 判定結果をその場で見せる（保存してから気づくのを防ぐ）
    $('#visionPreview').replaceChildren(models.length
        ? el('div', { class: 'small muted' },
            'いまの判定: '+ models.map(m => `${m} ${isVision(m) ? '画像OK': '画像なし' }`).join('／ '))
        : '');

    const cat = state.catalog || [];
    $('#catalogList').replaceChildren(...cat.map(v => el('option', { value: v })));
    $('#catalogHint').textContent = cat.length
        ? `APIが返したモデルは ${cat.length} 件です。`
          + 'この中から「一覧から選ぶ」で選ぶか、一覧に無い名前は直接入力してください。'
        : 'APIから一覧を取得できていません。モデル名を直接入力してください。';

    renderBudget();

    const box = $('#banner');
    box.replaceChildren();
    if (!state.llm_ready) {
        box.append(el('div', { class: 'alert alert--warn' },
            'LLMが未設定です。env の OPENAI_* を設定するまで、'
            + 'モデル一覧の取得とチャットは動きません。'));
    }
    // いまチャットに何が出ているかを、実態のまま出す。
    // ここがずれていると「設定が効いていない」ように見える。
    const eff = state.effective || [];
    if (state.source === 'admin') {
        box.append(el('div', { class: 'alert alert--info' },
            `この画面の設定が効いています。チャットのプルダウンには `
            + `${eff.length} 件（${eff.join('、')}）が出ます。`));
    } else if (state.source === 'env') {
        box.append(el('div', { class: 'alert alert--info' },
            'いまは env の OPENAI_MODELS をそのまま使っています'
            + `（${eff.join('、')}）。ここで保存すると、以後はこの画面の内容が優先されます。`));
    } else {
        box.append(el('div', { class: 'alert alert--warn' },
            '候補をまだ決めていません。いまチャットに出るのは、既定のモデルと'
            + `すでに誰かが選んでいるモデルだけです（${eff.join('、') || '（未設定）'}）。`
            + '「一覧から選ぶ」で使わせたいモデルを決めてください。'));
    }
}

/* --- 一覧から選ぶ（チェックボックス） ---------------------------------------------
   126件を1件ずつ手入力させるのは現実的ではないので、取得した一覧から選ばせる。 */

function openPicker() {
    const cat = state.catalog || [];
    if (!cat.length) {
        toast('APIから一覧を取得できていません。「一覧を取得」を試すか、名前を直接入力してください。', 'warn');
        return;
    }
    const picked = new Set(state.models || []);
    const back = el('div', { class: 'modal' });
    const close = () => back.remove();
    back.addEventListener('click', ev => { if (ev.target === back) close(); });

    const body = el('div', { class: 'modal__body' });
    const count = el('b', {}, '');
    const sync = () => { count.textContent = `${picked.size} 件を選択中`; };
    const rows = cat.map(name => {
        const cb = el('input', { type: 'checkbox', ...(picked.has(name) ? { checked: 'checked' } : {}) });
        cb.addEventListener('change', () => {
            if (cb.checked) picked.add(name); else picked.delete(name);
            sync();
        });
        return el('label', { class: 'fsrow', 'data-key': name },
            cb,
            el('span', { class: 'name' }, name),
            isVision(name) ? el('span', { class: 'small muted' }, '画像OK') : null,
            usersOf(name) ? el('span', { class: 'small muted' }, `利用者${usersOf(name)}人`) : null);
    });
    body.append(...rows);
    sync();

    const filter = el('input', {
        type: 'text', style: 'width:100%', placeholder: 'モデル名で絞り込み（例: gpt-4o）',
        oninput: ev => {
            const q = ev.target.value.trim().toLowerCase();
            rows.forEach(r => r.classList.toggle('hidden',
                !!q && !r.dataset.key.toLowerCase().includes(q)));
        },
    });

    back.append(el('div', { class: 'modal__box' },
        el('div', { class: 'modal__head' },
            el('b', { class: 'grow' }, '使わせるモデルを選ぶ'),
            el('button', { class: 'btn btn--sm btn--ghost', onclick: close }, icon('x', 'icon--sm'))),
        el('div', { style: 'padding:10px 14px 0' }, filter,
            el('div', { class: 'small muted mt' },
                `APIが返した ${cat.length} 件です。チェックしたものだけがチャットに出ます。`)),
        body,
        el('div', { class: 'modal__foot row', style: 'align-items:center' },
            el('span', { class: 'small muted grow' }, count),
            el('button', { class: 'btn btn--sm', onclick: close }, 'やめる'),
            el('button', {
                class: 'btn btn--sm btn--primary',
                onclick: () => {
                    // 一覧に無いのに手入力で足した名前は消さずに残す
                    const kept = (state.models || []).filter(m => !cat.includes(m));
                    state.models = [...kept, ...cat.filter(m => picked.has(m))];
                    if (!state.models.includes(state.default)) state.default = state.models[0] || '';
                    close(); render();
                    toast('選びました。下の「設定を保存」で確定します。', 'warn');
                },
            }, 'この内容にする'))));
    document.body.append(back);
    filter.focus();
}

/* --- カタログの量と、モデルの文脈に対する余裕 ------------------------------------
   数字だけ出しても判断できないので、「いまどれだけ使っていて、上限まで育てたら
   どうなるか」を並べて見せる。トークン数は実測から出した概算（llm.py 参照）。 */

const fmt = (n) => Number(n || 0).toLocaleString();


function renderBudget() {
    const total = state.catalog_chars || 0;
    const rows = state.contexts || [];
    const label = { override: '登録した値', table: '公式の表', default: '推定' };
    const box = $('#ctxTable');
    if (!rows.length) {
        box.replaceChildren(el('div', { class: 'small muted' }, '候補のモデルを選ぶと、ここに出ます。'));
        return;
    }
    box.replaceChildren(
        el('div', { class: 'small muted mb' },
            `いまのカタログ全体: ${fmt(total)} 字。この量が「カタログの上限」以下のモデルなら、`
            + '質問ごとの絞り込みなしで全データがそのまま渡ります。'),
        dataTable(['モデル', '一度に読める量', '出所', 'カタログの上限', 'いまのカタログ'],
            rows.map(m => [
                m.id,
                `${fmt(m.context)} tok`,
                label[m.source] || m.source,
                `${fmt(m.limit_chars)} 字`,
                m.fits ? '収まる（全部渡す）' : '超える（自動で絞る）',
            ])),
        ...(rows.some(m => m.source === 'default')
            ? [el('div', { class: 'alert alert--warn small mt' },
                '「推定」のモデルは表に無いため、既定値（'
                + fmt(state.env_context_default || 128000) + ' tok）を仮に使っています。'
                + '実際より大きい値だとカタログが溢れてエラーになるので、下の欄で登録してください。')]
            : []));

    // 登録済みの一覧（外せるように）
    const ov = state.context_overrides || {};
    const keys = Object.keys(ov);
    if (keys.length) {
        box.append(el('div', { class: 'small mt' }, el('b', {}, '登録済み: '),
            ...keys.map(k => el('span', { class: 'chip', style: 'margin-right:6px' },
                `${k} = ${fmt(ov[k])} tok`,
                el('button', { class: 'chip__x', title: '外す', onclick: () => {
                    delete state.context_overrides[k]; render();
                } }, '×')))));
    }
}

function addTo(key, input, normalize) {
    const v = (input.value || '').trim();
    if (!v) return;
    const value = normalize ? normalize(v) : v;
    state[key] = state[key] || [];
    if (state[key].some(x => x.toLowerCase() === value.toLowerCase())) {
        toast('すでに登録されています。', 'warn');
        return;
    }
    state[key].push(value);
    input.value = '';
    if (key === 'models'&& !state.default) state.default = value;
    render();
}

async function load(refresh) {
    state = await api(`/api/models/admin${refresh ? '?refresh=1': '' }`, undefined, 'GET');
    render();
    renderApiKey();
}

function renderApiKey() {
    const box = $('#apiKeyState');
    if (!box) return;
    const src = state.api_key_source;
    box.replaceChildren(
        src === 'screen'
            ? el('div', { class: 'alert alert--ok' }, 'この画面で保存したキーを使用中です。')
            : src === 'env'
                ? el('div', { class: 'alert alert--info' }, 'env ファイルのキーを使用中です。')
                : el('div', { class: 'alert alert--warn' },
                     'APIキーが未設定です。AIを呼び出せません。'));
    // 接続先URL（値も出所も表示する。入力中は上書きしない）
    [['#chatUrl', '#chatUrlNote', state.chat_url, state.chat_url_source, state.env_chat_url],
     ['#modelsUrl', '#modelsUrlNote', state.models_url, state.models_url_source, state.env_models_url]]
        .forEach(([inp, note, val, source, envval]) => {
            if (document.activeElement !== $(inp)) $(inp).value = val || '';
            $(note).textContent = source === 'screen'
                ? `この画面で保存したURLを使用中（envの値: ${envval || '未設定'}）`
                : (val ? 'env の値を使用中です。' : 'env が未設定です。URLを入力してください。');
        });
}

document.addEventListener('DOMContentLoaded', () => {
    state = window.MODELS || {};
    render();
    renderApiKey();

    $('#pickModel').addEventListener('click', openPicker);
    $('#addModel').addEventListener('click', () => addTo('models', $('#newModel')));
    $('#addVision').addEventListener('click',
        () => addTo('vision', $('#newVision'), v => v.toLowerCase()));
    [['#newModel', '#addModel'], ['#newVision', '#addVision']].forEach(([i, b]) =>
        $(i).addEventListener('keydown', ev => { if (ev.key === 'Enter') $(b).click(); }));

    $('#defaultModel').addEventListener('change', ev => { state.default = ev.target.value; });
    // 表に無いモデルの文脈量を登録する（保存で確定）
    $('#ctxAdd').addEventListener('click', () => {
        const name = ($('#ctxName').value || '').trim().toLowerCase();
        const n = parseInt(($('#ctxTokens').value || '').replace(/[,_]/g, ''), 10);
        if (!name) return toast('モデル名を入れてください。', 'warn');
        if (!n || n < 1000) return toast('文脈量はトークン数（1,000以上）で入れてください。', 'warn');
        state.context_overrides = { ...(state.context_overrides || {}), [name]: n };
        $('#ctxName').value = ''; $('#ctxTokens').value = '';
        render();
        toast('登録しました。「設定を保存」で確定します。', 'warn');
    });
    $('#ctxTokens').addEventListener('keydown', ev => { if (ev.key === 'Enter') $('#ctxAdd').click(); });

    $('#refresh').addEventListener('click', async ev => {
        ev.target.disabled = true;
        try { await load(true); toast('一覧を取り直しました。', 'ok'); }
        catch (e) { toast(e.message, 'err', 9000); }
        ev.target.disabled = false;
    });

    $('#apiKeyClear').addEventListener('click', async ev => {
        if (state.api_key_source !== 'screen') {
            toast('画面で保存したキーはありません（envのキーを使用中）。', 'warn');
            return;
        }
        if (!confirm('画面で保存したAPIキーを消して、envのキーに戻します。よろしいですか？')) return;
        ev.target.disabled = true;
        try {
            const r = await api('/api/models/admin', {
                models: state.models || [],
                default: state.default,
                vision: state.vision || [],
                context_overrides: state.context_overrides || {},
                api_key_clear: true,
            });  // URLは送らない＝変更しない
            state = { ...state, ...r };
            toast('envのキーに戻しました。', 'ok');
            render();
            renderApiKey();
        } catch (e) { toast(e.message, 'err', 9000); }
        ev.target.disabled = false;
    });

    $('#save').addEventListener('click', async ev => {
        ev.target.disabled = true;
        try {
            const key = ($('#apiKeyInput').value || '').trim();
            const r = await api('/api/models/admin', {
                models: state.models || [],
                default: state.default,
                vision: state.vision || [],
                context_overrides: state.context_overrides || {},
                chat_url: $('#chatUrl').value,
                models_url: $('#modelsUrl').value,
                ...(key ? { api_key: key } : {}),
            });
            state = { ...state, ...r };
            $('#apiKeyInput').value = '';
            toast(key ? '保存しました（APIキーも更新）。' : '保存しました。', 'ok');
            render();
            renderApiKey();
        } catch (e) { toast(e.message, 'err', 9000); }
        ev.target.disabled = false;
    });

    $('#reload').addEventListener('click', () => load(false));
});
})();

// ===== 元 table.js（window.TABLE_INIT がある画面だけ動く） =====
(() => {
if (!window.TABLE_INIT) return;
/* テーブル全体を見る画面。

   サンプル行の「テーブル全体を閲覧」から別タブで開く読み取り専用のビューア。
   行はサーバ側で1ページずつ切って返るので、何百万行あっても画面は重くならない。
   絞り込み・並べ替えもサーバ側（表示中のページだけを並べても意味がないため）。 */

const T = window.TABLE_INIT || {};
let state = {
    offset: 0, limit: 100, q: '', sort: '', dir: 'asc',
    total: 0, matched: 0,
    filters: {},          // { 列名: {values:[...]} | {op:'>=', value:'100'} }
};
let timer = null;

function filterParam() {
    return Object.keys(state.filters).length ? JSON.stringify(state.filters) : '';
}

async function load() {
    const box = $('#tableBox');
    box.replaceChildren(el('div', { class: 'small muted', style: 'padding:10px' },
        el('span', { class: 'spinner' }), ' 読み込み中…'));
    const p = new URLSearchParams({
        db: T.db, table: T.table, offset: state.offset, limit: state.limit,
        q: state.q, sort: state.sort, dir: state.dir, filters: filterParam(),
    });
    let r;
    try {
        r = await api('/api/table/rows?' + p.toString(), undefined, 'GET');
    } catch (e) {
        box.replaceChildren(el('div', { class: 'alert alert--err' }, e.message));
        return;
    }
    Object.assign(state, {
        total: r.total, matched: r.matched, offset: r.offset,
        limit: r.limit, sort: r.sort, dir: r.dir,
    });
    render(r);
}

/* 列の見出し。名前を押すと並べ替え、漏斗を押すとフィルター（Excelと同じ感覚）。 */
function headCell(col) {
    const on = !!state.filters[col];
    return el('th', {},
        el('div', { class: 'th__inner' },
            el('span', {
                class: 'th__name', title: `${col} で並べ替え`,
                onclick: () => {
                    if (state.sort === col) state.dir = state.dir === 'asc' ? 'desc' : 'asc';
                    else { state.sort = col; state.dir = 'asc'; }
                    state.offset = 0; load();
                },
            }, col, state.sort === col ? (state.dir === 'asc' ? ' ↑' : ' ↓') : ''),
            el('button', {
                class: 'th__filter' + (on ? ' is-on' : ''),
                title: on ? `${col} で絞り込み中（クリックで変更）` : `${col} で絞り込む`,
                onclick: ev => { ev.stopPropagation(); openFilter(col, ev.currentTarget); },
            }, icon('filter', 'icon--sm'))));
}

function render(r) {
    const head = el('thead', {}, el('tr', {},
        el('th', { style: 'text-align:right;width:1%' }, '#'),
        r.columns.map(headCell)));

    const body = el('tbody', {}, r.rows.map((row, i) => el('tr', {},
        el('td', { class: 'num muted' }, (r.offset + i + 1).toLocaleString()),
        row.map(v => {
            const info = cellInfo(v);
            const empty = v === null || v === undefined;
            // 値が NULL なのか空文字なのかは、集計の食い違いの原因になるので区別して出す
            return el('td', { class: empty ? 'muted' : (info.num ? 'num' : null), title: info.text },
                empty ? 'NULL' : info.text);
        }))));

    $('#tableBox').replaceChildren(el('table', { class: 'data' }, head, body));
    renderChips();

    const shown = r.rows.length;
    const range = shown
        ? `${(r.offset + 1).toLocaleString()}〜${(r.offset + shown).toLocaleString()}行目を表示`
        : '該当なし';
    const filtered = state.q || Object.keys(state.filters).length;
    $('#countLabel').textContent = filtered
        ? `全 ${state.total.toLocaleString()}行 中 ${state.matched.toLocaleString()}行が一致（${range}）`
        : `全 ${state.total.toLocaleString()}行 ・ ${r.columns.length}列（${range}）`;

    const end = Math.max(1, Math.ceil((state.matched || 0) / state.limit));
    const page = Math.floor(state.offset / state.limit) + 1;
    $('#pageLabel').textContent = `${page} / ${end} ページ`;
    $('#prev').disabled = $('#first').disabled = state.offset <= 0;
    $('#next').disabled = $('#last').disabled = state.offset + state.limit >= state.matched;
}

/* いま効いている絞り込みを見出しの下に並べる。1つずつ外せる。 */
function renderChips() {
    const box = $('#chips');
    const names = Object.keys(state.filters);
    box.replaceChildren();
    if (!names.length) { box.classList.add('hidden'); return; }
    box.classList.remove('hidden');
    box.append(...names.map(col => el('span', { class: 'chip' },
        el('b', {}, col), '：', describeFilter(state.filters[col]),
        el('button', {
            class: 'chip__x', title: 'この絞り込みを外す',
            onclick: () => { delete state.filters[col]; state.offset = 0; load(); },
        }, '×'))),
        el('button', {
            class: 'btn btn--sm btn--ghost',
            onclick: () => { state.filters = {}; state.offset = 0; load(); },
        }, 'すべて解除'));
}

function describeFilter(f) {
    if (f.values) {
        const v = f.values.map(x => (x === null ? 'NULL' : x));
        return v.length <= 3 ? v.join('、') : `${v.slice(0, 3).join('、')} ほか${v.length - 3}件`;
    }
    const label = { contains: 'を含む', not_contains: 'を含まない',
                    empty: '空(NULL)', not_empty: '空でない' }[f.op];
    if (f.op === 'empty' || f.op === 'not_empty') return label;
    if (label) return `「${f.value}」${label}`;
    return `${f.op} ${f.value}`;
}

/* --- 列ごとの絞り込み（Excelのフィルター） --------------------------------------
   値の一覧はサーバから取る（テーブル全体を見た一覧。表示中のページではない）。
   種類が多い列は上から300件までなので、探す欄で絞ってから選ぶ。 */

function openFilter(col, anchor) {
    $('.colfilter')?.remove();
    const cur = state.filters[col] || {};
    const box = el('div', { class: 'colfilter' });
    box.addEventListener('click', ev => ev.stopPropagation());

    // ① 条件（含む・比較など）
    const op = el('select', {},
        ['（選んだ値だけ）', '含む', '含まない', '=', '!=', '>', '>=', '<', '<=', '空(NULL)', '空でない']
            .map(t => el('option', {}, t)));
    const OPS = { '含む': 'contains', '含まない': 'not_contains', '=': '=', '!=': '!=',
                  '>': '>', '>=': '>=', '<': '<', '<=': '<=',
                  '空(NULL)': 'empty', '空でない': 'not_empty' };
    const NAMES = Object.fromEntries(Object.entries(OPS).map(([k, v]) => [v, k]));
    if (cur.op) op.value = NAMES[cur.op] || '（選んだ値だけ）';
    const opValue = el('input', { type: 'text', placeholder: '値', value: cur.value ?? '' });

    // ② 値の一覧（チェックボックス）
    const search = el('input', { type: 'text', placeholder: '値を探す' });
    const list = el('div', { class: 'colfilter__list' },
        el('div', { class: 'small muted' }, el('span', { class: 'spinner' }), ' 読み込み中…'));
    const picked = new Set((cur.values || []).map(v => JSON.stringify(v)));

    const syncMode = () => {
        const byValues = op.value === '（選んだ値だけ）';
        opValue.style.display = byValues || ['空(NULL)', '空でない'].includes(op.value) ? 'none' : '';
        search.style.display = list.style.display = byValues ? '' : 'none';
    };
    op.addEventListener('change', syncMode);
    syncMode();

    let vtimer = null;
    async function loadValues() {
        const p = new URLSearchParams({ db: T.db, table: T.table, column: col, q: search.value.trim() });
        let r;
        try { r = await api('/api/table/values?' + p.toString(), undefined, 'GET'); }
        catch (e) { list.replaceChildren(el('div', { class: 'alert alert--err small' }, e.message)); return; }
        const rows = r.values.map(v => {
            const key = JSON.stringify(v.value);
            const cb = el('input', { type: 'checkbox', ...(picked.has(key) ? { checked: 'checked' } : {}) });
            cb.addEventListener('change', () => (cb.checked ? picked.add(key) : picked.delete(key)));
            return el('label', { class: 'colfilter__row' }, cb,
                el('span', { class: 'grow' }, v.value === null || v.value === undefined ? 'NULL'
                    : (String(v.value) === '' ? '（空文字）' : String(v.value))),
                el('span', { class: 'muted small' }, v.count.toLocaleString()));
        });
        list.replaceChildren(
            el('div', { class: 'small muted mb' },
                `${r.kinds.toLocaleString()}種類` + (r.truncated ? '（多い順に300件まで表示。探す欄で絞れます）' : '')),
            ...(rows.length ? rows : [el('div', { class: 'small muted' }, '該当する値がありません。')]));
    }
    search.addEventListener('input', () => { clearTimeout(vtimer); vtimer = setTimeout(loadValues, 250); });

    const apply = () => {
        if (op.value === '（選んだ値だけ）') {
            const vals = [...picked].map(k => JSON.parse(k));
            if (vals.length) state.filters[col] = { values: vals };
            else delete state.filters[col];
        } else if (['空(NULL)', '空でない'].includes(op.value)) {
            state.filters[col] = { op: OPS[op.value] };
        } else if (opValue.value.trim() !== '') {
            state.filters[col] = { op: OPS[op.value], value: opValue.value.trim() };
        } else {
            delete state.filters[col];
        }
        box.remove(); state.offset = 0; load();
    };

    box.append(
        el('div', { class: 'colfilter__head' }, el('b', { class: 'grow' }, col),
            el('button', { class: 'btn btn--sm btn--ghost', onclick: () => box.remove() }, '×')),
        el('div', { class: 'row', style: 'gap:6px' }, op, opValue),
        search, list,
        el('div', { class: 'row mt', style: 'gap:6px' },
            el('button', {
                class: 'btn btn--sm', onclick: () => {
                    delete state.filters[col]; box.remove(); state.offset = 0; load();
                },
            }, '解除'),
            el('div', { class: 'spacer' }),
            el('button', { class: 'btn btn--sm btn--primary', onclick: apply }, '適用')));

    document.body.append(box);
    // 見出しの真下に出す。画面の右端からはみ出すときは左へずらす
    const r = anchor.getBoundingClientRect();
    box.style.top = `${Math.round(r.bottom + 4)}px`;
    box.style.left = `${Math.round(Math.min(r.left, window.innerWidth - box.offsetWidth - 12))}px`;
    loadValues();
    setTimeout(() => document.addEventListener('click', function once() {
        box.remove(); document.removeEventListener('click', once);
    }), 0);
}

function move(delta) {
    state.offset = Math.max(0, state.offset + delta * state.limit);
    load();
}

document.addEventListener('DOMContentLoaded', () => {
    if (T.error) return;                       // テーブルが無いときは表示だけ
    $('#q').addEventListener('input', ev => {
        // 1文字ごとに投げない（打ち終わりを待つ）
        clearTimeout(timer);
        timer = setTimeout(() => { state.q = ev.target.value.trim(); state.offset = 0; load(); }, 300);
    });
    $('#size').addEventListener('change', ev => {
        state.limit = Number(ev.target.value); state.offset = 0; load();
    });
    $('#first').addEventListener('click', () => { state.offset = 0; load(); });
    $('#prev').addEventListener('click', () => move(-1));
    $('#next').addEventListener('click', () => move(1));
    $('#last').addEventListener('click', () => {
        state.offset = Math.max(0, (Math.ceil(state.matched / state.limit) - 1) * state.limit);
        load();
    });
    load();
});
})();
""",

}
