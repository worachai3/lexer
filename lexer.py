import sys

class Atomata:
    def __init__(self, zigma, move_set, debug=False):
        self.zigma = zigma
        self.move_set = move_set
        self.cur_state = 'start'
        self.debug = debug

    def step(self, char):
        move = [s for s in self.move_set if char in s[1] and self.cur_state == s[0]]
        if self.debug:
            if len(move) > 0:
                print('current state: {} input: {} next state: {} output: {}'.format(move[0][0], char, move[0][2], [move[0][3]]))
        if len(move) > 0:
            self.cur_state = move[0][2]
            return move[0][3]
        else:
            self.cur_state = 'start'
            return 'ERROR'

class Lexer:
    zigma = {
        'Letter': 'abcdefghijklmnopqrstuvwxyz',
        'Digit': '1234567890',
        'Operator': '+-*/()',
        'Whitespace': '\n\t\r ',
        'dot': '.',
        'EOF': '\0'
    }

    states = [
    # (current_state, input, next_state, output)
        ('start', zigma['EOF'], 'EOF', None),
        ('start', zigma['Letter'], 'IDEN', None),
        ('start', zigma['Digit'], 'CONST', None),
        ('start', zigma['Operator'], 'LITERAL', None),
        ('start', zigma['Whitespace'], 'start', None),
        ('start', zigma['dot'], 'start', 'ERROR'),

        ('IDEN', zigma['EOF'], 'EOF', 'IDEN'),
        ('IDEN', zigma['Letter'], 'IDEN', None),
        ('IDEN', zigma['Digit'], 'CONST', 'IDEN'),
        ('IDEN', zigma['Operator'], 'LITERAL', 'IDEN'),
        ('IDEN', zigma['Whitespace'], 'start', 'IDEN'),
        ('IDEN', zigma['dot'], 'start', 'IDEN'),

        ('CONST', zigma['EOF'], 'EOF', 'CONST'),
        ('CONST', zigma['Letter'], 'IDEN', 'CONST'),
        ('CONST', zigma['Digit'], 'CONST', None),
        ('CONST', zigma['Operator'], 'LITERAL', 'CONST'),
        ('CONST', zigma['Whitespace'], 'start', 'CONST'),
        ('CONST', zigma['dot'], 'CONST_DOT', None),

        ('CONST_DOT', zigma['EOF'], 'EOF', 'ERROR'),
        ('CONST_DOT', zigma['Letter'], 'IDEN', 'ERROR'),
        ('CONST_DOT', zigma['Digit'], 'CONST', None),
        ('CONST_DOT', zigma['Operator'], 'LITERAL', 'ERROR'),
        ('CONST_DOT', zigma['Whitespace'], 'start', 'ERROR'),
        ('CONST_DOT', zigma['dot'], 'start', 'ERROR'),

        ('LITERAL', zigma['EOF'], 'EOF', 'LITERAL'),
        ('LITERAL', zigma['Letter'], 'IDEN', 'LITERAL'),
        ('LITERAL', zigma['Digit'], 'CONST', 'LITERAL'),
        ('LITERAL', zigma['Operator'], 'LITERAL', 'LITERAL'),
        ('LITERAL', zigma['Whitespace'], 'start', 'LITERAL'),
        ('LITERAL', zigma['dot'], 'start', 'LITERAL')
    ]

    def __init__(self, inp, debug=False):
        self.fa = Atomata(self.zigma, self.states)
        self.debug = debug
        self.inp = inp + '\0'

    def one_step(self, char):
        return self.fa.step(char)

    def split_word(self):
        word = ''
        res = []
        current_state = 'start'
        for c in self.inp:
            output = self.one_step(c)
            if current_state == output:
                word += c
            if output != None:
                word = c
                res.append([output, word])

        return res

if __name__=='__main__':
    inp = ''.join(sys.stdin.readlines())
    lexer = Lexer(inp, True)
    res = lexer.split_word()
    for r in res:
        print('{} {}'.format(r[0], r[1]))
