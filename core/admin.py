from django.contrib import admin
from .models import (
    UserProfile, Language, LessonCategory, DifficultyLevel, 
    Lesson, UserProgress, Achievement, UserAchievement, 
    ChatMessage, DailyChallenge, UserDailyChallenge
)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'preferred_language', 'current_streak', 'total_xp', 'level']
    list_filter = ['preferred_language', 'level']
    search_fields = ['user__username', 'user__email']

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'flag_emoji', 'is_active', 'order']
    list_editable = ['is_active', 'order']

@admin.register(LessonCategory)
class LessonCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'color']
    list_editable = ['icon', 'color']

@admin.register(DifficultyLevel)
class DifficultyLevelAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'color']
    list_editable = ['order', 'color']

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'language', 'category', 'difficulty', 'xp_reward', 'is_active']
    list_filter = ['language', 'category', 'difficulty', 'is_active']
    search_fields = ['title', 'description']
    list_editable = ['is_active', 'xp_reward']

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'status', 'score', 'time_spent_minutes']
    list_filter = ['status', 'lesson__language']
    search_fields = ['user__username', 'lesson__title']

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['name', 'xp_reward', 'requirement_type', 'requirement_value', 'category']
    list_filter = ['category']
    search_fields = ['name', 'description']

@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ['user', 'achievement', 'earned_at']
    list_filter = ['achievement']
    search_fields = ['user__username', 'achievement__name']

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'language', 'user_message', 'created_at']
    list_filter = ['language', 'created_at']
    search_fields = ['user__username', 'user_message']
    readonly_fields = ['created_at']

@admin.register(DailyChallenge)
class DailyChallengeAdmin(admin.ModelAdmin):
    list_display = ['title', 'language', 'xp_reward', 'date', 'is_active']
    list_editable = ['is_active', 'xp_reward']
    search_fields = ['title']

@admin.register(UserDailyChallenge)
class UserDailyChallengeAdmin(admin.ModelAdmin):
    list_display = ['user', 'challenge', 'completed', 'completed_at']
    list_filter = ['completed']
    search_fields = ['user__username']