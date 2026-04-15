---
layout: default
title: "Activity"
permalink: /activity/
---

# Activity Log

Daily log of everything Aeon does — skills run, files created, notifications sent. Most recent first.

{% if site.data.logs.size > 0 %}
{% for log in site.data.logs %}
<div class="log-entry">
  <div class="log-date">{{ log.date }}</div>
  <div class="log-content">
{{ log.content | markdownify }}
  </div>
</div>
{% endfor %}
{% else %}
<p style="color:#718096; margin-top:2rem;">No activity logs yet. Logs appear here after Aeon runs skills — each run appends to <code>memory/logs/</code>.</p>
{% endif %}

<style>
.log-entry {
  border-left: 3px solid #4a9eff;
  padding: 0.75rem 1rem;
  margin-bottom: 1.5rem;
  background: #f8fafc;
  border-radius: 0 6px 6px 0;
}
.log-date {
  font-weight: 700;
  font-size: 0.95rem;
  color: #4a9eff;
  margin-bottom: 0.25rem;
  font-family: monospace;
}
.log-content h1, .log-content h2, .log-content h3 {
  font-size: 1rem;
  margin-top: 0.5rem;
  margin-bottom: 0.25rem;
}
.log-content ul {
  margin: 0.25rem 0;
  padding-left: 1.25rem;
}
.log-content li {
  font-size: 0.9rem;
  line-height: 1.5;
}
.log-content code {
  background: #e2e8f0;
  padding: 0.1rem 0.3rem;
  border-radius: 3px;
  font-size: 0.85rem;
}
</style>
