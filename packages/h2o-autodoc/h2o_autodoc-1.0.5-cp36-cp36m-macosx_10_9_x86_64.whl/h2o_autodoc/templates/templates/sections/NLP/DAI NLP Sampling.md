{% if nlp.get_descriptions() %}

**NLP Sampling**

Driverless AI applied NLP-specific sampling techniques as part of the final model pipeline. The sampling approach for each NLP-based transformation is detailed below:

{% for description in nlp.get_descriptions() %}

#### {{ description.name }} 

{{ description.description }}

**Sampling Approach**: {{ description.sampling }}

{% endfor%}

{% endif %}

