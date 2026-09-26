"""assets.py — 画面の素材（HTML・CSS・JS）。

このファイルにあるのは、次の2つの辞書と、ヘルプを読み込む数行だけ:

  TEMPLATES     … Jinja2 のテンプレート。core.py の create_app が
                   DictLoader(TEMPLATES) で読む。
  STATIC_FILES  … css/app.css と js/app.js。core.py の /static/<path> が
                   ETag を付けて配る。

core.py から分けてあるのは、ここが大きく、
ヘルプの文言を1行直すだけでコード本体の差分になってしまうため。
分けても配り方は変わらない（core.py が import して使う）。

**ヘルプ（help.html）だけは、同じ場所の templates/help.html にある。**
48万字あって、このファイルの半分を占めていた。中身は文書なので、
コードとは別の速度で変わる。読み込みは下の方の1か所だけで、
TEMPLATES に入れたあとは他と区別が無い。

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

from pathlib import Path

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
  <symbol id="i-help" viewBox="0 0 24 24">
      <circle cx="12" cy="12" r="9"/><path d="M9.6 9.2a2.4 2.4 0 1 1 3.3 2.3c-.7.3-.9.8-.9 1.6M12 16.6h.01"/>
    </symbol>
  <symbol id="i-table" viewBox="0 0 24 24">
      <rect x="3.5" y="4.5" width="17" height="15" rx="2"/>
      <path d="M3.5 9.5h17M9.5 9.5v10"/>
    </symbol>
  {# ビュー（保存したSELECT）。実体の無い「写し」なので、重なった2枚の紙 #}
  <symbol id="i-view" viewBox="0 0 24 24">
      <rect x="7.5" y="3.5" width="13" height="14" rx="2"/>
      <path d="M3.5 7.5v11a2 2 0 0 0 2 2h11M11 8.5h6M11 12.5h6"/>
    </symbol>
    <symbol id="i-tool" viewBox="0 0 24 24">
      <path d="M14.5 6.5a4 4 0 0 1 5.2 5.2l-8 8a2.5 2.5 0 0 1-3.6-3.6l8-8"/>
      <path d="m9 9-5.2 5.2a3 3 0 0 0 4.2 4.2"/>
    </symbol>
  </defs>
</svg>
""",

# --- _admintabs.html ---
"_admintabs.html": r"""{# 管理者メニューのタブの帯。どの画面でも同じ並びを出し、いま開いている画面に印を付ける。
   データカタログの中のタブ（テーブル…ビュー）は、カタログ画面ではその場で切り替えるボタン、
   ほかの画面ではカタログ画面へ渡すリンク。取り込み以降は画面そのものが別なので常にリンク。
   使い方: {% from "_admintabs.html" import admintabs %} … <div class="tabs tabs--bar">{{ admintabs('import') }}</div> #}
{% macro admintabs(active) -%}
{% for key, label in [('tables', 'テーブル'), ('er', '結合・ER図'), ('glossary', '用語集・例文'), ('tools', 'ツール'), ('views', 'ビュー')] -%}
{% if active == 'catalog' %}<button class="tab {{ 'is-active' if loop.first }}" data-pane="{{ key }}">{{ label }}</button>
{% else %}<a class="tab" href="{{ url_for('catalog.index') }}#tab={{ key }}">{{ label }}</a>
{% endif %}{% endfor -%}
{% for key, ep, label in [('import', 'imp.index', '取り込み'), ('output', 'imp.output', '出力'), ('sep', '', ''),
                          ('knowledge', 'knowledge.index', 'ナレッジベース'), ('models', 'models.index', 'モデル設定'),
                          ('mail', 'mail.index', 'メール設定'), ('robots', 'catalog.robot_settings', 'マイロボット'),
                          ('memory', 'catalog.memory_admin', 'パーソナライズ'),
                          ('display', 'catalog.display_admin', '画面'),
                          ('usage', 'usage.index', '利用状況'), ('help', 'help.index', 'ヘルプ')] -%}
{% if key == 'sep' %}<span class="tabs__sep" aria-hidden="true"></span>
{% elif key == active %}<button class="tab is-active">{{ label }}</button>
{% else %}<a class="tab" href="{{ url_for(ep) }}">{{ label }}</a>
{% endif %}{% endfor -%}
{%- endmacro %}
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
    {# 管理者以外はマイエージェントしか使えないので、行き先が1つだけのメニューは出さない。
       URLを直に叩かれても admin_required で止まるので、ここは見た目の整理。 #}
    {# 各画面が何をする所かは data-desc に持たせ、マウスを乗せたときに出す。
       画面の上に固定で置くと、毎回読むものでもないのに場所だけ取り続けるため。
       吹き出しは body 直下に描かれるので、サイドバーの幅で切れない。 #}
    {% if user.is_admin %}
    <div class="sidebar__section">
      <a class="navlink {{ 'is-active' if nav.startswith('chat.') }}" href="{{ url_for('chat.index') }}"
         data-desc="データについて日本語で質問すると、AIがSQLを書いて答えます。">
        {{ icon('chat') }} マイエージェント</a>
      <a class="navlink {{ 'is-active' if nav.startswith('robots.') }}" href="{{ url_for('robots.index') }}"
         data-desc="保存した処理の流れ。押すと同じ手順をAIなしでそのまま実行します。作るのはマイエージェントの発言の「ロボットにする」から。">
        {{ icon('spark') }} マイロボット</a>
      {% if memory_feature %}
      <a class="navlink {{ 'is-active' if nav == 'chat.memory' }}" href="{{ url_for('chat.memory') }}"
         data-desc="AIがあなたについて覚えていること（前提・好み・期間）。会話から自動で書き足され、ここで直せます。本人だけのものです。">
        {{ icon('user') }} パーソナライズ</a>
      {% endif %}
      {# 管理者の画面は1本にまとめ、中はタブで切り替える（_admintabs.html）。
         データカタログ・取り込み・出力・ナレッジベース・モデル設定・メール設定・マイロボット・パーソナライズ・画面・利用状況・ヘルプ #}
      <a class="navlink {{ 'is-active' if nav.startswith(('catalog.', 'imp.', 'knowledge.', 'models.', 'mail.', 'usage.', 'help.')) }}" href="{{ url_for('catalog.index') }}"
         data-desc="管理者だけの画面。データカタログ（テーブル・結合・ER図・用語集・例文・ツール・ビュー）、取り込み、出力、ナレッジベース、モデル設定、メール設定、マイロボットの決めごと、パーソナライズ、画面、利用状況、ヘルプを、上のタブで切り替えます。カタログに書いた内容がそのまま AI の理解になります。">
        {{ icon('catalog') }} 管理者メニュー</a>
    </div>
    {% endif %}
    {# 一般利用者のメニュー。管理者の分は上の囲いにある（同じものを2回出さない）。
       ヘルプは管理者メニューのタブに移したので、ここには置かない #}
    {% if not user.is_admin %}
    <div class="sidebar__section">
      <a class="navlink {{ 'is-active' if nav.startswith('chat.') }}" href="{{ url_for('chat.index') }}"
         data-desc="データについて日本語で質問すると、AIがSQLを書いて答えます。">
        {{ icon('chat') }} マイエージェント</a>
      <a class="navlink {{ 'is-active' if nav.startswith('robots.') }}" href="{{ url_for('robots.index') }}"
         data-desc="保存した処理の流れ。押すと同じ手順をAIなしでそのまま実行します。作るのはマイエージェントの発言の「ロボットにする」から。">
        {{ icon('spark') }} マイロボット</a>
      {% if memory_feature %}
      <a class="navlink {{ 'is-active' if nav == 'chat.memory' }}" href="{{ url_for('chat.memory') }}"
         data-desc="AIがあなたについて覚えていること（前提・好み・期間）。会話から自動で書き足され、ここで直せます。本人だけのものです。">
        {{ icon('user') }} パーソナライズ</a>
      {% endif %}
    </div>
    {% endif %}

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
{% from "_admintabs.html" import admintabs %}
{% block title %}管理者メニュー — {{ app_title }}{% endblock %}
{# 見出しは置かない。画面の説明はサイドバーの項目にマウスを乗せると出る #}


{% block body %}
<div class="content content--wide">
{% if not target %}
  {# DBが無くても、モデル設定・取り込みなどほかのタブへは行けるようにする #}
  <div class="tabs tabs--bar">{{ admintabs('') }}</div>
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
    {{ admintabs('catalog') }}

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
        {# 種類のアイコン（格子＝表、重なった紙＝ビュー）。マイエージェントのサイドバー・ER図と同じ #}
        <span class="dbpick__kind" title="{{ 'ビュー（保存したSELECT）' if t.is_view else 'テーブル' }}">{{ icon('view' if t.is_view else 'table', 'icon--sm') }}</span>
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
        <button class="btn btn--sm" id="erArrange"
                title="表示中の表を関連にそって並べ直します（参照される側の表を右に、つながりのない表は下にまとめて）。&#10;この配置で残すには保存を押してください。Ctrl+Z で戻せます">整列</button>
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
                title="「結合を探す」で作った結合の候補（と、過去のSQLで使われたのに未登録の結合）を赤い線で重ねます。まだ探していなければ空です。&#10;線をクリックすると内容を確かめて登録できます。&#10;画面に出ている表どうしの候補だけが描かれます">結合候補</button>
        <button class="btn btn--sm" id="erDiscover"
                title="全表の全列を実データで調べて、結合の候補と多重度の推定を保存します。&#10;表が大きいと数分かかります。表の定義が変わらなければ探し直す必要はありません">結合を探す</button>
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
        線の両端の <b>0..1</b>・<b>1</b>・<b>0..*</b>・<b>1..*</b>＝多重度（0..＝相手の無い行あり）　実線＝登録済み／短い破線＝FOREIGN KEY
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
          SQLを実行するたびに自動で突き合わせ、食い違っていたらマイエージェントに警告を出します
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
          マイエージェントで回答が正しかったときの「この質問とSQLを例文として保存」からも増えます。
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
        登録するとテーブルと同じ扱いになり、テーブル一覧・ER図・マイエージェントの表選択に出ます
        （名前の前のアイコンで見分けられます: 格子＝表、重なった紙＝ビュー。マウスを乗せると「ビュー」と出ます）。
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
        <div id="viewUsed"></div>
        <div class="row mt mb" style="align-items:center;gap:10px;flex-wrap:wrap">
          <button class="btn btn--sm" id="viewExport"
                  title="このSQLを実データで動かし、結果を全件 Excel にしてダウンロードします（下に先頭の行も出ます）">結果をExcelでダウンロード</button>
          <button class="btn btn--sm" id="viewExplainBtn"
                  title="いま書いてあるSQLの解説（このSQLがしていること）と、使ったデータ（読む表と列）を出します。自分で書いたSQLや、直したあとに">AIに解説を書かせる</button>
          <span class="small muted">保存前でも、いま書いてあるSQLで動かします</span>
        </div>
        <div id="viewPreview"></div>

        <label class="field mt">3. まとまり・名前・説明</label>
        <div class="row mb" style="flex-wrap:wrap;align-items:center;gap:6px">
          <select id="viewGroup" style="max-width:240px" title="まとまり（表と同じ接頭辞）"></select>
          <input type="text" id="viewGroupNew" class="mono hidden" style="max-width:200px" placeholder="新しいまとまり名">
          <span class="mono muted">__</span>
          <input type="text" id="viewNameBody" class="mono" style="max-width:240px" placeholder="名前（例: 発注一覧）">
          <input type="text" id="viewDesc" class="grow"
                 placeholder="この一覧が何かの説明（AIが読みます）">
        </div>
        <div class="small muted mb" id="viewNameHint">
          まとまりは既存から選ぶか「＋ 新しいまとまりを作る」で作ります（取り込みと同じ）。保存する名前は「まとまり__名前」です。
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
  examplesMax: {{ examples_max|tojson }},
  er: {{ er|tojson }},
  suggestions: {{ suggestions|tojson }},
  joinStatus: {{ join_status|tojson }},
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
  chartFields: {{ chart_fields|tojson }}
};
window.MANAGE = { intervals: {{ intervals|tojson }}, refresh: () => loadManage(true) };
</script>
{% endif %}
{% endblock %}
""",

# --- chat.html ---
"chat.html": r"""{% extends "base.html" %}
{% from "_icons.html" import icon %}
{% block title %}マイエージェント — {{ app_title }}{% endblock %}
{# この画面だけ画面固定（ログの中をスクロールさせる）。CSSの .is-chat 参照 #}
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
    {# prefix はまとまり名。見出しに出ているので、表の行では「まとまり__」を省いて名前だけ見せる
       （データ属性と説明の見出しは正式名のまま。AIやSQLで使うのは正式名） #}
    {% macro table_row(t, prefix='') %}
      {% set short = t.name[(prefix|length) + 2:] if prefix and t.name.startswith(prefix ~ '__') else t.name %}
      <div class="dbpick__table">
        <input type="checkbox" class="tblpick" data-table="{{ t.name }}"
               {{ 'checked' if t.on }} title="AIが使う対象にする">
        {# 表とビューの見分け: 格子＝表、重なった紙＝ビュー（保存したSELECT） #}
        <span class="dbpick__kind" title="{{ 'ビュー（保存したSELECT。実体は無く、開くたびに計算します）' if t.type == 'view' else 'テーブル' }}">{{ icon('view' if t.type == 'view' else 'table', 'icon--sm') }}</span>
        <a href="{{ url_for('tableview.index') }}?db={{ data.db|urlencode }}&table={{ t.name|urlencode }}"
           target="_blank" rel="noopener" class="dbpick__tname"
           data-desc-title="{{ t.name }}{% if t.type == 'view' %}（ビュー）{% endif %}" data-desc="{% if t.type == 'view' %}ビュー: 保存したSELECT。実体は無く、開くたびに元の表から計算します。
{% endif %}{{ t.description }}{% if t.problem %}
⚠ 定期取り込み: {{ t.problem }}{% endif %}
（クリックで中身を別タブで開きます）"
           data-desc-meta="{{ '{:,}行'.format(t.rows) if t.rows is not none else '行数不明' }} / {{ t.columns }}列">{{ short }}</a>
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
          {% for t in g.tables %}{{ table_row(t, g.key) }}{% endfor %}
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
    <span class="sidebar__label">会話の履歴</span>
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
  folderOut: {{ folder_out|default(false)|tojson }},
  knowledge: {{ knowledge|tojson }},
  memory: {{ memory|tojson }},
  robotSchedVocab: {{ robot_sched_vocab|tojson }},
  robotMinIntervalHours: {{ robot_min_hours|tojson }},
  schedulerOn: {{ scheduler_on|tojson }},
  fold: {{ chat_display|tojson }},
  canContribute: {{ can_contribute|tojson }},
  mailAllowed: {{ mail_allowed|tojson }},
  starters: {{ starters|tojson }}
};
</script>
{% endblock %}
""",


# --- import.html ---
"import.html": r"""{% extends "base.html" %}
{% from "_icons.html" import icon %}
{% from "_admintabs.html" import admintabs %}
{% block title %}管理者メニュー（取り込み） — {{ app_title }}{% endblock %}
{# 見出しは置かない。画面の説明はサイドバーの項目にマウスを乗せると出る #}

{% block body %}
<div class="content content--wide">
  {# 管理者メニューの一画面。同じタブ帯を出して、行き来が同じ画面の中に見えるようにする #}
  <div class="tabs tabs--bar">{{ admintabs('import') }}</div>

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
        <button class="btn btn--sm" id="pickScraper"
                title="scrapers/ に置いたスクリプトを実行し、取得できたファイルを取り込み元にします">スクレイピングで取得する</button>
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

<!-- スクレイピングのスクリプトを選んで試すダイアログ -->
<div class="modal hidden" id="scraperModal">
  <div class="modal__box">
    <div class="modal__head">
      <b>スクレイピングで取得する</b>
      <div class="spacer"></div>
      <button class="btn btn--sm btn--ghost" id="scraperClose" title="閉じる" aria-label="閉じる">{{ icon('x', 'icon--sm') }}</button>
    </div>
    <div class="modal__body" id="scraperList"></div>
    <div class="modal__foot small muted">
      <code>{{ scraper_dir }}</code> 直下の .py が出ます。スクリプトは <code>fetch(out_dir)</code> を定義し、
      out_dir に Excel／CSV を書きます。「試す」で1回実行し、出来たファイルとシートを確認してから選びます。
      取得したファイルはサーバに残しません（表に入れたら消します）。
    </div>
  </div>
</div>

<script>
window.IMP = {
  scrapeTimeout: {{ scrape_timeout|tojson }},
  scrapeInterval: {{ scrape_interval|tojson }},
  scrapeLimits: {{ scrape_limits|tojson }},
  dbFiles: {{ db_files|tojson }},
  existing: {{ existing|tojson }},
  groups: {{ groups|tojson }},
  manage: {{ manage|tojson }},
  intervals: {{ intervals|tojson }},
  modes: {{ modes|tojson }},
  defaultTs: {{ default_ts|tojson }},
  maxKeep: {{ max_keep|tojson }}
};
</script>
{% endblock %}
""",

# --- output.html ---
"output.html": r"""{% extends "base.html" %}
{% from "_icons.html" import icon %}
{% from "_admintabs.html" import admintabs %}
{% block title %}管理者メニュー（出力） — {{ app_title }}{% endblock %}
{# 見出しは置かない。画面の説明はサイドバーの項目にマウスを乗せると出る #}

{% block body %}
<div class="content content--wide">
  {# 管理者メニューの一画面。同じタブ帯を出して、行き来が同じ画面の中に見えるようにする #}
  <div class="tabs tabs--bar">{{ admintabs('output') }}</div>

  {# 出力先フォルダ。利用者が「フォルダに出力して」と頼んだファイルを
     出力先/<利用者名>/ に置く。無ければ利用者名のフォルダを作る #}
  <div class="card">
    <div class="row" style="align-items:center">
      <div class="card__title" style="margin:0">出力先フォルダ</div>
      <span class="badge {{ 'badge--ok' if output.ok else ('badge--err' if output.path else '') }}" id="outBadge"
            style="margin-left:10px">{{ '使えます' if output.ok else ('問題あり' if output.path else '未設定') }}</span>
    </div>
    <div class="card__desc">
      利用者がマイエージェントで「フォルダに出力して」と頼んだファイル（Excel／CSV／テキスト／PowerPoint／Word）を、
      ここに決めたフォルダの中の<b>利用者名のフォルダ</b>に置きます（無ければ作ります）。
      会話に出たファイルの「フォルダに保存」ボタンも同じ場所に書きます。未設定ならダウンロードだけになります。
    </div>
    <div id="outStatus" class="small mb"
         data-ok="{{ 'true' if output.ok else 'false' }}">{{ output.message }}{% if output.source %}（{{ output.source }}の設定）{% endif %}</div>
    <div class="row">
      <input type="text" id="outDir" class="grow" value="{{ output.path }}"
             placeholder="出力先フォルダのパス（例: /mnt/out や \\\\server\\share\\出力）">
      <button class="btn btn--sm btn--primary" id="outSave">保存</button>
      <button class="btn btn--sm" id="outClear" title="出力先を外します（ダウンロードだけになります）">使わない</button>
    </div>
    <div class="small muted mt">
      保存すると書けるかを確かめてから <code>data/output_dir.yaml</code> に残します（<code>env</code> の <code>OUTPUT_DIR</code> が初期値）。
      アプリを動かしているアカウントが、そのフォルダに書ける必要があります。
      アプリ自身のフォルダやデータのフォルダは指定できません。
    </div>
  </div>

  <div class="card mt">
    <div class="card__title">置かれ方</div>
    <div class="card__desc">
      <code>出力先フォルダ／利用者名／ファイル名</code> の形で固定です。利用者名のフォルダは初めて出力したときに作られ、
      以後はそのまま使います。パスは利用者もAIも指定できません。<br>
      ファイル名の日時（付ける／付けない）と、同じ名前があるときの扱い（番号を付けて残す／置き換える）は<b>利用者が決めます</b>:
      マイエージェントでは言葉で（「日時なしで」「置き換えて」）、マイロボットでは登録時とカードの「フォルダ出力」の欄で。
      何も言わなければ「日時を付ける・番号を付けて残す」です。マイロボットで「実行結果をフォルダにも置く」をオンにしたものは、
      実行のたびにその決めごとでここへ出ます。
    </div>
  </div>
</div>
{% endblock %}

{% block scripts %}
<script>window.OUTPUT_INIT = { ok: {{ output.ok|tojson }} };</script>
{% endblock %}
""",

# --- robots.html ---
"robots.html": r"""{% extends "base.html" %}
{% from "_icons.html" import icon %}
{% block title %}マイロボット — {{ app_title }}{% endblock %}
{# 見出しは置かない。画面の説明はサイドバーの項目にマウスを乗せると出る #}

{% block body %}
<div class="content">
  <details class="card" id="howto">
    <summary class="card__title" style="cursor:pointer">マイロボットとは</summary>
    <div class="card__desc" style="margin-top:8px">
      マイエージェントとのやり取りの中でAIが実際に使った道具（SQLの実行・グラフ・Excel作成・メール下書き…）の
      並びに名前を付けて保存したものです。「いま試す」や定期実行で同じ手順を<b>AIなしでそのまま</b>実行するので、
      AIによるぶれなし・待ち時間なし・LLMの費用なし（期間は「実行日で変わる値」で実行日に合わせられます）。結果はマイエージェントの<b>新しい会話</b>に出ます
      （そのあと「これをグラフにして」と続けられます）。
      <ol style="margin:8px 0 0 18px;padding:0;line-height:1.9">
        <li>マイエージェントで、いつもの流れを一度やる（集計 → グラフ → Excel など）</li>
        <li>自分の発言にマウスを乗せて「<b>ロボットにする</b>」→ 含める質問にチェック → 名前 → 保存</li>
        <li>この画面の「いま試す」で、いまの日付で1回動かして確かめます。定期実行は決めた時刻にサーバが動かします</li>
      </ol>
      <div class="mt small muted">
        自分だけのものです（他の人には見えません）。1人 {{ settings.max_per_user }} 件まで
        {%- if interval_label %}、定期実行の間隔は {{ interval_label }}より短くできません{% endif %}
        （管理者が決めています）。同じ名前・同じ内容のものは二重に登録できません。
        全員で使いたい流れは、管理者が「例文」や「ユーザー定義ツール」として登録してください。
      </div>
    </div>
  </details>

  <div id="robotCards" class="mt"></div>
</div>
{% endblock %}

{% block scripts %}
<script>
window.ROBOTS_INIT = {
  robots: {{ robots|tojson }},
  schedVocab: {{ sched_vocab|tojson }},
  mailReady: {{ mail_ready|tojson }},
  allowedDomains: {{ allowed_domains|tojson }},
  minIntervalHours: {{ settings.min_interval_hours|tojson }},
  schedulerOn: {{ scheduler_on|tojson }},
  mailAllowed: {{ mail_allowed|tojson }},
  agentUrl: {{ url_for('chat.index')|tojson }}
};
</script>
{% endblock %}
""",

# --- knowledge.html ---
"knowledge.html": r"""{% extends "base.html" %}
{% from "_admintabs.html" import admintabs %}
{% block title %}管理者メニュー（ナレッジベース） — {{ app_title }}{% endblock %}
{# 見出しは置かない。画面の説明はサイドバーの項目にマウスを乗せると出る #}

{% block body %}
<div class="content">
  <div class="tabs tabs--bar">{{ admintabs('knowledge') }}</div>
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
        追加した瞬間から、マイエージェントのAIがそのナレッジベースを検索できるようになります。
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
      （マイエージェント画面の一覧にも出なくなります）。
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
      利用者はマイエージェント画面のサイドバーから個別に変えられます。ここに出ているのは
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
    {% if app_tagline %}
      <div class="small muted" style="text-align:center;margin:-6px 0 14px;letter-spacing:.04em">{{ app_tagline }}</div>
    {% endif %}

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
{% from "_admintabs.html" import admintabs %}
{% block title %}管理者メニュー（メール設定） — {{ app_title }}{% endblock %}
{# 見出しは置かない。画面の説明はサイドバーの項目にマウスを乗せると出る #}

{% block body %}
<div class="content">
  <div class="tabs tabs--bar">{{ admintabs('mail') }}</div>
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
    <div class="card__title">文面の決まり（このアプリから出す全部のメール）</div>
    <div class="card__desc">
      マイエージェントの下書きも、マイロボットの自動送信も、ここで決めた形で送られます。
      差出人の表示名は「差出人」の欄が空ならアプリ名（{{ app_title }}）になります。
    </div>
    <label class="field">本文の冒頭に必ず入れる断り書き</label>
    <textarea id="bodyHeader" rows="5" style="width:100%"
              placeholder="例: このメールは {app} が自動で作成・送信しています。"></textarea>
    <div class="small muted mt">
      <code>{app}</code> と書くとアプリ名（{{ app_title }}）に置き換わります。空にすると付けません。
    </div>
    <label class="mt" style="display:flex;align-items:center;gap:6px;cursor:pointer">
      <input type="checkbox" id="showSender">
      <span class="small">本文に「送信者（ログインID）」の行を入れる（誰が出したメールか受け取る人に分かるようにする）</span>
    </label>
    <div class="small muted mt">実際に送られる形:</div>
    <pre class="mono" id="bodySample" style="white-space:pre-wrap;background:var(--surface-2);padding:8px;border-radius:var(--radius-sm);font-size:12.5px"></pre>
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
{% from "_admintabs.html" import admintabs %}
{% block title %}管理者メニュー（モデル設定） — {{ app_title }}{% endblock %}
{# 見出しは置かない。画面の説明はサイドバーの項目にマウスを乗せると出る #}

{% block body %}
<div class="content">
  <div class="tabs tabs--bar">{{ admintabs('models') }}</div>
  <div id="banner"></div>

  <details class="card" id="howto">
    <summary class="card__title" style="cursor:pointer">この画面の使い方</summary>
    <div class="card__desc" style="margin-top:8px">
      APIが返すモデルは100件を超えることもあり、その中には旧世代のものや
      マイエージェントに使えないものが混ざっています。そのまま利用者に見せると選び間違えるので、
      <b>ここで「使ってよいモデル」を決めます</b>。
      <ol style="margin:8px 0 0 18px;padding:0;line-height:1.9">
        <li>「一覧から選ぶ」で、使わせたいモデルにチェックを入れる</li>
        <li>「既定のモデル」で、まだ自分で選んでいない利用者が使うものを決める</li>
        <li>下の「設定を保存」を押す</li>
      </ol>
      <div class="mt">
        保存すると、マイエージェント画面のプルダウンは<b>ここで選んだモデルだけ</b>になります。
        候補から外したモデルを選んでいた利用者は、次の質問から既定のモデルに変わります。
      </div>
    </div>
  </details>

  <div class="card">
    <div class="card__title">選択できるモデル</div>
    <div class="card__desc">
      ここに登録したモデルだけが、マイエージェント画面のプルダウンに出ます。
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
      <label class="field">AI呼び出し（chat completions）のURL</label>
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

# --- memory.html ---
"memory.html": r"""{% extends "base.html" %}
{% from "_icons.html" import icon %}
{% block title %}パーソナライズ — {{ app_title }}{% endblock %}
{# 見出しは置かない。画面の説明はサイドバーの項目にマウスを乗せると出る #}

{% block body %}
<div class="content">
  <details class="card" id="howto">
    <summary class="card__title" style="cursor:pointer">パーソナライズとは</summary>
    <div class="card__desc" style="margin-top:8px">
      ChatGPT のメモリと同じ発想です。マイエージェントで質問して答えが返るたびに、AIがもう一度だけ働き、
      やり取りの中から<b>次回以降の質問でも使える前提・好み・期間</b>（「うちの部署は関西工場」「Excel で欲しい」
      「特に言わなければ先月分」）をこの本文に書き足します。データの中身や1回きりの指示は覚えません。
      <div class="mt">
        本文はそのまま次の質問からAIに渡り、使ったときは回答の末尾に「（パーソナライズ「…」を使いました）」と出ます。
        ここで自由に直せます（1行に1つ、「- 」で始める箇条書きがおすすめ）。会話で「忘れて」と言えば、その回答のあとに消えます。
        「覚えない」にすると新しく覚えるのをやめ、いまの本文もAIに渡しません。他の利用者には見えませんが、管理者は管理者メニューで内容を見られます。
      </div>
    </div>
  </details>

  <div class="card memedit">
    <div class="row" style="align-items:center;gap:10px;flex-wrap:wrap">
      <div class="card__title" style="margin:0">AIが覚えていること</div>
      <span class="badge" id="memState"></span>
      <div class="spacer"></div>
      <button class="btn btn--sm btn--ghost" id="memToggle">覚えない</button>
    </div>
    <div class="alert alert--warn small mt hidden" id="memOffNote">
      管理者がこの機能を止めています。いま書いても、AIには渡りません（止めているあいだに覚えることもありません）。</div>
    <div class="alert alert--err small mt hidden" id="memBroken">
      保存ファイル（memory.yaml）が読めませんでした。下の欄は空で表示しています。
      ここで保存すると、新しい本文で置き換わります（読めなかった中身は戻りません）。</div>
    <textarea id="memText" spellcheck="false" placeholder="まだありません。マイエージェントで質問すると、答えのあとにここに書き足されます。&#10;自分で書いてもかまいません（例: - うちの部署は関西工場）"></textarea>
    <div class="row mt" style="align-items:center;gap:10px;flex-wrap:wrap">
      <button class="btn btn--primary btn--sm" id="memSave">保存</button>
      <button class="btn btn--sm btn--danger" id="memClear">全部消す</button>
      <span class="small muted" id="memCount"></span>
      <div class="spacer"></div>
      <span class="small muted" id="memNote"></span>
    </div>
  </div>
</div>
{% endblock %}

{% block scripts %}
<script>
window.MEMORY_INIT = {{ memory|tojson }};
</script>
{% endblock %}
""",

# --- display_admin.html ---
"display_admin.html": r"""{% extends "base.html" %}
{% from "_icons.html" import icon %}
{% from "_admintabs.html" import admintabs %}
{% block title %}管理者メニュー（画面） — {{ app_title }}{% endblock %}
{# 見出しは置かない。画面の説明はサイドバーの項目にマウスを乗せると出る #}

{% block body %}
<div class="content content--wide">
  <div class="tabs tabs--bar">{{ admintabs('display') }}</div>

  <div class="card">
    <div class="card__title">会話の中の枠を畳む</div>
    <div class="card__desc">
      マイエージェントの回答には、答えの文章のほかに SQL の枠・社内文書の検索・登録の提案カードが出ます。
      ちょっとした質問でも積み上がるので、チェックしたものは<b>1行の見出しに畳み、押した人にだけ開きます</b>。
      消すわけではありません。全利用者に同じ値が効き、保存すると、利用者が画面を次に開いたとき（再読み込み）から反映されます。
    </div>
    <div class="row mb" style="align-items:flex-start;gap:24px;flex-wrap:wrap">
      <label style="display:flex;align-items:center;gap:6px;cursor:pointer">
        <input type="checkbox" id="dsSql"> <span class="small">SQL の枠を畳む（SQL本文・日本語の解説・取り方の正誤）</span>
      </label>
      <label style="display:flex;align-items:center;gap:6px;cursor:pointer">
        <input type="checkbox" id="dsSources"> <span class="small">社内文書の検索を畳む（出典の一覧）</span>
      </label>
      <label style="display:flex;align-items:center;gap:6px;cursor:pointer">
        <input type="checkbox" id="dsProposals"> <span class="small">登録の提案カードを畳む（用語集・例文）</span>
      </label>
    </div>
    <div class="small muted mb">
      失敗した SQL は、畳む設定でも開いたまま出します（原因を見に来る場所なので）。
      初期値は SQL {{ '畳む' if defaults.fold_sql else '開く' }}・社内文書 {{ '畳む' if defaults.fold_sources else '開く' }}・提案 {{ '畳む' if defaults.fold_proposals else '開く' }}
      （環境変数 CHAT_FOLD_SQL / CHAT_FOLD_SOURCES / CHAT_FOLD_PROPOSALS でも変えられます）。
    </div>
    <div class="row" style="align-items:center;gap:10px">
      <button class="btn btn--primary btn--sm" id="dsSave">保存</button>
      <span class="small muted" id="dsNote">{% if note.updated_at %}{{ note.updated_at|replace('T', ' ') }} に {{ note.updated_by }} が保存{% else %}まだ保存していません（初期値のまま）{% endif %}</span>
    </div>
  </div>

  <div class="card mt">
    <div class="card__title">カタログに登録できる人</div>
    <div class="card__desc">
      マイエージェントの登録カード（用語集・例文）からカタログに書き込めるのは、<b>管理者と、ここに書いた人</b>だけです。
      カタログは全員のAIの理解になるので、書ける人を限っています。ここに無い人には
      「この質問と答え方を例文にする」のボタンと、提案カードの登録ボタンを出しません（提案カードそのものは出ます）。
    </div>
    {% if open_contrib %}
    <div class="small mb" style="color:var(--warn)">いまは環境変数 CATALOG_OPEN_CONTRIB で「全員が登録できる」になっているため、この一覧は使われません。</div>
    {% endif %}
    <label class="field" for="ccUsers">ログインID（1行に1人。大文字小文字は区別しません）</label>
    <textarea id="ccUsers" rows="6" style="max-width:420px;font-family:var(--mono);font-size:13px" placeholder="t.tanaka&#10;s.suzuki"></textarea>
    <div class="row mt" style="align-items:center;gap:10px">
      <button class="btn btn--primary btn--sm" id="ccSave">保存</button>
      <span class="small muted" id="ccNote">{% if contrib_note.updated_at %}{{ contrib_note.updated_at|replace('T', ' ') }} に {{ contrib_note.updated_by }} が保存（{{ contrib|length }} 人）{% elif open_contrib %}まだ誰も書いていません{% else %}まだ誰も書いていません（登録できるのは管理者だけ）{% endif %}</span>
    </div>
  </div>
</div>
{% endblock %}

{% block scripts %}
<script>
window.DISPLAY_SETTINGS_INIT = { settings: {{ settings|tojson }}, contrib: {{ contrib|tojson }} };
</script>
{% endblock %}
""",

# --- memory_admin.html ---
"memory_admin.html": r"""{% extends "base.html" %}
{% from "_icons.html" import icon %}
{% from "_admintabs.html" import admintabs %}
{% block title %}管理者メニュー（パーソナライズ） — {{ app_title }}{% endblock %}
{# 見出しは置かない。画面の説明はサイドバーの項目にマウスを乗せると出る #}

{% block body %}
<div class="content content--wide">
  <div class="tabs tabs--bar">{{ admintabs('memory') }}</div>

  <div class="card">
    <div class="card__title">パーソナライズの決めごと</div>
    <div class="card__desc">
      利用者のパーソナライズ（AIが会話から覚える、その人についての前提・好み・期間。1人につき1つの本文）の決めごとです。
      全利用者に同じ値が効き、保存するとすぐ反映されます。
    </div>
    <div class="row mb" style="align-items:flex-end;gap:20px;flex-wrap:wrap">
      <div>
        <label class="field">機能</label>
        <label style="display:flex;align-items:center;gap:6px;cursor:pointer">
          <input type="checkbox" id="msEnabled"> <span class="small">パーソナライズを使う（外すと、メニューから消え、AIにも渡しません）</span>
        </label>
      </div>
      <div>
        <label class="field">書き直しに使うモデル</label>
        <select id="msModel" style="min-width:240px">
          <option value="">回答と同じモデル</option>
          {% for m in models %}<option value="{{ m }}">{{ m }}</option>{% endfor %}
        </select>
        <div class="small muted" style="margin-top:4px">回答のたびに1回呼びます。安いモデルにすると費用を抑えられます（候補は「モデル設定」で使えるモデル）。</div>
      </div>
      <div>
        <label class="field">本文の上限（文字）</label>
        <div class="row" style="align-items:center;gap:6px">
          <input type="number" id="msMax" min="{{ ranges.max_chars[0] }}" max="{{ ranges.max_chars[1] }}" step="100" style="width:120px">
          <span class="small muted">（{{ ranges.max_chars[0] }}〜{{ ranges.max_chars[1] }}。超えた分は切ります。できるだけ行の切れ目で）</span>
        </div>
      </div>
    </div>
    <div class="small muted mb">
      初期値は {{ '使う' if defaults.enabled else '使わない' }}・{{ defaults.model or '回答と同じモデル' }}・{{ defaults.max_chars }} 文字
      （環境変数 MEMORY_ENABLED / MEMORY_MODEL / MEMORY_MAX_CHARS でも変えられます）。
    </div>
    <div class="row" style="align-items:center;gap:10px">
      <button class="btn btn--primary btn--sm" id="msSave">保存</button>
      <span class="small muted" id="msNote">{% if note.updated_at %}{{ note.updated_at|replace('T', ' ') }} に {{ note.updated_by }} が保存{% else %}まだ保存していません（初期値のまま）{% endif %}</span>
    </div>
  </div>

  <div class="card mt">
    <div class="card__title">全利用者のパーソナライズ</div>
    <div class="card__desc">利用者ごとの本文をそのまま表示します（閲覧のみ。直せるのは本人だけです）。利用者にも「管理者は見られる」と案内してあります。</div>
    {% if overview %}
    {% for o in overview %}
    <details class="acc">
      <summary>
        <strong>{{ o.user }}</strong>
        <span class="badge" style="margin-left:8px">{{ '覚えている' if o.on else '停止中' }}</span>
        {% if o.broken %}<span class="badge badge--warn" style="margin-left:4px">ファイルが読めません</span>{% endif %}
        <span class="small muted" style="margin-left:8px">{{ o.chars }} 文字・最終更新 {{ o.updated_at|replace('T', ' ') if o.updated_at else '—' }}</span>
      </summary>
      <div class="acc__body">
        {% if o.text %}<pre class="mono" style="white-space:pre-wrap;word-break:break-all;font-size:13px">{{ o.text }}</pre>{% else %}<div class="small muted">本文はありません。</div>{% endif %}
      </div>
    </details>
    {% endfor %}
    {% else %}
    <div class="small muted">まだ誰のパーソナライズもありません。</div>
    {% endif %}
  </div>
</div>
{% endblock %}

{% block scripts %}
<script>
window.MEMORY_SETTINGS_INIT = { settings: {{ settings|tojson }} };
</script>
{% endblock %}
""",

# --- robot_settings.html ---
"robot_settings.html": r"""{% extends "base.html" %}
{% from "_icons.html" import icon %}
{% from "_admintabs.html" import admintabs %}
{% block title %}管理者メニュー（マイロボット） — {{ app_title }}{% endblock %}
{# 見出しは置かない。画面の説明はサイドバーの項目にマウスを乗せると出る #}

{% block body %}
<div class="content content--wide">
  <div class="tabs tabs--bar">{{ admintabs('robots') }}</div>

  <div class="card">
    <div class="card__title">マイロボットの決めごと</div>
    <div class="card__desc">
      利用者が保存するマイロボット（気に入った処理の流れを、AIなしで繰り返すもの）の上限と、実行の間隔、定期実行で同時に動かす数を決めます。
      全利用者に同じ値が効きます（管理者も同じ）。保存するとすぐ反映されます。
    </div>
    <div class="row mb" style="align-items:flex-end;gap:20px;flex-wrap:wrap">
      <div>
        <label class="field">1人あたりの登録上限数</label>
        <div class="row" style="align-items:center;gap:6px">
          <input type="number" id="rsMax" min="{{ ranges.max_per_user[0] }}" max="{{ ranges.max_per_user[1] }}" step="1" style="width:110px">
          <span class="small muted">件（{{ ranges.max_per_user[0] }}〜{{ ranges.max_per_user[1] }}）</span>
        </div>
      </div>
      <div>
        <label class="field">定期実行の最短の間隔</label>
        <div class="row" style="align-items:center;gap:6px">
          <input type="number" id="rsInterval" min="{{ ranges.min_interval_hours[0] }}" max="{{ ranges.min_interval_hours[1] }}" step="0.5" style="width:110px">
          <span class="small muted">時間（0 で制限なし・最大 {{ ranges.min_interval_hours[1] }}）</span>
        </div>
      </div>
      <div>
        <label class="field">1つのロボットの手順数の上限</label>
        <div class="row" style="align-items:center;gap:6px">
          <input type="number" id="rsSteps" min="{{ ranges.max_steps[0] }}" max="{{ ranges.max_steps[1] }}" step="1" style="width:110px">
          <span class="small muted">手順（{{ ranges.max_steps[0] }}〜{{ ranges.max_steps[1] }}）</span>
        </div>
      </div>
      <div>
        <label class="field">同時に動かす数</label>
        <div class="row" style="align-items:center;gap:6px">
          <input type="number" id="rsWorkers" min="{{ ranges.workers[0] }}" max="{{ ranges.workers[1] }}" step="1" style="width:110px">
          <span class="small muted">本（{{ ranges.workers[0] }}〜{{ ranges.workers[1] }}）</span>
        </div>
      </div>
    </div>
    <div class="small muted mb">
      間隔は「前回うまくいった実行」から数えます（失敗した実行はすぐやり直せます）。
      上限に達した利用者は、使わないロボットを削除してから登録します。
      同じ名前・同じ内容のロボットは、決めごとに関係なく二重には登録できません。
      「同時に動かす数」は、時刻が来たロボットを定期実行で何本まで同時に動かすかです。多いほど全員に早く届きますが、そのぶん AI が混みます。
      初期値は {{ defaults.max_per_user }} 件・{{ '%g'|format(defaults.min_interval_hours) }} 時間・{{ defaults.max_steps }} 手順・{{ defaults.workers }} 本
      （環境変数 ROBOT_MAX_PER_USER / ROBOT_MIN_INTERVAL_HOURS / ROBOT_MAX_STEPS / ROBOT_WORKERS でも変えられます）。
    </div>
    <div class="row" style="align-items:center;gap:10px">
      <button class="btn btn--primary btn--sm" id="rsSave">保存</button>
      <span class="small muted" id="rsNote">{% if note.updated_at %}{{ note.updated_at|replace('T', ' ') }} に {{ note.updated_by }} が保存{% else %}まだ保存していません（初期値のまま）{% endif %}</span>
    </div>
  </div>

  <div class="card mt">
    <div class="card__title">いまの登録状況（全利用者）</div>
    <div class="card__desc">利用者ごとのマイロボット。名前を開くと、手順の中身（SQLなど）・実行日で変わる値・定期実行・メール・前回の実行まで見られます。</div>
    {% if overview %}
    {% for o in overview %}
    <details class="acc">
      <summary>
        <strong>{{ o.user }}</strong>{% if o.display_name and o.display_name != o.user %}<span class="small muted" style="margin-left:6px">{{ o.display_name }}</span>{% endif %}
        <span class="badge" style="margin-left:8px">{{ o.count }} 件</span>
        {% if o.scheduled %}<span class="badge" style="margin-left:4px">定期 {{ o.scheduled }} 件</span>{% endif %}
        <span class="small muted" style="margin-left:8px">最後の実行: {{ o.last_run|replace('T', ' ') if o.last_run else 'まだ実行していません' }}</span>
      </summary>
      <div class="acc__body">
        {% for r in o.robots %}
        <details class="acc robotdetail" style="margin-top:6px">
          <summary>
            <strong>{{ r.name }}</strong>
            <span class="small muted" style="margin-left:8px">{{ r.n_steps }}手順・{{ r.tools|join(' → ') }}</span>
            {% if r.schedule.kind != 'manual' %}<span class="badge" style="margin-left:6px">{{ r.schedule.interval_label }}{% if r.schedule.enabled is sameas false %}（止めています）{% elif r.schedule.next_at %}・次回 {{ r.schedule.next_at[5:16]|replace('T', ' ') }}{% endif %}</span>{% endif %}
            {% if r.mail_auto %}<span class="badge" style="margin-left:4px">メール自動送信</span>{% endif %}
            {% if r.last_status == 'error' %}<span class="badge badge--warn" style="margin-left:4px">前回失敗</span>{% endif %}
            <button class="btn btn--sm sbsec__act" data-test-user="{{ o.user }}" data-test-id="{{ r.id }}" data-test-name="{{ r.name }}"
                    data-test-mail="{{ '1' if r.has_mail_steps else '' }}" data-test-tools="{{ r.tools|join(' → ') }}" data-test-steps="{{ r.n_steps }}"
                    title="このロボットを管理者の名前で1回動かします（結果は自分のマイエージェントに。メールは自分宛て。利用者には何も残りません）">管理者として試す</button>
            {% if (r.schedule.interval_minutes and r.schedule.enabled is not sameas false) or r.mail_auto %}
            <button class="btn btn--sm btn--danger sbsec__act" data-stop-user="{{ o.user }}" data-stop-id="{{ r.id }}" data-stop-name="{{ r.name }}"
                    title="この利用者のロボットの定期実行と、メールの自動送信を止めます（手順は消しません。本人はあとで再開できます）">止める</button>
            {% endif %}
          </summary>
          <div class="acc__body small">
            <dl class="robotdetail">
              <dt>手順</dt>
              <dd>{% for sd in r.steps_detail %}<div><span class="badge">手順{{ sd.i }}</span> <b>{{ sd.label }}</b></div><pre class="mono">{{ sd.text }}</pre>{% if sd.explanation %}<div class="muted" style="margin:-4px 0 8px">{{ sd.explanation }}</div>{% endif %}{% endfor %}</dd>
              <dt>元の質問</dt><dd>{{ r.questions|join(' ／ ') or '—' }}</dd>
              <dt>実行日で変わる値</dt><dd>{% if r.dates %}{% for d in r.dates %}{{ d.label }}（登録時 {{ d.sample }} → 今日なら {{ d.now }}）{% if not loop.last %}、{% endif %}{% endfor %}{% else %}なし{% endif %}{% if r.holes %}／固定の値: {% for h in r.holes %}{{ h.label }}＝{{ h.sample }}{% if not loop.last %}、{% endif %}{% endfor %}{% endif %}</dd>
              <dt>使う表</dt><dd>{{ r.tables|join('、') or 'なし' }}</dd>
              <dt>フォルダ出力</dt><dd>{% if r.has_file_steps %}{{ '置く' if r.folder_out else '置かない' }}{% if r.folder_out %}（{{ '日時なし' if not r.folder_stamp else '日時あり' }}・{{ '置き換える' if r.folder_overwrite else '番号を付けて残す' }}）{% endif %}{% else %}ファイルを作る手順はありません{% endif %}</dd>
              <dt>定期実行</dt><dd>{% if r.schedule.kind != 'manual' %}{{ r.schedule.interval_label }}{% if r.schedule.start_at %}（開始 {{ r.schedule.start_at|replace('T', ' ') }}）{% endif %}{% if r.schedule.enabled is sameas false %}・止めています{% elif r.schedule.next_at %}・次回 {{ r.schedule.next_at|replace('T', ' ') }}{% endif %}{% if r.schedule.last_run %}・前回の定期実行 {{ r.schedule.last_run|replace('T', ' ') }}（{{ '成功' if r.schedule.last_status == 'ok' else ('実行中' if r.schedule.last_status == 'running' else '失敗') }}）{{ r.schedule.last_message }}{% endif %}{% else %}手動のみ{% endif %}</dd>
              <dt>メール</dt><dd>{% if r.has_mail_steps %}{{ '実行のたびに自動で送る' if r.mail_auto else '下書きを出すだけ' }}{% else %}メールの手順はありません{% endif %}{% if r.notify_to %}／失敗したら {{ r.notify_to|join('、') }} に知らせる{% endif %}</dd>
              <dt>実行履歴</dt>
              <dd>{% if r.history %}<div class="tablewrap" style="max-height:220px"><table class="data"><thead><tr><th style="width:120px">日時</th><th style="width:60px">種類</th><th style="width:56px">結果</th><th>内容</th></tr></thead><tbody>
                {% for h in r.history|reverse %}<tr><td>{{ h.at[:16]|replace('T', ' ') }}</td><td>{{ '定期' if h.source == 'schedule' else '試す' }}</td><td>{{ '成功' if h.ok else '失敗' }}</td><td>{{ h.message }}</td></tr>{% endfor %}
              </tbody></table></div>{% else %}まだ実行していません{% endif %}</dd>
              <dt>作成・更新・前回の実行</dt><dd>{{ r.created_at|replace('T', ' ') }} ／ {{ r.updated_at|replace('T', ' ') }} ／ {% if r.last_run %}{{ r.last_run|replace('T', ' ') }}（{{ '成功' if r.last_status == 'ok' else ('実行中' if r.last_status == 'running' else '失敗') }}）{{ r.last_message }}{% else %}まだ実行していません{% endif %}</dd>
            </dl>
          </div>
        </details>
        {% endfor %}
      </div>
    </details>
    {% endfor %}
    {% else %}
    <div class="small muted">まだ誰も登録していません。</div>
    {% endif %}
  </div>
</div>
{% endblock %}

{% block scripts %}
<script>
window.ROBOT_SETTINGS_INIT = { settings: {{ settings|tojson }}, mailAllowed: {{ mail_allowed|tojson }},
                               testMailDefault: {{ test_mail_default|tojson }}, agentUrl: {{ url_for('chat.index')|tojson }} };
</script>
<script>
/* 「止める」: 他の利用者の定期実行と自動送信を止める（管理者だけ）。押したら画面を読み直す */
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('[data-stop-id]').forEach(b => b.addEventListener('click', async ev => {
    ev.preventDefault(); ev.stopPropagation();
    if (!confirm(`「${b.dataset.stopName}」（${b.dataset.stopUser}）の定期実行とメールの自動送信を止めますか？`)) return;
    b.disabled = true;
    try {
      await api('/api/catalog/robots/stop', { user: b.dataset.stopUser, id: b.dataset.stopId });
      toast('止めました。'); location.reload();
    } catch (e) { b.disabled = false; toast(e.message, 'err', 9000); }
  }));
  /* 「管理者として試す」: 宛先を決めて1回動かし、所要時間を見せる。利用者側には何も残らない */
  document.querySelectorAll('[data-test-id]').forEach(b => b.addEventListener('click', ev => {
    ev.preventDefault(); ev.stopPropagation();
    const init = window.ROBOT_SETTINGS_INIT;
    const hasMail = b.dataset.testMail === '1';
    const mailTo = el('input', { type: 'text', style: 'width:100%;max-width:420px', value: init.testMailDefault || '',
                                 placeholder: '例: admin@example.co.jp（カンマ区切りで複数可）' });
    const pick = window.ROBOT.mailPicker(mailTo, init.mailAllowed || []);
    const body = el('div', {},
      el('div', { class: 'small' }, el('b', {}, b.dataset.testName), `（${b.dataset.testUser} の登録・${b.dataset.testSteps}手順）`),
      el('div', { class: 'small muted', style: 'margin-top:4px' }, `手順: ${b.dataset.testTools}`),
      el('div', { class: 'small muted', style: 'margin-top:8px;line-height:1.7' },
         '管理者の名前で1回動かします。結果は自分のマイエージェントの新しい会話に出て、フォルダ出力は自分の名前のフォルダに置かれます。'
         + '利用者の実行履歴・前回の実行・定期実行の予定には何も残りません。'),
      hasMail ? el('div', { style: 'margin-top:10px' },
        el('label', { class: 'field' }, 'メールの宛先（全部このアドレスに差し替えて送ります。件名に [試運転] が付きます）'),
        mailTo, pick.node) : null);
    const result = el('div', { class: 'small', style: 'margin-top:10px;white-space:pre-wrap' });
    const go = el('button', { class: 'btn btn--primary', onclick: async () => {
      go.disabled = true;
      result.textContent = '動かしています…';
      try {
        const r = await api('/api/catalog/robots/test', { user: b.dataset.testUser, id: b.dataset.testId, mail_to: mailTo.value });
        result.replaceChildren(
          el('div', { class: r.run_ok ? '' : 'alert alert--err' }, r.message),
          el('div', { class: 'mt' }, el('b', {}, '所要時間: '), r.timings_text || ''),
          el('div', { class: 'mt' }, el('a', { class: 'btn btn--sm', href: init.agentUrl }, '結果の会話を開く（マイエージェント）')));
        go.textContent = 'もう一度';
        go.disabled = false;
      } catch (e) { result.textContent = ''; toast(e.message, 'err', 9000); go.disabled = false; }
    } }, '動かす');
    const close = window.ROBOT.modal('管理者として試す', el('div', {}, body, result), [go], { wide: true });
    if (hasMail) mailTo.focus();
  }));
});
</script>
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
{% from "_admintabs.html" import admintabs %}
{% block title %}管理者メニュー（利用状況） — {{ app_title }}{% endblock %}
{# 見出しは置かない。画面の説明はサイドバーの項目にマウスを乗せると出る #}

{% block body %}
<div class="content content--wide">
  <div class="tabs tabs--bar">{{ admintabs('usage') }}</div>

  {# 集計の切り口と条件は1本の帯にまとめる。タブを切り替えても条件はそのまま持ち回る
     （上の管理者メニューの帯とは別。JSは data-view のあるタブだけを見る） #}
  <div class="tabs tabs--bar tabs--sub">
    {% for v in views if not v.merged %}
    {% if v.sep %}<span class="tabs__sep"></span>{% endif %}
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

  {# レポート。集計ではなく読み物なので、表の枠とは別に描く #}
  <div class="tabpane" id="pane-doc">
    <div class="row mb" style="align-items:center;gap:8px;flex-wrap:wrap">
      <input type="text" id="uRepName" style="max-width:140px" placeholder="2026-09">
      <button class="btn btn--sm btn--primary" id="uRepBuild"
              title="いまの条件で集計し、AIに1回だけ読み物を書かせます">レポートを作る</button>
      <select id="uRepPick" style="max-width:200px"><option value="">保存したレポート…</option></select>
      <span class="small muted" id="uRepNote"></span>
    </div>
    <div class="alert alert--warn small mb">
      作るときだけAIを1回呼びます（費用がかかります）。数字はこのアプリが数えたもので、
      AIには言葉だけを書かせています。集計の中身は左のタブで確かめてください。</div>
    <div id="uRepBody"></div>
  </div>

  {# 会話の履歴。左に一覧、右に中身 #}
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


# --- help.html はファイルから読む ---------------------------------------------------
# 48万字あって assets.py の半分を占めていた。中身は文書なので、コードとは
# 別の速度で変わる。HTMLのファイルとして持てば、編集も検査もしやすい。
#
# 配り方は変えていない。ここで TEMPLATES に入れるだけなので、この先の
# DictLoader も /help のルートも、検証スイートもそのまま通る。
_HELP_FILE = Path(__file__).parent / "templates" / "help.html"
try:
    TEMPLATES["help.html"] = _HELP_FILE.read_text(encoding="utf-8")
except OSError as _e:
    # 黙って404を返してはいけない。画面が真っ白なのに理由が分からなくなる。
    # 配り忘れはここで気づけるように、起動そのものを止める
    raise RuntimeError(
        f"ヘルプの本文が読めません: {_HELP_FILE}（{_e}）。"
        "assets.py と同じ場所に templates/help.html を置いてください。") from _e


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
   マイエージェントだけは画面に固定して、ログの中だけをスクロールさせたいので
   body に .is-chat を付けて切り替える（下の .is-chat .main を参照）。 */
.main { flex: 1; min-width: 0; display: flex; flex-direction: column; }
/* flexの既定で縮められると中身がはみ出して読めなくなるので、縮小を止める */
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
   以前ここでマイエージェントだけ display:none にしていたが、同じことをする画面が
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
.content { flex: none; padding: 24px 28px 72px; max-width: 1400px; width: 100%; }
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
/* 定期取り込みが設定どおりに動いていないDB・テーブルに付ける印（マイエージェントのサイドバー） */
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
/* 管理者メニューの帯: データカタログのタブと、それ以外の画面のタブの間の区切り */
.tabs__sep { width: 1px; background: var(--border); margin: 8px 6px; align-self: stretch; }
/* 帯の下にもう1段（利用状況の集計の切り口）。上の帯と続きに見えるよう、間を詰める */
.tabs--sub { margin-top: -8px; }
/* ビューの「使ったデータ」: 表ごとに1行、その下に読んだ列を並べる */
.usedrow { margin-top: 6px; }
.usedrow .icon { width: 14px; height: 14px; vertical-align: -2px; margin-right: 4px; }
.usedcols { display: flex; flex-wrap: wrap; gap: 2px 12px; margin: 2px 0 0 20px; font-size: 12.5px; }

details.acc { border: 1px solid var(--border); border-radius: var(--radius-sm); margin-bottom: 10px; background: var(--surface); }
details.acc > summary {
    padding: 9px 13px; cursor: pointer; font-weight: 600; font-size: 13px;
    list-style: none; display: flex; align-items: center; gap: 8px;
}
details.acc > summary::-webkit-details-marker { display: none; }
details.acc > summary::before { content: "▸"; color: var(--muted); }
details.acc[open] > summary::before { content: "▾"; }
details.acc > .acc__body { padding: 0 13px 13px; }
/* 畳める道具の枠。見出しが summary になり、右端に ▸ / ▾ を出す */
details.toolblock--fold > summary { cursor: pointer; list-style: none; }
details.toolblock--fold > summary::-webkit-details-marker { display: none; }
details.toolblock--fold > summary::after {
    content: "▸"; color: var(--muted); margin-left: auto; padding-left: 6px; flex: none;
}
details.toolblock--fold[open] > summary::after { content: "▾"; }
details.toolblock--fold > summary:hover { color: var(--text); }
details.toolblock--fold > .toolblock__inner { padding: 2px 0 6px; }
/* 提案カードは自前の見出しと枠を持つ。畳んだ枠の中では見出しは summary が兼ねるので、二重に出さない */
details.toolblock--fold > .toolblock__inner > .mailcard { border: 0; border-radius: 0; margin-bottom: 0; }
details.toolblock--fold > .toolblock__inner > .mailcard > .mailcard__head { display: none; }
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

/* マイエージェントから飛んできたテーブル。どれを開いたのかが一目で分かるように光らせる */
details.acc.is-target {
    border-color: var(--accent);
    box-shadow: 0 0 0 3px var(--accent-weak);
    transition: box-shadow .4s, border-color .4s;
}

/* --- マイエージェント --------------------------------------------------------------- */

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
    display: flex; align-items: center; gap: 8px; padding: 8px 12px; flex-wrap: wrap;
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

/* 触れているテーブルから、カタログの該当テーブルへ飛ぶリンク（マイエージェント画面） */
.catlinks { display: flex; align-items: center; gap: 8px; flex-wrap: wrap;
            font-size: 12px; }
.catlinks a { font-family: var(--mono); font-size: 11.5px; }

.plot { width: 100%; min-height: 340px; }
/* --- 社内文書の出典 -----------------------------------------------------------
   回答の [出典n] と突き合わせるための一覧。抜粋は2行に畳み、
   行を押すと全文が出る（長い抜粋が並ぶと、回答本文が埋もれるため）。 */

.srcs { padding: 8px 11px; display: flex; flex-direction: column; gap: 8px; }
.src { border-left: 2px solid var(--border); padding-left: 9px; }
.src__where { font-size: 12.5px; display: flex; gap: 6px; flex-wrap: wrap; align-items: baseline; }
.src__no { color: var(--accent); font-weight: 600; }
.src__text {
    /* 抜粋は先頭200字しか来ないので、切らずにそのまま出す。押す場所でもない。
       件数が多くて埋まる問題は「引用された出典だけ開く」の方で解いてある。 */
    /* 改行はそのままにしない。文書の抜粋には改行が多く、そのまま出すと
       1件で画面が埋まる。続けて流して、折り返しだけ任せる。 */
    color: var(--muted); font-size: 12.5px; line-height: 1.7; margin-top: 2px;
    word-break: break-word;
}
/* 引用されなかった出典を開く・畳む。件数を出すので、押す前に量が分かる */
.srcs__more {
    background: none; border: 0; padding: 0; font: inherit; font-size: 12px;
    color: var(--muted); cursor: pointer;
    text-decoration: underline; text-underline-offset: 3px;
}
.srcs__more:hover { color: var(--accent); }

/* 集計の切り口の帯に入れる区切り。左がニーズ、右が健康診断 */
.tabs--sub .tabs__sep { height: 18px; align-self: center; margin: 0 10px;
                        background: var(--border-2); flex: none; }

.filecard {
    display: flex; align-items: center; gap: 12px; padding: 13px 15px;
    border: 1px solid var(--border-2); background: var(--surface);
    border-radius: var(--radius-sm); margin-bottom: 10px;
}
.filecard .icon { color: var(--muted); }
.filecard .name { font-weight: 500; }

/* --- 画像のドロップ先 ------------------------------------------------------------
   ふだんは出さず、ファイルをドラッグしてきたときだけマイエージェント全体を覆う。
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
/* 触れるまで隠す（常時表示にすると短い吹き出しの文字に被って読みづらい）。
   キーボード操作でも出るように :focus-within を入れる */
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
.dbpick__tables { padding: 2px 10px 9px 22px; display: none; }
.dbpick.is-open .dbpick__tables { display: block; }
/* テーブル名は「押すと中身が開く」リンク。ふだんは一覧として静かに見せ、
   マウスを乗せたときだけ下線を出す（サイドバーが青いリンクだらけにならないように） */
.dbpick__table {
    display: flex; gap: 7px; align-items: center; font-size: 12px; padding: 2px 0;
}
/* 表／ビューの種類のアイコン。名前より一段薄く、行の高さを変えない */
.dbpick__kind { display: inline-flex; flex: 0 0 auto; color: var(--muted); }
.dbpick__kind .icon--sm { width: 13px; height: 13px; }
.ertable__name { display: flex; align-items: center; gap: 4px; }
.ertable__name .icon--sm { width: 13px; height: 13px; opacity: .8; }
.dbpick__tname {
    color: var(--muted); text-decoration: none; min-width: 0;
    overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.dbpick__tname:hover { color: var(--text); text-decoration: underline; text-underline-offset: 2px; }
/* 対象にする表の選択。外したものは薄くして、消さずに残す（また戻せることを示す） */
.tblpick, .grppick { flex: none; margin: 0; cursor: pointer; }
.dbpick__table:has(.tblpick:not(:checked)) .dbpick__tname { opacity: .45; }
/* 一覧はチェックの分だけ左を詰める（インデントが二重にならないように） */
/* --- この答えはどうだったか（回答の右下の3つの選択肢） ------------------------------
   「役に立ったか」と「合っているか」は別の軸だが、ボタンを4つ並べると
   非IT部門の人は読み分けられない。1行1問にして、選択肢を3つにする。
   見た目は静かに: 枠も背景も持たない薄い文字を細い縦線で区切り、右端に寄せる。
   本文は左から読むので、右端なら視線の通り道に入らない。乗せると下線が出て押せると分かる。
   強調色（オレンジ）は使わない。答えより評価が目立ってしまうため。 */
.fbrow {
    display: flex; align-items: center; gap: 0; flex-wrap: wrap; justify-content: flex-end;
    font-size: 11.5px; color: var(--muted); margin: 0 0 8px;
}
.fbrow__b {
    border: 0; border-left: 1px solid var(--border); background: transparent; color: var(--muted);
    border-radius: 0; padding: 1px 8px; font: inherit; font-size: 11.5px; line-height: 1.5; cursor: pointer;
}
.fbrow__b:first-of-type { border-left: 0; padding-left: 6px; }
.fbrow__b:hover { color: var(--text); text-decoration: underline; text-underline-offset: 3px; }
.fbrow__b:disabled { opacity: .5; cursor: default; text-decoration: none; }
.fbrow__done { color: var(--muted); }
/* SQLの枠の下: 「合っている／合っていない」は右へ、「この質問と答え方を例文にする」は左に枠なしで */
.toolblock__foot--judge > .fbrow { margin: 0 0 0 auto; order: 2; }
.toolblock__foot--judge > .btn { order: 1; border-color: transparent; background: transparent; color: var(--muted); }
.toolblock__foot--judge > .btn:hover { background: var(--surface-2); color: var(--text); }
.fbask {
    background: var(--surface-2); border: 1px solid var(--border); border-radius: var(--radius-sm);
    padding: 9px 11px; margin: 0 0 10px 2px; font-size: 12px; max-width: 640px;
}
.fbask input[type=text] { max-width: 260px; }
.fbask .row { gap: 7px; align-items: center; flex-wrap: wrap; margin-top: 6px; }

/* 答えきれなかったことの申告。AIが自分で書いた1行を、そのまま管理者に渡す */
.gapcard {
    background: var(--warn-weak); border: 1px solid var(--border); border-radius: var(--radius-sm);
    padding: 10px 12px; margin-bottom: 10px; font-size: 12.5px; max-width: 640px;
}
.gapcard__what { color: var(--muted); margin: 5px 0 9px; }

/* --- パーソナライズ（専用の画面。本文は1つのテキスト） ------------------------ */
.memedit textarea { width: 100%; min-height: 340px; margin-top: 10px; font-size: 14px; line-height: 1.75;
                    font-family: inherit; resize: vertical; }
.memedit.is-off textarea { opacity: .55; }

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
/* マイロボット: 登録ダイアログの質問ごとの囲いと、一覧のカード */
.robotturn { padding: 8px 10px; border: 1px solid var(--border); border-radius: var(--radius-sm);
             margin-bottom: 8px; }
.robotcard + .robotcard { margin-top: 10px; }
/* 宛先の候補（許可されたアドレス）。押すと入力欄に足す */
.mailpick { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 6px; }
.mailpick__item {
    border: 1px solid var(--border-2); background: var(--surface); color: var(--text);
    border-radius: 999px; padding: 2px 10px; font: inherit; font-size: 12px; cursor: pointer;
}
.mailpick__item:hover { border-color: var(--muted); background: var(--surface-2); }
/* 登録ダイアログ・詳細: 手順の中身（SQLなど）は折り返して全部読める */
.robotstep { margin-top: 6px; }
.robotstep__sum { white-space: pre-wrap; word-break: break-all; font-size: 12.5px; line-height: 1.5;
                  margin: 2px 0 0 6px; padding: 4px 8px; background: var(--surface-2); border-radius: var(--radius-sm); }
.robotdetail pre { white-space: pre-wrap; word-break: break-all; font-size: 12.5px; margin: 4px 0 8px;
                   padding: 6px 8px; background: var(--surface-2); border-radius: var(--radius-sm); }
.robotdetail dt { font-weight: 600; margin-top: 8px; }
.robotdetail dd { margin: 2px 0 0 0; }
.schedgrid { display: grid; grid-template-columns: max-content 1fr; gap: 6px 10px; align-items: center; }

/* --- ER図キャンバス --------------------------------------------------------- */

.er { position: relative; border: 1px solid var(--border); border-radius: var(--radius);
      background: var(--surface); overflow: hidden; height: 620px; }
/* マイエージェントのモーダル内での高さ。インラインstyleにすると .er--full の100vhが
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
    display: flex; flex-direction: column;
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
/* 広い版（マイロボットの登録）。手順のSQLを折り返して読めるように */
.modal__box--wide { max-width: 980px; max-height: 88vh; font-size: 14px; }
.modal__box--wide .modal__body { padding: 10px 14px; }
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

// --- 整列アルゴリズム（純粋関数。ER図の「整列」ボタンが使う） ---
/**
 * 関連にそって表を並べ直す。戻り値は {id: {x, y}}（渡した nodes の分だけ。左上が 0,0）。
 *   nodes  … [{id, table}]（表示中の表）
 *   edges  … [{from:[alias, table, col], to:[alias, table, col]}]
 *   sizeOf … id → {w, h}（画面の実寸）
 * 決め方:
 *   1. 関連でつながる表ごとの「かたまり」に分ける
 *   2. かたまりの中では、関連の to 側（参照される親・マスタ）を右の列へ。列は
 *      from → to の道のりの長さで決める（循環していても止まる）
 *   3. 同じ列の中は、隣の列でつながる相手の位置の平均に近い順に並べ、線の交差を減らす
 *   4. かたまりは大きい順に縦に積み、1表だけのもの（つながりのない表）は最後に格子で並べる
 */
function erArrangeLayout(nodes, edges, sizeOf) {
    const GAP_X = 90, GAP_Y = 36, GAP_BLOCK = 80, GRID_COLS = 4;
    const out = {};
    if (!nodes.length) return out;
    const ids = new Set(nodes.map(n => n.id));
    const byId = new Map(nodes.map(n => [n.id, n]));
    const name = id => String((byId.get(id) || {}).table || id);
    const byName = (a, b) => name(a).localeCompare(name(b), 'ja');
    // 隣接（向きなし）と、向き（from → to）
    const adj = new Map(nodes.map(n => [n.id, new Set()]));
    const outs = new Map(nodes.map(n => [n.id, new Set()]));
    (edges || []).forEach(e => {
        const f = `${e.from[0]}.${e.from[1]}`, t = `${e.to[0]}.${e.to[1]}`;
        if (!ids.has(f) || !ids.has(t) || f === t) return;
        adj.get(f).add(t); adj.get(t).add(f); outs.get(f).add(t);
    });
    // かたまり
    const seen = new Set(), comps = [];
    nodes.forEach(n => {
        if (seen.has(n.id)) return;
        const comp = [], stack = [n.id];
        seen.add(n.id);
        while (stack.length) {
            const id = stack.pop();
            comp.push(id);
            adj.get(id).forEach(m => { if (!seen.has(m)) { seen.add(m); stack.push(m); } });
        }
        comps.push(comp);
    });
    const linked = comps.filter(c => c.length > 1)
        .sort((a, b) => b.length - a.length || byName(a[0], b[0]));
    const alone = comps.filter(c => c.length === 1).map(c => c[0]).sort(byName);
    let y0 = 0;
    linked.forEach(comp => {
        const set = new Set(comp);
        // 列 = from → to の最長の道のり（循環があっても表の数で打ち切る）
        const level = new Map(comp.map(id => [id, 0]));
        for (let round = 0; round < comp.length; round++) {
            let changed = false;
            comp.forEach(f => outs.get(f).forEach(t => {
                const next = level.get(f) + 1;
                if (set.has(t) && level.get(t) < next && next < comp.length) {
                    level.set(t, next); changed = true;
                }
            }));
            if (!changed) break;
        }
        const ncol = Math.max(...level.values()) + 1;
        const cols = Array.from({ length: ncol }, () => []);
        comp.forEach(id => cols[level.get(id)].push(id));
        cols.forEach(c => c.sort(byName));
        // 隣の列の相手の位置の平均で並べ替え（左→右、右→左を1回ずつ）
        const pos = new Map();
        cols.forEach(c => c.forEach((id, k) => pos.set(id, k)));
        const sweep = (i, ref) => {
            const key = id => {
                const ns = [...adj.get(id)].filter(m => level.get(m) === ref).map(m => pos.get(m));
                return ns.length ? ns.reduce((s, v) => s + v, 0) / ns.length : Number.POSITIVE_INFINITY;
            };
            cols[i].sort((a, b) => (key(a) - key(b)) || byName(a, b));
            cols[i].forEach((id, k) => pos.set(id, k));
        };
        for (let i = 1; i < ncol; i++) sweep(i, i - 1);
        for (let i = ncol - 2; i >= 0; i--) sweep(i, i + 1);
        // 置く。列ごとに縦に積み、列の幅はいちばん広い表に合わせる。
        // 1つのマスタに多くの表がぶら下がると1列が縦に長くなりすぎるので、
        // MAX_ROWS を超えた列は隣に折り返して格子にする（並び順は保つ）
        const MAX_ROWS = 4;
        let x = 0, blockH = 0;
        cols.forEach(col => {
            for (let i = 0; i < col.length; i += MAX_ROWS) {
                let y = y0, w = 0;
                col.slice(i, i + MAX_ROWS).forEach(id => {
                    const s = sizeOf(id);
                    out[id] = { x, y };
                    y += s.h + GAP_Y;
                    w = Math.max(w, s.w);
                });
                blockH = Math.max(blockH, y - y0 - GAP_Y);
                x += w + GAP_X;
            }
        });
        y0 += blockH + GAP_BLOCK;
    });
    // つながりのない表は格子で
    let x = 0, y = y0, rowH = 0;
    alone.forEach((id, i) => {
        if (i && i % GRID_COLS === 0) { x = 0; y += rowH + GAP_Y; rowH = 0; }
        const s = sizeOf(id);
        out[id] = { x, y };
        x += s.w + GAP_X;
        rowH = Math.max(rowH, s.h);
    });
    return out;
}
// --- /整列アルゴリズム ---

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
    // 読み取り専用（マイエージェントからの表示）。編集の入口だけを閉じ、
    // 移動・パン・ズーム・全画面はそのまま使えるようにする。
    let ro = false;
    let docWired = false;         // documentへのキーハンドラは1回だけ張る
    // 過去の分析で実際に使われた結合の回数（{ "a.t.c||a.t.c": n }）。
    // 宣言された関連の上に「本当に通っている道」を重ねるためのもの。
    let usage = null;

    const NS = 'http://www.w3.org/2000/svg';
    // 多重度は "from側:to側"。from は外部キーを持つ子、to は参照される親。
    // 値は 0..1 / 1 / 0..* / 1..*（下限＝相手が無くてもよいか、上限＝1つか多か）。
    // 組み合わせは順不同で10通り。親側に小さい方を置いた向きで並べる
    let linking = false;   // 線を結んだ直後の実データ検査中（次の線は待ってもらう）
    const CARDS = ['0..*:1', '1..*:1', '0..*:0..1', '1..*:0..1',
                   '1:1', '0..1:1', '0..1:0..1',
                   '0..*:0..*', '0..*:1..*', '1..*:1..*'];
    const MULT_JA = { '1': 'ちょうど1件', '0..1': '0件か1件', '0..*': '0件以上', '1..*': '1件以上' };
    // 古い保存（N:1 / 1:N / 1:1 / N:M）も読めるように揃える。読めなければ既定の多対1
    function normCard(c) {
        const m = { N: '0..*', M: '0..*', '*': '0..*' };
        const p = String(c || '').split(':').map(x => m[x.trim()] || x.trim());
        return (p.length === 2 && p.every(x => x in MULT_JA)) ? p.join(':') : '0..*:1';
    }
    // 種類の名前（多対1・1対1・多対多・1対多）。上限だけで決まる
    function cardJa(c) {
        const [f, t] = normCard(c).split(':');
        const many = x => x.endsWith('*');
        if (many(f) && !many(t)) return '多対1';
        if (!many(f) && !many(t)) return '1対1';
        return many(f) && many(t) ? '多対多' : '1対多';
    }
    // 両端の意味を日本語で。ft/tt は from側・to側の表名
    function cardNote(c, ft, tt) {
        const [f, t] = normCard(c).split(':');
        return `「${tt}」1件につき「${ft}」は${MULT_JA[f]}。「${ft}」1件につき「${tt}」は${MULT_JA[t]}`;
    }

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
                // 名前の前に種類のアイコン（格子＝表、重なった紙＝ビュー）。サイドバーと同じ
                el('div', { class: 'ertable__name', title: n.type === 'view' ? 'ビュー（保存したSELECT）' : 'テーブル' },
                    icon(n.type === 'view' ? 'view' : 'table', 'icon--sm'), n.table),
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
            // 多重度は cardinality（"0..*:1" など。旧 "N:1" も normCard が読み替える）から組み立てる。
            // ラベル文字列（"* ─ 1"）を切り分ける形だと、区切りが罫線（─ U+2500）
            // なのに ASCII の "-" で切っていて必ず失敗し、
            // どの関連も既定の「* ─ 1」に見えていた（1:N も 1:1 も N:M も同じ形）。
            const [l, r] = normCard(e.cardinality).split(':');
            // 「0..*」は「1」より幅があるので、線の端から少し離す
            const off = x => (x.length > 1 ? 22 : 14);
            marks.push([p.a, l, p.a.x < p.b.x ? off(l) : -off(l), on],
                       [p.b, r, p.b.x > p.a.x ? -off(r) : off(r), on]);

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
            // 実線と同じIPA表記で多重度を描く
            const [cl, cr] = normCard(sg.cardinality).split(':');
            const offS = x => (x.length > 1 ? 22 : 14);
            marks.push([p.a, cl, p.a.x < p.b.x ? offS(cl) : -offS(cl), on, true],
                       [p.b, cr, p.b.x > p.a.x ? -offS(cr) : offS(cr), on, true]);
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
    let suggestions = [];       // 結合候補（「結合を探す」で保存したもの＋過去のSQL由来）。setSuggestions で受け取る
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
        panel.dataset.kind = (opts && opts.kind) || '';     // 何のパネルか（進み具合の描き直しの判定に使う）
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
                `多重度: ${normCard(sg.cardinality)}（${cardJa(sg.cardinality)}。登録後に変更できます）`),
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
                        `多重度（現在 ${normCard(e.cardinality)}＝${cardJa(e.cardinality)}: `
                        + `${cardNote(e.cardinality, e.from[1], e.to[1])}）`),
                    // 10通りを並べる。左の値が子（外部キー側）、右の値が親。表名は長いので見出しに1回だけ出す
                    el('div', { class: 'small muted mb' }, `左 = ${e.from[1]}（子）、右 = ${e.to[1]}（親）`),
                    // 旧表記 1:N を読み替えた "1:0..*" など、10通りに無い向きは選択状態にならないので注記する
                    CARDS.includes(normCard(e.cardinality)) ? '' : el('div', { class: 'alert alert--info small mb' },
                        `いまの多重度（${normCard(e.cardinality)}）は選択肢に無い向きです（子側が1・親側が多）。`
                        + '子と親が逆に登録されている形なので、下から選び直してください。'),
                    el('div', { class: 'mb', style: 'display:grid;gap:4px' }, CARDS.map(c =>
                        el('button', {
                            class: 'btn btn--sm' + (c === normCard(e.cardinality) ? ' btn--primary' : ''),
                            style: 'justify-content:flex-start;text-align:left;white-space:normal;height:auto',
                            title: cardNote(c, e.from[1], e.to[1]),
                            // index ではなく from/to で指す。表やビューを消すと
                            // 関連の配列が詰まり、index は別の関連を指してしまう
                            onclick: () => mutate({ action: 'update', index: e.index,
                                                    from: e.from_ref, to: e.to_ref,
                                                    cardinality: c }),
                        }, `${c.split(':')[0]} ─ ${c.split(':')[1]}（${cardJa(c)}）`))),
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
        // 主キーの編集はカタログ画面だけ（読み取り専用のマイエージェントでは出さない）。
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
        if (linking) { toast('前の線の実データを確認しています。終わってから操作してください。'); return; }
        const e = past.pop();
        if (!e) return;
        try { await e.undo(); future.push(e); toast(`元に戻しました: ${e.label}`); }
        catch (err) { toast(`元に戻せませんでした: ${err.message}`, 'err'); }
        syncHistoryUi();
    }

    async function redo() {
        if (linking) { toast('前の線の実データを確認しています。終わってから操作してください。'); return; }
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
        const adding = body.action === 'add';
        if (adding) {
            // 大きな表では実データの検査に数秒かかる。待っていることを見せ、終わるまで次の操作は待ってもらう
            // （元に戻す／やり直す・候補の登録もここを通るので、1か所で済ませる）
            linking = true;
            showPanel('実データを確認しています…', [
                el('div', { class: 'small muted' }, '結んだ2列の値の重なりと一意性を見ています。大きな表では数秒かかります。')]);
        }
        try {
            // 実データの検査が長引いても画面が固まらないよう、60秒で諦めて理由を出す（サーバ側は5秒で切り上げる作り）
            const r = await Promise.race([
                api('/api/catalog/relationship', { db: CAT.db, ...body }),
                new Promise((_, rej) => setTimeout(() => rej(new Error(
                    'サーバの応答が60秒ありません。表が大きく検査に時間がかかっています。少し待ってから画面を更新してください。')), 60000)),
            ]);
            // 保存せずに聞き返す応答（実データ判定で停止／複合キーの合流確認）には
            // 図データが入らない。ここで返さないと図を空で置き換えて壊してしまう
            if (r.check || r.ask) return r;
            applyEr(r.er); closePanel();
            return r;
        } catch (e) {
            if (adding) closePanel();                 // 「確認しています」を出したままにしない
            throw e;
        } finally {
            if (adding) linking = false;
        }
    }

    /* 人の操作から呼ぶ。サーバに保存したうえで、逆の操作を履歴に積む */
    async function mutate(body) {
        if (linking) { toast('前の線の実データを確認しています。終わってから操作してください。'); return; }
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
                // 多重度は主キーの並びからの推定なので、登録した線をそのまま選択状態にして
                // 10通りのパネルを開く。違っていれば1回押すだけで直せる
                const added = data.edges.find(e2 => e2.kind === 'meta' && e2.from_ref === a.from && e2.to_ref === a.to);
                if (added) {
                    selectEdge(added);
                    toast(`関連を登録しました（多重度 ${normCard(added.cardinality)}＝${cardJa(added.cardinality)}。違えば右のパネルで選び直せます）`);
                }
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
            if (linking) { toast('前の線の実データを確認しています。終わってから引いてください。'); return; }
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
        if (b) return '0..*:1';
        if (a) return '1:0..*';
        return '0..*:0..*';
    }


    function wireViewport() {
        // init は表の削除などで何度も呼ばれる。要素に印を付けて1回だけ張る
        // （フラグ1本にすると、要素ごと作り直すマイエージェント側で張られなくなる）
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

    /** 表示中の表を関連にそって並べ直す。1手として積むので Ctrl+Z で戻せる。保存は 💾。 */
    function arrange() {
        const shown = shownNodes();
        if (!shown.length) return;
        const sizeOf = id => {
            const b = world.querySelector(`.ertable[data-id="${CSS.escape(id)}"]`);
            return { w: b?.offsetWidth || 232, h: b?.offsetHeight || 120 };
        };
        const target = erArrangeLayout(shown, data.edges || [], sizeOf);
        // 表示中の表の左上を起点にする（まとまりで絞っているとき、他のまとまりの
        // 表が置いてある場所へ被せないように、いまの場所の近くに並べ直す）
        const minX = Math.min(...shown.map(n => n.x)), minY = Math.min(...shown.map(n => n.y));
        const before = Object.fromEntries(shown.map(n => [n.id, { x: n.x, y: n.y }]));
        const after = Object.fromEntries(shown.map(n =>
            [n.id, { x: Math.round(minX + target[n.id].x), y: Math.round(minY + target[n.id].y) }]));
        if (JSON.stringify(before) === JSON.stringify(after)) { toast('すでに整列しています。'); return; }
        const apply = m => {
            data.nodes.forEach(n => { if (m[n.id]) { n.x = m[n.id].x; n.y = m[n.id].y; } });
            render(); syncHistoryUi(); setTimeout(fit, 20);
        };
        record({ label: '整列', undo: () => apply(before), redo: () => apply(after) });
        apply(after);
        toast(ro ? '並べ直しました。'
                 : '並べ直しました。この配置で残すには保存（💾）を押してください。Ctrl+Z で戻せます。',
              'ok', 6000);
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
        // マイエージェントでは開くたびに init し直すので、前回の状態を持ち越さない
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
        once('#erDiscover', openDiscover);
        once('#erUndo', undo);
        once('#erRedo', redo);
        once('#erArrange', arrange);
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
                // 入力欄にいないときだけ受ける（他のタブやマイエージェントでは横取りしない）
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

    /* --- 結合を探す（全表の全列を実データで調べて候補を保存する） --------------------- */
    let joinStatus = null;
    function setJoinStatus(s) { joinStatus = s || null; syncDiscoverBtn(); }
    function syncDiscoverBtn() {
        const b = $('#erDiscover');
        if (!b) return;
        const stale = joinStatus ? (joinStatus.new || []).length + (joinStatus.changed || []).length : 0;
        b.textContent = joinStatus && !joinStatus.exists ? '結合を探す（まだ探していません）'
            : (joinStatus?.exists && stale ? `結合を探す（表が増えました ${stale}）` : '結合を探す');
    }
    async function fetchJoinStatus() {
        const r = await api(`/api/catalog/joins/status?db=${encodeURIComponent(CAT.db)}`, undefined, 'GET');
        joinStatus = r; syncDiscoverBtn();
        return r;
    }
    async function openDiscover() {
        let st;
        try { st = await fetchJoinStatus(); } catch (e) { toast(e.message, 'err'); return; }
        if (st.running) { showDiscoverProgress(); return; }
        const stale = (st.new || []).length + (st.changed || []).length;
        const lines = [];
        lines.push(el('div', { class: 'small muted mb' },
            '全表の全列を実データで調べ、値が重なる列の組を結合の候補にします。多重度も推定します。'
            + '表が大きいと数分かかります。表の定義が変わらなければ探し直す必要はありません。'));
        if (st.exists) {
            lines.push(el('div', { class: 'small mb' },
                `前回: ${String(st.computed_at || '').replace('T', ' ')}（候補 ${st.count} 件、${st.seconds ?? '?'} 秒）`));
            if (stale) lines.push(el('div', { class: 'alert alert--info small mb' },
                `定義が増えた・変わった表: ${[...(st.new || []), ...(st.changed || [])].slice(0, 8).join('、')}`
                + (stale > 8 ? ` ほか（計 ${stale}）` : '')));
        }
        const start = async (scope) => {
            try {
                const r = await api('/api/catalog/joins/discover', { db: CAT.db, scope });
                if (!r.started) { toast(r.message || '始められませんでした。'); return; }
                showDiscoverProgress();
            } catch (e) { toast(e.message, 'err'); }
        };
        const btns = [];
        if (st.exists && stale) btns.push(el('button', { class: 'btn btn--sm btn--primary', onclick: () => start('stale') },
                                          `増えた表だけ探す（${stale}）`));
        btns.push(el('button', { class: 'btn btn--sm' + (st.exists && stale ? '' : ' btn--primary'), onclick: () => start('all') },
                     st.exists ? 'すべて探し直す' : '探す'));
        lines.push(el('div', { class: 'row', style: 'gap:8px' }, ...btns));
        showPanel('結合を探す', lines);
    }
    let discoverTimer = null;
    function showDiscoverProgress() {
        clearTimeout(discoverTimer);
        // 進み具合のパネルは、出ている間だけ描き直す。閉じられたり別の線を選ばれたりしたら戻さず、静かに待つ
        const mine = () => !panel.classList.contains('hidden') && panel.dataset.kind === 'discover';
        const progressPanel = (p) => showPanel('結合を探しています…', [
            el('div', { class: 'small' }, `${p.phase || ''} ${p.done ?? 0} / ${p.total ?? 0}`),
            el('div', { class: 'small muted mt' }, '閉じても裏で続きます。終わると知らせが出て、候補が赤い点線で重なります。')], { kind: 'discover' });
        progressPanel({});
        const tick = async () => {
            let st;
            try { st = await fetchJoinStatus(); } catch (e) { toast(e.message, 'err'); return; }
            const p = st.progress || {};
            if (st.running) {
                if (mine()) progressPanel(p);
                discoverTimer = setTimeout(tick, 1500);
                return;
            }
            if (p.error) {
                if (mine()) showPanel('結合を探す', [el('div', { class: 'alert alert--err small' }, `失敗しました: ${p.error}`)]);
                else toast(`結合を探すのに失敗しました: ${p.error}`, 'err', 9000);
                return;
            }
            await refreshSuggestions();
            showSug = true; syncSugBtn(); render(); setTimeout(fit, 20);
            const msg = p.message || `候補 ${suggestions.length} 件`;
            if (mine()) {
                showPanel('結合を探しました', [
                    el('div', { class: 'small' }, msg),
                    el('div', { class: 'small muted mt' }, '赤い点線が候補です。線をクリックすると根拠と推定した多重度を確かめて登録できます。')]);
            } else {
                toast(`結合を探しました: ${msg}`);
            }
        };
        discoverTimer = setTimeout(tick, 800);
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

    return { init, refit: fit, mutate, setUsage, setSuggestions, setJoinStatus, dropTable };
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

/** スクレイピングの設定ごとの数値（最小間隔・タイムアウト）を、その場で変える欄。 */

function scrapeNumber(j, key, label, unit, title) {
    const inp = el('input', {
        type: 'number', value: String(j[key]), style: 'width:70px',
        title,
        // 保存しても管理欄は描き直さない。描き直すと、続けて入力中のもう一方の欄が消える
        onchange: async ev => {
            const before = j[key];
            try {
                await api('/api/jobs/update', { id: j.id, [key]: ev.target.value });
                j[key] = ev.target.value;
                toast(`「${j.name}」の${label}を ${ev.target.value}${unit} にしました。`);
            } catch (e) {
                ev.target.value = String(before);       // 断られた値は元に戻す
                toast(e.message, 'err', 8000);
            }
        },
    });
    return el('label', { class: 'small muted', style: 'display:flex;align-items:center;gap:4px' },
        `${label}`, inp, unit);
}

function jobControls(j) {
    const scraper = j.source_kind === 'scraper';
    return [
        // リアルタイム更新の切替。追記のジョブは対象外（サーバ側でも弾かれる）
        j.mode_label === '追記' ? null : el('button', {
            class: 'btn btn--sm',
            title: scraper
                ? (j.realtime
                    ? '質問のたびに、前回の取得から最小間隔が経っていればスクリプトを実行し直しています。押すとやめます。'
                    : '質問のたびに、前回の取得から最小間隔が経っていればスクリプトを実行し直して答えるようにします。')
                : (j.realtime
                    ? '質問のたびに元ファイルの更新を確認して取り込み直しています。押すとやめます。'
                    : '質問のたびに元ファイルの更新を確認し、変わっていれば取り込み直してから答えるようにします。'
                      + 'ファイルが読めないときは前回取り込んだ内容で答えます。'),
            onclick: () => tryUpdate(j, { realtime: !j.realtime },
                j.realtime
                    ? `「${j.name}」のリアルタイム更新を止めました。`
                    : `「${j.name}」をリアルタイム更新にしました。質問のたびに元ファイルへ追随します。`),
        }, j.realtime ? 'リアルタイム中' : 'リアルタイムにする'),
        el('select', {
            style: 'width:130px',
            title: '更新の頻度',
            onchange: ev => tryUpdate(j, { interval: ev.target.value },
                `「${j.name}」を ${ev.target.value} に変更しました。`),
        }, MANAGE.intervals.map(i => el('option',
            { ...(i === j.interval_label ? { selected: 'selected' } : {}) }, i))),
        // スクレイピングだけ: 質問に応じた取り直しの最小間隔（全件入れ替えのみ）とタイムアウト
        (scraper && j.mode_label !== '追記')
            ? scrapeNumber(j, 'scrape_interval_minutes', '最小間隔', '分',
                '質問を受けたとき、前回の取得からこの分数が経っていれば取り直します。0 なら質問のたびに。')
            : null,
        scraper
            ? scrapeNumber(j, 'scrape_timeout_sec', 'タイムアウト', '秒',
                'スクリプト1回の実行にこれ以上かかったら打ち切ります。')
            : null,
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
            onclick: () => tryUpdate(j, { enabled: j.enabled === false },
                j.enabled === false
                    ? `「${j.name}」の自動更新を再開しました。`
                    : `「${j.name}」の自動更新を止めました。「再開」でいつでも戻せます。`),
        }, j.enabled === false ? '再開' : '停止'),
        el('button', {
            class: 'btn btn--sm btn--danger',
            title: '定期取り込みの設定だけを消します（テーブルと中のデータは残ります）。'
                   + 'このテーブルは自動更新されなくなります。',
            onclick: async () => {
                if (!confirm(`定期取り込み「${j.name}」の設定を削除しますか？\n`
                    + '（テーブルと中のデータは残ります）')) return;
                try {
                    await api('/api/jobs/delete', { id: j.id });
                    toast('定期取り込みの設定を削除しました。');
                } catch (e) { toast(e.message, 'err', 8000); }
                MANAGE.refresh();
            },
        }, '設定を削除'),
    ];
}

/** 設定の変更を送る。断られたら理由を出して、表示を実際の値に戻す（描き直す）。 */
async function tryUpdate(j, patch, okMessage) {
    try {
        await api('/api/jobs/update', { id: j.id, ...patch });
        toast(okMessage);
    } catch (e) { toast(e.message, 'err', 9000); }
    MANAGE.refresh();
}

/** 1件ぶんの定期取り込みの中身（取り込み元と更新のしかた）。 */

function jobDetail(j, withName) {
    const box = el('div', { style: 'margin-top:6px' });
    if (withName) {
        box.append(el('div', { style: 'font-weight:600;font-size:12.5px;margin-bottom:2px' },
            `${j.name}`,
            j.enabled === false ? el('span', { class: 'badge badge--warn' }, '停止中') : null));
    }
    if (j.source_kind === 'scraper') {
        box.append(
            kv('取り込み元', `スクレイピング（${j.source}）`, true),
            kv('取得ファイル', j.scrape_file || '（出来たファイルを使う）'),
            kv('最小間隔', j.mode === 'append' ? '（追記は定期実行のみ）' : `${j.scrape_interval_minutes} 分`),
            kv('タイムアウト', `${j.scrape_timeout_sec} 秒`));
    } else {
        box.append(
            kv('ファイル名', j.source_label ? j.source_label.split(/[\\/]/).pop() : '―', true),
            kv('フルパス', j.source));
    }
    box.append(
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
/* マイエージェント画面。描画アイテム（text/sql/table/chart/file/error）を組み立てて流す。 */

let currentChatId = window.CHAT_INIT.chatId || null;
let busy = false;
// 表示中のビューの世代。マイエージェントを切り替える（＝ログを描き直す）たびに進める。
// 送信処理は開始時の世代を覚えておき、届いた回答は世代が一致するときだけ描く。
// これが無いと、送信中に別のマイエージェントへ切り替えたとき、後から届いた回答が
// 関係ないマイエージェントの画面に紛れ込む。
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

/* --- パーソナライズ（利用者について、会話から自動で覚える） ------------------------
   保存はサーバが回答のあとに別スレッドで行う（end のあと数秒で増える）。ここは見せる・消す・止める。 */

let mem = window.CHAT_INIT.memory || { enabled: false, on: true, text: '', updated_at: '' };
let memTimers = [];                 // 取り直しの予約。次の質問が来たら前の予約は捨てる（二重に知らせない）

/* 回答のあと、サーバがパーソナライズを書き直していれば一言知らせる。書き直しは別スレッドなので、
   end の数秒あとに何回か見る。中身はメニューの「パーソナライズ」で見る。 */
function scheduleMemoryRefresh() {
    if (!mem.enabled || !mem.on) return;
    memTimers.forEach(clearTimeout);
    memTimers = [];
    const check = async () => {
        try {
            const r = await api('/api/memory', undefined, 'GET');
            if ((r.updated_at || '') === (mem.updated_at || '')) return false;
            const grew = (r.text || '').length > (mem.text || '').length;
            mem = { ...mem, ...r };
            toast((grew ? 'パーソナライズに書き足しました' : 'パーソナライズを書き直しました')
                  + '（メニューの「パーソナライズ」で見られます）。', 'ok', 7000);
            return true;
        } catch (_) { return true; }         // 取れないときは黙って諦める
    };
    memTimers.push(setTimeout(async () => {
        if (await check()) return;
        memTimers.push(setTimeout(async () => {
            if (await check()) return;
            memTimers.push(setTimeout(check, 15000));
        }, 7000));
    }, 3000));
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
            onclick: ev => {
                if (ev.target.closest('.histitem__del')) return;
                // 別のタブで消された会話を押すと api() が投げる。黙って止まらないよう受ける
                openChat(c.id).catch(e => { toast(e.message, 'warn'); refreshHistory(); });
            },
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
    // このマイエージェントの質問を送信中なら「考えています…」を出し直す
    // （開始時刻は busyStart から続き）。clearLog で表示ごと消えるため、
    // これが無いと切替後は待ち秒数が見えない。よそのマイエージェントの質問のときは
    // 出さない（無関係な画面にカウントが出るのは紛らわしいだけのため）。
    if (busy && busyChatId === id) setBusy(true);
    refreshHistory();
    scrollDown(true);
}

/* --- マイロボット（登録） -----------------------------------------------------
   気に入った処理の流れ（AIが呼んだ道具の列）に名前を付けて保存し、AIなしで再現する。
   登録は各発言の「ロボットにする」から。一覧と実行はメニューの「マイロボット」画面
   （robots.js。ダイアログの枠は window.ROBOT にある共通部品）。 */

/** 登録。会話から手順を取り出して見せ、名前・実行日で変わる値・定期実行・届け先を決めて保存する。
 *  「穴」（実行のたびに聞く値）は無い。日付らしい値は実行日から自動で決める（案A）。 */
async function registerRobot(upto) {
    if (!currentChatId) { toast('この会話はまだ保存されていません。', 'warn'); return; }
    if (busy) { toast('回答を待っているあいだは登録できません。', 'warn'); return; }
    // 押した時点の会話に固定する（応答待ちの間に別の会話を開いても、保存先がずれないように）
    const chatId = currentChatId;
    let r;
    try {
        r = await api('/api/robots/extract', { chat_id: chatId, upto });
    } catch (e) { toast(e.message, 'err', 8000); return; }
    if (!r.turns.length) {
        toast('ここまでのやり取りには、保存できる手順（SQLの実行・グラフ・ファイル作成など）がありません。', 'warn', 8000);
        return;
    }
    const sec = (title, ...kids) => el('div', { style: 'margin-top:14px' },
        el('div', { style: 'font-weight:600;font-size:13px;margin-bottom:4px' }, title), ...kids);

    // 1. 名前
    const name = el('input', { type: 'text', style: 'width:100%',
                               value: (r.title || '').slice(0, 40) || 'マイロボット' });

    // 2. 手順（畳んで確認。チェックを外した質問は入れない）
    const turnChecks = {};
    let nSteps = 0;
    const turnList = el('div', {}, ...r.turns.map(t => {
        const cb = el('input', { type: 'checkbox', checked: 'checked' });
        turnChecks[t.turn] = cb;
        nSteps += t.steps.length;
        return el('div', { class: 'robotturn' },
            el('label', { style: 'display:flex;gap:8px;align-items:flex-start;cursor:pointer' },
                cb, el('div', { class: 'grow' },
                    el('div', { style: 'font-weight:600' }, t.question || '（質問なし）'),
                    ...t.steps.map(s => el('div', { class: 'small robotstep' },
                        el('div', { style: 'display:flex;gap:6px;align-items:center' },
                            el('span', { class: 'badge' }, `手順${s.i + 1}`),
                            el('span', {}, s.label)),
                        el('div', { class: 'mono muted robotstep__sum' }, s.summary))))));
    }));
    const stepsBox = el('details', { class: 'acc', ...(r.turns.length > 1 ? {} : {}) },
        el('summary', { class: 'small', style: 'cursor:pointer' },
           `${r.turns.length} つの質問・${nSteps} 手順（開いて確認。チェックを外した質問は入れません）`),
        el('div', { class: 'acc__body' }, turnList));

    // 3. 実行日で変わる値（日付らしい値ごとに1行。同じ値はまとめる）
    const dateRows = new Map();                  // 値 → {g, sel, prev, place}
    const dateBody = el('tbody');
    const dateNote = el('div', { class: 'small muted', style: 'margin-top:4px' });
    function addDateRow(g) {
        if (dateRows.has(g.value)) {
            const row = dateRows.get(g.value);
            (g.places || []).forEach(p => { if (row.g.places.indexOf(p) < 0) row.g.places.push(p); });
            row.place.textContent = row.g.places.join('、');
            return;
        }
        const sel = el('select', { style: 'max-width:200px' }, ...g.options.map(o =>
            el('option', { value: o.mode, ...(o.mode === g.suggested ? { selected: 'selected' } : {}) }, o.label)));
        const prev = el('span', { class: 'mono small' });
        const syncPrev = () => {
            const o = g.options.find(x => x.mode === sel.value) || g.options[0];
            prev.textContent = sel.value === 'fixed' ? '（変わりません）' : `今日なら ${o.preview}`;
        };
        sel.addEventListener('change', syncPrev);
        syncPrev();
        const place = el('td', { class: 'small muted' }, (g.places || []).join('、'));
        const tr = el('tr', {},
            el('td', { class: 'mono small', style: 'white-space:nowrap' }, g.value),
            place, el('td', {}, sel), el('td', {}, prev));
        dateBody.append(tr);
        dateRows.set(g.value, { g, sel, prev, place, tr });
        syncDateNote();
    }
    function syncDateNote() {
        const n = [...dateRows.values()].filter(x => x.sel.value !== 'fixed').length;
        dateNote.textContent = n
            ? `${n} 件を実行日に合わせます。実行のたびに「先月＝2026-08 として動きました」のように会話の先頭に残ります。`
            : '全部「固定のまま」です。毎回同じ期間の結果になります（定期実行なら、たいてい「先月」などにします）。';
    }
    dateBody.addEventListener('change', syncDateNote);
    (r.dates || []).forEach(addDateRow);
    const datesSec = sec('実行日で変わる値',
        el('div', { class: 'small muted', style: 'margin-bottom:6px' },
           '手順の中の日付らしい値です。「先月」などにすると、実行のたびに実行日から計算して差し込みます（AIは呼びません）。'),
        el('div', { class: 'tablewrap', style: 'max-height:260px' },
            el('table', { class: 'data' },
                el('thead', {}, el('tr', {}, el('th', { style: 'width:150px' }, '値'), el('th', {}, 'どこに'),
                                       el('th', { style: 'width:210px' }, '扱い'), el('th', { style: 'width:170px' }, '例'))),
                dateBody)),
        dateNote);
    const syncDatesSec = () => datesSec.classList.toggle('hidden', !dateRows.size);
    syncDatesSec();
    syncDateNote();

    // 4. 定期実行。「先月」を使うなら毎月1日、「前日」なら毎日を初期値に
    const modes = [...dateRows.values()].map(x => x.sel.value);
    let sugSched = modes.some(m => m.startsWith('last_month')) ? { kind: 'monthly_day', day: 1, time: '08:00' }
        : modes.some(m => m === 'yesterday' || m === 'today') ? { kind: 'daily', time: '08:00' }
        : modes.some(m => m.startsWith('last_week')) ? { kind: 'weekly', weekday: 0, time: '08:00' }
        : {};
    {   // 管理者の最低間隔より短い初期値は付けない（保存で断られるだけになる）
        const floorMin = Number(window.CHAT_INIT.robotMinIntervalHours || 0) * 60;
        const gap = sugSched.kind ? window.ROBOT.scheduleGap(sugSched.kind, 1) : 0;
        if (gap > 0 && floorMin > 0 && gap < floorMin) sugSched = {};
    }
    const notifyBox = el('div', { class: 'hidden', style: 'margin-top:8px' });
    let syncDeliver = () => {};
    const sched = window.ROBOT.scheduleOptions({ schedule: sugSched, holes: [] }, window.CHAT_INIT.robotSchedVocab,
        () => { notifyBox.classList.toggle('hidden', sched.value().kind === 'manual'); syncDeliver(); }, false,
        { minIntervalHours: window.CHAT_INIT.robotMinIntervalHours, schedulerOn: window.CHAT_INIT.schedulerOn });
    notifyBox.classList.toggle('hidden', sched.value().kind === 'manual');

    // 5. 届け先
    const folder = r.has_file_steps ? window.ROBOT.folderOptions(r) : null;
    const mailEdits = {};                        // 手順の番号 → {subject, body}
    const mailCb = el('input', { type: 'checkbox', checked: 'checked' });
    const mailTable = el('input', { type: 'checkbox', checked: 'checked' });
    const numbersIn = (text) => {
        let t = String(text || '');
        // 長い値から除く（'2026-08' を先に除くと '2026-08-31' の '31' が数字として残る）
        [...dateRows.keys()].sort((a, b) => b.length - a.length).forEach(value => { t = t.split(value).join(' '); });
        return [...new Set((t.match(/[0-9][0-9,]*(?:\.[0-9]+)?/g) || []).map(x => x.replace(/,/g, '')))];
    };
    let detectTimer = null;
    const mailBoxes = (r.mail_steps || []).map(ms => {
        const subject = el('input', { type: 'text', value: ms.subject || '', style: 'width:100%' });
        const body = el('textarea', { rows: 6, style: 'width:100%;font-family:inherit;font-size:13px' });
        body.value = ms.body || '';
        const numNote = el('div', { class: 'small', style: 'margin-top:4px;color:var(--warn)' });
        const syncNums = () => {
            const nums = numbersIn(subject.value + '\n' + body.value);
            if (!nums.length) { numNote.textContent = ''; numNote.classList.add('hidden'); return; }
            numNote.classList.remove('hidden');
            const marked = nums.map(n => (r.result_numbers || []).indexOf(n) >= 0 ? `${n}（手順の結果の値）` : n);
            numNote.textContent = `本文に数字があります: ${marked.join('、')}。本文は登録時の文章のまま送られるので、`
                + '数字を書いている場合は毎回同じ文になります。数字は本文に書かず、下の「結果の表を付ける」に任せてください。';
        };
        const detect = () => {
            clearTimeout(detectTimer);
            detectTimer = setTimeout(async () => {
                try {
                    const text = subject.value + '\n' + body.value;
                    const d = await api('/api/robots/detect', { text, base: r.base || '' });
                    const place = `手順${ms.i + 1} メール`;
                    (d.dates || []).forEach(g => addDateRow({ ...g, places: [place] }));
                    // メールにしか無かった値が本文から消えたら、行も消す（数と保存の内容をいまの本文に合わせる）
                    [...dateRows.entries()].forEach(([value, row]) => {
                        const mailOnly = row.g.places.every(p => p === place);
                        if (mailOnly && text.indexOf(value) < 0) { row.tr.remove(); dateRows.delete(value); }
                    });
                    syncDatesSec(); syncDateNote(); syncNums();
                } catch (_) { /* 取り直せなくても保存時にサーバが見る */ }
            }, 500);
        };
        const onEdit = () => { mailEdits[ms.i] = { subject: subject.value, body: body.value }; syncNums(); detect(); };
        subject.addEventListener('input', onEdit);
        body.addEventListener('input', onEdit);
        syncNums();
        return el('div', { class: 'robotturn', style: 'margin-top:6px' },
            el('div', { class: 'small muted' }, `手順${ms.i + 1} のメール（宛先: ${(ms.to || []).join(', ') || '—'}）。件名と本文はここで直せます。`),
            el('label', { class: 'field', style: 'margin-top:6px' }, '件名'), subject,
            el('label', { class: 'field', style: 'margin-top:6px' }, '本文'), body,
            numNote);
    });
    const notify = el('input', { type: 'text', style: 'width:100%;max-width:420px',
                                 placeholder: '例: yamada@example.co.jp（カンマ区切りで複数可）' });
    const notifyPick = window.ROBOT.mailPicker(notify, window.CHAT_INIT.mailAllowed || []);
    notifyBox.append(el('label', { class: 'field' }, '定期実行が失敗したときに知らせるメール（任意）'), notify, notifyPick.node,
        el('div', { class: 'small muted', style: 'margin-top:3px' },
           '定期実行は無人で動くので、入れておくと失敗に気づけます。管理者が「メール設定」で許可したアドレスだけ指定できます（入力すると候補が出ます）。'));
    const deliver = sec('届け先',
        folder ? el('div', { class: 'small muted' },
                    'フォルダ出力（実行のたびに、出力先フォルダの自分の名前のフォルダへ置くか）'
                    + (window.CHAT_INIT.folderOut ? '' : '　※いまは出力先フォルダが未設定です。管理者が設定すると効きます')) : null,
        folder ? folder.node : null,
        r.has_mail_steps ? el('div', { class: 'robotturn', style: 'margin-top:8px' },
            el('label', { style: 'display:flex;align-items:center;gap:6px;cursor:pointer' }, mailCb,
               el('span', {}, '実行のたびに、作ったメールの下書きをそのまま送る（確認なし）')),
            el('div', { class: 'small muted', style: 'margin:2px 0 0 22px' },
               '宛先の許可・件数の上限・テスト送信モードは「メール設定」のとおりです。外すと、下書きが会話に出るだけで送りません。'),
            el('label', { style: 'display:flex;align-items:center;gap:6px;cursor:pointer;margin-top:6px' }, mailTable,
               el('span', {}, '結果の表を本文の末尾に付ける（直前の手順の表の先頭20行。それより多いぶんは添付を見てもらう）')),
            ...mailBoxes) : null,
        notifyBox);

    // 届け先に出すものが何も無ければ（ファイルもメールも無く、手動のみ）節ごと出さない
    syncDeliver = () => deliver.classList.toggle('hidden', !folder && !r.has_mail_steps && sched.value().kind === 'manual');
    syncDeliver();
    const body = el('div', {},
        el('label', { class: 'field' }, '名前'), name,
        sec('手順', stepsBox),
        datesSec,
        sec('定期実行', el('div', { class: 'small muted', style: 'margin-bottom:4px' },
            '決めた時刻にサーバが自動で動かします。「手動のみ」なら、マイロボットの画面の「いま試す」を押したときだけ動きます。'),
            el('div', { class: 'robotturn' }, sched.node)),
        deliver);
    const save = el('button', { class: 'btn btn--primary', onclick: async () => {
        const turns = Object.entries(turnChecks).filter(([, cb]) => cb.checked).map(([t]) => Number(t));
        const dates = [...dateRows.values()].map(x => ({ value: x.g.value, mode: x.sel.value }));
        save.disabled = true;
        try {
            const res = await api('/api/robots/save', { chat_id: chatId, upto, name: name.value, turns, dates,
                                                       mail_edits: mailEdits, mail_table: mailTable.checked,
                                                       schedule: sched.value(), mail_auto: mailCb.checked,
                                                       notify_to: sched.value().kind === 'manual' ? '' : notify.value,
                                                       ...(folder ? folder.value() : {}) });
            toast(`マイロボット「${res.robot.name}」を保存しました（${res.robot.n_steps}手順）。`
                + 'メニューの「マイロボット」で確かめられます。', 'ok', 9000);
            close();
        } catch (e) { toast(e.message, 'err', 9000); save.disabled = false; }
    } }, '保存する');
    const close = window.ROBOT.modal('マイロボットにする', body, [save,
        el('span', { class: 'small muted' }, 'AIの説明文は保存されません。道具の列だけを再現します。')], { wide: true });
    name.focus(); name.select();
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
    fbTurn = null;               // 前の会話の「この答えはどうだったか」を持ち越さない
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
                    el('button', { class: 'btn btn--sm', id: 'erFull' }, '全画面'),
                    el('button', { class: 'btn btn--sm', id: 'erArrange',
                                   title: '表を関連にそって並べ直します（この画面では保存されません）' }, '整列')),
                el('div', { class: 'er__viewport', id: 'erViewport' },
                    svgEl,
                    el('div', { class: 'er__world', id: 'erWorld' })),
                el('div', { class: 'er__legend' },
                    el('b', {}, 'IPA表記'), '　下線＝主キー　線の両端の 0..1・1・0..*・1..*＝多重度　',
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

/** カタログに登録できる人か（管理者、または管理者メニュー → 画面 の一覧にある人）。サーバが決めて渡す。 */
function canContribute() {
    return !!(window.CHAT_INIT || {}).canContribute;
}

/** 登録カードの末尾の行。登録できない人には、ボタンの代わりに一言だけ置く（カード自体は出す）。 */
function contribRow(note, btn) {
    if (!canContribute()) {
        return el('div', { class: 'mailcard__row' },
            el('span', { class: 'small muted grow' },
                '登録できるのは管理者と、管理者が決めた人だけです。登録したい内容は管理者に伝えてください。'));
    }
    return el('div', { class: 'mailcard__row', style: 'justify-content:flex-end' },
        el('span', { class: 'small muted grow' }, note), btn);
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
    card.append(contribRow('登録すると全員のAIがこの定義に従います。登録した人と変更の記録は残ります。', btn));
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
    card.append(contribRow('登録すると似た質問へのAIのお手本になります。登録した人と変更の記録は残ります。', btn));
    return card;
}

/* --- 社内文書の検索結果（出典） -------------------------------------------------
   回答の中の [出典n] と突き合わせられるように、番号・ナレッジベース名・
   ファイル名・本文の抜粋を並べる。AIの回答を人が検証できることが目的なので、
   折りたたんで隠さず、行の抜粋だけを畳んでおく（クリックで全文）。 */

/* --- この答えはどうだったか ------------------------------------------------------
   応えられなかった質問は、失敗としてはどこにも残らない。無い表について聞かれると
   AIは「そのデータはありません」と答えて正常に終わるので、記録の上では
   「成功した1問で終わった会話」になり、満足した人と見分けがつかない。
   だからここで1回だけ聞く。

   聞くのは「どうだったか」の1問だけ。選択肢は3つで、そのまま3つの直し方に対応する。
     これでいい           → 例文の候補
     数字が違う/書いてある… → カタログか文書を直す
     知りたいことと違う    → データか文書を足す
   ボタンを4つ並べて2つの軸を混ぜない（非IT部門の人は読み分けられない）。 */
let fbTurn = null;

function fbStart(turn) {
    fbTurn = { turn, chatId: currentChatId, usedSql: false, usedDoc: false,
               node: null, ask: null, sent: false, busy: false };
}

/** 真ん中のボタンの文言は、その回答が何で答えたかで変える。
 *  表なら「数字が違う」、社内文書なら「書いてあることと違う」、両方なら「内容が違う」。 */
function fbMidLabel(st) {
    if (st.usedSql && st.usedDoc) return '内容が違う';
    if (st.usedDoc) return '書いてあることと違う';
    if (st.usedSql) return '数字が違う';
    return '内容が違う';          // 表も文書も使わずに答えた回（「データがありません」など）
}

/** 「数字が違う」のあとに1行だけ聞く。任意。
 *  値が入ると、苦情が検算のもとに変わる（管理者がSQLを既知の値と突き合わせられる）。 */
function fbFollowLabel(st) {
    if (st.usedDoc && !st.usedSql) return '正しくはどの文書に書いてありますか（任意）';
    if (st.usedSql) return '正しい値が分かれば教えてください（任意）';
    return 'どこが違いましたか（任意）';
}

/** 評価を送る。**押した行の turn** を送る（いまの turn ではない）。
 *  ここを取り違えると、前の質問の行を押したときに別の質問の評価として残る。
 *  会話IDも、その行を作ったときのものを使う（途中で会話を切り替えても正しく残る）。 */
async function fbSend(st, kind, detail) {
    if (!st || st.turn === undefined || st.turn === null) return false;
    if (st.busy) return false;                 // 連打で同じものを2回送らない
    st.busy = true;
    try {
        await api('/api/feedback', { chat_id: st.chatId || currentChatId, turn: st.turn,
                                     kind, detail: detail || '' });
        return true;
    } catch (e) {
        toast(e.message, 'warn');
        return false;
    } finally {
        st.busy = false;
    }
}

/** 回答の下に1行だけ置く。答えが増えるたびに末尾へ動かす（turn の最後に居させる）。 */
function feedbackRow() {
    if (!fbTurn || fbTurn.turn === undefined || fbTurn.turn === null) return;
    if (fbTurn.sent) return;                  // もう押された turn には出し直さない
    if (fbTurn.node) fbTurn.node.remove();
    const st = fbTurn;
    const row = el('div', { class: 'fbrow' }, el('span', {}, 'この答えは'));
    const done = (msg) => {
        st.sent = true;
        row.replaceChildren(el('span', { class: 'fbrow__done' }, msg));
        if (st.ask) st.ask.remove();
    };
    const ask = (kind) => {
        if (st.ask) st.ask.remove();          // 2回押しても欄は1つにする
        const inp = el('input', { type: 'text', placeholder: '' });
        const send = async (b, value) => {
            b.disabled = true;                // 応答を待つあいだの連打を止める
            if (await fbSend(st, kind, value)) done('ありがとうございます。管理者に伝わりました。');
            else b.disabled = false;
        };
        const box = el('div', { class: 'fbask' },
            el('b', {}, fbFollowLabel(st)),
            el('div', { class: 'row' }, inp,
                el('button', { class: 'btn btn--sm btn--primary',
                    onclick: ev => send(ev.currentTarget, inp.value) }, '送る'),
                el('button', { class: 'btn btn--sm',
                    onclick: ev => send(ev.currentTarget, '') }, '分からない')));
        st.ask = box;
        row.after(box);
        inp.focus();
    };
    const btn = (label, fn) => el('button', { class: 'fbrow__b', onclick: fn }, label);
    const one = (kind, msg) => async (ev) => {
        ev.currentTarget.disabled = true;     // 応答を待つあいだの連打を止める
        if (await fbSend(st, kind, '')) done(msg);
        else ev.currentTarget.disabled = false;
    };
    row.append(
        btn('これでいい', one('ok', 'ありがとうございます。例文の候補にします。')),
        btn(fbMidLabel(st), () => ask('wrong')),
        btn('知りたいことと違う', one('off_target', 'ありがとうございます。管理者に伝わりました。')));
    st.node = row;
    // その質問の最後の吹き出しの中に入れる。#logInner に直に足すと、
    // このあと道具の結果が来たときに、行がその上へ取り残される
    (slot('assistant') || $('#logInner')).append(row);
}

/** AIが「答えきれなかった」と申告したとき。記録はサーバ側で済んでいるので、
 *  ここは本人に見せて、要らなければ取り消せるようにするだけ。 */
/** 種別ごとの聞き方。語尾を機械的に落とすと「この説明が足りないを」のような文になるので、
 *  そのまま文になる言い方を種別ごとに持つ。 */
const GAP_ASK = {
    data: 'このデータがほしい、と管理者に伝えますか？',
    doc: 'この文書がほしい、と管理者に伝えますか？',
    feature: 'この機能がほしい、と管理者に伝えますか？',
    explain: 'この説明が足りない、と管理者に伝えますか？',
};

function gapCard(item) {
    const st = fbTurn;                        // この回の turn を掴んでおく
    const box = el('div', { class: 'gapcard' });
    box.append(el('b', {}, GAP_ASK[item.gap_kind] || '足りないものを、管理者に伝えますか？'),
               el('div', { class: 'gapcard__what' }, item.what || ''));
    const foot = el('div', { class: 'row', style: 'gap:7px' });
    const close = (msg) => box.replaceChildren(el('span', { class: 'small muted' }, msg));
    const pick = (kind, msg) => async (ev) => {
        ev.currentTarget.disabled = true;     // 応答を待つあいだの連打を止める
        if (await fbSend(st, kind, item.what || '')) close(msg);
        else ev.currentTarget.disabled = false;
    };
    foot.append(
        el('button', { class: 'btn btn--sm btn--primary',
                       onclick: pick('gap_confirm', '管理者に伝えました。') }, '伝える'),
        el('button', { class: 'btn btn--sm',
                       onclick: pick('gap_dismiss', '伝えませんでした。') }, '伝えない'));
    box.append(foot);
    return box;
}


/* --- 会話の中の枠を畳む ----------------------------------------------------------
   SQLの枠・社内文書の検索・登録の提案カードは、答えの上に積まれて画面を食う。
   管理者が「畳む」と決めた種類は、見出し1行の details にして、押した人にだけ開く。
   畳んでも消さない（根拠を辿れないと意味がない）。設定は CHAT_INIT.fold で来る。 */
function foldOn(key) {
    return !!(((window.CHAT_INIT || {}).fold || {})[key]);
}

/** 道具の枠。head は見出しの中身（配列）、あとは本体。畳む設定なら details にする。 */
function toolBlock(foldKey, head, ...parts) {
    if (!foldOn(foldKey)) {
        return el('div', { class: 'toolblock' }, el('div', { class: 'toolblock__head' }, ...head), ...parts);
    }
    return el('details', { class: 'toolblock toolblock--fold' },
              el('summary', { class: 'toolblock__head' }, ...head), ...parts);
}

/** 自前の枠を持つカード（提案カード）を、畳む設定のときだけ details で包む。 */
function foldCard(foldKey, head, card) {
    if (!foldOn(foldKey)) return card;
    return el('details', { class: 'toolblock toolblock--fold' },
              el('summary', { class: 'toolblock__head' }, ...head),
              el('div', { class: 'toolblock__inner' }, card));
}

/** 失敗が出たら、その原因になったSQLの枠を開く。原因を見に来る場所なので、畳んだままにしない。
 *  失敗の項目には call_id（どの道具の呼び出しか）が付いて来る。付いていない古い会話では、
 *  同じ回答の中で直前に置かれたSQLの枠だけを開く（別の質問のSQLや、SQL以外の失敗では開かない）。 */
function openFailedSql(item, body) {
    let target = null;
    if (item.call_id) {
        target = $$('#logInner details.toolblock--fold').find(d => d.dataset.callId === String(item.call_id));
    } else {
        const last = body.lastElementChild;      // 失敗の表示を足す前の、直前の要素
        if (last && last.matches('details.toolblock--fold') && last.querySelector('pre.mono')) target = last;
    }
    if (target) target.open = true;
}

/** 提案カードの「新規登録／既存」の印。畳んだ見出しにも出す（開かなくても分かるように）。 */
function proposalBadge(item, existsText) {
    return el('span', { class: 'badge' + (item.exists ? ' badge--warn' : ' badge--ok') },
              item.exists ? existsText : '新規登録');
}

/** 回答の本文に出てきた出典番号。半角・全角どちらの括弧でも拾う。
 *  括弧無しの「出典15」まで拾うと、「出典が15件」のような文まで数えてしまうので取らない。 */
function citedNumbers(text) {
    const out = new Set();
    // [出典1、3] のように1つの括弧に複数入ることがあるので、括弧の中の数字を全部拾う。
    // 括弧の無い「出典15」は拾わない（「出典が15件」のような文まで数えてしまうため）
    String(text || '').replace(/[\[［]\s*出典[^\]］]*/g, (block) => {
        String(block).replace(/\d+/g, (n) => { out.add(String(Number(n))); return ''; });
        return '';
    });
    return out;
}

/** まだ答え合わせをしていない出典カードに、引用された番号を教えて開き直す。
 *  出典番号は質問ごとに1から振り直されるので、古いカードに当てないよう
 *  「pending のものだけ」を対象にする（済んだカードは二度と触らない）。 */
function revealCitedSources(text) {
    const nums = [...citedNumbers(text)].join(',');
    document.querySelectorAll('.srcs[data-fold="pending"]').forEach(list => {
        list.dataset.fold = 'done';
        list.dataset.cited = nums;
        if (list.syncFold) list.syncFold();
    });
}

function sourcesCard(item) {
    const sources = item.sources || [];
    const block = toolBlock('fold_sources', [
        icon('book', 'icon--sm'),
        el('span', {}, '社内文書の検索'),
        el('span', { class: 'muted small' }, `— 「${item.query}」`),
        el('div', { class: 'spacer' }),
        el('span', { class: 'badge' }, `${sources.length}件`)]);

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
        const rows = sources.map(s => {
            // サーバが送ってくるのは先頭だけ（全文ではない）。
            // 「全文」と書くと、ここに無い＝文書に無い、と読まれてしまう
            // 押しても何も起きないので、押す場所にはしない。
            // 抜粋の続き（200字の先）はそもそも画面に来ていないため、
            // どう押しても出せない。原本はファイル名から当たってもらう。
            const cut = s.excerpt_cut;
            const row = el('div', { class: 'src' },
                el('div', { class: 'src__where' },
                    el('span', { class: 'src__no' }, `[出典${s.index}]`),
                    el('span', {}, s.knowledge_base),
                    s.file_path ? el('span', { class: 'muted' }, ` / ${s.file_path}`) : null,
                    cut ? el('span', { class: 'small muted' },
                            ` （先頭${s.excerpt_chars || 200}字）`) : null),
                el('div', { class: 'src__text' }, (s.excerpt || '') + (cut ? '…' : '')));
            row.dataset.no = String(s.index);
            return row;
        });
        // 最初はどれが引用されるか分からないので、全部畳んでおく（pending）。
        // 回答の本文が出そろった時点で revealCitedSources が引用番号を入れて開き直す。
        const list = el('div', { class: 'srcs' }, rows);
        list.dataset.fold = 'pending';
        const more = el('button', { class: 'srcs__more' });
        const sync = () => {
            const cited = (list.dataset.cited || '').split(',').filter(Boolean);
            const all = list.dataset.open === '1';
            let hidden = 0;
            rows.forEach(r => {
                const on = all || cited.indexOf(r.dataset.no) >= 0;
                r.hidden = !on;
                if (!on) hidden++;
            });
            // hidden 属性は .srcs の display:flex に負けるので、クラスで消す
            list.classList.toggle('hidden', hidden === rows.length);
            more.hidden = !all && !hidden;
            foot.classList.toggle('hidden', more.hidden);   // 空の帯だけ残さない
            more.textContent = all ? '引用されなかった分を畳む'
                : (list.dataset.fold === 'pending' ? `見つかった ${hidden} 件を見る`
                                                   : `引用されなかった ${hidden} 件も見る`);
        };
        more.addEventListener('click', () => {
            list.dataset.open = list.dataset.open === '1' ? '' : '1';
            sync();
        });
        const foot = el('div', { class: 'toolblock__foot' }, more);
        list.syncFold = sync;
        sync();
        block.append(list, foot);
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
        fbStart(item.turn);                  // この質問ぶんの「どうだったか」を始める
        body.append(userTurn(item));
    } else if (item.kind === 'text') {
        body.append(el('div', { html: `<p>${mdToHtml(item.content)}</p>` },
                      catalogLinks(item.tables)));
        revealCitedSources(item.content);     // この本文が根拠にした出典だけを開く
        feedbackRow();                        // 「この答えはどうだったか」を末尾に置き直す
    } else if (item.kind === 'sql') {
        const block = toolBlock('fold_sql',
            [icon('table', 'icon--sm'), el('span', {}, item.label || item.tool),
             item.purpose ? el('span', { class: 'muted small' }, `— ${item.purpose}`) : null],
            el('pre', { class: 'mono' }, item.sql),
            // SQLを読めない人向けの解説。AIが書いたものなので、根拠はSQL本体で確かめられる
            item.explanation
                ? el('div', { class: 'toolblock__note' },
                    el('b', {}, 'このSQLがしていること'),
                    el('div', { style: 'white-space:pre-wrap;margin-top:3px' }, item.explanation))
                : null);
        if (item.call_id) block.dataset.callId = String(item.call_id);   // 失敗の項目から辿るため
        if (fbTurn) fbTurn.usedSql = true;
        const links = catalogLinks(item.tables);
        {
            const foot = el('div', { class: 'toolblock__foot toolblock__foot--judge' });
            // 取り方が合っているかは、解説を読んだ人にしか判断できない。
            // 押せる人を絞るのではなく、解説のすぐ下に置いて目に入るようにする。
            // 「合っている」は、そのまま例文にしてよいという評価と同じもの。
            // 見た目は回答の下の「この答えは」と同じ（.fbrow）。右に寄せるのは CSS 側。
            const judge = el('div', { class: 'fbrow' }, el('span', {}, 'この取り方は'));
            const sqlSt = fbTurn;             // このSQLが出た回の turn を掴んでおく
            const pick = (kind, msg) => async (ev) => {
                ev.currentTarget.disabled = true;   // 応答を待つあいだの連打を止める
                if (await fbSend(sqlSt, kind, item.sql || '')) {
                    judge.replaceChildren(el('span', { class: 'small fbrow__done' }, msg));
                } else {
                    ev.currentTarget.disabled = false;
                }
            };
            judge.append(
                el('button', { class: 'fbrow__b',
                    onclick: pick('sql_ok', 'ありがとうございます。例文の候補にします。') }, '合っている'),
                el('button', { class: 'fbrow__b',
                    onclick: pick('sql_ng', 'ありがとうございます。管理者に伝わりました。') }, '合っていない'));
            foot.append(judge);
            if (item.question && canContribute()) {
                // 直接保存ではなくAIに頼む。AIが内容の日本語説明と実データ付きの
                // 登録カードを出し、そこで確定する（何が登録されるか見えるように）
                // 登録できない人（管理者メニュー → 画面 の一覧に無い人）には出さない
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
        // フォルダへの保存の状態。道具が保存済みならその場所、失敗なら理由。
        // どちらでもなく出力先が使えるなら「フォルダに保存」ボタン（AIは呼ばない）
        const savedLine = (p, replaced) => el('div', { class: 'small', style: 'margin-top:3px;display:flex;gap:4px;align-items:center' },
            icon('folder', 'icon--sm'), 'フォルダに保存済み: ', el('span', { class: 'mono' }, p),
            replaced ? el('span', { class: 'muted' }, '（前のファイルを置き換えました）') : null);
        const status = item.saved_to ? savedLine(item.saved_to, item.replaced)
            : (item.save_error ? el('div', { class: 'small', style: 'margin-top:3px;color:var(--err)' },
                                     `フォルダへの保存は失敗: ${item.save_error}`) : null);
        const saveBtn = (item.url && !item.saved_to && window.CHAT_INIT.folderOut)
            ? el('button', {
                class: 'btn btn--sm',
                title: '出力先フォルダの中の、自分の名前のフォルダにこのファイルを置きます',
                onclick: async ev => {
                    ev.target.disabled = true;
                    try {
                        const r = await api('/api/file/save-to-folder', { token: item.url.split('/').pop() });
                        item.saved_to = r.path;
                        ev.target.replaceWith(el('span'));
                        info.append(savedLine(r.path, r.replaced));
                        toast(`フォルダに保存しました: ${r.path}`, 'ok', 8000);
                    } catch (e) { toast(e.message, 'err', 9000); ev.target.disabled = false; }
                },
            }, 'フォルダに保存') : null;
        const info = el('div', { class: 'grow' },
            el('div', { class: 'name' }, item.filename),
            el('div', { class: 'small muted' },
                item.note || (item.sheets || []).map(s => `${s.name}: ${s.total}行`).join('/ ')),
            status);
        const card = el('div', { class: 'filecard' },
            icon('file', 'icon--lg'),
            info,
            saveBtn,
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
        body.append(foldCard('fold_proposals',
            [icon('catalog', 'icon--sm'), el('span', {}, '用語集への登録の提案'),
             item.term ? el('span', { class: 'muted small' }, `— ${item.term}`) : null,
             el('div', { class: 'spacer' }), proposalBadge(item, '既存の定義を変更')],
            glossaryCard(item)));
    } else if (item.kind === 'example_proposal') {
        body.append(foldCard('fold_proposals',
            [icon('catalog', 'icon--sm'), el('span', {}, '例文への登録の提案'),
             item.question ? el('span', { class: 'muted small' }, `— ${String(item.question).slice(0, 40)}`) : null,
             el('div', { class: 'spacer' }), proposalBadge(item, '既存の例文を更新')],
            exampleCard(item)));
    } else if (item.kind === 'sources') {
        if (fbTurn) fbTurn.usedDoc = true;
        body.append(sourcesCard(item));
    } else if (item.kind === 'gap') {
        body.append(gapCard(item));
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
        openFailedSql(item, body);            // 失敗の原因を見に来る場所なので、畳んだままにしない
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
        }, icon('tool', 'icon--sm'), el('span', { class: 'turn__btn__t' }, '書き直す')),
        // ここまでの流れ（AIが使った道具の列）を保存して、AIなしで繰り返せるようにする
        el('button', {
            class: 'turn__btn', title: 'ここまでのやり取りでAIが使った道具の列に名前を付けて保存し、'
                + 'AIなしで同じ処理を繰り返せるようにします',
            onclick: () => registerRobot(item.turn),
        }, icon('spark', 'icon--sm'), el('span', { class: 'turn__btn__t' }, 'ロボットにする')));
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
        if (send) scheduleMemoryRefresh();        // 書き直して送ったときは、サーバがパーソナライズを抜き出す
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
    if (item.sent_at) {
        // マイロボットの「実行のたびに送る」で、もう送ってある
        foot.append(el('span', { class: 'small' }, `${p.dry_run ? '確認しました（テスト送信モード・未送信）' : '送信済み'}（${String(item.sent_at).replace('T', ' ')}・マイロボットの自動送信）`));
    } else if ((p.errors || []).length) {
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
// マイエージェント切替でログを描き直すと要素ごと消えるため。戻ってきたときに
// この値から表示を作り直せば、経過秒数は数え直しにならず続きから出る。
let busyStart = null;
let busyLabel = '';
let busyChatId = null;   // いま回答を待っている質問が、どのマイエージェントのものか

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
    busyChatId = currentChatId;             // この質問が属するマイエージェント（新規なら null）
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
            // 途中で他のマイエージェントを見て戻ってきた。完成形を読み直して揃える
            openChat(r.chat_id);
        }
        refreshHistory();
        scheduleMemoryRefresh();
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
        // 本文が空のまま答え合わせをしない。closeText は道具の結果が来るたびに呼ばれるので、
        // 空で通すと「まだ引用されていない出典カード」を引用ゼロで確定させてしまう
        if (buf.trim()) {
            revealCitedSources(buf);
            feedbackRow();                        // 答えが出そろってから1行置く
        }
        node = null; buf = '';
    };

    const handle = (event, data) => {
        if (event === 'end') {
            if (viewToken === myView) {
                // 送信したときの画面のまま。ライブで全部描けているので何もしない
                currentChatId = data.chat_id || currentChatId;
            } else if (missed && data.chat_id && currentChatId === data.chat_id) {
                // 途中で他のマイエージェントを見て戻ってきた。描き逃した分があるので、
                // 保存済みの完成形（サーバは end を送る前に保存している）を読み直す
                openChat(data.chat_id);
            }
            refreshHistory();
            scheduleMemoryRefresh();
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

/* マイエージェントから「カタログで説明を書く」で来たとき、そのテーブルを開いて光らせる。
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
   食い違っていればマイエージェントに警告が出る（verify.py）。ここはその管理画面。 */

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

/* --- ビューの名前: まとまり（プルダウン）＋ 名前 -------------------------------------
   取り込み画面と同じ形。まとまりは既存の表・ビューの接頭辞から拾い、「＋ 新しいまとまりを作る」で足せる。 */
function viewGroups() {
    const names = (CAT.tables || []).map(t => t.name).concat((CAT.views || []).map(v => v.name));
    return [...new Set(names.map(n => n.split('__')[0]).filter(Boolean))].sort((a, b) => a.localeCompare(b, 'ja'));
}

function fillViewGroups(selected) {
    const sel = $('#viewGroup');
    if (!sel) return;
    const groups = viewGroups();
    sel.replaceChildren(
        el('option', { value: '' }, 'まとまりを選ぶ'),
        ...groups.map(g2 => el('option', { value: g2, ...(g2 === selected ? { selected: 'selected' } : {}) }, g2)),
        el('option', { value: '__new__', ...(selected && !groups.includes(selected) ? { selected: 'selected' } : {}) }, '＋ 新しいまとまりを作る'));
    $('#viewGroupNew').classList.toggle('hidden', sel.value !== '__new__');
    if (selected && !groups.includes(selected)) $('#viewGroupNew').value = selected;
}

/** 「まとまり__名前」を欄に分けて入れる。空なら全部空にする。 */
function setViewName(full) {
    const i = (full || '').indexOf('__');
    const group = i > 0 ? full.slice(0, i) : '';
    const body = i > 0 ? full.slice(i + 2) : (full || '');
    fillViewGroups(group);
    if (!group) $('#viewGroupNew').value = '';
    $('#viewNameBody').value = body;
}

/** 欄から「まとまり__名前」を組み立てる。足りなければ ''。 */
function readViewName() {
    const sel = $('#viewGroup');
    const group = sel.value === '__new__' ? $('#viewGroupNew').value.trim() : sel.value;
    const body = $('#viewNameBody').value.trim();
    return group && body ? `${group}__${body}` : '';
}
let viewExplainText = '';    // いま出ている解説（保存時に一緒に送る。SQLを直したら空に戻る）

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
                // 登録後も、解説と使ったデータは畳まずに全部見せる
                v.explanation
                    ? el('div', { class: 'alert alert--info mb' },
                        el('div', { class: 'mb' }, el('b', {}, 'このSQLがしていること')),
                        el('div', { style: 'white-space:pre-wrap' }, v.explanation))
                    : el('div', { class: 'small muted mb' },
                        'このSQLの解説はまだありません（「編集」→「AIに解説を書かせる」→ 保存 で付けられます）。'),
                usedDataBox(v.used, 'alert alert--info mb'),
                el('div', { class: 'row' },
                    el('button', { class: 'btn btn--sm', onclick: ev => previewView(v, out, ev.target) }, 'プレビュー'),
                    el('button', { class: 'btn btn--sm', title: 'このビューの中身を全件 Excel にしてダウンロードします',
                                   onclick: ev => exportView(v.sql, v.name, ev.target) }, 'Excel'),
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

/** SQLを実データで動かして全件を Excel にする。戻りの先頭の行はプレビューにも使える。 */
async function exportView(sql, name, btn) {
    if (!String(sql || '').trim()) { toast('SQLを書いてください。', 'warn'); return null; }
    btn.disabled = true;
    const old = btn.textContent;
    btn.textContent = '作成中…';
    try {
        const r = await api('/api/catalog/view/export', { db: CAT.db, sql, name: name || '' });
        toast(`${r.filename} を作りました（${Number(r.rows).toLocaleString()}行${r.truncated ? '・上限で切り詰め' : ''}）。`, 'ok', 8000);
        location.href = r.url;
        return r;
    } catch (e) {
        toast(e.message, 'err', 10000);
        return null;
    } finally {
        btn.disabled = false;
        btn.textContent = old;
    }
}

function renderViewExplain(text) {
    viewExplainText = text || '';
    const box = $('#viewExplain');
    if (!box) return;
    if (!text) { box.replaceChildren(); return; }
    box.replaceChildren(el('div', { class: 'alert alert--info mt' },
        el('div', { class: 'mb' }, el('b', {}, 'このSQLがしていること')),
        el('div', { style: 'white-space:pre-wrap' }, text)));
}

/** 「使ったデータ」の欄。表ごとに、読んだ列を説明つきで並べる（ビュー経由で読む元の表も出る）。 */
function usedDataBox(used, cls) {
    if (!used || !used.length) return null;
    return el('div', { class: cls || 'alert alert--info mt' },
        el('div', { class: 'mb' }, el('b', {}, '使ったデータ'),
           el('span', { class: 'small muted', style: 'margin-left:8px' },
              'このSQLが読む表と列（ビューを使っていれば、その元の表も）')),
        ...used.map(t => el('div', { class: 'usedrow' },
            el('div', {},
                icon(t.type === 'view' ? 'view' : 'table'),
                el('b', { class: 'mono' }, t.name),
                t.type === 'view' ? el('span', { class: 'badge', style: 'margin-left:6px' }, 'ビュー') : null,
                t.description ? el('span', { class: 'small muted', style: 'margin-left:8px' }, t.description) : null),
            el('div', { class: 'usedcols' },
                ...(t.columns.length
                    ? t.columns.map(c => el('span', { title: c.description || '' },
                        el('span', { class: 'mono' }, c.name),
                        c.description ? el('span', { class: 'muted' }, `（${c.description}）`) : null))
                    : [el('span', { class: 'muted' }, '（表全体。件数を数えるなど、特定の列は読みません）')])))));
}

function renderViewUsed(used) {
    const box = $('#viewUsed');
    if (!box) return;
    box.replaceChildren(usedDataBox(used) || '');
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
    renderViewExplain(v.explanation || '');     // 保存してある解説はそのまま出す（SQLを直したら消える）
    renderViewUsed(v.used || []);
    $('#viewPurpose').value = '';
    $('#viewSqlWrap').classList.remove('hidden');
    $('#viewSql').value = v.sql || '';
    setViewName(v.name);
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
        setViewName('');
        $('#viewDesc').value = '';
        $('#viewPreview').replaceChildren();
        $('#viewNote').replaceChildren();
        renderViewExplain('');
        renderViewUsed([]);
        $('#viewSqlWrap').classList.add('hidden');
    });

    $('#viewGroup').addEventListener('change', () => {
        $('#viewGroupNew').classList.toggle('hidden', $('#viewGroup').value !== '__new__');
        if ($('#viewGroup').value === '__new__') $('#viewGroupNew').focus();
    });

    $('#viewManual').addEventListener('click', () => {
        $('#viewNote').replaceChildren();
        $('#viewSqlWrap').classList.remove('hidden');
        $('#viewSql').focus();
    });

    // 人がSQLを直したら、AIの解説も使ったデータも当てはまらなくなるので下ろす
    $('#viewSql').addEventListener('input', () => { renderViewExplain(''); renderViewUsed([]); });
    // AIが使えないときは「解説を書かせる」を出さない（押しても未設定のエラーになるだけ）
    if (!CAT.llmReady) $('#viewExplainBtn').classList.add('hidden');

    // いま書いてあるSQLを実データで動かして全件を Excel に。先頭の行は下にも出す
    // （SQLを自分で書いたときの「確かめ」を兼ねる）
    $('#viewExport').addEventListener('click', async ev => {
        const r = await exportView($('#viewSql').value, readViewName(), ev.target);
        if (r) {
            $('#viewPreview').replaceChildren(viewPreviewBox({ columns: r.columns, rows: r.preview, total: r.rows }));
            renderViewUsed(r.used);
        }
    });

    // いま書いてあるSQLの解説をAIに書かせる（自分で書いたSQL・直したSQLに解説を付ける）
    $('#viewExplainBtn').addEventListener('click', async ev => {
        const sql = $('#viewSql').value.trim();
        if (!sql) { toast('SQLを書いてください。', 'warn'); return; }
        ev.target.disabled = true;
        const old = ev.target.textContent;
        ev.target.textContent = 'AIが考えています...';
        try {
            const r = await api('/api/catalog/view/explain', { db: CAT.db, sql });
            renderViewExplain(r.explanation || '');
            renderViewUsed(r.used || []);
            if (!r.explanation) toast('解説を書けませんでした。', 'warn');
        } catch (e) {
            toast(e.message, 'err', 12000);
        } finally {
            ev.target.disabled = false;
            ev.target.textContent = old;
        }
    });

    $('#viewDraft').addEventListener('click', async ev => {
        const purpose = $('#viewPurpose').value.trim();
        if (!purpose) { toast('どんな一覧が欲しいかを書いてください。', 'warn'); return; }
        ev.target.disabled = true;
        const old = ev.target.textContent;
        ev.target.textContent = 'AIが考えています...';
        // 前回の理由・解説・結果は先に下ろす（考えている間、古い内容が残らないように）
        $('#viewNote').replaceChildren();
        renderViewExplain('');
        renderViewUsed([]);
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
            // まとまりと名前は、まだ空の欄だけ埋める（選んでおいたまとまりや、打った名前は消さない）
            {
                const i = (r.name || '').indexOf('__');
                const g2 = i > 0 ? r.name.slice(0, i) : '';
                const body2 = i > 0 ? r.name.slice(i + 2) : (r.name || '');
                const sel = $('#viewGroup');
                if (!sel.value && !$('#viewGroupNew').value.trim() && g2) fillViewGroups(g2);
                if (!$('#viewNameBody').value.trim() && body2) $('#viewNameBody').value = body2;
            }
            if (!$('#viewDesc').value) $('#viewDesc').value = r.description || '';
            renderViewExplain(r.explanation);
            renderViewUsed(r.used);
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

    $('#viewSave').addEventListener('click', async ev => {
        const name = readViewName();
        const sql = $('#viewSql').value.trim();
        if (!name) { toast('まとまりと名前を入れてください。', 'warn'); return; }
        if (!sql) { toast('SQLを書いてください。', 'warn'); return; }
        ev.target.disabled = true;
        try {
            const payload = {
                db: CAT.db, name, sql,
                description: $('#viewDesc').value.trim(),
                explanation: viewExplainText,        // 登録後も読めるように、解説も一緒に残す
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
            toast('保存しました。テーブル一覧やマイエージェントからも使えます。');
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
    ER.setJoinStatus(CAT.joinStatus || null);
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
    // 集計側が「この表はグラフにしない」と言っているなら描かない。
    // 1列目が長い文の表は、棒を並べても軸が読めないため
    if (table.chart === false) return null;
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

/* --- 会話の履歴 ------------------------------------------------------------
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
                el('div', { class: 'qa__clamp' }, x.text),
                // 押された評価。どの質問で何が押されたかが、そのまま改善の入口になる
                ...((x.fb || []).length
                    ? [el('div', { class: 'small' },
                         ...(x.fb || []).map(f => el('span', {
                             class: 'badge' + (f === 'これでいい' ? '' : ' badge--warn'),
                             style: 'margin-right:4px',
                         }, f)))]
                    : [])),
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

/* --- レポート（AIに1回だけ書かせる読み物） --------------------------------------
   数字はコードが出し、AIには言葉だけを書かせている。だからここでは
   返ってきた文をそのまま並べるだけで、計算も整形もしない。
   作るのはボタンを押したときだけ（画面を開いただけでは呼ばない）。 */
const REP_SECTIONS = [
    ['used', 'よく使われている用途'],
    ['teams', '部署ごとの様子'],
    ['want_data', 'ほしいと言われたデータ'],
    ['want_func', 'ほしいと言われた機能'],
    ['actions', '次の1か月で打つ手'],
    ['unknown', 'この記録からは分からないこと'],
];

function renderReport(rec) {
    const body = $('#uRepBody');
    if (!rec) {
        body.replaceChildren(el('div', { class: 'empty' },
            'まだレポートがありません。上の「レポートを作る」を押してください。'));
        return;
    }
    const card = el('div', { class: 'card' },
        el('div', { class: 'card__title' }, `${rec.name} のレポート`),
        el('div', { class: 'small muted' },
           `作成: ${String(rec.at || '').slice(0, 16).replace('T', ' ')}`
           + (rec.by ? `（${rec.by}）` : '')));
    const b = rec.body || {};
    let any = false;
    REP_SECTIONS.forEach(([key, label]) => {
        const items = b[key] || [];
        if (!items.length) return;
        any = true;
        card.append(el('div', { class: 'card__title', style: 'margin-top:14px;font-size:13px' }, label),
                    el('ul', { style: 'margin:4px 0 0 0;padding-left:20px' },
                       ...items.map(x => el('li', { style: 'margin-bottom:3px' }, String(x)))));
    });
    if (!any) card.append(el('div', { class: 'small muted mt' }, '書ける内容がありませんでした。'));
    body.replaceChildren(card);
}

async function loadReportList(pick) {
    let r;
    try { r = await api('/api/usage/reports', undefined, 'GET'); } catch (e) { return; }
    const sel = $('#uRepPick');
    sel.replaceChildren(el('option', { value: '' }, '保存したレポート…'),
        ...(r.reports || []).map(x => el('option', { value: x.name }, x.name)));
    if (pick) sel.value = pick;
    $('#uRepNote').textContent = (r.reports || []).length
        ? `保存済み ${r.reports.length} 本` : '';
}

async function openReport(name) {
    if (!name) { renderReport(null); return; }
    try {
        renderReport(await api(`/api/usage/reports?name=${encodeURIComponent(name)}`,
                               undefined, 'GET'));
    } catch (e) {
        toast(e.message, 'warn');
    }
}

async function buildReport() {
    const btn = $('#uRepBuild');
    const name = ($('#uRepName').value || '').trim();
    if (!confirm('AIを1回呼んでレポートを作ります。よろしいですか？')) return;
    btn.disabled = true;
    const label = btn.textContent;
    btn.textContent = '作成中…';
    try {
        const rec = await api('/api/usage/report-build', { days: days(), user: who(), name });
        renderReport(rec);
        await loadReportList(rec.name);
        toast(`レポート「${rec.name}」を作りました。`, 'ok');
    } catch (e) {
        toast(e.message, 'warn');
    } finally {
        btn.disabled = false;
        btn.textContent = label;
    }
}


/* --- タブ・条件・Excel ------------------------------------------------------- */

function showTab(key) {
    $$('.tab[data-view]').forEach(t => t.classList.toggle('is-active', t.dataset.view === key));
    const isChats = key === 'chats';
    const isDoc = key === 'report';       // レポートは集計ではなく読み物
    $('#pane-report').classList.toggle('is-active', !isChats && !isDoc);
    $('#pane-chats').classList.toggle('is-active', isChats);
    $('#pane-doc').classList.toggle('is-active', isDoc);
    // Excel出力は集計のためのもの。読み物のタブでは押せないようにする
    $('#uExport').disabled = isDoc;
    if (isChats) loadChats();
    else if (isDoc) { loadReportList(); renderReport(null); }
    else { view = key; loadReport(); }
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
    $$('.tab[data-view]').forEach(t => t.addEventListener('click', () => showTab(t.dataset.view)));
    const reload = () => {
        if ($('#pane-doc').classList.contains('is-active')) return;   // 読み物は作り直さない
        if ($('#pane-chats').classList.contains('is-active')) loadChats();
        else loadReport();
    };
    $('#uRange').addEventListener('change', reload);
    $('#uUser').addEventListener('change', reload);
    $('#uChatFilter').addEventListener('input', renderChatList);
    wireQaHeader();
    $('#uExport').addEventListener('click', exportExcel);
    $('#uRepBuild').addEventListener('click', buildReport);
    $('#uRepPick').addEventListener('change', ev => openReport(ev.target.value));
    // 最初に選ばれているタブは、サーバが決める（USAGE_VIEWS の先頭）。
    // ここで 'summary' を決め打ちすると、下線の付いたタブと中身が食い違う
    showTab($('.tab[data-view].is-active')?.dataset.view || view);
});
})();

// ===== 元 import.js（window.IMP がある画面だけ動く） =====
(() => {
if (!window.IMP) return;
/* データ取り込み画面。プレビュー 列の設定 取り込み先 実行 / 定期登録。 */

let plan = [];          // 列の設定
let previewInfo = null;
// いま選ばれている取り込み元。サーバのファイル（path）・アップロード（upload）・
// スクレイピングの出来上がり（scraper + 預かり札 upload）のどれか。
let source = null;      // {kind:'server'|'upload'|'scraper', path?, upload?, scraper?, file?, name}

function readOptions() {
    return {
        path: source?.kind === 'server' ? source.path : '',
        // スクレイピングの出来上がりはアップロードと同じ預かり場所から読む
        upload: (source?.kind === 'upload' || source?.kind === 'scraper') ? source.upload : null,
        scraper: source?.kind === 'scraper' ? source.scraper : null,
        scrape_file: source?.kind === 'scraper' ? source.file : null,
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

/* --- スクレイピングのスクリプトを選んで試すダイアログ ------------------------------
   scrapers/ 直下の .py を一覧し、「試す」で1回実行する。出来たファイルは
   アップロードと同じ預かり場所（メモリ）に置かれ、その預かり札でプレビューする。
   ファイル（Excelならシートも）を選ぶと、あとはサーバのファイルと同じ流れ。 */

let scraperRunning = 0;          // 「試す」を実行中の数。閉じたり作り直したりしない

async function openScrapers() {
    $('#scraperModal').classList.remove('hidden');
    if (scraperRunning > 0) return;      // 実行中の一覧をそのまま見せる（作り直すと結果が消える）
    const list = $('#scraperList');
    list.replaceChildren(el('div', { class: 'fsrow' }, el('span', { class: 'spinner' }), '読み込み中...'));
    let r;
    try {
        r = await api('/api/scrapers', undefined, 'GET');
    } catch (e) {
        list.replaceChildren(el('div', { class: 'alert alert--err' }, e.message));
        return;
    }
    if (!r.ok) {
        list.replaceChildren(el('div', { class: 'alert alert--warn' },
            `フォルダ ${r.dir} がありません。作成して .py を置いてください。`));
        return;
    }
    if (!r.scrapers.length) {
        list.replaceChildren(el('div', { class: 'small muted', style: 'padding:12px' },
            `${r.dir} に .py がありません。`));
        return;
    }
    list.replaceChildren(...r.scrapers.map(s => scraperRow(s, r.timeout_sec)));
}

function scraperRow(s, timeoutSec) {
    const result = el('div', { style: 'padding:0 0 4px 28px' });
    const btn = el('button', {
        class: 'btn btn--sm',
        title: `スクリプトを1回実行します（最大 ${Math.round(timeoutSec / 60)} 分）`,
        onclick: async () => {
            btn.disabled = true;
            btn.innerHTML = '<span class="spinner"></span> 実行中';
            result.replaceChildren(el('div', { class: 'small muted' },
                `実行しています（最大 ${Math.round(timeoutSec / 60)} 分待ちます）...`));
            scraperRunning++;
            try {
                const r = await api('/api/scrapers/test', { name: s.name, timeout_sec: timeoutSec });
                result.replaceChildren(
                    el('div', { class: 'small muted' },
                        `${r.seconds} 秒で ${r.files.length} ファイルできました。取り込むファイルを選んでください。`),
                    ...r.files.map(f => el('div', {
                        class: 'fsrow',
                        onclick: () => { chooseScraped(s.name, f); closeScrapers(); },
                    },
                        icon('file', 'icon--sm'), el('span', { class: 'name' }, f.name),
                        el('span', { class: 'meta' },
                            `${(f.size / 1024).toFixed(0)} KB`
                            + (f.sheets.length ? ` ・ シート: ${f.sheets.join('、')}` : '')))));
            } catch (e) {
                // 失敗の理由（スクリプトの出力の末尾つき）をそのまま見せる。
                // ここで読めないと、何を直せばよいか分からない
                result.replaceChildren(el('pre', { class: 'alert alert--err small mono',
                    style: 'white-space:pre-wrap;margin:4px 0' }, e.message));
            } finally {
                scraperRunning--;
            }
            btn.disabled = false;
            btn.textContent = '試す';
        },
    }, '試す');
    return el('div', {},
        el('div', { class: 'fsrow', style: 'cursor:default' },
            icon('file', 'icon--sm'), el('span', { class: 'name' }, s.name),
            el('span', { class: 'meta' }, `${(s.size / 1024).toFixed(0)} KB ・ ${s.mtime}`),
            btn),
        result);
}

function closeScrapers() {
    if (scraperRunning > 0) {
        // 閉じても実行は続くが結果の出し先が消えるので、待ってもらう（相手サイトへ二度行かないため）
        toast('スクリプトの実行が終わるまでお待ちください。', 'warn');
        return;
    }
    $('#scraperModal').classList.add('hidden');
}

function chooseScraped(script, f) {
    source = { kind: 'scraper', scraper: script, upload: f.upload, file: f.name, name: f.name };
    showChosen('', f.name,
        `スクレイピング ${script} の出来上がり（${(f.size / 1024).toFixed(0)} KB）`
        + (f.sheets.length ? ` ・ シート: ${f.sheets.join('、')}` : ''));
    loadPreview();
}

/* --- 選択の確定 ----------------------------------------------------------------- */

function showChosen(icon, label, note) {
    $('#chosen').replaceChildren(el('div', { class: 'chosenfile' },
        el('span', {}, icon),
        el('div', { class: 'grow' },
            el('div', { style: 'font-weight:700' }, label),
            note ? el('div', { class: 'small muted' }, note) : null)));
    $('#readOpts').classList.remove('hidden');
    // 前のファイルのシート名を引きずらない（別の Excel に切り替えたとき、
    // 無いシート名を送り続けてプレビューが失敗し続けるのを防ぐ）
    $('#sheet').replaceChildren();
    $('#sheetWrap').classList.add('hidden');
    $('#sepWrap').classList.remove('hidden');
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
        // Excel ならシート欄を出す。選択肢は中身が変わったときだけ入れ替える
        // （同じ数の別のシート名でも入れ替わるように、件数ではなく名前で比べる）
        const has = (r.sheets || []).length > 0;
        $('#sheetWrap').classList.toggle('hidden', !has);
        $('#sepWrap').classList.toggle('hidden', has);
        const now = [...$('#sheet').options].map(o => o.value);
        // 区切りは、シート名に絶対に出てこない制御文字。ファイルの中には
        // 文字そのものではなく \x01 と書く。生の制御文字を置くと、編集や
        // 文字コードの変換で黙って消え、区切りが空文字になって
        // 別々の並びが同じものとして通ってしまう
        if (has && now.join('\x01') !== r.sheets.join('\x01')) {
            $('#sheet').replaceChildren(...r.sheets.map(s => el('option', {}, s)));
        }
        renderPreview(r);
    } catch (e) {
        if (source?.kind === 'scraper' && previewInfo) {
            // 試した出来上がりの預かりが切れた等。入力途中の設定を消さず、案内だけ出す
            toast(e.message + ' もう一度「スクレイピングで取得する」から試してください。', 'err', 10000);
            renderPreview(previewInfo);
            return;
        }
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
                                { ...(i === '1日ごと' ? { selected: 'selected' } : {}) }, i)))),
                // スクレイピングだけの欄。1回にどれだけ待つか／質問に応じた取り直しの最小間隔
                el('div', { id: 'scrapeIntervalWrap', class: 'hidden', style: 'width:150px' },
                    el('label', { class: 'field' }, '最小間隔（分）'),
                    el('input', { type: 'number', id: 'scrapeInterval', value: String(IMP.scrapeInterval),
                        min: '0', max: String(IMP.scrapeLimits.interval_max),
                        title: '質問を受けたとき、前回の取得からこの分数が経っていれば取り直します。'
                             + '0 なら質問のたびに取りに行きます。' })),
                el('div', { id: 'scrapeTimeoutWrap', class: 'hidden', style: 'width:150px' },
                    el('label', { class: 'field' }, 'タイムアウト（秒）'),
                    el('input', { type: 'number', id: 'scrapeTimeout', value: String(IMP.scrapeTimeout),
                        min: String(IMP.scrapeLimits.timeout_min), max: String(IMP.scrapeLimits.timeout_max),
                        title: 'スクリプト1回の実行にこれ以上かかったら打ち切ります。' }))),
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
    const scraper = source?.kind === 'scraper';
    ['#keepWrap', '#appendNote'].forEach(s => $(s)?.classList.toggle('hidden', !append));
    $('#jobIntervalWrap')?.classList.toggle('hidden', !append || upload);
    $('#jobStartWrap')?.classList.toggle('hidden', !append || upload);
    // アップロードは登録できない（サーバに残らず読み直せない）ので、名前も聞かない
    $('#jobNameWrap')?.classList.toggle('hidden', upload);
    // スクレイピングだけの欄。最小間隔は「質問に応じた取り直し」＝全件入れ替えのときだけ
    $('#scrapeTimeoutWrap')?.classList.toggle('hidden', !scraper);
    $('#scrapeIntervalWrap')?.classList.toggle('hidden', !scraper || append);

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
        if (scraper && append) {
            text = `決めた間隔で自動的に ${source.scraper} を実行し、出来たファイルを1回ぶんずつ溜めます。`
                + '開始日時を入れると、その時刻を過ぎるまで動きません（空なら登録後すぐ対象）。'
                + '取得したファイルはサーバに残しません。'
                + '手動で1回だけ取り込むことはできません'
                + '（1回ぶん余計に増えて、保存回数の数え方が崩れるため）。';
        } else if (scraper) {
            text = '登録した時点で、いま試した出来上がりを取り込みます。以降は、マイエージェントで質問を'
                + `受けるたびに、前回の取得から最小間隔が経っていれば ${source.scraper} を実行し直して`
                + '表を入れ替えてから答えます（経っていなければ前回の内容で答えます）。'
                + '取得したファイルはサーバに残しません。'
                + '実行に失敗したときは、最後に取り込んだ内容で答えます'
                + '（そのときはカタログに警告が出ます）。';
        } else if (upload && append) {
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
            text = '登録した時点で1回取り込みます。以降は、マイエージェントで質問を受けるたびに'
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
    if (source?.kind === 'scraper') {
        const lim = IMP.scrapeLimits;
        const t = parseInt(($('#scrapeTimeout')?.value || '').trim(), 10);
        if (!Number.isInteger(t) || t < lim.timeout_min || t > lim.timeout_max) {
            out.push(`タイムアウト（秒）は ${lim.timeout_min}〜${lim.timeout_max} で指定してください。`);
        }
        if ($('#mode').value !== 'append') {
            const m = parseInt(($('#scrapeInterval')?.value || '').trim(), 10);
            if (!Number.isInteger(m) || m < 0 || m > lim.interval_max) {
                out.push(`最小間隔（分）は 0〜${lim.interval_max} で指定してください。`);
            }
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
        ...(source?.kind === 'scraper' ? {
            scrape_timeout_sec: $('#scrapeTimeout')?.value,
            // 最小間隔は全件入れ替えのときだけ（追記では欄が隠れているので、隠れた値は送らない）
            ...($('#mode').value !== 'append'
                ? { scrape_interval_minutes: $('#scrapeInterval')?.value } : {}),
        } : {}),
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
                + (source?.kind === 'scraper'
                    ? '以降は質問のたびに（最小間隔が経っていれば）取得し直します。'
                    : '以降は質問のたびに元ファイルへ追随します。'), 'ok', 8000);
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
    $('#pickScraper')?.addEventListener('click', openScrapers);
    $('#scraperClose')?.addEventListener('click', closeScrapers);
    $('#scraperModal')?.addEventListener('click', ev => {
        if (ev.target.id === 'scraperModal') closeScrapers();
    });
    document.addEventListener('keydown', ev => {
        if (ev.key === 'Escape') { closeBrowser(); closeScrapers(); }
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

// ===== マイロボット共通（ダイアログの枠と穴の入力。マイエージェント画面とマイロボット画面の両方で使う） =====
(() => {
/** 汎用のダイアログ枠。閉じる関数を返す。
 *  opts.closable=false … 背景クリック・×では閉じない（実行中の表示など）
 *  opts.onClose        … どの経路で閉じても1回だけ呼ぶ */
function modal(title, bodyNode, footNodes, opts) {
    const o = opts || {};
    const back = el('div', { class: 'modal' });
    const boxClass = o.wide ? 'modal__box modal__box--wide' : 'modal__box';
    let closed = false;
    const close = () => {
        if (closed) return;
        closed = true;
        back.remove();
        if (o.onClose) o.onClose();
    };
    if (o.closable !== false) back.addEventListener('click', ev => { if (ev.target === back) close(); });
    back.append(el('div', { class: boxClass },
        el('div', { class: 'modal__head' }, el('b', {}, title), el('div', { class: 'spacer' }),
            o.closable === false ? null
                : el('button', { class: 'btn btn--sm btn--ghost', title: '閉じる', onclick: close },
                     icon('x', 'icon--sm'))),
        el('div', { class: 'modal__body' }, bodyNode),
        el('div', { class: 'modal__foot row', style: 'gap:8px;align-items:center' }, ...(footNodes || []))));
    document.body.append(back);
    return close;
}

/** 穴の値を聞く。実行なら {h1: 値, ...}、閉じたら null を返す。 */
function askHoles(r) {
    return new Promise(resolve => {
        const inputs = {};
        let done = false;
        const finish = v => { if (!done) { done = true; resolve(v); } };
        const body = el('div', {},
            el('div', { class: 'small muted', style: 'margin-bottom:8px' },
               '実行のたびに入れ替える値です。登録したときの値が最初から入っています。'),
            ...r.holes.map(h => el('div', { style: 'margin-bottom:10px' },
                el('label', { class: 'field' }, h.label,
                   el('span', { class: 'muted small' }, h.kind === 'number' ? '（数値）' : '')),
                inputs[h.key] = el('input', { type: 'text', value: h.sample || '',
                                              style: 'width:100%' }))));
        const go = el('button', { class: 'btn btn--primary', onclick: () => {
            const v = {};
            for (const h of r.holes) v[h.key] = inputs[h.key].value.trim();
            finish(v);
            close();
        } }, '実行する');
        // 背景クリック・×で閉じたときは null（枠側がどの経路でも onClose を1回呼ぶ）
        const close = modal(`マイロボット「${r.name}」`, body,
            [go, el('span', { class: 'small muted' }, `${r.n_steps}手順を実行します`)],
            { onClose: () => finish(null) });
        const first = Object.values(inputs)[0];
        if (first) { first.focus(); first.select(); }
        body.addEventListener('keydown', ev => { if (ev.key === 'Enter') go.click(); });
    });
}

/** フォルダ出力の決めごとの欄。{node, value()} を返す。onChange を渡すと変更のたびに呼ぶ。
 *  r は {folder_out, folder_stamp, folder_overwrite} を持つ。 */
function folderOptions(r, onChange) {
    const on = el('input', { type: 'checkbox', ...(r.folder_out ? { checked: 'checked' } : {}) });
    const stamp = el('select', {},
        el('option', { value: '1', ...(r.folder_stamp !== false ? { selected: 'selected' } : {}) }, '日時を付ける（例: 一覧_20260912_1005.xlsx）'),
        el('option', { value: '0', ...(r.folder_stamp === false ? { selected: 'selected' } : {}) }, '付けない（例: 一覧.xlsx）'));
    const ow = el('select', {},
        el('option', { value: '0', ...(!r.folder_overwrite ? { selected: 'selected' } : {}) }, '番号を付けて残す（_2, _3）'),
        el('option', { value: '1', ...(r.folder_overwrite ? { selected: 'selected' } : {}) }, '置き換える（前のファイルは消える）'));
    const detail = el('div', { class: 'row', style: 'gap:10px;flex-wrap:wrap;margin-top:4px' },
        el('label', { class: 'small', style: 'display:flex;align-items:center;gap:4px' },
           el('span', { style: 'white-space:nowrap' }, '名前:'), stamp),
        el('label', { class: 'small', style: 'display:flex;align-items:center;gap:4px' },
           el('span', { style: 'white-space:nowrap' }, '同じ名前があるとき:'), ow));
    const sync = () => { detail.classList.toggle('hidden', !on.checked); if (onChange) onChange(); };
    on.addEventListener('change', sync);
    stamp.addEventListener('change', () => { if (onChange) onChange(); });
    ow.addEventListener('change', () => { if (onChange) onChange(); });
    detail.classList.toggle('hidden', !on.checked);
    const node = el('div', { class: 'robotturn' },
        el('label', { style: 'display:flex;align-items:center;gap:6px;cursor:pointer' }, on,
           el('span', {}, '実行結果をフォルダにも置く')),
        detail);
    const value = () => ({ folder_out: on.checked, folder_stamp: stamp.value === '1', folder_overwrite: ow.value === '1' });
    return { node, value };
}

/** 定期実行の欄。{node, value()} を返す。onChange を渡すと変更のたびに呼ぶ。
 *  intervals は {表示名: 分}（定期取り込みと同じ一覧）。r.schedule と r.holes を見る。
 *  withValues=true なら、穴の値（定期実行のたびに使う値）と「止める」も出す（カード用）。 */
/** その設定で、実行と実行のあいだが最短で何分空くか（管理者の最低間隔と比べる用。サーバと同じ計算）。 */
function scheduleGap(kind, hours) {
    if (kind === 'hours') return Number(hours || 1) * 60;
    return { manual: 0, daily: 1440, weekly: 10080, monthly_day: 40320, monthly_nth: 40320 }[kind] || 0;
}

function scheduleOptions(r, vocab, onChange, withValues, extra) {
    const x = extra || {};
    const v = vocab || { kinds: {}, hours: [], weekdays: [], nth: {} };
    const floorMin = Number(x.minIntervalHours || 0) * 60;
    const sch = r.schedule || {};
    const curKind = sch.kind || 'manual';
    // いまの最低間隔でも選べる「時間ごと」の値。1時間ごとが短いからといって
    // 6時間ごとまで塞いではいけないので、しかたの可否もこの中の最短で判定する。
    const okHours = v.hours.filter(h => !(floorMin > 0 && h * 60 < floorMin));
    // 保存済みの値は、いま短くなっていてもそのまま見せる（何が設定されているか分かるように）
    const savedHours = Number(sch.hours || 0);
    const pickHours = (curKind === 'hours' && v.hours.indexOf(savedHours) >= 0)
        ? savedHours : (okHours.length ? okHours[0] : (v.hours[0] || 1));
    // しかた（手動のみ／時間ごと／毎日／毎週／毎月／毎月第N曜日）
    const kindSel = el('select', { style: 'max-width:210px' }, ...Object.entries(v.kinds).map(([k, label]) => {
        const gap = scheduleGap(k, pickHours);
        const tooShort = gap > 0 && floorMin > 0 && gap < floorMin && k !== curKind;
        return el('option', { value: k, ...(curKind === k ? { selected: 'selected' } : {}),
                              ...(tooShort ? { disabled: 'disabled' } : {}) },
                  label + (tooShort ? '（管理者の最低間隔より短い）' : ''));
    }));
    const hoursSel = el('select', { style: 'max-width:130px' }, ...v.hours.map(h => {
        const tooShort = floorMin > 0 && h * 60 < floorMin && !(curKind === 'hours' && Number(sch.hours) === h);
        return el('option', { value: String(h), ...(pickHours === h ? { selected: 'selected' } : {}),
                              ...(tooShort ? { disabled: 'disabled' } : {}) }, `${h}時間ごと`);
    }));
    const timeIn = el('input', { type: 'time', value: sch.time || '08:00', style: 'width:110px' });
    const wdaySel = el('select', { style: 'max-width:110px' }, ...v.weekdays.map((w, i) =>
        el('option', { value: String(i), ...(Number(sch.weekday || 0) === i ? { selected: 'selected' } : {}) }, w + '曜日')));
    const daySel = el('select', { style: 'max-width:100px' }, ...Array.from({ length: 31 }, (_, i) => i + 1).map(d =>
        el('option', { value: String(d), ...(Number(sch.day || 1) === d ? { selected: 'selected' } : {}) }, `${d}日`)));
    const nthSel = el('select', { style: 'max-width:100px' }, ...Object.entries(v.nth).map(([k, label]) =>
        el('option', { value: k, ...(String(sch.nth || 1) === k ? { selected: 'selected' } : {}) }, label)));
    const start = el('input', { type: 'datetime-local', value: (sch.start_at || '').slice(0, 16), style: 'max-width:210px' });
    const on = el('input', { type: 'checkbox', ...(sch.enabled === false ? {} : { checked: 'checked' }) });
    const holeInputs = {};
    // しかたに応じて出す欄
    const detail = el('div', { class: 'row', style: 'gap:8px;flex-wrap:wrap;align-items:center' },
        hoursSel, nthSel, wdaySel, daySel, timeIn);
    const syncDetail = () => {
        const k = kindSel.value;
        hoursSel.classList.toggle('hidden', k !== 'hours');
        nthSel.classList.toggle('hidden', k !== 'monthly_nth');
        wdaySel.classList.toggle('hidden', k !== 'weekly' && k !== 'monthly_nth');
        daySel.classList.toggle('hidden', k !== 'monthly_day');
        timeIn.classList.toggle('hidden', k === 'manual' || k === 'hours');
        detail.classList.toggle('hidden', k === 'manual');
    };
    const rows = [
        el('span', { class: 'small' }, 'しかた'), el('div', {}, kindSel),
        el('span', { class: 'small' }, 'いつ'), detail,
        el('span', { class: 'small' }, '開始日時'), el('div', {}, start,
            el('span', { class: 'small muted', style: 'margin-left:6px' }, 'この日時より前には動きません（空なら登録した時刻から）')),
    ];
    if (withValues) {
        rows.push(el('span', { class: 'small' }, '動かす'), el('label', { style: 'display:flex;align-items:center;gap:6px;cursor:pointer' },
            on, el('span', { class: 'small' }, '止めるとチェックを外す（設定は残ります）')));
        (r.holes || []).forEach(h => {
            const inp = el('input', { type: 'text', value: (sch.values || {})[h.key] ?? h.sample ?? '', style: 'max-width:260px' });
            holeInputs[h.key] = inp;
            rows.push(el('span', { class: 'small' }, `固定の値「${h.label}」`), el('div', {}, inp,
                el('span', { class: 'small muted', style: 'margin-left:6px' }, '登録時の値。実行日で変える場合は登録し直してください')));
        });
    }
    const grid = el('div', { class: 'schedgrid mt' }, ...rows);
    const note = el('div', { class: 'small muted mt' },
        'アプリのサーバが動いていれば、この画面を閉じていても・自分のPCを消していても、時刻になったら動きます。'
        + '結果はマイエージェントの会話に残り、フォルダ出力やメールの自動送信を選んでいればそれも行われます。');
    const warn = x.schedulerOn === false
        ? el('div', { class: 'alert alert--warn small mt' },
             'いまアプリの定期実行（スケジューラ）が止まっています。設定は保存できますが、時刻になっても動きません。管理者に確認してください。')
        : null;
    // いま保存されている設定は、短すぎても選択肢に残してある（何が設定されているかを
    // 見せるため）。数に入れると「選び直してください」と言いながら選べるのは今の設定だけ、
    // という案内になるので、ここでは除く
    const choosable = [...kindSel.options].some(
        o => !o.disabled && o.value !== 'manual' && o.value !== curKind);
    const blocked = (sch.floor_blocked)
        ? el('div', { class: 'alert alert--warn small mt' },
             choosable ? '管理者が決めた最低間隔より短いので、いまは動きません。間隔を選び直してください。'
                       : `いまの最低間隔（${x.minIntervalHours} 時間）では、選べる間隔がありません。`
                         + '定期実行を使うには、管理者に最低間隔を短くしてもらってください。')
        : (!choosable && Number(x.minIntervalHours || 0) > 0
            ? el('div', { class: 'alert alert--warn small mt' },
                 `いまの最低間隔（${x.minIntervalHours} 時間）では、選べる間隔がありません（手動のみになります）。`)
            : null);
    const sync = () => { syncDetail(); if (onChange) onChange(); };
    [kindSel, hoursSel, timeIn, wdaySel, daySel, nthSel, start, on,
     ...Object.values(holeInputs)].forEach(i => i.addEventListener('change', sync));
    syncDetail();
    const node = el('div', {}, grid, note, warn, blocked);
    const value = () => {
        const out = { kind: kindSel.value, hours: Number(hoursSel.value || 1),
                      time: timeIn.value || '08:00', weekday: Number(wdaySel.value || 0),
                      day: Number(daySel.value || 1), nth: Number(nthSel.value || 1),
                      start_at: start.value || '' };
        if (withValues) {
            out.enabled = on.checked;
            out.values = Object.fromEntries(Object.entries(holeInputs).map(([k, i]) => [k, i.value]));
        }
        return out;
    };
    // 保存を断られたとき、いま保存されている値に戻す（断られた値が残ったままだと、次の変更も同じ理由で断られる）
    const reset = () => {
        const s2 = r.schedule || {};
        kindSel.value = s2.kind || 'manual';
        hoursSel.value = String(v.hours.indexOf(Number(s2.hours)) >= 0 ? s2.hours : pickHours);
        timeIn.value = s2.time || '08:00';
        wdaySel.value = String(s2.weekday || 0);
        daySel.value = String(s2.day || 1);
        nthSel.value = String(s2.nth || 1);
        start.value = (s2.start_at || '').slice(0, 16);
        syncDetail();
        on.checked = s2.enabled !== false;
        const sample = Object.fromEntries((r.holes || []).map(h => [h.key, h.sample ?? '']));
        Object.entries(holeInputs).forEach(([k, i]) => { i.value = (s2.values || {})[k] ?? sample[k] ?? ''; });
    };
    return { node, value, reset };
}

/** 定期実行を一言で（カードの表示用）。 */
function scheduleLabel(r) {
    const sch = r.schedule || {};
    if ((sch.kind || 'manual') === 'manual') return '定期実行: 手動のみ';
    if (sch.enabled === false) return `定期実行: ${sch.interval_label}（止めています）`;
    return `定期実行: ${sch.interval_label}` + (sch.next_at ? `・次回 ${sch.next_at.slice(5, 16).replace('T', ' ')}` : '');
}

/** 決めごとを一言で（カードの表示用）。 */
function folderLabel(r) {
    if (!r.folder_out) return 'フォルダ: 置かない';
    return 'フォルダ: ' + (r.folder_stamp === false ? '日時なし' : '日時あり') + '・'
        + (r.folder_overwrite ? '置き換える' : '番号を付けて残す');
}

/** 宛先の候補（管理者が「メール設定」で許可したアドレス）。入力欄の下に、いま打っている分に合う候補を並べ、押すと足す。
 *  複数はカンマ区切り。最後のカンマより後ろを「いま打っている分」として絞る。{node, refresh} を返す。 */
function mailPicker(input, candidates) {
    const all = (candidates || []).map(String);
    const node = el('div', { class: 'mailpick hidden' });
    const parts = () => input.value.split(/[,、;]/);
    const refresh = () => {
        const q = (parts().slice(-1)[0] || '').trim().toLowerCase();
        const have = new Set(parts().slice(0, -1).map(s => s.trim().toLowerCase()).filter(Boolean));
        // いま打っている分と完全に同じものは、もう入っているので候補に出さない
        const hits = all.filter(a => a.toLowerCase().includes(q) && !have.has(a.toLowerCase()) && a.toLowerCase() !== q).slice(0, 12);
        node.replaceChildren(...hits.map(a => el('button', { type: 'button', class: 'mailpick__item',
            // click より先に blur が来て消えないよう、mousedown で拾う
            onmousedown: ev => { ev.preventDefault(); pick(a); } }, a)));
        if (!hits.length) {
            node.append(el('span', { class: 'small muted' },
                all.length ? (q ? '合う宛先がありません（許可されたアドレスだけ指定できます）' : '')
                           : '管理者がまだ宛先を許可していません（「メール設定」で登録すると候補に出ます）'));
        }
        node.classList.toggle('hidden', !node.textContent.trim());
    };
    const pick = (a) => {
        const ps = parts().map(s => s.trim()).filter(Boolean);
        // 打ちかけ（許可リストに無い最後の分）は、選んだものに置き換える
        if (ps.length && !all.some(x => x.toLowerCase() === ps[ps.length - 1].toLowerCase())) ps.pop();
        if (!ps.some(x => x.toLowerCase() === a.toLowerCase())) ps.push(a);
        input.value = ps.join(', ');
        input.dispatchEvent(new Event('change'));   // カードはこれで保存する
        refresh();
    };
    input.addEventListener('input', refresh);
    input.addEventListener('focus', refresh);
    input.addEventListener('blur', () => setTimeout(() => node.classList.add('hidden'), 150));
    return { node, refresh };
}

window.ROBOT = { modal, askHoles, folderOptions, folderLabel, scheduleOptions, scheduleLabel, scheduleGap, mailPicker };
})();

// ===== マイロボットの画面（window.ROBOTS_INIT がある画面だけ動く） =====
(() => {
if (!window.ROBOTS_INIT) return;
/* 保存した処理の流れの一覧。実行すると結果の会話が「いま開いている会話」になるので、
   終わったらマイエージェントの画面へ移る（結果はそこに並ぶ）。 */
let robots = window.ROBOTS_INIT.robots || [];
let running = false;          // 実行中はもう1つ走らせない（同じ手順が二重に走る）

function render() {
    const box = $('#robotCards');
    box.replaceChildren();
    if (!robots.length) {
        box.append(el('div', { class: 'card' },
            el('div', { class: 'card__title' }, 'まだありません'),
            el('div', { class: 'card__desc' },
               'マイエージェントで、いつもの流れ（集計 → グラフ → Excel など）を一度やってから、'
               + '自分の発言にマウスを乗せて「ロボットにする」を押すと、ここに並びます。'),
            el('a', { class: 'btn btn--primary', href: window.ROBOTS_INIT.agentUrl }, 'マイエージェントへ')));
        return;
    }
    robots.forEach(r => box.append(card(r)));
}

/** カードの見出しの一言（設定を変えたら作り直す）。 */
function cardMeta(r) {
    const wait = !!(r.next_run && new Date(r.next_run) > new Date());
    return `${r.n_steps}手順`
        + ((r.dates || []).length ? `・${[...new Set(r.dates.map(d => d.label))].join('、')}` : '')
        + ((r.holes || []).length ? `・固定の値 ${r.holes.map(h => h.label).join('、')}` : '')
        + (r.last_run ? `・前回 ${r.last_run.slice(5, 16).replace('T', ' ')}` : '・まだ実行していません')
        + (wait ? `・次に試せるのは ${r.next_run.slice(5, 16).replace('T', ' ')} 以降` : '')
        + (((r.schedule || {}).kind || 'manual') !== 'manual' ? `・${window.ROBOT.scheduleLabel(r).replace('定期実行: ', '定期 ')}` : '')
        + (r.mail_auto ? '・メール自動送信' : '')
        + (r.from_title ? `・元の会話「${r.from_title}」` : '');
}

let waitTimer = null;
function card(r) {
    // 連打止めで、まだ試せない（サーバも同じ判断で断るが、押してから知るより先に見せる）
    const wait = !!(r.next_run && new Date(r.next_run) > new Date());
    const nextAt = wait ? r.next_run.slice(5, 16).replace('T', ' ') : '';
    if (wait) {
        // 数分で明けるので、明けたら一覧を取り直してボタンを戻す（読み直さなくてよいように）
        clearTimeout(waitTimer);
        waitTimer = setTimeout(async () => {
            try { const res = await api('/api/robots', undefined, 'GET'); robots = res.robots || robots; render(); } catch (_) { /* 次に開いたときに直る */ }
        }, Math.min(Math.max(new Date(r.next_run) - Date.now() + 500, 1000), 10 * 60 * 1000));
    }
    const meta = cardMeta(r);
    return el('div', { class: 'card robotcard' },
        el('div', { class: 'row', style: 'align-items:center;gap:10px' },
            icon('spark'),
            el('div', { class: 'grow', style: 'min-width:0' },
                el('div', { class: 'card__title', style: 'margin:0' }, r.name),
                el('div', { class: 'small muted', 'data-meta': r.id }, meta)),
            el('button', { class: 'btn btn--primary', onclick: () => run(r),
                           ...(wait ? { disabled: 'disabled' } : {}),
                           title: wait ? `続けて押しています。次に試せるのは ${nextAt} 以降です`
                                       : 'いまの日付で1回動かして確かめます（AIなし。結果はマイエージェントの新しい会話に出ます。定期実行の予定は動きません）' },
               'いま試す'),
            el('button', { class: 'btn btn--sm', title: '名前を変える', onclick: () => rename(r) }, '名前'),
            el('button', { class: 'btn btn--sm btn--danger', title: '削除', onclick: () => remove(r) }, '削除')),
        el('div', { class: 'small mt' }, el('span', { class: 'muted' }, '手順: '), r.tools.join(' → ')),
        r.questions.length
            ? el('div', { class: 'small muted' }, '元の質問: ' + r.questions.join(' ／ ')) : null,
        r.has_file_steps ? folderRow(r) : null,
        scheduleRow(r),
        r.has_mail_steps ? mailRow(r) : null,
        detailRow(r),
        historyRow(r),
        r.last_status === 'error'
            ? el('div', { class: 'alert alert--err small mt' }, `前回の実行: ${r.last_message}`) : null);
}

/** 定期実行の設定（間隔・開始・止める・穴の値）。変えるとその場で保存。 */
function scheduleRow(r) {
    const summary = el('span', { class: 'small muted' }, window.ROBOT.scheduleLabel(r));
    const opts = window.ROBOT.scheduleOptions(r, window.ROBOTS_INIT.schedVocab, async () => {
        try {
            const res = await api('/api/robots/update', { id: r.id, schedule: opts.value() });
            const fresh = res.robots.find(x => x.id === r.id);
            if (fresh) {
                Object.assign(r, fresh);
                summary.textContent = window.ROBOT.scheduleLabel(r);
                const meta = document.querySelector(`[data-meta="${r.id}"]`);
                if (meta) meta.textContent = cardMeta(r);       // 見出しも新しい設定に合わせる
            }
            toast('定期実行の設定を保存しました。' + (r.schedule && r.schedule.next_at
                ? ` 次回は ${r.schedule.next_at.slice(5, 16).replace('T', ' ')} です。` : ''));
        } catch (e) { opts.reset(); toast(e.message, 'err', 9000); }
    }, true, { minIntervalHours: window.ROBOTS_INIT.minIntervalHours, schedulerOn: window.ROBOTS_INIT.schedulerOn });
    const sch = r.schedule || {};
    // 失敗したときの知らせ先。管理者が許可したアドレスだけ（サーバも同じ判断で断る）
    const notify = el('input', { type: 'text', value: (r.notify_to || []).join(', '),
                                 style: 'max-width:340px',
                                 placeholder: '例: yamada@example.co.jp（カンマ区切りで複数可）' });
    const saveNotify = async () => {
        try {
            const res = await api('/api/robots/update', { id: r.id, notify_to: notify.value });
            const fresh = res.robots.find(x => x.id === r.id);
            if (fresh) { Object.assign(r, fresh); notify.value = (r.notify_to || []).join(', '); }
            toast((r.notify_to || []).length ? '失敗したときの知らせ先を保存しました。' : '知らせ先を空にしました。');
        } catch (e) { notify.value = (r.notify_to || []).join(', '); toast(e.message, 'err', 9000); }
    };
    notify.addEventListener('change', saveNotify);
    const notifyPick = window.ROBOT.mailPicker(notify, window.ROBOTS_INIT.mailAllowed || []);
    const notifyBox = el('div', { class: 'mt' },
        el('label', { class: 'field' }, '定期実行が失敗したときに知らせるメール（任意）'),
        notify, notifyPick.node,
        el('div', { class: 'small muted mt' },
           window.ROBOTS_INIT.mailReady
               ? `${window.ROBOTS_INIT.allowedDomains} のうち、管理者が「メール設定」で許可したアドレスだけ指定できます（入力すると候補が出ます）。`
               : 'いまメールを送れる設定になっていません（管理者がメール設定を終えると使えます）。'));
    return el('details', { class: 'acc', style: 'margin-top:8px' },
        el('summary', { class: 'small', style: 'cursor:pointer' }, summary),
        el('div', { class: 'acc__body' }, opts.node, notifyBox,
            sch.last_run ? el('div', { class: `small mt ${sch.last_status === 'error' ? 'alert alert--err' : 'muted'}` },
                `前回の定期実行: ${sch.last_run.slice(5, 16).replace('T', ' ')} ${sch.last_message || ''}`) : null));
}

/** メールの自動送信（下書きを作る手順があるロボットだけ）。 */
function mailRow(r) {
    const cb = el('input', { type: 'checkbox', ...(r.mail_auto ? { checked: 'checked' } : {}) });
    cb.addEventListener('change', async () => {
        try {
            const res = await api('/api/robots/update', { id: r.id, mail_auto: cb.checked });
            const fresh = res.robots.find(x => x.id === r.id);
            if (fresh) {
                Object.assign(r, fresh);
                const meta = document.querySelector(`[data-meta="${r.id}"]`);
                if (meta) meta.textContent = cardMeta(r);
            }
            toast(cb.checked ? '実行のたびにメールを送ります（宛先の許可はメール設定のとおり）。' : 'メールは下書きのまま出します（送りません）。');
        } catch (e) { cb.checked = !cb.checked; toast(e.message, 'err', 8000); }
    });
    const tb = el('input', { type: 'checkbox', ...(r.mail_table ? { checked: 'checked' } : {}) });
    tb.addEventListener('change', async () => {
        try {
            const res = await api('/api/robots/update', { id: r.id, mail_table: tb.checked });
            const fresh = res.robots.find(x => x.id === r.id);
            if (fresh) Object.assign(r, fresh);
            toast(tb.checked ? '結果の表を本文の末尾に付けます（先頭20行）。' : '本文は登録時の文章だけを送ります。');
        } catch (e) { tb.checked = !tb.checked; toast(e.message, 'err', 8000); }
    });
    return el('div', { class: 'small', style: 'margin-top:8px' },
        el('label', { style: 'display:flex;align-items:center;gap:6px;cursor:pointer' }, cb,
           el('span', {}, '実行のたびに、作ったメールの下書きをそのまま送る（確認なし）')),
        el('label', { style: 'display:flex;align-items:center;gap:6px;cursor:pointer;margin-top:4px' }, tb,
           el('span', {}, '結果の表を本文の末尾に付ける（直前の手順の表の先頭20行）')),
        el('div', { class: 'muted', style: 'margin:2px 0 0 22px' },
           '本文は登録時の文章のまま送られます。数字を本文に書いている場合は毎回同じ文になるので、数字は表に任せてください。'));
}

/** 実行履歴。いつ・手動か定期か・成否・一言。不具合はまずここを見る。 */
function historyRow(r) {
    const rows = [...(r.history || [])].reverse();
    const label = rows.length
        ? `実行履歴（${rows.length}件・失敗 ${rows.filter(h => !h.ok).length}件）`
        : '実行履歴（まだありません）';
    const body = rows.length
        ? el('div', { class: 'tablewrap', style: 'max-height:320px' },
            el('table', { class: 'data' },
                el('thead', {}, el('tr', {}, el('th', { style: 'width:120px' }, '日時'),
                                   el('th', { style: 'width:70px' }, '種類'),
                                   el('th', { style: 'width:60px' }, '結果'),
                                   el('th', {}, '内容'))),
                el('tbody', {}, ...rows.map(h => el('tr', {},
                    el('td', { class: 'small' }, (h.at || '').slice(0, 16).replace('T', ' ')),
                    el('td', { class: 'small' }, h.source === 'schedule' ? '定期' : '試す'),
                    el('td', { class: 'small' }, h.ok ? '成功' : el('b', { style: 'color:var(--err)' }, '失敗')),
                    el('td', { class: 'small', style: 'white-space:pre-wrap' }, h.message || ''))))))
        : el('div', { class: 'small muted' }, 'まだ実行していません。');
    return el('details', { class: 'acc', style: 'margin-top:8px' },
        el('summary', { class: 'small', style: 'cursor:pointer' },
           el('span', { class: r.history && r.history.some(h => !h.ok) ? '' : 'muted' }, label)),
        el('div', { class: 'acc__body' }, body,
            el('div', { class: 'small muted mt' },
               '定期実行の失敗はここに残ります。原因が「表が見つかりません」なら、'
               + '表の名前が変わったか消えています。作り直すと直ります。')));
}

/** 登録内容の詳細（手順の中身・穴・表・決めごと）。 */
function detailRow(r) {
    const sch = r.schedule || {};
    const steps = (r.steps_detail || []).map(sd => el('div', {},
        el('div', {}, el('span', { class: 'badge' }, `手順${sd.i}`), ' ', el('b', {}, sd.label)),
        el('pre', { class: 'mono' }, sd.text || ''),
        sd.explanation ? el('div', { class: 'small muted', style: 'margin:-4px 0 8px' }, sd.explanation) : null));
    const dl = el('dl', { class: 'robotdetail small' },
        el('dt', {}, '手順'), el('dd', {}, ...steps),
        el('dt', {}, '実行日で変わる値'),
        el('dd', {}, (r.dates || []).length
            ? r.dates.map(d => `${d.label}（登録時 ${d.sample} → 今日なら ${d.now}）`).join('、')
            : 'なし（毎回同じ期間の結果になります）'),
        ...(r.holes.length ? [el('dt', {}, '固定の値（昔の「穴」）'),
                              el('dd', {}, r.holes.map(h => `${h.label}＝${h.sample}`).join('、') + '。実行日で変える場合は登録し直してください')] : []),
        el('dt', {}, '使う表'), el('dd', {}, (r.tables || []).join('、') || 'なし'),
        el('dt', {}, 'フォルダ出力'), el('dd', {}, r.has_file_steps ? window.ROBOT.folderLabel(r).replace('フォルダ: ', '') : 'ファイルを作る手順はありません'),
        el('dt', {}, '定期実行'), el('dd', {}, window.ROBOT.scheduleLabel(r).replace('定期実行: ', '')
            + ((sch.kind || 'manual') !== 'manual' && sch.start_at ? `（開始 ${sch.start_at.replace('T', ' ')}）` : '')),
        el('dt', {}, 'メール'), el('dd', {}, r.has_mail_steps
            ? el('div', {}, (r.mail_auto ? '実行のたびに自動で送る' : '下書きを出すだけ（送らない）') + (r.mail_table ? '・結果の表を本文に付ける' : ''),
                ...(r.mail_steps || []).map(ms => el('div', { style: 'margin-top:4px' },
                    el('div', {}, el('b', {}, '件名: '), ms.subject || '（無題）'),
                    el('pre', { class: 'mono', style: 'white-space:pre-wrap' }, ms.body || ''))))
            : 'メールの手順はありません'),
        el('dt', {}, '元の会話'), el('dd', {}, r.from_title || '—'),
        el('dt', {}, '作成・更新'), el('dd', {}, `${(r.created_at || '').replace('T', ' ')} ／ ${(r.updated_at || '').replace('T', ' ')}`),
        el('dt', {}, '前回の実行'), el('dd', {}, r.last_run ? `${r.last_run.replace('T', ' ')}（${r.last_status === 'ok' ? '成功' : '失敗'}）${r.last_message || ''}` : 'まだ実行していません'));
    return el('details', { class: 'acc', style: 'margin-top:8px' },
        el('summary', { class: 'small', style: 'cursor:pointer' }, el('span', { class: 'muted' }, '詳細（手順の中身・変わる値・表・決めごと）')),
        el('div', { class: 'acc__body' }, dl));
}

/** フォルダ出力の決めごと（ファイルを作る手順があるロボットだけ）。変えるとその場で保存。 */
function folderRow(r) {
    const summary = el('span', { class: 'small muted' }, window.ROBOT.folderLabel(r));
    const opts = window.ROBOT.folderOptions(r, async () => {
        try {
            const res = await api('/api/robots/update', { id: r.id, ...opts.value() });
            const fresh = res.robots.find(x => x.id === r.id);
            if (fresh) { Object.assign(r, fresh); summary.textContent = window.ROBOT.folderLabel(r); }
            toast('フォルダ出力の決めごとを保存しました。');
        } catch (e) { toast(e.message, 'err', 8000); }
    });
    return el('details', { class: 'acc', style: 'margin-top:8px' },
        el('summary', { class: 'small', style: 'cursor:pointer' }, summary),
        el('div', { class: 'acc__body' }, opts.node));
}

async function run(r) {
    if (running) return;
    const values = {};                       // 昔の「穴」は登録時の値で動く（聞かない）
    running = true;
    // 待ち（次に実行できる時刻まで）で止めてあるボタンは、失敗のあとも止めたままにする
    const buttons = [...document.querySelectorAll('#robotCards button')].filter(b => !b.disabled);
    buttons.forEach(b => { b.disabled = true; });
    // 実行中の表示は閉じられない（閉じられると、走っている最中にもう一度押せてしまう）
    const close = window.ROBOT.modal(`マイロボット「${r.name}」`,
        el('div', { class: 'row', style: 'align-items:center;gap:8px;padding:8px 0' },
            el('span', { class: 'spinner' }), `${r.n_steps}手順をいまの日付で動かしています…`),
        [], { closable: false });
    try {
        await api('/api/robots/run', { id: r.id, values });
        // 実行した会話が「いま開いている会話」になっている。結果はそこに並ぶ
        window.location.href = window.ROBOTS_INIT.agentUrl;
    } catch (e) {
        close();
        running = false;
        buttons.forEach(b => { b.disabled = false; });
        toast(e.message, 'err', 9000);
        // 断られた理由（次に実行できる時刻など）が一覧に反映されるよう、取り直して描き直す
        try {
            const res = await api('/api/robots', undefined, 'GET');
            robots = res.robots || robots;
            render();
        } catch (_) { /* 取り直せなくても、いまの表示のまま */ }
    }
}

async function rename(r) {
    const name = prompt('マイロボットの名前', r.name);
    if (name === null) return;
    try {
        const res = await api('/api/robots/update', { id: r.id, name });
        robots = res.robots; render();
    } catch (e) { toast(e.message, 'err', 8000); }
}

async function remove(r) {
    if (!confirm(`マイロボット「${r.name}」を削除しますか？`)) return;
    try {
        const res = await api('/api/robots/delete', { id: r.id });
        robots = res.robots; render();
        toast('削除しました。');
    } catch (e) { toast(e.message, 'err', 8000); }
}

document.addEventListener('DOMContentLoaded', render);
})();

// ===== マイロボットの決めごと（window.ROBOT_SETTINGS_INIT がある画面だけ動く） =====
(() => {
if (!window.ROBOT_SETTINGS_INIT) return;
/* 管理者が決める上限・間隔・手順数。範囲の外はサーバが断る（画面はその文言をそのまま出す）。 */
function fill(s) {
    $('#rsMax').value = s.max_per_user;
    $('#rsInterval').value = s.min_interval_hours;
    $('#rsSteps').value = s.max_steps;
    $('#rsWorkers').value = s.workers;
}
document.addEventListener('DOMContentLoaded', () => {
    fill(window.ROBOT_SETTINGS_INIT.settings || {});
    $('#rsSave').addEventListener('click', async () => {
        const btn = $('#rsSave');
        btn.disabled = true;
        try {
            const r = await api('/api/catalog/robot-settings', {
                max_per_user: $('#rsMax').value, min_interval_hours: $('#rsInterval').value,
                max_steps: $('#rsSteps').value, workers: $('#rsWorkers').value });
            fill(r.settings || {});
            if (r.updated_at) $('#rsNote').textContent = `${r.updated_at.replace('T', ' ')} に ${r.updated_by} が保存`;
            toast('保存しました。すぐ効きます。');
        } catch (e) { toast(e.message, 'err', 9000); }
        btn.disabled = false;
    });
});
})();

// ===== パーソナライズの決めごと（window.MEMORY_SETTINGS_INIT がある画面だけ動く。管理者） =====
(() => {
if (!window.MEMORY_SETTINGS_INIT) return;
function fill(s) {
    $('#msEnabled').checked = !!s.enabled;
    $('#msModel').value = s.model || '';
    if ($('#msModel').value !== (s.model || '')) {     // 一覧に無いモデルが保存されていたら、選べるように足す
        $('#msModel').append(el('option', { value: s.model, selected: 'selected' }, s.model));
    }
    $('#msMax').value = s.max_chars;
}
document.addEventListener('DOMContentLoaded', () => {
    fill(window.MEMORY_SETTINGS_INIT.settings || {});
    $('#msSave').addEventListener('click', async () => {
        const btn = $('#msSave'); btn.disabled = true;
        try {
            const r = await api('/api/catalog/memory-settings', {
                enabled: $('#msEnabled').checked, model: $('#msModel').value, max_chars: $('#msMax').value });
            fill(r.settings || {});
            if (r.updated_at) $('#msNote').textContent = `${r.updated_at.replace('T', ' ')} に ${r.updated_by} が保存`;
            toast('保存しました。すぐ効きます（メニューの表示は次に画面を開いたときに変わります）。');
        } catch (e) { toast(e.message, 'err', 9000); }
        btn.disabled = false;
    });
});
})();

// ===== 画面の決めごと（window.DISPLAY_SETTINGS_INIT がある画面だけ動く。管理者） =====
(() => {
if (!window.DISPLAY_SETTINGS_INIT) return;
function fill(s) {
    $('#dsSql').checked = !!s.fold_sql;
    $('#dsSources').checked = !!s.fold_sources;
    $('#dsProposals').checked = !!s.fold_proposals;
}
document.addEventListener('DOMContentLoaded', () => {
    fill(window.DISPLAY_SETTINGS_INIT.settings || {});
    $('#dsSave').addEventListener('click', async () => {
        const btn = $('#dsSave'); btn.disabled = true;
        try {
            const r = await api('/api/catalog/chat-display', {
                fold_sql: $('#dsSql').checked, fold_sources: $('#dsSources').checked,
                fold_proposals: $('#dsProposals').checked });
            fill(r.settings || {});
            if (r.updated_at) $('#dsNote').textContent = `${r.updated_at.replace('T', ' ')} に ${r.updated_by} が保存`;
            toast('保存しました。利用者がマイエージェントの画面を次に開いたとき（再読み込み）から効きます。');
        } catch (e) { toast(e.message, 'err', 9000); }
        btn.disabled = false;
    });
    // カタログに登録できる人（1行に1人）
    $('#ccUsers').value = (window.DISPLAY_SETTINGS_INIT.contrib || []).join('\n');
    $('#ccSave').addEventListener('click', async () => {
        const btn = $('#ccSave'); btn.disabled = true;
        try {
            // 1行に1人が基本だが、読点や空白で区切って書かれても1人ずつに分ける（IDに空白は入らない）
            const users = $('#ccUsers').value.split(/[\r\n,、\s]+/).map(s => s.trim()).filter(Boolean);
            const r = await api('/api/catalog/contrib-users', { users });
            $('#ccUsers').value = (r.users || []).join('\n');
            if (r.updated_at) $('#ccNote').textContent = `${r.updated_at.replace('T', ' ')} に ${r.updated_by} が保存（${(r.users || []).length} 人）`;
            toast('保存しました。利用者がマイエージェントの画面を次に開いたとき（再読み込み）から効きます。');
        } catch (e) { toast(e.message, 'err', 9000); }
        btn.disabled = false;
    });
});
})();

// ===== パーソナライズの画面（window.MEMORY_INIT がある画面だけ動く） =====
(() => {
if (!window.MEMORY_INIT) return;
/* 本文は1つのテキスト。保存はボタンで（打っている途中でAIの書き足しが来ても、消さずに知らせる）。 */
let m = window.MEMORY_INIT;
let dirty = false;

function show() {
    const box = document.querySelector('.memedit');
    const off = !m.enabled;                       // 管理者が機能ごと止めている
    $('#memState').textContent = off ? '機能停止中' : (m.on ? '覚えています' : '停止中');
    $('#memToggle').textContent = m.on ? '覚えない' : '覚える';
    $('#memToggle').classList.toggle('hidden', off);   // 押しても何も変わらないので出さない
    $('#memOffNote').classList.toggle('hidden', !off);
    $('#memBroken').classList.toggle('hidden', !m.broken);
    box.classList.toggle('is-off', off || !m.on);
    const len = $('#memText').value.length;
    $('#memCount').textContent = `${len} / ${m.max_chars} 文字`
        + (len > m.max_chars ? '（上限を超えた分は保存時に切ります）' : '');
    $('#memNote').textContent = m.updated_at ? `最終更新 ${m.updated_at.replace('T', ' ')}` : 'まだありません';
}

document.addEventListener('DOMContentLoaded', () => {
    $('#memText').value = m.text || '';
    show();
    $('#memText').addEventListener('input', () => { dirty = true; show(); });
    $('#memSave').addEventListener('click', async () => {
        const btn = $('#memSave'); btn.disabled = true;
        const sent = $('#memText').value;
        try {
            m = { ...m, ...(await api('/api/memory/save', { text: sent })) };
            $('#memText').value = m.text || ''; dirty = false; show();
            const cut = sent.trim().length > (m.text || '').length;
            toast(cut ? `保存しました（上限 ${m.max_chars} 文字を超えた分は切りました）。`
                      : (m.enabled ? '保存しました。次の質問からAIに渡ります。'
                                   : '保存しました（いまは機能が止まっているので、AIには渡りません）。'),
                  cut ? 'warn' : 'ok', cut ? 9000 : 4000);
        } catch (e) { toast(e.message, 'err', 9000); }
        btn.disabled = false;
    });
    $('#memClear').addEventListener('click', async () => {
        if (!confirm('パーソナライズの内容を全部消しますか？（元に戻せません）')) return;
        try {
            m = { ...m, ...(await api('/api/memory/clear')) };
            $('#memText').value = ''; dirty = false; show();
            toast('全部消しました。');
        } catch (e) { toast(e.message, 'err', 9000); }
    });
    $('#memToggle').addEventListener('click', async () => {
        try {
            m = { ...m, ...(await api('/api/memory/toggle', { on: !m.on })) };
            show();
            toast(m.on ? '覚えるのを再開しました。' : '覚えるのをやめました（いまの本文もAIに渡しません）。');
        } catch (e) { toast(e.message, 'err', 9000); }
    });
    // 別の画面で答えが返って本文が変わったら、打っている途中でなければ差し替える。
    // 印（時刻）は秒までしか無いので、本文そのものを比べる
    setInterval(async () => {
        try {
            const r = await api('/api/memory', undefined, 'GET');
            if ((r.text || '') === (m.text || '')) { m = { ...m, ...r }; return; }
            const grew = (r.text || '').startsWith((m.text || '').slice(0, 40)) && (r.text || '').length > (m.text || '').length;
            m = { ...m, ...r };
            const what = grew ? 'AIがパーソナライズに書き足しました。' : 'AIがパーソナライズを書き直しました。';
            if (!dirty) { $('#memText').value = m.text || ''; show(); toast(what); }
            else toast(what + 'いま打っている内容を保存すると上書きになります（画面を読み直すと新しい本文が見えます）。', 'warn', 9000);
        } catch (_) { /* 取れないときは何もしない */ }
    }, 20000);
});
})();

// ===== 出力の画面（window.OUTPUT_INIT がある画面だけ動く） =====
(() => {
if (!window.OUTPUT_INIT) return;
/* 出力先フォルダの設定。保存は書けるかをサーバが確かめてから。 */
document.addEventListener('DOMContentLoaded', () => {
    const save = $('#outSave');
    if (!save) return;
    const show = st => {
        $('#outStatus').textContent = st.message + (st.source ? `（${st.source}の設定）` : '');
        $('#outStatus').dataset.ok = st.ok ? 'true' : 'false';
        const b = $('#outBadge');
        b.textContent = st.ok ? '使えます' : (st.path ? '問題あり' : '未設定');
        b.className = 'badge ' + (st.ok ? 'badge--ok' : (st.path ? 'badge--err' : ''));
        $('#outDir').value = st.path || '';
    };
    const submit = async path => {
        save.disabled = true;
        try {
            const st = await api('/api/output-dir', { path });
            show(st);
            toast(path ? `出力先フォルダを保存しました: ${st.path}` : '出力先フォルダを外しました。');
        } catch (e) { toast(e.message, 'err', 9000); }
        save.disabled = false;
    };
    save.addEventListener('click', () => submit($('#outDir').value.trim()));
    $('#outDir').addEventListener('keydown', ev => { if (ev.key === 'Enter') submit($('#outDir').value.trim()); });
    $('#outClear').addEventListener('click', () => {
        if (!confirm('出力先フォルダを外しますか？（フォルダへの出力ができなくなります。ダウンロードは今までどおり）')) return;
        submit('');
    });
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
            + 'マイエージェントのAIは、質問の内容に応じてこの中から調べ先を選びます。')
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
    // 文面の決まり（打っている最中は上書きしない）
    if (document.activeElement !== $('#bodyHeader')) $('#bodyHeader').value = s.body_header || '';
    $('#showSender').checked = s.show_sender !== false;
    ['#bodyHeader', '#showSender'].forEach(x => { $(x).disabled = !editable(); });
    $('#bodySample').textContent = s.sample_body || '';
    $('#dryNote').replaceChildren(s.dry_run
        ? el('div', { class: 'alert alert--info' },
            'テスト送信モードです。マイエージェントの「送信」を押しても外にはメールが出ず、'
            + '組み立てた内容の確認だけを行います。動作を確かめてから外してください。')
        : el('div', { class: 'alert alert--warn' },
            '本番送信モードです。マイエージェントの「送信」を押すと実際にメールが送られます。'));

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
    $('#bodyHeader').addEventListener('input', ev => { state.body_header = ev.target.value; });
    $('#showSender').addEventListener('change', ev => { state.show_sender = ev.target.checked; });
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
                body_header: $('#bodyHeader').value,
                show_sender: $('#showSender').checked,
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
   マイエージェントのプルダウンに出す候補・既定・画像判定キーワードを決める。 */

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
            + 'モデル一覧の取得とマイエージェントは動きません。'));
    }
    // いまマイエージェントに何が出ているかを、実態のまま出す。
    // ここがずれていると「設定が効いていない」ように見える。
    const eff = state.effective || [];
    if (state.source === 'admin') {
        box.append(el('div', { class: 'alert alert--info' },
            `この画面の設定が効いています。マイエージェントのプルダウンには `
            + `${eff.length} 件（${eff.join('、')}）が出ます。`));
    } else if (state.source === 'env') {
        box.append(el('div', { class: 'alert alert--info' },
            'いまは env の OPENAI_MODELS をそのまま使っています'
            + `（${eff.join('、')}）。ここで保存すると、以後はこの画面の内容が優先されます。`));
    } else {
        box.append(el('div', { class: 'alert alert--warn' },
            '候補をまだ決めていません。いまマイエージェントに出るのは、既定のモデルと'
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
                `APIが返した ${cat.length} 件です。チェックしたものだけがマイエージェントに出ます。`)),
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
