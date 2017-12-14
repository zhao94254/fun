test = {
  'name': 'Question 20',
  'points': 2,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          scm> (analyze 1)
          7107157269a542fea41c45a208299f75
          # locked
          scm> (analyze 'a)
          89071e830e420b7da43a9a51f7a3f447
          # locked
          scm> (analyze '(+ 1 2))
          4e53a14d84c3aa6eb632f21334d56423
          # locked
          scm> (analyze '(let ((a 1)
          ....                 (b 2))
          ....                (+ a b)))
          e440e68fc0dd209e68f7173a9fa7d6a8
          # locked
          """,
          'hidden': False,
          'locked': True
        },
        {
          'code': r"""
          scm> '(quoted expressions remain the same)
          (quoted expressions remain the same)
          scm> (analyze '(quote (let ((a 1) (b 2)) (+ a b))))
          (quote (let ((a 1) (b 2)) (+ a b)))
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      scm> (load 'questions)
      """,
      'teardown': '',
      'type': 'scheme'
    },
    {
      'cases': [
        {
          'code': r"""
          scm> '(Lambda parameters not affected but body affected)
          (lambda parameters not affected but body affected)
          scm> (analyze '(lambda (let a b) (+ let a b)))
          (lambda (let a b) (+ let a b))
          scm> (analyze '(lambda (x) a (let ((a x)) a)))
          (lambda (x) a ((lambda (a) a) x))
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> (analyze '(let ((a (let ((a 2)) a))
          ....                 (b 2))
          ....                (+ a b)))
          ((lambda (a b) (+ a b)) ((lambda (a) a) 2) 2)
          scm> (analyze '(let ((a 1))
          ....                (let ((b a))
          ....                     b)))
          ((lambda (a) ((lambda (b) b) a)) 1)
          scm> (analyze '(+ 1 (let ((a 1)) a)))
          (+ 1 ((lambda (a) a) 1))
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      scm> (load 'questions)
      """,
      'teardown': '',
      'type': 'scheme'
    }
  ]
}