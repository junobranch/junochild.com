# -*- coding: utf-8 -*-
"""連携機関の声 vol.1（あーるいー 石田様）のページを生成する。
共通ヘッダー・フッターは column/index.html（絶対パス化済み）から取り出す。
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
SITE = 'https://junochild.com'
URL = SITE + '/voices/re-ishida.html'
DATE = '2026-11-11'
TITLE = '「できることは、きっと多い」——相談支援事業所あーるいー 石田玲弥さんに聞く、医療と福祉がつながる支援'
DESC = '連携機関の声 vol.1。名古屋市天白区の相談支援事業所あーるいー・石田玲弥さん（相談支援専門員）に、子どもと家族の支援への思いと、医療と福祉の連携について伺いました。'

src = open('column/index.html', encoding='utf-8').read()
head_top = src[:src.index('  <title>')]
links = src[src.index('  <link rel="preconnect"'):src.index('  <style>')]
nav = src[src.index('<nav class="nav"'):src.index('</nav>') + len('</nav>')]
nav = nav.replace(' aria-current="page"', '')
nav = nav.replace('<a href="/for-professionals.html" class="nav__link">', '<a href="/for-professionals.html" class="nav__link" aria-current="page">', 1)
tail = src[src.index('<footer'):]

ld = {
    '@context': 'https://schema.org', '@type': 'Article',
    'headline': '連携機関の声 vol.1 相談支援事業所あーるいー 石田玲弥さん',
    'description': DESC, 'datePublished': DATE, 'dateModified': DATE,
    'image': SITE + '/assets/img/voices/re-ishida-1.jpg',
    'author': {'@type': 'Organization', 'name': 'こども訪問看護ステーションJuno'},
    'publisher': {'@type': 'Organization', 'name': 'こども訪問看護ステーションJuno', 'url': SITE + '/'},
    'inLanguage': 'ja', 'mainEntityOfPage': URL,
}

style = '''  <style>
    /* 連携機関の声：インタビュー記事 */
    .vc-wrap { max-width: 760px; margin-inline: auto; }
    .vc-back { display: inline-flex; align-items: center; gap: 6px; color: var(--juno-primary-dark); font-size: 0.875rem; font-weight: 600; margin-bottom: 28px; }
    .vc-back:hover { text-decoration: underline; }
    .vc-meta { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; margin-bottom: 14px; }
    .vc-tag { display: inline-block; font-size: 0.75rem; font-weight: 700; color: var(--juno-primary-dark); background: var(--juno-primary-light); border-radius: 100px; padding: 3px 12px; }
    .vc-date { font-family: 'Nunito', sans-serif; font-size: 0.85rem; color: var(--juno-text-sub); }
    .vc-title { font-size: 1.55rem; font-weight: 700; line-height: 1.6; color: var(--juno-text); margin-bottom: 28px; text-wrap: balance; }
    .vc-title span { display: block; font-size: 1.05rem; font-weight: 600; color: var(--juno-text-sub); margin-top: 8px; }
    .vc-photo { margin: 0 0 32px; }
    .vc-photo img { display: block; width: 100%; height: auto; border-radius: 14px; }
    .vc-photo--main img { aspect-ratio: 4 / 3; object-fit: cover; }
    .vc-photo--sub { margin: 36px auto; max-width: 560px; }
    .vc-photo figcaption { font-size: 0.8rem; color: var(--juno-text-sub); margin-top: 8px; text-align: center; }
    .vc-lead { font-size: 1rem; line-height: 2; color: var(--juno-text); background: var(--juno-primary-light); border-radius: 12px; padding: 20px 24px; margin-bottom: 8px; }
    .vc-h2 { font-size: 1.2rem; font-weight: 700; line-height: 1.6; color: var(--juno-text); margin: 48px 0 16px; padding-left: 12px; border-left: 3px solid var(--juno-primary); }
    .vc-p { font-size: 1rem; line-height: 2.05; color: var(--juno-text); margin-bottom: 1.1em; }
    .vc-after { margin-top: 56px; padding: 26px 28px; background: var(--juno-bg); border: 1px solid var(--juno-border); border-radius: 14px; }
    .vc-after .vc-h2 { margin-top: 0; }
    .vc-profile { margin-top: 40px; border-top: 1px solid var(--juno-border); padding-top: 20px; }
    .vc-profile__name { font-size: 1rem; font-weight: 700; color: var(--juno-text); margin-bottom: 8px; }
    .vc-profile dl { display: grid; grid-template-columns: auto 1fr; gap: 6px 16px; font-size: 0.9rem; line-height: 1.7; }
    .vc-profile dt { color: var(--juno-text-sub); white-space: nowrap; }
    .vc-profile dd { margin: 0; color: var(--juno-text); }
    .vc-links { margin-top: 36px; display: flex; flex-direction: column; gap: 10px; font-size: 0.9rem; }
    .vc-links a { color: var(--juno-primary-dark); font-weight: 600; border-bottom: 1px solid var(--juno-primary); align-self: flex-start; }
    @media (max-width: 768px) {
      .vc-title { font-size: 1.3rem; }
      .vc-title span { font-size: 0.95rem; }
      .vc-lead, .vc-after { padding: 18px 18px; }
    }
  </style>
'''


def P(t):
    return f'      <p class="vc-p">{t}</p>\n'


def H(t):
    return f'      <h2 class="vc-h2">{t}</h2>\n'


def IMG(n, alt, sub=True):
    cls = 'vc-photo vc-photo--sub' if sub else 'vc-photo vc-photo--main'
    lazy = ' loading="lazy"' if sub else ''
    h = 901 if n == 2 else 900
    return f'      <figure class="{cls}"><img src="/assets/img/voices/re-ishida-{n}.jpg" alt="{alt}" width="1200" height="{h}"{lazy}></figure>\n'


body = (
    IMG(1, 'インタビューに答える、相談支援事業所あーるいーの石田玲弥さん', sub=False)
    + '      <p class="vc-lead">お子さまやご家族を支えるのは、ひとつの事業所だけではありません。Juno と連携してくださっている地域の支援者の方に、日々の思いを伺いました。第1回は、名古屋市天白区で相談支援事業所あーるいーを運営する、石田玲弥さんです。</p>\n'
    + H('大人の生活支援から、子どもの相談へ')
    + P('相談支援専門員として、もともとはグループホーム探しや、日々の暮らし、お仕事のことなど、大人の方の相談を中心に受けてきました。就労移行支援や就労継続支援A型・B型、職業訓練校など、働くための道を一緒に考えることも多いです。')
    + P('お子さんの相談に力を入れるようになったのは、身近に発達の支援が必要な人がいたことがきっかけです。知れば知るほど、早い時期に周りの大人がどう関わるかで、その後が大きく変わると感じるようになりました。')
    + H('叱られてきた子に、「できることは多いよ」と伝えたい')
    + P('私のところに来るお子さんは、自信をなくした状態で出会うことが少なくありません。たくさん叱られてきた歴史を、小さな体に抱えているんだと思います。')
    + P('だから最初に伝えたいのは、「いやいや、できることは多いよ」ということです。こうして話ができる、聞かれたことに答えられる。それだけでも大きいんです。好きなこと、得意なことは、掘り下げればどんどん出てきます。そこに目を向けて引き出すことを、一番大切にしています。')
    + P('親御さんとも、じっくり話すようにしています。親としての願いがあるからこそ、お子さんのしんどさが見えにくくなることもある。第三者だからこそ伝えられることもあるので、一人ひとりに時間をかけて向き合っています。')
    + H('つまずきが表に出やすいのは、小学校に入ってから')
    + P('ご相談で多いのは、癇癪、言葉の遅れ、落ち着きのなさ、勉強の困りごとなどです。ただ、根っこをたどると、親子のコミュニケーションがうまくかみ合わず、それが癇癪につながっていることもよくあります。')
    + P('時期でいえば、小学1年生の夏休み明けや、2年生の終わりの進級前後。「このまま通常級でいけるのか」「支援級を考えたほうがいいのか」と悩まれるタイミングで、相談に来られる方が多いです。区役所や基幹相談支援センターを回ったうえで、「ほかに何かできることはないの？」と訪ねてこられるご家族もいます。')
    + IMG(2, '相談支援事業所あーるいーの石田玲弥さん')
    + H('訪問看護は、まだ「知られていない社会資源」')
    + P('訪問看護は、多くのご家族にほとんど知られていません。医療だからお金がかかるのでは、という不安もありますし、子どもの医療証で使えることもあまり知られていません。相談の中で私から聞いて、初めて知ったという方も少なくありません。')
    + P('その中で、今は安心して Juno さんにお願いしています。一番ありがたいのは、お子さんの得意なこと・苦手なことを、とても丁寧に分析してくださることです。お父さん、お母さんでも気づけなかったところまで見つけてくれる。それをもとに、私も「次はこんな支援を使ってみませんか」と提案しやすくなります。')
    + P('相談支援専門員は、ご家庭に伺う頻度に限りがあります。だからこそ、日々の暮らしの中に入って、こまやかに関わってくれる存在は心強いです。支援者の目で見た詳細な記録があることで、親御さんが「自分たちの関わり方は合っていたんだ」とほっとされる場面もたくさん見てきました。相談を受ける中でも、Juno さんの評価はとても高いんですよ。')
    + H('つながりが切れないように')
    + P('以前、福祉サービスの利用が途切れてしまうかもしれない、というご家庭がありました。お母さんにとっては、子育ての相談先がなくなってしまうかもしれない状況です。そのとき、「医療として看護師さんとつながっておけば、関わりは切れない」と考えて、Juno さんを紹介し、急いで動いてもらいました。')
    + P('お母さんが安定していないと、お子さんの支援はうまくいきません。家族が孤立しないように、医療と福祉でそれぞれの得意を持ち寄って支えていく。そうした連携を、これからも大切にしたいと思っています。')
    + IMG(3, 'お子さんと家族への思いを語る石田玲弥さん')
    + H('困っている方へ')
    + P('いつも皆さんにお伝えしているのは、「自分の気持ちを大切にしてね」ということです。親から言われたから、周りに言われたから、ではなく、自分がやりたいと思ったことを選んでほしい。学校のことも、お仕事のことも同じです。')
    + P('自分で決めて動けたことは、それだけで大きな一歩です。迷ったときは、一人で抱え込まずに、まずは相談してみてください。')
    + '      <div class="vc-after">\n'
    + H('取材を終えて（Juno より）')
    + P('取材は、石田さんの愛車の話から始まりました。お子さんを後ろに乗せて走れるように、バイクを乗り換えたそうです。うれしそうに話すその表情に、ご家族を大切にされる方なのだと感じました。')
    + P('お話を伺う中で何度も感じたのは、石田さんのまなざしの優しさです。お子さまの「できること」に目を向け、親御さんの迷いや不安にもそっと寄り添う。その一方で、「自分の気持ちを大切にしてほしい」という言葉には、どんなときもご本人の思いを真ん中に置く、揺るがない芯が通っていました。')
    + P('「その子のできること」から出発する石田さんの姿勢は、Juno が大切にしている考え方とも重なります。また石田さんのもとには、日々たくさんのご相談が寄せられています。Juno にご紹介いただいたご家族のお話からも、石田さんへの信頼の厚さが伝わってきます。地域で頼りにされている相談支援専門員だと、あらためて実感しました。')
    + P('医療と福祉が、それぞれの立場からできることを持ち寄れば、ご家族が一人で抱え込まずにすむ地域に近づけるはずです。Juno はこれからも、地域の社会資源同士として連携を深めていきます。')
    + '      </div>\n'
    + '''      <div class="vc-profile">
        <p class="vc-profile__name">相談支援事業所あーるいー</p>
        <dl>
          <dt>運営</dt><dd>合同会社Re</dd>
          <dt>代表</dt><dd>石田 玲弥（相談支援専門員・介護福祉士）</dd>
          <dt>所在地</dt><dd>〒468-0067 名古屋市天白区池見1丁目115-1 池見グリーンハイツ102号室</dd>
        </dl>
      </div>
'''
)

page = (head_top
        + '  <title>連携機関の声 vol.1 相談支援事業所あーるいー 石田玲弥さん | こども訪問看護ステーションJuno</title>\n'
        + f'  <meta name="description" content="{DESC}">\n'
        + f'  <link rel="canonical" href="{URL}">\n'
        + '  <meta property="og:image" content="' + SITE + '/assets/img/voices/re-ishida-1.jpg">\n'
        + links
        + '  <script type="application/ld+json">\n  ' + json.dumps(ld, ensure_ascii=False, indent=2).replace('\n', '\n  ') + '\n  </script>\n'
        + style + '</head>\n<body>\n\n' + nav + '\n\n'
        + '<section class="section" style="padding-top:48px;">\n  <div class="container">\n    <div class="vc-wrap">\n'
        + '      <a href="/for-professionals.html" class="vc-back">← 関連機関との連携へ</a>\n'
        + '      <article>\n'
        + f'      <div class="vc-meta"><span class="vc-tag">連携機関の声 vol.1</span><span class="vc-date"><time datetime="{DATE}">{DATE.replace("-", ".")}</time></span></div>\n'
        + '      <h1 class="vc-title">「できることは、きっと多い」<span>相談支援事業所あーるいー 石田玲弥さんに聞く、医療と福祉がつながる支援</span></h1>\n'
        + body
        + '      </article>\n'
        + '      <div class="vc-links">\n'
        + '        <a href="/for-professionals.html">関連機関との連携について ＞</a>\n'
        + '        <a href="/service.html">Junoの事業内容・サービス ＞</a>\n'
        + '      </div>\n'
        + '    </div>\n  </div>\n</section>\n\n'
        + tail)
open('voices/re-ishida.html', 'w', encoding='utf-8').write(page)
print('written voices/re-ishida.html', len(page))
