"""
Emotion-Based Music Recommendation Engine for EmotionAI Dashboard
Provides local Flask audio streams for guaranteed in-app speaker sound playback, plus Spotify & YouTube links.
"""

MUSIC_CATALOG = {
    'happy': [
        {
            'id': 'h1',
            'title': 'Phir Se Ud Chala',
            'artist': 'Mohit Chauhan (Rockstar)',
            'genre': 'Bollywood Motivational',
            'spotify_url': 'https://open.spotify.com/track/1S1wD8q0vJq6Q9z4',
            'youtube_url': 'https://www.youtube.com/watch?v=2mWaqBmupvE',
            'audio_url': '/static/audio/happy.wav',
            'spotify_embed': 'https://open.spotify.com/embed/track/1S1wD8q0vJq6Q9z4?utm_source=generator',
            'badge': 'Bollywood Energy'
        },
        {
            'id': 'h2',
            'title': "Can't Stop the Feeling!",
            'artist': 'Justin Timberlake',
            'genre': 'Happy English Pop',
            'spotify_url': 'https://open.spotify.com/track/6RUKvYjG3jU2B6Z6',
            'youtube_url': 'https://www.youtube.com/watch?v=ru0K8uYEZWw',
            'audio_url': '/static/audio/happy.wav',
            'spotify_embed': 'https://open.spotify.com/embed/track/6RUKvYjG3jU2B6Z6?utm_source=generator',
            'badge': 'Global Hit'
        },
        {
            'id': 'h3',
            'title': 'Zinda (Bhaag Milkha Bhaag)',
            'artist': 'Siddharth Mahadevan',
            'genre': 'Bollywood Motivational',
            'spotify_url': 'https://open.spotify.com/track/2ZlQnF24W2pY80w1',
            'youtube_url': 'https://www.youtube.com/watch?v=8Vz_2wt28UQ',
            'audio_url': '/static/audio/happy.wav',
            'spotify_embed': 'https://open.spotify.com/embed/track/2ZlQnF24W2pY80w1?utm_source=generator',
            'badge': 'Motivation Boost'
        },
        {
            'id': 'h4',
            'title': 'Happy',
            'artist': 'Pharrell Williams',
            'genre': 'Feel Good Pop',
            'spotify_url': 'https://open.spotify.com/track/60nZcImufyMA1Z8',
            'youtube_url': 'https://www.youtube.com/watch?v=ZbZSe6N_BXs',
            'audio_url': '/static/audio/happy.wav',
            'spotify_embed': 'https://open.spotify.com/embed/track/60nZcImufyMA1Z8?utm_source=generator',
            'badge': 'Feel Good'
        }
    ],

    'sad': [
        {
            'id': 's1',
            'title': 'Kun Faya Kun',
            'artist': 'A.R. Rahman, Javed Ali, Mohit Chauhan',
            'genre': 'Calm & Spiritual',
            'spotify_url': 'https://open.spotify.com/track/7f3K9zP',
            'youtube_url': 'https://www.youtube.com/watch?v=T94PHkuydcw',
            'audio_url': '/static/audio/sad.wav',
            'spotify_embed': 'https://open.spotify.com/embed/track/7f3K9zP?utm_source=generator',
            'badge': 'Soul Soothing'
        },
        {
            'id': 's2',
            'title': 'Fix You',
            'artist': 'Coldplay',
            'genre': 'Relaxing Rock/Alternative',
            'spotify_url': 'https://open.spotify.com/track/7lPN2wws',
            'youtube_url': 'https://www.youtube.com/watch?v=k4V3Mo61fJM',
            'audio_url': '/static/audio/sad.wav',
            'spotify_embed': 'https://open.spotify.com/embed/track/7lPN2wws?utm_source=generator',
            'badge': 'Emotional Healing'
        },
        {
            'id': 's3',
            'title': 'Agar Tum Saath Ho',
            'artist': 'Arijit Singh, Alka Yagnik',
            'genre': 'Melodic Calm',
            'spotify_url': 'https://open.spotify.com/track/3yH4x0v',
            'youtube_url': 'https://www.youtube.com/watch?v=sK7riqg254H',
            'audio_url': '/static/audio/sad.wav',
            'spotify_embed': 'https://open.spotify.com/embed/track/3yH4x0v?utm_source=generator',
            'badge': 'Acoustic Comfort'
        },
        {
            'id': 's4',
            'title': 'Weightless',
            'artist': 'Marconi Union',
            'genre': 'Ambient Relaxation',
            'spotify_url': 'https://open.spotify.com/track/6kkwzN',
            'youtube_url': 'https://www.youtube.com/watch?v=UfcAVejslrU',
            'audio_url': '/static/audio/sad.wav',
            'spotify_embed': 'https://open.spotify.com/embed/track/6kkwzN?utm_source=generator',
            'badge': 'Deep Relaxation'
        }
    ],

    'angry': [
        {
            'id': 'a1',
            'title': 'Peaceful Piano Chill',
            'artist': 'Ludovico Einaudi',
            'genre': 'Peaceful Ambient Instrumental',
            'spotify_url': 'https://open.spotify.com/track/1L8V6W',
            'youtube_url': 'https://www.youtube.com/watch?v=9Q6u2W5Qd3E',
            'audio_url': '/static/audio/angry.wav',
            'spotify_embed': 'https://open.spotify.com/embed/track/1L8V6W?utm_source=generator',
            'badge': 'Mind Calming'
        },
        {
            'id': 'a2',
            'title': 'River Flows In You',
            'artist': 'Yiruma',
            'genre': 'Peaceful Classical',
            'spotify_url': 'https://open.spotify.com/track/62r4x0',
            'youtube_url': 'https://www.youtube.com/watch?v=7maJOI3QMu0',
            'audio_url': '/static/audio/angry.wav',
            'spotify_embed': 'https://open.spotify.com/embed/track/62r4x0?utm_source=generator',
            'badge': 'Peaceful Stream'
        },
        {
            'id': 'a3',
            'title': 'Tere Bina (Guru)',
            'artist': 'A.R. Rahman',
            'genre': 'Peaceful Indian Acoustic',
            'spotify_url': 'https://open.spotify.com/track/2yN5x9',
            'youtube_url': 'https://www.youtube.com/watch?v=5Vz1y48H',
            'audio_url': '/static/audio/angry.wav',
            'spotify_embed': 'https://open.spotify.com/embed/track/2yN5x9?utm_source=generator',
            'badge': 'Serene Harmonies'
        }
    ],

    'neutral': [
        {
            'id': 'n1',
            'title': 'Lofi Hip Hop Radio - Beats to Relax/Study to',
            'artist': 'Lofi Girl',
            'genre': 'Lo-Fi Chill Beats',
            'spotify_url': 'https://open.spotify.com/playlist/0vvR1w',
            'youtube_url': 'https://www.youtube.com/watch?v=jfKfPfyJRdk',
            'audio_url': '/static/audio/neutral.wav',
            'spotify_embed': 'https://open.spotify.com/embed/playlist/0vvR1w?utm_source=generator',
            'badge': 'Lo-Fi Chill'
        },
        {
            'id': 'n2',
            'title': 'Coffee Break Lofi',
            'artist': 'Chillhop Music',
            'genre': 'Ambient Lo-Fi',
            'spotify_url': 'https://open.spotify.com/track/3kX91z',
            'youtube_url': 'https://www.youtube.com/watch?v=5qap5aO4i9A',
            'audio_url': '/static/audio/neutral.wav',
            'spotify_embed': 'https://open.spotify.com/embed/track/3kX91z?utm_source=generator',
            'badge': 'Work Focus'
        },
        {
            'id': 'n3',
            'title': 'Night Trouble',
            'artist': 'Petit Biscuit',
            'genre': 'Chill Electronic',
            'spotify_url': 'https://open.spotify.com/track/0wK8xL',
            'youtube_url': 'https://www.youtube.com/watch?v=13F1c7kXv-E',
            'audio_url': '/static/audio/neutral.wav',
            'spotify_embed': 'https://open.spotify.com/embed/track/0wK8xL?utm_source=generator',
            'badge': 'Chill Vibe'
        }
    ],

    'fear': [
        {
            'id': 'f1',
            'title': 'Safe & Sound',
            'artist': 'Taylor Swift ft. The Civil Wars',
            'genre': 'Relaxing Folk Acoustic',
            'spotify_url': 'https://open.spotify.com/track/0P5W2',
            'youtube_url': 'https://www.youtube.com/watch?v=RzhAS_Vx1',
            'audio_url': '/static/audio/fear.wav',
            'spotify_embed': 'https://open.spotify.com/embed/track/0P5W2?utm_source=generator',
            'badge': 'Comforting'
        },
        {
            'id': 'f2',
            'title': 'Iraaday',
            'artist': 'Abdul Hannan, Rakan',
            'genre': 'Soothing Indie Acoustic',
            'spotify_url': 'https://open.spotify.com/track/4X9zP1',
            'youtube_url': 'https://www.youtube.com/watch?v=papuvlVeZg8',
            'audio_url': '/static/audio/fear.wav',
            'spotify_embed': 'https://open.spotify.com/embed/track/4X9zP1?utm_source=generator',
            'badge': 'Soft Comfort'
        }
    ],

    'surprise': [
        {
            'id': 'su1',
            'title': 'Uptown Funk',
            'artist': 'Mark Ronson ft. Bruno Mars',
            'genre': 'Upbeat Dance Funk',
            'spotify_url': 'https://open.spotify.com/track/32OlwWu',
            'youtube_url': 'https://www.youtube.com/watch?v=OPf0YbXqDm0',
            'audio_url': '/static/audio/surprise.wav',
            'spotify_embed': 'https://open.spotify.com/embed/track/32OlwWu?utm_source=generator',
            'badge': 'Upbeat Grooves'
        },
        {
            'id': 'su2',
            'title': 'Kar Gayi Chull',
            'artist': 'Badshah, Neha Kakkar',
            'genre': 'Upbeat Bollywood Party',
            'spotify_url': 'https://open.spotify.com/track/4kX91z',
            'youtube_url': 'https://www.youtube.com/watch?v=N_KpjLhJa1k',
            'audio_url': '/static/audio/surprise.wav',
            'spotify_embed': 'https://open.spotify.com/embed/track/4kX91z?utm_source=generator',
            'badge': 'Party Energy'
        }
    ],

    'disgust': [
        {
            'id': 'd1',
            'title': 'Sunflower',
            'artist': 'Post Malone & Swae Lee',
            'genre': 'Chill Refreshing Vibe',
            'spotify_url': 'https://open.spotify.com/track/3K4x0v',
            'youtube_url': 'https://www.youtube.com/watch?v=ApXoWvfEYVU',
            'audio_url': '/static/audio/disgust.wav',
            'spotify_embed': 'https://open.spotify.com/embed/track/3K4x0v?utm_source=generator',
            'badge': 'Chill Reset'
        },
        {
            'id': 'd2',
            'title': 'Pasoori',
            'artist': 'Ali Sethi & Shae Gill',
            'genre': 'Melodic Fusion',
            'spotify_url': 'https://open.spotify.com/track/1X8vW',
            'youtube_url': 'https://www.youtube.com/watch?v=5Eqb_-j3FDA',
            'audio_url': '/static/audio/disgust.wav',
            'spotify_embed': 'https://open.spotify.com/embed/track/1X8vW?utm_source=generator',
            'badge': 'Fresh Fusion'
        }
    ]
}


def get_recommendations(emotion):
    """
    Fetch recommended music list for the given emotion tag.
    Defaults to 'neutral' if emotion is unknown.
    """
    emotion_key = str(emotion).lower().strip()
    tracks = MUSIC_CATALOG.get(emotion_key, MUSIC_CATALOG['neutral'])
    return tracks
