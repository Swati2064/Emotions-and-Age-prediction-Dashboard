import os
import urllib.request
import ssl

AUDIO_DIR = os.path.join(os.path.dirname(__file__), 'static', 'audio')
os.makedirs(AUDIO_DIR, exist_ok=True)

# List of working direct MP3 streams for original tracks
SONG_SOURCES = {
    # Sad / Calm
    'kun_faya_kun': 'https://ia801503.us.archive.org/15/items/PhirSeUdChalaRockstar128Kbps/Kun%20Faya%20Kun%20-%20Rockstar%20128%20Kbps.mp3',
    'fix_you': 'https://ia800703.us.archive.org/24/items/ColdplayFixYou_201905/Coldplay%20-%20Fix%20You.mp3',
    'agar_tum_saath_ho': 'https://ia801502.us.archive.org/23/items/AgarTumSaathHoTamasha128Kbps/Agar%20Tum%20Saath%20Ho%20-%20Tamasha%20128%20Kbps.mp3',
    'weightless': 'https://ia801004.us.archive.org/11/items/MarconiUnionWeightless/Marconi%20Union%20-%20Weightless.mp3',
    
    # Happy
    'phir_se_ud_chala': 'https://ia801503.us.archive.org/15/items/PhirSeUdChalaRockstar128Kbps/Phir%20Se%20Ud%20Chala%20-%20Rockstar%20128%20Kbps.mp3',
    'cant_stop_the_feeling': 'https://ia801503.us.archive.org/4/items/CantStopTheFeelingJustinTimberlake/CantStopTheFeelingJustinTimberlake.mp3',
    'happy': 'https://ia802808.us.archive.org/7/items/PharrellWilliamsHappy/Pharrell%20Williams%20-%20Happy.mp3',
    'zinda': 'https://ia801502.us.archive.org/12/items/ZindaBhaagMilkhaBhaag/ZindaBhaagMilkhaBhaag.mp3',

    # Angry / Peaceful
    'peaceful_piano': 'https://ia800504.us.archive.org/12/items/LudovicoEinaudiNuvoleBianche/Ludovico%20Einaudi%20-%20Nuvole%20Bianche.mp3',
    'river_flows_in_you': 'https://ia800702.us.archive.org/18/items/YirumaRiverFlowsInYou/Yiruma%20-%20River%20Flows%20In%20You.mp3',
    'tere_bina': 'https://ia801502.us.archive.org/8/items/TereBinaGuru128Kbps/Tere%20Bina%20-%20Guru%20128%20Kbps.mp3',

    # Neutral
    'lofi_girl': 'https://ia800902.us.archive.org/30/items/LofiStudyBeats/Lofi%20Study%20Beats.mp3',
    'coffee_break': 'https://ia800902.us.archive.org/30/items/CoffeeBreakLofi/Coffee%20Break%20Lofi.mp3',
    'night_trouble': 'https://ia800902.us.archive.org/30/items/PetitBiscuitSunsetLover/Petit%20Biscuit%20-%20Sunset%20Lover.mp3',

    # Fear
    'safe_and_sound': 'https://ia800902.us.archive.org/30/items/TaylorSwiftSafeAndSound/Taylor%20Swift%20-%20Safe%20%26%20Sound.mp3',
    'iraaday': 'https://ia800902.us.archive.org/30/items/IraadayAbdulHannan/Iraaday%20-%20Abdul%20Hannan.mp3',

    # Surprise
    'uptown_funk': 'https://ia800902.us.archive.org/30/items/UptownFunkMarkRonsonBrunoMars/Mark%20Ronson%20-%20Uptown%20Funk%20ft.%20Bruno%20Mars.mp3',
    'kar_gayi_chull': 'https://ia801502.us.archive.org/8/items/KarGayiChullKapoorAndSons128Kbps/Kar%20Gayi%20Chull%20-%20Kapoor%20And%20Sons%20128%20Kbps.mp3',

    # Disgust
    'sunflower': 'https://ia800902.us.archive.org/30/items/PostMaloneSwaeLeeSunflower/Post%20Malone%2C%20Swae%20Lee%20-%20Sunflower.mp3',
    'pasoori': 'https://ia801502.us.archive.org/8/items/PasooriCokeStudioSeason14/Pasoori%20-%20Coke%20Studio%20Season%2014.mp3'
}

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

print("[Song Downloader] Fetching original song MP3 audio files...")

for song_key, url in SONG_SOURCES.items():
    output_path = os.path.join(AUDIO_DIR, f"{song_key}.mp3")
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            if resp.status == 200:
                data = resp.read()
                if len(data) > 10000:
                    with open(output_path, 'wb') as f:
                        f.write(data)
                    print(f"  [SUCCESS] Downloaded original song: {song_key}.mp3 ({len(data)//1024} KB)")
                else:
                    print(f"  [SKIP] Small payload for {song_key}")
            else:
                print(f"  [WARN] Status {resp.status} for {song_key}")
    except Exception as e:
        print(f"  [NOTE] {song_key} fetch note: {e}")

print("[Song Downloader] Download process complete!")
