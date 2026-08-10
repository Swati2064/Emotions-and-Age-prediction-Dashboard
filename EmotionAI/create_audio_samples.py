import os
import wave
import math
import struct

AUDIO_DIR = os.path.join(os.path.dirname(__file__), 'static', 'audio')
os.makedirs(AUDIO_DIR, exist_ok=True)

def generate_tone_wav(filename, notes, duration=15.0, sample_rate=22050):
    """
    Generate pleasant harmonic audio WAV file for emotion playback.
    """
    filepath = os.path.join(AUDIO_DIR, filename)
    num_samples = int(duration * sample_rate)
    
    with wave.open(filepath, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        
        raw_data = bytearray()
        for i in range(num_samples):
            t = i / sample_rate
            sample_val = 0.0
            
            # Combine harmonic note frequencies with gentle envelope
            envelope = min(1.0, t * 2.0) * max(0.0, 1.0 - (t / duration) ** 2)
            
            for freq, amp in notes:
                # Add slight vibrato/tremolo for pleasant acoustic feel
                tremolo = 1.0 + 0.15 * math.sin(2 * math.pi * 3.0 * t)
                sample_val += amp * math.sin(2 * math.pi * freq * t) * tremolo
                
            sample_val = max(-1.0, min(1.0, sample_val * envelope * 0.4))
            packed_val = struct.pack('<h', int(sample_val * 32767))
            raw_data.extend(packed_val)
            
        wav_file.writeframes(raw_data)
    print(f"[Audio Generator] Created {filename} ({duration}s)")

# Note Frequencies (Hz)
C4, D4, E4, F4, G4, A4, B4 = 261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88
C5, E5, G5, A5 = 523.25, 659.25, 783.99, 880.00

# 1. Happy: Upbeat C-Major / G-Major triad
generate_tone_wav('happy.wav', [(C4, 0.4), (E4, 0.3), (G4, 0.3), (C5, 0.2)], duration=12.0)

# 2. Sad: Calm A-Minor triad
generate_tone_wav('sad.wav', [(A4 / 2, 0.5), (C4, 0.3), (E4, 0.3)], duration=12.0)

# 3. Angry: Peaceful F-Major soothing ambient
generate_tone_wav('angry.wav', [(F4 / 2, 0.5), (A4, 0.3), (C5, 0.3)], duration=12.0)

# 4. Neutral: Lo-Fi Chill Synth tone (D-Minor7)
generate_tone_wav('neutral.wav', [(D4, 0.4), (F4, 0.3), (A4, 0.3), (C5, 0.2)], duration=12.0)

# 5. Fear: Soothing G-Major acoustic
generate_tone_wav('fear.wav', [(G4 / 2, 0.5), (B4 / 2, 0.3), (D4, 0.3)], duration=12.0)

# 6. Surprise: Upbeat C-Major Fanfare
generate_tone_wav('surprise.wav', [(C4, 0.3), (E4, 0.3), (G4, 0.3), (E5, 0.3)], duration=12.0)

# 7. Disgust: Soft E-Minor Chill
generate_tone_wav('disgust.wav', [(E4 / 2, 0.5), (G4, 0.3), (B4, 0.3)], duration=12.0)
