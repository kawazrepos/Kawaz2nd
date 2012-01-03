(function() {
  var BaseMapEvent, BaseStageScene, BlankEvent, BlockEvent, Cursor, LifeLabel, Map1, Map2, Map3, MyGame, Player, Runner, SceneManager, Settings, SpeedLabel, StageScene1, StageScene2, StageScene3, StageSelect1, StageSelectLabel, StageSelectScene1, TimeLabel, TitleLabel, TitleLabel2, TitleMap, TitleScene, settings;
  var __hasProp = Object.prototype.hasOwnProperty, __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor; child.__super__ = parent.prototype; return child; };

  enchant();

  Settings = (function() {

    function Settings() {}

    Settings.chipSize = 32;

    return Settings;

  })();

  settings = new Settings;

  StageSelect1 = (function() {

    __extends(StageSelect1, Map);

    function StageSelect1(width, height, image) {
      StageSelect1.__super__.constructor.call(this, width, height);
      this.image = image;
      this.x = 0;
      this.y = 32;
      this.lowMapData = [[221, 221, 221, 221, 221, 221, 221, 221, 221, 221], [222, 222, 222, 222, 222, 222, 222, 222, 222, 222], [224, 224, 224, 224, 224, 224, 224, 224, 224, 224], [224, 224, 224, 224, 224, 224, 224, 224, 224, 224], [224, 224, 224, 224, 224, 224, 224, 224, 224, 224], [224, 224, 224, 224, 224, 224, 224, 224, 224, 224], [224, 224, 224, 224, 224, 224, 224, 224, 224, 224], [224, 224, 224, 224, 224, 224, 224, 224, 224, 224]];
      this.highMapData = [[251, -1, -1, -1, -1, -1, -1, 251, -1, -1], [-1, -1, -1, 251, -1, -1, -1, -1, -1, 251], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, 321, -1, -1, 322, -1, -1, 323, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, 324, -1, -1, 325, -1, -1, 326, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]];
      this.getMapEvent = function(mapNum) {
        if (mapNum < 0) {
          return "none";
        } else if (mapNum === 321) {
          return "stage1";
        } else if (mapNum === 322) {
          return "stage2";
        } else if (mapNum === 323) {
          return "stage3";
        } else if (mapNum === 324) {
          return "stage4";
        } else {
          return "block";
        }
      };
    }

    return StageSelect1;

  })();

  TitleMap = (function() {

    __extends(TitleMap, Map);

    function TitleMap(width, height, image) {
      TitleMap.__super__.constructor.call(this, width, height);
      this.image = image;
      this.x = 0;
      this.y = 32;
      this.lowMapData = [[221, 221, 221, 221, 221, 221, 221, 221, 221, 221], [222, 222, 222, 222, 222, 222, 222, 222, 222, 222], [223, 223, 223, 223, 223, 223, 223, 210, 210, 223], [224, 224, 210, 210, 210, 210, 210, 211, 211, 210], [210, 210, 211, 211, 211, 211, 224, 224, 224, 224], [211, 211, 224, 224, 224, 224, 224, 210, 210, 210], [224, 224, 224, 210, 210, 210, 210, 211, 211, 211], [210, 210, 210, 211, 211, 211, 211, 211, 211, 211]];
      this.highMapData = [[251, -1, -1, -1, -1, -1, -1, 251, -1, -1], [-1, 251, -1, -1, 251, -1, -1, -1, -1, 251], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]];
    }

    return TitleMap;

  })();

  Map1 = (function() {

    __extends(Map1, Map);

    function Map1(width, height, image) {
      Map1.__super__.constructor.call(this, width, height);
      this.image = image;
      this.x = 0;
      this.y = 32;
      this.lowMapData = [[206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, -1, 206, -1, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, -1, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, -1, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206], [-1, -1, -1, 206, 206, 206, 206, 206, 206, -1, 206, 206, 206, 206, 206, 206, 206, 206, 206, -1, 206, -1, 206, -1, 206, 206, 206, 206, 206, 206, 206, -1, 206, -1, 206, 206, 206, 206, 206, 206, 206, -1, 206, 206, -1, 206, -1, 206, -1, 206, 206, -1, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206], [-1, -1, -1, -1, -1, 206, 206, -1, -1, -1, -1, 206, 206, 206, 206, 206, -1, -1, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, -1, 206, 206, -1, 206, -1, 206, 206, 206, 206, -1, 206, 206, -1, 206, -1, 206, -1, -1, 206, 206, 206, 206, 206, -1, -1, -1, 206, -1, 206, 206, -1, 206, 206, 206, 206], [206, 206, 206, -1, -1, -1, -1, -1, -1, 206, -1, -1, 206, -1, 206, -1, -1, -1, -1, 206, 206, 206, 206, 206, 206, -1, 206, 206, 206, 206, 206, 206, -1, 206, 206, 206, -1, 206, -1, 206, -1, 206, 206, 206, -1, 206, -1, 206, 206, -1, -1, 206, 206, 206, 206, -1, 206, 206, -1, 206, 206, -1, 206, -1], [206, 206, 206, 206, 206, -1, -1, 206, 206, 206, 206, -1, 206, -1, 206, -1, 206, 206, -1, 206, 206, 206, 206, 206, -1, 206, 206, -1, 206, 206, -1, 206, 258, 206, -1, -1, -1, -1, 206, 206, 206, 206, -1, 206, -1, 206, -1, -1, 206, 206, 206, 206, 206, 206, 206, 206, 206, -1, 206, 206, -1, 206, 206, 206], [206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, -1, 206, -1, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, -1, 206, -1, 206, -1, 206, -1, 206, 206, 206, -1, 206, -1, 206, 206, 206, 206, -1, 206, 206, 206, 206, 206, -1, -1, -1, 206, 206, 206, 206, -1, 206, 206, -1, 206], [206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, -1, 206, -1, 206, 206, 206, 206, 206, -1, 206, -1, 206, 206, 206, -1, 206, 206, 206, 206, 258, 206, 258, 206, 206, 206, 206, 206, 206, 206, -1, 206, 206, -1, 206, -1, 206, 206, 206, 206, -1, 206, 206, 206, 206, 206, 206, -1, 206, 206, -1, 206, 206], [206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, -1, 206, -1, 206, 206, 206, 206, 206, 206, 206, 206, 206, -1, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, -1, 206, -1, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, -1, 206, 206, 206]];
      this.getMapEvent = function(mapNum) {
        if (mapNum < 0) {
          return "none";
        } else if (mapNum === 258) {
          return "damage";
        } else {
          return "block";
        }
      };
    }

    return Map1;

  })();

  Map2 = (function() {

    __extends(Map2, Map);

    function Map2(width, height, image) {
      Map2.__super__.constructor.call(this, width, height);
      this.image = image;
      this.x = 0;
      this.y = 32;
      this.lowMapData = [[211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211], [-1, -1, -1, 211, 211, 211, -1, -1, -1, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, -1, -1], [-1, -1, -1, 211, 211, 211, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 211, -1, -1, 258, -1, -1, -1, 258, -1, -1, -1, 211, 211, 211, 211, -1, -1, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, -1, 211], [-1, -1, -1, 211, 211, 211, -1, -1, -1, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 211, 211, 211, 211, 211, 211, -1, 211], [211, 211, 211, -1, -1, -1, 211, 211, 211, -1, -1, -1, -1, -1, -1, -1, -1, 211, 211, -1, 211, 211, -1, 211, 211, -1, 211, 211, 211, 211, 211, 211, -1, -1, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, -1, -1, -1, -1, -1, 211, 211, -1, 211], [211, 211, 211, -1, -1, -1, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 258, -1, 258, -1, 258, -1, 258, -1, -1, 211, 211, 211, 211, 211, 211, 211, 211, -1, -1, -1, -1, 211], [211, 211, 211, -1, -1, -1, 211, 211, 211, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, -1, 211], [211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, -1, 211]];
      this.getMapEvent = function(mapNum) {
        if (mapNum < 0) {
          return "none";
        } else if (mapNum === 258) {
          return "damage";
        } else {
          return "block";
        }
      };
    }

    return Map2;

  })();

  Map3 = (function() {

    __extends(Map3, Map);

    function Map3(width, height, image) {
      Map3.__super__.constructor.call(this, width, height);
      this.image = image;
      this.x = 0;
      this.y = 32;
      this.lowMapData = [[205, 205, 205, 205, -1, 205, -1, 205, -1, 205, 205, -1, 205, 205, -1, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, -1, 205, 205, 205, 205, 205, 205, 205, -1, 205], [-1, -1, -1, 205, 205, 205, 205, 205, 205, 205, 205, 205, -1, -1, 205, 205, 205, 205, 205, 205, 205, 205, 205, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 205, -1, 205, -1, 205, -1, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205], [-1, 205, -1, 205, -1, 205, -1, 205, -1, 258, 258, -1, 205, 205, -1, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, -1, 205, 205, -1, 205, -1, 205, -1, -1, -1, -1, 258, -1, -1, -1, -1, -1, -1, -1, -1, -1, 258, -1, -1, -1, -1, -1, -1, -1, -1, 205, 205], [-1, 205, -1, 205, -1, -1, -1, 205, -1, 205, 205, -1, 258, 258, -1, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, -1, 205, -1, 205, -1, 205, -1, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, -1, 205, 205, 205, 205, 205, 205, 205, 205, 205], [-1, 205, -1, 205, -1, 205, -1, 205, -1, -1, -1, -1, 205, 205, -1, 205, 205, 205, 205, 205, 205, 205, 205, 258, -1, 258, -1, 258, -1, 258, -1, 258, -1, 205, 205, -1, 205, -1, 205, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 258, -1, -1, -1, 258, -1, 258, -1, 258, -1, 258, -1], [-1, 205, -1, -1, -1, 205, -1, 205, -1, 205, 205, -1, 258, 258, -1, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 258, -1, -1, 205, -1, 205, -1, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, -1, 205, 205, 205, 205, 205, 205, 205, 205, 205], [-1, 205, -1, 205, 258, 205, 258, -1, -1, 258, 258, -1, 205, 205, 258, -1, -1, -1, -1, -1, -1, -1, -1, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, -1, 205, -1, 205, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 258, -1, -1, -1, -1, 258, -1, -1, -1, -1, -1, -1, -1, 205, 205], [205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, -1, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205]];
      this.getMapEvent = function(mapNum) {
        if (mapNum < 0) {
          return "none";
        } else if (mapNum === 258) {
          return "damage";
        } else {
          return "block";
        }
      };
    }

    return Map3;

  })();

  BaseMapEvent = (function() {

    function BaseMapEvent() {
      this.isBlock = false;
      this.name = "default";
    }

    return BaseMapEvent;

  })();

  BlankEvent = (function() {

    __extends(BlankEvent, BaseMapEvent);

    function BlankEvent() {
      BlankEvent.__super__.constructor.apply(this, arguments);
      this.name = "blank";
    }

    return BlankEvent;

  })();

  BlockEvent = (function() {

    __extends(BlockEvent, BaseMapEvent);

    function BlockEvent() {
      BlockEvent.__super__.constructor.apply(this, arguments);
      this.isBlock = true;
      this.name = "block";
    }

    return BlockEvent;

  })();

  Runner = (function() {

    __extends(Runner, Sprite);

    function Runner(width, height, game) {
      var runner_image;
      var _this = this;
      Runner.__super__.constructor.call(this, width, height);
      runner_image = new Surface(96, 128);
      runner_image.draw(game.assets['chara0.gif'], 128, 0, 96, 128, 0, 0, 96, 128);
      this.game = game;
      this.map = game.map;
      this.image = runner_image;
      this.mapx = 0;
      this.mapy = 1;
      this.x = 32 * this.mapx;
      this.y = 32 * this.mapy;
      this.direction = 2;
      this.life = 10;
      this.walk = 1;
      this.wait = 40;
      this.minwait = 18;
      this.maxwait = 50;
      this.count = 0;
      this.isFalling = false;
      this.fallingCount = 0;
      this.frame = this.direction * 3 + this.walk;
      this.move = function(x, y) {
        if (x !== 0) {
          if (_this.map.getMapEvent(_this.map.lowMapData[_this.mapy][_this.mapx + 1]) === "block") {
            _this.wait = _this.maxwait;
          } else {
            _this.mapx += x;
            if (_this.wait > _this.minwait) _this.wait -= 2;
          }
        }
        if (_this.mapy !== _this.map.lowMapData.length - 1) {
          if (_this.map.getMapEvent(_this.map.lowMapData[_this.mapy + 1][_this.mapx]) !== "block" && y > 0) {
            _this.mapy += y;
          }
        }
        if (_this.mapy !== 0) {
          if (_this.map.getMapEvent(_this.map.lowMapData[_this.mapy - 1][_this.mapx]) !== "block" && y < 0) {
            _this.mapy += y;
          }
        }
        return _this.statusChange();
      };
      this.statusChange = function() {
        var se;
        _this.count = 0;
        _this.fallingCount = 0;
        if (_this.map.getMapEvent(_this.map.lowMapData[_this.mapy][_this.mapx]) === "damage") {
          se = Sound.load("sound/se/hit.mp3", "audio/mp3");
          se.play();
          _this.life -= 1;
        }
        if (_this.map.lowMapData[0].length - 2 < _this.mapx) {
          return _this.game.gameClear();
        }
      };
      this.fallAction = function() {
        if (_this.mapy < _this.game.map.lowMapData.length - 1) {
          if (_this.map.getMapEvent(_this.map.lowMapData[_this.mapy + 1][_this.mapx]) !== "block") {
            _this.isFalling = true;
          } else {
            _this.isFalling = false;
            _this.fallingCount = 0;
          }
          if (_this.isFalling) {
            if (_this.fallingCount >= _this.height) {
              _this.move(0, 1);
              return _this.fallingCount = 0;
            } else {
              return _this.fallingCount += 2;
            }
          }
        } else {
          return _this.isFalling = false;
        }
      };
      this.positioningAction = function() {
        _this.y = 32 + 32 * _this.mapy + _this.fallingCount;
        return _this.x = 32 * _this.mapx;
      };
      this.action = function() {
        _this.fallAction();
        if (!_this.isFalling && _this.count >= _this.wait) _this.move(1, 0);
        _this.positioningAction();
        return _this.count++;
      };
      this.addEventListener('enterframe', this.action);
    }

    return Runner;

  })();

  Cursor = (function() {

    __extends(Cursor, Sprite);

    function Cursor(width, height, game, scene) {
      var image;
      var _this = this;
      Cursor.__super__.constructor.call(this, width, height);
      this.game = game;
      this.mapx = 0;
      this.mapy = 0;
      this.x = this.mapx * 32;
      this.y = this.mapy * 32 + 32;
      image = new Surface(32, 32);
      image.context.beginPath();
      image.context.fillStyle = 'rgba(255, 0, 0, 0.4)';
      image.context.fillRect(0, 0, 32, 32);
      this.image = image;
      this.inputwait = game.fps / 10;
      this.move = function(x, y) {
        _this.mapx += x;
        _this.mapy += y;
        return _this.positioningAction();
      };
      this.positioningAction = function() {
        _this.x = 32 * _this.mapx;
        return _this.y = 32 + 32 * _this.mapy;
      };
      this.inputAction = function() {
        var event;
        if (_this.game.input.left) {
          _this.move(-1, 0);
          _this.inputwait = game.fps / 10;
        } else if (_this.game.input.right) {
          _this.move(1, 0);
          _this.inputwait = game.fps / 10;
        } else if (_this.game.input.up) {
          _this.move(0, -1);
          _this.inputwait = game.fps / 10;
        } else if (_this.game.input.down) {
          _this.move(0, 1);
          _this.inputwait = game.fps / 10;
        }
        if (_this.game.input.a) {
          event = scene.highmap.getMapEvent(scene.highmap.highMapData[_this.mapy][_this.mapx]);
          _this.game.manager.switchScene(event, null);
          console.log("okk");
          return _this.inputwait = game.fps / 10;
        }
      };
      this.action = function() {
        if (_this.inputwait <= 0) {
          return _this.inputAction();
        } else {
          return _this.inputwait--;
        }
      };
      this.addEventListener('enterframe', this.action);
    }

    return Cursor;

  })();

  Player = (function() {

    __extends(Player, Sprite);

    function Player(width, height, game) {
      var image;
      var _this = this;
      Player.__super__.constructor.call(this, width, height);
      this.game = game;
      this.map = game.map;
      this.runner = game.runner;
      this.mapx = 0;
      this.x = this.mapx * 32;
      this.y = 320 - 32;
      image = new Surface(96, 128);
      image.draw(game.assets['chara0.gif'], 192, 0, 96, 128, 0, 0, 96, 128);
      this.image = image;
      this.direction = 3;
      this.walk = 1;
      this.speed = 1;
      this.inputwait = game.fps / 10;
      this.frame = this.direction * 3 + this.walk;
      this.move = function(x, y) {
        _this.mapx += x;
        _this.mapy += y;
        return _this.positioningAction();
      };
      this.positioningAction = function() {
        return _this.x = 32 * _this.mapx;
      };
      this.inputAction = function() {
        var num, renum, temp, _ref, _ref2;
        if (_this.game.input.left) {
          _this.move(-1, 0);
          _this.inputwait = game.fps / 10;
        } else if (_this.game.input.right) {
          _this.move(1, 0);
          _this.inputwait = game.fps / 10;
        }
        if (_this.game.input.up && _this.canUp()) {
          temp = _this.map.lowMapData[0][_this.mapx];
          for (num = 0, _ref = _this.map.lowMapData.length - 2; 0 <= _ref ? num <= _ref : num >= _ref; 0 <= _ref ? num++ : num--) {
            _this.map.lowMapData[num][_this.mapx] = _this.map.lowMapData[num + 1][_this.mapx];
          }
          _this.map.lowMapData[_this.map.lowMapData.length - 1][_this.mapx] = temp;
          _this.map.loadData(_this.map.lowMapData);
          if (_this.isRunnerUp()) _this.runner.move(0, -1);
          return _this.inputwait = game.fps / 10;
        } else if (_this.game.input.down && _this.canDown()) {
          temp = _this.map.lowMapData[_this.map.lowMapData.length - 1][_this.mapx];
          for (num = 0, _ref2 = _this.map.lowMapData.length - 2; 0 <= _ref2 ? num <= _ref2 : num >= _ref2; 0 <= _ref2 ? num++ : num--) {
            renum = (_this.map.lowMapData.length - 1) - num;
            _this.map.lowMapData[renum][_this.mapx] = _this.map.lowMapData[renum - 1][_this.mapx];
          }
          _this.map.lowMapData[0][_this.mapx] = temp;
          _this.map.loadData(_this.map.lowMapData);
          if (_this.isRunnerDown()) _this.runner.move(0, 1);
          return _this.inputwait = game.fps / 10;
        }
      };
      this.canUp = function() {
        if (_this.mapx !== _this.runner.mapx) {
          return true;
        } else {
          if (_this.runner.mapy !== 0) return true;
        }
        return false;
      };
      this.isRunnerUp = function() {
        if (_this.mapx === _this.runner.mapx) {
          if (_this.runner.mapy !== 0) {
            if (_this.map.getMapEvent(_this.map.lowMapData[_this.runner.mapy][_this.runner.mapx]) === "block") {
              return true;
            }
          }
        }
        return false;
      };
      this.canDown = function() {
        if (_this.mapx !== _this.runner.mapx) {
          return true;
        } else {
          if (_this.runner.mapy !== _this.map.lowMapData.length - 1) {
            return true;
          } else {
            if (_this.map.getMapEvent(_this.map.lowMapData[_this.runner.mapy - 1][_this.runner.mapx]) !== "block") {
              return true;
            }
          }
        }
        return false;
      };
      this.isRunnerDown = function() {
        if (_this.mapx === _this.runner.mapx) {
          if (_this.map.getMapEvent(_this.map.lowMapData[_this.runner.mapy][_this.runner.mapx]) === "block") {
            return true;
          }
        }
        return false;
      };
      this.action = function() {
        if (_this.inputwait <= 0) {
          return _this.inputAction();
        } else {
          return _this.inputwait--;
        }
      };
      this.addEventListener('enterframe', this.action);
    }

    return Player;

  })();

  TimeLabel = (function() {

    __extends(TimeLabel, Label);

    function TimeLabel(game) {
      var _this = this;
      TimeLabel.__super__.constructor.apply(this, arguments);
      this.startTime = new Date().getTime();
      this.passedTime = 0;
      this.font = "12px 'Arial Black'";
      this.isRunning = true;
      this.action = function() {
        var lastTime;
        if (_this.isRunning) {
          _this.passedTime = (new Date().getTime() - _this.startTime) / 1000;
          lastTime = (game.timelimit - _this.passedTime).toFixed(1);
          _this.text = "Time : " + lastTime;
          if (lastTime <= game.timelimit / 5) {
            _this.color = "red";
          } else if (lastTime <= game.timelimit / 3) {
            _this.color = "orange";
          } else {
            _this.color = "black";
          }
          if (_this.passedTime > game.timelimit) return game.gameOver();
        }
      };
      this.addEventListener('enterframe', this.action);
    }

    return TimeLabel;

  })();

  LifeLabel = (function() {

    __extends(LifeLabel, Label);

    function LifeLabel(game) {
      var _this = this;
      LifeLabel.__super__.constructor.apply(this, arguments);
      this.font = "12px 'Arial Black'";
      this.x = 150;
      this.y = 0;
      this.action = function() {
        _this.text = "Life : " + game.runner.life;
        if (game.runner.life <= 2) {
          _this.color = "red";
        } else if (game.runner.life <= 5) {
          _this.color = "yellow";
        } else {
          _this.color = "black";
        }
        if (game.runner.life <= 0) return game.gameOver();
      };
      this.addEventListener('enterframe', this.action);
    }

    return LifeLabel;

  })();

  SpeedLabel = (function() {

    __extends(SpeedLabel, Label);

    function SpeedLabel(game) {
      var waitgap;
      var _this = this;
      SpeedLabel.__super__.constructor.apply(this, arguments);
      this.x = 220;
      this.y = 0;
      this.font = "12px 'Arial Black'";
      waitgap = game.runner.maxwait - game.runner.minwait;
      this.action = function() {
        var speed;
        speed = Math.floor((game.runner.maxwait - game.runner.wait) / waitgap * 100);
        _this.text = "Speed : " + speed + "%";
        if (speed >= 100) {
          return _this.color = "#006600";
        } else if (speed >= 70) {
          return _this.color = "#226622";
        } else if (speed >= 40) {
          return _this.color = "#336633";
        } else {
          return _this.color = "#556655";
        }
      };
      this.addEventListener('enterframe', this.action);
    }

    return SpeedLabel;

  })();

  TitleLabel = (function() {

    __extends(TitleLabel, Label);

    function TitleLabel(game) {
      TitleLabel.__super__.constructor.apply(this, arguments);
      this.x = 50;
      this.y = 40;
      this.font = "25px 'Arial Black'";
      this.color = "black";
      this.text = "Molehill Runner";
    }

    return TitleLabel;

  })();

  TitleLabel2 = (function() {

    __extends(TitleLabel2, Label);

    function TitleLabel2(game) {
      TitleLabel2.__super__.constructor.apply(this, arguments);
      this.x = 75;
      this.y = 260;
      this.font = "20px 'Arial Rounded MT Bold'";
      this.color = "white";
      this.text = "Press Z To Start";
    }

    return TitleLabel2;

  })();

  StageSelectLabel = (function() {

    __extends(StageSelectLabel, Label);

    function StageSelectLabel(game) {
      StageSelectLabel.__super__.constructor.apply(this, arguments);
      this.x = 60;
      this.y = 5;
      this.font = "16px 'Arial Black'";
      this.color = "black";
      this.text = "Stage Select";
    }

    return StageSelectLabel;

  })();

  BaseStageScene = (function() {

    function BaseStageScene(game) {
      var _this = this;
      this.game = game;
      this.game.runner = new Runner(32, 32, this.game);
      this.game.player = new Player(32, 32, this.game);
      this.game.timeLabel = new TimeLabel(this.game);
      this.game.lifeLabel = new LifeLabel(this.game);
      this.game.speedLabel = new SpeedLabel(this.game);
      this.game.stage = new Group();
      this.game.action = function() {
        var x;
        x = Math.min((_this.game.width - 160) / 2 - _this.game.runner.x, 0);
        x = Math.max(_this.game.width, x + _this.game.map.width) - _this.game.map.width;
        return _this.game.stage.x = x;
      };
      this.game.currentScene.addEventListener('enterframe', this.game.action);
      this.game.stage.addChild(this.game.map);
      this.game.stage.addChild(this.game.runner);
      this.game.stage.addChild(this.game.player);
      this.game.currentScene.addChild(this.game.stage);
      this.game.currentScene.addChild(this.game.timeLabel);
      this.game.currentScene.addChild(this.game.speedLabel);
      this.game.currentScene.addChild(this.game.lifeLabel);
    }

    return BaseStageScene;

  })();

  StageScene1 = (function() {

    __extends(StageScene1, BaseStageScene);

    function StageScene1(game) {
      this.game = game;
      this.game.map = new Map1(32, 32, this.game.assets['wholemap32.gif']);
      this.game.map.loadData(this.game.map.lowMapData);
      this.game.timelimit = 100;
      StageScene1.__super__.constructor.apply(this, arguments);
    }

    return StageScene1;

  })();

  StageScene2 = (function() {

    __extends(StageScene2, BaseStageScene);

    function StageScene2(game) {
      this.game = game;
      this.game.map = new Map2(32, 32, this.game.assets['wholemap32.gif']);
      this.game.map.loadData(this.game.map.lowMapData);
      this.game.timelimit = 60;
      StageScene2.__super__.constructor.apply(this, arguments);
    }

    return StageScene2;

  })();

  StageScene3 = (function() {

    __extends(StageScene3, BaseStageScene);

    function StageScene3(game) {
      this.game = game;
      this.game.map = new Map3(32, 32, this.game.assets['wholemap32.gif']);
      this.game.map.loadData(this.game.map.lowMapData);
      this.game.timelimit = 60;
      StageScene3.__super__.constructor.apply(this, arguments);
    }

    return StageScene3;

  })();

  StageSelectScene1 = (function() {

    function StageSelectScene1(game) {
      var scene;
      this.game = game;
      scene = this.game.currentScene;
      scene.lowmap = new StageSelect1(32, 32, this.game.assets['wholemap32.gif']);
      scene.lowmap.loadData(scene.lowmap.lowMapData);
      scene.highmap = new StageSelect1(32, 32, this.game.assets['wholemap32.gif']);
      scene.highmap.loadData(scene.highmap.highMapData);
      scene.cursor = new Cursor(32, 32, this.game, scene);
      scene.stage = new Group();
      scene.label = new StageSelectLabel(game);
      scene.stage.addChild(scene.lowmap);
      scene.stage.addChild(scene.highmap);
      scene.stage.addChild(scene.cursor);
      scene.stage.addChild(scene.label);
      scene.addChild(scene.stage);
    }

    return StageSelectScene1;

  })();

  TitleScene = (function() {

    function TitleScene(game) {
      var action, scene;
      var _this = this;
      this.game = game;
      scene = this.game.currentScene;
      scene.lowmap = new TitleMap(32, 32, this.game.assets['wholemap32.gif']);
      scene.lowmap.loadData(scene.lowmap.lowMapData);
      scene.highmap = new TitleMap(32, 32, this.game.assets['wholemap32.gif']);
      scene.highmap.loadData(scene.highmap.highMapData);
      scene.stage = new Group();
      scene.titleLabel = new TitleLabel(game);
      scene.titleLabel2 = new TitleLabel2(game);
      scene.runner = new Sprite(32, 32);
      scene.runner.image = new Surface(96, 128);
      scene.runner.image.draw(game.assets['chara0.gif'], 128, 0, 96, 128, 0, 0, 96, 128);
      scene.runner.x = 7 * 32;
      scene.runner.y = 5 * 32;
      scene.runner.frame = 2 * 3 + 1;
      scene.player = new Sprite(32, 32);
      scene.player.image = new Surface(96, 128);
      scene.player.image.draw(game.assets['chara0.gif'], 192, 0, 96, 128, 0, 0, 96, 128);
      scene.player.x = 4 * 32;
      scene.player.y = 6 * 32;
      scene.player.frame = 2 * 3;
      action = function() {
        return _this.game.manager.switchScene("stageselect1", "");
      };
      scene.addEventListener(Event.A_BUTTON_DOWN, action);
      scene.stage.addChild(scene.lowmap);
      scene.stage.addChild(scene.highmap);
      scene.stage.addChild(scene.player);
      scene.stage.addChild(scene.runner);
      scene.stage.addChild(scene.titleLabel);
      scene.stage.addChild(scene.titleLabel2);
      scene.addChild(scene.stage);
    }

    return TitleScene;

  })();

  SceneManager = (function() {

    function SceneManager(game) {
      var _this = this;
      this.game = game;
      this.sceneData = null;
      this.clear = function() {
        return _this.game.replaceScene(new Scene());
      };
      this.switchScene = function(scene, prm) {
        switch (scene) {
          case "stage1":
            _this.clear();
            return _this.sceneData = new StageScene1(_this.game);
          case "stage2":
            _this.clear();
            return _this.sceneData = new StageScene2(_this.game);
          case "stage3":
            _this.clear();
            return _this.sceneData = new StageScene3(_this.game);
          case "stageselect1":
            _this.clear();
            return _this.sceneData = new StageSelectScene1(_this.game);
          case "title":
            _this.clear();
            return _this.sceneData = new TitleScene(_this.game);
        }
      };
    }

    return SceneManager;

  })();

  MyGame = (function() {

    __extends(MyGame, Game);

    function MyGame(width, height) {
      var _this = this;
      MyGame.__super__.constructor.call(this, width, height);
      this.fps = 30;
      this.preload('wholemap32.gif', 'chara0.gif');
      this.keybind(90, 'a');
      this.isPause = false;
      this.bgm = Sound.load("sound/bgm/bgm1.mp3", "audio/mp3");
      this.bgm._element.loop = true;
      this.bgm.play();
      this.onload = function() {
        if (window.first) {
          _this.init();
          return window.first = false;
        }
      };
      this.init = function() {
        this.manager = new SceneManager(this);
        return this.manager.switchScene("title", "");
      };
      this.callPause = function() {
        var filter, filterImage, pauseScene;
        filter = new Sprite(320, 320);
        filterImage = new Surface(10, 10);
        filterImage.clear();
        filterImage.context.beginPath();
        filterImage.context.fillStyle = 'rgba(255, 255, 255, 0.5)';
        filterImage.context.fillRect(0, 0, 10, 10);
        filter.image = filterImage;
        this.pause();
        pauseScene = new Scene;
        pauseScene.addChild(filter);
        return this.pushScene(pauseScene);
      };
      this.exitPause = function() {
        return this.start();
      };
      this.gameOver = function() {
        var action, clearLogo, filter, filterImage;
        var _this = this;
        console.log("game over");
        this.timeLabel.isRunning = false;
        filter = new Sprite(320, 320);
        filterImage = new Surface(5, 5);
        filterImage.clear();
        filterImage.context.beginPath();
        filterImage.context.fillStyle = 'rgba(255, 255, 255, 0.5)';
        filterImage.context.fillRect(0, 0, 5, 5);
        filter.image = filterImage;
        clearLogo = new Label("Game Over...");
        clearLogo.font = "24px 'Arial Black'";
        clearLogo.y = 130;
        clearLogo._element.style.textAlign = "center";
        this.currentScene.addChild(filter);
        this.currentScene.addChild(clearLogo);
        this.pause();
        action = function() {
          _this.manager.switchScene("stageselect1", "");
          return _this.start();
        };
        return this.currentScene.addEventListener(Event.A_BUTTON_DOWN, action);
      };
      this.gameClear = function() {
        var action, clearLogo, filter, filterImage, score, scoreLabel;
        var _this = this;
        console.log("clear!");
        this.timeLabel.isRunning = false;
        filter = new Sprite(320, 320);
        filterImage = new Surface(5, 5);
        filterImage.clear();
        filterImage.context.beginPath();
        filterImage.context.fillStyle = 'rgba(255, 255, 255, 0.5)';
        filterImage.context.fillRect(0, 0, 5, 5);
        filter.image = filterImage;
        clearLogo = new Label("Clear !!");
        clearLogo.font = "24px 'Arial Black'";
        clearLogo.y = 130;
        clearLogo._element.style.textAlign = "center";
        score = Math.floor((5000 - (this.timeLabel.passedTime * 10)) * this.runner.life / 10);
        scoreLabel = new Label("Score:" + score);
        scoreLabel.y = 160;
        scoreLabel._element.style.textAlign = "center";
        this.currentScene.addChild(filter);
        this.currentScene.addChild(clearLogo);
        this.currentScene.addChild(scoreLabel);
        this.pause();
        action = function() {
          _this.manager.switchScene("stageselect1", "");
          return _this.start();
        };
        return this.currentScene.addEventListener(Event.A_BUTTON_DOWN, action);
      };
    }

    return MyGame;

  })();

  window.onload = function() {
    var game;
    game = new MyGame(320, 320);
    game.start();
    return window.first = true;
  };

}).call(this);
