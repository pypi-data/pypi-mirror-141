{% if nlp.get_descriptions() %}

{% for description in nlp.get_descriptions() %}

DAI used NLP-model-based transformations in the final model pipeline. The sampling approach for each transformer is detailed below:

- **{{description.name}}** : {{description.sampling}}

{% endfor%}

{% endif %}

