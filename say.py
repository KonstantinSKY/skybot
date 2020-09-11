

class Say(str):             # Class Say extends the class str, adding the ability to highlight with different colors
    color = {
        'Purple': '\033[95m',
        'Cyan': '\033[96m',
        'Blue': '\033[94m',
        'Green': '\033[92m',
        'Yellow': '\033[93m',
        'Red': '\033[91m'
    }
    style = {
        'Bold': '\033[1m',
        'Underline': '\033[4m',
    }
    styles_end = '\033[0m'

    def __init__(self, text):
        super().__init__()
        self.text = text
        self.default_color = ''
        self. default_style = ''

    def prn(self, **options):
        color = self.default_color
        style = self.default_style
        color_key = options.get("color")
        style_key = options.get("style")
        styles_end = ''
        if color_key:
            color = Say.color[color_key]
        if style_key:
            style = Say.style[style_key]
        styles = f'{color}{style}'
        if styles:
            styles_end = Say.styles_end
        print(f'{styles}{self.text}{styles_end}')

    def prn_ok(self, **options):
        self.default_color = Say.color["Green"]
        self.prn(**options)

    def prn_err(self, **options):
        self.default_color = Say.color["Red"]
        self.prn(**options)

