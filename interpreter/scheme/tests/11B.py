test = {
  'name': 'Question 11',
  'partner': 'B',
  'points': 2,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> check_formals(read_line('(a b c)'))
          >>> check_formals(read_line('(a b a)'))
          SchemeError
          >>> check_formals(read_line('(0 a)'))
          SchemeError
          >>> check_formals(read_line('(a b c 0)'))
          SchemeError
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from scheme import *
      >>> from scheme_reader import *
      """,
      'teardown': '',
      'type': 'doctest'
    },
    {
      'cases': [
        {
          'code': r"""
          scm> (lambda (x y z) x)
          (lambda (x y z) x)
          scm> (lambda (x1 x2 x3) (+ x1 x2 x3))
          (lambda (x1 x2 x3) (+ x1 x2 x3))
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> (lambda (0 y z) x)
          SchemeError
          scm> (lambda (x y nil) x)
          SchemeError
          scm> (lambda (x y (and z)) x)
          SchemeError
          scm> (lambda (x #t z) x)
          SchemeError
          scm> (lambda (h e l l o) 'world)
          SchemeError
          scm> (lambda (c s 6 1 a) 'yay)
          SchemeError
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': '',
      'teardown': '',
      'type': 'scheme'
    }
  ]
}