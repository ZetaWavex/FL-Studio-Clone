import numpy as np
import wave
import struct
import os
from typing import List, Dict, Optional

class AudioProcessor:
    def __init__(self, sample_rate=44100, buffer_size=512):
        self.sample_rate = sample_rate
        self.buffer_size = buffer_size
        self.channels = []
        self.effects = {}
        
    def generate_sine_wave(self, frequency, duration, amplitude=0.5):
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        return amplitude * np.sin(2 * np.pi * frequency * t)
    
    def generate_square_wave(self, frequency, duration, amplitude=0.5):
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        return amplitude * np.sign(np.sin(2 * np.pi * frequency * t))
    
    def generate_sawtooth_wave(self, frequency, duration, amplitude=0.5):
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        return amplitude * (2 * (frequency * t - np.floor(0.5 + frequency * t)))
    
    def generate_triangle_wave(self, frequency, duration, amplitude=0.5):
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        return amplitude * (2 * np.abs(2 * (frequency * t - np.floor(0.5 + frequency * t))) - 1)
    
    def apply_envelope(self, audio, attack=0.01, decay=0.1, sustain=0.7, release=0.1):
        samples = len(audio)
        envelope = np.ones(samples)
        
        attack_samples = int(attack * self.sample_rate)
        decay_samples = int(decay * self.sample_rate)
        release_samples = int(release * self.sample_rate)
        
        if attack_samples > 0:
            envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        
        if decay_samples > 0 and attack_samples + decay_samples < samples:
            envelope[attack_samples:attack_samples + decay_samples] = np.linspace(1, sustain, decay_samples)
        
        if release_samples > 0:
            envelope[-release_samples:] = np.linspace(sustain, 0, release_samples)
        
        return audio * envelope
    
    def apply_reverb(self, audio, decay=0.5, delay=0.05):
        delay_samples = int(delay * self.sample_rate)
        output = np.copy(audio)
        
        for i in range(delay_samples, len(audio)):
            output[i] += output[i - delay_samples] * decay
        
        return output
    
    def apply_delay(self, audio, delay_time=0.3, feedback=0.4):
        delay_samples = int(delay_time * self.sample_rate)
        output = np.copy(audio)
        
        for i in range(delay_samples, len(audio)):
            output[i] += output[i - delay_samples] * feedback
        
        return output
    
    def apply_distortion(self, audio, drive=2.0):
        return np.tanh(audio * drive)
    
    def apply_compressor(self, audio, threshold=-20, ratio=4, attack=0.005, release=0.1):
        threshold_linear = 10 ** (threshold / 20)
        output = np.copy(audio)
        
        for i in range(len(output)):
            amplitude = np.abs(output[i])
            if amplitude > threshold_linear:
                gain_reduction = (amplitude - threshold_linear) * (1 - 1/ratio)
                output[i] *= (threshold_linear / amplitude) * (1 + gain_reduction)
        
        return output
    
    def apply_eq(self, audio, low_gain=1.0, mid_gain=1.0, high_gain=1.0):
        from scipy.signal import butter, lfilter
        
        nyquist = self.sample_rate / 2
        
        if low_gain != 1.0:
            low_cutoff = 300 / nyquist
            b, a = butter(2, low_cutoff, btype='low')
            low_freq = lfilter(b, a, audio)
            audio = audio + (low_gain - 1) * low_freq
        
        if high_gain != 1.0:
            high_cutoff = 3000 / nyquist
            b, a = butter(2, high_cutoff, btype='high')
            high_freq = lfilter(b, a, audio)
            audio = audio + (high_gain - 1) * high_freq
        
        return audio
    
    def mix_channels(self, channel_data_list, volumes=None):
        if not channel_data_list:
            return np.array([])
        
        max_length = max(len(ch) for ch in channel_data_list)
        mixed = np.zeros(max_length)
        
        for i, channel in enumerate(channel_data_list):
            volume = volumes[i] if volumes else 0.75
            padded = np.zeros(max_length)
            padded[:len(channel)] = channel
            mixed += padded * volume
        
        mixed = np.clip(mixed, -1.0, 1.0)
        return mixed
    
    def export_to_wav(self, audio, filename, sample_width=2):
        audio = np.clip(audio, -1.0, 1.0)
        
        if sample_width == 2:
            audio_int = (audio * 32767).astype(np.int16)
        else:
            audio_int = (audio * 2147483647).astype(np.int32)
        
        with wave.open(filename, 'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(sample_width)
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(audio_int.tobytes())
        
        return filename
    
    def note_to_frequency(self, midi_note):
        return 440.0 * (2 ** ((midi_note - 69) / 12.0))
    
    def generate_note(self, midi_note, duration, waveform='sine', amplitude=0.5):
        frequency = self.note_to_frequency(midi_note)
        
        if waveform == 'sine':
            audio = self.generate_sine_wave(frequency, duration, amplitude)
        elif waveform == 'square':
            audio = self.generate_square_wave(frequency, duration, amplitude)
        elif waveform == 'sawtooth':
            audio = self.generate_sawtooth_wave(frequency, duration, amplitude)
        elif waveform == 'triangle':
            audio = self.generate_triangle_wave(frequency, duration, amplitude)
        else:
            audio = self.generate_sine_wave(frequency, duration, amplitude)
        
        return self.apply_envelope(audio)
    
    def process_channel_rack(self, channel_data, step_duration=0.25):
        all_audio = []
        volumes = []
        
        for channel in channel_data:
            if channel.get('muted', False):
                continue
            
            channel_audio = np.zeros(int(self.sample_rate * step_duration * 16))
            
            for step_idx, is_active in enumerate(channel.get('steps', [])):
                if is_active:
                    note_audio = self.generate_note(
                        channel.get('note', 60),
                        step_duration,
                        channel.get('waveform', 'sine'),
                        channel.get('volume', 0.75) / 100.0
                    )
                    
                    start_sample = int(step_idx * step_duration * self.sample_rate)
                    end_sample = start_sample + len(note_audio)
                    
                    if end_sample <= len(channel_audio):
                        channel_audio[start_sample:end_sample] += note_audio
            
            all_audio.append(channel_audio)
            volumes.append(1.0)
        
        if all_audio:
            return self.mix_channels(all_audio, volumes)
        
        return np.zeros(int(self.sample_rate * step_duration * 16))