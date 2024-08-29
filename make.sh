# Building icon
mkdir icon.iconset
cp icon-assets/Icon-MacOS-16x16@1x.png icon.iconset/icon_16x16.png
cp icon-assets/Icon-MacOS-16x16@2x.png icon.iconset/icon_16x16@2x.png
cp icon-assets/Icon-MacOS-32x32@1x.png icon.iconset/icon_32x32.png
cp icon-assets/Icon-MacOS-32x32@2x.png icon.iconset/icon_32x32@2x.png
cp icon-assets/Icon-MacOS-128x128@1x.png icon.iconset/icon_128x128.png
cp icon-assets/Icon-MacOS-128x128@2x.png icon.iconset/icon_128x128@2x.png
cp icon-assets/Icon-MacOS-256x256@1x.png icon.iconset/icon_256x256.png
cp icon-assets/Icon-MacOS-256x256@2x.png icon.iconset/icon_256x256@2x.png
cp icon-assets/Icon-MacOS-512x512@1x.png icon.iconset/icon_512x512.png
cp icon-assets/Icon-MacOS-512x512@2x.png icon.iconset/icon_512x512@2x.png
iconutil -c icns icon.iconset
rm -R icon.iconset
# Build the app
pyinstaller \
    -w -F \
    --name "Bing Wallpaper Transfer" \
    -i icon.icns \
    --target-arch universal2 \
    --osx-bundle-identifier "com.zanderp25.BingWallpaperTransfer" \
    main.py --noconfirm
