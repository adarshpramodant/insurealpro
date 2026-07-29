/* ==========================================================================
   INSUREAI PRO - INTERACTIVE CHARTS & RADAR CONTROLLER
   ========================================================================== */

let charts = {};

function getChartColors() {
  const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
  return {
    text: isDark ? '#9ca3af' : '#475569',
    grid: isDark ? 'rgba(255, 255, 255, 0.08)' : 'rgba(0, 0, 0, 0.08)',
    primary: '#6366f1',
    cyan: '#06b6d4',
    emerald: '#10b981',
    rose: '#f43f5e',
    amber: '#f59e0b'
  };
}

function prepareCanvas(id) {
  const canvas = document.getElementById(id);
  if (!canvas) return null;
  if (charts[id]) {
    charts[id].destroy();
    delete charts[id];
  }
  canvas.removeAttribute('style');
  canvas.removeAttribute('width');
  canvas.removeAttribute('height');
  return canvas;
}

/* 1. Health Risk Radar Chart */
function renderHealthRadarChart(scores) {
  const canvas = prepareCanvas('chartHealthRadar');
  if (!canvas) return;

  const colors = getChartColors();

  charts.chartHealthRadar = new Chart(canvas, {
    type: 'radar',
    data: {
      labels: ['BMI Score', 'Lifestyle Score', 'Tobacco Safety', 'Age Tier', 'Dependents', 'Overall Risk'],
      datasets: [{
        label: 'Health Profile Score',
        data: [scores.health_score, scores.lifestyle_score, 80, 75, 90, scores.affordability_score],
        backgroundColor: 'rgba(99, 102, 241, 0.25)',
        borderColor: colors.primary,
        pointBackgroundColor: colors.cyan,
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        r: {
          min: 0,
          max: 100,
          angleLines: { color: colors.grid },
          grid: { color: colors.grid },
          pointLabels: { color: colors.text, font: { size: 10 } },
          ticks: { display: false }
        }
      },
      plugins: { legend: { display: false } }
    }
  });
}

/* 2. Projected 5-Year Health Risk Timeline Chart */
function renderHealthTimelineChart() {
  const canvas = prepareCanvas('chartHealthTimeline');
  if (!canvas) return;

  const colors = getChartColors();

  charts.chartHealthTimeline = new Chart(canvas, {
    type: 'line',
    data: {
      labels: ['Today', '1 Year', '3 Years', '5 Years'],
      datasets: [{
        label: 'Projected Premium Curve (INR)',
        data: [42013, 43483, 46634, 50415],
        borderColor: colors.cyan,
        backgroundColor: 'rgba(6, 182, 212, 0.15)',
        fill: true,
        tension: 0.35,
        pointRadius: 6,
        pointBackgroundColor: colors.primary
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: colors.text } },
        tooltip: { callbacks: { label: (c) => ` Projected: ₹${c.raw.toLocaleString('en-IN')}` } }
      },
      scales: {
        x: { ticks: { color: colors.text }, grid: { color: colors.grid } },
        y: { ticks: { color: colors.text }, grid: { color: colors.grid } }
      }
    }
  });
}

/* 3. Analytics Dashboard Charts */
async function renderAnalyticsDashboard() {
  try {
    const [metricsRes, importanceRes] = await Promise.all([
      fetch('/api/metrics').then(r => r.json()),
      fetch('/api/feature-importance').then(r => r.json())
    ]);

    if (metricsRes.success) renderModelBenchmarkChart(metricsRes.data);
    if (importanceRes.success) renderFeatureImportanceChart(importanceRes.data);

    renderSmokerImpactChart();
    renderHealthTimelineChart();
  } catch (err) {
    console.error("Error rendering analytics charts:", err);
  }
}

function renderModelBenchmarkChart(metricsData) {
  const canvas = prepareCanvas('chartModelBenchmark');
  if (!canvas) return;

  const colors = getChartColors();
  const labels = metricsData.map(m => m.model);
  const r2Scores = metricsData.map(m => m.r2 * 100);

  charts.chartModelBenchmark = new Chart(canvas, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Validation R² Score (%)',
        data: r2Scores,
        backgroundColor: r2Scores.map(score => score > 88 ? '#10b981' : score > 82 ? '#06b6d4' : '#6366f1'),
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { ticks: { color: colors.text, font: { size: 10 } }, grid: { display: false } },
        y: { min: 70, max: 100, ticks: { color: colors.text }, grid: { color: colors.grid } }
      }
    }
  });
}

function renderFeatureImportanceChart(importanceData) {
  const canvas = prepareCanvas('chartFeatureImportance');
  if (!canvas) return;

  const colors = getChartColors();
  const sortedKeys = Object.keys(importanceData).slice(0, 8);
  const sortedVals = sortedKeys.map(k => importanceData[k]);

  charts.chartFeatureImportance = new Chart(canvas, {
    type: 'bar',
    data: {
      labels: sortedKeys,
      datasets: [{
        label: 'SHAP Value Weight',
        data: sortedVals,
        backgroundColor: colors.primary,
        borderRadius: 6
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { ticks: { color: colors.text }, grid: { color: colors.grid } },
        y: { ticks: { color: colors.text }, grid: { display: false } }
      }
    }
  });
}

function renderSmokerImpactChart() {
  const canvas = prepareCanvas('chartSmokerImpact');
  if (!canvas) return;

  const colors = getChartColors();
  charts.chartSmokerImpact = new Chart(canvas, {
    type: 'doughnut',
    data: {
      labels: ['Non-Smoker Average', 'Smoker Average'],
      datasets: [{
        data: [8434, 32050],
        backgroundColor: [colors.emerald, colors.rose],
        borderWidth: 0
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: colors.text } },
        tooltip: { callbacks: { label: (c) => ` Avg Premium: ₹${c.raw.toLocaleString('en-IN')}` } }
      }
    }
  });
}
