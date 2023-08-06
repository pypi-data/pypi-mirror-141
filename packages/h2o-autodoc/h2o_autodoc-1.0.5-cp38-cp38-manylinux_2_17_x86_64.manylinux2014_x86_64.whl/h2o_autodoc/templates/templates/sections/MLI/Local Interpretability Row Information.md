{% if mli._individual_rows %}

{% for row, info in
mli.get_individual_info(config.autodoc_num_features,config.autodoc_num_features).items()%}

{% if show_row_value %}ROW INDEX: {{row}}

{{  info["formatted"] }}

{% endif %}

{% if show_klime_table %}{% if mli.has_klime() %}KLIME FOR ROW: {{row}}

{{ info["klime"] }}

{% endif %}{% endif %}

{% if show_loco_plot %}LOCO PLOT FOR ROW: {{row}}

{{info["loco"]["rendered_image"]}}

{% endif %}

{% if show_ice_plots %}ICE PLOTS FOR ROW: {{row}}

{% for feature, ice in info["ice"].items() %}

{{ice["rendered_image"]}}

{% endfor %}

{% endif %}{% endfor %}{% else %}The user did not select any individual
records.{% endif %}
