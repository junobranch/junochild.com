(function () {
  'use strict';

  const GAS_URL = 'https://script.google.com/macros/s/AKfycbxllnHsC23d7P2Wp9p8PRS59iTwPJxXDMeVfkTZaD8Ps2cMoLhy3X4fBfmzQcK0BiCTHg/exec';

  const form = document.getElementById('contact-form');
  if (!form) return;

  // Section elements
  const sectionCommon  = document.getElementById('section-common');
  const sectionFooter  = document.getElementById('section-footer');
  const msgEvening     = document.getElementById('msg-evening');
  const submitBtn      = document.getElementById('submit-btn');
  const formError      = document.getElementById('form-error');

  const categorySections = {
    'visit':   document.getElementById('section-visit'),
    'recruit': document.getElementById('section-recruit'),
    'media':   document.getElementById('section-media'),
    'other':   document.getElementById('section-other'),
  };

  const CATEGORY_KEY_MAP = {
    '訪問看護のご利用に関するご相談':         'visit',
    '採用・カジュアル面談に関するお問い合わせ': 'recruit',
    '取材に関するお問い合わせ':               'media',
    'その他のお問い合わせ':                   'other',
  };

  // ── カテゴリ変更 ──────────────────────────────────
  document.querySelectorAll('input[name="category"]').forEach(function (radio) {
    radio.addEventListener('change', onCategoryChange);
  });

  function onCategoryChange() {
    var cat = getCheckedValue('category');
    var key = CATEGORY_KEY_MAP[cat];

    sectionCommon.hidden = false;
    sectionFooter.hidden = false;

    Object.keys(categorySections).forEach(function (k) {
      categorySections[k].hidden = (k !== key);
    });

    clearAllErrors();

    if (window.gtag && cat) {
      gtag('event', 'form_category_select', { category: cat });
    }
  }

  // ── 夕方選択 → 案内メッセージ表示（警告ではない）──
  document.querySelectorAll('input[name="visitTime"]').forEach(function (r) {
    r.addEventListener('change', function () {
      if (msgEvening) {
        msgEvening.hidden = (this.value !== '平日夕方（15:00以降）');
      }
    });
  });

  // ── 職業「その他」テキスト入力 ────────────────────
  document.querySelectorAll('input[name="occupation"]').forEach(function (r) {
    r.addEventListener('change', function () {
      var wrap = document.getElementById('occupation-other-wrap');
      if (wrap) wrap.hidden = (this.value !== 'その他');
    });
  });

  // ── フォーム送信 ──────────────────────────────────
  form.addEventListener('submit', function (e) {
    e.preventDefault();

    // ハニーポット
    var honeypot = form.querySelector('input[name="website"]');
    if (honeypot && honeypot.value) return;

    if (!validateForm()) return;

    var data = collectData();

    submitBtn.disabled = true;
    submitBtn.textContent = '送信中...';
    formError.style.display = 'none';

    fetch(GAS_URL, {
      method: 'POST',
      mode: 'no-cors',
      headers: { 'Content-Type': 'text/plain' },
      body: JSON.stringify(data),
    }).then(function () {
      if (window.gtag) {
        gtag('event', 'form_submit_success', { form_type: data.category });
      }
      window.location.href = '/thanks.html';
    }).catch(function () {
      formError.style.display = 'block';
      submitBtn.disabled = false;
      submitBtn.textContent = '送信する';
      formError.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
  });

  // ── バリデーション ────────────────────────────────
  function validateForm() {
    clearAllErrors();
    var valid = true;
    var firstErrorEl = null;

    // カテゴリ
    var cat = getCheckedValue('category');
    if (!cat) {
      showError('err-category', 'お問い合わせの種別を選択してください。');
      firstErrorEl = firstErrorEl || document.getElementById('err-category');
      valid = false;
    }

    if (!cat) {
      scrollToFirst(firstErrorEl);
      return false;
    }

    // 共通項目
    var nameKanji = document.getElementById('nameKanji');
    if (!nameKanji.value.trim()) {
      markError(nameKanji, 'err-nameKanji', 'お名前（漢字）を入力してください。');
      firstErrorEl = firstErrorEl || nameKanji;
      valid = false;
    }

    var nameKana = document.getElementById('nameKana');
    if (!nameKana.value.trim()) {
      markError(nameKana, 'err-nameKana', 'お名前（カタカナ）を入力してください。');
      firstErrorEl = firstErrorEl || nameKana;
      valid = false;
    }

    var email = document.getElementById('email');
    if (!isValidEmail(email.value.trim())) {
      markError(email, 'err-email', '正しいメールアドレスを入力してください。');
      firstErrorEl = firstErrorEl || email;
      valid = false;
    }

    var tel = document.getElementById('tel');
    if (!tel.value.trim()) {
      markError(tel, 'err-tel', '電話番号を入力してください。');
      firstErrorEl = firstErrorEl || tel;
      valid = false;
    }

    if (!getCheckedValue('contactMethod')) {
      showError('err-contactMethod', 'ご希望の連絡方法を選択してください。');
      firstErrorEl = firstErrorEl || document.getElementById('err-contactMethod');
      valid = false;
    }

    // カテゴリ別バリデーション
    if (cat === '訪問看護のご利用に関するご相談') {
      var childAge = document.getElementById('childAge');
      if (!childAge.value) {
        markError(childAge, 'err-childAge', 'お子さまのご年齢を選択してください。');
        firstErrorEl = firstErrorEl || childAge;
        valid = false;
      }
      if (!getCheckedValue('childGender')) {
        showError('err-childGender', 'お子さまの性別を選択してください。');
        firstErrorEl = firstErrorEl || document.getElementById('err-childGender');
        valid = false;
      }
      if (!getCheckedValue('area')) {
        showError('err-area', 'お住まいのエリアを選択してください。');
        firstErrorEl = firstErrorEl || document.getElementById('err-area');
        valid = false;
      }
      if (!getCheckedValue('visitTime')) {
        showError('err-visitTime', 'ご希望の訪問時間帯（第一希望）を選択してください。');
        firstErrorEl = firstErrorEl || document.getElementById('err-visitTime');
        valid = false;
      }
      var msgVisit = document.getElementById('msg-visit');
      if (!msgVisit.value.trim()) {
        markError(msgVisit, 'err-msg-visit', 'お問い合わせ内容を入力してください。');
        firstErrorEl = firstErrorEl || msgVisit;
        valid = false;
      }
    }

    if (cat === '採用・カジュアル面談に関するお問い合わせ') {
      var applicantAge = document.getElementById('applicantAge');
      if (!applicantAge.value.trim()) {
        markError(applicantAge, 'err-applicantAge', 'ご年齢を入力してください。');
        firstErrorEl = firstErrorEl || applicantAge;
        valid = false;
      }
      var jobTypeChecked = document.querySelectorAll('input[name="jobType"]:checked');
      if (jobTypeChecked.length === 0) {
        showError('err-jobType', '応募区分を1つ以上選択してください。');
        firstErrorEl = firstErrorEl || document.getElementById('err-jobType');
        valid = false;
      }
    }

    if (cat === '取材に関するお問い合わせ') {
      var mediaName = document.getElementById('mediaName');
      if (!mediaName.value.trim()) {
        markError(mediaName, 'err-mediaName', '媒体名を入力してください。');
        firstErrorEl = firstErrorEl || mediaName;
        valid = false;
      }
      var msgMedia = document.getElementById('msg-media');
      if (!msgMedia.value.trim()) {
        markError(msgMedia, 'err-msg-media', 'お問い合わせ内容を入力してください。');
        firstErrorEl = firstErrorEl || msgMedia;
        valid = false;
      }
    }

    if (cat === 'その他のお問い合わせ') {
      var msgOther = document.getElementById('msg-other');
      if (!msgOther.value.trim()) {
        markError(msgOther, 'err-msg-other', 'お問い合わせ内容を入力してください。');
        firstErrorEl = firstErrorEl || msgOther;
        valid = false;
      }
    }

    // プライバシー同意
    if (!document.getElementById('privacyAgree').checked) {
      showError('err-privacy', 'プライバシーポリシーへの同意をお願いします。');
      firstErrorEl = firstErrorEl || document.getElementById('err-privacy');
      valid = false;
    }

    if (!valid) scrollToFirst(firstErrorEl);
    return valid;
  }

  // ── データ収集 ────────────────────────────────────
  function collectData() {
    var cat = getCheckedValue('category');
    var tel = (document.getElementById('tel').value || '').replace(/[-\s]/g, '');

    var data = {
      category:      cat,
      nameKanji:     document.getElementById('nameKanji').value.trim(),
      nameKana:      document.getElementById('nameKana').value.trim(),
      email:         document.getElementById('email').value.trim(),
      tel:           tel,
      contactMethod: getCheckedValue('contactMethod'),
    };

    if (cat === '訪問看護のご利用に関するご相談') {
      data.childAge   = document.getElementById('childAge').value;
      data.childGender = getCheckedValue('childGender');
      data.area       = getCheckedValue('area');
      data.visitTime  = getCheckedValue('visitTime');
      data.visitTime2 = getCheckedValue('visitTime2');
      data.source     = getCheckedValues('source', '#section-visit');
      data.message    = document.getElementById('msg-visit').value.trim();
    }

    if (cat === '採用・カジュアル面談に関するお問い合わせ') {
      data.applicantAge = document.getElementById('applicantAge').value.trim();
      data.jobType      = getCheckedValues('jobType', '#section-recruit');
      var occ           = getCheckedValue('occupation');
      var occOther      = document.getElementById('occupationOtherText').value.trim();
      data.occupation   = (occ === 'その他' && occOther) ? 'その他：' + occOther : occ;
      data.source       = getCheckedValues('recruitSource', '#section-recruit');
      data.message      = (document.getElementById('msg-recruit').value || '').trim();
    }

    if (cat === '取材に関するお問い合わせ') {
      data.mediaName = document.getElementById('mediaName').value.trim();
      data.message   = document.getElementById('msg-media').value.trim();
    }

    if (cat === 'その他のお問い合わせ') {
      data.message = document.getElementById('msg-other').value.trim();
    }

    return data;
  }

  // ── ユーティリティ ────────────────────────────────
  function getCheckedValue(name) {
    var el = document.querySelector('input[name="' + name + '"]:checked');
    return el ? el.value : '';
  }

  function getCheckedValues(name, scopeSelector) {
    var scope = scopeSelector ? document.querySelector(scopeSelector) : document;
    if (!scope) scope = document;
    var els = scope.querySelectorAll('input[name="' + name + '"]:checked');
    return Array.prototype.map.call(els, function (el) { return el.value; }).join(',');
  }

  function isValidEmail(v) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);
  }

  function markError(inputEl, errId, msg) {
    inputEl.classList.add('cf-input--error');
    showError(errId, msg);
    inputEl.addEventListener('input', function () {
      inputEl.classList.remove('cf-input--error');
      clearError(errId);
    }, { once: true });
  }

  function showError(errId, msg) {
    var el = document.getElementById(errId);
    if (el) { el.textContent = msg; el.style.display = 'block'; }
  }

  function clearError(errId) {
    var el = document.getElementById(errId);
    if (el) { el.style.display = 'none'; el.textContent = ''; }
  }

  function clearAllErrors() {
    form.querySelectorAll('.cf-input--error').forEach(function (el) {
      el.classList.remove('cf-input--error');
    });
    form.querySelectorAll('.cf-error-msg').forEach(function (el) {
      el.style.display = 'none';
      el.textContent = '';
    });
  }

  function scrollToFirst(el) {
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }

})();
