from django.core.management.base import BaseCommand
from core.models import Language, LessonCategory, DifficultyLevel, Achievement, DailyChallenge
from django.utils import timezone
import datetime

class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')
        
        # Create Languages
        languages = [
            {'name': 'Spanish', 'code': 'es', 'flag_emoji': '🇪🇸', 'order': 1},
            {'name': 'French', 'code': 'fr', 'flag_emoji': '🇫🇷', 'order': 2},
            {'name': 'German', 'code': 'de', 'flag_emoji': '🇩🇪', 'order': 3},
            {'name': 'Japanese', 'code': 'ja', 'flag_emoji': '🇯🇵', 'order': 4},
            {'name': 'Chinese', 'code': 'zh', 'flag_emoji': '🇨🇳', 'order': 5},
            {'name': 'Italian', 'code': 'it', 'flag_emoji': '🇮🇹', 'order': 6},
            {'name': 'Portuguese', 'code': 'pt', 'flag_emoji': '🇧🇷', 'order': 7},
        ]
        
        for lang_data in languages:
            Language.objects.get_or_create(
                code=lang_data['code'],
                defaults=lang_data
            )
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(languages)} languages'))
        
        # Create Lesson Categories
        categories = [
            {'name': 'Speaking', 'icon': 'fa-comments', 'description': 'Practice conversation and pronunciation', 'color': '#6366f1'},
            {'name': 'Reading', 'icon': 'fa-book', 'description': 'Improve reading comprehension', 'color': '#8b5cf6'},
            {'name': 'Writing', 'icon': 'fa-pen', 'description': 'Learn to write in your target language', 'color': '#10b981'},
            {'name': 'Listening', 'icon': 'fa-headphones', 'description': 'Train your listening skills', 'color': '#f59e0b'},
            {'name': 'Vocabulary', 'icon': 'fa-spell-check', 'description': 'Expand your word bank', 'color': '#ec4899'},
            {'name': 'Grammar', 'icon': 'fa-graduation-cap', 'description': 'Master grammar rules', 'color': '#06b6d4'},
        ]
        
        for cat_data in categories:
            LessonCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(categories)} lesson categories'))
        
        # Create Difficulty Levels
        difficulties = [
            {'name': 'Beginner', 'order': 1, 'color': '#10b981'},
            {'name': 'Intermediate', 'order': 2, 'color': '#f59e0b'},
            {'name': 'Advanced', 'order': 3, 'color': '#ef4444'},
        ]
        
        for diff_data in difficulties:
            DifficultyLevel.objects.get_or_create(
                name=diff_data['name'],
                defaults=diff_data
            )
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(difficulties)} difficulty levels'))
        
        # Create Achievements
        achievements = [
            {'name': 'First Steps', 'description': 'Complete your first lesson', 'icon': 'fa-play', 'xp_reward': 50, 'requirement_type': 'first_lesson', 'requirement_value': 1, 'category': 'progress'},
            {'name': 'Quick Learner', 'description': 'Complete 5 lessons', 'icon': 'fa-star', 'xp_reward': 100, 'requirement_type': 'five_lessons', 'requirement_value': 5, 'category': 'progress'},
            {'name': 'Dedicated Student', 'description': 'Complete 10 lessons', 'icon': 'fa-graduation-cap', 'xp_reward': 200, 'requirement_type': 'ten_lessons', 'requirement_value': 10, 'category': 'progress'},
            {'name': 'Language Enthusiast', 'description': 'Complete 25 lessons', 'icon': 'fa-trophy', 'xp_reward': 500, 'requirement_type': 'twentyfive_lessons', 'requirement_value': 25, 'category': 'progress'},
            {'name': 'Week Warrior', 'description': 'Maintain a 7-day streak', 'icon': 'fa-fire', 'xp_reward': 150, 'requirement_type': 'week_streak', 'requirement_value': 7, 'category': 'streak'},
            {'name': 'Monthly Master', 'description': 'Maintain a 30-day streak', 'icon': 'fa-calendar', 'xp_reward': 500, 'requirement_type': 'month_streak', 'requirement_value': 30, 'category': 'streak'},
            {'name': 'Chatty Beginner', 'description': 'Send 50 messages', 'icon': 'fa-comments', 'xp_reward': 100, 'requirement_type': 'messages', 'requirement_value': 50, 'category': 'practice'},
            {'name': 'Conversation Pro', 'description': 'Send 200 messages', 'icon': 'fa-message', 'xp_reward': 300, 'requirement_type': 'messages', 'requirement_value': 200, 'category': 'practice'},
        ]
        
        for ach_data in achievements:
            Achievement.objects.get_or_create(
                name=ach_data['name'],
                defaults=ach_data
            )
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(achievements)} achievements'))
        
        # Create Today's Daily Challenge
        today = timezone.now().date()
        DailyChallenge.objects.get_or_create(
            date=today,
            defaults={
                'title': 'Daily Conversation',
                'description': 'Have 5 conversations with the AI tutor today',
                'language': Language.objects.get(code='es'),
                'xp_reward': 50,
                'is_active': True
            }
        )
        
        self.stdout.write(self.style.SUCCESS('Created daily challenge'))
        
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))