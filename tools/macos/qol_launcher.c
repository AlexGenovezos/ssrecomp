// Finder/Steam entry point for the local QoL installation. Keep the ROM and
// in-game save in Games; application bundles contain only this small launcher.
#include <errno.h>
#include <fcntl.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

static void location(char *buffer, const char *home, const char *suffix) {
    int length = snprintf(buffer, PATH_MAX, "%s/%s", home, suffix);
    if (length < 0 || length >= PATH_MAX) {
        fputs("SoulSilver launcher: home directory path is too long\n", stderr);
        exit(1);
    }
}

int main(void) {
    const char *home = getenv("HOME");
    char binary[PATH_MAX], rom[PATH_MAX], save[PATH_MAX], config[PATH_MAX];
    char game_dir[PATH_MAX], log[PATH_MAX];
    if (!home || !*home) {
        fputs("SoulSilver launcher: HOME is unavailable\n", stderr);
        return 1;
    }
    location(binary, home, "Library/Application Support/ssrecomp/build-macos-arm64/ssrecomp");
    location(log, home, "Library/Application Support/ssrecomp/game.log");
    location(game_dir, home, "Games/SoulSilver Single-Screen");
    location(rom, home, "Games/SoulSilver Single-Screen/SoulSilver QoL.nds");
    location(save, home, "Games/SoulSilver Single-Screen/soulsilver.sav");
    location(config, home, "Games/SoulSilver Single-Screen/ssrecomp.cfg");
    int output = open(log, O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (output < 0) {
        perror("SoulSilver launcher log");
        return 1;
    }
    if (dup2(output, STDOUT_FILENO) < 0 || dup2(output, STDERR_FILENO) < 0) {
        perror("SoulSilver launcher logging");
        close(output);
        return 1;
    }
    if (output != STDOUT_FILENO && output != STDERR_FILENO) close(output);
    if (chdir(game_dir) < 0) {
        perror("SoulSilver game directory");
        return 1;
    }
    execl(binary, binary, rom, "--save", save, "--config", config, "--fullscreen", (char *)NULL);
    perror("SoulSilver native executable");
    return 1;
}
