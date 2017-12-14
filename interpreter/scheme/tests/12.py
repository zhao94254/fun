test = {
  'name': 'Question 12',
  'points': 2,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          scm> (define (square x) (* x x))
          square
          scm> (square 21)
          441
          scm> (define square (lambda (x) (* x x)))
          square
          scm> (square (square 21))
          194481
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> ((lambda (x) (list x (list (quote quote) x))) (quote (lambda (x) (list x (list (quote quote) x)))))
          ((lambda (x) (list x (list (quote quote) x))) (quote (lambda (x) (list x (list (quote quote) x)))))
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': '',
      'teardown': '',
      'type': 'scheme'
    },
    {
      'cases': [
        {
          'code': r"""
          scm> (define (outer x y)
          ....   (define (inner z x)
          ....     (+ x (* y 2) (* z 3)))
          ....   (inner x 10))
          outer
          scm> (outer 1 2)
          17
          scm> (define (outer-func x y)
          ....   (define (inner z x)
          ....     (+ x (* y 2) (* z 3)))
          ....   inner)
          outer-func
          scm> ((outer-func 1 2) 1 10)
          17
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> (define square (lambda (x) (* x x)))
          square
          scm> (define (sum-of-squares x y) (+ (square x) (square y)))
          sum-of-squares
          scm> (sum-of-squares 3 4)
          25
          scm> (define double (lambda (x) (* 2 x)))
          double
          scm> (define compose (lambda (f g) (lambda (x) (f (g x)))))
          compose
          scm> (define apply-twice (lambda (f) (compose f f)))
          apply-twice
          scm> ((apply-twice double) 5)
          20
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