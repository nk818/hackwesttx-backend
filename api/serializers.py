from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from .models import (
    PasswordResetToken, Department, Professor, ClassPortfolio, 
    MarketplaceListing, PortfolioPurchase, Syllabus, SyllabusExtraction,
    ImportantDate, LectureMaterial, Flashcard, Quiz, QuizQuestion, QuizSubmission,
    ClassReview, StudyGroup, Notification, ResourceRecommendation,
    Post, Like, Comment, ProcessedFile, Document, DocumentQuiz, YouTubeVideo, CalendarEvent
)

# Get Django's default User model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone', 
                 'university', 'graduation_year', 'major', 'role', 'is_verified', 
                 'profile_visibility', 'date_joined']
        read_only_fields = ['id', 'date_joined', 'role', 'is_verified']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 
                 'last_name', 'phone', 'university', 'graduation_year', 'major']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate_email(self, value):
        try:
            User.objects.get(email=value.lower())
        except User.DoesNotExist:
            raise serializers.ValidationError("No user found with this email address.")
        return value.lower()

class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=6)
    new_password_confirm = serializers.CharField()
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def validate_token(self, value):
        try:
            token_obj = PasswordResetToken.objects.get(token=value)
            if not token_obj.is_valid():
                raise serializers.ValidationError("Invalid or expired token")
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError("Invalid token")
        return value

class UserRoleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['role', 'is_verified']
    
    def validate_role(self, value):
        # Only admins can change roles
        if not self.context.get('request').user.is_admin():
            raise serializers.ValidationError("Only admins can change user roles")
        return value

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'code']

class ProfessorSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Professor
        fields = ['id', 'name', 'email', 'department', 'department_id']


class ClassPortfolioSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = ClassPortfolio
        fields = ['id', 'professor', 'course', 'semester', 'year', 'price', 'created_by', 'created_at', 'is_public', 'color']
        read_only_fields = ['id', 'created_at', 'created_by']
    
    def create(self, validated_data):
        # Set created_by to the current user
        validated_data['created_by'] = self.context['request'].user
        
        # If no color provided, generate a random one
        if 'color' not in validated_data or not validated_data['color']:
            validated_data['color'] = ClassPortfolio.generate_random_color()
        
        portfolio = ClassPortfolio.objects.create(**validated_data)
        return portfolio

class MarketplaceListingSerializer(serializers.ModelSerializer):
    portfolio = ClassPortfolioSerializer(read_only=True)
    portfolio_id = serializers.IntegerField(write_only=True)
    buyers_count = serializers.SerializerMethodField()
    
    class Meta:
        model = MarketplaceListing
        fields = ['id', 'portfolio', 'portfolio_id', 'price', 'status', 'created_at', 
                 'updated_at', 'promo_code', 'campus_license_available', 
                 'campus_license_price', 'buyers_count']
        read_only_fields = ['created_at', 'updated_at']
    
    def get_buyers_count(self, obj):
        return obj.buyers.count()
    
    def create(self, validated_data):
        portfolio_id = validated_data.pop('portfolio_id')
        portfolio = ClassPortfolio.objects.get(id=portfolio_id)
        validated_data['portfolio'] = portfolio
        return MarketplaceListing.objects.create(**validated_data)

class PortfolioPurchaseSerializer(serializers.ModelSerializer):
    listing = MarketplaceListingSerializer(read_only=True)
    buyer = UserSerializer(read_only=True)
    listing_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = PortfolioPurchase
        fields = ['id', 'listing', 'listing_id', 'buyer', 'purchase_price', 
                 'promo_code_used', 'purchased_at', 'payment_method', 'payment_id']
        read_only_fields = ['buyer', 'purchased_at']

class SyllabusSerializer(serializers.ModelSerializer):
    extraction = serializers.SerializerMethodField()
    
    class Meta:
        model = Syllabus
        fields = ['id', 'file', 'uploaded_at', 'extracted_text', 'extraction_status', 
                 'extraction_error', 'extraction']
    
    def get_extraction(self, obj):
        if hasattr(obj, 'extraction'):
            return SyllabusExtractionSerializer(obj.extraction).data
        return None

class SyllabusExtractionSerializer(serializers.ModelSerializer):
    all_important_dates = serializers.ReadOnlyField()
    
    class Meta:
        model = SyllabusExtraction
        fields = [
            'id', 'course_title', 'course_code', 'course_description', 'credits', 'prerequisites',
            'professor_name', 'professor_email', 'professor_office', 'professor_office_hours', 'professor_phone',
            'class_days', 'class_time', 'class_location', 'semester',
            'exam_dates', 'homework_dates', 'project_dates', 'quiz_dates', 'final_exam_date', 'midterm_dates',
            'grading_scale', 'grade_breakdown', 'late_policy', 'attendance_policy',
            'academic_integrity', 'disability_accommodations', 'course_objectives',
            'textbook_required', 'textbook_recommended', 'course_website', 'additional_resources',
            'extraction_confidence', 'extraction_method', 'extracted_at', 'last_updated',
            'all_important_dates'
        ]

class ImportantDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportantDate
        fields = ['id', 'portfolio', 'title', 'date_type', 'due_date', 'description', 
                 'points', 'is_synced', 'created_at']

class LectureMaterialSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer(read_only=True)
    file = serializers.FileField(required=False, allow_null=True)
    
    class Meta:
        model = LectureMaterial
        fields = ['id', 'portfolio', 'title', 'material_type', 'file', 'uploaded_by', 
                 'uploaded_at', 'topic']

class FlashcardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flashcard
        fields = ['id', 'material', 'front', 'back', 'difficulty', 'created_at']

class QuizQuestionSerializer(serializers.ModelSerializer):
    correct_answer = serializers.SerializerMethodField()
    
    class Meta:
        model = QuizQuestion
        fields = ['id', 'quiz', 'question_text', 'question_type', 'options', 'correct_option_index', 
                 'is_true', 'points', 'explanation', 'correct_answer']
    
    def get_correct_answer(self, obj):
        """Return the correct answer based on question type"""
        return obj.get_correct_answer()

class QuizSerializer(serializers.ModelSerializer):
    questions = QuizQuestionSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Quiz
        fields = ['id', 'portfolio', 'title', 'quiz_type', 'topic', 'created_by', 'created_at', 
                 'is_published', 'time_limit_minutes', 'questions']

class QuizSubmissionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    quiz = QuizSerializer(read_only=True)
    
    class Meta:
        model = QuizSubmission
        fields = ['id', 'quiz', 'user', 'submitted_at', 'time_taken_minutes', 
                 'score', 'total_points', 'answers']

class ClassReviewSerializer(serializers.ModelSerializer):
    reviewer = UserSerializer(read_only=True)
    
    class Meta:
        model = ClassReview
        fields = ['id', 'reviewer', 'final_grade', 'difficulty_rating', 
                 'teaching_quality_rating', 'workload_rating', 'comments', 
                 'tips', 'created_at']

class StudyGroupSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    members = UserSerializer(many=True, read_only=True)
    member_count = serializers.SerializerMethodField()
    
    class Meta:
        model = StudyGroup
        fields = ['id', 'name', 'description', 'created_by', 'members', 
                 'max_members', 'is_active', 'created_at', 'member_count']
    
    def get_member_count(self, obj):
        return obj.members.count()

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'notification_type', 'is_read', 
                 'created_at', 'related_date']

class ResourceRecommendationSerializer(serializers.ModelSerializer):
    recommended_by = UserSerializer(read_only=True)
    
    class Meta:
        model = ResourceRecommendation
        fields = ['id', 'title', 'url', 'resource_type', 'description', 
                 'topic', 'recommended_by', 'created_at']

# Portfolio Detail Serializer with all related data
class PortfolioDetailSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    syllabus = SyllabusSerializer(read_only=True)
    important_dates = ImportantDateSerializer(many=True, read_only=True)
    materials = LectureMaterialSerializer(many=True, read_only=True)
    quizzes = QuizSerializer(many=True, read_only=True)
    reviews = ClassReviewSerializer(many=True, read_only=True)
    study_groups = StudyGroupSerializer(many=True, read_only=True)
    recommendations = ResourceRecommendationSerializer(many=True, read_only=True)
    
    class Meta:
        model = ClassPortfolio
        fields = ['id', 'professor', 'course', 'semester', 'year', 'price', 'created_by', 
                 'created_at', 'is_public', 'color', 'syllabus', 'important_dates', 
                 'materials', 'quizzes', 'reviews', 'study_groups', 'recommendations']
        read_only_fields = ['id', 'created_at', 'created_by']
    
    def validate_color(self, value):
        """Validate hex color format"""
        if value and not value.startswith('#'):
            raise serializers.ValidationError("Color must be in hex format (e.g., #FF5733)")
        if value and len(value) != 7:
            raise serializers.ValidationError("Color must be 7 characters long (e.g., #FF5733)")
        return value
    
    def update(self, instance, validated_data):
        """Allow updating specific fields like color while keeping others unchanged"""
        # Update only the fields that are in validated_data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

# Keep existing serializers for backward compatibility
class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'created_at', 'updated_at']

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'tags', 'image_url', 
                 'is_published', 'views', 'created_at', 'updated_at', 
                 'comments', 'likes_count', 'is_liked']
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags', 'image_url', 'is_published']

class ProcessedFileSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer(read_only=True)
    portfolio_title = serializers.SerializerMethodField()
    
    class Meta:
        model = ProcessedFile
        fields = ['id', 'original_file', 'file_name', 'file_type', 'file_size', 
                 'context', 'extracted_text', 'ai_summary', 'processing_status', 
                 'processing_error', 'metadata', 'word_count', 'char_count',
                 'uploaded_by', 'portfolio', 'portfolio_title', 'uploaded_at', 
                 'processed_at']
        read_only_fields = ['id', 'uploaded_by', 'uploaded_at', 'processed_at', 
                           'processing_status', 'processing_error', 'metadata', 
                           'word_count', 'char_count', 'extracted_text', 'ai_summary']
    
    def get_portfolio_title(self, obj):
        if obj.portfolio:
            return f"{obj.portfolio.course.code} - {obj.portfolio.course.name}"
        return None

class ProcessedFileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessedFile
        fields = ['original_file', 'file_name', 'file_type', 'file_size', 
                 'context', 'portfolio']
    
    def validate_file_type(self, value):
        """Validate file type based on file extension"""
        allowed_types = ['pdf', 'docx', 'doc', 'pptx', 'ppt', 'txt']
        if value not in allowed_types:
            raise serializers.ValidationError(f"Unsupported file type: {value}")
        return value

class DocumentSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer(read_only=True)
    portfolio = ClassPortfolioSerializer(read_only=True)
    portfolio_id = serializers.IntegerField(write_only=True, required=False)
    is_successful = serializers.ReadOnlyField()
    summary_data = serializers.ReadOnlyField()
    extracted_key_points = serializers.ReadOnlyField()
    
    class Meta:
        model = Document
        fields = [
            'id', 'file_id', 'filename', 'download_url', 'bucket', 'folder',
            'learn_method', 'learning_result', 'key_points', 'uploaded_by',
            'portfolio', 'portfolio_id', 'is_processed', 'processing_error',
            'created_at', 'updated_at', 'is_successful', 'summary_data',
            'extracted_key_points'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'uploaded_by']
    
    def create(self, validated_data):
        # Set uploaded_by to the current user
        validated_data['uploaded_by'] = self.context['request'].user
        
        # Handle portfolio association
        portfolio_id = validated_data.pop('portfolio_id', None)
        if portfolio_id:
            try:
                from .models import ClassPortfolio
                validated_data['portfolio'] = ClassPortfolio.objects.get(id=portfolio_id)
            except ClassPortfolio.DoesNotExist:
                raise serializers.ValidationError("Portfolio not found")
        
        return super().create(validated_data)

class DocumentCreateSerializer(serializers.ModelSerializer):
    """Simplified serializer for document creation"""
    portfolio_id = serializers.IntegerField(required=False)
    
    class Meta:
        model = Document
        fields = [
            'file_id', 'filename', 'download_url', 'bucket', 'folder',
            'learn_method', 'learning_result', 'key_points', 'portfolio_id',
            'is_processed', 'processing_error'
        ]
    
    def create(self, validated_data):
        # Set uploaded_by to the current user
        validated_data['uploaded_by'] = self.context['request'].user
        
        # Handle portfolio association
        portfolio_id = validated_data.pop('portfolio_id', None)
        if portfolio_id:
            try:
                from .models import ClassPortfolio
                validated_data['portfolio'] = ClassPortfolio.objects.get(id=portfolio_id)
            except ClassPortfolio.DoesNotExist:
                raise serializers.ValidationError("Portfolio not found")
        
        return super().create(validated_data)

class DocumentQuizSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    document = DocumentSerializer(read_only=True)
    
    class Meta:
        model = DocumentQuiz
        fields = ['id', 'user', 'document', 'filename', 'topic', 'total_questions', 
                 'text_length', 'word_count', 'quiz_data', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']
    
    def create(self, validated_data):
        # Set user to the current user
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class DocumentQuizCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentQuiz
        fields = ["document", "filename", "topic", "total_questions", 
                 "text_length", "word_count", "quiz_data"]
    
    def create(self, validated_data):
        # Set user to the current user
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class YouTubeVideoSerializer(serializers.ModelSerializer):
    """Serializer for learning links (keeping name for API backward compatibility)"""
    user = UserSerializer(read_only=True)
    link_type = serializers.ReadOnlyField()
    video_id = serializers.ReadOnlyField()
    thumbnail_url = serializers.ReadOnlyField()
    embed_url = serializers.ReadOnlyField()
    
    class Meta:
        model = YouTubeVideo
        fields = ['id', 'user', 'url', 'title', 'description', 'link_type', 'video_id', 
                 'thumbnail_url', 'embed_url', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user', 'link_type']
    
    def create(self, validated_data):
        # Set user to the current user
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class YouTubeVideoCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating learning links (keeping name for API backward compatibility)"""
    class Meta:
        model = YouTubeVideo
        fields = ['url', 'title', 'description']
    
    def create(self, validated_data):
        # Set user to the current user
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def validate_url(self, value):
        """
        Validate that the URL is safe and appropriate for learning content.
        The model's validate_safe_url function handles the actual validation.
        """
        # The model's validator will automatically be called,
        # but we can add additional checks here if needed
        from .models import validate_safe_url
        validate_safe_url(value)
        return value


class CalendarEventSerializer(serializers.ModelSerializer):
    """Serializer for calendar events"""
    user = UserSerializer(read_only=True)
    class_portfolio = ClassPortfolioSerializer(read_only=True)
    class_portfolio_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    linked_resources = YouTubeVideoSerializer(many=True, read_only=True)
    linked_resource_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
        help_text="IDs of learning resources to link to this event"
    )
    is_overdue = serializers.ReadOnlyField()
    days_until_due = serializers.ReadOnlyField()
    is_due_soon = serializers.ReadOnlyField()
    
    class Meta:
        model = CalendarEvent
        fields = [
            'id', 'user', 'class_portfolio', 'class_portfolio_id', 'title', 'description', 'event_type',
            'due_date', 'reminder_time', 'status', 'priority', 'points', 'location',
            'linked_resources', 'linked_resource_ids', 'created_at', 'updated_at',
            'completed_at', 'is_overdue', 'days_until_due', 'is_due_soon'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'completed_at']
    
    def create(self, validated_data):
        # Extract linked_resource_ids if provided
        linked_resource_ids = validated_data.pop('linked_resource_ids', [])
        
        # Handle class_portfolio_id
        class_portfolio_id = validated_data.pop('class_portfolio_id', None)
        if class_portfolio_id:
            validated_data['class_portfolio_id'] = class_portfolio_id
        
        # Set user to the current user
        validated_data['user'] = self.context['request'].user
        
        # Create the calendar event
        event = super().create(validated_data)
        
        # Link learning resources if provided
        if linked_resource_ids:
            resources = YouTubeVideo.objects.filter(
                id__in=linked_resource_ids,
                user=self.context['request'].user
            )
            event.linked_resources.set(resources)
        
        return event
    
    def update(self, instance, validated_data):
        # Extract linked_resource_ids if provided
        linked_resource_ids = validated_data.pop('linked_resource_ids', None)
        
        # Update the calendar event
        event = super().update(instance, validated_data)
        
        # Update linked resources if provided
        if linked_resource_ids is not None:
            resources = YouTubeVideo.objects.filter(
                id__in=linked_resource_ids,
                user=self.context['request'].user
            )
            event.linked_resources.set(resources)
        
        return event


class CalendarEventCreateSerializer(serializers.ModelSerializer):
    """Simplified serializer for creating calendar events"""
    linked_resource_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        help_text="IDs of learning resources to link to this event"
    )
    
    class Meta:
        model = CalendarEvent
        fields = [
            'title', 'description', 'event_type', 'due_date', 'reminder_time',
            'status', 'priority', 'points', 'location', 'class_portfolio', 'linked_resource_ids'
        ]
    
    def create(self, validated_data):
        # Extract linked_resource_ids if provided
        linked_resource_ids = validated_data.pop('linked_resource_ids', [])
        
        # Set user to the current user
        validated_data['user'] = self.context['request'].user
        
        # Create the calendar event
        event = CalendarEvent.objects.create(**validated_data)
        
        # Link learning resources if provided
        if linked_resource_ids:
            resources = YouTubeVideo.objects.filter(
                id__in=linked_resource_ids,
                user=self.context['request'].user
            )
            event.linked_resources.set(resources)
        
        return event
