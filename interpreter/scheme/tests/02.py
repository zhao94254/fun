test = {
  'name': 'Question 2',
  'points': 2,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> read_line("(a . b)")
          Pair('a', 'b')
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> read_line("(a b . c)")
          Pair('a', Pair('b', 'c'))
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
    },
    {
      'cases': [
        {
          'code': r"""
          >>> read_line("(a b . c d)")
          SyntaxError
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> read_line("(a . (b . (c . ())))")
          Pair('a', Pair('b', Pair('c', nil)))
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> read_line("(a . ((b . (c)))))")
          Pair('a', Pair(Pair('b', Pair('c', nil)), nil))
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> read_line("(. . 2)")
          SyntaxError
          >>> read_line("(2 . 3 4 . 5)")
          SyntaxError
          >>> read_line("(2 (3 . 4) 5)")
          Pair(2, Pair(Pair(3, 4), Pair(5, nil)))
          >>> read_line("(1 2")
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