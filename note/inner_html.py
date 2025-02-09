class Tag:

    def __init__(self, name, content=''):
        self.name = name
        self.content = content
        self.children = []

    def __call__(self, *args):
        self.children.extend(args)
        return self

    def __str__(self):
        inner_html = f"<{self.name}>{self.content + ''.join([str(child) for child in self.children])}</{self.name}>"
        return inner_html


def body(*args):
    return Tag('body')(*args)


def p(content):
    return Tag('p', content)


def div(*args):
    return Tag('div')(*args)


def myfunction(*args): 
    return ''.join([str(arg) for arg in args])


# Example usage
html = myfunction(
    body(
        div(
            p(
                'hello world'
            )
        ),
        div(
            p(
                'goodbye world'
            )
        )
    )
)

print(html)
