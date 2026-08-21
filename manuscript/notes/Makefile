NOTES := \
	aspr23_bound_audit \
	aesp_cd_l1_rppr \
	aesp_locgd_star_lower_bound \
	adaptive_revisit_control \
	hybrid_aesp_locsor \
	hybrid_local_solver_complete_note \
	hybrid_local_solver_synthesis \
	volume_gated_acceleration \
	rlsor_terminal_exact_rung \
	delayed_reflection_ladder \
	propagate_settle_framework \
	evolving_support_cg \
	incremental_active_set_sdd \
	frontier_adaptive_ladder \
	two_rung_sor \
	two_rung_direct_theory \
	response_preconditioned_hybrid \
	local_solver_oracle_hierarchy

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
