---
layout: publication
permalink: /publications/
title: publications
description: publications
years: [2024, 2023, 2022, 2019, 2018, 2016, 2015, 2014]
nav: true
nav_order: 2
---
<!-- _pages/publications.md -->

<p>An up-to-date list is available on <a href="https://scholar.google.com/citations?user=30e95fEAAAAJ" target="_blank" rel="noopener noreferrer">Google Scholar</a>.</p>

<div class="publications">

{%- for y in page.years %}
  <h2 class="year">{{y}}</h2>
  {% bibliography -f {{ site.scholar.bibliography }} -q @*[year={{y}}]* %}
{% endfor %}

</div>
