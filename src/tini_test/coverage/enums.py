from enum import Enum


class LineCoverageStatus(Enum):
    EMPTY    = 'EMPTY'
    RUN      = 'RUN'
    MISSING  = 'MISSING'
    EXCLUDED = 'EXCLUDED'

    def __str__(self) -> str:
        return self.value.lower()


class HTMLNodeType(Enum):
    ROOT    = '<html>%s</html>'
    HEAD    = '<head>%s</head>'
    BODY    = '<body>%s</body>'

    LINK    = '<link %s> %s' #!

    DIV     = '<div %s>%s</div>'
    ARTICLE = '<article %s>%s</article>'
    SPAN    = '<span %s>%s</span>'
    BUTTON  = '<button %s>%s</button>'
    SCRIPT  = '<script %s>%s</script>'
    HREF    = '<a %s>%s</a>'

    UL      = '<ul %s>%s</ul>'
    LI      = '<li %s>%s</li>'

    TABLE   = '<table %s>%s</table>'
    TR      = '<tr %s>%s</tr>'
    TH      = '<th %s>%s</th>'
    TD      = '<td %s>%s</td>'

