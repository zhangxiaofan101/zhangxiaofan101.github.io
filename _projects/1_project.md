---
layout: page
title: Multi-stained Pathology Image Analysis
description: model pretraining, cross-strain image generation, lymphoma classification
img: assets/img/path_0.png
importance: 1
category: work
---


<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.html path="assets/img/path_wsi.png" title="Pathology WSIs with HE and IHC stains" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<!-- <div class="caption">
    This image can also have a caption. It's like magic.
</div> -->

Hematoxylin and Eosin (H&E) stained images are the most common modality of pathological images, while accurate tumor subtyping is reliant on the information provided by various Immunohistochemistry (IHC) images. 

We initially attempted qualitative and quantitative analyses on the PD-L1. The focus on the project of lymphoma diagnosis with both H&E image and tens of IHC markers, simulating the entire workflow of pathological diagnosis.

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.html path="assets/img/path_pdl1.jpg" title="Assessment of PD-L1 Expression" class="img-fluid rounded z-depth-1" %}
    </div>
</div>

#### Foundation Model PathoDuet

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.html path="assets/img/path_duet.png" title="Pretrain Framework" class="img-fluid rounded z-depth-1" %}
    </div>
</div>

Here is the proposed self-supervised learning (SSL) framework. This framework aims at exploiting characteristics of histopathological images by introducing a pretext token during the training. The pretext token is only a small piece of image, but contains special knowledge. [Code & Model](https://github.com/openmedlab/PathoDuet)

#### Foundation Model Adaptation PathoTune

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.html path="assets/img/path_tune.jpg" title="Adaptation Framework" class="img-fluid rounded z-depth-1" %}
    </div>
</div>

To mitigate foundation-task gap and the task-instance gap, we introduce PathoTune, a framework designed to efficiently adapt pathological or even visual foundation models to pathology-specific tasks via multi-modal prompt tuning.