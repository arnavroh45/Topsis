from django import forms
#models.py are used to define database models, we used forms here instead of models as we are not storing the inputs in a database rather just need it for processing of the ranks
# if we want to store the inputs for future reference we can use models.py

#idea - use models.py and keep a history for each user
class TopsisForm(forms.Form):
    input_file = forms.FileField(label='CSV Input File')
    weights = forms.CharField(label='Weights (comma-separated)', max_length=100)
    impacts = forms.CharField(label='Impacts (comma-separated + or -)', max_length=100)
