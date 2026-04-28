from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
import random

from .models import (
    UserProfile, Language, LessonCategory, DifficultyLevel, 
    Lesson, UserProgress, Achievement, UserAchievement, 
    ChatMessage, DailyChallenge, UserDailyChallenge
)
from .forms import RegisterForm, LoginForm, UserProfileForm, UserForm


# AI Responses for chatbot
AI_RESPONSES = {
    'Spanish': {
        'greetings': [
            "¡Hola! ¿Cómo estás hoy? Let's practice some Spanish.",
            "¡Bienvenido! I'm here to help you learn Spanish.",
            "¡Hola! What would you like to practice today?"
        ],
        'default': [
            "That's great! Try saying: '{phrase}'",
            "Good attempt! Let me give you a tip: {tip}",
            "Interesting! In Spanish, we say: '{translation}'"
        ]
    },
    'French': {
        'greetings': [
            "Bonjour! Comment allez-vous aujourd'hui?",
            "Bienvenue! Let's practice some French together.",
            "Salut! What would you like to learn today?"
        ],
        'default': [
            "Bien joué! Try: '{phrase}'",
            "Bon effort! Remember: {tip}",
            "Intéressant! In French: '{translation}'"
        ]
    },
    'German': {
        'greetings': [
            "Guten Tag! Wie geht es Ihnen heute?",
            "Willkommen! Let's practice German together.",
            "Hallo! Was möchten Sie heute üben?"
        ],
        'default': [
            "Gut gemacht! Try: '{phrase}'",
            "Guter Versuch! Tipp: {tip}",
            "Interessant! Auf Deutsch: '{translation}'"
        ]
    },
    'Japanese': {
        'greetings': [
            "こんにちは! How can I help you today?",
            "ようこそ! Let's practice Japanese.",
            "やあ! What would you like to learn?"
        ],
        'default': [
            "很好的尝试! Say: '{phrase}'",
            "不错! Remember: {tip}",
            "In Japanese: '{translation}'"
        ]
    },
    'Chinese': {
        'greetings': [
            "你好! Let's practice Chinese together.",
            "欢迎! What would you like to learn today?",
            "你好! How can I help you?"
        ],
        'default': [
            "很好! Try: '{phrase}'",
            "不错! Tip: {tip}",
            "In Chinese: '{translation}'"
        ]
    }
}

TIPS = {
    'Spanish': [
        'Remember to roll your "r" sounds',
        'Practice the gender of nouns (el/la)',
        'Use "ser" for permanent traits and "estar" for temporary states'
    ],
    'French': [
        'Remember to liaison - link final consonants to next word',
        'The "r" sound comes from the back of your throat',
        'Watch out for silent letters at the end of words'
    ],
    'German': [
        'Compound words are common - try breaking them down',
        'Remember the three genders: der, die, das',
        'Verb at position 2 in main clauses'
    ],
    'Japanese': [
        'Use polite forms (です/ます) in formal settings',
        'Remember: Hiragana for grammar, Katakana for foreign words',
        'Context matters - the same word can have different meanings'
    ],
    'Chinese': [
        'Tones are crucial - practice each one carefully',
        'Characters carry meaning, not just sound',
        'Word order is similar to English (Subject-Verb-Object)'
    ]
}

SAMPLE_PHRASES = {
    'Spanish': ['Hola, ¿cómo estás?', 'Me llamo...', 'Mucho gusto', 'Gracias', 'Por favor'],
    'French': ['Bonjour, comment ça va?', 'Je m\'appelle...', 'Enchanté', 'Merci', 'S\'il vous plaît'],
    'German': ['Guten Tag, wie geht es Ihnen?', 'Ich heiße...', 'Freut mich', 'Danke', 'Bitte'],
    'Japanese': ['こんにちは', '私の名前は...', 'はじめまして', 'ありがとう', 'お願いします'],
    'Chinese': ['你好', '我叫...', '很高兴认识你', '谢谢', '请']
}


def index(request):
    """Landing page"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    languages = Language.objects.filter(is_active=True)[:5]
    categories = LessonCategory.objects.all()
    achievements = Achievement.objects.all()[:6]
    
    context = {
        'languages': languages,
        'categories': categories,
        'achievements': achievements
    }
    return render(request, 'index.html', context)


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or username}!')
                return redirect('dashboard')
        messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})


def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to LinguaAI.')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form})


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('index')


@login_required
def dashboard(request):
    """User dashboard with progress and stats"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=request.user)
        profile = request.user.profile
    
    # Get user progress
    completed_lessons = UserProgress.objects.filter(
        user=request.user, 
        status='completed'
    ).count()
    
    in_progress_lessons = UserProgress.objects.filter(
        user=request.user, 
        status='in_progress'
    ).count()
    
    # Get recent activity
    recent_progress = UserProgress.objects.filter(
        user=request.user
    ).select_related('lesson')[:5]
    
    # Get achievements
    user_achievements = UserAchievement.objects.filter(
        user=request.user
    ).select_related('achievement')[:6]
    
    # Get all achievements to show locked ones
    all_achievements = Achievement.objects.all()[:6]
    earned_ids = set(user_achievements.values_list('achievement_id', flat=True))
    
    # Get recommended lessons
    recommended = Lesson.objects.filter(
        language__name=profile.preferred_language,
        is_active=True
    ).exclude(
        user_progress__user=request.user,
        user_progress__status='completed'
    )[:4]
    
    # Get today's challenge
    today = timezone.now().date()
    daily_challenge = DailyChallenge.objects.filter(date=today).first()
    challenge_completed = False
    if daily_challenge:
        challenge_completed = UserDailyChallenge.objects.filter(
            user=request.user,
            challenge=daily_challenge,
            completed=True
        ).exists()
    
    # Calculate daily goal progress (target: 3 lessons per day)
    daily_goal = 3
    today_lessons = UserProgress.objects.filter(
        user=request.user,
        completed_at__date=today,
        status='completed'
    ).count()
    daily_progress = min(today_lessons / daily_goal * 100, 100)
    
    context = {
        'profile': profile,
        'completed_lessons': completed_lessons,
        'in_progress_lessons': in_progress_lessons,
        'recent_progress': recent_progress,
        'user_achievements': user_achievements,
        'all_achievements': all_achievements,
        'earned_ids': earned_ids,
        'recommended': recommended,
        'daily_challenge': daily_challenge,
        'challenge_completed': challenge_completed,
        'daily_progress': daily_progress,
        'daily_goal': daily_goal,
    }
    return render(request, 'dashboard.html', context)


@login_required
def lessons(request):
    """Lessons browsing page"""
    # Get filter parameters
    language_filter = request.GET.get('language')
    category_filter = request.GET.get('category')
    difficulty_filter = request.GET.get('difficulty')
    
    # Get all filters
    languages = Language.objects.filter(is_active=True)
    categories = LessonCategory.objects.all()
    difficulties = DifficultyLevel.objects.all()
    
    # Build query
    lessons = Lesson.objects.filter(is_active=True).select_related(
        'language', 'category', 'difficulty'
    )
    
    if language_filter:
        lessons = lessons.filter(language__name=language_filter)
    if category_filter:
        lessons = lessons.filter(category__name=category_filter)
    if difficulty_filter:
        lessons = lessons.filter(difficulty__name=difficulty_filter)
    
    # Get user progress for each lesson
    user_progress = {}
    for progress in UserProgress.objects.filter(user=request.user):
        user_progress[progress.lesson_id] = progress
    
    # Add progress to lessons
    lessons_list = []
    for lesson in lessons:
        progress = user_progress.get(lesson.id)
        lessons_list.append({
            'lesson': lesson,
            'progress': progress
        })
    
    context = {
        'lessons_list': lessons_list,
        'languages': languages,
        'categories': categories,
        'difficulties': difficulties,
        'selected_language': language_filter,
        'selected_category': category_filter,
        'selected_difficulty': difficulty_filter,
    }
    return render(request, 'lessons.html', context)


@login_required
def practice(request):
    """AI Practice page with chatbot"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=request.user)
        profile = request.user.profile
    
    # Get recent chat history
    chat_history = ChatMessage.objects.filter(
        user=request.user,
        language__name=profile.preferred_language
    )[:10]
    
    # Get today's challenge
    today = timezone.now().date()
    daily_challenge = DailyChallenge.objects.filter(date=today).first()
    challenge_completed = False
    if daily_challenge:
        challenge_completed = UserDailyChallenge.objects.filter(
            user=request.user,
            challenge=daily_challenge,
            completed=True
        ).exists()
    
    context = {
        'profile': profile,
        'chat_history': chat_history,
        'daily_challenge': daily_challenge,
        'challenge_completed': challenge_completed,
    }
    return render(request, 'practice.html', context)


@login_required
def profile(request):
    """User profile page"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=request.user)
        profile = request.user.profile
    
    # Get user stats
    completed_lessons = UserProgress.objects.filter(
        user=request.user, 
        status='completed'
    ).count()
    
    total_time = UserProgress.objects.filter(
        user=request.user
    ).aggregate(total=models.Sum('time_spent_minutes'))['total'] or 0
    
    # Get achievements
    achievements = UserAchievement.objects.filter(
        user=request.user
    ).select_related('achievement')
    
    # Get all achievements
    all_achievements = Achievement.objects.all()
    earned_ids = set(achievements.values_list('achievement_id', flat=True))
    
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)
    
    context = {
        'profile': profile,
        'completed_lessons': completed_lessons,
        'total_time': total_time,
        'achievements': achievements,
        'all_achievements': all_achievements,
        'earned_ids': earned_ids,
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'profile.html', context)


@csrf_exempt
def chat_api(request):
    """API for AI chatbot"""
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')
        language = data.get('language', 'Spanish')
        
        # Get user profile for XP
        try:
            profile = request.user.profile
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=request.user)
            profile = request.user.profile
        
        # Generate AI response
        lang_responses = AI_RESPONSES.get(language, AI_RESPONSES['Spanish'])
        lang_tips = TIPS.get(language, TIPS['Spanish'])
        phrases = SAMPLE_PHRASES.get(language, SAMPLE_PHRASES['Spanish'])
        
        # Check for greetings
        greetings = ['hola', 'hello', 'hi', 'bonjour', 'guten tag', 'konnichiwa', 'nihao']
        is_greeting = any(greet in user_message.lower() for greet in greetings)
        
        if is_greeting:
            response = random.choice(lang_responses['greetings'])
        else:
            # Generate contextual response
            tip = random.choice(lang_tips)
            phrase = random.choice(phrases)
            response = random.choice(lang_responses['default']).format(
                phrase=phrase,
                tip=tip,
                translation=f"'{user_message}' in {language}"
            )
        
        # Save chat message
        lang_obj = Language.objects.filter(name=language).first()
        if lang_obj:
            ChatMessage.objects.create(
                user=request.user,
                language=lang_obj,
                user_message=user_message,
                ai_response=response
            )
        
        # Update user streak and give XP
        profile.update_streak()
        profile.add_xp(5)  # 5 XP per message
        
        return JsonResponse({
            'response': response,
            'xp': profile.total_xp,
            'streak': profile.current_streak
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def progress_api(request):
    """API for updating lesson progress"""
    if request.method == 'POST':
        data = json.loads(request.body)
        lesson_id = data.get('lesson_id')
        status = data.get('status')
        score = data.get('score', 0)
        
        try:
            lesson = Lesson.objects.get(id=lesson_id)
            profile = request.user.profile
            
            # Update or create progress
            progress, created = UserProgress.objects.update_or_create(
                user=request.user,
                lesson=lesson,
                defaults={
                    'status': status,
                    'score': score,
                    'completed_at': timezone.now() if status == 'completed' else None
                }
            )
            
            # Give XP for completion
            if status == 'completed' and not created:
                # Only give XP first time
                pass
            elif status == 'completed':
                profile.add_xp(lesson.xp_reward)
                profile.update_streak()
            
            # Check for new achievements
            new_achievements = []
            completed_count = UserProgress.objects.filter(
                user=request.user,
                status='completed'
            ).count()
            
            # Check lesson completion achievements
            achievement_checks = [
                ('first_lesson', 1, 'First Steps', 'Complete your first lesson'),
                ('five_lessons', 5, 'Quick Learner', 'Complete 5 lessons'),
                ('ten_lessons', 10, 'Dedicated Student', 'Complete 10 lessons'),
                ('twentyfive_lessons', 25, 'Language Enthusiast', 'Complete 25 lessons'),
            ]
            
            for req_type, req_val, name, desc in achievement_checks:
                if completed_count >= req_val:
                    achievement = Achievement.objects.filter(
                        requirement_type=req_type,
                        requirement_value=req_val
                    ).first()
                    
                    if achievement and not UserAchievement.objects.filter(
                        user=request.user,
                        achievement=achievement
                    ).exists():
                        UserAchievement.objects.create(
                            user=request.user,
                            achievement=achievement
                        )
                        new_achievements.append(achievement)
            
            return JsonResponse({
                'success': True,
                'xp': profile.total_xp,
                'level': profile.level,
                'streak': profile.current_streak,
                'new_achievements': [
                    {'name': a.name, 'description': a.description, 'xp': a.xp_reward}
                    for a in new_achievements
                ]
            })
            
        except Lesson.DoesNotExist:
            return JsonResponse({'error': 'Lesson not found'}, status=404)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)