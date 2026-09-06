/* =====================================================
   NETFLIX CONTENT INTELLIGENCE DASHBOARD — dashboard.js
   ===================================================== */

'use strict';

// ── Chart.js Global Defaults ──────────────────────────
Chart.defaults.color         = '#9a9aab';
Chart.defaults.font.family   = "'Inter', sans-serif";
Chart.defaults.font.size     = 12;
Chart.defaults.plugins.legend.display = false;
Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(22,22,32,0.95)';
Chart.defaults.plugins.tooltip.borderColor      = 'rgba(255,255,255,0.1)';
Chart.defaults.plugins.tooltip.borderWidth      = 1;
Chart.defaults.plugins.tooltip.padding          = 10;
Chart.defaults.plugins.tooltip.titleColor       = '#f0f0f5';
Chart.defaults.plugins.tooltip.bodyColor        = '#9a9aab';
Chart.defaults.plugins.tooltip.cornerRadius     = 10;
Chart.defaults.plugins.tooltip.displayColors    = true;

// ── Palette ───────────────────────────────────────────
const RED     = '#E50914';
const TEAL    = '#4ecdc4';
const YELLOW  = '#ffe66d';
const PURPLE  = '#a29bfe';
const PINK    = '#fd79a8';
const GREEN   = '#00b894';
const ORANGE  = '#ff9f43';
const BLUE    = '#54a0ff';
const CORAL   = '#e17055';
const INDIGO  = '#6c5ce7';

const PALETTE = [RED, TEAL, YELLOW, PURPLE, PINK, GREEN, ORANGE, BLUE, CORAL, INDIGO];

// ── Utility: grid line color ──────────────────────────
const GRID = 'rgba(255,255,255,0.06)';

function scaleDefaults() {
  return {
    grid: { color: GRID, drawBorder: false },
    ticks: { color: '#9a9aab' }
  };
}

// ── DATA ─────────────────────────────────────────────
const DATA = {
  yearly: {
    labels: ['2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021'],
    movies: [1,2,1,13,3,6,19,56,253,839,1237,1424,1284,993],
    tv:     [1,0,0,0, 0,5,5, 26,176,349,412, 592, 595, 505]
  },
  tvShare: {
    labels: ['2013','2014','2015','2016','2017','2018','2019','2020','2021'],
    values: [45.5, 20.8, 31.7, 41.0, 29.4, 25.0, 29.4, 31.7, 33.7]
  },
  monthly: {
    labels: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
    values: [738,563,742,764,632,728,827,755,770,760,705,813]
  },
  countries: {
    labels: ['United States','India','United Kingdom','Canada','France','Japan','Spain','South Korea','Germany','Mexico'],
    values: [3690,1046,806,445,393,318,232,231,226,169]
  },
  genres: {
    labels: ['International Movies','Dramas','Comedies','International TV Shows','Documentaries',
             'Action & Adventure','TV Dramas','Independent Movies','Children & Family','Romantic Movies'],
    values: [2752,2427,1674,1351,869,859,763,756,641,616]
  },
  ratings: {
    labels: ['TV-MA','TV-14','TV-PG','R','PG-13','TV-Y7','TV-Y','PG','TV-G','NR'],
    values: [3207,2160,863,799,490,334,307,287,220,80]
  },
  audience: {
    labels: ['Adults','Teens','Older Kids','Kids','Unrated'],
    values: [4009,2650,1150,908,90]
  }
};

// ════════════════════════════════════════════════════
// TAB SWITCHING
// ════════════════════════════════════════════════════
const charts = {};

function switchTab(tabId) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));

  document.getElementById('tab-' + tabId).classList.add('active');
  const panel = document.getElementById('panel-' + tabId);
  panel.classList.add('active');

  // Render charts for this tab on first show
  setTimeout(() => renderChartsForTab(tabId), 50);
}

document.getElementById('tabNav').addEventListener('click', e => {
  const btn = e.target.closest('.tab-btn');
  if (btn) switchTab(btn.dataset.tab);
});

// ════════════════════════════════════════════════════
// COUNT-UP ANIMATION
// ════════════════════════════════════════════════════
function animateCountUp(el, target, duration = 1600) {
  const start = performance.now();
  function step(now) {
    const progress = Math.min((now - start) / duration, 1);
    const ease = 1 - Math.pow(1 - progress, 3);
    el.textContent = Math.round(ease * target).toLocaleString();
    if (progress < 1) requestAnimationFrame(step);
    else el.textContent = target.toLocaleString();
  }
  requestAnimationFrame(step);
}

function startCountUps() {
  document.querySelectorAll('.count-up').forEach(el => {
    const target = parseInt(el.dataset.target, 10);
    animateCountUp(el, target);
  });
}

// ════════════════════════════════════════════════════
// CHART BUILDERS
// ════════════════════════════════════════════════════

/* TAB 1 — Overview */
function buildYearlyChart() {
  if (charts.yearlyChart) return;
  const ctx = document.getElementById('yearlyChart');
  if (!ctx) return;

  charts.yearlyChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: DATA.yearly.labels,
      datasets: [
        {
          label: 'Movies',
          data: DATA.yearly.movies,
          backgroundColor: RED,
          borderRadius: 4,
          borderSkipped: false
        },
        {
          label: 'TV Shows',
          data: DATA.yearly.tv,
          backgroundColor: TEAL,
          borderRadius: 4,
          borderSkipped: false
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            footer: (items) => 'Total: ' + items.reduce((s, i) => s + i.raw, 0).toLocaleString()
          }
        }
      },
      scales: {
        x: { ...scaleDefaults(), stacked: true },
        y: { ...scaleDefaults(), stacked: true, ticks: { color: '#9a9aab', callback: v => v >= 1000 ? (v/1000).toFixed(0)+'K' : v } }
      },
      animation: { duration: 900, easing: 'easeOutQuart' }
    }
  });
}

function buildSplitDonut() {
  if (charts.splitDonut) return;
  const ctx = document.getElementById('splitDonut');
  if (!ctx) return;

  charts.splitDonut = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Movies (69.6%)', 'TV Shows (30.4%)'],
      datasets: [{
        data: [6131, 2676],
        backgroundColor: [RED, TEAL],
        borderWidth: 0,
        hoverOffset: 8
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '68%',
      plugins: {
        legend: {
          display: true,
          position: 'bottom',
          labels: { color: '#9a9aab', font: { size: 12 }, padding: 16, boxWidth: 12, borderRadius: 4 }
        },
        tooltip: {
          callbacks: { label: i => ` ${i.label}: ${i.raw.toLocaleString()} titles` }
        }
      },
      animation: { animateRotate: true, duration: 900 }
    }
  });
}

function buildTvShareLine() {
  if (charts.tvShareLine) return;
  const ctx = document.getElementById('tvShareLine');
  if (!ctx) return;

  charts.tvShareLine = new Chart(ctx, {
    type: 'line',
    data: {
      labels: DATA.tvShare.labels,
      datasets: [{
        label: 'TV Share (%)',
        data: DATA.tvShare.values,
        borderColor: TEAL,
        backgroundColor: 'rgba(78,205,196,0.12)',
        pointBackgroundColor: TEAL,
        pointBorderColor: '#fff',
        pointRadius: 5,
        pointHoverRadius: 8,
        borderWidth: 2.5,
        fill: true,
        tension: 0.4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        tooltip: {
          callbacks: { label: i => ` TV Share: ${i.raw}%` }
        }
      },
      scales: {
        x: scaleDefaults(),
        y: {
          ...scaleDefaults(),
          min: 0, max: 55,
          ticks: { color: '#9a9aab', callback: v => v + '%' }
        }
      },
      animation: { duration: 900 }
    }
  });
}

function buildMonthlyBar() {
  if (charts.monthlyBar) return;
  const ctx = document.getElementById('monthlyBar');
  if (!ctx) return;

  const colors = DATA.monthly.values.map(v =>
    v === Math.max(...DATA.monthly.values) ? YELLOW :
    v === Math.min(...DATA.monthly.values) ? PINK : RED
  );

  charts.monthlyBar = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: DATA.monthly.labels,
      datasets: [{
        label: 'Titles Added',
        data: DATA.monthly.values,
        backgroundColor: colors,
        borderRadius: 5,
        borderSkipped: false
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { tooltip: { callbacks: { label: i => ` ${i.raw.toLocaleString()} titles` } } },
      scales: {
        x: scaleDefaults(),
        y: {
          ...scaleDefaults(),
          ticks: { color: '#9a9aab', callback: v => v >= 1000 ? (v/1000).toFixed(1)+'K' : v }
        }
      },
      animation: { duration: 800, delay: ctx => ctx.dataIndex * 40 }
    }
  });
}

/* TAB 2 — Global */
function buildCountryBar() {
  if (charts.countryBar) return;
  const ctx = document.getElementById('countryBar');
  if (!ctx) return;

  charts.countryBar = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: DATA.countries.labels,
      datasets: [{
        label: 'Titles',
        data: DATA.countries.values,
        backgroundColor: DATA.countries.values.map((v, i) => PALETTE[i % PALETTE.length]),
        borderRadius: 6,
        borderSkipped: false
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      plugins: { tooltip: { callbacks: { label: i => ` ${i.raw.toLocaleString()} titles` } } },
      scales: {
        x: { ...scaleDefaults(), ticks: { color: '#9a9aab', callback: v => v >= 1000 ? (v/1000).toFixed(0)+'K' : v } },
        y: { ...scaleDefaults(), ticks: { color: '#f0f0f5' } }
      },
      animation: { duration: 1000 }
    }
  });
}

function buildIndiaUsDonut() {
  if (charts.indiaUsDonut) return;
  const ctx = document.getElementById('indiaUsDonut');
  if (!ctx) return;

  charts.indiaUsDonut = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['India Movies (92%)', 'India TV (8%)', 'US Movies (74.6%)', 'US TV (25.4%)'],
      datasets: [
        {
          label: 'India',
          data: [963, 83],
          backgroundColor: [ORANGE, '#ff6b6b'],
          borderWidth: 0,
          hoverOffset: 6
        },
        {
          label: 'United States',
          data: [2753, 937],
          backgroundColor: [RED, TEAL],
          borderWidth: 2,
          borderColor: '#161620',
          hoverOffset: 6
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '45%',
      plugins: {
        legend: {
          display: true,
          position: 'bottom',
          labels: { color: '#9a9aab', font: { size: 11 }, padding: 10, boxWidth: 10 }
        },
        tooltip: {
          callbacks: {
            label: i => {
              const total = i.dataset.data.reduce((a, b) => a + b, 0);
              const pct = ((i.raw / total) * 100).toFixed(1);
              return ` ${i.label}: ${i.raw.toLocaleString()} (${pct}%)`;
            }
          }
        }
      },
      animation: { duration: 900 }
    }
  });
}

function buildCountryPie() {
  if (charts.countryPie) return;
  const ctx = document.getElementById('countryPie');
  if (!ctx) return;

  charts.countryPie = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: DATA.countries.labels,
      datasets: [{
        data: DATA.countries.values,
        backgroundColor: PALETTE,
        borderWidth: 2,
        borderColor: '#161620',
        hoverOffset: 10
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: true,
          position: 'right',
          labels: {
            color: '#9a9aab', font: { size: 11 }, padding: 8, boxWidth: 10,
            generateLabels: chart => {
              const data = chart.data;
              const total = data.datasets[0].data.reduce((a, b) => a + b, 0);
              return data.labels.map((label, i) => ({
                text: `${label.split(' ')[0]} (${((data.datasets[0].data[i]/total)*100).toFixed(1)}%)`,
                fillStyle: data.datasets[0].backgroundColor[i],
                strokeStyle: '#161620',
                lineWidth: 1,
                hidden: false,
                index: i
              }));
            }
          }
        },
        tooltip: {
          callbacks: { label: i => ` ${i.label}: ${i.raw.toLocaleString()} titles` }
        }
      },
      animation: { duration: 900 }
    }
  });
}

/* TAB 3 — Genre & Audience */
function buildGenreBar() {
  if (charts.genreBar) return;
  const ctx = document.getElementById('genreBar');
  if (!ctx) return;

  charts.genreBar = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: DATA.genres.labels,
      datasets: [{
        label: 'Titles',
        data: DATA.genres.values,
        backgroundColor: DATA.genres.values.map((_, i) => PALETTE[i % PALETTE.length]),
        borderRadius: 5,
        borderSkipped: false
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      plugins: { tooltip: { callbacks: { label: i => ` ${i.raw.toLocaleString()} titles` } } },
      scales: {
        x: { ...scaleDefaults(), ticks: { color: '#9a9aab', callback: v => v >= 1000 ? (v/1000).toFixed(0)+'K' : v } },
        y: { ...scaleDefaults(), ticks: { color: '#f0f0f5', font: { size: 11 } } }
      },
      animation: { duration: 1000 }
    }
  });
}

function buildAudienceDonut() {
  if (charts.audienceDonut) return;
  const ctx = document.getElementById('audienceDonut');
  if (!ctx) return;

  charts.audienceDonut = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: DATA.audience.labels,
      datasets: [{
        data: DATA.audience.values,
        backgroundColor: [RED, TEAL, YELLOW, PURPLE, PINK],
        borderWidth: 0,
        hoverOffset: 8
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '62%',
      plugins: {
        legend: {
          display: true,
          position: 'bottom',
          labels: { color: '#9a9aab', font: { size: 12 }, padding: 14, boxWidth: 12 }
        },
        tooltip: {
          callbacks: {
            label: i => {
              const total = DATA.audience.values.reduce((a, b) => a + b, 0);
              return ` ${i.label}: ${i.raw.toLocaleString()} (${((i.raw/total)*100).toFixed(1)}%)`;
            }
          }
        }
      },
      animation: { duration: 900 }
    }
  });
}

function buildRatingBar() {
  if (charts.ratingBar) return;
  const ctx = document.getElementById('ratingBar');
  if (!ctx) return;

  charts.ratingBar = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: DATA.ratings.labels,
      datasets: [{
        label: 'Titles',
        data: DATA.ratings.values,
        backgroundColor: DATA.ratings.values.map((_, i) => PALETTE[i % PALETTE.length]),
        borderRadius: 5,
        borderSkipped: false
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { tooltip: { callbacks: { label: i => ` ${i.raw.toLocaleString()} titles` } } },
      scales: {
        x: { ...scaleDefaults(), ticks: { color: '#f0f0f5' } },
        y: { ...scaleDefaults(), ticks: { color: '#9a9aab', callback: v => v >= 1000 ? (v/1000).toFixed(0)+'K' : v } }
      },
      animation: { duration: 900 }
    }
  });
}

/* TAB 4 — Freshness */
function buildMonthlyFreshChart() {
  if (charts.monthlyFreshChart) return;
  const ctx = document.getElementById('monthlyFreshChart');
  if (!ctx) return;

  charts.monthlyFreshChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: DATA.monthly.labels,
      datasets: [
        {
          label: 'Titles Added',
          data: DATA.monthly.values,
          borderColor: GREEN,
          backgroundColor: 'rgba(0,184,148,0.15)',
          pointBackgroundColor: GREEN,
          pointBorderColor: '#fff',
          pointRadius: 6,
          pointHoverRadius: 9,
          borderWidth: 2.5,
          fill: true,
          tension: 0.4
        },
        {
          label: 'Average',
          data: Array(12).fill(Math.round(DATA.monthly.values.reduce((a, b) => a + b, 0) / 12)),
          borderColor: 'rgba(229,9,20,0.5)',
          backgroundColor: 'transparent',
          pointRadius: 0,
          borderWidth: 1.5,
          borderDash: [6, 4],
          tension: 0
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: true,
          position: 'top',
          align: 'end',
          labels: { color: '#9a9aab', font: { size: 11 }, padding: 12, boxWidth: 18 }
        },
        tooltip: { callbacks: { label: i => ` ${i.dataset.label}: ${i.raw.toLocaleString()}` } }
      },
      scales: {
        x: scaleDefaults(),
        y: {
          ...scaleDefaults(),
          min: 400,
          ticks: { color: '#9a9aab', callback: v => v >= 1000 ? (v/1000).toFixed(1)+'K' : v }
        }
      },
      animation: { duration: 900 }
    }
  });
}

function buildFreshnessDonut() {
  if (charts.freshnessDonut) return;
  const ctx = document.getElementById('freshnessDonut');
  if (!ctx) return;

  charts.freshnessDonut = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Fresh (within 1yr)', 'Back-Catalogue (>1yr)'],
      datasets: [{
        data: [55, 45],
        backgroundColor: [GREEN, '#636e72'],
        borderWidth: 0,
        hoverOffset: 8
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '68%',
      plugins: {
        legend: {
          display: true,
          position: 'bottom',
          labels: { color: '#9a9aab', font: { size: 12 }, padding: 16, boxWidth: 12 }
        },
        tooltip: { callbacks: { label: i => ` ${i.label}: ${i.raw}%` } }
      },
      animation: { duration: 900 }
    }
  });
}

function buildFreshYearlyStack() {
  if (charts.freshYearlyStack) return;
  const ctx = document.getElementById('freshYearlyStack');
  if (!ctx) return;

  const recent = [9,11,12,13,14,15,16];
  const labels = DATA.yearly.labels.slice(-recent.length < 0 ? 0 : DATA.yearly.labels.length - 7);
  const movies = DATA.yearly.movies.slice(-7);
  const tv     = DATA.yearly.tv.slice(-7);
  const totalLabels = DATA.yearly.labels.slice(-7);

  charts.freshYearlyStack = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: totalLabels,
      datasets: [
        {
          label: 'Movies',
          data: movies,
          backgroundColor: RED,
          borderRadius: 4,
          borderSkipped: false
        },
        {
          label: 'TV Shows',
          data: tv,
          backgroundColor: TEAL,
          borderRadius: 4,
          borderSkipped: false
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: true,
          position: 'top',
          align: 'end',
          labels: { color: '#9a9aab', font: { size: 11 }, padding: 12, boxWidth: 12 }
        },
        tooltip: {
          callbacks: {
            footer: items => 'Total: ' + items.reduce((s, i) => s + i.raw, 0).toLocaleString()
          }
        }
      },
      scales: {
        x: { ...scaleDefaults(), stacked: true },
        y: {
          ...scaleDefaults(),
          stacked: true,
          ticks: { color: '#9a9aab', callback: v => v >= 1000 ? (v/1000).toFixed(1)+'K' : v }
        }
      },
      animation: { duration: 900 }
    }
  });
}

// ════════════════════════════════════════════════════
// TAB → CHART MAP
// ════════════════════════════════════════════════════
function renderChartsForTab(tabId) {
  switch (tabId) {
    case 'overview':
      buildYearlyChart();
      buildSplitDonut();
      buildTvShareLine();
      buildMonthlyBar();
      break;
    case 'global':
      buildCountryBar();
      buildIndiaUsDonut();
      buildCountryPie();
      break;
    case 'genre':
      buildGenreBar();
      buildAudienceDonut();
      buildRatingBar();
      break;
    case 'freshness':
      buildMonthlyFreshChart();
      buildFreshnessDonut();
      buildFreshYearlyStack();
      break;
  }
}

// ════════════════════════════════════════════════════
// INIT
// ════════════════════════════════════════════════════
document.addEventListener('DOMContentLoaded', () => {
  // Render first tab
  renderChartsForTab('overview');

  // Start count-up animations with a small delay
  setTimeout(startCountUps, 300);

  // Staggered KPI card entrance
  const kpiCards = document.querySelectorAll('.kpi-card');
  kpiCards.forEach((card, i) => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    setTimeout(() => {
      card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
      card.style.opacity = '1';
      card.style.transform = 'translateY(0)';
    }, 100 + i * 80);
  });
});
