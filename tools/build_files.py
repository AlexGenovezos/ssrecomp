"""Find the linked ELF image produced by either decompilation build variant."""
from pathlib import Path


def linked_image(build_dir):
    candidates = sorted(p.name for p in Path(build_dir).iterdir()
                        if p.is_file() and p.suffix in ('.nef', '.elf'))
    if len(candidates) != 1:
        raise SystemExit(f'Expected one linked .nef or .elf in {build_dir}; found {candidates}')
    return candidates[0]
