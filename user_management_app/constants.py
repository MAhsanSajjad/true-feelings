SOCIAL_PLATFORM_CHOICES = [
    ('facebook', 'Facebook'),
    ('google', 'Google'),
    ('apple', 'Apple'),
]


TRANSACTION_CHOICES = [
    ('deposit', 'Deposit'), 
    ('withdraw', 'Withdraw')
    ]



STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
]

USER_TYPE_CHOICES = [
    ('user', 'User'),
    ('admin', 'Admin'),
    ('representative', 'Representative'),
]

GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
]

SALARY_TYPPE_CHOICES = [
    ('weekly', 'Weekly'),
    ('monthly', 'Monthly'),
]

SERVICE_CHOICES = [
        ('standard', 'Standard'),
        ('advance', 'Advance'),
    ]

DURATION_CHOICES = [
        (10, '10 Min'),
        (30, '30 Min'),
        (60, '60 Min'),
    ]

STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]