enchant();                                                      // ライブラリを使用するための初期化処理：必ず最初に呼び出す。おまじないのようなもの

window.onload = function() {
    var game = new Game(320, 320);                              // ゲーム画面を320×320で作る。Gameはゲーム全体の処理（メインループやシーン遷移）を管理するクラス。
    game.fps = 30;                                              // FPSを30に設定。パッケージのサンプルではデフォルトで24
    game.score = 0;                                             // スコア用の変数を定義
    game.keybind(90, 'a');                                      // AボタンをZキーに設定(今回は不使用)
    game.preload('miku.gif', 'map.gif', 'bullet.png');          // ゲーム中使用する画像をあらかじめ読み込んでおく
    
    game.onload = function() {
        var miku = new Sprite(44, 32);                          // 画像表示機能を持ったオブジェクト(Sprite)を生成
        miku.x = 138;                                           // 表示位置を指定
        miku.y = 288;                                           // = 320 - 32
        miku.speed = 0;                                         // mikuの移動速度[pixel/frame]を定義。
        miku.image = game.assets['miku.gif'];                   // 表示に使う画像を設定
        miku.pose = 0;                                          // アニメーションに使う変数
        
        // イベントリスナまとめ : http://techblog.55w.jp/?p=473
        miku.addEventListener('enterframe', function() {        // 毎フレーム発生するイベントに使う関数を定義
            // 入力によって動かす処理
            this.speed = 0;
            if (game.input.left) {
                this.scaleX = 1;                               	// 左右反転表示させる
                this.speed = -5;
            } else if (game.input.right) {
                this.scaleX = -1;                               // 左右反転表示させる
                this.speed = 5;
            }
        
            // アニメーションの更新:移動中3フレームごとに。
            if (game.frame % 4 == 0) {
                if (this.speed != 0) {
                    this.pose++;
                    this.pose %= 2;
                    this.frame = this.pose + 1;
                } else {
                    this.frame = 0;
                }
            }
            
            // 位置の更新
            this.x += this.speed;
        });
        game.rootScene.addChild(miku);                          // シーンに追加する。（しないと表示されないので注意）
        
        var items = new Array();
        var itemNum = 5;
        for (i = 0; i < itemNum; i++) {
            var item = new Sprite(24, 24);                      // mikuと同様にSpriteとして生成
            item.x = 32 + i * 64;
            item.y = -64;
            item.speed = 5;
            item.image = game.assets['bullet.png'];
            item.se = enchant.Sound.load('item.mp3', 'audio/mp3');
            item.se.volume = 0.5;
            item.addEventListener('enterframe', function() {
                // 位置の更新
                this.y += this.speed;
                
                // mikuと当たるか、下まで行ったら元の位置に戻る
                if (this.intersect(miku)) {
                    this.se.play();
                    game.score += 100;
                    this.y = -64;
                } else if (this.y > 320) {
                    this.y = -64;
                }
            });
            
            game.rootScene.addChild(item);
        }
        
        var score = new Label();
        score.font = "12px 'Arial Black'";                      // フォントの指定
        score.addEventListener('enterframe', function() {
            this.text = "Score : " + game.score;
        });
        
        var clearLogo = new Label("Clear !!");                  // クリア時に表示する文字
        clearLogo.font = "24px 'Arial Black'";
        clearLogo.y = 160;
        clearLogo._element.style.textAlign = "center";          // CSSで中央揃えする
        game.addEventListener('enterframe', function() {
            if (this.score >= 2000) {
                game.rootScene.addChild(clearLogo);             // クリア時に文字が表示される処理をイベントに追加
            }
        });
        
        game.rootScene.addChild(score);
        game.rootScene.backgroundColor = 'rgb(182, 255, 255)';  // 背景色の設定
    }
    game.start();                                               // ゲーム起動
}