from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def api_root(request):
    return JsonResponse({
        'message': 'HackWestTX Class Portfolio API',
        'version': '2.0.0',
        'description': 'Comprehensive backend for Class Portfolio management system',
        'endpoints': {
            'health': '/api/health/',
            'auth': {
                'register': '/api/auth/register/',
                'login': '/api/auth/login/',
                'me': '/api/auth/me/'
            },
            'departments': {
                'list': '/api/departments/',
                'detail': '/api/departments/{id}/'
            },
            'professors': {
                'list': '/api/professors/',
                'detail': '/api/professors/{id}/'
            },
            'courses': {
                'list': '/api/courses/',
                'detail': '/api/courses/{id}/'
            },
            'portfolios': {
                'list': '/api/portfolios/',
                'detail': '/api/portfolios/{id}/',
                'search': '/api/portfolios/?search=query&department=code&professor=name'
            },
            'syllabi': {
                'upload': '/api/syllabi/',
                'detail': '/api/syllabi/{id}/'
            },
            'important_dates': {
                'list': '/api/important-dates/',
                'detail': '/api/important-dates/{id}/',
                'upcoming': '/api/upcoming-deadlines/'
            },
            'materials': {
                'list': '/api/materials/',
                'detail': '/api/materials/{id}/'
            },
            'flashcards': {
                'list': '/api/flashcards/',
                'detail': '/api/flashcards/{id}/'
            },
            'quizzes': {
                'list': '/api/quizzes/',
                'detail': '/api/quizzes/{id}/',
                'questions': '/api/quiz-questions/'
            },
            'grades': {
                'list': '/api/grades/',
                'detail': '/api/grades/{id}/',
                'analytics': '/api/portfolios/{id}/analytics/'
            },
            'reviews': {
                'list': '/api/reviews/',
                'detail': '/api/reviews/{id}/'
            },
            'study_groups': {
                'list': '/api/study-groups/',
                'detail': '/api/study-groups/{id}/',
                'join': '/api/study-groups/{id}/join/',
                'leave': '/api/study-groups/{id}/leave/'
            },
            'notifications': {
                'list': '/api/notifications/',
                'mark_read': '/api/notifications/{id}/read/'
            },
            'recommendations': {
                'list': '/api/recommendations/',
                'detail': '/api/recommendations/{id}/'
            },
            'users': {
                'profile': '/api/users/profile/{id}/',
                'search': '/api/users/search/?q=query'
            },
            'posts': {
                'list': '/api/posts/',
                'detail': '/api/posts/{id}/',
                'like': '/api/posts/{id}/like/',
                'comment': '/api/posts/{id}/comments/'
            },
            'admin': '/admin/'
        },
        'features': [
            'Smart Syllabus Scanner with date extraction',
            'Interactive Learning Space with flashcards and quizzes',
            'Class Performance Tracker with grade analytics',
            'End-of-Class Review & Archive system',
            'Marketplace & Sharing functionality',
            'Class Creation & Collaboration tools',
            'Community & Networking features',
            'Mobile-ready notifications system'
        ],
        'documentation': 'See README.md for detailed API documentation'
    })

urlpatterns = [
    path('', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]