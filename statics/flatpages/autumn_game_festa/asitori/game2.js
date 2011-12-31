enchant();

window.onload = function() {
    var game = new Game(400, 320);//画面のサイズ設定
    game.fps =30;//画面の１秒間のコマ数
    game.preload('kawaz.gif','itemA.png','itemB.png');//画像の読み込み
    game.keybind(90, 'a'); //z
    
    game.onload = function() {
    
        //けーき・へび↓
    
        var itemA = new Sprite(30, 30);//画像のサイズ
        itemA.image = game.assets['itemA.png'];//画像の名前
        itemA.x = 0;
        itemA.y = 110;//画像の位置
        itemA.pose = 0;//poseをけーきに定義
        
        itemA.addEventListener('enterframe',function(){
            this.speed = 0;
            
            if (game.input.up) {//↑を押したとき
                this.speed = -5;
            } else if (game.input.down) {//↓を押したとき
                this.speed = 5;
            }
            
            if(game.input.left) {//←を押したとき
                this.x = 0;
                this.scaleX = 1;
            } else if (game.input.right){//→を押したとき
                this.x = 370;
                this.scaleX = -1;
            }
            this.y += this.speed;
            
            if(game.input.a) { // ｚを押したとき
             this.frame = 1;
            } else {
             this.frame = 0;
            }
            
            if(this.y < 0){
                this.y = 0;
            } else if(this.y > 370){
                this.y = 370;
            }
        });
        
        game.rootScene.addChild(itemA);
        
        //けーき・へび　ここまで↑
    
        //かわずたん↓
    
        var kawaz = new Sprite(45, 65);
        kawaz.image = game.assets['kawaz.gif'];
        kawaz.x = 138;
        kawaz.y = 110;
        kawaz.pose = 0;
        
        kawaz.addEventListener('enterframe', function(){
            
            if(this.x > itemA.x) {         //けーきが左にあるとき
                this.scaleX = 1;
                this.speed = -2;
            } else if(this.x < itemA.x) {  //けーきが右にあるとき
                this.scaleX = -1;
                this.speed = 2;
            }
            this.x += this.speed;
            
            if(this.y > itemA.y) {         //けーきが上にあるとき
                this.speed = -2;
            } else if(this.y < itemA.y) {  //けーきが下にあるとき
                this.speed = 2;
            } else if(this.y == itemA.y) {  //けーきが横にあるとき
                this.speed = 0;
            }
            this.y += this.speed;
            
            if(game.input.a && this.x > itemA.x) {           //へびが左にあるとき
                this.scaleX = -1;
                this.speed = 2;
            } else if(game.input.a && this.x < itemA.x) {    //へびが右にあるとき
                this.scaleX = 1;
                this.speed = -2;
            }
            this.x += this.speed;
            
            if(game.input.a && this.y > itemA.y) {          //へびが上にあるとき
                this.speed = 2;
            } else if(game.input.a && this.y < itemA.y){    //へびが下にあるとき
                this.speed = -2;
            } else if(game.input.a && this.y == itemA.y){    //へびが横にあるとき
                this.speed = 0;
            }
            this.y += this.speed;
            
        });
        
        game.rootScene.addChild(kawaz);
        
        //かわずたん　ここまで↑
        
        //はーと↓
        
        var itemBNum = 5;
        for (i = 0; i < itemBNum; i++) {
           var itemB = new Sprite(30, 30);
           itemB.x = Math.floor(Math.random() * game.width);
           itemB.y = Math.floor(Math.random() * game.height);
           itemB.image = game.assets['itemB.png']
           itemB.pose = 0;
           
           itemB.addEventListener('enterframe', function(){
           
           if (game.frame % 15 == 0) {
               this.pose++;
               this.pose %= 2;
               this.frame = this.pose + 1;
           }
           
           });
        
        game.rootScene.addChild(itemB);
        
           
       }
        //はーと　ここまで↑
        
    }
    
    game.start();
}