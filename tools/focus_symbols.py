"""Resolve frontend probes against either supported game-source naming scheme."""

ALIASES = {
    # Game history ad7307e15, b89ab4d7b and f33668cdb (start_menu.c).
    'sub_0203D264': 'Task_StartMenu_WaitSaveAppOpen',
    'sub_0203D288': 'Task_StartMenu_WaitSaveAppClose',
    'sub_0203D2CC': 'StartMenu_SelectUnionChatLog',
    'sub_0203D2EC': 'StartMenu_State19_Advance',
    'sub_0203D304': 'StartMenu_State20_Close',
    # Game history 33b55d7b7 and e2935a47f (touch choice/mart tasks).
    'ov27_0225C434': 'TouchscreenChoiceMenu_Task',
    'ov31_0225D7A0': 'TouchMartApp_RunTask',
}


def find_focus(functions, name):
    for candidate in (name, ALIASES.get(name)):
        if candidate is None:
            continue
        found = [(name, sec, addr) for sec, addr, size, actual in functions if actual == candidate]
        if found:
            return found
    return []
