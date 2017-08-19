pyinstaller programme/theochrone.pyw ^
	--name theochrone64 ^
	--onedir ^
	--paths programme ^
	--paths programme/gui ^
	--hiddenimport PyQt5 ^
	--add-binary data;data ^
	--add-binary programme/i18n;i18n ^
	--add-binary programme/gui/icons;gui/icons ^
	--clean 
pyinstaller theochrone64.spec 
