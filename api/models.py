from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator, URLValidator
from django.core.exceptions import ValidationError
import re

class User(AbstractUser):
    # User roles
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    ]
    
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    university = models.CharField(max_length=200, blank=True)
    graduation_year = models.IntegerField(null=True, blank=True)
    major = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    is_verified = models.BooleanField(default=False)
    profile_visibility = models.CharField(
        max_length=20, 
        choices=[('public', 'Public'), ('private', 'Private')], 
        default='public'
    )
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super().save(*args, **kwargs)
    
    def is_student(self):
        return self.role == 'student'
    
    def is_moderator(self):
        return self.role == 'moderator'
    
    def is_admin(self):
        return self.role == 'admin'
    
    def can_moderate_content(self):
        return self.role in ['moderator', 'admin']
    
    def can_access_admin_panel(self):
        return self.role == 'admin'

class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_tokens')
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def is_valid(self):
        return not self.is_used and not self.is_expired()

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return f"{self.code} - {self.name}"

class Professor(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='professors')
    
    def __str__(self):
        return self.name

class ClassPortfolio(models.Model):
    professor = models.CharField(max_length=100)
    course = models.CharField(max_length=100, blank=True, help_text="Course name or code")
    semester = models.CharField(max_length=20)  # e.g., "Fall 2024"
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Price in USD")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_portfolios')
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)
    color = models.CharField(
        max_length=7, 
        default='#6366F1',
        help_text="Hex color code for visual identification (e.g., #FF5733)"
    )
    
    class Meta:
        unique_together = ['professor', 'semester', 'year']
    
    def __str__(self):
        return f"{self.professor} ({self.semester} {self.year})"
    
    @staticmethod
    def generate_random_color():
        """Generate a random pleasant color for class identification"""
        import random
        # Predefined set of pleasant colors for better UX
        colors = [
            '#6366F1',  # Indigo
            '#8B5CF6',  # Purple
            '#EC4899',  # Pink
            '#EF4444',  # Red
            '#F59E0B',  # Amber
            '#10B981',  # Emerald
            '#06B6D4',  # Cyan
            '#3B82F6',  # Blue
            '#F97316',  # Orange
            '#84CC16',  # Lime
            '#14B8A6',  # Teal
            '#A855F7',  # Violet
            '#F43F5E',  # Rose
            '#22C55E',  # Green
        ]
        return random.choice(colors)

class MarketplaceListing(models.Model):
    """Marketplace listing for paid portfolios"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('sold', 'Sold'),
        ('paused', 'Paused'),
        ('removed', 'Removed'),
    ]
    
    portfolio = models.OneToOneField(ClassPortfolio, on_delete=models.CASCADE, related_name='marketplace_listing')
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price in USD")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Purchase tracking
    buyers = models.ManyToManyField(User, through='PortfolioPurchase', related_name='purchased_portfolios')
    
    # Promotional features
    promo_code = models.CharField(max_length=50, blank=True, null=True)
    campus_license_available = models.BooleanField(default=False)
    campus_license_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.portfolio.course.code} - ${self.price} ({self.status})"
    
    def is_available(self):
        return self.status == 'active'
    
    def get_effective_price(self, promo_code=None):
        """Get effective price after applying promo code"""
        if promo_code and self.promo_code == promo_code:
            # Apply 20% discount for promo codes
            return self.price * 0.8
        return self.price

class PortfolioPurchase(models.Model):
    """Track portfolio purchases"""
    listing = models.ForeignKey(MarketplaceListing, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    promo_code_used = models.CharField(max_length=50, blank=True, null=True)
    purchased_at = models.DateTimeField(auto_now_add=True)
    
    # Payment tracking
    payment_method = models.CharField(max_length=50, default='stripe')  # stripe, paypal, etc.
    payment_id = models.CharField(max_length=200, blank=True, null=True)
    
    class Meta:
        unique_together = ['listing', 'buyer']
        ordering = ['-purchased_at']
    
    def __str__(self):
        return f"{self.buyer.username} purchased {self.listing.portfolio.course.code} for ${self.purchase_price}"

class Syllabus(models.Model):
    portfolio = models.OneToOneField(ClassPortfolio, on_delete=models.CASCADE, related_name='syllabus')
    file = models.FileField(upload_to='syllabi/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    extracted_text = models.TextField(blank=True)
    extraction_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], default='pending')
    extraction_error = models.TextField(blank=True)
    
    def __str__(self):
        return f"Syllabus for {self.portfolio}"

class SyllabusExtraction(models.Model):
    """AI-powered extraction of syllabus data"""
    syllabus = models.OneToOneField(Syllabus, on_delete=models.CASCADE, related_name='extraction')
    
    # Course Information
    course_title = models.CharField(max_length=200, blank=True)
    course_code = models.CharField(max_length=20, blank=True)
    course_description = models.TextField(blank=True)
    credits = models.IntegerField(null=True, blank=True)
    prerequisites = models.TextField(blank=True)
    
    # Professor Information
    professor_name = models.CharField(max_length=200, blank=True)
    professor_email = models.EmailField(blank=True)
    professor_office = models.CharField(max_length=200, blank=True)
    professor_office_hours = models.TextField(blank=True)
    professor_phone = models.CharField(max_length=20, blank=True)
    
    # Class Schedule
    class_days = models.CharField(max_length=50, blank=True)  # e.g., "MWF", "TTh"
    class_time = models.CharField(max_length=50, blank=True)  # e.g., "10:00-10:50 AM"
    class_location = models.CharField(max_length=200, blank=True)  # e.g., "Room 101"
    semester = models.CharField(max_length=50, blank=True)  # e.g., "Fall 2024"
    
    # Important Dates (extracted from syllabus)
    exam_dates = models.JSONField(default=list, blank=True)  # List of exam dates
    homework_dates = models.JSONField(default=list, blank=True)  # List of homework due dates
    project_dates = models.JSONField(default=list, blank=True)  # List of project due dates
    quiz_dates = models.JSONField(default=list, blank=True)  # List of quiz dates
    final_exam_date = models.DateTimeField(null=True, blank=True)
    midterm_dates = models.JSONField(default=list, blank=True)  # List of midterm dates
    
    # Grading Information
    grading_scale = models.TextField(blank=True)
    grade_breakdown = models.JSONField(default=dict, blank=True)  # e.g., {"exams": 40, "homework": 30}
    late_policy = models.TextField(blank=True)
    attendance_policy = models.TextField(blank=True)
    
    # Course Policies
    academic_integrity = models.TextField(blank=True)
    disability_accommodations = models.TextField(blank=True)
    course_objectives = models.TextField(blank=True)
    
    # Additional Information
    textbook_required = models.TextField(blank=True)
    textbook_recommended = models.TextField(blank=True)
    course_website = models.URLField(blank=True)
    additional_resources = models.TextField(blank=True)
    
    # Extraction Metadata
    extraction_confidence = models.FloatField(default=0.0)  # 0.0 to 1.0
    extraction_method = models.CharField(max_length=50, default='ai_extraction')
    extracted_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Extraction for {self.syllabus.portfolio}"
    
    @property
    def all_important_dates(self):
        """Combine all extracted dates into a single list"""
        all_dates = []
        all_dates.extend(self.exam_dates)
        all_dates.extend(self.homework_dates)
        all_dates.extend(self.project_dates)
        all_dates.extend(self.quiz_dates)
        all_dates.extend(self.midterm_dates)
        if self.final_exam_date:
            all_dates.append({
                'title': 'Final Exam',
                'date': self.final_exam_date.isoformat(),
                'type': 'final'
            })
        return sorted(all_dates, key=lambda x: x.get('date', ''))

class ImportantDate(models.Model):
    TYPE_CHOICES = [
        ('exam', 'Exam'),
        ('quiz', 'Quiz'),
        ('assignment', 'Assignment'),
        ('project', 'Project'),
        ('midterm', 'Midterm'),
        ('final', 'Final'),
        ('other', 'Other'),
    ]
    
    portfolio = models.ForeignKey(ClassPortfolio, on_delete=models.CASCADE, related_name='important_dates')
    title = models.CharField(max_length=200)
    date_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    due_date = models.DateTimeField()
    description = models.TextField(blank=True)
    points = models.IntegerField(null=True, blank=True)
    is_synced = models.BooleanField(default=False)  # Google/Outlook sync
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['due_date']
    
    def __str__(self):
        return f"{self.title} - {self.due_date.strftime('%Y-%m-%d')}"

class LectureMaterial(models.Model):
    MATERIAL_TYPE_CHOICES = [
        ('notes', 'Lecture Notes'),
        ('slides', 'PowerPoint'),
        ('pdf', 'PDF'),
        ('image', 'Image'),
        ('video', 'Video'),
        ('audio', 'Audio'),
    ]
    
    portfolio = models.ForeignKey(ClassPortfolio, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=200)
    material_type = models.CharField(max_length=20, choices=MATERIAL_TYPE_CHOICES)
    file = models.FileField(upload_to='materials/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    topic = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.title} - {self.material_type}"

class Flashcard(models.Model):
    material = models.ForeignKey(LectureMaterial, on_delete=models.CASCADE, related_name='flashcards')
    front = models.TextField()
    back = models.TextField()
    difficulty = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Flashcard: {self.front[:50]}..."

class Quiz(models.Model):
    QUIZ_TYPE_CHOICES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('mixed', 'Mixed (Multiple Choice + True/False)'),
    ]
    
    portfolio = models.ForeignKey(ClassPortfolio, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=200)
    quiz_type = models.CharField(max_length=20, choices=QUIZ_TYPE_CHOICES, default='mixed')
    topic = models.CharField(max_length=100, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    time_limit_minutes = models.IntegerField(null=True, blank=True, help_text="Time limit in minutes (optional)")
    
    def __str__(self):
        return f"{self.title} - {self.quiz_type}"

class QuizQuestion(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
    ]
    
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES, default='multiple_choice')
    
    # For multiple choice questions
    options = models.JSONField(default=list, blank=True, help_text="List of answer options for multiple choice")
    correct_option_index = models.IntegerField(null=True, blank=True, help_text="Index of correct option (0-based)")
    
    # For true/false questions
    is_true = models.BooleanField(null=True, blank=True, help_text="True if answer is True, False if answer is False")
    
    # General fields
    points = models.IntegerField(default=1)
    explanation = models.TextField(blank=True, help_text="Explanation for the correct answer")
    
    def __str__(self):
        return f"Q: {self.question_text[:50]}... ({self.question_type})"
    
    def get_correct_answer(self):
        """Get the correct answer based on question type"""
        if self.question_type == 'multiple_choice':
            if self.correct_option_index is not None and 0 <= self.correct_option_index < len(self.options):
                return self.options[self.correct_option_index]
            return None
        elif self.question_type == 'true_false':
            return "True" if self.is_true else "False"
        return None
    
    def validate_answer(self, user_answer):
        """Validate user's answer"""
        if self.question_type == 'multiple_choice':
            return user_answer == self.get_correct_answer()
        elif self.question_type == 'true_false':
            return user_answer.lower() in ['true', 'false'] and (
                (user_answer.lower() == 'true' and self.is_true) or 
                (user_answer.lower() == 'false' and not self.is_true)
            )
        return False

class QuizSubmission(models.Model):
    """Track user quiz submissions and answers"""
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='submissions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_submissions')
    submitted_at = models.DateTimeField(auto_now_add=True)
    time_taken_minutes = models.IntegerField(null=True, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    total_points = models.IntegerField(default=0)
    answers = models.JSONField(default=dict, help_text="Dictionary of question_id: user_answer")
    
    class Meta:
        unique_together = ['quiz', 'user']
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} ({self.score}%)"
    
    def calculate_score(self):
        """Calculate score based on answers"""
        correct_answers = 0
        total_points = 0
        
        for question_id, user_answer in self.answers.items():
            try:
                question = QuizQuestion.objects.get(id=question_id)
                total_points += question.points
                
                if question.validate_answer(user_answer):
                    correct_answers += question.points
            except QuizQuestion.DoesNotExist:
                continue
        
        if total_points > 0:
            self.score = (correct_answers / total_points) * 100
            self.total_points = total_points
            self.save()
            return self.score
        return 0

class ClassReview(models.Model):
    portfolio = models.ForeignKey(ClassPortfolio, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    final_grade = models.CharField(max_length=2, blank=True)  # A, B+, etc.
    difficulty_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    teaching_quality_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    workload_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comments = models.TextField(blank=True)
    tips = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review for {self.portfolio} by {self.reviewer.username}"

class StudyGroup(models.Model):
    portfolio = models.ForeignKey(ClassPortfolio, on_delete=models.CASCADE, related_name='study_groups')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_study_groups')
    members = models.ManyToManyField(User, related_name='study_groups')
    max_members = models.IntegerField(default=10)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.portfolio}"

class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = [
        ('deadline', 'Deadline Reminder'),
        ('grade', 'Grade Update'),
        ('study', 'Study Reminder'),
        ('group', 'Study Group Update'),
        ('general', 'General'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    related_date = models.ForeignKey(ImportantDate, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"

class ResourceRecommendation(models.Model):
    portfolio = models.ForeignKey(ClassPortfolio, on_delete=models.CASCADE, related_name='recommendations')
    title = models.CharField(max_length=200)
    url = models.URLField()
    resource_type = models.CharField(max_length=50)  # youtube, textbook, website, etc.
    description = models.TextField(blank=True)
    topic = models.CharField(max_length=100, blank=True)
    recommended_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.resource_type}"

# Keep existing models for backward compatibility
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    tags = models.CharField(max_length=500, blank=True, help_text='Comma-separated tags')
    image_url = models.URLField(blank=True, null=True)
    is_published = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def tags_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['post', 'user']

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

class ProcessedFile(models.Model):
    """Store processed files and their AI-generated summaries"""
    FILE_TYPE_CHOICES = [
        ('pdf', 'PDF Document'),
        ('docx', 'Word Document'),
        ('pptx', 'PowerPoint Presentation'),
        ('doc', 'Word Document (Legacy)'),
        ('ppt', 'PowerPoint (Legacy)'),
        ('txt', 'Text Document'),
    ]
    
    CONTEXT_CHOICES = [
        ('lecture_notes', 'Lecture Notes'),
        ('syllabus', 'Syllabus'),
        ('assignment', 'Assignment'),
        ('textbook', 'Textbook Chapter'),
        ('presentation', 'Presentation Slides'),
        ('handout', 'Handout'),
        ('other', 'Other'),
    ]
    
    # File information
    original_file = models.FileField(upload_to='processed_files/')
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES)
    file_size = models.BigIntegerField()
    context = models.CharField(max_length=50, choices=CONTEXT_CHOICES, default='other')
    
    # Processing results
    extracted_text = models.TextField()
    ai_summary = models.TextField(blank=True)
    processing_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], default='pending')
    processing_error = models.TextField(blank=True)
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    word_count = models.IntegerField(default=0)
    char_count = models.IntegerField(default=0)
    
    # Relationships
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='processed_files')
    portfolio = models.ForeignKey(ClassPortfolio, on_delete=models.CASCADE, related_name='processed_files', null=True, blank=True)
    
    # Timestamps
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.file_name} ({self.get_file_type_display()}) - {self.get_context_display()}"

class Document(models.Model):
    """Document model for storing uploaded files and their metadata"""
    
    # File identification
    file_id = models.CharField(max_length=100, unique=True, help_text="Unique file identifier")
    filename = models.CharField(max_length=255, help_text="Original filename")
    download_url = models.URLField(help_text="S3 download URL")
    
    # Storage information
    bucket = models.CharField(max_length=100, help_text="S3 bucket name")
    folder = models.CharField(max_length=100, help_text="S3 folder path")
    
    # Learning configuration
    learn_method = models.CharField(
        max_length=50,
        choices=[
            ('summary', 'Summary'),
            ('extract', 'Extract'),
            ('analyze', 'Analyze'),
        ],
        default='summary',
        help_text="Learning method applied to the document"
    )
    
    # Learning results
    learning_result = models.JSONField(
        default=dict,
        help_text="Results from document processing"
    )
    
    # Key points extracted
    key_points = models.JSONField(
        default=list,
        help_text="Key points extracted from the document"
    )
    
    # User and portfolio association
    uploaded_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='uploaded_documents',
        help_text="User who uploaded the document"
    )
    portfolio = models.ForeignKey(
        ClassPortfolio,
        on_delete=models.CASCADE,
        related_name='documents',
        null=True,
        blank=True,
        help_text="Associated portfolio (optional)"
    )
    
    # Status tracking
    is_processed = models.BooleanField(default=False, help_text="Whether document has been processed")
    processing_error = models.TextField(blank=True, help_text="Error message if processing failed")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'
    
    def __str__(self):
        return f"{self.filename} ({self.learn_method}) - {self.uploaded_by.username}"
    
    @property
    def is_successful(self):
        """Check if document processing was successful"""
        return self.learning_result.get('success', False)
    
    @property
    def summary_data(self):
        """Get summary data from learning result"""
        return self.learning_result.get('summary_data', {})
    
    @property
    def extracted_key_points(self):
        """Get key points from learning result"""
        return self.learning_result.get('summary_data', {}).get('key_points', [])


class DocumentQuiz(models.Model):
    """Model to store quiz data generated from documents"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='document_quizzes')
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='document_quizzes', null=True, blank=True)
    filename = models.CharField(max_length=255, help_text="Original filename of the document")
    topic = models.CharField(max_length=255, help_text="Quiz topic/subject")
    total_questions = models.IntegerField(help_text="Total number of questions in the quiz")
    text_length = models.IntegerField(help_text="Length of the source text")
    word_count = models.IntegerField(help_text="Word count of the source text")
    quiz_data = models.JSONField(default=dict, help_text="Complete quiz data including questions and answers")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Document Quiz'
        verbose_name_plural = 'Document Quizzes'
    
    def __str__(self):
        return f"{self.topic} - {self.user.username} ({self.total_questions} questions)"
    
    @property
    def questions(self):
        """Get quiz questions from quiz_data"""
        return self.quiz_data.get('quiz', {}).get('questions', [])
    
    @property
    def metadata(self):
        """Get quiz metadata from quiz_data"""
        return self.quiz_data.get('metadata', {})
    
    @property
    def is_successful(self):
        """Check if quiz generation was successful"""
        return self.quiz_data.get('success', False)


def validate_safe_url(value):
    """
    Validator to ensure URLs are safe and appropriate for learning content.
    Blocks known adult content, gambling, and other inappropriate sites.
    """
    # List of blocked domains and keywords (expandable)
    blocked_patterns = [
        # Adult content
        r'porn', r'xxx', r'adult', r'sex', r'nsfw', r'onlyfans',
        r'xvideos', r'pornhub', r'xhamster', r'redtube', r'youporn',
        # Gambling
        r'casino', r'gambling', r'poker', r'betting',
        # Other inappropriate
        r'gore', r'shock', r'extreme',
    ]
    
    url_lower = value.lower()
    
    for pattern in blocked_patterns:
        if re.search(pattern, url_lower):
            raise ValidationError(
                f'This URL contains inappropriate content and cannot be added as a learning resource.',
                code='unsafe_url'
            )
    
    # Basic URL validation
    url_validator = URLValidator()
    url_validator(value)
    
    return value


class YouTubeVideo(models.Model):
    """Model to store learning resource URLs associated with users.
    Note: Despite the name, this model now accepts any safe educational URL, not just YouTube.
    The name is kept for backward compatibility with existing database and API endpoints.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='youtube_videos')
    url = models.URLField(
        max_length=500, 
        validators=[validate_safe_url],
        help_text="Learning resource URL (YouTube, Coursera, articles, etc.)"
    )
    title = models.CharField(max_length=255, blank=True, help_text="Resource title (optional)")
    description = models.TextField(blank=True, help_text="Resource description (optional)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Learning Link'
        verbose_name_plural = 'Learning Links'
    
    def __str__(self):
        return f"{self.title or self.link_type} - {self.user.username}"
    
    @property
    def link_type(self):
        """Detect the type of learning resource from URL"""
        url_lower = self.url.lower()
        
        if 'youtube.com' in url_lower or 'youtu.be' in url_lower:
            return 'YouTube'
        elif 'vimeo.com' in url_lower:
            return 'Vimeo'
        elif 'coursera.org' in url_lower:
            return 'Coursera'
        elif 'udemy.com' in url_lower:
            return 'Udemy'
        elif 'khanacademy.org' in url_lower:
            return 'Khan Academy'
        elif 'edx.org' in url_lower:
            return 'edX'
        elif 'medium.com' in url_lower:
            return 'Medium'
        elif 'github.com' in url_lower:
            return 'GitHub'
        elif 'stackoverflow.com' in url_lower:
            return 'Stack Overflow'
        elif 'wikipedia.org' in url_lower:
            return 'Wikipedia'
        elif 'mit.edu' in url_lower or 'stanford.edu' in url_lower or '.edu' in url_lower:
            return 'Educational'
        else:
            return 'Web Resource'
    
    @property
    def video_id(self):
        """Extract YouTube video ID from URL (for backward compatibility)"""
        if 'youtube.com' not in self.url.lower() and 'youtu.be' not in self.url.lower():
            return None
            
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
            r'youtube\.com\/v\/([^&\n?#]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, self.url)
            if match:
                return match.group(1)
        return None
    
    @property
    def thumbnail_url(self):
        """Generate thumbnail URL (primarily for YouTube, returns None for other links)"""
        video_id = self.video_id
        if video_id:
            return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        return None
    
    @property
    def embed_url(self):
        """Generate embed URL (primarily for YouTube, returns None for other links)"""
        video_id = self.video_id
        if video_id:
            return f"https://www.youtube.com/embed/{video_id}"
        return None


class CalendarEvent(models.Model):
    """Model to store calendar events (homework, tests, exams, etc.) for users"""
    
    EVENT_TYPE_CHOICES = [
        ('homework', 'Homework'),
        ('test', 'Test'),
        ('exam', 'Exam'),
        ('quiz', 'Quiz'),
        ('project', 'Project'),
        ('presentation', 'Presentation'),
        ('lab', 'Lab'),
        ('reading', 'Reading'),
        ('study_session', 'Study Session'),
        ('office_hours', 'Office Hours'),
        ('review_session', 'Review Session'),
        ('other', 'Other'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calendar_events')
    class_portfolio = models.ForeignKey(
        'ClassPortfolio', 
        on_delete=models.CASCADE, 
        related_name='calendar_events',
        null=True,
        blank=True,
        help_text="Optional: Link to a specific class"
    )
    
    # Basic Information
    title = models.CharField(max_length=255, help_text="Event title")
    description = models.TextField(blank=True, help_text="Event description (optional)")
    event_type = models.CharField(
        max_length=20, 
        choices=EVENT_TYPE_CHOICES, 
        default='other',
        help_text="Type of event"
    )
    
    # Date and Time
    due_date = models.DateTimeField(help_text="Due date/time for the event")
    reminder_time = models.DateTimeField(
        null=True, 
        blank=True,
        help_text="Optional: Time to send reminder"
    )
    
    # Status and Priority
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='not_started',
        help_text="Current status"
    )
    priority = models.CharField(
        max_length=10, 
        choices=PRIORITY_CHOICES, 
        default='medium',
        help_text="Priority level"
    )
    
    # Additional Information
    points = models.IntegerField(
        null=True, 
        blank=True,
        help_text="Points/grade weight (optional)"
    )
    location = models.CharField(
        max_length=255, 
        blank=True,
        help_text="Location of event (optional)"
    )
    
    # Learning Resources
    linked_resources = models.ManyToManyField(
        YouTubeVideo,
        blank=True,
        related_name='calendar_events',
        help_text="Learning resources linked to this event"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(
        null=True, 
        blank=True,
        help_text="When the event was completed"
    )
    
    class Meta:
        ordering = ['due_date']
        verbose_name = 'Calendar Event'
        verbose_name_plural = 'Calendar Events'
        indexes = [
            models.Index(fields=['user', 'due_date']),
            models.Index(fields=['event_type', 'due_date']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.get_event_type_display()} ({self.due_date.strftime('%Y-%m-%d')})"
    
    @property
    def is_overdue(self):
        """Check if the event is overdue"""
        if self.status in ['completed', 'submitted', 'graded', 'cancelled']:
            return False
        return timezone.now() > self.due_date
    
    @property
    def days_until_due(self):
        """Calculate days until due date"""
        delta = self.due_date - timezone.now()
        return delta.days
    
    @property
    def is_due_soon(self):
        """Check if event is due within 24 hours"""
        if self.status in ['completed', 'submitted', 'graded', 'cancelled']:
            return False
        days = self.days_until_due
        return 0 <= days <= 1
    
    def mark_completed(self):
        """Mark event as completed"""
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()
    
    def add_learning_resource(self, resource):
        """Add a learning resource to this event"""
        self.linked_resources.add(resource)
    
    def remove_learning_resource(self, resource):
        """Remove a learning resource from this event"""
        self.linked_resources.remove(resource)