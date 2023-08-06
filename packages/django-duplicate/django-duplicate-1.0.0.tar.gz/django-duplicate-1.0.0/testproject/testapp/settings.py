
SECRET_KEY = 'dummy'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.sessions',
    'testapp',
    'duplicate',
]

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)
MIDDLEWARE = MIDDLEWARE_CLASSES

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

MEDIA_ROOT = '/tmp/django_duplicate/'

MEDIA_PATH = '/media/'

ROOT_URLCONF = 'testapp.urls'

DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': TEMPLATE_DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DJANGO_DUPLICATE_KNOWN_RELATIONS = {
    "duplicate.Author": [
        "book_set",
    ],
    "duplicate.Book": [
        "author",
        "library_set",
    ],
    "duplicate.Building": [
        "building_set",
        "library",
        "nearest_libraries",
        "previous_building",
    ],
    "duplicate.Cart": [
        "client_set",
        "prioritycart",
        "products",
    ],
    "duplicate.Child": [
        "childforparent_set",
        "parent_set",
    ],
    "duplicate.ChildForParent": [
        "child",
        "parent",
    ],
    "duplicate.Client": [
        "cart",
    ],
    "duplicate.Document": [],
    "duplicate.Library": [
        "books",
        "building_set",
        "nearest_building",
    ],
    "duplicate.Library_books": [
        "book",
        "library",
    ],
    "duplicate.Parent": [
        "children",
    ],
    "duplicate.PriorityCart": [
        "cart_ptr",
        "client_set",
        "products",
    ],
    "duplicate.Product": [
        "cart_set",
        "productincart_set",
    ],
    "duplicate.ProductInCart": [
        "cart",
        "product",
    ],
}
