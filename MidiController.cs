using System;
using System.Collections.Generic;
using System.Threading;

namespace FLStudioClone
{
    public class MidiController
    {
        private bool _isInitialized;
        private List<MidiNote> _activeNotes;
        private readonly object _lockObject = new object();

        public event EventHandler<MidiNoteEventArgs> NoteOn;
        public event EventHandler<MidiNoteEventArgs> NoteOff;
        public event EventHandler<ControlChangeEventArgs> ControlChanged;

        public bool IsConnected { get; private set; }
        public string DeviceName { get; private set; }

        public MidiController()
        {
            _activeNotes = new List<MidiNote>();
            _isInitialized = false;
            IsConnected = false;
        }

        public bool Initialize(string deviceName = "Default")
        {
            try
            {
                DeviceName = deviceName;
                _isInitialized = true;
                IsConnected = true;
                Console.WriteLine($"MIDI Controller initialized: {deviceName}");
                return true;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Failed to initialize MIDI controller: {ex.Message}");
                return false;
            }
        }

        public void Shutdown()
        {
            lock (_lockObject)
            {
                _isInitialized = false;
                IsConnected = false;
                _activeNotes.Clear();
            }
        }

        public void SendNoteOn(int note, int velocity, int channel = 0)
        {
            if (!_isInitialized) return;

            var midiNote = new MidiNote(note, velocity, channel);
            lock (_lockObject)
            {
                _activeNotes.Add(midiNote);
            }

            NoteOn?.Invoke(this, new MidiNoteEventArgs(midiNote));
        }

        public void SendNoteOff(int note, int velocity = 0, int channel = 0)
        {
            if (!_isInitialized) return;

            lock (_lockObject)
            {
                _activeNotes.RemoveAll(n => n.Note == note && n.Channel == channel);
            }

            var midiNote = new MidiNote(note, velocity, channel);
            NoteOff?.Invoke(this, new MidiNoteEventArgs(midiNote));
        }

        public void SendControlChange(int controller, int value, int channel = 0)
        {
            if (!_isInitialized) return;

            ControlChanged?.Invoke(this, new ControlChangeEventArgs(controller, value, channel));
        }

        public List<MidiNote> GetActiveNotes()
        {
            lock (_lockObject)
            {
                return new List<MidiNote>(_activeNotes);
            }
        }

        public void Panic()
        {
            lock (_lockObject)
            {
                foreach (var note in _activeNotes)
                {
                    SendNoteOff(note.Note, 0, note.Channel);
                }
                _activeNotes.Clear();
            }
        }
    }

    public class MidiNote
    {
        public int Note { get; set; }
        public int Velocity { get; set; }
        public int Channel { get; set; }
        public DateTime Timestamp { get; set; }

        public MidiNote(int note, int velocity, int channel)
        {
            Note = note;
            Velocity = Math.Max(0, Math.Min(127, velocity));
            Channel = channel;
            Timestamp = DateTime.Now;
        }

        public float GetFrequency()
        {
            return 440.0f * (float)Math.Pow(2, (Note - 69) / 12.0);
        }
    }

    public class MidiNoteEventArgs : EventArgs
    {
        public MidiNote Note { get; }

        public MidiNoteEventArgs(MidiNote note)
        {
            Note = note;
        }
    }

    public class ControlChangeEventArgs : EventArgs
    {
        public int Controller { get; }
        public int Value { get; }
        public int Channel { get; }

        public ControlChangeEventArgs(int controller, int value, int channel)
        {
            Controller = controller;
            Value = value;
            Channel = channel;
        }
    }

    public class MidiSequencer
    {
        private List<MidiEvent> _events;
        private bool _isPlaying;
        private int _currentPosition;
        private readonly MidiController _controller;
        private Timer _playbackTimer;
        private readonly object _lockObject = new object();

        public int BPM { get; set; }
        public bool IsPlaying => _isPlaying;
        public int CurrentPosition => _currentPosition;

        public MidiSequencer(MidiController controller)
        {
            _controller = controller;
            _events = new List<MidiEvent>();
            _isPlaying = false;
            _currentPosition = 0;
            BPM = 140;
        }

        public void AddEvent(MidiEvent midiEvent)
        {
            lock (_lockObject)
            {
                _events.Add(midiEvent);
                _events.Sort((a, b) => a.Position.CompareTo(b.Position));
            }
        }

        public void RemoveEvent(MidiEvent midiEvent)
        {
            lock (_lockObject)
            {
                _events.Remove(midiEvent);
            }
        }

        public void ClearEvents()
        {
            lock (_lockObject)
            {
                _events.Clear();
                _currentPosition = 0;
            }
        }

        public void Play()
        {
            if (_isPlaying) return;

            _isPlaying = true;
            _currentPosition = 0;

            double intervalMs = (60000.0 / BPM) / 4.0;
            _playbackTimer = new Timer(PlaybackTick, null, 0, (int)intervalMs);
        }

        public void Stop()
        {
            _isPlaying = false;
            _playbackTimer?.Dispose();
            _controller.Panic();
            _currentPosition = 0;
        }

        public void SetBPM(int bpm)
        {
            BPM = Math.Max(20, Math.Min(999, bpm));

            if (_isPlaying)
            {
                _playbackTimer?.Dispose();
                double intervalMs = (60000.0 / BPM) / 4.0;
                _playbackTimer = new Timer(PlaybackTick, null, 0, (int)intervalMs);
            }
        }

        private void PlaybackTick(object state)
        {
            if (!_isPlaying) return;

            lock (_lockObject)
            {
                var eventsToPlay = _events.FindAll(e => e.Position == _currentPosition);

                foreach (var evt in eventsToPlay)
                {
                    if (evt.Type == MidiEventType.NoteOn)
                    {
                        _controller.SendNoteOn(evt.Note, evt.Velocity, evt.Channel);
                    }
                    else if (evt.Type == MidiEventType.NoteOff)
                    {
                        _controller.SendNoteOff(evt.Note, evt.Velocity, evt.Channel);
                    }
                }

                _currentPosition++;
            }
        }
    }

    public enum MidiEventType
    {
        NoteOn,
        NoteOff,
        ControlChange
    }

    public class MidiEvent
    {
        public MidiEventType Type { get; set; }
        public int Note { get; set; }
        public int Velocity { get; set; }
        public int Channel { get; set; }
        public int Position { get; set; }

        public MidiEvent(MidiEventType type, int note, int velocity, int channel, int position)
        {
            Type = type;
            Note = note;
            Velocity = velocity;
            Channel = channel;
            Position = position;
        }
    }
}