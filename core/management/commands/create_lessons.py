from django.core.management.base import BaseCommand
from core.models import Language, LessonCategory, DifficultyLevel, Lesson

class Command(BaseCommand):
    help = 'Create sample lessons'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample lessons...')
        
        # Get data
        spanish = Language.objects.get(name='Spanish')
        french = Language.objects.get(name='French')
        german = Language.objects.get(name='German')
        japanese = Language.objects.get(name='Japanese')
        chinese = Language.objects.get(name='Chinese')
        
        speaking = LessonCategory.objects.get(name='Speaking')
        reading = LessonCategory.objects.get(name='Reading')
        writing = LessonCategory.objects.get(name='Writing')
        listening = LessonCategory.objects.get(name='Listening')
        vocabulary = LessonCategory.objects.get(name='Vocabulary')
        grammar = LessonCategory.objects.get(name='Grammar')
        
        beginner = DifficultyLevel.objects.get(name='Beginner')
        intermediate = DifficultyLevel.objects.get(name='Intermediate')
        advanced = DifficultyLevel.objects.get(name='Advanced')
        
        lessons_data = [
            # Spanish Lessons
            {
                'title': 'Basic Greetings',
                'description': 'Learn essential Spanish greetings like Hola, Buenos días, and more.',
                'language': spanish,
                'category': speaking,
                'difficulty': beginner,
                'xp_reward': 50,
                'duration_minutes': 15,
                'order': 1,
                'content': {'topics': ['greetings', 'introductions']}
            },
            {
                'title': 'Numbers 1-100',
                'description': 'Master counting in Spanish from one to one hundred.',
                'language': spanish,
                'category': vocabulary,
                'difficulty': beginner,
                'xp_reward': 50,
                'duration_minutes': 20,
                'order': 2,
                'content': {'topics': ['numbers', 'counting']}
            },
            {
                'title': 'Common Phrases',
                'description': 'Learn the most common Spanish phrases for daily conversation.',
                'language': spanish,
                'category': speaking,
                'difficulty': beginner,
                'xp_reward': 75,
                'duration_minutes': 25,
                'order': 3,
                'content': {'topics': ['phrases', 'daily_use']}
            },
            {
                'title': 'Past Tense Basics',
                'description': 'Introduction to the preterite tense in Spanish.',
                'language': spanish,
                'category': grammar,
                'difficulty': intermediate,
                'xp_reward': 100,
                'duration_minutes': 30,
                'order': 4,
                'content': {'topics': ['preterite', 'past_tense']}
            },
            {
                'title': 'Subjunctive Mood',
                'description': 'Master the Spanish subjunctive for advanced expression.',
                'language': spanish,
                'category': grammar,
                'difficulty': advanced,
                'xp_reward': 150,
                'duration_minutes': 45,
                'order': 5,
                'content': {'topics': ['subjunctive', 'mood']}
            },
            # French Lessons
            {
                'title': 'French Greetings',
                'description': 'Learn essential French greetings and polite expressions.',
                'language': french,
                'category': speaking,
                'difficulty': beginner,
                'xp_reward': 50,
                'duration_minutes': 15,
                'order': 1,
                'content': {'topics': ['greetings', 'politeness']}
            },
            {
                'title': 'French Numbers',
                'description': 'Count from 1 to 100 in French.',
                'language': french,
                'category': vocabulary,
                'difficulty': beginner,
                'xp_reward': 50,
                'duration_minutes': 20,
                'order': 2,
                'content': {'topics': ['numbers', 'counting']}
            },
            {
                'title': 'Passé Composé',
                'description': 'Learn the French past tense for storytelling.',
                'language': french,
                'category': grammar,
                'difficulty': intermediate,
                'xp_reward': 100,
                'duration_minutes': 30,
                'order': 3,
                'content': {'topics': ['passe_compose', 'past_tense']}
            },
            # German Lessons
            {
                'title': 'German Basics',
                'description': 'Essential German phrases for beginners.',
                'language': german,
                'category': speaking,
                'difficulty': beginner,
                'xp_reward': 50,
                'duration_minutes': 15,
                'order': 1,
                'content': {'topics': ['basics', 'greetings']}
            },
            {
                'title': 'German Cases',
                'description': 'Master the nominative, accusative, dative, and genitive cases.',
                'language': german,
                'category': grammar,
                'difficulty': intermediate,
                'xp_reward': 150,
                'duration_minutes': 40,
                'order': 2,
                'content': {'topics': ['cases', 'grammar']}
            },
            # Japanese Lessons
            {
                'title': 'Hiragana Basics',
                'description': 'Learn to read and write Hiragana characters.',
                'language': japanese,
                'category': reading,
                'difficulty': beginner,
                'xp_reward': 75,
                'duration_minutes': 25,
                'order': 1,
                'content': {'topics': ['hiragana', 'writing']}
            },
            {
                'title': 'Katakana Introduction',
                'description': 'Learn Katakana for foreign words.',
                'language': japanese,
                'category': reading,
                'difficulty': beginner,
                'xp_reward': 75,
                'duration_minutes': 25,
                'order': 2,
                'content': {'topics': ['katakana', 'writing']}
            },
            {
                'title': 'Japanese Particles',
                'description': 'Master essential Japanese particles like は, が, を.',
                'language': japanese,
                'category': grammar,
                'difficulty': intermediate,
                'xp_reward': 100,
                'duration_minutes': 30,
                'order': 3,
                'content': {'topics': ['particles', 'grammar']}
            },
            # Chinese Lessons
            {
                'title': 'Chinese Characters',
                'description': 'Introduction to reading and writing Chinese characters.',
                'language': chinese,
                'category': reading,
                'difficulty': beginner,
                'xp_reward': 75,
                'duration_minutes': 25,
                'order': 1,
                'content': {'topics': ['characters', 'writing']}
            },
            {
                'title': 'Chinese Tones',
                'description': 'Master the four tones in Mandarin Chinese.',
                'language': chinese,
                'category': speaking,
                'difficulty': beginner,
                'xp_reward': 75,
                'duration_minutes': 20,
                'order': 2,
                'content': {'topics': ['tones', 'pronunciation']}
            },
        ]
        
        for lesson_data in lessons_data:
            Lesson.objects.get_or_create(
                title=lesson_data['title'],
                language=lesson_data['language'],
                defaults=lesson_data
            )
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(lessons_data)} lessons'))
        self.stdout.write(self.style.SUCCESS('Lessons created successfully!'))