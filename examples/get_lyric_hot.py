import jysdlib

top_rank = jysdlib.get_daily_ranking(top_rank=True, show_debug=False)
jysdlib.get_lyric(top_rank["naviGroupId"])