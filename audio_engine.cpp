#include "audio_engine.h"
#include <algorithm>
#include <stdexcept>

AudioEngine::AudioEngine()
    : m_sampleRate(44100)
    , m_bufferSize(512)
    , m_bpm(140.0f)
    , m_masterVolume(0.75f)
    , m_isPlaying(false)
    , m_currentSample(0)
{
}

AudioEngine::~AudioEngine() {
    shutdown();
}

void AudioEngine::initialize(int sampleRate, int bufferSize) {
    std::lock_guard<std::mutex> lock(m_mutex);
    m_sampleRate = sampleRate;
    m_bufferSize = bufferSize;
    m_currentSample = 0;
}

void AudioEngine::shutdown() {
    std::lock_guard<std::mutex> lock(m_mutex);
    m_isPlaying = false;
    m_oscillators.clear();
}

void AudioEngine::play() {
    std::lock_guard<std::mutex> lock(m_mutex);
    m_isPlaying = true;
}

void AudioEngine::stop() {
    std::lock_guard<std::mutex> lock(m_mutex);
    m_isPlaying = false;
    m_currentSample = 0;
}

void AudioEngine::pause() {
    std::lock_guard<std::mutex> lock(m_mutex);
    m_isPlaying = !m_isPlaying;
}

void AudioEngine::setBPM(float bpm) {
    std::lock_guard<std::mutex> lock(m_mutex);
    m_bpm = std::max(20.0f, std::min(999.0f, bpm));
}

void AudioEngine::setMasterVolume(float volume) {
    std::lock_guard<std::mutex> lock(m_mutex);
    m_masterVolume = std::max(0.0f, std::min(1.0f, volume));
}

void AudioEngine::addOscillator(float frequency, float amplitude, const std::string& type) {
    std::lock_guard<std::mutex> lock(m_mutex);
    Oscillator osc;
    osc.frequency = frequency;
    osc.amplitude = amplitude;
    osc.phase = 0.0f;
    osc.type = type;
    m_oscillators.push_back(osc);
}

void AudioEngine::removeOscillator(int index) {
    std::lock_guard<std::mutex> lock(m_mutex);
    if (index >= 0 && index < static_cast<int>(m_oscillators.size())) {
        m_oscillators.erase(m_oscillators.begin() + index);
    }
}

void AudioEngine::clearOscillators() {
    std::lock_guard<std::mutex> lock(m_mutex);
    m_oscillators.clear();
}

float AudioEngine::generateSine(float frequency, float phase) {
    return std::sin(2.0f * static_cast<float>(M_PI) * phase);
}

float AudioEngine::generateSquare(float frequency, float phase) {
    float value = std::sin(2.0f * static_cast<float>(M_PI) * phase);
    return value >= 0.0f ? 1.0f : -1.0f;
}

float AudioEngine::generateSaw(float frequency, float phase) {
    return 2.0f * (phase - std::floor(phase + 0.5f));
}

float AudioEngine::generateTriangle(float frequency, float phase) {
    return 2.0f * std::abs(2.0f * (phase - std::floor(phase + 0.5f))) - 1.0f;
}

float AudioEngine::applyEnvelope(float value, int sampleIndex) {
    const int attackSamples = static_cast<int>(m_sampleRate * 0.01f);
    const int releaseSamples = static_cast<int>(m_sampleRate * 0.1f);

    if (sampleIndex < attackSamples) {
        return value * (static_cast<float>(sampleIndex) / attackSamples);
    }

    return value;
}

void AudioEngine::processBuffer(std::vector<AudioSample>& buffer) {
    std::lock_guard<std::mutex> lock(m_mutex);

    if (!m_isPlaying || m_oscillators.empty()) {
        for (auto& sample : buffer) {
            sample.left = 0.0f;
            sample.right = 0.0f;
        }
        return;
    }

    for (size_t i = 0; i < buffer.size(); ++i) {
        float mixedValue = 0.0f;

        for (auto& osc : m_oscillators) {
            float sampleValue = 0.0f;

            if (osc.type == "sine") {
                sampleValue = generateSine(osc.frequency, osc.phase);
            } else if (osc.type == "square") {
                sampleValue = generateSquare(osc.frequency, osc.phase);
            } else if (osc.type == "saw") {
                sampleValue = generateSaw(osc.frequency, osc.phase);
            } else if (osc.type == "triangle") {
                sampleValue = generateTriangle(osc.frequency, osc.phase);
            }

            sampleValue = applyEnvelope(sampleValue, m_currentSample);
            mixedValue += sampleValue * osc.amplitude;

            osc.phase += osc.frequency / m_sampleRate;
            if (osc.phase >= 1.0f) {
                osc.phase -= 1.0f;
            }
        }

        mixedValue /= static_cast<float>(m_oscillators.size());
        mixedValue *= m_masterVolume;

        mixedValue = std::max(-1.0f, std::min(1.0f, mixedValue));

        buffer[i].left = mixedValue;
        buffer[i].right = mixedValue;

        m_currentSample++;
    }
}