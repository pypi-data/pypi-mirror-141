{% if nlp.get_descriptions() %}

{% for description in nlp.get_descriptions() %}

DAI used NLP-model-based transformations in the final model pipeline. The transformer NLP-model components include:

- {{ nlp_transformer.name }}: {{ nlp_transformer.architecture}}

{% endfor%}

{% endif %}