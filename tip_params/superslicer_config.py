import configparser
import os
import tempfile
from typing import Any, Dict, List


def receive_superslicer_config(config_file) -> List[Dict[str, Dict[str, Any]]]:
    temp_file = tempfile.NamedTemporaryFile(
        prefix="uploaded_ss_config_", suffix=".ini", delete=False, mode="wb+"
    )
    toolchange_parameters = []
    try:
        with temp_file as destination:
            for chunk in config_file.chunks():
                destination.write(chunk)

        config = configparser.ConfigParser()
        config.read(temp_file.name)
        for section in config.sections():
            if not section.startswith("filament"):
                continue

            config_name = section.removeprefix("filament:")
            filament_values = {
                "name": config_name,
                "diameter": config.getfloat(section, "filament_diameter"),
            }
            toolchange_parameters_values = {}
            toolchange_parameters_values["toolchange_temperature"] = (
                config.getint(section, "filament_toolchange_temp")
                if config.getboolean(section, "filament_enable_toolchange_temp")
                else 0
            )
            toolchange_parameters_values[
                "string_reduction_enable_skinnydip"
            ] = config.getboolean(section, "filament_use_skinnydip")
            toolchange_parameters_values[
                "string_reduction_insertion_distance"
            ] = config.getfloat(section, "filament_skinnydip_distance")
            toolchange_parameters_values[
                "string_reduction_pause_in_melt_zone"
            ] = config.getint(section, "filament_melt_zone_pause")
            toolchange_parameters_values[
                "string_reduction_pause_before_extraction"
            ] = config.getint(section, "filament_cooling_zone_pause")
            toolchange_parameters_values[
                "string_reduction_speed_to_move_into_melt_zone"
            ] = config.getint(section, "filament_dip_insertion_speed")
            toolchange_parameters_values[
                "string_reduction_speed_to_extract_from_melt_zone"
            ] = config.getint(section, "filament_dip_extraction_speed")
            toolchange_parameters_values[
                "minimal_purge_on_wipe_tower"
            ] = config.getfloat(section, "filament_minimal_purge_on_wipe_tower")
            toolchange_parameters_values[
                "max_speed_on_the_wipe_tower"
            ] = config.getfloat(section, "filament_max_wipe_tower_speed")
            toolchange_parameters_values["loading_speed_at_start"] = config.getfloat(
                section, "filament_loading_speed_start"
            )
            toolchange_parameters_values["loading_speed"] = (
                config.getfloat(section, "filament_loading_speed"),
            )
            toolchange_parameters_values["unloading_speed_at_start"] = config.getfloat(
                section, "filament_unloading_speed_start"
            )
            toolchange_parameters_values["unloading_speed"] = (
                config.getfloat(section, "filament_unloading_speed"),
            )
            toolchange_parameters_values["number_of_cooling_moves"] = config.getfloat(
                section, "filament_cooling_moves"
            )
            toolchange_parameters_values[
                "speed_of_the_first_cooling_move"
            ] = config.getfloat(section, "filament_cooling_initial_speed")
            toolchange_parameters_values[
                "speed_of_the_last_cooling_move"
            ] = config.getfloat(section, "filament_cooling_final_speed")
            toolchange_parameters_values["pigment_percentage"] = config.getfloat(
                section, "filament_wipe_advanced_pigment"
            )
            toolchange_parameters_values["ramming_parameters"] = (
                config.get(section, "filament_ramming_parameters"),
            )
            toolchange_parameters.append(
                {
                    "filament": filament_values,
                    "toolchange_parameters": toolchange_parameters_values,
                }
            )

        os.remove(temp_file.name)
        return toolchange_parameters
    except Exception as e:
        os.remove(temp_file.name)
        print(e)
        return toolchange_parameters
