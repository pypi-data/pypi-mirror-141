{{final_model._final_model_desc.overview}}

{% for key, value in final_model._final_model_desc.base_learners.items()%}

- {{value.string|e}}

{{value.params}}

{% endfor %}