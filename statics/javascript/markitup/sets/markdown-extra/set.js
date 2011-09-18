// -------------------------------------------------------------------
// markItUp!
// -------------------------------------------------------------------
// Copyright (C) 2008 Jay Salvat
// http://markitup.jaysalvat.com/
// -------------------------------------------------------------------
// MarkDown tags example
// http://en.wikipedia.org/wiki/Markdown
// http://daringfireball.net/projects/markdown/
// -------------------------------------------------------------------
// Feel free to add more tags
// -------------------------------------------------------------------
mySettings = {
	previewInWindow: 'width=800, height=600, resizable=yes, scrollbars=yes',
	previewParserPath:	'/preview/',
	onShiftEnter:		{keepDefault:false, openWith:'\n\n'},
	markupSet: [
		{name:'トップ見出し', key:'1', className:"h1", placeHolder:'ここにタイトルを入力してください', closeWith:function(markItUp) { return miu.markdownTitle(markItUp, '=') } },
		{name:'第二見出し', key:'2', className:"h2", placeHolder:'ここにタイトルを入力してください', closeWith:function(markItUp) { return miu.markdownTitle(markItUp, '-') } },
		{name:'第三見出し', key:'3', className:"h3", openWith:'### ', placeHolder:'ここにタイトルを入力してください' },
		{separator:'---------------' },		
		{name:'強い強調', key:'B', className:"strong", openWith:'**', closeWith:'**'},
		{name:'弱い強調', key:'I', className:"em", openWith:'_', closeWith:'_'},
		{separator:'---------------' },
		{name:'リスト', className:"list", openWith:'-   ' },
		{name:'番号リスト', className:"list-order", openWith:function(markItUp) {
			return markItUp.line+'.  ';
		}},
		{separator:'---------------' },
		{name:'画像リンク', key:'I', className:"image", replaceWith:'![[![Alt（画像が読めない場合に代わりに表示される文字列）を入力してください]!]]([![画像ファイルのURLを入力してください:!:http://]!] "[![Title（マウスホバー時に表示される文字列）を入力してください]!]")'},
		{name:'外部リンク', key:'L', className:"link", openWith:'[', closeWith:']([![リンクしたいURLを入力してください:!:http://]!] "[![Title（マウスホバー時に表示される文字列）を入力してください]!]")', placeHolder:'ここにテキストを入力してください' },
		{name:'添付', className:"attache"},
		{separator:'---------------'},	
		{name:'引用', className:"quote", openWith:'>   '},
		{name:'コードモード', className:"code", openWith:'~~~\n', closeWith:'\n~~~\n'},
		{name:'AAモード', className:"AA", openWith:'~~~.AA\n', closeWith:'\n~~~\n'},
		{separator:'---------------'},
		{name:'フルスクリーン', className:"fullscreen"},
		{name:'インデント機能を無効化', className:"disindentable"},
		{separator:'---------------'},
		{name:'プレビュー表示', className:"preview", call:'preview'}
	]
};
// mIu nameSpace to avoid conflict.
miu = {
	markdownTitle: function(markItUp, char) {
		heading = '';
		n = $.trim(markItUp.selection||markItUp.placeHolder).length;
		for(i = 0; i < n; i++) {
			heading += char;
		}
		return '\n'+heading;
	}
};