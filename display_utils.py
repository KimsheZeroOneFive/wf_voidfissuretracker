import sys
from datetime import datetime, timezone
from config import (
    TIER_ICONS,
    MISSION_COLORS,
    HIGHLIGHT_TIERS,
    HIGHLIGHT_MISSIONS,
    HIGHLIGHT_BG,
    HIGHLIGHT_FG,
    STEEL_NOTE,
    SEPARATOR_LENGTH,
    INDENT,
    TIER_ORDER,
    MAX_MISSION_NAME_LENGTH,
    PADDING_BUFFER,
    ANSI_CLEAR_BELOW,
    ANSI_SAVE_CURSOR,
    ANSI_RESTORE_CURSOR,
    HEADER_COLOR,
    COLOR_RESET
)

# ANSI code to clear from cursor to end of line
ANSI_CLEAR_LINE = "\033[K"

# Load ASCII header ONCE at module import and apply color
try:
    with open("warframe_ascii.txt", "r") as f:
        raw_header = f.read().splitlines()
        # MODIFIED: Apply color to each line of the header
        ASCII_HEADER = [HEADER_COLOR + line + COLOR_RESET for line in raw_header]
except FileNotFoundError:
    ASCII_HEADER = []


def print_fissures(fissures):
    separator = "=" * SEPARATOR_LENGTH

    # Build header (using pre-loaded ASCII_HEADER)
    header_lines = [line + ANSI_CLEAR_LINE for line in ASCII_HEADER] + [
        ANSI_CLEAR_LINE,
        INDENT + separator + ANSI_CLEAR_LINE,
        INDENT + "VOID FISSURES".center(SEPARATOR_LENGTH) + ANSI_CLEAR_LINE,
        INDENT + separator + ANSI_CLEAR_LINE
    ]

    if not fissures:
        no_fissures_msg = INDENT + "No active fissures detected".center(SEPARATOR_LENGTH) + ANSI_CLEAR_LINE
        full_output = "\n".join(header_lines + [no_fissures_msg])
        full_output += "\n" + ANSI_CLEAR_BELOW
        return full_output

    current_time = datetime.now(timezone.utc)
    tier_groups = {tier: [] for tier in TIER_ORDER}

    # Pre-calculate max lengths
    all_nodes = []
    all_missions = []
    for fissure_data in fissures:
        fissure, expiry, is_hard = fissure_data
        tier = fissure['tier']

        # Normalize to UTC
        expiry = expiry.astimezone(timezone.utc) if expiry.tzinfo else expiry.replace(tzinfo=timezone.utc)
        remaining = expiry - current_time

        if remaining.total_seconds() <= 0:
            continue

        node = fissure['node']
        mission = fissure['missionType']

        all_nodes.append(node)
        all_missions.append(mission)
        tier_groups[tier].append((node, mission, is_hard, remaining))

    max_node_len = max(len(node) for node in all_nodes) if all_nodes else 0
    max_mission_len = max(len(mission) for mission in all_missions) if all_missions else 0

    # Build content lines
    content_lines = []
    for tier in TIER_ORDER:
        if not tier_groups[tier]:
            continue

        # One blank line between tier groups (not before the first)
        if content_lines and content_lines[-1] != ANSI_CLEAR_LINE:
            content_lines.append(ANSI_CLEAR_LINE)

        content_lines.append(f"{INDENT}{TIER_ICONS.get(tier, '●')} {tier.upper()} FISSURES:{ANSI_CLEAR_LINE}")

        for node, mission, is_hard, remaining in tier_groups[tier]:
            total_seconds = int(remaining.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            # Prevent timer overflow
            time_str = (
                f"{hours}h {minutes:02d}m {seconds:02d}s"
                if hours < 10
                else f"{hours}h_{minutes:02d}m_{seconds:02d}s"
            )

            # Mission processing (pad based on raw text; color after)
            raw_mission = mission
            display_mission = raw_mission.replace(' ', '_') if (len(raw_mission) > MAX_MISSION_NAME_LENGTH and ' ' in raw_mission) else raw_mission
            color_code = MISSION_COLORS.get(raw_mission, COLOR_RESET)  # MODIFIED: Use COLOR_RESET instead of hardcoded
            colored_mission = f"{color_code}{display_mission}{COLOR_RESET}"  # MODIFIED: Use COLOR_RESET

            # Highlight logic
            highlight_on = ""
            highlight_off = ""
            if mission in HIGHLIGHT_MISSIONS and tier in HIGHLIGHT_TIERS:
                highlight_on = f"{HIGHLIGHT_BG}{HIGHLIGHT_FG}"
                highlight_off = COLOR_RESET  # MODIFIED: Use COLOR_RESET

            # Padding uses raw mission length; add small visual buffer
            padding_needed = max_mission_len - len(raw_mission) + PADDING_BUFFER
            padding = ' ' * max(0, padding_needed)

            steel_note = STEEL_NOTE if is_hard else ""

            line_content = (
                f"{highlight_on}{node.ljust(max_node_len)}{highlight_off}"
                " : "
                f"{colored_mission}{padding}"
                f"⌛ {time_str}"
                f"{steel_note}"
            )
            # Prevent color bleed to next line
            if not line_content.endswith(COLOR_RESET):  # MODIFIED: Use COLOR_RESET
                line_content += COLOR_RESET  # MODIFIED: Use COLOR_RESET

            content_lines.append(INDENT + line_content + ANSI_CLEAR_LINE)

    # Compile full output
    full_output = "\n".join(header_lines + content_lines)

    # Clear everything below the output to prevent clumping
    full_output += "\n" + ANSI_CLEAR_BELOW

    if not full_output.endswith(COLOR_RESET):  # MODIFIED: Use COLOR_RESET
        full_output += COLOR_RESET  # MODIFIED: Use COLOR_RESET
    return full_output
