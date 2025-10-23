from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, PasswordResetToken, Department, Professor, ClassPortfolio, 
    MarketplaceListing, PortfolioPurchase, Syllabus, SyllabusExtraction,
    ImportantDate, LectureMaterial, Flashcard, Quiz, QuizQuestion, QuizSubmission,
    ClassReview, StudyGroup, Notification, ResourceRecommendation,
    Post, Like, Comment, ProcessedFile, Document, DocumentQuiz, YouTubeVideo, CalendarEvent
)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_verified', 'is_staff')
    list_filter = ('role', 'is_verified', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone', 'university', 'graduation_year', 'major', 'role', 'is_verified', 'profile_visibility')}),
    )

@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'token', 'created_at', 'expires_at', 'is_used']
    list_filter = ['is_used', 'created_at', 'expires_at']
    search_fields = ['user__username', 'user__email', 'token']
    readonly_fields = ['token', 'created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

@admin.register(ClassPortfolio)
class ClassPortfolioAdmin(admin.ModelAdmin):
    list_display = ['professor', 'course', 'semester', 'year', 'price', 'created_by', 'is_public', 'created_at']
    list_filter = ['is_public', 'semester', 'year', 'created_at']
    search_fields = ['professor', 'course', 'created_by__username']
    fieldsets = (
        ('Basic Information', {
            'fields': ('professor', 'course', 'semester', 'year', 'price', 'created_by', 'is_public')
        }),
    )

@admin.register(MarketplaceListing)
class MarketplaceListingAdmin(admin.ModelAdmin):
    list_display = ['portfolio', 'price', 'status', 'created_at', 'buyers_count']
    list_filter = ['status', 'created_at', 'campus_license_available']
    search_fields = ['portfolio__professor']
    
    def buyers_count(self, obj):
        return obj.buyers.count()
    buyers_count.short_description = 'Buyers'

@admin.register(PortfolioPurchase)
class PortfolioPurchaseAdmin(admin.ModelAdmin):
    list_display = ['buyer', 'listing', 'purchase_price', 'purchased_at', 'payment_method']
    list_filter = ['purchased_at', 'payment_method', 'promo_code_used']
    search_fields = ['buyer__username', 'buyer__email', 'listing__portfolio__professor']
    readonly_fields = ['purchased_at']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']
    search_fields = ['code', 'name']

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'department']
    list_filter = ['department']
    search_fields = ['name', 'email']


@admin.register(Syllabus)
class SyllabusAdmin(admin.ModelAdmin):
    list_display = ['portfolio', 'uploaded_at', 'extraction_status']
    list_filter = ['extraction_status', 'uploaded_at']
    search_fields = ['portfolio__professor']

@admin.register(SyllabusExtraction)
class SyllabusExtractionAdmin(admin.ModelAdmin):
    list_display = ['syllabus', 'course_title', 'professor_name', 'extraction_confidence', 'extracted_at']
    list_filter = ['extraction_method', 'extraction_confidence', 'extracted_at']
    search_fields = ['course_title', 'professor_name']
    readonly_fields = ['extracted_at', 'last_updated']

@admin.register(ImportantDate)
class ImportantDateAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_type', 'due_date', 'portfolio', 'is_synced']
    list_filter = ['date_type', 'is_synced', 'due_date']
    search_fields = ['title']

@admin.register(LectureMaterial)
class LectureMaterialAdmin(admin.ModelAdmin):
    list_display = ['title', 'material_type', 'uploaded_by', 'portfolio', 'uploaded_at']
    list_filter = ['material_type', 'uploaded_at']
    search_fields = ['title', 'topic']

@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    list_display = ['front', 'difficulty', 'material', 'created_at']
    list_filter = ['difficulty', 'created_at']

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'quiz_type', 'topic', 'created_by', 'created_at']
    list_filter = ['quiz_type', 'created_at']
    search_fields = ['title', 'topic']

@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'question_type', 'quiz', 'points']
    list_filter = ['question_type', 'quiz', 'points']
    search_fields = ['question_text']

@admin.register(QuizSubmission)
class QuizSubmissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'score', 'submitted_at', 'time_taken_minutes']
    list_filter = ['quiz', 'submitted_at', 'score']
    search_fields = ['user__username', 'quiz__title']
    readonly_fields = ['submitted_at', 'score', 'total_points']

@admin.register(ClassReview)
class ClassReviewAdmin(admin.ModelAdmin):
    list_display = ['portfolio', 'reviewer', 'final_grade', 'difficulty_rating', 'teaching_quality_rating']
    list_filter = ['final_grade', 'difficulty_rating', 'teaching_quality_rating']

@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'portfolio', 'created_by', 'max_members', 'is_active']
    list_filter = ['is_active', 'created_at']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']

@admin.register(ResourceRecommendation)
class ResourceRecommendationAdmin(admin.ModelAdmin):
    list_display = ['title', 'resource_type', 'topic', 'recommended_by', 'created_at']
    list_filter = ['resource_type', 'created_at']

# Keep existing admin for backward compatibility
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_published', 'created_at']
    list_filter = ['is_published', 'created_at']
    search_fields = ['title', 'content']

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['created_at']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'created_at']
    list_filter = ['created_at']

@admin.register(ProcessedFile)
class ProcessedFileAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'file_type', 'context', 'uploaded_by', 'processing_status', 'uploaded_at']
    list_filter = ['file_type', 'context', 'processing_status', 'uploaded_at']
    search_fields = ['file_name', 'uploaded_by__username', 'uploaded_by__email']
    readonly_fields = ['uploaded_at', 'processed_at', 'word_count', 'char_count']
    fieldsets = (
        ('File Information', {
            'fields': ('original_file', 'file_name', 'file_type', 'file_size', 'context')
        }),
        ('Processing Results', {
            'fields': ('processing_status', 'processing_error', 'extracted_text', 'ai_summary')
        }),
        ('Metadata', {
            'fields': ('metadata', 'word_count', 'char_count'),
            'classes': ('collapse',)
        }),
        ('Relationships', {
            'fields': ('uploaded_by', 'portfolio')
        }),
        ('Timestamps', {
            'fields': ('uploaded_at', 'processed_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['filename', 'uploaded_by', 'learn_method', 'is_processed', 'is_successful', 'created_at']
    list_filter = ['learn_method', 'is_processed', 'created_at', 'uploaded_by']
    search_fields = ['filename', 'uploaded_by__username', 'portfolio__professor']
    readonly_fields = ['file_id', 'created_at', 'updated_at', 'is_successful', 'summary_data', 'extracted_key_points']
    
    fieldsets = (
        ('File Information', {
            'fields': ('file_id', 'filename', 'download_url', 'bucket', 'folder')
        }),
        ('Processing', {
            'fields': ('learn_method', 'learning_result', 'key_points', 'is_processed', 'processing_error')
        }),
        ('Associations', {
            'fields': ('uploaded_by', 'portfolio')
        }),
        ('Status', {
            'fields': ('is_successful', 'summary_data', 'extracted_key_points'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def is_successful(self, obj):
        return obj.is_successful
    is_successful.boolean = True
    is_successful.short_description = 'Successful'

@admin.register(DocumentQuiz)
class DocumentQuizAdmin(admin.ModelAdmin):
    list_display = ['topic', 'user', 'filename', 'total_questions', 'is_successful', 'created_at']
    list_filter = ['created_at', 'total_questions', 'user']
    search_fields = ['topic', 'filename', 'user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at', 'quiz_data']
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'document', 'filename', 'topic')
        }),
        ('Quiz Details', {
            'fields': ('total_questions', 'text_length', 'word_count')
        }),
        ('Quiz Data', {
            'fields': ('quiz_data',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def is_successful(self, obj):
        return obj.is_successful
    is_successful.boolean = True
    is_successful.short_description = 'Successful'


@admin.register(YouTubeVideo)
class YouTubeVideoAdmin(admin.ModelAdmin):
    """Admin interface for Learning Links (model name kept for backward compatibility)"""
    list_display = ['get_title_display', 'user', 'link_type', 'created_at']
    list_filter = ['created_at', 'user']
    search_fields = ['title', 'description', 'url', 'user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at', 'link_type', 'video_id', 'thumbnail_url', 'embed_url']
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'url', 'title', 'description')
        }),
        ('Link Details', {
            'fields': ('link_type', 'video_id', 'thumbnail_url', 'embed_url'),
            'classes': ('collapse',),
            'description': 'Automatically detected information about the learning resource'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_title_display(self, obj):
        """Display title or link type if no title"""
        return obj.title or f"[{obj.link_type}]"
    get_title_display.short_description = 'Title'
    
    def link_type(self, obj):
        return obj.link_type
    link_type.short_description = 'Link Type'
    
    def video_id(self, obj):
        return obj.video_id or 'N/A'
    video_id.short_description = 'Video ID (YouTube only)'
    
    def thumbnail_url(self, obj):
        return obj.thumbnail_url or 'N/A'
    thumbnail_url.short_description = 'Thumbnail URL'
    
    def embed_url(self, obj):
        return obj.embed_url or 'N/A'
    embed_url.short_description = 'Embed URL'


@admin.register(CalendarEvent)
class CalendarEventAdmin(admin.ModelAdmin):
    """Admin interface for Calendar Events"""
    list_display = ['title', 'user', 'event_type', 'due_date', 'status', 'priority', 'is_overdue']
    list_filter = ['event_type', 'status', 'priority', 'due_date', 'created_at']
    search_fields = ['title', 'description', 'user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at', 'completed_at', 'is_overdue', 'days_until_due', 'is_due_soon']
    filter_horizontal = ['linked_resources']
    date_hierarchy = 'due_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'class_portfolio', 'title', 'description', 'event_type')
        }),
        ('Schedule', {
            'fields': ('due_date', 'reminder_time')
        }),
        ('Status & Priority', {
            'fields': ('status', 'priority', 'points', 'location')
        }),
        ('Learning Resources', {
            'fields': ('linked_resources',),
            'description': 'Link learning resources to this calendar event'
        }),
        ('Metadata', {
            'fields': ('is_overdue', 'days_until_due', 'is_due_soon', 'created_at', 'updated_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )
    
    def is_overdue(self, obj):
        return obj.is_overdue
    is_overdue.boolean = True
    is_overdue.short_description = 'Overdue'
    
    actions = ['mark_as_completed', 'mark_as_not_started']
    
    def mark_as_completed(self, request, queryset):
        """Admin action to mark events as completed"""
        count = 0
        for event in queryset:
            event.mark_completed()
            count += 1
        self.message_user(request, f'{count} event(s) marked as completed.')
    mark_as_completed.short_description = 'Mark selected events as completed'
    
    def mark_as_not_started(self, request, queryset):
        """Admin action to mark events as not started"""
        queryset.update(status='not_started', completed_at=None)
        self.message_user(request, f'{queryset.count()} event(s) marked as not started.')
    mark_as_not_started.short_description = 'Mark selected events as not started'
