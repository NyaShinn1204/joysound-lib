import jysdlib

search_result = jysdlib.search_song("勇者", "YOASOBI", show_count=1, show_debug=False)
jysdlib.get_lyric(search_result[0])