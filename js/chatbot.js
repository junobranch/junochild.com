/* =============================================
   Juno チャットボット（キーワード対応版）
   ============================================= */

(function () {

  /* -----------------------------------------------
   * 回答データ
   * ----------------------------------------------- */
  const RESPONSES = {
    service: {
      message: 'Junoでは、0〜15歳のお子さまを対象に、ご自宅への訪問看護を提供しています。\n\nASD・ADHD・DCD・不登校など、発達に関わるさまざまな困りごとに対応しており、診断がなくてもご利用いただけます。\n\n詳しくはスタッフが直接ご説明しますね。',
      choices: [
        { label: '費用・保険について',   next: 'cost' },
        { label: '利用の流れを知りたい', next: 'flow' },
        { label: '相談してみる',       url:  'https://forms.gle/hnKDimt3xWUCR43N7' },
        { label: 'メニューに戻る',       next: 'welcome' },
      ],
    },
    cost: {
      message: '医療保険が適用されるため、利用者の方の費用負担は基本的にゼロです。\n\n※ 所得や保険の状況によって異なる場合があります。詳しくはお気軽にご相談ください。',
      choices: [
        { label: 'サービス内容を知りたい', next: 'service' },
        { label: '相談してみる',         url:  'https://forms.gle/hnKDimt3xWUCR43N7' },
        { label: 'メニューに戻る',         next: 'welcome' },
      ],
    },
    area: {
      message: '現在の対応エリアは以下の通りです。\n\n📍 名古屋市緑区\n📍 名古屋市天白区\n📍 名古屋市瑞穂区\n📍 東郷町\n\nエリア外の場合も、まずはご相談ください。',
      choices: [
        { label: 'サービス内容を知りたい', next: 'service' },
        { label: '相談してみる',         url:  'https://forms.gle/hnKDimt3xWUCR43N7' },
        { label: 'メニューに戻る',         next: 'welcome' },
      ],
    },
    flow: {
      message: 'ご利用開始までの流れです。\n\n① お問い合わせ（見学・相談も無料）\n② 初回面談（訪問またはオンライン）\n③ いまここシート実施\n④ 訪問開始\n\nまずは気軽にご連絡ください😊',
      choices: [
        { label: 'いまここシートとは？', url:  'imacoco.html' },
        { label: '相談してみる',       url:  'https://forms.gle/hnKDimt3xWUCR43N7' },
        { label: 'メニューに戻る',       next: 'welcome' },
      ],
    },
    imahere: {
      message: '「いまここシート」は、Junoが独自に開発した発達アセスメントツールです。\n\n感覚・運動・言語・情動など多角的な視点でお子さまの現在地を確認し、支援の方針を立てるために使います。\n\n詳しくは専用ページをご覧ください。',
      choices: [
        { label: 'いまここシートを詳しく見る', url:  'imacoco.html' },
        { label: '利用の流れを知りたい',       next: 'flow' },
        { label: 'メニューに戻る',             next: 'welcome' },
      ],
    },
    grey: {
      message: 'グレーゾーンとは、発達障害の診断基準には満たないものの、日常生活に困りごとがある状態を指すことが多いです。\n\nJunoでは「診断がない」「グレーかもしれない」という段階からご利用いただけます。まずはお気軽にご相談ください。',
      choices: [
        { label: 'サービス内容を知りたい', next: 'service' },
        { label: '費用・保険について',     next: 'cost' },
        { label: '相談してみる',         url:  'https://forms.gle/hnKDimt3xWUCR43N7' },
        { label: 'メニューに戻る',         next: 'welcome' },
      ],
    },
    futoko: {
      message: '不登校のお子さまへの支援も行っています。\n\n学校に行けない背景には、感覚過敏・不安・睡眠リズムの乱れなど様々な要因があります。Junoでは医療的視点からその背景を整理し、ご家庭でできる関わり方を一緒に考えます。',
      choices: [
        { label: 'サービス内容を知りたい', next: 'service' },
        { label: '相談してみる',         url:  'https://forms.gle/hnKDimt3xWUCR43N7' },
        { label: 'メニューに戻る',         next: 'welcome' },
      ],
    },
    recruit: {
      message: 'Junoでは現在、こどもの発達支援に関心のある看護師さんを募集しています。\n\n正規・非常勤ともに歓迎です。まずはカジュアル面談（オンラインOK）からどうぞ。',
      choices: [
        { label: '採用ページを見る', url:  'recruit.html' },
        { label: 'メニューに戻る',   next: 'welcome' },
      ],
    },
    contact: {
      message: '以下のフォームからお問い合わせください。見学・相談も無料です。スタッフが丁寧にご対応します😊\n\nお電話でのご相談もどうぞ。\n📞 052-627-3959（8:30〜17:30 / 土日定休）',
      choices: [
        { label: 'お問い合わせフォームへ', url:  'https://forms.gle/hnKDimt3xWUCR43N7' },
        { label: 'メニューに戻る',         next: 'welcome' },
      ],
    },
    welcome: {
      message: 'こんにちは！Junoの案内窓口です😊\n\nご質問をテキストで入力いただくか、下のボタンから選んでください。',
      choices: [
        { label: 'サービスについて知りたい', next: 'service' },
        { label: '費用・保険について',       next: 'cost' },
        { label: '対応エリアを知りたい',     next: 'area' },
        { label: '利用の流れを知りたい',     next: 'flow' },
        { label: '求人・採用について',       next: 'recruit' },
        { label: '相談してみる',           next: 'contact' },
      ],
    },
    fallback: {
      messageHTML: '申し訳ありません。こちらはご案内チャットのため、いただいたご質問にはうまくお答えできませんでした。\n\n「気になること」「聞いてみたいこと」など、どんな些細なことでもスタッフが直接お受けいたします。\n\n👉 <a href="https://forms.gle/hnKDimt3xWUCR43N7" target="_blank" rel="noopener noreferrer" style="color:#0ABAB5;font-weight:700;text-decoration:underline;">相談してみる</a>\n📞 052-627-3959（8:30〜17:30 / 土日定休）',
      choices: [
        { label: 'メニューに戻る', next: 'welcome' },
      ],
    },
  };

  /* -----------------------------------------------
   * キーワードマッピング
   * ----------------------------------------------- */
  const KEYWORD_MAP = [
    { keys: ['サービス','訪問看護','支援','内容','何をして','どんなこと','ASD','ADHD','DCD','自閉','多動','発達障害','神経発達','診断'], node: 'service' },
    { keys: ['費用','保険','医療保険','お金','いくら','無料','負担','ゼロ','タダ'], node: 'cost' },
    { keys: ['エリア','場所','地域','どこ','緑区','天白区','瑞穂区','東郷','名古屋'], node: 'area' },
    { keys: ['流れ','手順','手続き','始め','利用開始','申し込み','どうすれば'], node: 'flow' },
    { keys: ['いまここ','シート','アセスメント','評価'], node: 'imahere' },
    { keys: ['グレーゾーン','グレー','診断なし','診断がない','気になる','気になって'], node: 'grey' },
    { keys: ['不登校','登校','学校','行けない','行かない'], node: 'futoko' },
    { keys: ['採用','求人','働く','看護師','就職','転職','募集'], node: 'recruit' },
    { keys: ['相談','問い合わせ','連絡','話したい','聞きたい'], node: 'contact' },
  ];

  function matchKeyword(text) {
    const normalized = text.replace(/\s/g, '');
    for (const entry of KEYWORD_MAP) {
      if (entry.keys.some(k => normalized.includes(k))) {
        return entry.node;
      }
    }
    return null;
  }

  /* -----------------------------------------------
   * DOM組み立て
   * ----------------------------------------------- */
  function buildUI() {
    const wrap = document.createElement('div');
    wrap.id = 'juno-chat';
    wrap.innerHTML = `
      <button class="juno-chat__toggle" aria-label="チャットで気軽に相談する" aria-expanded="false">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
        </svg>
        <span>ちょっと聞いてみる</span>
      </button>
      <div class="juno-chat__window" role="dialog" aria-label="Junoに相談する" hidden>
        <div class="juno-chat__header">
          <span>Junoに聞いてみる</span>
          <button class="juno-chat__close" aria-label="閉じる">✕</button>
        </div>
        <div class="juno-chat__body" id="juno-chat-body"></div>
        <div class="juno-chat__input-wrap">
          <input type="text" id="juno-chat-input" placeholder="ご質問をどうぞ…" autocomplete="off" maxlength="200">
          <button id="juno-chat-send" aria-label="送信">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
          </button>
        </div>
        <div class="juno-chat__footer" id="juno-chat-choices"></div>
      </div>
    `;
    document.body.appendChild(wrap);

    const style = document.createElement('style');
    style.textContent = `
      #juno-chat { position: fixed; bottom: 100px; right: 32px; z-index: 300; font-family: 'Noto Sans JP', sans-serif; }
      .juno-chat__toggle {
        display: flex; align-items: center; gap: 8px;
        background: #0ABAB5; color: #fff;
        border: none; border-radius: 50px; padding: 12px 20px;
        font-size: 0.875rem; font-weight: 700; cursor: pointer;
        box-shadow: 0 6px 24px rgba(10,186,181,0.4);
        transition: all 0.25s ease;
      }
      .juno-chat__toggle:hover { background: #08918D; transform: translateY(-2px); }
      .juno-chat__window {
        position: absolute; bottom: 60px; right: 0;
        width: 360px; max-height: 540px;
        background: #fff; border-radius: 16px;
        box-shadow: 0 16px 48px rgba(10,186,181,0.2);
        display: flex; flex-direction: column; overflow: hidden;
        animation: chatSlideUp 0.3s ease;
      }
      .juno-chat__window[hidden] { display: none; }
      @keyframes chatSlideUp { from { opacity:0; transform:translateY(20px); } to { opacity:1; transform:translateY(0); } }
      .juno-chat__header {
        background: #0ABAB5; color: #fff;
        display: flex; justify-content: space-between; align-items: center;
        padding: 14px 20px; font-weight: 700; font-size: 0.95rem;
        flex-shrink: 0;
      }
      .juno-chat__close { background: none; border: none; color: #fff; font-size: 1rem; cursor: pointer; padding: 4px; }
      .juno-chat__body {
        flex: 1; overflow-y: auto; padding: 16px;
        display: flex; flex-direction: column; gap: 10px;
        min-height: 160px;
      }
      .juno-chat__msg {
        background: #E6F9F8; border-radius: 4px 16px 16px 16px;
        padding: 10px 14px; font-size: 0.83rem; line-height: 1.8;
        white-space: pre-wrap; max-width: 88%; align-self: flex-start;
      }
      .juno-chat__msg--user {
        background: #0ABAB5; color: #fff;
        border-radius: 16px 4px 16px 16px;
        align-self: flex-end; text-align: right;
      }
      .juno-chat__typing {
        background: #E6F9F8; border-radius: 4px 16px 16px 16px;
        padding: 10px 16px; font-size: 0.83rem; align-self: flex-start;
        display: flex; gap: 4px; align-items: center;
      }
      .juno-chat__typing span {
        width: 7px; height: 7px; background: #0ABAB5; border-radius: 50%;
        animation: typingBounce 1.2s infinite ease-in-out;
        display: inline-block;
      }
      .juno-chat__typing span:nth-child(2) { animation-delay: 0.2s; }
      .juno-chat__typing span:nth-child(3) { animation-delay: 0.4s; }
      @keyframes typingBounce { 0%,60%,100%{transform:translateY(0)} 30%{transform:translateY(-5px)} }
      .juno-chat__input-wrap {
        display: flex; align-items: center; gap: 8px;
        padding: 10px 12px; border-top: 1px solid #D0ECEA; flex-shrink: 0;
        background: #fff;
      }
      #juno-chat-input {
        flex: 1; border: 1.5px solid #D0ECEA; border-radius: 50px;
        padding: 8px 14px; font-size: 0.82rem; outline: none;
        font-family: inherit; transition: border-color 0.2s;
        background: #FAFEFE;
      }
      #juno-chat-input:focus { border-color: #0ABAB5; }
      #juno-chat-send {
        background: #0ABAB5; border: none; border-radius: 50%;
        width: 36px; height: 36px; display: flex; align-items: center; justify-content: center;
        cursor: pointer; color: #fff; flex-shrink: 0; transition: background 0.2s;
      }
      #juno-chat-send:hover { background: #08918D; }
      .juno-chat__footer {
        padding: 8px 12px 12px; display: flex; flex-direction: column; gap: 6px;
        border-top: 1px solid #D0ECEA; flex-shrink: 0; background: #fff;
        max-height: 180px; overflow-y: auto;
      }
      .juno-chat__choice {
        background: #fff; border: 1.5px solid #0ABAB5; color: #0ABAB5;
        border-radius: 50px; padding: 7px 14px; font-size: 0.78rem; font-weight: 700;
        cursor: pointer; text-align: left; transition: all 0.2s ease; font-family: inherit;
      }
      .juno-chat__choice:hover { background: #0ABAB5; color: #fff; }
      @media (max-width: 480px) {
        #juno-chat { right: 16px; bottom: 80px; }
        .juno-chat__window { width: calc(100vw - 32px); right: 0; }
      }
    `;
    document.head.appendChild(style);
  }

  /* -----------------------------------------------
   * メッセージ・UI操作
   * ----------------------------------------------- */
  function addMessage(text, isUser = false, isHTML = false) {
    const body = document.getElementById('juno-chat-body');
    const msg = document.createElement('div');
    msg.className = 'juno-chat__msg' + (isUser ? ' juno-chat__msg--user' : '');
    if (isHTML) {
      msg.innerHTML = text.replace(/\n/g, '<br>');
    } else {
      msg.textContent = text;
    }
    body.appendChild(msg);
    body.scrollTop = body.scrollHeight;
  }

  function showTyping() {
    const body = document.getElementById('juno-chat-body');
    const el = document.createElement('div');
    el.className = 'juno-chat__typing';
    el.id = 'juno-typing';
    el.innerHTML = '<span></span><span></span><span></span>';
    body.appendChild(el);
    body.scrollTop = body.scrollHeight;
  }

  function removeTyping() {
    const el = document.getElementById('juno-typing');
    if (el) el.remove();
  }

  function showChoices(choices) {
    const footer = document.getElementById('juno-chat-choices');
    footer.innerHTML = '';
    choices.forEach(choice => {
      const btn = document.createElement('button');
      btn.className = 'juno-chat__choice';
      btn.textContent = choice.label;
      btn.addEventListener('click', () => {
        if (choice.url) {
          window.location.href = choice.url;
        } else if (choice.next) {
          navigate(choice.next);
        }
      });
      footer.appendChild(btn);
    });
  }

  function navigate(nodeKey, userText = null) {
    const node = RESPONSES[nodeKey];
    if (!node) return;
    if (userText) addMessage(userText, true);
    showTyping();
    setTimeout(() => {
      removeTyping();
      if (node.messageHTML) {
        addMessage(node.messageHTML, false, true);
      } else {
        addMessage(node.message);
      }
      showChoices(node.choices);
    }, 700);
  }

  /* -----------------------------------------------
   * テキスト入力処理
   * ----------------------------------------------- */
  function handleInput() {
    const input = document.getElementById('juno-chat-input');
    const text = input.value.trim();
    if (!text) return;
    input.value = '';
    const matched = matchKeyword(text);
    navigate(matched || 'fallback', text);
  }

  /* -----------------------------------------------
   * 初期化
   * ----------------------------------------------- */
  function init() {
    buildUI();

    const toggle   = document.querySelector('.juno-chat__toggle');
    const win      = document.querySelector('.juno-chat__window');
    const closeBtn = document.querySelector('.juno-chat__close');
    const sendBtn  = document.getElementById('juno-chat-send');
    const input    = document.getElementById('juno-chat-input');
    let opened = false;

    toggle.addEventListener('click', () => {
      const isHidden = win.hasAttribute('hidden');
      if (isHidden) {
        win.removeAttribute('hidden');
        toggle.setAttribute('aria-expanded', 'true');
        if (!opened) { navigate('welcome'); opened = true; }
        setTimeout(() => input.focus(), 300);
      } else {
        win.setAttribute('hidden', '');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });

    closeBtn.addEventListener('click', () => {
      win.setAttribute('hidden', '');
      toggle.setAttribute('aria-expanded', 'false');
    });

    sendBtn.addEventListener('click', handleInput);
    input.addEventListener('keydown', e => {
      if (e.key === 'Enter') handleInput();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
