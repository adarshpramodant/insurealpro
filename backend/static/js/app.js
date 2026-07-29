/* ==========================================================================
   INSUREAI PRO - FRONTEND APPLICATION CONTROLLER
   ========================================================================== */

let state = {
  sex: 'female',
  smoker: 'no',
  unitSystem: 'metric',
  currentPrediction: null,
  theme: localStorage.getItem('insurance_theme') || 'dark',
  highContrast: false,
  largeFont: false,
  reducedMotion: false
};

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  fetchModelOverview();
  calculateSmartBMI();
  updateLiveEstimate();
});

/* Theme & Accessibility */
function initTheme() {
  document.documentElement.setAttribute('data-theme', state.theme);
  updateThemeIcon();
}

function toggleTheme() {
  state.theme = state.theme === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', state.theme);
  localStorage.setItem('insurance_theme', state.theme);
  updateThemeIcon();
}

function updateThemeIcon() {
  const icon = document.getElementById('themeIcon');
  if (icon) icon.className = state.theme === 'dark' ? 'fa-solid fa-sun' : 'fa-solid fa-moon';
}

function toggleContrast() {
  state.highContrast = !state.highContrast;
  document.documentElement.setAttribute('data-high-contrast', state.highContrast);
}

function toggleLargeFont() {
  state.largeFont = !state.largeFont;
  document.documentElement.setAttribute('data-large-font', state.largeFont);
}

function toggleReducedMotion() {
  state.reducedMotion = !state.reducedMotion;
  document.documentElement.setAttribute('data-reduced-motion', state.reducedMotion);
}

/* Page Navigation */
function switchPage(pageId) {
  document.querySelectorAll('.page-view').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));

  const targetPage = document.getElementById(`page-${pageId}`);
  const targetNav = document.getElementById(`nav-${pageId}`);

  if (targetPage) targetPage.classList.add('active');
  if (targetNav) targetNav.classList.add('active');

  window.scrollTo({ top: 0, behavior: 'smooth' });

  if (pageId === 'history') fetchHistoryData();
  else if (pageId === 'analytics') renderAnalyticsDashboard();
  else if (pageId === 'admin') fetchAdminData();
  else if (pageId === 'whatif' && state.currentPrediction) triggerWhatIfSimulation();
}

/* Segmented Toggle Helper */
function selectSegment(group, value) {
  state[group] = value;
  if (group === 'sex') {
    document.getElementById('sexFemale').classList.toggle('active', value === 'female');
    document.getElementById('sexMale').classList.toggle('active', value === 'male');
  } else if (group === 'smoker') {
    document.getElementById('smokerNo').classList.toggle('active', value === 'no');
    document.getElementById('smokerYes').classList.toggle('active', value === 'yes');
  }
  updateLiveEstimate();
}

/* Smart BMI Calculator */
function setUnitSystem(sys) {
  state.unitSystem = sys;
  const lblH = document.getElementById('lblHeight');
  const lblW = document.getElementById('lblWeight');
  
  if (sys === 'metric') {
    lblH.innerText = 'Height (cm)';
    lblW.innerText = 'Weight (kg)';
    document.getElementById('calcHeight').value = 170;
    document.getElementById('calcWeight').value = 75;
  } else {
    lblH.innerText = 'Height (inches)';
    lblW.innerText = 'Weight (lbs)';
    document.getElementById('calcHeight').value = 67;
    document.getElementById('calcWeight').value = 165;
  }
  calculateSmartBMI();
}

function calculateSmartBMI() {
  const h = parseFloat(document.getElementById('calcHeight').value) || 170;
  const w = parseFloat(document.getElementById('calcWeight').value) || 75;
  let bmi = 24.0;

  if (state.unitSystem === 'metric') {
    const hMeter = h / 100.0;
    if (hMeter > 0) bmi = w / (hMeter * hMeter);
  } else {
    if (h > 0) bmi = (w / (h * h)) * 703;
  }

  bmi = Math.round(bmi * 10) / 10;
  document.getElementById('calcBmiResult').innerText = bmi.toFixed(1);
  document.getElementById('inputBmi').value = bmi;
  document.getElementById('bmiVal').innerText = bmi.toFixed(1);

  const badge = document.getElementById('calcBmiBadge');
  if (bmi < 18.5) { badge.innerText = 'Underweight'; badge.className = 'risk-badge warning'; }
  else if (bmi < 25.0) { badge.innerText = 'Normal'; badge.className = 'risk-badge success'; }
  else if (bmi < 30.0) { badge.innerText = 'Overweight'; badge.className = 'risk-badge info'; }
  else { badge.innerText = 'Obese'; badge.className = 'risk-badge danger'; }

  updateLiveEstimate();
}

/* Live Estimate Preview */
function updateLiveEstimate() {
  const age = parseInt(document.getElementById('inputAge').value) || 35;
  const bmi = parseFloat(document.getElementById('inputBmi').value) || 26.0;
  const children = parseInt(document.getElementById('inputChildren').value) || 0;
  const smoker = state.smoker === 'yes';

  let est = 3200 + (age * 260) + (bmi * 115) + (children * 500);
  if (smoker) est = (est * 2.85) + (bmi > 30 ? 4000 : 0);

  document.getElementById('prevAnnual').innerText = `₹${est.toLocaleString('en-IN', { maximumFractionDigits: 0 })}`;
  document.getElementById('prevMonthly').innerText = `₹${Math.round(est/12).toLocaleString('en-IN')}`;
  document.getElementById('prevQuarterly').innerText = `₹${Math.round(est/4).toLocaleString('en-IN')}`;
  document.getElementById('prevDaily').innerText = `₹${Math.round(est/365).toLocaleString('en-IN')}`;
}

/* Prediction Form Submission with Progress Loader */
async function handlePredictionSubmit(event) {
  event.preventDefault();
  
  const loader = document.getElementById('loaderModal');
  const loaderStatus = document.getElementById('loaderStatusText');
  loader.classList.add('active');

  const steps = [
    "Analyzing Health Profile...",
    "Executing 3-Model Ensemble (XGBoost + RF + CatBoost)...",
    "Calculating SHAP Explainability...",
    "Generating Optimization Advisory Package..."
  ];

  for (let s of steps) {
    loaderStatus.innerText = s;
    await new Promise(r => setTimeout(r, 350));
  }

  const payload = {
    age: parseInt(document.getElementById('inputAge').value),
    sex: state.sex,
    bmi: parseFloat(document.getElementById('inputBmi').value),
    children: parseInt(document.getElementById('inputChildren').value),
    smoker: state.smoker,
    region: document.getElementById('inputRegion').value
  };

  try {
    const res = await fetch('/api/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    loader.classList.remove('active');

    if (data.success) {
      state.currentPrediction = data.data;
      displayPredictionResult(data.data);
      document.getElementById('nav-result').style.display = 'flex';
      switchPage('result');
    } else {
      alert(`Error: ${data.errors ? data.errors.join(', ') : data.error}`);
    }
  } catch (err) {
    loader.classList.remove('active');
    alert('Server connection error. Please verify backend service.');
  }
}

/* Display Prediction Result */
function displayPredictionResult(res) {
  document.getElementById('resPredictedCharge').innerText = `₹${res.predicted_charge.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
  document.getElementById('resExpectedRange').innerText = `Likely Range: ${res.expected_range.formatted}`;

  const riskBadge = document.getElementById('resRiskBadge');
  riskBadge.className = `risk-badge ${res.risk_color}`;
  riskBadge.innerHTML = `<i class="fa-solid fa-shield-virus"></i> ${res.risk_level} Risk`;

  document.getElementById('resAgreement').innerText = `Model Agreement: ${res.agreement_pct}%`;
  document.getElementById('resConfidenceRating').innerText = res.confidence_rating;

  // Model Estimates
  const estList = document.getElementById('resModelEstimatesList');
  estList.innerHTML = '';
  res.multi_model_estimates.forEach(m => {
    const div = document.createElement('div');
    div.className = 'model-est-item';
    div.innerHTML = `<span>${m.model}</span> <span style="font-weight:700;">₹${m.prediction.toLocaleString('en-IN')}</span>`;
    estList.appendChild(div);
  });

  const adv = res.advisory_package;
  document.getElementById('resPlainEnglish').innerText = adv.plain_english_explanation;

  // Percentage Breakdown
  const pctList = document.getElementById('resPercentageBreakdownList');
  pctList.innerHTML = '';
  adv.percentage_breakdown.forEach(p => {
    const item = document.createElement('div');
    item.style.cssText = 'display:flex; justify-content:space-between; padding:8px 12px; background:rgba(255,255,255,0.03); border-radius:8px; font-size:0.9rem;';
    item.innerHTML = `<span>${p.factor}</span> <span style="font-weight:700; color:${p.impact==='positive'?'var(--accent-rose)':'var(--accent-emerald)'};">${p.percentage}</span>`;
    pctList.appendChild(item);
  });

  // Optimization Savings
  const optList = document.getElementById('resOptimizationList');
  optList.innerHTML = '';
  adv.optimization_options.forEach(opt => {
    const card = document.createElement('div');
    card.style.cssText = 'padding:1.2rem; background:rgba(16, 185, 129, 0.08); border-radius:12px; border:1px solid rgba(16, 185, 129, 0.2);';
    card.innerHTML = `
      <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
        <strong style="font-size:0.95rem;">${opt.action}</strong>
        <span class="savings-badge">${opt.badge}</span>
      </div>
      <div style="font-size:1.4rem; font-weight:800; color:var(--accent-emerald);">Save ₹${opt.estimated_savings_annual.toLocaleString('en-IN')}/yr</div>
    `;
    optList.appendChild(card);
  });

  // Health Scores
  document.getElementById('resHealthScore').innerText = adv.scores.health_score;
  document.getElementById('resAffordabilityScore').innerText = adv.scores.affordability_score;

  // Tier Plans
  const tierGrid = document.getElementById('resTierGrid');
  tierGrid.innerHTML = '';
  adv.tier_plans.forEach(plan => {
    const card = document.createElement('div');
    card.className = `glass-card tier-card ${plan.tier.includes('Recommended')?'popular':''}`;
    card.innerHTML = `
      <h4>${plan.tier}</h4>
      <div style="font-size:1.8rem; font-weight:800; margin:8px 0; color:var(--accent-secondary);">₹${plan.annual_premium.toLocaleString('en-IN')}<span style="font-size:0.8rem;">/yr</span></div>
      <div style="font-size:0.85rem; color:var(--text-muted); margin-bottom:1rem;">₹${plan.monthly_premium.toLocaleString('en-IN')}/month</div>
      <p style="font-size:0.88rem; color:var(--text-secondary); margin-bottom:1rem;">${plan.recommended_for}</p>
    `;
    tierGrid.appendChild(card);
  });

  renderHealthRadarChart(adv.scores);
}

/* What-If Scenario Simulator */
async function triggerWhatIfSimulation() {
  if (!state.currentPrediction) return;

  const overrides = {
    simulated_smoker: document.getElementById('whatifSmoker').value,
    simulated_bmi: parseFloat(document.getElementById('whatifBmi').value),
    age_delta_years: parseInt(document.getElementById('whatifAgeDelta').value)
  };

  try {
    const res = await fetch('/api/simulate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ baseline: state.currentPrediction.inputs, overrides: overrides })
    });
    const data = await res.json();
    if (data.success) {
      const d = data.data;
      document.getElementById('whatifCurrent').innerText = `₹${d.baseline_premium.toLocaleString('en-IN')}`;
      document.getElementById('whatifSimulated').innerText = `₹${d.simulated_premium.toLocaleString('en-IN')}`;
      document.getElementById('whatifSavings').innerText = `₹${Math.abs(d.annual_savings).toLocaleString('en-IN')}`;
      document.getElementById('whatifPctChange').innerText = `${Math.abs(d.percentage_change)}% ${d.is_savings ? 'Reduction' : 'Increase'}`;
    }
  } catch (e) {}
}

/* Multi-Format Export */
async function exportCurrentResult(format) {
  if (!state.currentPrediction) return;
  try {
    const res = await fetch('/api/export', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ format: format, prediction: state.currentPrediction })
    });
    if (res.ok) {
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `InsureAI_Pro_Quote_${state.currentPrediction.record_id || 'latest'}.${format === 'excel' ? 'xlsx' : format}`;
      document.body.appendChild(a);
      a.click();
      a.remove();
    }
  } catch (e) {}
}

/* Floating AI Chatbot */
function toggleChatbot() {
  document.getElementById('chatbotDrawer').classList.toggle('active');
}

async function sendChatMessage() {
  const input = document.getElementById('chatInput');
  const msg = input.value.trim();
  if (!msg) return;

  const chatBody = document.getElementById('chatBody');
  const uMsg = document.createElement('div');
  uMsg.className = 'chat-msg user';
  uMsg.innerText = msg;
  chatBody.appendChild(uMsg);

  input.value = '';
  chatBody.scrollTop = chatBody.scrollHeight;

  const ctx = state.currentPrediction ? {
    predicted_charge: state.currentPrediction.predicted_charge,
    risk_level: state.currentPrediction.risk_level,
    bmi: state.currentPrediction.inputs.bmi,
    age: state.currentPrediction.inputs.age,
    smoker: state.currentPrediction.inputs.smoker
  } : {};

  try {
    const res = await fetch('/api/chatbot', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: msg, context: ctx })
    });
    const data = await res.json();
    const bMsg = document.createElement('div');
    bMsg.className = 'chat-msg bot';
    bMsg.innerText = data.reply || "I'm here to help with your policy questions.";
    chatBody.appendChild(bMsg);
    chatBody.scrollTop = chatBody.scrollHeight;
  } catch (e) {}
}

/* Admin Dashboard Data Loader */
async function fetchAdminData() {
  try {
    const [statsRes, logsRes] = await Promise.all([
      fetch('/api/admin/stats').then(r => r.json()),
      fetch('/api/admin/audit-logs').then(r => r.json())
    ]);

    if (statsRes.success) {
      const s = statsRes.data;
      document.getElementById('admTotalPreds').innerText = s.total_predictions;
      document.getElementById('admAvgPremium').innerText = `₹${s.average_premium.toLocaleString('en-IN')}`;
      document.getElementById('admAvgBmi').innerText = s.average_bmi;
      document.getElementById('admSmokerRatio').innerText = `${s.smoker_percentage}%`;
    }

    if (logsRes.success) {
      const tbody = document.getElementById('adminAuditTableBody');
      tbody.innerHTML = '';
      logsRes.data.items.forEach(l => {
        const tr = document.createElement('tr');
        tr.innerHTML = `<td>#${l.id}</td><td>${l.timestamp}</td><td><strong>${l.action_type}</strong></td><td>${l.ip_address}</td><td>${JSON.stringify(l.details)}</td>`;
        tbody.appendChild(tr);
      });
    }
  } catch (e) {}
}

/* History Database Fetcher */
async function fetchHistoryData() {
  const search = document.getElementById('historySearch').value;
  const smoker = document.getElementById('historySmokerFilter').value;

  try {
    const res = await fetch(`/api/history?search=${encodeURIComponent(search)}&smoker=${smoker}`);
    const data = await res.json();
    if (data.success) {
      const tbody = document.getElementById('historyTableBody');
      tbody.innerHTML = '';
      data.data.items.forEach(r => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td>#${r.id}</td>
          <td>${r.timestamp}</td>
          <td>${r.age} yrs | ${r.sex.toUpperCase()} | ${r.region.toUpperCase()}</td>
          <td>BMI: ${r.bmi} | Smoker: ${r.smoker.toUpperCase()}</td>
          <td><span class="risk-badge info">${r.risk_level}</span></td>
          <td style="font-weight:700; color:var(--accent-secondary);">₹${r.predicted_charge.toLocaleString('en-IN')}</td>
          <td><button style="background:none; border:none; color:var(--accent-rose); cursor:pointer;" onclick="deleteHistoryRecord(${r.id})"><i class="fa-solid fa-trash"></i></button></td>
        `;
        tbody.appendChild(tr);
      });
    }
  } catch (e) {}
}

async function deleteHistoryRecord(id) {
  if (!confirm(`Delete record #${id}?`)) return;
  await fetch(`/api/history/${id}`, { method: 'DELETE' });
  fetchHistoryData();
}

async function clearAllHistory() {
  if (!confirm('Clear ALL prediction history records?')) return;
  await fetch('/api/history', { method: 'DELETE' });
  fetchHistoryData();
}

function exportHistoryCsv() {
  window.open('/api/history?per_page=1000', '_blank');
}

async function fetchModelOverview() {
  try {
    const res = await fetch('/api/model-info');
    const data = await res.json();
    if (data.success) {
      document.getElementById('landingR2Score').innerText = `${(data.data.r2_score * 100).toFixed(1)}%`;
    }
  } catch (e) {}
}
