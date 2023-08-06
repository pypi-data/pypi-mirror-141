**Feature Distribution Plots**

The following plots from the training dataset include histograms for numeric columns and count plots for categorical columns. Note, x-axis tick labels are not shown for categorical features with over {{config.cardinality_limit}} levels.

{% for image in final_features.histogram_plots(width=75, set_font_size=22).values() %}{{ image }}{% endfor %}