url = 'https://www.marathonbet.ru/su/betting/Football/Clubs.+International/UEFA+Champions+League/Play-Offs/Quarter+Final/1st+Leg/Arsenal+vs+Bayern+Munich+-+18236227'

link_array = str(url).split("+")
uniq_game_code = link_array[-1]
id_to_find = 'shortcutLink_event' + uniq_game_code + 'type3'
print(id_to_find)
print('shortcutLink_event18236227type3')