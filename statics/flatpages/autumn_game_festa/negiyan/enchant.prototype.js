/*
 enchantの中でHTML要素として画面に表示される要素に対して、
 elementプロパティでelementを取り出せるようにする（？
 */
enchant.Entity.prototype.element = function(){
	return this._element;
};

enchant.Scene.prototype.element = function(){
	return this._element;
};

enchant.Surface.prototype.element = function(){
	return this._element;
};