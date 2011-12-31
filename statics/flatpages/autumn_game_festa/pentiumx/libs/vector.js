enchant();
(function(){
  enchant.Vector = Class.create({
    initialize: function(x, y){
      this.set(x, y);
    },
    set:function(x, y){
      this.x = x;
      this.y = y;
    },
    add:function(v){
      this.x += v.x;
      this.y += v.y;
      return this;
    },
    sub:function(v){
      this.x -= v.x;
      this.y -= v.y;
      return this;
    },
    scale:function(n){
      this.x *= n;
      this.y *= n;
      return this;
    },
    div:function(n){
      if(n){
        this.x /= n;
        this.y /= n;
      }
      return this;
    },
    inner_product:function(v){
      return this.x * v.x + this.y * v.y;
    },
    length:function(){
      return Math.sqrt(this.x*this.x + this.y*this.y);
    },
    resize:function(n){
      if(this.length()){
        this.scale(n/this.length());
      }
      return this;
    },
    normalize:function(){
      return this.resize(1);
    },
    angle:function(){
      return (180*Math.atan2(this.y, this.x))/Math.PI;
    },
    rotate:function(deg){
      var rad = (deg * Math.PI)/180;
      var size = this.length();
      this.x = Math.sin(rad)*this.y + Math.cos(rad)*this.x;
      this.y = Math.cos(rad)*this.y - Math.sin(rad)*this.x;
      this.resize(size);
      return this;
    },
    clone:function(){
      return new Vector(this.x, this.y);
    },
    reverse:function(){
      this.x *= -1;
      this.y *= -1;
    }
  });
})();
