from django.urls import path
from . import views
from django.http import JsonResponse

def api_root(request):
    """API root endpoint"""
    return JsonResponse({
        'message': 'HackWestTX Class Portfolio API',
        'version': '2.0.0',
        'endpoints': {
            'auth': {
                'register': '/api/auth/register/',
                'login': '/api/auth/login/',
                'me': '/api/auth/me/'
            },
            'departments': '/api/departments/',
            'professors': '/api/professors/',
            'portfolios': '/api/portfolios/',
            'materials': '/api/materials/',
            'flashcards': '/api/flashcards/',
            'quizzes': '/api/quizzes/',
            'important-dates': '/api/important-dates/',
            'reviews': '/api/reviews/',
            'study-groups': '/api/study-groups/',
            'notifications': '/api/notifications/',
            'posts': '/api/posts/',
            'users': '/api/users/',
            'courses': '/api/courses/',
            'search': '/api/search/',
            'visitor': {
                'landing': '/api/visitor/landing/',
                'search': '/api/visitor/search/'
            }
        }
    })

urlpatterns = [
    # API Root
    path('', api_root, name='api-root'),
    # Search & Discovery
    path('search/', views.global_search, name='global-search'),
    path('search/autocomplete/', views.search_autocomplete, name='search-autocomplete'),
    path('search/suggestions/', views.search_suggestions, name='search-suggestions'),
    path('search/analytics/', views.search_analytics, name='search-analytics'),
    path('search/save/', views.save_search, name='save-search'),
    
    # Non-functional Requirements
    path('privacy-policy/', views.privacy_policy, name='privacy-policy'),
    path('dmca/takedown/', views.dmca_takedown_request, name='dmca-takedown'),
    path('security/status/', views.security_status, name='security-status'),
    path('performance/metrics/', views.performance_metrics, name='performance-metrics'),
    path('accessibility/features/', views.accessibility_features, name='accessibility-features'),
    path('analytics/user/', views.user_analytics, name='user-analytics'),
    path('audit/log/', views.audit_log, name='audit-log'),
    path('security/anti-scraping/', views.anti_scraping_protection, name='anti-scraping'),
    path('system/status/', views.system_status, name='system-status'),
    
    # Preview Rules & Content Restrictions
    path('portfolios/<int:portfolio_id>/preview-content/', views.portfolio_preview_content, name='portfolio-preview-content'),
    path('documents/<int:file_id>/preview/', views.document_preview, name='document-preview'),
    
    # Visitor Landing & Onboarding
    path('visitor/landing/', views.visitor_landing, name='visitor-landing'),
    path('visitor/search/', views.search_portfolios, name='search-portfolios'),
    path('visitor/portfolio/<int:portfolio_id>/preview/', views.portfolio_preview_simple, name='portfolio-preview'),
    
    # Onboarding & Creation Flow
    path('onboarding/status/', views.onboarding_status, name='onboarding-status'),
    path('portfolios/create-wizard/', views.create_portfolio_wizard, name='create-portfolio-wizard'),
    
    # Authentication
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login, name='login'),
    path('auth/me/', views.me, name='me'),
    path('auth/delete-account/', views.delete_user_account, name='delete-user-account'),
    
    # Password Reset
    path('auth/request-password-reset/', views.request_password_reset, name='request-password-reset'),
    path('auth/confirm-password-reset/', views.confirm_password_reset, name='confirm-password-reset'),
    
    # User Management (Admin only)
    path('admin/users/', views.list_users, name='list-users'),
    path('admin/users/<int:user_id>/role/', views.update_user_role, name='update-user-role'),
    path('admin/users/<int:user_id>/delete/', views.delete_user, name='delete-user'),
    
    # Health Check
    path('health/', views.health_check, name='health'),
    
    # Comprehensive Connection Verification
    path('verify-connections/', views.verify_all_connections, name='verify-connections'),
    
    # Debug Authentication
    path('debug-auth/', views.debug_auth, name='debug-auth'),
    
    # Departments
    path('departments/', views.DepartmentListCreateView.as_view(), name='department-list'),
    path('departments/<int:pk>/', views.DepartmentDetailView.as_view(), name='department-detail'),
    
    # Professors
    path('professors/', views.ProfessorListCreateView.as_view(), name='professor-list'),
    path('professors/<int:pk>/', views.ProfessorDetailView.as_view(), name='professor-detail'),
    
    
    # Class Portfolios
    path('portfolios/', views.PortfolioListCreateView.as_view(), name='portfolio-list'),
    path('portfolios/user/', views.user_portfolios, name='user-portfolios'),
    path('portfolios/public/', views.public_portfolios, name='public-portfolios'),
    path('portfolios/<int:portfolio_id>/update/', views.update_portfolio, name='update-portfolio'),
    path('portfolios/<int:pk>/', views.PortfolioDetailView.as_view(), name='portfolio-detail'),
    
    # Marketplace
    path('marketplace/', views.MarketplaceListingListCreateView.as_view(), name='marketplace-list'),
    path('marketplace/<int:pk>/', views.MarketplaceListingDetailView.as_view(), name='marketplace-detail'),
    path('marketplace/<int:listing_id>/purchase/', views.purchase_portfolio, name='purchase-portfolio'),
    path('purchases/', views.user_purchases, name='user-purchases'),
    
    # Syllabus
    path('syllabi/', views.SyllabusUploadView.as_view(), name='syllabus-upload'),
    path('syllabi/<int:pk>/', views.SyllabusDetailView.as_view(), name='syllabus-detail'),
    path('syllabi/<int:syllabus_id>/extract/', views.extract_syllabus, name='extract-syllabus'),
    path('syllabi/<int:syllabus_id>/extraction/', views.SyllabusExtractionView.as_view(), name='syllabus-extraction'),
    path('syllabi/<int:syllabus_id>/create-dates/', views.create_important_dates_from_extraction, name='create-dates-from-extraction'),
    
    # Page-Level Endpoints
    path('portfolios/<int:portfolio_id>/syllabus-page/', views.syllabus_page_data, name='syllabus-page'),
    path('portfolios/<int:portfolio_id>/sync-calendar/', views.sync_to_calendar, name='sync-calendar'),
    path('portfolios/<int:portfolio_id>/learning-space/', views.learning_space_page_data, name='learning-space'),
    path('portfolios/<int:portfolio_id>/generate-content/', views.generate_learning_content, name='generate-content'),
    path('portfolios/<int:portfolio_id>/performance-tracker/', views.performance_tracker_page_data, name='performance-tracker'),
    path('portfolios/<int:portfolio_id>/what-if-scenario/', views.calculate_what_if_scenario, name='what-if-scenario'),
    
    # Important Dates
    path('important-dates/', views.ImportantDateListCreateView.as_view(), name='important-date-list'),
    path('important-dates/<int:pk>/', views.ImportantDateDetailView.as_view(), name='important-date-detail'),
    path('upcoming-deadlines/', views.upcoming_deadlines, name='upcoming-deadlines'),
    
    # Lecture Materials
    path('materials/', views.LectureMaterialListCreateView.as_view(), name='material-list'),
    path('materials/<int:pk>/', views.LectureMaterialDetailView.as_view(), name='material-detail'),
    
    # Flashcards
    path('flashcards/', views.FlashcardListCreateView.as_view(), name='flashcard-list'),
    path('flashcards/<int:pk>/', views.FlashcardDetailView.as_view(), name='flashcard-detail'),
    
    # Quizzes
    path('quizzes/', views.QuizListCreateView.as_view(), name='quiz-list'),
    path('quizzes/<int:pk>/', views.QuizDetailView.as_view(), name='quiz-detail'),
    path('quiz-questions/', views.QuizQuestionListCreateView.as_view(), name='quiz-question-list'),
    path('quiz-questions/<int:pk>/', views.QuizQuestionDetailView.as_view(), name='quiz-question-detail'),
    
    # Quiz Submissions
    path('quiz-submissions/', views.QuizSubmissionListCreateView.as_view(), name='quiz-submission-list'),
    path('quiz-submissions/<int:pk>/', views.QuizSubmissionDetailView.as_view(), name='quiz-submission-detail'),
    path('quizzes/<int:quiz_id>/submit/', views.submit_quiz, name='submit-quiz'),
    path('quizzes/<int:quiz_id>/results/', views.quiz_results, name='quiz-results'),
    
    # Grades (now part of portfolios)
    path('portfolios/<int:portfolio_id>/analytics/', views.grade_analytics, name='grade-analytics'),
    path('portfolios/<int:portfolio_id>/add-grade/', views.add_grade, name='add-grade'),
    path('portfolios/<int:portfolio_id>/update-breakdown/', views.update_grade_breakdown, name='update-grade-breakdown'),
    
    # Class Reviews
    path('reviews/', views.ClassReviewListCreateView.as_view(), name='review-list'),
    path('reviews/<int:pk>/', views.ClassReviewDetailView.as_view(), name='review-detail'),
    
    # Study Groups
    path('study-groups/', views.StudyGroupListCreateView.as_view(), name='study-group-list'),
    path('study-groups/<int:pk>/', views.StudyGroupDetailView.as_view(), name='study-group-detail'),
    path('study-groups/<int:group_id>/join/', views.join_study_group, name='join-study-group'),
    path('study-groups/<int:group_id>/leave/', views.leave_study_group, name='leave-study-group'),
    
    # Notifications
    path('notifications/', views.NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark-notification-read'),
    
    # Resource Recommendations
    path('recommendations/', views.ResourceRecommendationListCreateView.as_view(), name='recommendation-list'),
    path('recommendations/<int:pk>/', views.ResourceRecommendationDetailView.as_view(), name='recommendation-detail'),
    
    # Users (existing)
    path('users/', views.list_users, name='user-list'),
    path('users/profile/<int:pk>/', views.UserProfileView.as_view(), name='user-profile'),
    path('users/search/', views.UserSearchView.as_view(), name='user-search'),
    
    # Courses (placeholder - add actual course endpoints if needed)
    path('courses/', views.DepartmentListCreateView.as_view(), name='course-list'),  # Using departments as courses for now
    
    # Posts (existing)
    path('posts/', views.PostListCreateView.as_view(), name='post-list'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:post_id>/like/', views.like_post, name='like-post'),
    path('posts/<int:post_id>/comments/', views.comment_post, name='comment-post'),
    
    # File Processing
    path('files/', views.ProcessedFileListCreateView.as_view(), name='processed-file-list'),
    path('files/<int:pk>/', views.ProcessedFileDetailView.as_view(), name='processed-file-detail'),
    path('files/upload/', views.upload_and_process_file, name='upload-and-process-file'),
    path('files/<int:file_id>/reprocess/', views.reprocess_file, name='reprocess-file'),
    
    # Documents
    path('documents/', views.DocumentListCreateView.as_view(), name='document-list'),
    path('documents/user/', views.user_documents, name='user-documents'),
    path('documents/create/', views.create_document, name='create-document'),
    path('documents/<int:pk>/', views.DocumentDetailView.as_view(), name='document-detail'),
    path('documents/<int:document_id>/processing/', views.update_document_processing, name='update-document-processing'),
    path('documents/analytics/', views.document_analytics, name='document-analytics'),
    
    # Document Quizzes
    path('quizzes/', views.DocumentQuizListCreateView.as_view(), name='document-quiz-list'),
    path('quizzes/user/', views.user_document_quizzes, name='user-document-quizzes'),
    path('quizzes/create/', views.create_document_quiz, name='create-document-quiz'),
    path('quizzes/<int:pk>/', views.DocumentQuizDetailView.as_view(), name='document-quiz-detail'),
    
    # YouTube Videos
    path('youtube-videos/', views.YouTubeVideoListCreateView.as_view(), name='youtube-video-list'),
    path('youtube-videos/user/', views.user_youtube_videos, name='user-youtube-videos'),
    path('youtube-videos/public/', views.public_youtube_videos, name='public-youtube-videos'),
    path('youtube-videos/create/', views.create_youtube_video, name='create-youtube-video'),
    path('youtube-videos/<int:pk>/', views.YouTubeVideoDetailView.as_view(), name='youtube-video-detail'),
    
    # Calendar Events
    path('calendar-events/', views.CalendarEventListCreateView.as_view(), name='calendar-event-list'),
    path('calendar-events/user/', views.user_calendar_events, name='user-calendar-events'),
    path('calendar-events/create/', views.create_calendar_event, name='create-calendar-event'),
    path('calendar-events/<int:pk>/', views.CalendarEventDetailView.as_view(), name='calendar-event-detail'),
    path('calendar-events/<int:event_id>/complete/', views.mark_event_completed, name='mark-event-completed'),
    path('calendar-events/<int:event_id>/link-resource/', views.link_resource_to_event, name='link-resource-to-event'),
    path('calendar-events/<int:event_id>/unlink-resource/<int:resource_id>/', views.unlink_resource_from_event, name='unlink-resource-from-event'),
    
]