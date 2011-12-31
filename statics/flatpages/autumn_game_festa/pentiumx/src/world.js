enchant();

(function() {
    enchant.World = Class.create(Group, {
        initialize:function(lvl){
            Group.call(this);
            this.addEventListener('enterframe', function() {
                this.update();
            });
            this.playerPos = 90;
            this.clearPos = 3100;
            this.levelNum = lvl;
            this.deadNum = 0;
            this.levels = new Array();
            switch (lvl) {
                case 0:
                    this.levels.push(new Level1());
                    break;
                case 1:
                    this.levels.push(new Level2());
                    break;
                case 2:
                    this.levels.push(new Level3());
                    break;
            }
        },
        update:function() {
            this.collide();
            enchant.level.x = enchant.world.playerPos - enchant.level.bear.x;
            enchant.level.enemies.forEach(function(e, j) {
                if (e.y > enchant.game.height && e.isAlive) {
                    e.pop(j);
                }
            });
            if (enchant.level.bear.x > enchant.world.clearPos) {
                enchant.game.isCleared = true;
            }
        },
        collide:function() {
                // characterÇ∆bullet
                enchant.level.bullets.forEach(function(b, i) {
                    var ishit = false;
                    if (b.isHostile) {// bulletÇ™ìGëÆê´Ç»ÇÁ
                        ishit = enchant.level.bear.intersect(b);
                        if (ishit) {
                            enchant.level.bear.HP--;
                            b.pop(i);
                        }
                    } else {
                        enchant.level.enemies.forEach(function(e, j) {
                            if (e.isActive) {
                                ishit = e.intersect(b);
                                if (ishit) {
                                    enchant.game.score += 100;
                                    e.HP--;
                                    b.pop();
                                    if (e.HP <= 0) {
                                        enchant.game.score += 500;
                                        enchant.world.deadNum++;
                                        var ef = new Effect(16, 16, enchant.game.assets['effect0.gif'], 5, new Vector(e.x, e.y)
                                            , /*enchant.world.deadNum % 3 == 0 ? true : */false);// SEÇ™èdÇ≠Çƒé~Ç‹ÇÈÇÃÇ≈ífîO
                                        enchant.level.addChild(ef);
                                        e.pop(j);
                                    }
                                }
                            }
                        })
                    }
                })
                // playerÇ∆enemy
                var bear = enchant.level.bear;
                enchant.level.enemies.some(function(e, i) {
                    if (e.isActive) {
                        if (!bear.isDamaged && bear.intersect(e)) {
                            bear.HP--;
                            bear.isDamaged = true;
                            return false;
                        }
                    }
                })
            }
    });
})();