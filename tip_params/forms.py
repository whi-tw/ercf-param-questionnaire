from django import forms

from .models import Filament, Hotend, Nozzle, ToolchangeParameters


class UploadSuperSlicerConfigForm(forms.Form):
    superslicer_config_file = forms.FileField()


class FormatUploadedConfigForm(forms.Form):
    test = forms.CharField(max_length=255)


class HotendForm(forms.ModelForm):
    class Meta:
        model = Hotend
        fields = ["manufacturer", "model", "notes"]


class NozzleForm(forms.ModelForm):
    class Meta:
        model = Nozzle
        fields = ["manufacturer", "model", "diameter", "notes"]


class FilamentForm(forms.ModelForm):
    class Meta:
        model = Filament
        fields = ["manufacturer", "model", "diameter"]


class ToolChangeParametersForm(forms.ModelForm):
    class Meta:
        model = ToolchangeParameters
        fields = ["toolchange_temperature", "string_reduction_enable_skinnydip"]
