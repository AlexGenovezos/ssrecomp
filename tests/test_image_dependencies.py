"""Changing .incbin data must refresh the linked image without changing assembly."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import recomp


@unittest.skipUnless(shutil.which('cmake') and shutil.which('ninja') and shutil.which('cc'),
                     'Needs CMake, Ninja and a native compiler')
class ImageDependencyTests(unittest.TestCase):
    def test_rebuild_embeds_changed_binary_and_preserves_unchanged_assembly(self):
        with tempfile.TemporaryDirectory(prefix='ssr image dependencies ') as directory:
            root = Path(directory)
            generated = root / 'generated'
            generated.mkdir()
            recomp.write_images(str(generated), [SimpleNamespace(image=b'\x07')])
            source = generated / 'rc_images.S'
            before = (source.read_bytes(), source.stat().st_mtime_ns)
            (root / 'main.c').write_text('''
#include <stdio.h>
extern const unsigned char rc_image_0[];
int main(void) { printf("%u\\n", rc_image_0[0]);return 0; }
''')
            # Include the same production dependency rules. Before the fix the
            # file is absent, reproducing the original untracked-incbin graph.
            helper = (ROOT / 'cmake/GeneratedImages.cmake').as_posix()
            (root / 'CMakeLists.txt').write_text(f'''
cmake_minimum_required(VERSION 3.16)
project(image_dependency C ASM)
set(SSR_GENERATED_DIR "${{CMAKE_CURRENT_SOURCE_DIR}}/generated")
if(EXISTS "{helper}")
    include("{helper}")
endif()
add_executable(embed main.c "${{SSR_GENERATED_DIR}}/rc_images.S")
target_compile_options(embed PRIVATE "$<$<COMPILE_LANGUAGE:ASM>:-Wa,-I${{SSR_GENERATED_DIR}}>")
''')
            build = root / 'build'
            def run(*args):
                process = subprocess.run(args, cwd=root, text=True, capture_output=True)
                self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
                return process.stdout
            run('cmake', '-S', str(root), '-B', str(build), '-G', 'Ninja')
            run('cmake', '--build', str(build))
            executable = build / ('embed.exe' if os.name == 'nt' else 'embed')
            self.assertEqual(run(str(executable)).strip(), '7')
            (generated / 'rc_image_0.bin').write_bytes(b'\x09')
            self.assertEqual((source.read_bytes(), source.stat().st_mtime_ns), before)
            run('cmake', '--build', str(build))
            self.assertEqual(run(str(executable)).strip(), '9')
