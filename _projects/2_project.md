---
layout: page
title: Large Language Model in Medical Domain
description: prompt Learning, RLHF related, downstream tasks
img: assets/img/llm_0.png
importance: 2
category: work
---

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.html path="assets/img/llm_1.png" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<!-- <div class="caption">
    This image can also have a caption. It's like magic.
</div> -->

We collected a dataset consists of textbooks, guidelines, EHR, medical & generic domain instruction tuning task, Q&A tasks, multi-round dialog, plugins to fine-tune a large language model (LLM) in medical domain.

A self-evaluation prompt is added in the reward model training and standard PPO framework are further optimized for better performance. Plugins for the downstream applications are under development.


We released [PULSE](https://github.com/openmedlab/PULSE), a Chinese medical large language model and its related applications.

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.html path="assets/img/llm_logo.jpg" title="PULSE" class="img-fluid rounded z-depth-1" %}
    </div>
</div>

### Elo Evaluation
| model_name                    | model_size   |   ALL |   MedQA_Mainland |   PromptCBLUE |   webMedQA |
|:------------------------------|:-------------|------:|-----------------:|--------------:|-----------:|
| GPT4                          | 220B*8(?)    |  1195 |             1087 |          1134 |       1107 |
| ChatGPT                       | 175B(?)      |  1123 |             1053 |          1089 |       1067 |
| PULSE_7b with prompt          | 7B           |  1074 |             1019 |          1047 |       1060 |
| PULSE_14b                     | 14B          |  1055 |             1001 |          1037 |       1056 |
| PULSE_7b                      | 7B           |  1054 |             1028 |          1037 |       1030 |
| BianQue                       | 6B           |   926 |              939 |           920 |       1011 |
| QiZhenGPT                     | 13B          |   918 |              949 |           935 |        974 |
| Med-ChatGLM                   | 6B           |   864 |              988 |           921 |        859 |
| BenTsao                       | 7B           |   846 |              966 |           913 |        859 |
| DoctorGLM                     | 6B           |   812 |              935 |           891 |        856 |