HIGHLIGHT_MISSIONS = {'Defense', 'Rescue', 'Extermination', 'Capture', 'Survival'}
HIGHLIGHT_TIERS = {'Axi'}
HIGHLIGHT_BG = "\033[47m"           # White background
HIGHLIGHT_FG = "\033[30m"           # Black text
TIER_ICONS = {                      # There TIER_ICONS is more readable
    'Lith': '🪨',
    'Meso': '🟡',
    'Neo': '🔵',
    'Axi': '💠',
    'Omnia': '✨',
    'Requiem': '💀'
}
STEEL_NOTE = " \033[91m⚔️\033[0m"   # Red sword symbol for Steel Path
COLOR_RESET = '\033[0m'
HEADER_COLOR = '\033[97m'           # Bright white for ASCII header
MISSION_COLORS = {
    'Extermination': '\033[91m',    # Red
    'Sabotage': '\033[93m',         # Yellow
    'Rescue': '\033[92m',           # Green
    'Capture': '\033[94m',          # Blue
    'Defense': '\033[95m',          # Purple
    'Survival': '\033[96m',         # Cyan
    'Interception': '\033[97m',     # White

    'Spy': '\033[97m',              # Bright White
    'Disruption': '\033[97m',       # Bright White
    'Alchemy': '\033[97m',          # Bright White
    'Assault': '\033[97m',          # Bright White
    'Corruption': '\033[97m',       # Bright White
    'Mobile Defence': '\033[97m',   # Bright White

    'Reset': '\033[0m'              # Reset code (not quite white, not quite black)
}

# API Configuration
API_URL = 'https://api.warframestat.us/pc/fissures'
REQUIRED_FISSURE_FIELDS = ['id', 'node', 'missionType', 'tier', 'expiry']

# Refresh Rates (seconds)
REFRESH_API = 60                    # How often to fetch new data from API
REFRESH_UI = 1                      # How often to update the display

# Display Formatting
SEPARATOR_LENGTH = 59
INDENT = "    "
TIER_ORDER = ['Lith', 'Meso', 'Neo', 'Axi', 'Omnia', 'Requiem']
MAX_MISSION_NAME_LENGTH = 16        # When to replace spaces with underscores
PADDING_BUFFER = 3                  # Extra padding after mission names

# ANSI Terminal Control Codes
ANSI_HIDE_CURSOR = "\033[?25l"
ANSI_SHOW_CURSOR = "\033[?25h"
ANSI_HOME = "\033[H"
ANSI_CLEAR_SCREEN = "\033[2J"
ANSI_CLEAR_BELOW = "\033[0J"
ANSI_SAVE_CURSOR = "\033[s"
ANSI_RESTORE_CURSOR = "\033[u"
