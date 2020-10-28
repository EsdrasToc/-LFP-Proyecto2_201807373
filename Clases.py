class Token:
    token = ''
    content = ''
    description = ''
    line = 0
    column = 0
    
    def __init__(self, token, content, description, line, column):
        self.token = token
        self.content = content
        self.description = description
        self.line = line
        self.column = column