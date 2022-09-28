from django.shortcuts import redirect, render

from .forms import (
    FilamentForm,
    HotendForm,
    NozzleForm,
    ToolChangeParametersForm,
    UploadSuperSlicerConfigForm,
)
from .superslicer_config import receive_superslicer_config


def upload_ss_config_form(request):
    if request.method == "POST":
        ss_config_form = UploadSuperSlicerConfigForm(request.POST, request.FILES)
        if ss_config_form.is_valid():
            uploaded_file = request.FILES["superslicer_config_file"]
            if uploaded_file:
                toolchange_parameters = receive_superslicer_config(uploaded_file)
                params_forms = []

                for param_instance in toolchange_parameters:
                    form_collection = {
                        "filament": FilamentForm(initial=param_instance["filament"]),
                        "toolchange_parameters": ToolChangeParametersForm(
                            initial=param_instance["toolchange_parameters"]
                        ),
                    }
                    params_forms.append(form_collection)

                return render(
                    request,
                    "format_uploaded_config.html",
                    {
                        "params_forms": params_forms,
                        "nozzle_form": NozzleForm(),
                        "hotend_form": HotendForm(),
                    },
                )

    else:
        ss_config_form = UploadSuperSlicerConfigForm()

    return render(
        request,
        "config_upload.html",
        {
            "ss_config_form": ss_config_form,
        },
    )
