import requests
from datetime import datetime, timezone
import time
import sys

# === NEW CONSTANT ===
NOTIFY_MISSIONS = {'Defense', 'Rescue', 'Extermination', 'Capture'} #valid Defense, Survival, Extermination, Rescue, Capture
NOTIFY_TIERS = {'Axi'} #valid Lith, Meso, Neo, Axi
# Existing constants...
TIER_ICONS = {'Lith': '🪨', 'Meso': '🟡', 'Neo': '🔵', 'Axi': '💠', 'Omnia': '✨'}
COLORS = {
    'Defense': '\033[95m',    # Pink
    'Survival': '\033[94m',   # Purple
    'Extermination': '\033[96m', # Teal
    'Rescue': '\033[93m',     # Yellow
    'Reset': '\033[0m'
}

# === NEW GLOBAL ===
notified_fissures = set()  # Track fissure IDs we've notified

def fetch_fissures():
    try:
        response = requests.get("https://api.warframestat.us/pc/fissures", timeout=5)
        response.raise_for_status()
        fissures = response.json()
        validated = []
        for f in fissures:
            if f.get('isStorm', False):
                continue
            if not all(k in f for k in ['id', 'node','missionType','tier','expiry']):  # Added 'id'
                continue
            try:
                expiry = datetime.fromisoformat(f['expiry'].replace('Z', '+00:00'))
                validated.append((f, expiry, f.get('isHard', False)))
            except ValueError:
                continue
        return validated, None
    except Exception as e:
        return None, f"Error: {str(e)}"

def color_mission(mission_type):
    raw = mission_type
    if 'Defense' in raw and 'Mobile' not in raw:
        return f"{COLORS['Defense']}{raw}{COLORS['Reset']}", len(raw)
    elif 'Survival' in raw:
        return f"{COLORS['Survival']}{raw}{COLORS['Reset']}", len(raw)
    elif 'Extermination' in raw:
        return f"{COLORS['Extermination']}{raw}{COLORS['Reset']}", len(raw)
    elif 'Rescue' in raw:
        return f"{COLORS['Rescue']}{raw}{COLORS['Reset']}", len(raw)
    return raw, len(raw)

def beep_notification():
    """Cross-platform terminal beep sequence"""
    try:
        for _ in range(10):
            print('\a', end='', flush=True)  # System bell character
            time.sleep(0.8)
    except Exception:
        pass


def main():
    global notified_fissures
    
    try:
        while True:
            print("🔄 Fetching fissures...", end='\r', flush=True)  # Loading indicator
            fissures, error = fetch_fissures()
            
            if error:
                print(f"⚠️ {error}\nRetrying in 10s...")
                time.sleep(10)
                continue
            print("\033c", end='')

            # === NOTIFICATION HANDLING ===
            current_fissure_ids = {f[0]['id'] for f in fissures}
            new_fissures = []
        
            for f, expiry, is_steel in fissures:
                fissure_id = f['id']
                if fissure_id not in notified_fissures:
                    mission_ok = f['missionType'] in NOTIFY_MISSIONS
                    tier_ok = f['tier'] in NOTIFY_TIERS
                
                    if mission_ok and tier_ok:
                        new_fissures.append(f)
                        notified_fissures.add(fissure_id)
        
            if new_fissures:
                print("\n🔔 NEW MATCHING FISSURES:")
                for nf in new_fissures:
                    print(f"  {nf['tier']} {nf['missionType']} @ {nf['node']}")
                beep_notification()
            # === END NOTIFICATION LOGIC ===
            
            print("🔥 VOID FISSURE TRACKER 🔥")
            current_time = datetime.now(timezone.utc)
            
            for tier, icon in TIER_ICONS.items():
                tier_fissures = []
                for f, expiry, is_steel in fissures:
                    rem = expiry - current_time
                    if rem.total_seconds() <= 0:
                        continue
                    if f.get('tier') == tier:
                        tier_fissures.append((f['node'], f['missionType'], rem, is_steel))
                
                if not tier_fissures:
                    continue
                    
                print(f"\n{icon} {tier.upper()} FISSURES:")
                for node, mission, rem, is_steel in tier_fissures:
                    clean_node = node[:28] + '..' if len(node) > 30 else node
                    
                    total_seconds = int(rem.total_seconds())
                    hours, remainder = divmod(total_seconds, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    time_str = f"{hours}:{minutes:02}:{seconds:02}"
                    
                    colored_mission, raw_len = color_mission(mission)
                    padding_needed = max(0, 20 - raw_len)
                    steel_note = " ⚔️" if is_steel else ""
                    
                    print(f"  {clean_node.ljust(30)} : {colored_mission}{' ' * padding_needed} ⌛ {time_str}{steel_note}")# ... (rest of display logic unchanged) ...

            print("\n🔄 \033[95m Refreshing, like every now and then...")
            time.sleep(3)

    except KeyboardInterrupt:
        print("\n👋 Exiting tracker...")
        sys.exit(0)

if __name__ == "__main__":
    main()
