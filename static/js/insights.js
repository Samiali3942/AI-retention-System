async function fetchInsights() {
  const res = await fetch('/api/insights');
  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: 'Failed to load' }));
    throw new Error(err.error || 'Failed to load insights');
  }
  return res.json();
}

function createCanvasCol(id) {
  const col = document.createElement('div');
  col.className = 'col-12 col-md-6 col-xl-4';
  const card = document.createElement('div');
  card.className = 'card';
  const body = document.createElement('div');
  body.className = 'card-body';
  const canvas = document.createElement('canvas');
  canvas.id = id;
  body.appendChild(canvas);
  card.appendChild(body);
  col.appendChild(card);
  return { col, canvas };
}

function renderBarChart(ctx, label, labels, data) {
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [{ label, data, backgroundColor: 'rgba(54, 162, 235, 0.5)' }],
    },
    options: { responsive: true, maintainAspectRatio: false, scales: { x: { ticks: { autoSkip: false } } } },
  });
}

function renderPieChart(ctx, label, labels, data) {
  new Chart(ctx, {
    type: 'pie',
    data: { labels, datasets: [{ label, data }] },
    options: { responsive: true, maintainAspectRatio: false },
  });
}

async function init() {
  try {
    const data = await fetchInsights();
    const shape = document.getElementById('shape');
    if (shape) {
      shape.textContent = `${data.shape.rows} rows, ${data.shape.cols} cols`;
    }

    if (data.notice) {
      const shape = document.getElementById('shape');
      if (shape) shape.textContent = 'No data found. Please upload newone.csv';
      return;
    }

    const numericWrap = document.getElementById('numeric-charts');
    Object.keys(data.numeric || {}).forEach((col) => {
      const id = `num-${col}`;
      const { col: div, canvas } = createCanvasCol(id);
      numericWrap.appendChild(div);
      div.style.height = '320px';
      renderBarChart(canvas.getContext('2d'), col, data.numeric[col].labels, data.numeric[col].counts);
    });

    const categoricalWrap = document.getElementById('categorical-charts');
    Object.keys(data.categorical || {}).forEach((col) => {
      const id = `cat-${col}`;
      const { col: div, canvas } = createCanvasCol(id);
      categoricalWrap.appendChild(div);
      div.style.height = '320px';
      renderBarChart(canvas.getContext('2d'), col, data.categorical[col].labels, data.categorical[col].counts);
    });

    const extraWrap = document.getElementById('extra-charts');
    if (data.extra) {
      Object.keys(data.extra).forEach((key) => {
        const id = `extra-${key}`;
        const { col: div, canvas } = createCanvasCol(id);
        extraWrap.appendChild(div);
        div.style.height = '320px';
        const labels = data.extra[key].labels;
        const counts = data.extra[key].counts;
        const usePie = labels.length <= 6;
        if (usePie) {
          renderPieChart(canvas.getContext('2d'), key, labels, counts);
        } else {
          renderBarChart(canvas.getContext('2d'), key, labels, counts);
        }
      });
    }
  } catch (e) {
    console.error(e);
    alert(`Failed to load insights: ${e.message}`);
  }
}

document.addEventListener('DOMContentLoaded', init);


