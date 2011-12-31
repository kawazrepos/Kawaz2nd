enchant();

window.onload = function() {
  var game = new Game(256, 256);
  game.fps = 15;
  game.preload('map1.gif', 'chara0.gif' , 'chara5.gif', 'chara6.gif');
  game.keybind(13, 'a');
  game.onload = function() {
    var map = new Map(16, 16);
    map.image = game.assets['map1.gif'];
    map.loadData([
                 [322,322,322,322,322,322,224,225,225,225,225,225,167,205,205,205],
                 [322,322,322,322,322,322,322,322,322,322,322,322,224,225,225,225],
                 [322,322,322,322,322,322,322,322,322,322,322,322,322,322,322,322],
                 [322,322,322,342,342,342,342,342,342,342,322,322,322,322,322,322],
                 [322,322,322,342,342,342,342,342,342,342,322,322,322,322,322,322],
                 [322,322,322,342,342,342,342,342,342,342,322,322,322,322,322,322],
                 [322,322,322,342,342,342,342,342,342,342,322,322,322,322,322,322],
                 [322,322,322,342,342,342,342,342,342,342,322,322,322,322,322,322],
                 [322,322,322,342,342,342,342,342,342,342,322,322,322,322,322,322],
                 [322,322,322,342,342,342,341,341,341,342,322,322,322,322,322,322],
                 [322,322,322, 24, 25, 25, 25, 26,322,322,322,322,322,322,322,322],
                 [322,322,322, 44, 45, 45, 45, 46,322,322,322,322,322,322,322,322],
                 [322,322,322, 64,  7,  6, 65, 66,322,322,322,322,322,322,322,322],
                 [322,322,322,322, 44, 46,322,322,322,322,322,322,322,322,322,322],
                 [322,322,322,322, 44, 46,322,322,322,322,322,322,322,322,322,322],
                 [322,322,322,322, 44, 46,322,322,322,322,322,322,322,322,322,322],
    ],[
    [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [ -1,461,462, -1,461,462, -1,461,462,421,461,462, -1, -1, -1, -1],
    [ -1,481,482, -1,481,482,421,481,482,421,481,482, -1, -1, -1, -1],
    [ -1,421,421,321,341,341,341,341,341,321, -1, -1, -1, -1, -1, -1],
    [ -1,461,462,321,422, -1, -1,400,400,321,461,462, -1, -1, -1, -1],
    [ -1,481,482,321, -1, -1, -1, -1,400,321,481,482, -1, -1, -1, -1],
    [ -1, -1, -1,321,521,521,521,521,521,321,421, -1, -1, -1, -1, -1],
    [ -1,461,462,321, -1, -1, -1, -1, -1,321,461,462, -1, -1, -1, -1],
    [ -1,481,482,321, -1, -1, -1, -1,400,321,481,482, -1, -1, -1, -1],
    [ -1, -1, -1,341, -1, -1, -1, -1, -1,341,421, -1, -1, -1, -1, -1],
    [ -1, -1, -1, -1, -1, -1, -1, -1,421,421, -1, -1, -1, -1, -1, -1],
    [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,461],
    [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,481],
    [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    ]);
    map.collisionData = [
      [  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1],
      [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1],
      [  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  0,  0,  0],
      [  0,  0,  0,  1,  1,  1,  1,  1,  1,  1,  0,  0,  0,  0,  0,  0],
      [  0,  0,  0,  1,  0,  0,  0,  1,  1,  1,  0,  0,  0,  0,  0,  0],
      [  0,  1,  1,  1,  0,  0,  0,  0,  1,  1,  1,  1,  0,  0,  0,  0],
      [  0,  0,  0,  1,  1,  1,  1,  1,  1,  1,  0,  0,  0,  0,  0,  0],
      [  0,  0,  0,  1,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0],
      [  0,  1,  1,  1,  0,  0,  0,  0,  1,  1,  1,  1,  0,  0,  0,  0],
      [  0,  0,  0,  1,  0,  0,  1,  1,  1,  1,  0,  0,  0,  0,  0,  0],
      [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
      [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
      [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
      [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1],
      [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
      [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    ];

    var foregroundMap = new Map(16, 16);
    foregroundMap.image = game.assets['map1.gif'];
    foregroundMap.loadData([
                           [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                           [ -1,461,462, -1,461,462, -1,461,462, -1,461,462, -1, -1, -1, -1],
                           [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                           [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                           [ -1,461,462, -1, -1, -1, -1, -1, -1, -1,461,462, -1, -1, -1, -1],
                           [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                           [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                           [ -1,461,462, -1, -1, -1, -1, -1, -1, -1,461,462, -1, -1, -1, -1],
                           [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                           [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                           [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                           [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                           [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,461],
                           [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                           [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                           [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],   
    ]);


    var player = new Sprite(32, 32);
    player.x = 6 * 16 - 8;
    player.y = 10 * 16;
    var image = new Surface(96, 128);
    image.draw(game.assets['chara0.gif'], 0, 0, 96, 128, 0, 0, 96, 128);
    player.image = image;

    player.isMoving = false;
    player.direction = 0;
    player.walk = 1;
    player.addEventListener('enterframe', function() {
      this.frame = this.direction * 3 + this.walk;

      if(frag2){  
        this.vx = this.vy = 0;
      }else{
        if (this.isMoving) {
          this.moveBy(this.vx, this.vy);

          if (!(game.frame % 3)) {
            this.walk++;
            this.walk %= 3;
          }
          if ((this.vx && (this.x-8) % 16 == 0) || (this.vy && this.y % 16 == 0)) {
            this.isMoving = false;
            this.walk = 1;
          }
        } else {
          this.vx = this.vy = 0;
          if (game.input.left) {
            this.direction = 1;
            this.vx = -4;
          } else if (game.input.right) {
            this.direction = 2;
            this.vx = 4;
          } else if (game.input.up) {
            this.direction = 3;
            this.vy = -4;
          } else if (game.input.down) {
            this.direction = 0;
            this.vy = 4;
          }
          if (this.vx || this.vy) {
            var x = this.x + (this.vx ? this.vx / Math.abs(this.vx) * 16 : 0) + 16;
            var y = this.y + (this.vy ? this.vy / Math.abs(this.vy) * 16 : 0) + 16;
            if (0 <= x && x < map.width && 0 <= y && y < map.height && !map.hitTest(x, y)) {
              this.isMoving = true;
              arguments.callee.call(this);
            }
          }
        }
      }


    });    


    var message = new Label("「俺の名前はニート。23歳で独身だ。」");  
    var frag = false;
    var frag2= true;
    var scene = 0;
    var turn = 0;
    message.font = "10px 'Arial White'";
    console.log(message.width);
    message.y = 224;
    message._element.style.textAlign = "left";

    var message2= new Label(" 本当に名前通りニートになってしまった。」"); 
    message2.font = "10px 'Arial White'";
    console.log(message2.width);
    message2.y = 240;
    message2._element.style.textAlign = "left";

    var messages = [message, message2]; 

    game.addEventListener('enterframe', function() {

      if (game.input.a) {
        frag = true;
      }

      if(frag && !game.input.a){
        game.rootScene.removeChild(messages[0]);
        game.rootScene.removeChild(messages[1]);
        scene +=1;
        frag = false;
      }    
      if(turn == 0){
        if(scene == 0){
          game.rootScene.addChild(messages[0]);  
        }
        if(scene == 1){
          message.text = "「こんなふざけた名前のおかげで就活に失敗し、"; 
          game.rootScene.addChild(messages[0]); 
          game.rootScene.addChild(messages[1]); 
        }
        if(scene == 2){
          message.text = "「それから数年、俺は自室に篭りっきりになった。";    
          message2.text = " それが俺の、せめてもの両親への復讐だったのだ。」"; 
          game.rootScene.addChild(messages[0]); 
          game.rootScene.addChild(messages[1]);     
        }
        if(scene == 3){
          frag2 = false;
          scene = 0;
          turn++;    
        }
      }
      if(turn == 1.1){
        frag2 = true;

        if(scene == 0){
          message.text = "「ここから先は立ち入り禁止区域だ。";    
          message2.text = " さっさと引き返すんだな。」"; 
          game.rootScene.addChild(messages[0]); 
          game.rootScene.addChild(messages[1]);     
        }
        /*if(scene == 1){
          message.text = "「……何故立ち入り禁止なのかだと？"; 
      message.text = "なんだ、知らなかいのか？」";
          game.rootScene.addChild(messages[0]); 
          game.rootScene.addChild(messages[1]); 
        }
        if(scene == 2){
          message.text = "「この先は製作者の手抜きで、マップが存在しないんだ。";    
          message2.text = " バグや強制終了になりたくなければ引き返すんだな。」"; 
          game.rootScene.addChild(messages[0]); 
          game.rootScene.addChild(messages[1]);     
        }
        if(scene == 3){
          message.text = "……ずいぶんメタな発言をする兵士だ。";    
          game.rootScene.addChild(messages[0]);     
        }
        if(scene == 4){
          message.text = "しかし自分がゲームの駒の一つに過ぎないと知りつつも、";    
          message2.text = " 役割を全うしているあたり意外と良い人なのかもしれない"; 
          game.rootScene.addChild(messages[0]); 
          game.rootScene.addChild(messages[1]);   
        }
  */
        if(scene == 1){
          frag2 = false;
          turn = 1;
          scene = 0;

          if(player.x>knight.x){
            player.x +=8;
          }else{
            player.x -=8;
          }
          if(player.y>knight.y){
            player.y+=8;
          }else{
            player.y-=8;
          }
          player.isMoving = false;
        }
      }
  });        

    var clerk = new Sprite(32, 32);
    clerk.x = 5 * 16 + 8;
    clerk.y = 4 * 16;
    var image = new Surface(32, 32);
    image.draw(game.assets['chara0.gif'], 128, 0, 32, 32, 0, 0, 32, 32);
    clerk.image = image;

    game.addEventListener('enterframe', function() {
      game.rootScene.addChild(clerk);              
    });        

    var knight = new Sprite(32, 32);
    knight.x = 12 * 16 + 8;
    knight.y = 4 * 16;
    var image = new Surface(32, 32);
    image.draw(game.assets['chara5.gif'], 32, 0, 32, 32, 0, 0, 32, 32);
    knight.image = image;

    game.addEventListener('enterframe', function() {
      if(knight.intersect(player)){
        turn = 1.1;
      }    
      game.rootScene.addChild(knight);    
    });    

    var stage = new Group();
    stage.addChild(map);
    stage.addChild(player);
    stage.addChild(foregroundMap);
    game.rootScene.addChild(stage);

    var pad = new Pad();
    pad.x = 0;
    pad.y = 220;
    game.rootScene.addChild(pad);

    game.rootScene.addEventListener('enterframe', function(e) {
      var x = Math.min((game.width  - 16) / 2 - player.x, 0);
      var y = Math.min((game.height - 16) / 2 - player.y, 0);
      x = Math.max(game.width,  x + map.width)  - map.width;
      y = Math.max(game.height, y + map.height) - map.height;
      stage.x = x;
      stage.y = y;
    });
  };
  game.start();
};
