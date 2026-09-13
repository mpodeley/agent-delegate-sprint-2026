# Resources

Status: corrected 2026-09-13 (Agustín). The 2026-09-12 version of this note inferred logistics that were wrong: it called the model runs post-hackathon, left the H100 provider open and treated frontier API agents as an open question. The facts below come from the team; anything not confirmed is marked open.

## Compute

- **H100s: Mateo's.** They come from his workplace, for personal side projects, and he runs the jobs himself. Model runs happen **during the sprint**, in the remaining day and a half, not afterwards. The figure in circulation on 2026-09-12 was more than ten hours; the exact allocation for today is Mateo's to state.
- **Inference endpoint used so far.** Every Kimi K3 run in `results/kimi-delegate-ctf/` went through an OpenAI-compatible server Mateo operates on a private Tailscale (`.ts.net`) address, with per-person credentials (`experiments/kimi-delegate-ctf/README.md`). Pulling the branch does not grant access; a teammate needs Docker, `uv`, the host address and their own key. Reported token usage varies: working traces used 9,921–24,726 tokens; several 150k-limit runs overshot that limit at the final response, and the 2M baseline reported 2,006,825 tokens. Later bridge contact occurred below 150k. These are usage counts, not monetary costs; see [kimi-runs-log.md](kimi-runs-log.md).
- **Strix Halo (Matías).** Ryzen AI Max+ 395, 96 GB unified memory, llama.cpp with HIP. Every run in the paper happened there (Qwen3-4B, Gemma-3-4B, their abliterated derivatives, Qwen3.8-27B; provenance in `data/`). Fine for developing prompts and fixtures; not where the pilot runs.
- **Model scope: open-weight only.** The study is defined over open-weight models because that is what the team can run freely and reproduce. Testing the same design on frontier API models is a plausible extension, not part of the study. This closes the "external API model" question in `CLAUDE.md` for this experiment: Kimi K3 on Mateo's server is in scope.

## People

- Matías Podeley: project lead and experimental design; repo owner; the paper and the submission.
- Agustín Brusco: evaluation design, taxonomy, analysis, the notes on this branch.
- Mateo Zárate: the Control Tower environments and scenarios, the Kimi runs, the H100s.

## Time

Deadline 2026-09-13 23:59 AoE (2026-09-14 08:59 in Buenos Aires). The honeypot mini-pilot ([honeypot-pilot.md](honeypot-pilot.md)) is runnable now and is meant to run today on Mateo's machine. Whether its numbers enter the submission is Matías's call. Whatever is not finished by the deadline continues as the follow-up sketched in `docs/research-program.md`.

## Open

- Hours and concurrency Mateo can commit today, and therefore how many epochs per cell the pilot gets (the script defaults to five per cell, four cells).
- A second open-weight model family for the held-out run (`docs/help-seeking-eval-design.md` asks for at least two). Not needed for today's pilot.
