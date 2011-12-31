enchant();

window.onload = function() {
  var game = new Game(400, 320);//画面のサイズ設定
  game.fps =30;//画面の１秒間のコマ数
  game.preload('kawaz.gif','itemA.png','itemB.png','back.png','gigi1.gif','gigi2.png');//画像の読み込み
  game.keybind(90, 'a'); //z
  game.score = 0;
  var timer = new Timer(30); //1秒＝30フレーム
  timer.play();

  game.addEventListener('enterframe', function(){
    timer.tick();
    if(timer.isOver()){
      // console.log("owata");
    }
  });

  game.onload = function() {

    var back = new Sprite(400,320);     //背景は「game.rootScene.backgroundColor = 'rgb(○, ○, ○)';」でも可
    back.image = game.assets['back.png'];
    back.x = 0;
    back.y = 0;

    game.rootScene.addChild(back);


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

      if(this.y <= 0 ) {
        this.y == game.height;
      }
      if(this.y + this.height > game.height) {
        this.y = game.height - this.height;
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
    var isFull = false; // 満腹フラグ　は　立ってない
    var eatTime = 0; // 食べはじめた時間

    kawaz.addEventListener('enterframe', function(){

      if(!isFull){
        // 食べてないとき
        if(!game.input.a) {                //けーきが
          if(this.x > itemA.x) {         //左にあるとき
            this.scaleX = 1;
            this.speed = -2;
          } else if(this.x < itemA.x) {  //右にあるとき
            this.scaleX = -1;
            this.speed = 2;
          }
          this.x += this.speed;

          if(this.y+32 > itemA.y+30) {         //上にあるとき
            this.speed = -2;
          } else if(this.y+32 < itemA.y) {  //下にあるとき
            this.speed = 2;
          } else if(itemA.y < this.y+32 < itemA.y+30) { //横にあるとき
            this.speed = 0;
          }
          this.y += this.speed;
        } else if(game.input.a) {          //へびが

          if(this.x > itemA.x) {         //左にあるとき
            this.scaleX = -1;
            this.speed = 5;
          } else if(this.x < itemA.x) {  //右にあるとき
            this.scaleX = 1;
            this.speed = -5;
          }
          this.x += this.speed;

          if(this.y+32 > itemA.y+30) {         //上にあるとき
            this.speed = 5;
          } else if(this.y+32 < itemA.y){   //下にあるとき
            this.speed = -5;
          } else if(itemA.y < this.y+32 < itemA.y+30){  //横にあるとき
            this.speed = 0;
          }
          this.y += this.speed;
        }
        if(this.intersect(itemA)) { //けーきとぶつかったとき
          this.speed = 0;         //止まる
          isFull = true;          //満腹フラグが立つ
          eatTime = game.frame;   //食べ始めた時間がいつなのか記録（eatTimeに現在のgame.frameを代入）
        }
      } else {
        //　食べてるとき
        if(game.frame > eatTime + 90){ //全体の時間が、食べ始めた時間+90フレーム（3秒）になったとき
          isFull = false;            //満腹フラグがなくなる
        }
      }


      //画面からはみ出ないように↓
      if(this.x <= 0 ) {
        this.x = 0;
      }
      if(this.x + this.width > game.width){
        this.x = game.width - this.width;
      }
      if(this.y <= 0 ) {
        this.y = 0;
      }
      if(this.y + this.height > game.height) {
        this.y = game.height - this.height;
      }
      //はみだしここまで↑


      //アニメーション↓

      if (!isFull && game.frame % 4 == 0) {
        this.pose++;
        this.pose %= 4;
        this.frame = this.pose + 1;
      }else if (isFull) {
        this.frame = 0;
      }

      //アニメここまで↑


    });

    game.rootScene.addChild(kawaz);

    //かわずたん　ここまで↑

    //ぎぎねこ↓

    var gigi = new Sprite(50, 50);
    gigi.image = game.assets['gigi1.gif'];
    initialX = [-50, 450][Math.floor(Math.random() * 2)]; // -50か450をランダムで返す
    gigi.x = initialX;
    gigi.y = Math.floor(Math.random() * game.height-50);
    gigi.speed = 0;
    gigi.pose = 0;
    var moe = false; // 萌えフラグは立ってない
    var moeTime = 0;
    var appearTime = Math.floor(Math.random() * 120); // 出現時間を初期化する

    gigi.addEventListener('enterframe', function(){
      if(game.frame >= appearTime) {  // game.frameが出現時間以上になったら
        if(!moe){
          if(this.x == -50) {
            this.scaleX = -1;
            this.speed = 8;
          } else if (this.x == 450) {
            this.scaleX = 1;
            this.speed = -8;
          }

          this.x += this.speed;
          if (game.frame % 3 == 0) {     //あにめーしょん
            this.pose++;
            this.pose %= 2;
            this.frame = this.pose + 1;
          }
          if(this.x < -50 || this.x > 450) {
            appearTime = game.frame + Math.floor(Math.random() * 120); // 出現時間を変える。今の時間から1分以内のどこかにする。
            this.x = initialX;
          }

          if(this.intersect(kawaz)) { //かわずたんとぶつかったとき
            this.speed = 0;         //止まる
            moe = true;          //萌えフラグが立つ
            moeTime = game.frame;   //ぶつかった時間がいつなのか記録（moeTimeに現在のgame.frameを代入）

            var neko = new Sprite(210, 280);       //ぎぎねこ大表示
            neko.image = game.assets['gigi2.png'];
            neko.x = 100;
            neko.y = 10;
            neko.opacity = 1;     //透明度100％
            game.rootScene.addChild(neko);

            neko.addEventListener('enterframe', function(){
              if(game.frame<moeTime + 40) {
                this.opacity = 1 - (game.frame - moeTime) * 0.025;  //透明度を変えて3秒間でフェードイン、フェードアウト
              } else if(moeTime + 40 < game.frame < moeTime + 50) {
                this.opacity = 0;
              } else if(moeTime + 50 < game.frame){
                this.opacity = 0 + (game.frame - moeTime + 50) * 0.025;
              }
              //タイマー止める
            });
          }
        } else {
          //  萌えてるとき
          if(game.frame > moeTime + 90){         //全体の時間が、萌え始めた時間+90フレーム（3秒）になったとき
            game.rootScene.removeChild(neko);  //ぎぎねこ非表示（フェードアウトさせたい）
            moe = false;                       //萌えフラグがなくなる
            appearTime = game.frame + Math.floor(Math.random() * 120); // 出現時間を変える。今の時間から1分以内のどこかにする。
            gigi.x = initialX;

            var itemBNum =10;                  //新たにハートをたくさん出す
            for (i = 0; i < itemBNum; i++) {
              var itemB = new Sprite(30, 30);
              itemB.x = Math.random() * 370;
              itemB.y = Math.random() * 290;
              itemB.image = game.assets['itemB.png']
              itemB.pose = 0;

              itemB.addEventListener('enterframe', function(){

                if (game.frame % 15 == 0) {     //あにめーしょん
                  this.pose++;
                  this.pose %= 2;
                  this.frame = this.pose + 1;
                }
              })
            }

            //タイマー再開
          }
        }

      }
    });
    game.rootScene.addChild(gigi);

    //ぎぎねこここまで↑

    //はーと↓

    var itemBNum = 6;
    for (i = 0; i < itemBNum; i++) {
      var itemB = new Sprite(30, 30);
      itemB.x = Math.random() * 370;
      itemB.y = Math.random() * 290;
      itemB.image = game.assets['itemB.png']
      itemB.pose = 0;

      itemB.addEventListener('enterframe', function(){

    /*　↑

    Math.floor → 小数点以下切り捨て
    Math.random() → ０以上１未満の数をランダムで出す
    * game.width → ゲーム画面の幅をかける

*/

        if(this.intersect(kawaz)){       //スコア
          game.score += 10;
          this.x = Math.random() * 370;
          this.y = Math.random() * 290;
          console.log(game.score);
        }

        if (game.frame % 15 == 0) {     //あにめーしょん
          this.pose++;
          this.pose %= 2;
          this.frame = this.pose + 1;
        }

      });

      game.rootScene.addChild(itemB);


    }
    //はーと　ここまで↑
    //スコア↓

    var score = new Label();
    score.font = "12px 'Arial Black'";                      
    score.addEventListener('enterframe', function() {
      this.text = "Score : " + game.score;
    });

    game.rootScene.addChild(score);

    //スコアここまで↑
	
    /*タイマー↓
	
	var time_label = new Label();
        time_label.x = time_label.y = 15;
        time_label._element.style.zIndex = 128;
		
        time_label.addEventListener(enchant.Event.ENTER_FRAME, function(){
            var progress = parseInt(game.frame/game.fps);          //経過時間の取得
            time = LIMIT_TIME - parseInt(game.frame/game.fps)+"";
            this.text = "リミット : " + time;
            // タイムが0以下になったらゲームオーバーシーンに移行する
            //if (time <= 0) { changeToGameOverScene(); }
        });
        game.rootScene.addChild(time_label);

    タイマーここまで↑*/

	

  }
  game.start();
}
