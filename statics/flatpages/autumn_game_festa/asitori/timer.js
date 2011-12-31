var Timer;
Timer = (function() {
  function Timer(max, repeat, time, active, complete) {
    if (repeat == null) {
      repeat = false;
    }
    if (time == null) {
      time = 0;
    }
    if (active == null) {
      active = false;
    }
    if (complete == null) {
      complete = void 0;
    }
    this.set(max);
    this._time = time;
    this._active = active;
    this._complete = complete;
    this._repeat = repeat;
  }
  Timer.prototype.set = function(max) {
    if (max == null) {
      max = 0;
    }
    this._max = max;
    return this;
  };
  Timer.prototype.play = function() {
    this._active = true;
    return this;
  };
  Timer.prototype.stop = function() {
    this._active = false;
    this._time = 0;
    return this;
  };
  Timer.prototype.pause = function() {
    this._active = false;
    return this;
  };
  Timer.prototype.reset = function() {
    this._time = 0;
    return this;
  };
  Timer.prototype.tick = function() {
    if (this._time < this._max && this._active) {
      ++this._time;
      if (this._time === this._max) {
        if (this._complete != null) {
          this._complete();
        }
        if (this._repeat) {
          this._time = 0;
        }
      }
    }
    return this;
  };
  Timer.prototype.now = function() {
    return this._time;
  };
  Timer.prototype.setComplete = function(func) {
    this._complete = func;
    return this;
  };
  Timer.prototype.setRepeat = function(repeat) {
    this._repeat = repeat;
    return this;
  };
  Timer.prototype.isActive = function() {
    return this._active;
  };
  Timer.prototype.isOver = function() {
    return this._time >= this._max;
  };
  return Timer;
})();