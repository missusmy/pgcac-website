(function() {
  const STRIPE_BASE = 'https://donate.stripe.com/';
  const links = {
    monthly: {
      10: '4gMbJ17aNgJXbQn6jF00001',
      15: '3cI8wPfHjctH9IfeQb00002',
      20: 'dRmeVdeDfctH1bJ37t00003',
      25: '4gMeVdcv7dxL4nVeQb00004',
      50: '14A5kD7aN79n3jRbDZ00005',
      100: 'aFa3cvbr3ctH7A78rN00006'
    },
    onetime: {
      10: 'cNi28r0MpbpD5rZcI300007',
      25: '00wcN58eRfFT3jR37t00008',
      50: '5kQ14ndzb3Xbf2zazV00009',
      100: 'dRm5kD3YB51f9If23p0000a',
      250: '7sYdR90MpbpDaMjfUf0000b',
      500: '3cIbJ11Qt1P31bJgYj0000c'
    }
  };
  function redirect(pathOrUrl) {
    if (!pathOrUrl) return alert('This amount is not yet configured.');
    const url = /^https?:\/\//.test(pathOrUrl) ? pathOrUrl : (STRIPE_BASE + pathOrUrl);
    window.open(url, '_blank', 'noopener,noreferrer');
  }
  // One-time selection buttons (select, do not navigate)
  let selectedOnetime = null;
  const onetimeButtons = Array.from(document.querySelectorAll('#onetime .js-choose-onetime'));
  function setOnetimeActive(targetBtn) {
    onetimeButtons.forEach(b => {
      b.classList.remove('btn-secondary', 'active');
      b.classList.add('btn-outline-secondary');
      b.setAttribute('aria-pressed', 'false');
    });
    targetBtn.classList.remove('btn-outline-secondary');
    targetBtn.classList.add('btn-secondary', 'active');
    targetBtn.setAttribute('aria-pressed', 'true');
  }
  onetimeButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      selectedOnetime = btn.getAttribute('data-amount');
      setOnetimeActive(btn);
    });
  });
  // Monthly selection buttons (select, do not navigate)
  let selectedMonthly = null;
  const monthlyButtons = Array.from(document.querySelectorAll('#monthlyAmounts .js-choose-monthly'));
  function setMonthlyActive(targetBtn) {
    monthlyButtons.forEach(b => {
      b.classList.remove('btn-primary', 'active');
      b.classList.add('btn-outline-primary');
      b.setAttribute('aria-pressed', 'false');
    });
    targetBtn.classList.remove('btn-outline-primary');
    targetBtn.classList.add('btn-primary', 'active');
    targetBtn.setAttribute('aria-pressed', 'true');
  }
  monthlyButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      selectedMonthly = btn.getAttribute('data-amount');
      setMonthlyActive(btn);
    });
  });
  // Default monthly selection: $10
  const defaultMonthlyBtn = document.querySelector('#monthlyAmounts .js-choose-monthly[data-amount="10"]');
  if (defaultMonthlyBtn) {
    selectedMonthly = '10';
    setMonthlyActive(defaultMonthlyBtn);
  }
  document.getElementById('monthlyDonate')?.addEventListener('click', () => {
    if (!selectedMonthly) {
      alert('Please choose a monthly amount.');
      return;
    }
    const url = links.monthly && links.monthly[selectedMonthly];
    redirect(url);
  });
  // One-time Donate click: redirect according to selected amount
  document.getElementById('customDonate')?.addEventListener('click', () => {
    if (!selectedOnetime) {
      alert('Please choose a one-time amount.');
      return;
    }
    const url = links.onetime && links.onetime[selectedOnetime];
    redirect(url);
  });
  // Default one-time selection: highlight $50 button
  const defaultOnetimeBtn = document.querySelector('#onetime .js-choose-onetime[data-amount="50"]');
  if (defaultOnetimeBtn) {
    selectedOnetime = '50';
    setOnetimeActive(defaultOnetimeBtn);
  }
})();