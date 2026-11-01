# Single-screen QoL build

The paired game source is maintained on the `qol-mods` branch of
https://github.com/AlexGenovezos/pokeheartgold-single-screen.

This branch starts from ClickingMaster/ssrecomp main revision
`3146fb2d4d88522b12b4bf25dee74285120975e2`. Its frontend imports `main.cpp`,
`battlewide.h`, `gpucompose.h` and `merged.h` from the game fork's existing
`frontend/` at `780bf8dd458539de5a85a57799e557c2fdb41649`. These are the
single-screen composition and controller/menu changes shipped with that game
source. Retain ClickingMaster's attribution and the existing frontend license.

Generate `gen/` from the matching locally built game, then rebuild the native
executable. Do not reuse retail ROM layout metadata for modified game code.
Game binaries, generated code, local Python environments and save data stay
outside commits. Test with a copied in-game save; old memory snapshots are not
portable across code builds.

The local Mac launcher is maintained in `tools/macos/qol_launcher.c`. It keeps
the existing application/Steam shortcut and runs the paired executable from
Application Support against `~/Games/SoulSilver Single-Screen/SoulSilver QoL.nds`.
It uses the existing `soulsilver.sav` and explicitly loads the Games folder's
`ssrecomp.cfg`; output goes to Application Support's `game.log`.

The game source at `f627ef607` contains instant text, reusable TMs, unlocked
HM actions and effectiveness previews. Generation IX/Fairy rules are pending.
Validation on macOS arm64: 26 native host checks, boot (600 frames), Options
navigation (1,100 frames from frame 2,400), and battle move selection/use
(700 frames from frame 7,600) passed. Lockstep compares every ARM9 instruction
to the interpreter; reported totals after restoring a snapshot are absolute
frame numbers. Options and the single-battle move cards were visually checked.
Double-battle target menus and all late-game HM environments still require
gameplay testing. The shared HM and matchup logic have host regressions.
