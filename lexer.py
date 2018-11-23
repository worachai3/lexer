import sys

class Atomata:
    def __init__(self, zigma, move_set):
        self.zigma = zigma
        self.move_set = move_set
        self.cur_state = 'start'

    def step(self, char):
        move = [s for s in self.move_set if char in s[1] and self.cur_state == s[0]]
        if len(move) > 0:
            self.cur_state = move[0][2]
            return self.cur_state, move[0][3]
        else:
            self.cur_state = 'start'
            return self.cur_state, 'NOT FOUND'

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
        ('IDEN', zigma['Digit'], 'IDEN', None),
        ('IDEN', zigma['Operator'], 'LITERAL', 'IDEN'),
        ('IDEN', zigma['Whitespace'], 'start', 'IDEN'),
        ('IDEN', zigma['dot'], 'ERROR', 'IDEN'),

        ('ERROR', zigma['EOF'], 'EOF', 'ERROR'),
        ('ERROR', zigma['Letter'], 'IDEN', 'ERROR'),
        ('ERROR', zigma['Digit'], 'IDEN', 'ERROR'),
        ('ERROR', zigma['Operator'], 'LITERAL', 'ERROR'),
        ('ERROR', zigma['Whitespace'], 'start', 'ERROR'),
        ('ERROR', zigma['dot'], 'ERROR', 'ERROR'),

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

    def __init__(self, inp):
        self.fa = Atomata(self.zigma, self.states)
        self.inp = inp + '\0'

    def one_step(self, char):
        return self.fa.step(char)

    def split_word(self):
        word = ''
        res = []
        cur_state = 'start'
        prev_state = 'start'
        for c in self.inp:
            cur_state, output = self.fa.step(c)
            if output == 'NOT FOUND' and prev_state == 'start':
                res.append(['ERROR', c])
            elif output == 'NOT FOUND' and prev_state != 'start':
                res.append([prev_state, word])
                res.append(['ERROR', c])
                word = ''
            elif output == None:
                if c not in self.zigma['Whitespace']:
                    word += c
            else:
                res.append([output, word])
                if c not in self.zigma['Whitespace']:
                    word = c
                else:
                    word = ''
            prev_state = cur_state
        return res

if __name__=='__main__':
    inp = ''.join(sys.stdin.readlines())
    lexer = Lexer(inp)
    res = lexer.split_word()
    for r in res:
        print('{}\t{}'.format(r[0], r[1]))
