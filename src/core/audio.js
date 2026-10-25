export class AmbientAudio {
  constructor() {
    this.context = null;
    this.enabled = false;
    this.nodes = null;
  }

  async enable() {
    if (!this.context) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (!AudioContext) return false;
      this.context = new AudioContext();
      this._build();
    }
    await this.context.resume();
    this.enabled = true;
    this._setGain(0.055, 0.6);
    return true;
  }

  disable() {
    if (!this.context) return;
    this.enabled = false;
    this._setGain(0, 0.4);
  }

  async toggle() {
    if (this.enabled) {
      this.disable();
      return false;
    }
    return this.enable();
  }

  _setGain(value, seconds) {
    if (!this.nodes) return;
    const now = this.context.currentTime;
    this.nodes.master.gain.cancelScheduledValues(now);
    this.nodes.master.gain.setTargetAtTime(value, now, seconds / 3);
  }

  _build() {
    const context = this.context;
    const master = context.createGain();
    master.gain.value = 0;
    master.connect(context.destination);

    const buffer = context.createBuffer(1, context.sampleRate * 4, context.sampleRate);
    const data = buffer.getChannelData(0);
    let last = 0;
    for (let i = 0; i < data.length; i += 1) {
      const white = Math.random() * 2 - 1;
      last = (last + 0.02 * white) / 1.02;
      data[i] = last * 3.5;
    }

    const wind = context.createBufferSource();
    wind.buffer = buffer;
    wind.loop = true;

    const windFilter = context.createBiquadFilter();
    windFilter.type = 'lowpass';
    windFilter.frequency.value = 360;
    windFilter.Q.value = 0.7;

    const windGain = context.createGain();
    windGain.gain.value = 0.8;

    const gust = context.createBufferSource();
    gust.buffer = buffer;
    gust.loop = true;

    const gustFilter = context.createBiquadFilter();
    gustFilter.type = 'bandpass';
    gustFilter.frequency.value = 820;
    gustFilter.Q.value = 0.9;

    const gustGain = context.createGain();
    gustGain.gain.value = 0.16;

    const lfo = context.createOscillator();
    lfo.frequency.value = 0.06;
    const lfoGain = context.createGain();
    lfoGain.gain.value = 120;
    lfo.connect(lfoGain).connect(windFilter.frequency);

    const drone = context.createOscillator();
    drone.type = 'sine';
    drone.frequency.value = 55;
    const droneGain = context.createGain();
    droneGain.gain.value = 0.08;

    wind.connect(windFilter).connect(windGain).connect(master);
    gust.connect(gustFilter).connect(gustGain).connect(master);
    drone.connect(droneGain).connect(master);
    wind.start();
    gust.start();
    lfo.start();
    drone.start();

    this.nodes = { master, wind, gust, drone, lfo };
  }
}
