NOTES := \
	aesp_cd_l1_rppr \
	aesp_locgd_star_lower_bound \
	hybrid_aesp_locsor \
	hybrid_local_solver_complete_note \
	hybrid_local_solver_synthesis \
	volume_gated_acceleration

.PHONY: all clean distclean $(NOTES)

all: $(NOTES)

$(NOTES):
	$(MAKE) -C $@

clean:
	@set -e; for note in $(NOTES); do $(MAKE) -C $$note clean; done

distclean:
	@set -e; for note in $(NOTES); do $(MAKE) -C $$note distclean; done
