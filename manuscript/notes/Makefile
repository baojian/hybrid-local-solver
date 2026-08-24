NOTES := $(shell python3 tools/note_inventory.py ids --format plain)

.PHONY: all audit report targets graph clean distclean $(NOTES)

all: $(NOTES)

audit:
	uv run python tools/note_inventory.py check

report:
	uv run python tools/note_inventory.py report --format markdown

targets:
	uv run python tools/note_inventory.py targets --format markdown

graph:
	uv run python tools/note_inventory.py graph --format mermaid

$(NOTES):
	$(MAKE) -C $@

clean:
	@set -e; for note in $(NOTES); do $(MAKE) -C $$note clean; done

distclean:
	@set -e; for note in $(NOTES); do $(MAKE) -C $$note distclean; done
