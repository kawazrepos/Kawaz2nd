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
	previewParserPath:	'',
	onShiftEnter:		{keepDefault:false, openWith:'\n\n'},
	markupSet: [
		{name:'First Level Heading', key:'1', placeHolder:'ここにタイトルを入力してください', closeWith:function(markItUp) { return miu.markdownTitle(markItUp, '=') } },
		{name:'Second Level Heading', key:'2', placeHolder:'ここにタイトルを入力してください', closeWith:function(markItUp) { return miu.markdownTitle(markItUp, '-') } },
		{name:'Heading 3', key:'3', openWith:'### ', placeHolder:'ここにタイトルを入力してください' },
		{name:'Heading 4', key:'4', openWith:'#### ', placeHolder:'ここにタイトルを入力してください' },
		{name:'Heading 5', key:'5', openWith:'##### ', placeHolder:'ここにタイトルを入力してください' },
		{name:'Heading 6', key:'6', openWith:'###### ', placeHolder:'ここにタイトルを入力してください' },
		{separator:'---------------' },		
		{name:'Bold', key:'B', openWith:'**', closeWith:'**'},
		{name:'Italic', key:'I', openWith:'_', closeWith:'_'},
		{separator:'---------------' },
		{name:'Bulleted List', openWith:'- ' },
		{name:'Numeric List', openWith:function(markItUp) {
			return markItUp.line+'. ';
		}},
		{separator:'---------------' },
		{name:'Picture', key:'P', replaceWith:'![[![Alt（画像が読めない場合に代わりに表示される文字列）を入力してください]!]]([![画像ファイルのURLを入力してください:!:http://]!] "[![Title（マウスホバー時に表示される文字列）を入力してください]!]")'},
		{name:'Link', key:'L', openWith:'[', closeWith:']([![リンクしたいURLを入力してください:!:http://]!] "[![Title（マウスホバー時に表示される文字列）を入力してください]!]")', placeHolder:'ここにテキストを入力してください' },
		{separator:'---------------'},	
		{name:'Quotes', openWith:'> '},
		{name:'Code Block / Code', openWith:'~~~\n', closeWith:'\n~~~\n'},
		{separator:'---------------'},
		{name:'Preview', call:'preview', className:"preview"}
	]
}

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
}