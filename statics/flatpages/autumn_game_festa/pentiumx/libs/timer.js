enchant();
(function(){
  enchant.Timer = Class.create(EventTarget, {
    initialize: function(max){
      this.set(max);
    },
    set:function(max){
      this.max = max;
      this.now = 0;
      this.active = false;
      this.loop = false;
    },
    play:function(){
      this.active = true;
    },
    stop:function(){
      this.active = false;
      this.now = 0;
    },
    reset:function(){
      this.now = 0;
    },
    pause:function(){
      this.active = false;
    },
    isOver:function(){
      return this.now >= this.max;
    },
    count:function(){
      if(this.active && !this.isOver()){
        ++this.now;
      }
    },
    tick:function(){
      this.count();
      if(this.isOver()){
        if(this.loop){
          this.reset()
        }
      }
    }
  });
})();
