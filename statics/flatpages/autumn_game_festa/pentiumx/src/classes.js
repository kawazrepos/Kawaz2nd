enchant();

(function() {
    enchant.Rectangle = enchant.Class.create({
        initialize: function(x, y, width, height) {
            this.x = x;
            this.y = y;
            this.width = width;
            this.height = height;
        },
        right: {
            get: function() {
                return this.x + this.width;
            }
        },
        bottom: {
            get: function() {
                return this.y + this.height;
            }
        }
    });

    enchant.MapSprite = Class.create(Sprite, {// x, yは表示矩形のサイズであって位置ではない
        initialize:function(x, y, image){
            Sprite.call(this, x, y);
            //enchant.level = enchant.world.levels[enchant.world.levelNum];// コンストラクタ内だからundefinedってことか...!!
            this.image = image;
            this.x = x;
            this.y = y;
            this.v = new Vector(0, 0);
            this.addEventListener('enterframe', function(){
                //if (enchant.level == undefined) enchant.level = enchant.world.levels[enchant.world.levelNum];
                this.update();
                //this.update();// 苦肉の策
            });
            // デバッグ用
            this.addEventListener('touchstart', function() {
                console.log(this.x); console.log(this.y);
            });
        },
        update:function(){
            this.x += this.v.x;
            this.y += this.v.y;
        },
        isOutOfScreen:function(){
            return this.x < -this.image.width || this.x > enchant.game.width
                || this.y < -this.image.height || this.y > enchant.game.height;
        },
        pop:function(){
            enchant.level.removeChild(this);
        }
    });
    enchant.Effect = Class.create(Sprite, {
        initialize:function(x, y, image, frameNum, pos, play) {
            Sprite.call(this, x, y, image);
            this.frameNum = frameNum;
            this.image = image;
            this.x = pos.x;
            this.y = pos.y;
            this.count = 0;
            this.scaleX = this.scaleY = 2.0;
            this.addEventListener('enterframe', function(){
                this.update();
            });
            // 音もついでに
            if (play) {//enchant.world.deadNum % 5 == 0) {// SE重すぎるのでここも削減
                //enchant.game.assets['blast_small.wav'].play();

                var se = enchant.Sound.load('blast_small.wav', 'audio/wav');
                se.volume = 0.3;
                se.play();/**/
            }
        },
        update:function() {
            if (this.count > 0 && this.frame <  this.frameNum-1) this.frame++;
            if (this.count >= this.frameNum) {
                this.pop();
            }
            this.count++;
        },
        pop:function() {
            //console.log(this.frame);
            enchant.level.removeChild(this);
            this.removeEventListener('enterframe', arguments.callee);
        }
    });
    enchant.Character = Class.create(enchant.MapSprite, {
        initialize:function(x, y, image, map){
            MapSprite.call(this, x, y, image);
            this.image = image;
            this.map = map;
            this.speed = 1;
            this.offset = -30;
            this.HP = 0;
            this.isAlive = true;
            /*this.addEventListener('enterframe', function(){
                this.update();
            });*/
        },
        shot: function(){
            var b = new Bullet(this.x + this.image.width/2, this.y + this.offset
                , new Vector(0, -1), 10);
            enchant.level.bullets.push(b);
            enchant.game.currentScene.addChild(b);
        },
        update:function(){
            this.v.resize(this.speed);
            this.x += this.v.x;
            this.y += this.v.y;
        },
        update_motion:function(){
            var friction = 0;
            if (this.v.x > 0.6) {//0.3
                friction = -0.6;
            } else if (this.v.x > 0) {
                friction = -this.v.x;
            }
            if (this.v.x < -0.6) {
                friction = 0.6;
            } else if (this.v.x < 0) {
                friction = -this.v.x;
            }
            friction = 0.80;//0.40;
            
            // ブレーキング
            if (this.v.x > 0) {
                this.v.x += -(1.2 * friction);//.60
                if (this.v.x < 0) this.v.x = 0;
            }
            if (this.v.x < 0) {
                this.v.x += (1.2 * friction)
                if (this.v.x > 0) this.v.x = 0;
            }
            if (this.v.x > 0) this.scaleX = 1;
            if (this.v.x < 0) this.scaleX = -1;
            
            this.v.y += /*this.ay + */1.60;//0.60;
            
            // 最大速度を超えたら制限する
            this.v.x = Math.min(Math.max(this.v.x, -10), 10);
            this.v.y = Math.min(Math.max(this.v.y, -20), 10);
            
            var dest = new Rectangle(
                this.x + this.v.x + 5, this.y + this.v.y + 2,
                this.width-10, this.height-2
            );
            this.jumping = true;
            
            // サンプルの当たり判定そのまま。すり抜ける場合が多いので可能なら書き換えたい
            while (true) {
                var boundary, crossing;
                var dx = dest.x - this.x - 5;
                var dy = dest.y - this.y - 2;
                if (dx > 0 && Math.floor(dest.right / 16) != Math.floor((dest.right - dx) / 16)) {
                    boundary = Math.floor(dest.right / 16) * 16;
                    crossing = (dest.right - boundary) / dx * dy + dest.y;
                    if ((this.map.hitTest(boundary, crossing) && !this.map.hitTest(boundary-16, crossing)) ||
                        (this.map.hitTest(boundary, crossing + dest.height) && !this.map.hitTest(boundary-16, crossing + dest.height))) {
                        this.v.x = 0;
                        dest.x = boundary - dest.width - 0.01;
                        continue;
                    }
                } else if (dx < 0 && Math.floor(dest.x / 16) != Math.floor((dest.x - dx) / 16)) {
                    boundary = Math.floor(dest.x / 16) * 16 + 16;
                    crossing = (boundary - dest.x) / dx * dy + dest.y;
                    if ((this.map.hitTest(boundary-16, crossing) && !this.map.hitTest(boundary, crossing)) ||
                        (this.map.hitTest(boundary-16, crossing + dest.height) && !this.map.hitTest(boundary, crossing + dest.height))) {
                        this.v.x = 0;
                        dest.x = boundary + 0.01;
                        continue;
                    }
                }
                if (dy > 0 && Math.floor(dest.bottom / 16) != Math.floor((dest.bottom - dy) / 16)) {
                    boundary = Math.floor(dest.bottom / 16) * 16;
                    crossing = (dest.bottom - boundary) / dy * dx + dest.x;
                    if ((this.map.hitTest(crossing, boundary) && !this.map.hitTest(crossing, boundary-16)) ||
                        (this.map.hitTest(crossing + dest.width, boundary) && !this.map.hitTest(crossing + dest.width, boundary-16))) {
                        this.jumping = false;
                        this.v.y = 0;
                        dest.y = boundary - dest.height - 0.01;
                        continue;
                    }
                } else if (dy < 0 && Math.floor(dest.y / 16) != Math.floor((dest.y - dy) / 16)) {
                    boundary = Math.floor(dest.y / 16) * 16 + 16;
                    crossing = (boundary - dest.y) / dy * dx + dest.x;
                    if ((this.map.hitTest(crossing, boundary-16) && !this.map.hitTest(crossing, boundary)) ||
                        (this.map.hitTest(crossing + dest.width, boundary-16) && !this.map.hitTest(crossing + dest.width, boundary))) {
                        this.v.y = 0;
                        dest.y = boundary + 0.01;
                        continue;
                    }
                }
                break;
            }
            this.x = dest.x-5;
            this.y = dest.y-2;
        }
    });
    
    
    enchant.Bullet = Class.create(enchant.MapSprite, {
        initialize: function(x, y, bulDir, bulSpeed, user, classname) {
            MapSprite.call(this, x, y, enchant.game.assets['bullet.png']);
            this.v = bulDir;
            //console.log(this.v.x);
            this.speed = bulSpeed;// bulletが動かないバグはこの１行のせいでした本当に(ry
            this.user = user;
            this.x = user.x + 16;
            this.y = user.y + 16;
            this.classname = classname;
            this.isHostile = !(this.classname == 'Player');
            //console.log(this.x);
            /*this.addEventListener('enterframe', function() {
                this.update();
            });*/
        },
        update:function(x, y) {
            //console.log("bul");
            this.v.resize(this.speed);
            //console.log(this.v.x);
            this.x += this.v.x;
            this.y += this.v.y;
            //console.log(this.x);// NaN...!?
            
            if (this.isOutOfScreen()) {
                //console.log("bullet removed");
                enchant.level.removeChild(this);
                enchant.level.bullets.splice(this, 1);
                this.removeEventListener('enterframe', arguments.callee);
            }
        },/**/ // コメントアウトしたら動いた
        isOutOfScreen:function() {
            var b = enchant.level.bear;
            var p = enchant.level.playerPos;
            return this.x < -this.image.width + b.x - p || this.x > enchant.game.width + b.x// + enchant.level.bear.x
                || this.y < -this.image.height || this.y > enchant.game.height;
        },
        pop:function(i) {
            enchant.level.removeChild(this);
            enchant.level.bullets.splice(i, 1);//(this, 1);
            this.removeEventListener('enterframe', arguments.callee);
        }
    });
})();