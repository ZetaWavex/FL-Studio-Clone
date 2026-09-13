#ifndef AUDIO_ENGINE_H
#define AUDIO_ENGINE_H

#include <vector>
#include <string>
#include <mutex>
#include <cmath>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

struct AudioSample {
    float left;
    float right;
};

class AudioEngine {
public:
    AudioEngine();
    ~AudioEngine();

    void initialize(int sampleRate = 44100, int bufferSize = 512);
    void shutdown();

    void play();
    void stop();
    void pause();

    bool isPlaying() const { return m_isPlaying; }

    void setBPM(float bpm);
    float getBPM() const { return m_bpm; }

    void setMasterVolume(float volume);
    float getMasterVolume() const { return m_masterVolume; }

    void addOscillator(float frequency, float amplitude, const std::string& type);
    void removeOscillator(int index);
    void clearOscillators();

    void processBuffer(std::vector<AudioSample>& buffer);

    int getSampleRate() const { return m_sampleRate; }
    int getBufferSize() const { return m_bufferSize; }

private:
    struct Oscillator {
        float frequency;
        float amplitude;
        float phase;
        std::string type;
    };

    float generateSine(float frequency, float phase);
    float generateSquare(float frequency, float phase);
    float generateSaw(float frequency, float phase);
    float generateTriangle(float frequency, float phase);

    float applyEnvelope(float value, int sampleIndex);

    int m_sampleRate;
    int m_bufferSize;
    float m_bpm;
    float m_masterVolume;
    bool m_isPlaying;

    std::vector<Oscillator> m_oscillators;
    std::mutex m_mutex;

    int m_currentSample;
};

#endif