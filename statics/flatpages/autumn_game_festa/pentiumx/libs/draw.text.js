enchant.draw = { assets: ['font.png'] };
enchant.draw.Text = enchant.Class.create(enchant.Sprite, {
    initialize: function(posX, posY, txt) {
        var game = enchant.Game.instance;
        this.fontSize = 16;
        this.widthItemNum = 16;
        enchant.Sprite.call(this, this.fontSize*txt.length, this.fontSize);
        this.image = new Surface(this.fontSize*txt.length, this.fontSize);
        this.x = posX;
        this.y = posY;
        this.setText(txt);
    },
    setText: function(txt) {
        var i, x, y, wNum, charCode, charPos;
        var game = enchant.Game.instance;
        this._text = txt;
        for(i=0; i<txt.length; i++) {
            charCode = txt.charCodeAt(i);
            if (charCode >= 32 && charCode <= 127) {
                charPos = charCode - 32;
            } else {
                charPos = 0;
            }
            x = charPos % this.widthItemNum;
            y = Math.floor(charPos / this.widthItemNum);
            // drawImage(image, sx, sy, sw, sh, dx, dy, dw, dh)
            this.image.draw(game.assets['font.png'], 
                x*this.fontSize, y*this.fontSize, this.fontSize, this.fontSize,
                i*this.fontSize, 0, this.fontSize, this.fontSize);
        }
    },
    text: {
        get: function() {
            return this._text;
        },
        set: function() {
        }
    }
});
enchant.draw.MutableText = enchant.Class.create(enchant.Sprite, {
    initialize: function(posX, posY, width, txt) {
        var game = enchant.Game.instance;
        this.fontSize = 16;
        this.widthItemNum = 16;
        enchant.Sprite.call(this, width, this.fontSize);
        this.image = new Surface(width, this.fontSize);
        this.x = posX;
        this.y = posY;
        this.setText(txt);
    },
    setText: function(txt) {
        var i, x, y, wNum, charCode, charPos;
        var game = enchant.Game.instance;
        this._text = txt;
        this.image.context.clearRect(0, 0, this.width, this.height);
        for(i=0; i<txt.length; i++) {
            charCode = txt.charCodeAt(i);
            if (charCode >= 32 && charCode <= 127) {
                charPos = charCode - 32;
            } else {
                charPos = 0;
            }
            x = charPos % this.widthItemNum;
            y = Math.floor(charPos / this.widthItemNum);
            // drawImage(image, sx, sy, sw, sh, dx, dy, dw, dh)
            this.image.draw(game.assets['font.png'], 
                x*this.fontSize, y*this.fontSize, this.fontSize, this.fontSize,
                i*this.fontSize, 0, this.fontSize, this.fontSize);
        }
    },
    text: {
        get: function() {
            return this._text;
        },
        set: function(txt) {
            this.setText(txt);
        }
    },
});
