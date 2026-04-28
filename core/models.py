from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    """Extended user profile with gamification features"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', default='default-avatar.png', blank=True)
    preferred_language = models.CharField(max_length=50, default='Spanish')
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    total_xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    last_practice_date = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def add_xp(self, amount):
        self.total_xp += amount
        # Level up every 1000 XP
        self.level = (self.total_xp // 1000) + 1
        self.save()

    def update_streak(self):
        today = timezone.now().date()
        if self.last_practice_date:
            if self.last_practice_date == today:
                return  # Already practiced today
            elif self.last_practice_date == today - timezone.timedelta(days=1):
                self.current_streak += 1
            else:
                self.current_streak = 1
        else:
            self.current_streak = 1
        
        if self.current_streak > self.longest_streak:
            self.longest_streak = self.current_streak
        
        self.last_practice_date = today
        self.save()


class Language(models.Model):
    """Supported languages"""
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10, unique=True)
    flag_emoji = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class LessonCategory(models.Model):
    """Lesson categories (Speaking, Reading, Writing, Listening)"""
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=50)
    description = models.TextField()
    color = models.CharField(max_length=20, default='#6366F1')

    class Meta:
        verbose_name_plural = 'Lesson Categories'

    def __str__(self):
        return self.name


class DifficultyLevel(models.Model):
    """Difficulty levels"""
    name = models.CharField(max_length=20)  # Beginner, Intermediate, Advanced
    order = models.IntegerField(default=0)
    color = models.CharField(max_length=20)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """Language lessons"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='lessons')
    category = models.ForeignKey(LessonCategory, on_delete=models.CASCADE, related_name='lessons')
    difficulty = models.ForeignKey(DifficultyLevel, on_delete=models.CASCADE, related_name='lessons')
    content = models.JSONField(default=dict)
    xp_reward = models.IntegerField(default=50)
    duration_minutes = models.IntegerField(default=15)
    order = models.IntegerField(default=0)
    is_premium = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['language', 'difficulty', 'order']

    def __str__(self):
        return f"{self.title} ({self.language.name})"


class UserProgress(models.Model):
    """Track user progress through lessons"""
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='user_progress')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    score = models.IntegerField(default=0)
    time_spent_minutes = models.IntegerField(default=0)
    attempts = models.IntegerField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'lesson']
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"


class Achievement(models.Model):
    """Achievements users can earn"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50)
    xp_reward = models.IntegerField(default=100)
    requirement_type = models.CharField(max_length=50)  # lessons_completed, streak_days, xp_total
    requirement_value = models.IntegerField()
    category = models.CharField(max_length=50, default='general')

    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    """Track earned achievements"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name='earners')
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'achievement']

    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"


class ChatMessage(models.Model):
    """AI Chat conversation history"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages')
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    user_message = models.TextField()
    ai_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.language.name}"


class DailyChallenge(models.Model):
    """Daily practice challenges"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    xp_reward = models.IntegerField(default=25)
    is_active = models.BooleanField(default=True)
    date = models.DateField(unique=True)

    def __str__(self):
        return self.title


class UserDailyChallenge(models.Model):
    """Track daily challenge completion"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_challenges')
    challenge = models.ForeignKey(DailyChallenge, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['user', 'challenge']

    def __str__(self):
        return f"{self.user.username} - {self.challenge.title}"