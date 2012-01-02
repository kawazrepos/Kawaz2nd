enchant();
// ライブラリを使用するための初期化処理：必ず最初に呼び出す。おまじないのようなもの

messages = [											//メッセージの配列をつくっておく（多次元配列。台詞,ジェド表情,ラチカ表情）
["ー聖ニコラウス学園ー",7,6],
["この学園には、世界中から「意識の高い学生（笑）」たちが集う。",7,6],
["彼らが志し高く目指しているもの、それは……",7,6],
["【ラチカ】<br/>「ほーほーほー」",7,2],
["【ジェド】<br/>「違う。もっと腹の奥で響かせるように」",0,2],
["【ラチカ】<br/>「ほーほーほー！」",0,3],
["【ジェド】<br/>「違うぞ『HO-HO-HO』だ！</br>　ちゃんとアルファベットで発音しろ！（？）」",2,3],
["【ラチカ】<br/>「あのー、せんせぇ」",2,1],
["【ジェド】<br/>「どうした、ラチカ」",0,1],
["【ラチカ】<br/>「これって……必要なくだりですかね？」",0,1],
["【ジェド】<br/>「ああ……。大いに、必要なくだりだ」",6,1],
["【ジェド】<br/>「昔から、『サンタ・クロース』の鳴き声（？）といえば<br/>　『HO-HO-HO！』と相場が決まっている」",6,1],
["【ジェド】<br/>「この発声できなくして、お前は一人前の<br/>　『サンタ・クロース』にはなれんのだぞ、ラチカ！」",2,1],
["【ラチカ】<br/>「う、うにゅぅ……」",5,1],
["【ジェド】<br/>「いいか。これは、お前が萌えキャラであるために<br/>　『うにゅぅ』などと鳴くのと、同じくらい<br/>　重要なことなのである（大真面目に）」",6,1],
["【ラチカ】<br/>「うにゅぅ……わかりましたぁ（？）」",5,1],
["【ジェド】<br/>「とまあ、これまでは、このように<br/>　意味のない授業を繰り広げてきた訳だが」<br/>【ラチカ】<br/>「やっぱり意味なかったのかよ……（笑）」",6,1],
["【ジェド】<br/>「明日からは、いよいよ実習を行う」",0,1],
["【ラチカ】<br/>「はあ。実習、ですか」",0,4],
["【ジェド】<br/>「そうだ。今年のクリスマスは、この偉大なる<br/>　1級サンタ ジェド様の元で1日使いパシｒ…<br/>　実際に、世界中の子どもたちへプレゼントを配ってもらう」",1,4],
["【ラチカ】<br/>「へえ〜☆」<br/>【ジェド】<br/>「わりと重大な発表なのに超ひとごと！？」",4,0],
["【ジェド】<br/>「なお、この実習はプロサンタ試験の一貫であるからして、<br/>　真面目にやらなければお前は一生アマチュアサンタで、<br/>　ニートで、二流の萌えキャラで、<br/>　そして、社会から忘れ去られてしまうのが関の山だ」",0,0],
["【ラチカ】<br/>「うにゅにゅうう……世の中甘くないよぉ！」",5,1],
["【ジェド】<br/>「まあ心配するな。サンタ界のファイナル・ウェポンと呼ばれた<br/>　このジェド様が、マンツーマンで指導してやるのだからな」",1,1],
["【ラチカ】<br/>「さすがです！ジェド先生！」",1,0],
["【ジェド】<br/>「シビれるだろう？　って、大丈夫？このネタ」",1,0],
["【ジェド】<br/>「さて、連絡は以上だ。何か質問はあるか？」",0,2],
["【ラチカ】<br/>「あ、せんせぇ。ずっと疑問だったんですけど、」",5,4],
["【ラチカ】<br/>「どうして冬場が稼ぎ時のサンタなのに、<br/>　制服がヘソ出しなんですか〜？」",5,2],
["【ジェド】<br/>「それはな、ラチカ……」",6,2],
["【ジェド】<br/>「………………」",6,2],
["【ラチカ】<br/>「………………」",6,2],
["【ジェド】<br/>「………………………」",6,2],
["【ラチカ】<br/>「………………………」",6,2],
["【ジェド】<br/>「学園長の、趣味だ（きっぱり）」",0,2],
["【ラチカ】<br/>「うにゅう…」",0,2],
["【ラチカ】<br/>「端的に言って、寒い。」<br/>【ジェド】<br/>「わかる（？）」",5,2],
["【ジェド】<br/>「ちなみに、サンタの乗るソリはとてつもなく高級なため、<br/>　かわいそうな貧乏ヘソ出し実習生は、<br/>　直接トナカイにつかまって飛行してもらう」",0,2],
["【ラチカ】<br/>「うにゅう……そこはかとなく危険だよぉ……」",0,1],
["【ラチカ】<br/>「でも、先生の隣になんかそれこそ乗りたくないし」<br/>【ジェド】<br/>「ですよねぇーっ☆（白目）」",3,2],
["【ジェド】<br/>「というわけだ。お前の準備が整ったら、今晩すぐに出発するぞ」",0,2],
["【ラチカ】<br/>「らじゃ〜☆」",0,0],
["storyEnd",0,0]
];


window.onload = function() {
	var game = new Game(800, 600);	// ゲーム画面を640×480で作る。Gameはゲーム全体の処理（メインループやシーン遷移）を管理するクラス。
	game.fps = 30;									// FPSを30に設定。パッケージのサンプルではデフォルトで24
	game.score = 0;								// スコア用の変数を定義
	game.keybind(90, 'a');						// AボタンをZキーに設定(今回は不使用)
	game.keybind(32, 'space');				// spaceキーを設定
	// ゲーム中使用する画像をあらかじめ読み込んでおく
	game.preload('img/n_yes.png','img/title_ui.png', 'img/title_btn.png','img/title.jpg','img/n_no.png', 'img/bg.jpg', 'img/jed.png', 'img/ratica.png','img/guide1.png','img/guide2.png', 'img/game_ui.png', 'img/msg_ui.png', 'img/game_bg.jpg', 'img/g_ratica.png','img/g_rud.png','img/g_bag.png','img/g_jed.png','img/ready.png','se1.wav', 'se2.wav','img/result.jpg','img/gohobi.jpg','img/result_ui.png','img/result_btn.png','img/present.png','img/love.png','img/stage1.png');

	var LAYER_BG = 0;							//背景レイヤ
	var LAYER_CHARA = 1;						//キャラレイヤ
	var LAYER_FRAME = 2;						//フレームレイヤ
	var LAYER_MSG = 3;							//メッセージレイヤ
	msgClick = 0;									//メッセージ送り用変数
	rePlay = 0;

	//ここから処理を書いていく！
	game.onload = function() {
		
		var titleScene = new Scene();		//タイトル画面を用意
		var storyScene = new Scene();		//ストーリー画面を用意
		var guideScene = new Scene();		//チュートリアル（ガイド）画面を用意
		var gameScene = new Scene();		//ゲームのメイン画面を用意
		var gameoverScene = new Scene();	//ジェドが突き落とす画面用
		var scoreScene = new Scene();		//プレイ後のスコア画面を用意
		var startTime = 0;							//もろもろ表示前の一時停止用

	//タイトル画面の中身
	
		//背景レイヤ設置
		var bg0 = new Sprite(800, 600);
		bg0.x = -30;
		bg0.y = 40; 
		bg0._element.style.zIndex = LAYER_BG;
		bg0.image = game.assets['img/title.jpg'];
		titleScene.addChild(bg0);

		//フレームレイヤ設置
		var frame0 = new Sprite(800, 600);
		frame0._element.style.zIndex = LAYER_FRAME;
		frame0.image = game.assets['img/title_ui.png'];
		titleScene.addChild(frame0);
		frame0.addEventListener('touchstart', function() {		//クリックされたときの挙動
			msgClick += 1;
		});
		
		//ストーリーボタン設置
		var ssButton = new Sprite(250,95)
		ssButton.image = game.assets['img/title_btn.png']
		ssButton.x = 70;
		ssButton.y = 150;
		ssButton._element.style.zIndex = LAYER_MSG;
		ssButton.addEventListener('touchstart', function() {		//クリックされたときの挙動
			game.replaceScene(storyScene);									//ストーリーシーンへ移動
		});
		titleScene.addChild(ssButton);										//ストーリーボタン表示
		
		//hou to設置
		var psButton = new Sprite(250,95)
		psButton.image = game.assets['img/title_btn.png']
		psButton.x = 70;
		psButton.y = 235;
		psButton.frame = 1;
		psButton._element.style.zIndex = LAYER_MSG;
		psButton.addEventListener('touchstart', function() {	//クリックされたときの挙動
			game.replaceScene(guideScene);
		});
		titleScene.addChild(psButton);									//ゲームスタートボタン表示
		
				
		//ゲームスタートボタン設置
		var gsButton = new Sprite(250,90)
		gsButton.image = game.assets['img/title_btn.png']
		gsButton.x = 60;
		gsButton.y = 310;
		gsButton.frame = 2;
		gsButton._element.style.zIndex = LAYER_MSG;
		gsButton.addEventListener('touchstart', function() {	//クリックされたときの挙動
			game.replaceScene(gameScene);
		});
		titleScene.addChild(gsButton);									//ゲームスタートボタン表示
			
		//雪なんか降らせてみる 
	    	var snow = new Array();
        	var snowNum = 30;
        	for (i=0; i < snowNum; i++){
        	var snowSpd = Math.floor(Math.random() * 4);
            var snow = new Label("＊");           
            snow.font = "25px 'Arial Black'";
			snow.color = "#ffffff"           
            snow._element.style.zIndex = LAYER_CHARA;
          	snow.x =  snowSpd +i * 60;
            snow.y = -60;
            snow.speed = snowSpd;
            snow.addEventListener('enterframe', function() {
                // 位置の更新
                var snowRnd = Math.floor(Math.random() * 2);
                this.x += this.speed * snowRnd;
                if (this.x > 800){
                	this.x = 0;
                }
                this.y += this.speed;
        	    if (this.y > 600) {
                    this.y = -60;
                }
            });
         	titleScene.addChild(snow);
         }
        
	//ストーリーモードの中身
		//背景レイヤ設置
		var bg1 = new Sprite(800, 600);
		bg1._element.style.zIndex = LAYER_BG;
		bg1.image = game.assets['img/bg.jpg'];
		storyScene.addChild(bg1);

		//フレームレイヤ設置
		var frame1 = new Sprite(800, 600);
		frame1._element.style.zIndex = LAYER_FRAME;
		frame1.image = game.assets['img/msg_ui.png'];
		frame1.addEventListener('touchstart', function() {				//クリックされたときの挙動
			msgClick += 1;
		});
		storyScene.addChild(frame1);

		//メッセージ表示
		var msg = new Label(" ");
		msg.color = '#fff'; 
		msg.font = "16px 'sans-serif'";
		msg.x = 95;
		msg.y = 430;
		msg._element.style.zIndex = LAYER_MSG;
		msg.addEventListener('enterframe', function() {
			if (messages[msgClick][0] === "storyEnd"){
				msgClick = 0;
				game.replaceScene(titleScene);
			}
			msg.text = messages[msgClick][0];									//messagesのmsgClick番目の文章をとってくる
		/*	if (messages.length === msgClick){								//多次元配列はlengthをとってこれない
				msgClick = 0;
				game.replaceScene(titleScene);
		} */
		});
		storyScene.addChild(msg);												//メッセージ表示
				
		//ラチカ設置
		var ratica = new Sprite(395, 600);
		ratica.x = 400;
		ratica.y = 60;
		ratica._element.style.zIndex = LAYER_CHARA;
		ratica.image = game.assets['img/ratica.png'];
		ratica.frame = 2;																//表示する表情
		ratica.addEventListener('enterframe', function() {// 毎フレーム発生するイベントに使う関数を定義
				this.frame = messages[msgClick][2];
			});
		storyScene.addChild(ratica);
		
		//ジェド先生
		var jed = new Sprite(300, 650);
		jed.x = 40;
		jed.y = 40;
		jed._element.style.zIndex = LAYER_CHARA;
		jed.image = game.assets['img/jed.png'];
		jed.frame = 0;															//表示する表情
		jed.addEventListener('enterframe', function() {// 毎フレーム発生するイベントに使う関数を定義
	    	this.frame = messages[msgClick][1];
			});
		storyScene.addChild(jed);
		
		//タイトルボタン
		var titleBtn = new Sprite(135, 75);
		titleBtn.x = 610;
		titleBtn.y = 5;
		titleBtn._element.style.zIndex = LAYER_MSG;
		titleBtn.image = game.assets['img/result_btn.png'];
		titleBtn.frame = 1;
		titleBtn.addEventListener('touchstart', function() {	//クリックされたときの挙動
			msgClick = 0;
			game.replaceScene(titleScene);
		});
		storyScene.addChild(titleBtn);

//ゲーム画面の中身 ここから
		
	//ゲーム説明（guideScene)ここから
		
		 //フレームレイヤ設置
		var frame = new Sprite(800, 600);
		frame._element.style.zIndex = LAYER_FRAME;
		frame.image = game.assets['img/game_ui.png'];
		guideScene.addChild(frame);
		 
		 //背景の表示
			// スクロール背景１
		var gbA = new Sprite(800, 600);
		gbA.x = 0;
		gbA.y = 0;
		gbA._element.style.zIndex = LAYER_BG;
		gbA.image = game.assets["img/game_bg.jpg"];
		gbA.addEventListener('enterframe', function() {
			this.speed = 2;
			if(this.x >= game.width) {											//右はじまでいってきえたら
				this.x = gbB.x - this.width + 1;					//左はじ（画面外）にもっていく
			}
			this.x += this.speed;
		});
		
		// スクロール背景２
		var gbB = new Sprite(800, 600);
		gbB.x = gbB.width;								//初期位置をAとずらす（左はじから開始）
		gbB.y = 0;
		gbB._element.style.zIndex = LAYER_BG;
		gbB.image = game.assets["img/game_bg.jpg"];
		gbB.addEventListener('enterframe', function() {
			this.speed = 2;
			if(this.x >= game.width) {											//右はじまでいってきえたら
				this.x = gbA.x - this.width + 1;					//左はじ（画面外）にもっていく
			}
			this.x += this.speed;
		});
		guideScene.addChild(gbA);
		guideScene.addChild(gbB);
		 
		 //説明文
		var guide = new Sprite(521,350);
		gyonda = 0;
		guide.x = 120;
		guide.y = 90;
		guide._element.style.zIndex = LAYER_MSG;
		guide.image = game.assets['img/guide1.png'];
		guide.addEventListener('enterframe',function(){
			if(gyonda ===1){
				this.image = game.assets['img/guide2.png'];
			}else if(gyonda ===2){
				game.replaceScene(gameScene);
				gyonda = 0;
				this.image = game.assets['img/guide1.png'];
			}
		});
		guide.addEventListener('touchstart',function(){
			gyonda += 1;
		});
		guideScene.addChild(guide); 

//ゲーム本編ここから

		// スクロール背景１
		var backgroundA = new Sprite(800, 600);
		backgroundA.x = 0;
		backgroundA.y = 0;
		backgroundA._element.style.zIndex = LAYER_BG;
		backgroundA.image = game.assets["img/game_bg.jpg"];
		backgroundA.addEventListener('enterframe', function() {
			this.speed = 2;
			if(this.x >= game.width) {											//右はじまでいってきえたら
				this.x = backgroundB.x - this.width + 1;					//左はじ（画面外）にもっていく
			}
			this.x += this.speed;
		});
		
		// スクロール背景２
		var backgroundB = new Sprite(800, 600);
		backgroundB.x = backgroundB.width;								//初期位置をAとずらす（左はじから開始）
		backgroundB.y = 0;
		backgroundB._element.style.zIndex = LAYER_BG;
		backgroundB.image = game.assets["img/game_bg.jpg"];
		backgroundB.addEventListener('enterframe', function() {
			this.speed = 2;
			if(this.x >= game.width) {											//右はじまでいってきえたら
				this.x = backgroundA.x - this.width + 1;					//左はじ（画面外）にもっていく
			}
			this.x += this.speed;
		});
		gameScene.addChild(backgroundA);
		gameScene.addChild(backgroundB);

		//トナカイ設置
		var rudo = new Sprite(180, 137);
		rudo.x = 510;
		rudo.y = 270;
		rudo._element.style.zIndex = LAYER_CHARA;
		rudo.image = game.assets['img/g_rud.png'];
		rudoLimit = 0;					//表示する表情のための変数
		rudo.addEventListener('enterframe',function(){
				if (rudoLimit < 5){
	    			this.frame = 0;
	    			}else if (rudoLimit < 10) {
                	this.frame = 1;
         			 }
          	 rudoLimit = rudoLimit + 1;
            	if (rudoLimit === 35){
            	rudoLimit = 0;
            	}
	    	});
		gameScene.addChild(rudo);

		//ミニラチカ設置
		var mRatica = new Sprite(219, 221);
		mRatica.x = 500;
		mRatica.y = 180;
		mRatica._element.style.zIndex = LAYER_CHARA;
		mRatica.image = game.assets['img/g_ratica.png'];
		poseLimit = 0;					//表示する表情のための変数
		mRatica.addEventListener('enterframe',function(){
			if(startTime < 80){
	    		// ゲームが始まる前
	    		}else{
	    		// 始まったあと
	    			if (poseLimit < 5){
	    			this.frame = 0;
	    			}else if (poseLimit < 8) {
                   		this.frame = 1;
                	} else if (poseLimit < 30){
                   		this.frame = 2;
                	}
                poseLimit = poseLimit + 1;
            
            	if (poseLimit === 30){
            	poseLimit = 0;
            	}
            }
	    	});
		gameScene.addChild(mRatica);
		
		//袋設置
		var bag = new Sprite(124,115)
		bag.x = 600;
		bag.y = 270;
		bag.image = game.assets['img/g_bag.png']
		bag._element.style.zIndex = LAYER_CHARA;
		gameScene.addChild(bag);
		
		//ステージテーマ設置
		var stageTheme = new Sprite(508,89)
		stageTheme.x = -80;
		stageTheme.y = 320;
		stageTheme.image = game.assets['img/stage1.png']
		stageTheme._element.style.zIndex = LAYER_CHARA;
		gameScene.addChild(stageTheme);

		//フレームレイヤ設置
		var frame = new Sprite(800, 600);
		frame._element.style.zIndex = LAYER_FRAME;
		frame.image = game.assets['img/game_ui.png'];
		gameScene.addChild(frame);
		
		//are you ready?
		var auReady = new Sprite(592,68);
		auReady.image = game.assets['img/ready.png'];
		auReady.x = 90;
		auReady.y = 90;
		auReady._element.style.zIndex = LAYER_CHARA;
		auReady.addEventListener('enterframe',function(){
			if(startTime < 50){
				this.opacity = 1;
			}else{
				this.opacity = 0;
			}
		});
		gameScene.addChild(auReady);
		
		//ハート（正解マーク）設置
		var heart = new Sprite(115, 110);
		heart.x = 370;		// 表示位置を指定
		heart.y = 105;
		heart.image = game.assets['img/love.png'];
		heart._element.style.zIndex = LAYER_MSG;
		seikai = 0;			//正解かどうかの変数をセット
		heart.addEventListener('enterframe', function() {
		if(seikai ===1 ){
				this.opacity = 1;
			}else{
				this.opacity = 0;
				}
		});
		gameScene.addChild(heart);
				
		//プレゼント画像設置
		var present = new Sprite(196, 174);
		present._element.style.zIndex = LAYER_CHARA;
		present.x = 340;		// 表示位置を指定
		present.y = 70;
		limit = 0;					//画像を切り替えるタイマー
		kubaru = 0;

			//タイマー0のとき必ず正解か不正解の画像をランダムで選ぶ
			//30fr以内にボタンをおしたかおさないか。ボタンをおされたとき正解だったか不正解だったかで分岐。
	    present.addEventListener('enterframe', function() {// 毎フレーム発生するイベントに使う関数を定義
	   /* 	if (rePlay === 1){
	    	limit = 0;
	    	rePlay = 0;	
	    	};
	    	*/
	    	
	    	startTime = startTime + 1;
	    	if(startTime < 80){
	 //   	if(game.frame < startTime + 80){
	    		// ゲームが始まる前80フレーム停止   		
	    	}else{
	    		// 始まったあと
				if(limit === 0) {
					var sound1 = game.assets['se1.wav'].clone();
					//cloneを入れると、サウンドオブジェクトの複製をしなくてすむ（このタグだけで何度も再生可に！）
					sound1.play();
					isYes = Math.floor(Math.random() * 4);
					//floorは()内の小数点以下を切り捨てる。Math.random()は0〜0.999...(1未満)の数がかえってくるので範囲を2倍して0〜1.999…（2未満)までかえるようにすると、切り捨てたら0か1が均一にかえる。
					//正解か不正解の画像をランダムで選ぶ
					if(isYes >= 1) {//この場合範囲が0,1,2,3,4で、そのうち1以上のとき正解＝4/5の確率で正解画像
						yesindex = Math.floor(Math.random() * 3);
						this.image = game.assets['img/n_yes.png'];
						// 表示に使う画像を設定
						this.frame = yesindex;
					} else {	　																		//0のとき、不正解画像（1/5の確率）
						noindex = Math.floor(Math.random() * 3);
						this.image = game.assets['img/n_no.png'];
						// 表示に使う画像を設定
						this.frame = noindex;
					}
				}

				//タイマーが30以下なら画像を表示、そうでなければ非表示
				
				if (limit < 28) {
					this.opacity = 1;
					//opacity…透明度
				} else {
					this.opacity = 0;
					if(kubaru === 0) {//タイマーが30〜35のとき、もし配るボタン（spaceキー）が押されていなかったら
						if(isYes >= 1) {//かつ、正解の画像だったら
							this.opacity = 0;
							game.replaceScene(gameoverScene);
							//リザルト画面に（ゲームオーバー）
						}
					}
				}

				//タイマーの更新を30まで続けて、30になったらリセット
				limit = limit + 1;
				//タイマーを1すすめる
				if(limit === 30) {
					kubaru = 0;							//ボタンが押されたかのフラグをリセット
					seikai = 0;							//正解したかどうかのフラグをリセット
					limit = 0;
				}
			}
		});

		//正解のときにスペースボタンが押されたらスコアに100足す
		game.addEventListener('spacebuttondown', function() {
			kubaru += 1;
			//スペースキーが押されて配ったか？
			if(kubaru === 1){
				if(isYes >= 1) {
					var sound2 = game.assets['se2.wav'].clone();
					//cloneを入れると、サウンドオブジェクトの複製をしなくてすむ（このタグだけで何度も再生可に！）
					sound2.play();
					seikai += 1;
					game.score += 100;
					} else {
					present.opacity = 0;	
					game.replaceScene(gameoverScene);
					}
			}
		});
		gameScene.addChild(present);
		// シーンにプレゼントを追加する。（しないと表示されないので注意）

		//プレゼントぶんなげるアニメ
		var pNage = new Sprite(92, 84);
		pNage.x = 450;		// 表示位置を指定
		pNage.y = 250;
		pNage.image = game.assets['img/present.png'];
		pNage._element.style.zIndex = LAYER_CHARA;
		seikai = 0;			//正解かどうかの変数をセット
		pNage.addEventListener('enterframe', function() {
		if(seikai ===1 ){
				if(limit < 28){
					this.opacity = 1;
					this.x -= 20;
					this.y += 10;
				}else{
					this.opacity = 0;
					this.x = 450;
					this.y = 250;
					}
			}else{
				this.opacity = 0;
				}
		});
		gameScene.addChild(pNage);
		
		//スコア設置
		var score = new Label();
		score._element.style.zIndex = LAYER_MSG;
		score.font = "32px 'Arial Black'";					// フォントの指定
		score.y = 524;
		score.x = 400;
		score._element.style.textAlign = "right";
		score.addEventListener('enterframe', function() {
			this.text = game.score;
		});
		gameScene.addChild(score);

//不正解時にふってくるジェドのシーン(gameoverScene)
		
		// 背景
		var goBg = new Sprite(800, 600);
		goBg._element.style.zIndex = LAYER_BG;
		goBg.image = game.assets["img/game_bg.jpg"];
		gameoverScene.addChild(goBg);

		//トナカイ設置
		var goRudo = new Sprite(180, 137);
		goRudo.x = 510;
		goRudo.y = 270;
		goRudo._element.style.zIndex = LAYER_CHARA;
		goRudo.image = game.assets['img/g_rud.png'];
		gameoverScene.addChild(goRudo);

		//ミニラチカ設置
		var goRatica = new Sprite(219, 221);
		goRatica.x = 500;
		goRatica.y = 180;
		goRatica._element.style.zIndex = LAYER_CHARA;
		goRatica.image = game.assets['img/g_ratica.png'];
		goRatica.addEventListener('enterframe', function() {
					this.y += 15;
					if(this.y > 1000){
						this.y = 180;
					}
		});
		gameoverScene.addChild(goRatica);
		
		//袋設置
		var goBag = new Sprite(124,115)
		goBag.x = 600;
		goBag.y = 270;
		goBag.image = game.assets['img/g_bag.png']
		goBag._element.style.zIndex = LAYER_CHARA;
		gameoverScene.addChild(goBag);

		//フレームレイヤ設置
		var goFrame = new Sprite(800, 600);
		goFrame._element.style.zIndex = LAYER_FRAME;
		goFrame.image = game.assets['img/game_ui.png'];
		gameoverScene.addChild(goFrame);

		//ジェドてんてー
		var mjed = new Sprite(201, 252);
		mjed.x = 550;		// 表示位置を指定
		mjed.y = -30;
		mjed.image = game.assets['img/g_jed.png'];
		mjed._element.style.zIndex = LAYER_CHARA;
		mjed.addEventListener('enterframe', function() {
					this.y += 20;
					if(this.y > 1000){
						game.replaceScene(scoreScene);
						this.y = -30;
					}
		});
		gameoverScene.addChild(mjed);

		
//リザルト画面
		
		//リザルト背景
		var rBg = new Sprite(800, 600);
		rBg.x = 20;
		rBg.y = 30;
		rBg._element.style.zIndex = LAYER_BG;
		rBg.image = game.assets['img/result.jpg'];
		scoreScene.addChild(rBg);	

		//フレームレイヤ設置
		var rframe = new Sprite(800, 600);
		rframe._element.style.zIndex = LAYER_FRAME;
		rframe.image = game.assets['img/result_ui.png'];
		scoreScene.addChild(rframe);
		
		//リプレイボタン
		var replayBtn = new Sprite(135, 75);
		replayBtn.x = 480;
		replayBtn.y = 510;
		replayBtn._element.style.zIndex = LAYER_MSG;
		replayBtn.image = game.assets['img/result_btn.png'];
		replayBtn.frame = 0;
		replayBtn.addEventListener('touchstart', function() {	//クリックされたときの挙動
			isYes = 0;
			game.score = 0;
			startTime = 0;
			rePlay = 1;
			game.replaceScene(gameScene);
		});
		scoreScene.addChild(replayBtn);
		
		//タイトルボタン
		var titleBtn2 = new Sprite(135, 75);
		titleBtn2.x = 610;
		titleBtn2.y = 515;
		titleBtn2._element.style.zIndex = LAYER_MSG;
		titleBtn2.image = game.assets['img/result_btn.png'];
		titleBtn2.frame = 1;
		titleBtn2.addEventListener('touchstart', function() {	//クリックされたときの挙動
			game.replaceScene(titleScene);
			isYes = 0;
			game.score = 0;
			startTime = 0;
		});
		scoreScene.addChild(titleBtn2);
		
		//給料（スコア）
		var finalScore = new Label(" ");
		finalScore.font = "28px 'Arial Black'";					// フォントの指定
		finalScore.x = 230;
		finalScore.y =226;
		finalScore._element.style.zIndex = LAYER_MSG;
		finalScore._element.style.textAlign = "left";
		finalScore.addEventListener('enterframe', function() {
			this.text = game.score + "円";
		});
		scoreScene.addChild(finalScore);			//最終スコア表示
		
		//ランク表示
		var rank = new Label(" ");
		rank.font = "28px 'Arial Black'";
		rank.x = 230;
		rank.y = 256;
		rank._element.style.zIndex = LAYER_MSG;
		rank._element.style.textAlign = "left";
		console.log(game.score);
		shogoLv = 0;					//称号分け用変数
		rank.addEventListener('enterframe', function() {
		if ((0 <= game.score ) &&  (game.score < 500)){
			rank.text = "D";
			shogoLv = 1;
		}else if  ((500 <= game.score ) &&  (game.score < 1000)){
			rank.text = "C";
			shogoLv = 2;
		}else if  ((1000 <= game.score ) &&  (game.score < 5000)){
			rank.text = "B";
			shogoLv = 3;
		}else if  ((5000 <= game.score ) &&  (game.score < 10000)){
			rank.text = "A";
			shogoLv = 4;
		}else if  ((10000 <= game.score ) &&  (game.score <= 100000)){
			rank.text = "S";
			shogoLv = 5;
		}else if (game. score > 100000){
			rank.text = "SSS";
			shogoLv = 6;
		};
		});
		scoreScene.addChild(rank);
		
		//称号表示
		var shogo = new Label(" ");
		var gohobi = new Sprite(395,600);
		gohobi.x = 430;
		gohobi.y = 60;
		gohobi._element.style.zIndex = LAYER_CHARA;
		gohobi.image = game.assets['img/ratica.png'];
		gohobi.frame = 6;
		shogo.font = "20px 'Arial Black'";
		shogo._element.style.textAlign = "left";
		shogo.x = 230;
		shogo.y = 291;
		shogo._element.style.zIndex = LAYER_MSG;
		shogo.addEventListener('enterframe', function() {
		if (shogoLv === 1){
			shogo.text = "へたれ見習いサンタ";
			gohobi.x = 430;
			gohobi.frame = 1;
		}else if (shogoLv === 2){
			shogo.text = "お手伝いさん";
			gohobi.x = 430;
			gohobi.frame = 4;
		}else if  (shogoLv === 3){
			shogo.text = "期待の新人";
			gohobi.x = 400;
			gohobi.frame = 3;
		}else if  (shogoLv === 4){
			shogo.text = "サンタ試験 1級（ジェドよりすごい）";
			gohobi.x = 400;
			gohobi.frame = 0;
		}else if  (shogoLv === 5){
			shogo.text = "レジェンド・オブ・サンタ";
			gohobi.x = 400;
			gohobi.frame = 5;
		}else if (shogoLv === 6){
			shogo.text = "全てを超えし者（神）";
			gohobi.x = 400;
			gohobi.frame = 5;
		};
		});
		scoreScene.addChild(gohobi);
		scoreScene.addChild(shogo);

		
	/*	//クリアーCG
		var cCg = new Sprite(320, 600);
		cCg.x = 480;
		cCg.y = 40;
		cCg._element.style.zIndex = LAYER_CHARA;
		cCg.image = game.assets['img/gohobi.jpg'];
		scoreScene.addChild(cCg);
*/

		//タイトル画面を出す
		game.pushScene(titleScene);

	}
	game.start();
	// ゲーム起動
};
