# Volume-gated acceleration research note

This directory contains a standalone LaTeX note reconstructing the project
discussion on active-volume flattening, spider obstructions, RPPR-based safe
support gates, and accelerated continuation across expanding subspaces. It is
a curated mathematical synthesis rather than a verbatim transcript.

Build from this directory with:

```bash
make
```

The note embeds its bibliography and deliberately uses note-scoped
normalizations while the repository-wide residual convention remains open.
It separately labels source results, new proofs, conditional implications,
refuted claims, and open conjectures.

The main closed statements are:

- every principal PageRank system has condition number at most `1 / alpha`,
  and a depth-`L` spider prefix has condition number
  `Theta(1 / (alpha + L^(-2)))`;
- an exact PPR core of volume `1 / tau` exists;
- fixed RPPR regularization gives support volume at most `1 / rho` and PPR
  error at most `rho`;
- signed accelerated candidates can be corrected to safe lower envelopes,
  yielding safe support admission and a one-sided KKT error certificate;
- choosing `rho = tau = epsilon / 2` proves peak working volume at most
  `2 / epsilon` and final PPR error at most `epsilon`;
- an endpoint-source path refutes the claim that support changes require only
  `O(log(1 / epsilon))` ordinary restarts uniformly in `alpha`;
- continuous restricted re-solving costs telescope to an accelerated term
  plus one discrete term per support expansion.

The graph-uniform
`O_tilde(1 / (rho * sqrt(alpha)))` work theorem remains open. Its precise
missing ingredient is a one-sided projected continuation lemma for safely
expanding subspaces, or the weaker ability to charge expansion overhead only
to newly admitted degree volume.
