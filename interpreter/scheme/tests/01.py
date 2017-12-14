test = {
  'name': 'Question 1',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> read_line('3')
          3
          >>> read_line('-123')
          -123
          >>> read_line('1.25')
          1.25
          >>> read_line('true')
          True
          >>> read_line('(a)')
          Pair('a', nil)
          >>> read_line(')')
          SyntaxError
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> read_line(" (quote x) ")
          Pair('quote', Pair('x', nil))
          >>> read_line(" 'x ")
          520174e039ae892fc519beaf52ddc316
          # locked
          # choice: Pair('x', nil)
          # choice: 'x'
          # choice: Pair('quote', 'x')
          # choice: Pair('quote', Pair('x', nil))
          >>> read_line(" (a b) ")
          39ef3dd781f503a70c687f6ed274971b
          # locked
          # choice: Pair('a', Pair('b', nil))
          # choice: Pair('quote', Pair(Pair('a', Pair('b', nil)), nil))
          # choice: Pair('quote', Pair('a', 'b'))
          # choice: Pair('quote', Pair('a', Pair('b', nil)))
          >>> read_line(" '(a b) ")
          9f8f2f44d05a3e1e92f6ebe88eb55479
          # locked
          # choice: Pair('a', Pair('b', nil))
          # choice: Pair('quote', Pair(Pair('a', Pair('b', nil)), nil))
          # choice: Pair('quote', Pair('a', 'b'))
          # choice: Pair('quote', Pair('a', Pair('b', nil)))
          >>> read_line(" '((a)) ")
          2b6ce7bcc8ad55f7432341e9d3e017f5
          # locked
          # choice: Pair('quote', Pair(Pair('a', nil), nil))
          # choice: Pair('quote', Pair(Pair('a', nil), nil), nil)
          # choice: Pair('quote', Pair(Pair('a'), nil))
          # choice: Pair('quote', Pair(Pair('a'), nil), nil)
          # choice: Pair('quote', Pair(Pair(Pair('a', nil), nil), nil))
          """,
          'hidden': False,
          'locked': True
        },
        {
          'code': r"""
          >>> read_line("(a (b 'c))")
          Pair('a', Pair(Pair('b', Pair(Pair('quote', Pair('c', nil)), nil)), nil))
          >>> read_line("(a (b '(c d)))")
          Pair('a', Pair(Pair('b', Pair(Pair('quote', Pair(Pair('c', Pair('d', nil)), nil)), nil)), nil))
          >>> read_line("')")
          SyntaxError
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from scheme_reader import *
      """,
      'teardown': '',
      'type': 'doctest'
    }
  ]
}