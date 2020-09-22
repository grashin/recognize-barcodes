import qrcode
# img = qrcode.make('babina #20')
# img.save('/Users/grashin/video_detection/babina_20.png')
qr = qrcode.QRCode(version = 1, box_size = 20, border = 10)
data = 'babina #32'
qr.add_data(data)
qr.make(fit = True)
img = qr.make_image(fill = 'black', back_color = 'white')
img.save('someqrcode.png')