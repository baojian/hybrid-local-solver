# frontier_adaptive_ladder

Complete specification, with pseudocode, of the frontier agent's solver from
the August 2026 work-metered campaign (69,351,213 charged operations, 24/24
certified, audited, arena-reproduced exactly). Three ideas: the alternating
(omega, 1) eight-phase ladder ending exact; per-instance omega from a
classical prior with accuracy damping and a cross-instance memory of the
charge-weighted revisit ratio; and stacked guarded sweeps that pack up to 24
Gauss-Seidel passes into one metered call. Companion measurements show the
alternation is the ingredient that survives distillation; the adaptive
machinery is beaten 12% by a fixed two-rung schedule.

Build: `make` (latexmk).
