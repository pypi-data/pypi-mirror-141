{% if config.autodoc_full_architecture_in_appendix and nlp.get_descriptions() %}

### Advanced NLP and Image Transformation Architectures

{% for description in nlp.get_descriptions() %}

#### {{ description.name }}

```
{{description.architecture}}
```

{% if  'embedding'  in description  %}

{{ description.embedding}}

{% endif %}

{% endfor%}

{% endif %}

