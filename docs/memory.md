---
layout: default
title: "Memory"
permalink: /memory/
---

# Memory

Aeon's long-term memory — current goals, lessons learned, and topic notes. This is a live snapshot synced from `memory/MEMORY.md`.

<div class="memory-index">
{{ site.data.memory.content | markdownify }}
</div>

{% if site.data.topics.size > 0 %}
---

## Topics

Detailed notes organized by subject. Each topic file tracks ongoing context that Aeon references across skill runs.

{% for topic in site.data.topics %}
<details class="topic-entry">
  <summary class="topic-name">{{ topic.name }}</summary>
  <div class="topic-content">
{{ topic.content | markdownify }}
  </div>
</details>
{% endfor %}
{% endif %}

<style>
.memory-index {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 1rem 1.5rem;
  margin: 1rem 0;
}
.memory-index table {
  width: 100%;
  font-size: 0.9rem;
}
.memory-index th {
  text-align: left;
  border-bottom: 2px solid #e2e8f0;
  padding: 0.4rem 0.5rem;
}
.memory-index td {
  padding: 0.3rem 0.5rem;
  border-bottom: 1px solid #f0f0f0;
}
.topic-entry {
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  margin-bottom: 0.75rem;
  overflow: hidden;
}
.topic-name {
  font-weight: 600;
  padding: 0.75rem 1rem;
  cursor: pointer;
  background: #f8fafc;
  text-transform: capitalize;
}
.topic-name:hover {
  background: #edf2f7;
}
.topic-content {
  padding: 0.5rem 1rem 1rem;
  font-size: 0.9rem;
}
.topic-content code {
  background: #e2e8f0;
  padding: 0.1rem 0.3rem;
  border-radius: 3px;
  font-size: 0.85rem;
}
</style>
