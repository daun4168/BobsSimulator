import re

# Line Regex
TIMESTAMP_RE_TEXT = r'D (?P<hour>\d{2}):(?P<min>\d{2}):(?P<sec>\d{2})\.\d{7} '
GAME_STATE_DEBUG_PRINT_POWER_RE = re.compile(TIMESTAMP_RE_TEXT + r'GameState\.DebugPrintPower\(\) - (?P<context>.*)')
GAME_STATE_DEBUG_PRINT_POWER_LIST_RE = re.compile(TIMESTAMP_RE_TEXT + r'GameState\.DebugPrintPowerList\(\) - (?P<context>.*)')
GAME_STATE_DEBUG_PRINT_GAME_RE = re.compile(TIMESTAMP_RE_TEXT + r'GameState\.DebugPrintGame\(\) - (?P<context>.*)')
POWER_TASK_LIST_DEBUG_DUMP_RE = re.compile(TIMESTAMP_RE_TEXT + r'PowerTaskList\.DebugDump\(\) - (?P<context>.*)')
POWER_TASK_LIST_DEBUG_PRINT_POWER_RE = re.compile(TIMESTAMP_RE_TEXT + r'PowerTaskList\.DebugPrintPower\(\) - (?P<context>.*)')
POWER_PROCESSOR_PREPARE_HISTORY_FOR_CURRENT_TASK_LIST_RE = re.compile(TIMESTAMP_RE_TEXT + r'PowerProcessor\.PrepareHistoryForCurrentTaskList\(\) - (?P<context>.*)')
POWER_PROCESSOR_END_CURRENT_TASK_LIST_RE = re.compile(TIMESTAMP_RE_TEXT + r'PowerProcessor\.EndCurrentTaskList\(\) - (?P<context>.*)')
POWER_PROCESSOR_DO_TASK_LIST_FOR_CARD_TASK_LIST_RE = re.compile(TIMESTAMP_RE_TEXT + r'PowerProcessor\.DoTaskListForCard\(\) - (?P<context>.*)')
GAME_STATE_DEBUG_PRINT_OPTIONS_RE = re.compile(TIMESTAMP_RE_TEXT + r'GameState\.DebugPrintOptions\(\) - (?P<context>.*)')
GAME_STATE_SEND_OPTION_RE = re.compile(TIMESTAMP_RE_TEXT + r'GameState\.SendOption\(\) - (?P<context>.*)')
GAME_STATE_DEBUG_PRINT_ENTITY_CHOICES_RE = re.compile(TIMESTAMP_RE_TEXT + r'GameState\.DebugPrintEntityChoices\(\) - (?P<context>.*)')
GAME_STATE_DEBUG_PRINT_ENTITY_CHOSEN_RE = re.compile(TIMESTAMP_RE_TEXT + r'GameState\.DebugPrintEntitiesChosen\(\) - (?P<context>.*)')
GAME_STATE_SEND_CHOICES_RE = re.compile(TIMESTAMP_RE_TEXT + r'GameState\.SendChoices\(\) - (?P<context>.*)')
TRIGGER_SPELL_CONTROLLER_RE = re.compile(TIMESTAMP_RE_TEXT + r'TriggerSpellController .* - (?P<context>.*)')
POWER_SPELL_CONTROLLER_RE = re.compile(TIMESTAMP_RE_TEXT + r'PowerSpellController .* - (?P<context>.*)')
CHOICE_CARD_MGR_HIDE_RE = re.compile(TIMESTAMP_RE_TEXT + r'ChoiceCardMgr\.WaitThenHideChoicesFromPacket\(\) - (?P<context>.*)')
CHOICE_CARD_MGR_SHOW_RE = re.compile(TIMESTAMP_RE_TEXT + r'ChoiceCardMgr\.WaitThenShowChoices\(\) - (?P<context>.*)')

# Debug Print Game Regex
BUILD_NUMBER_RE = re.compile(r'BuildNumber=(?P<BuildNumber>\d+)')
GAME_TYPE_RE = re.compile(r'GameType=(?P<GameType>\w+)')
FORMAT_TYPE_RE = re.compile(r'FormatType=(?P<FormatType>\w+)')
SCENARIO_ID_RE = re.compile(r'ScenarioID=(?P<ScenarioID>\d+)')
PLAYER_ID_NAME_RE = re.compile(r'PlayerID=(?P<PlayerID>\d+), PlayerName=(?P<PlayerName>\S+)')

# Entity Regex
ENTITY_DESCRIPTION_RE_TEXT = r'\[entityName=.+ id=(?P<id>\d+) zone=(?P<zone>\w+) zonePos=(?P<zonePos>\d+) cardId=(?P<cardId>\w+) player=(?P<player>\d+)\]'
ENTITY_DESCRIPTION_RE = re.compile(r'\[entityName=.+ id=(?P<id>\d+) zone=(?P<zone>\w+) zonePos=(?P<zonePos>\d+) cardId=(?P<cardId>\w*) player=(?P<player>\d+)\]')

CREATE_GAME_ENTITY_RE = re.compile(r'CREATE_GAME')
GAME_ENTITY_RE = re.compile(r'GameEntity EntityID=(?P<EntityID>\d+)')
PLAYER_ENTITY_RE = re.compile(r'Player EntityID=(?P<EntityID>\d+) PlayerID=(?P<PlayerID>\d+) GameAccountId=\[hi=(?P<hi>\d+) lo=(?P<lo>\d+)\]')
BLOCK_START_ENTITY_RE = re.compile(r'BLOCK_START BlockType=(?P<BlockType>\w+) Entity=(?P<Entity>.+) EffectCardId=(?P<EffectCardId>\w*) EffectIndex=(?P<EffectIndex>[0-9-]*) Target=(?P<Target>.*) SubOption=(?P<SubOption>[0-9-]*).*')
BLOCK_END_ENTITY_RE = re.compile(r'BLOCK_END')
FULL_ENTITY_CREATING_RE = re.compile(r'FULL_ENTITY - Creating ID=(?P<ID>\d+) CardID=(?P<CardID>\w*)')
TAG_CHANGE_RE = re.compile(rf'TAG_CHANGE Entity=(?P<Entity>.+) tag=(?P<tag>\w+) value=(?P<value>\w+)')
SHOW_ENTITY_RE = re.compile(r'SHOW_ENTITY - Updating Entity=(?P<Entity>.+) CardID=(?P<CardID>\w*)')
HIDE_ENTITY_RE = re.compile(r'HIDE_ENTITY - Entity=(?P<Entity>.+) tag=(?P<tag>\w+) value=(?P<value>\w+)')
META_DATA_RE = re.compile(r'META_DATA .*')
CHANGE_ENTITY_RE = re.compile(r'CHANGE_ENTITY - Updating Entity=(?P<Entity>.+) CardID=(?P<CardID>\w*)')
SUB_SPELL_START_RE = re.compile(r'SUB_SPELL_START .*')
SUB_SPELL_END_RE = re.compile(r'SUB_SPELL_END')

TAG_VALUE_RE = re.compile(r'tag=(?P<tag>\w+) value=(?P<value>\w+)')
INFO_RE = re.compile(rf'Info\[(?P<num>\d+)\] = (\d+|{ENTITY_DESCRIPTION_RE_TEXT}|.+)')
TARGETS_RE = re.compile(rf'Targets\[(?P<num>\d+)\] = (\d+|{ENTITY_DESCRIPTION_RE_TEXT})')
SOURCE_RE = re.compile(rf'Source = {ENTITY_DESCRIPTION_RE_TEXT}')
