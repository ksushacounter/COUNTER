def prepare_curve_data_for_visualization(curves_info, tag_ids, well_ids):
    scaling_interval = []
    well_curve_names = []
    for well_id in well_ids:
        curr_curves_info = curves_info[well_id]["curve_info"]
        interval = {}
        curve_names = {}
        for tag_id in tag_ids:
            interval[tag_id] = [None, None]
            curve_names[tag_id] = None
        for key in curr_curves_info:
            curve_type = curr_curves_info[key]["type"]
            if curve_type in tag_ids:
                interval[curve_type] = [
                    curr_curves_info[key]["min_value"],
                    curr_curves_info[key]["max_value"],
                ]
                curve_names[curve_type] = key
        scaling_interval.append([val for _, val in sorted(interval.items())])
        well_curve_names.append([val for _, val in sorted(curve_names.items())])
    return scaling_interval, well_curve_names


def update_visual_props(curve_tags_info, tag_ids):
    type_scale = {}
    type_display = {}
    priority = {}
    colors = {}
    auto_scaling = {}
    manual_scaling_interval = {}
    manual_scaling_step = {}

    for tag_name in list(curve_tags_info.keys()):
        if curve_tags_info[tag_name]["id"] in tag_ids:
            type_scale[curve_tags_info[tag_name]["id"]] = curve_tags_info[tag_name][
                "type_scale"
            ]
            type_display[curve_tags_info[tag_name]["id"]] = curve_tags_info[tag_name][
                "type_display"
            ]
            priority[curve_tags_info[tag_name]["id"]] = curve_tags_info[tag_name][
                "priority"
            ]
            colors[curve_tags_info[tag_name]["id"]] = curve_tags_info[tag_name][
                "line_color"
            ]
            auto_scaling[curve_tags_info[tag_name]["id"]] = curve_tags_info[tag_name][
                "auto_scaling"
            ]
            manual_scaling_interval[curve_tags_info[tag_name]["id"]] = curve_tags_info[
                tag_name
            ]["manual_scaling_interval"]
            manual_scaling_step[curve_tags_info[tag_name]["id"]] = curve_tags_info[
                tag_name
            ]["manual_scaling_step"]

    visual_properties = {
        "type_scale": [val for _, val in sorted(type_scale.items())],
        "type_display": [val for _, val in sorted(type_display.items())],
        "priority": [val for _, val in sorted(priority.items())],
        "colors": [val for _, val in sorted(colors.items())],
        "auto_scaling": [val for _, val in sorted(auto_scaling.items())],
        "manual_scaling_interval": [
            val for _, val in sorted(manual_scaling_interval.items())
        ],
        "manual_scaling_step": [val for _, val in sorted(manual_scaling_step.items())],
    }

    return visual_properties


def get_strat_levels(well_ids, strat_levels_info):
    strat_levels_names = []
    strat_levels_depths = []
    for i in range(len(well_ids)):
        well_start_levels = strat_levels_info[well_ids[i]]["strat_levels"]
        strat_levels_names.append(list(well_start_levels.keys()))
        level_depths = []
        for strat_level in strat_levels_names[i]:
            level_depths.append(well_start_levels[strat_level]["level_depth"])
        strat_levels_depths.append(level_depths)
    return strat_levels_names, strat_levels_depths
