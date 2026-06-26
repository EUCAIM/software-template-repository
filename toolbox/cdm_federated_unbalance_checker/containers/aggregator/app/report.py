#!/usr/bin/env python3

import math

__template_output__ = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Data Imbalance Dashboard</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #0f172a;
      --panel: #0b1020;
      --card: #11182d;
      --accent: #4f46e5;
      --accent-2: #22d3ee;
      --muted: #94a3b8;
      --text: #e2e8f0;
      --good: #22c55e;
      --warn: #f59e0b;
      --bad: #ef4444;
      --border: #1e293b;
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      min-height: 100vh;
      font-family: 'Space Grotesk', 'Segoe UI', sans-serif;
      color: var(--text);
      background: radial-gradient(circle at 10% 20%, rgba(79, 70, 229, 0.18), transparent 30%),
                  radial-gradient(circle at 80% 10%, rgba(34, 211, 238, 0.16), transparent 26%),
                  linear-gradient(135deg, #0a0f1f 0%, #0d1528 100%);
      display: flex;
      justify-content: center;
      padding: 32px;
    }

    .shell {
      width: min(1200px, 100%);
    }

    header {
      display: flex;
      align-items: flex-end;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 20px;
    }

    h1 {
      margin: 0;
      font-size: 28px;
      letter-spacing: -0.02em;
    }

    .subtitle {
      color: var(--muted);
      margin: 4px 0 0;
      font-size: 15px;
    }

    .legend {
      display: flex;
      gap: 8px;
      align-items: center;
      color: var(--muted);
      font-size: 13px;
    }

    .chip {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 10px;
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border);
    }

    .pill {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 4px 8px;
      border-radius: 12px;
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      font-weight: 600;
      border: 1px solid var(--border);
    }

    .pill.good { color: var(--good); background: rgba(34, 197, 94, 0.08); }
    .pill.bad { color: var(--bad); background: rgba(239, 68, 68, 0.08); }
    .pill.warn { color: var(--warn); background: rgba(245, 158, 11, 0.08); }

    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 12px;
      margin-bottom: 20px;
    }

    .card {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 16px;
      box-shadow: 0 15px 40px rgba(0, 0, 0, 0.35);
    }

    .card h3 {
      margin: 0 0 8px;
      font-size: 15px;
      color: var(--muted);
      font-weight: 500;
    }

    .metric {
      font-size: 26px;
      font-weight: 600;
      display: flex;
      align-items: baseline;
      gap: 6px;
    }

    .metric span.small { font-size: 14px; color: var(--muted); }

    .table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 6px;
    }

    .table thead {
      color: var(--muted);
      font-size: 13px;
    }

    .table th, .table td {
      padding: 10px 12px;
      border-bottom: 1px solid var(--border);
      text-align: left;
      font-size: 14px;
    }

    .table tbody tr:hover { background: rgba(255, 255, 255, 0.02); }

    .badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 8px;
      border-radius: 10px;
      border: 1px solid var(--border);
      font-size: 12px;
    }

    .badge i {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      display: inline-block;
    }

    .badge.good { color: var(--good); }
    .badge.good i { background: var(--good); }
    .badge.bad { color: var(--bad); }
    .badge.bad i { background: var(--bad); }

    .panel {
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 18px;
      margin-top: 14px;
    }

    .section-title {
      margin: 0 0 8px;
      font-size: 18px;
      letter-spacing: -0.01em;
    }

    .muted { color: var(--muted); }

    @media (max-width: 720px) {
      header { flex-direction: column; align-items: flex-start; }
      .table { display: block; overflow-x: auto; }
    }
  </style>
</head>
<body>
  <div class="shell">
    <header>
      <div>
        <h1>Data Imbalance Dashboard</h1>
        <p class="subtitle">Individual datasets and their federated combination.</p>
      </div>
    </header>

    <div class="grid" id="summary-cards"></div>

    <div class="panel">
      <h2 class="section-title">Individual Datasets</h2>
      <table class="table" id="datasets-table"></table>
    </div>
  </div>

  <script>
    const datasetStats = [
      ###datasetStats###
    ];

    const valdBool = (value) => value ? '<span class="pill good">Valid</span>' : '<span class="pill bad">Invalid</span>';
    const fmtBool = (value) => value ? '<span class="pill bad">Unbalanced</span>' : '<span class="pill good">Balanced</span>';

    function renderSummary() {

      const cards = [
        ###aggregatedStats###
      ];

      document.getElementById('summary-cards').innerHTML = cards.map(card => `
        <div class="card">
          <h3>${card.title}</h3>
          <div class="metric">${card.value}<span class="small">${card.hint}</span></div>
        </div>
      `).join('');
    }

    function renderDatasets() {
      const head = `
        <thead>
          <tr>
            <th>Dataset</th>
            <th>Valid</th>
            <th>Format</th>
            <th>Patients</th>
            <th>Age (mean +/- std)</th>
            <th>Sex</th>
            <th>Ethnicity</th>
            <th>Age</th>
            <th>Sex</th>
            <th>Ethnicity</th>
          </tr>
        </thead>`;

      const body = datasetStats.map(ds => {
        const sexBreakdown = ds.valid == "Valid" ? Object.entries(ds.stats.sex).map(([k, v]) => `${k}: ${v}`).join(', ') : ds.stats.sex;
        const ethBreakdown = ds.valid == "Valid" ? Object.entries(ds.stats.ethnicity).map(([k, v]) => `${k}: ${v}`).join(', ') : ds.stats.ethnicity;
        return `
          <tr>
            <td>${ds.label}</td>
            <td>${valdBool(ds.valid == "Valid")}</td>
            <td>${ds.stats.format}</td>
            <td>${ds.stats.patients}</td>
            <td>${ds.valid == "Valid" ? ds.stats.ageMean.toFixed(2) : ds.stats.ageMean} ${ds.valid == "Valid" ? " +/- " : ""} ${ds.valid == "Valid" ? ds.stats.ageStd.toFixed(2) : ""}</td>
            <td>${sexBreakdown}</td>
            <td>${ethBreakdown}</td>
            <td>${fmtBool(ds.imbalance.age)}</td>
            <td>${fmtBool(ds.imbalance.sex)}</td>
            <td>${fmtBool(ds.imbalance.ethnicity)}</td>
          </tr>`;
      }).join('');

      document.getElementById('datasets-table').innerHTML = head + '<tbody>' + body + '</tbody>';
    }

    renderSummary();
    renderDatasets();
  </script>
</body>
</html>
"""

def get_stats(ds, label):
    if label == 'exitcode':
        return '"Valid"' if ds['exitcode'] == 0 else '"Invalid"'
    elif label == 'dataset_id':
        return '"' + str(ds['dataset_id']) + '"'
    elif label == 'dataset_type':
        return '"' + str(ds['dataset_type']) + '"'

    if ds['exitcode'] != 0:
        return '"Unknown"'
    
    if label in ('num_patients', 'age_mean', 'age_std'):
        return str(ds[label])
    elif label == 'sex':
        if ds['sex_counts'] is None:
            return '"NA"'
        else:
          return '{ ' + ','.join([ k + ': ' + str(v) for k,v in ds['sex_counts'].items()]) + ' }'
    elif label == 'ethnicity':
        if ds['ethnicity_counts'] is None:
            return '"NA"'
        else:
            return '{ ' + ','.join([ k + ': ' + str(v) for k,v in ds['ethnicity_counts'].items()]) + ' }'

def age_imbalance_single(stats, max_cv=0.25, min_std=1.0):
    mean = stats['age_mean']
    std = stats['age_std']
    
    if mean is None or mean <= 0:
        return 'true' #, {"reason": "invalid_mean"}

    cv = std / mean
    
    imbalance = (cv > max_cv) or (std < min_std)
    
    return 'true' if imbalance else 'false' #, {
    #    "mean": mean,
    #    "std": std,
    #    "cv": cv
    #}

def categorical_imbalance_single(counts, min_frac = 0.3, entropy_threshold = 0.6):
    if counts is None:
        return 'true'
    
    total = sum(counts.values())
    if total == 0:
        return 'true' #, {"reason": "empty_counts"}
    
    fractions = {k: v / total for k, v in counts.items()}
    dominant_frac = max(fractions.values())

    # If only one category, thre is no problem locally but at federation level
    if len(fractions) == 1:
        return 'false'
    
    # Shannon entropy (normalized)
    entropy = -sum(p * math.log(p) for p in fractions.values())
    max_entropy = math.log(len(fractions))
    norm_entropy = entropy / max_entropy if max_entropy > 0 else 0
    
    imbalance = (
        dominant_frac > (1 - min_frac) or
        norm_entropy < entropy_threshold
    )
    
    return 'true' if imbalance else 'false' #, {
    #    "fractions": fractions,
    #    "dominant_frac": dominant_frac,
    #    "normalized_entropy": norm_entropy
    #}


def generate_html_report(output_path, aggregated_stats, dataset_stats):
    report_html = __template_output__

    individual_datset_info = ",\n      ".join(
        [
            "{ id: " + str(n) + ", label: " + get_stats(ds, 'dataset_id') + ", valid: " + get_stats(ds, 'exitcode') + ", format: " + get_stats(ds, 'dataset_type') + ", stats: {" +\
                " patients: " + get_stats(ds, 'num_patients') +\
                ", ageMean: " + get_stats(ds, 'age_mean') +\
                ", ageStd: " + get_stats(ds, 'age_std') +\
                ", sex: " + get_stats(ds, 'sex') +\
                ", ethnicity: " + get_stats(ds, "ethnicity") +\
            "}, imbalance: { age: " + age_imbalance_single(ds) +\
                ", sex: " + categorical_imbalance_single(ds['sex_counts']) +\
                ", ethnicity: " + categorical_imbalance_single(ds['ethnicity_counts']) +\
            "} }" for n,ds in enumerate(dataset_stats)
        ]
    )
    
    aggregated_dataset_infp = "{ title: 'Datasets', value: " + str(aggregated_stats['evaluated_sets']) + ", hint: 'sources of " + str(aggregated_stats['number_sets']) + "' }," +\
    "{ title: 'Age', value: '" + ('⚠️' if aggregated_stats['age_imbalance'] else '✔️') + "', hint: '" + ('This combination is imbalanced' if aggregated_stats['age_imbalance'] else '') + "'}, " +\
    "{ title: 'Sex', value: '" + ('⚠️' if aggregated_stats['sex_imbalance'] else '✔️') + "', hint: '" + ('This combination is imbalanced' if aggregated_stats['sex_imbalance'] else '') + "'}, " +\
    "{ title: 'Ethnicity', value: '" + ('⚠️' if aggregated_stats['ethnicity_imbalance'] else '✔️') + "', hint: '" + ('This combination is imbalanced' if aggregated_stats['ethnicity_imbalance'] else '') + "'}"


    report_html = report_html.replace("###datasetStats###", individual_datset_info)
    report_html = report_html.replace("###aggregatedStats###", aggregated_dataset_infp)

    with open(output_path, "w") as f:
        f.write(report_html)