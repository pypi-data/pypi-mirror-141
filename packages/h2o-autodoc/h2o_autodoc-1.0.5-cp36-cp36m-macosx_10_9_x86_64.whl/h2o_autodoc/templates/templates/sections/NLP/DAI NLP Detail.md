### {% if nlp.get_descriptions() %}Advanced NLP and Image Transformations
Driverless AI used advanced NLP/Image transformations in the final model pipeline. Detailed description of each advanced transformer includes the assumptions, limitations and the architecture of the transformer. There may be multiple transformers of the same type in the final pipeline having different architectures.

{% for description in nlp.get_descriptions(config.autodoc_transformer_architecture_max_lines) %}

#### {{ description.name }}

{{ description.description}}

**Assumptions**

{{ description.assumptions}}

**Limitations**

{{ description.limitations}}

**Sampling**

{{ description.sampling }}

**Architecture**

```
{{description.architecture}}
```

{% if  'embedding'  in description  %}

{{ description.embedding}}

{% endif %}

{% endfor%}

{% endif %}

