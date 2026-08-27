/**
 * Juno サイト コンバージョン計測
 * GA4 のカスタムイベントを送信する
 */
document.addEventListener('DOMContentLoaded', function () {
  // gtag が読み込まれていない場合は何もしない
  function sendEvent(name, params) {
    if (typeof gtag === 'function') {
      gtag('event', name, params);
    }
  }
  // ------------------------------------------------------------
  // 1. 電話番号のタップ・クリック
  //    スマートフォンからの発信を計測する
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
  // 2. 相談フォーム（Googleフォーム）への遷移
  //    現時点の最重要コンバージョン
  // ------------------------------------------------------------
  var formSelectors = [
    'a[href*="forms.gle"]',
    'a[href*="docs.google.com/forms"]'
  ].join(',');
  document.querySelectorAll(formSelectors).forEach(function (el) {
    el.addEventListener('click', function () {
      sendEvent('contact_form_click', {
        page_path: window.location.pathname,
        link_text: (el.textContent || '').trim()
      });
    });
  });
  // ------------------------------------------------------------
  // 3. メールアドレスのクリック
  // ------------------------------------------------------------
  document.querySelectorAll('a[href^="mailto:"]').forEach(function (el) {
    el.addEventListener('click', function () {
      sendEvent('mail_click', {
        page_path: window.location.pathname
      });
    });
  });
});
