### Driverless Settings

{{section.table(
    columns=['Dial Settings', 'Description', 'Setting Value', 'Range of Possible Values'],
    data=[
        ['Accuracy', 'Controls accuracy needs of the model', params._params.accuracy, accuracy_range],
        ['Time', 'Controls duration of the experiment', params._params.time, time_range],
        ['Interpretability', 'Controls complexity of the model', params._params.interpretability, interpretability_range]
    ]
)}}
