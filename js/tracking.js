/**
 * Juno サイト コンバージョン計測
 * GA4 のカスタムイベントを送信する
 */
document.addEventListener('DOMContentLoaded', function () {
  function sendEvent(name, params) {
    if (typeof gtag === 'function') {
      gtag('event', name, params);
    }
  }

  // ------------------------------------------------------------
  // 1. 電話番号のタップ・クリック
  // ------------------------------------------------------------
  document.querySelectorAll('a[href^="tel:"]').forEach(function (el) {
    el.addEventListener('click', function () {
      sendEvent('tel_click', {
        page_path: window.location.pathname,
        link_text: (el.textContent || '').trim()
      });
    });
  });

  // ------------------------------------------------------------
  // 2. メールアドレスのクリック
  // ------------------------------------------------------------
  document.querySelectorAll('a[href^="mailto:"]').forEach(function (el) {
    el.addEventListener('click', function () {
      sendEvent('mail_click', {
        page_path: window.location.pathname
      });
    });
  });

  // ------------------------------------------------------------
  // 3. お問い合わせフォーム（サイト内）
  //    以下のイベントは contact-form.js から送信される
  //
  //    form_category_select  : 種別ラジオボタンを選択したとき
  //      { category: '訪問看護のご利用に関するご相談' }
  //
  //    form_submit_success   : フォーム送信が完了したとき
  //      { form_type: '訪問看護のご利用に関するご相談' }
  //
  //    GA4 でのコンバージョン設定:
  //      form_submit_success をキーイベントに設定してください
  // ------------------------------------------------------------
});
