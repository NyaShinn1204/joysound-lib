import requests
import json
import re

def set_data(name: str = None, songid: int = None):
    payload1 = {
        "kind1": "compound",
        "word1": name,
        "match1": "partial",
        "kindCnt": "1",
        "format": "group",
        "start": "1",
        "count": "5",
        "sort": "popular",
        "order": "desc",
        "apiVer": "1.0",
    }
    payload2 = {
        "kind": "naviGroupId",
        "selSongNo": songid,
        "interactionFlg": "0",
        "apiVer": "1.0",
    }
    header = {
        "Accept":"*application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ja;q=0.7",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Origin": "https://www.joysound.com",
        "Referer": "https://www.joysound.com/",
        "Sec-Ch-Ua": "'Brave';v='123', 'Not(A:Brand';v='8', 'Chromium';v='123'",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "'Windows'",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Gpc": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "X-Jsp-App-Name": "0000800"
    }
    return header, payload1, payload2

def search_song(song_name: str, artist: str = None, show_count: int = None, all_hit: bool = False, include_sabikara: bool = False, show_debug: bool = False):
    """
    
    曲を検索します

    ※ デフォルトの表示数は5です
    
    ※ 変更可能です
    
    ※ 推奨されませんがすべて表示することも可能です
    

    #### Useage

        >>> import jysdlib
        ※ アーティストを指定する場合
        >>> jysdlib.search_song("勇者", "YOASOBI")
        ※ アーティストを指定しない場合
        >>> jysdlib.search_song("勇者")
        ※ 表示数を変更する場合
        >>> jysdlib.search_song("勇者", show_count=15)
        ※ すべて表示する場合
        >>> jysdlib.search_song("勇者", all_hit=True)
        ※ [サビカラ]を含める場合
        >>> jysdlib.search_song("勇者", include_sabikara=True)
        ※ [サビカラ]を含めない場合
        >>> jysdlib.search_song("勇者", include_sabikara=False)
    """
    
    songs = []
    
    if include_sabikara == False:
        removed_sabikara_count = 0
    else:
        removed_sabikara_count = None
    
    header = set_data()[0]
    get_hitcount = requests.post("https://mspxy.joysound.com/Common/ContentsList", data=set_data(name=song_name)[1], headers=header)
    hitcount = get_hitcount.json()["contentsHitCount"]
    
    payload = set_data(song_name)[1]
    if all_hit == True:
        payload["count"] = hitcount        
    elif all_hit == False and (show_count != None and show_count != 5):
        payload["count"] = show_count
    
    res = requests.post("https://mspxy.joysound.com/Common/ContentsList", data=payload, headers=header)
    for artist_data in res.json()["contentsList"]:
        if artist != None:
            if re.search(rf'{artist}', artist_data.get('artistName', ''), re.IGNORECASE) and re.search(rf'{song_name}', artist_data.get('songName', ''), re.IGNORECASE):
                if not include_sabikara and re.search(r'\[サビカラ\]', artist_data.get('songName', ''), re.IGNORECASE):
                    removed_sabikara_count += 1
                else:
                    get_data = json.dumps(artist_data, indent=4, ensure_ascii=False)
                    if show_debug:
                        print(json.loads(get_data)["songName"])
                songs.append(json.loads(get_data)["naviGroupId"])
            
        else:    
            if re.search(rf'{song_name}', artist_data.get('songName', ''), re.IGNORECASE):
                if not include_sabikara and re.search(r'\[サビカラ\]', artist_data.get('songName', ''), re.IGNORECASE):
                    removed_sabikara_count += 1
                else:
                    get_data = json.dumps(artist_data, indent=4, ensure_ascii=False)
                    if show_debug:
                        print(json.loads(get_data)["songName"])
                songs.append(json.loads(get_data)["naviGroupId"])
    if include_sabikara == False and show_debug:
        print("[サビカラ] を", removed_sabikara_count,"個削除しました")
    return songs
        
def get_lyric(songid: int):
    """
    
    曲の歌詞を取得します

    #### Useage

        >>> import jysdlib
        >>> jysdlib.get_lyric(songid=990758)
        ※ song_idは、省いてもﾖｼ
    """
    
    header = set_data()[0]
    res = requests.post("https://mspxy.joysound.com/Common/Lyric", data=set_data(songid=songid)[2], headers=header)
    for lyric_data in res.json()["lyricList"]:
        print(lyric_data["lyric"])
        
def get_daily_ranking(top_rank: bool = False, show_debug: bool = False):
    """
    
    デイリーランキングを取得します
    100件から変更は不可能です

    #### Useage

        >>> import jysdlib
        >>> jysdlib.get_daily_ranking()
        ※ トップだけを返すようにする場合
        >>> jysdlib.get_daily_ranking(top_rank=True)
    """

    daily_rank = []
    
    header = set_data()[0]
    res = requests.get("https://www.joysound.com/web/feature/karaoke/ranking/contents/all_daily.json", headers=header)
    for hot_data in res.json()["genreRankingList"]:
        if show_debug:
            print(hot_data["songName"])
        daily_rank.append(hot_data)
    if top_rank:
        return res.json()["genreRankingList"][0]
    return daily_rank