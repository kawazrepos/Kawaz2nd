enchant();

window.onload = function() {
    var game = new Game(320, 320);
    enchant.game = game;
    game.fps = 30;
    game.preload('kawaz.png', 'chara1.gif', 'map2.gif', 'bear.gif', 'bullet.png','map.gif', 'map1.gif', 'effect0.gif'
    ,'gameover.png', 'clear.png', 'blast_small.wav', 'bullet.wav', 'bullet2.mp3', 'bgm.mp3', 'gameover.mp3', 'clear0.wav', 'clear1.wav');
    game.keybind(90, 'a');      // Zキー
    game.keybind(88, 'b');      // Xキー
    game.maxLevel = 2;
    game.onload = function() {
        this.iniedPlayer = false;
        this.isOvered = false;
        this.isCleared = false;
        this.isPaused = false;
        this.gameScene = new Scene();
        this.levelNum = 0;
        this.score = 0;
        enchant.world = new World(0);
        this.gameScene.addChild(enchant.world);
        enchant.world.addChild(enchant.world.levels[0]);
        enchant.level = enchant.world.levels[0];
        
        var score = new Label();
        score.font = "12px 'Arial Black'";                      
        score.addEventListener('enterframe', function() {
            this.text = "Score : " + enchant.game.score;
        });
        var UI = new Label();
        UI.font = "12px 'Arial Balck'";
        UI.addEventListener('enterframe', function() {
            this.text = "HP : " + enchant.world.levels[enchant.world.levelNum].bear.HP;
        });
        UI.x = 280;
        this.gameScene.addChild(score);
        this.gameScene.addChild(UI);

        /*var pad = new Pad();
        pad.x = 0;
        pad.y = 224;
        var apad = new APad();
        apad.x = 224;
        apad.y = 224;
        this.gameScene.addChild(pad);
        this.gameScene.addChild(apad);*/
        this.gameScene.backgroundColor = 'rgb(182, 255, 255)';
        
        // ロゴ
        var titleScene = new Scene();
        var logo = new Scene();
        var logoSurface = game.assets['kawaz.png']
        var logo = new Sprite(logoSurface.width, logoSurface.height);
        logo.x = 20;
        logo.y = 100;
        logo.image = logoSurface;
        logo.scale(.5, .5);
        titleScene.addChild(logo);
        titleScene.e = 0;
        titleScene.addEventListener('enterframe', function() {
            this.e += .01;
            logo._element.style.opacity = Math.sin(this.e * 8) / 2.0 + 0.5;;
        });
        game.pushScene(titleScene);
        var v = new Vector(0, 0);
        var timer = new Timer(60);
        timer.play();
        this.startGame = false;
       
        
        this.addEventListener('enterframe', function() {
            timer.count();
            if (!this.startGame && timer.isOver()){
                game.pushScene(this.gameScene);
                this.startGame = true;
            }
            if (this.isOvered) {
                var overScene = new GameOver();
                this.pushScene(overScene);
                this.isOvered = false;
            } else if (this.isCleared) {
                var clearScene = new ClearScene();
                this.pushScene(clearScene);
                this.isCleared= false;
            }
        });
    };
    game.ini = function(curNum) {
        this.levelNum = curNum;
        this.gameScene = new Scene();
        enchant.world = new World(curNum);
        this.gameScene.addChild(enchant.world);
        enchant.world.levelNum = curNum;
        enchant.world.addChild(enchant.world.levels[0]);
        this.p = new Label();
        this.p.font = "12px 'Arial Black'";
        this.p.x = 160;
        this.p.y = 160;
        this.p.text = "";
        var score = new Label();
        score.font = "12px 'Arial Black'";
        score.addEventListener('enterframe', function() {
            this.text = "Score : " + enchant.game.score;
        });
        var UI = new Label();
        UI.font = "12px 'Arial Balck'";
        UI.addEventListener('enterframe', function() {
            this.text = "HP : " + enchant.level.bear.HP;
        });
        UI.x = 280;
        this.gameScene.addChild(score);
        this.gameScene.addChild(UI);
        
        switch (curNum) {
            default :
                this.gameScene.backgroundColor = 'rgb(182, 255, 255)';
                break;
            case 1:
                this.gameScene.backgroundColor = 'rgb(120, 30, 55)';
                break;
            case 2:
                this.gameScene.backgroundColor = 'rgb(100, 100, 255)';
                break;
        }
        this.pushScene(this.gameScene);
    };
    game.start();
};
