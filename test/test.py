from PIL import ImageGrab


def is_green(rgb):
    """
    两次都做错,会进入释义界面,在固定位置会有一个绿点,以此判断
    判断给定的 RGB 值是否属于绿色。
    """
    r, g, b = rgb
    return g > r and g > b


screenshot = ImageGrab.grab()
rgb_color2 = screenshot.getpixel((98, 651))
print(rgb_color2)
