{% if nlp.get_descriptions() %}

In addition, for this experiment, DAI used NLP-model-based transformations in the final model pipeline. The assumptions and limitations for each of the NLP transformers are as follows:

{% for description in nlp.get_descriptions() %}

#### {{ description.name }}

{{ description.description}}

**Assumptions**: {{ description.assumptions}}

**Limitations**: {{ description.limitations}}

{% endfor%}

{% endif %}

