enchant();

(function() {
    enchant.Player = Class.create(enchant.Character, {
        initialize:function(x, y, image, map) {
            Character.call(this, x, y, image, map);
            this.pose = 0;
            this.HP = 30;
            this.isDamaged = false;
            this.iniTimer = false;
            this.frameCount = 0;
            this.jumping = true;
            this.jumpBoost = 0;
            this.map = map;
            this.se = enchant.Sound.load('bullet2.mp3', 'audio/mp3');
            this.se.volume = 0.1;
            this.timer = new Timer(15);// ダメージ後の無敵時間にセット
            if (enchant.game.levelNum == 0 && !enchant.game.iniedPlayer) {
                enchant.game.addEventListener('abuttonhasbeendown', function() {
                    if (enchant.game.input.up) {
                        enchant.level.bear.shot(1, 1);
                    } else if (enchant.game.input.down) {
                        enchant.level.bear.shot(1, 2);
                    } else {
                        enchant.level.bear.shot(1, 0);
                    }
                });
                enchant.game.iniedPlayer = true;
            }
        },
        shot: function(type, dir) {
            switch (type) {
                case 0:
                    var b = new Bullet(24, 24, new Vector(1, 0), 20, this, 'Player');
                    enchant.level.bullets.push(b);
                    enchant.level.addChild(b);
                    break;
                case 1:
                    var speed = 5;	                        // 個々のbulletのスピード
                    var width = 30;                             // 射撃するbulletsの幅(degree)
                    var rad = 0;
                    switch (dir) {
                        case 0:
                            if (this.scaleX > 0) rad = Math.atan2(this.y - this.y, this.x + 160 - this.x);
                            else rad = Math.atan2(this.y - this.y, this.x - 160 - this.x);
                            break;
                        case 1:
                            if (this.scaleX > 0) rad = Math.atan2((this.y - 160) - this.y, this.x + 160 - this.x);
                            else rad = Math.atan2((this.y - 160) - this.y, this.x - 160 - this.x);
                            break;
                        case 2:
                            if (this.scaleX > 0) rad = Math.atan2((this.y + 160) - this.y, this.x + 160 - this.x);
                            else rad = Math.atan2((this.y + 160) - this.y, this.x - 160 - this.x);
                            break;
                    }
                    var rotation = 0.0;                         // 最終的な個々のbulletに与える角度(radian)

                    // 角度の割り振り
                    for (i = 0; i < 5; i++) {
                        var tmp = (4 - i) / 4.0;                // 0.0～1.0に丸める
                        tmp -= .5;	                        // -0.5～0.5にする
                        var rot = tmp * width;	                // 角度を求める
                        rotation = rad + rot * Math.PI / 180.0;
                        var vx = Math.cos(rotation) * speed;
                        var vy = Math.sin(rotation) * speed;
                        var b = new Bullet(24, 24, new Vector(vx, vy), 20, this, 'Player');
                        enchant.level.bullets.push(b);
                        enchant.level.addChild(b);
                    }
                    break;
            }
        },
        update:function() {
            this.update_motion_ex();
            this.damage_detection();

            this.timer.count();
        },
        // ダメージ判定、死亡判定
        damage_detection:function() {
            if (this.isDamaged && !this.iniTimer) {
                this.timer.set(15);
                this.timer.play();
                this.iniTimer = true;
                this.v = this.scaleX > 0 ? new Vector(-7, -7) : new Vector(7, -7);// ダメージ時の反動
            }
            if (this.isDamaged) {
                 this.frame = 3;
                 this.scaleX = this.v.x > 0 ? -1 : 1;
            }
            if (this.isDamaged && this.iniTimer && this.timer.isOver()) {
                this.iniTimer = false;
                this.isDamaged = false;
            }
            
            if (this.y > enchant.game.height || this.HP <= 0) {
                var score = Math.round(this.x);
                this.frame = 3;
                this.v.y = -0;
                enchant.game.isOvered = true;
                this.removeEventListener('enterframe', arguments.callee);
            }
        },
        update_motion_ex:function() {
            // 移動とアニメーション
            this.frame = 0;
            this.frameCount++;
            if (!this.isDamaged) {
                if (enchant.game.input.left) this.v.x = -7;
                if (enchant.game.input.right) this.v.x = 7;
                if (this.jumping) {
                if (!enchant.game.input.b) {
                }
                } else {
                    if (enchant.game.input.b) {
                        this.v.y = -20;
                    }
                }
            }
            
            if (!this.isDamaged) {
                if (this.v.x != 0) {
                    if (enchant.game.frame % 3 == 0) {
                        this.pose++;
                        this.pose %= 2;
                    }
                    this.frame = this.pose + 1;
                } else {
                    this.frame = 0;
                }
            }
            this.update_motion();
        }
    });
})();