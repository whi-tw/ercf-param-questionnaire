from django.db import models


class Manufacturer(models.Model):
    name = models.CharField(max_length=255)


class Hotend(models.Model):
    manufacturer: Manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.CASCADE
    )
    model = models.CharField(max_length=255)
    notes = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.manufacturer.name} {self.model}"


class Nozzle(models.Model):
    manufacturer: Manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.CASCADE
    )
    model = models.CharField(max_length=255)
    diameter = models.DecimalField(default=0.4, decimal_places=2, max_digits=3)
    notes = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.manufacturer.name} {self.model}"


class Filament(models.Model):
    class FilamentDiameter(float, models.Choices):
        ONE_SEVEN_FIVE = 1.75, "1.75mm"
        TWO_EIGHT_FIVE = 2.85, "2.85mm"

    manufacturer: Manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.CASCADE
    )
    model = models.CharField(max_length=255)
    diameter = models.DecimalField(
        default=FilamentDiameter.ONE_SEVEN_FIVE,
        decimal_places=2,
        max_digits=3,
        choices=FilamentDiameter.choices,
    )

    def __str__(self) -> str:
        return f"{self.manufacturer.name} {self.model} ({self.diameter}mm)"


class ToolchangeParameters(models.Model):
    hotend: Hotend = models.ForeignKey(Hotend, on_delete=models.CASCADE)
    nozzle: Nozzle = models.ForeignKey(Nozzle, on_delete=models.CASCADE)
    filament: Filament = models.ForeignKey(Filament, on_delete=models.CASCADE)

    _default_decimalfield_kwargs = {"decimal_places": 2, "max_digits": 5}

    # Multimaterial toolchange temperature

    toolchange_temperature = models.IntegerField(default=0)

    # Multimaterial toolchance string reduction

    string_reduction_enable_skinnydip = models.BooleanField(default=False)
    string_reduction_insertion_distance = models.DecimalField(
        default=31, **_default_decimalfield_kwargs
    )
    string_reduction_pause_in_melt_zone = models.IntegerField(default=0)
    string_reduction_pause_before_extraction = models.IntegerField(default=0)
    string_reduction_speed_to_move_into_melt_zone = models.DecimalField(
        default=33, **_default_decimalfield_kwargs
    )
    string_reduction_speed_to_extract_from_melt_zone = models.DecimalField(
        default=70, **_default_decimalfield_kwargs
    )

    # Wipe tower parameters

    minimal_purge_on_wipe_tower = models.DecimalField(
        default=15, **_default_decimalfield_kwargs
    )
    max_speed_on_the_wipe_tower = models.DecimalField(
        default=0, decimal_places=2, max_digits=3
    )

    # Toolchange parameters with single extruder MM printers

    loading_speed_at_start = models.DecimalField(
        default=3, **_default_decimalfield_kwargs
    )
    loading_speed = models.DecimalField(default=28, **_default_decimalfield_kwargs)
    unloading_speed_at_start = models.DecimalField(
        default=100, **_default_decimalfield_kwargs
    )
    unloading_speed = models.DecimalField(default=90, **_default_decimalfield_kwargs)
    number_of_cooling_moves = models.DecimalField(
        default=4, **_default_decimalfield_kwargs
    )
    speed_of_the_first_cooling_move = models.DecimalField(
        default=2.2, **_default_decimalfield_kwargs
    )
    speed_of_the_last_cooling_move = models.DecimalField(
        default=3.4, **_default_decimalfield_kwargs
    )
    pigment_percentage = models.DecimalField(
        default=0.5, **_default_decimalfield_kwargs
    )

    # ramming parameters
    total_ramming_time = models.DecimalField(
        default=2.5, **_default_decimalfield_kwargs
    )
    ramming_line_width = models.DecimalField(
        default=1.2, **_default_decimalfield_kwargs
    )
    ramming_line_spacing = models.DecimalField(
        default=1, **_default_decimalfield_kwargs
    )

    ramming_parameters = models.TextField(blank=True)
