My first solo project in Python.. I am not a programmer, but when I get old-er
maybe I'll be a bit more efficient :)

Anywho.

config.py contains most if not all constants for colors indents separators
update timers and such. You can highligt specific fissures and tiers by editing
the HIGHLIGHT_FISSURE and HIGHLIGHT_TIER both have to match for it to highlight
a fissure.

display_utils.py does coloring and formating.

fissure_fetcher.py has the logic for grapping fissures through warframes API
API address in config.py.

main.py logic for refreshing the display. This is done via cursor not
full-screen refresh to avoid flickering.

Not sure how you found this but since you did I hope you enjoy it.
