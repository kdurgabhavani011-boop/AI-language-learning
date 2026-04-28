// LinguaAI - Gamification JavaScript

class Gamification {
    constructor() {
        this.xp = 0;
        this.level = 1;
        this.streak = 0;
        this.achievements = [];
        this.dailyGoal = 3;
        this.init();
    }
    
    init() {
        this.loadUserData();
        this.setupEventListeners();
        this.updateUI();
    }
    
    loadUserData() {
        const userData = storage.get('user_gamification');
        if (userData) {
            this.xp = userData.xp || 0;
            this.level = userData.level || 1;
            this.streak = userData.streak || 0;
            this.achievements = userData.achievements || [];
        }
    }
    
    saveUserData() {
        storage.set('user_gamification', {
            xp: this.xp,
            level: this.level,
            streak: this.streak,
            achievements: this.achievements
        });
    }
    
    setupEventListeners() {
        // Listen for XP gains
        document.addEventListener('xpGained', (e) => {
            this.addXP(e.detail.amount);
        });
        
        // Listen for achievements
        document.addEventListener('achievementEarned', (e) => {
            this.unlockAchievement(e.detail.achievement);
        });
    }
    
    addXP(amount) {
        const oldLevel = this.level;
        this.xp += amount;
        this.level = Math.floor(this.xp / 1000) + 1;
        
        // Check for level up
        if (this.level > oldLevel) {
            this.showLevelUp(oldLevel, this.level);
        }
        
        this.saveUserData();
        this.updateUI();
        
        // Dispatch event
        document.dispatchEvent(new CustomEvent('xpGained', { 
            detail: { amount, total: this.xp, level: this.level } 
        }));
    }
    
    updateStreak() {
        const lastPractice = storage.get('last_practice_date');
        const today = new Date().toDateString();
        
        if (lastPractice === today) {
            return; // Already practiced today
        }
        
        const yesterday = new Date();
        yesterday.setDate(yesterday.getDate() - 1);
        
        if (lastPractice === yesterday.toDateString()) {
            this.streak++;
        } else if (lastPractice !== today) {
            this.streak = 1;
        }
        
        storage.set('last_practice_date', today);
        this.saveUserData();
        this.updateUI();
    }
    
    unlockAchievement(achievement) {
        if (!this.achievements.includes(achievement.id)) {
            this.achievements.push(achievement.id);
            this.addXP(achievement.xpReward);
            this.showAchievement(achievement);
        }
    }
    
    updateUI() {
        // Update XP display
        const xpElements = document.querySelectorAll('[data-xp]');
        xpElements.forEach(el => {
            el.textContent = this.xp;
        });
        
        // Update level display
        const levelElements = document.querySelectorAll('[data-level]');
        levelElements.forEach(el => {
            el.textContent = this.level;
        });
        
        // Update streak display
        const streakElements = document.querySelectorAll('[data-streak]');
        streakElements.forEach(el => {
            el.textContent = this.streak;
        });
        
        // Update progress bar
        const progressFill = document.querySelector('.xp-progress-fill');
        if (progressFill) {
            const levelProgress = (this.xp % 1000) / 10;
            progressFill.style.width = levelProgress + '%';
        }
    }
    
    showLevelUp(oldLevel, newLevel) {
        const notification = document.createElement('div');
        notification.className = 'notification level-up-notification';
        notification.innerHTML = `
            <div class="notification-content">
                <div class="level-up-icon">🎉</div>
                <div class="level-up-text">
                    <h3>Level Up!</h3>
                    <p>You've reached Level ${newLevel}!</p>
                </div>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);
        
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 5000);
    }
    
    showAchievement(achievement) {
        const notification = document.createElement('div');
        notification.className = 'notification achievement-notification';
        notification.innerHTML = `
            <div class="notification-content">
                <div class="achievement-icon">
                    <i class="fas fa-${achievement.icon || 'trophy'}"></i>
                </div>
                <div class="achievement-text">
                    <h3>Achievement Unlocked!</h3>
                    <p>${achievement.name}</p>
                    <span>+${achievement.xpReward} XP</span>
                </div>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);
        
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 5000);
    }
    
    checkAchievements(completedLessons, totalXP) {
        const achievements = [
            { id: 'first_lesson', name: 'First Steps', icon: 'play', xpReward: 50, requirement: 1, type: 'lessons' },
            { id: 'five_lessons', name: 'Quick Learner', icon: 'star', xpReward: 100, requirement: 5, type: 'lessons' },
            { id: 'ten_lessons', name: 'Dedicated Student', icon: 'graduation-cap', xpReward: 200, requirement: 10, type: 'lessons' },
            { id: 'week_streak', name: 'Week Warrior', icon: 'fire', xpReward: 150, requirement: 7, type: 'streak' },
            { id: 'month_streak', name: 'Monthly Master', icon: 'calendar', xpReward: 500, requirement: 30, type: 'streak' },
            { id: 'xp_1000', name: 'XP Hunter', icon: 'coins', xpReward: 100, requirement: 1000, type: 'xp' },
            { id: 'xp_5000', name: 'XP Master', icon: 'crown', xpReward: 500, requirement: 5000, type: 'xp' }
        ];
        
        achievements.forEach(achievement => {
            let earned = false;
            
            switch (achievement.type) {
                case 'lessons':
                    earned = completedLessons >= achievement.requirement;
                    break;
                case 'streak':
                    earned = this.streak >= achievement.requirement;
                    break;
                case 'xp':
                    earned = this.xp >= achievement.requirement;
                    break;
            }
            
            if (earned && !this.achievements.includes(achievement.id)) {
                this.unlockAchievement(achievement);
            }
        });
    }
}

// Daily Challenge System
class DailyChallenge {
    constructor() {
        this.challenges = this.getDailyChallenges();
        this.init();
    }
    
    init() {
        this.loadProgress();
        this.checkDailyReset();
    }
    
    getDailyChallenges() {
        return [
            {
                id: 'practice_30',
                title: '30-Minute Practice',
                description: 'Practice for at least 30 minutes today',
                xpReward: 50,
                type: 'time',
                requirement: 30
            },
            {
                id: 'complete_3',
                title: 'Triple Threat',
                description: 'Complete 3 lessons today',
                xpReward: 75,
                type: 'lessons',
                requirement: 3
            },
            {
                id: 'chat_10',
                title: 'Chatty Cathy',
                description: 'Have 10 conversations with the AI',
                xpReward: 60,
                type: 'messages',
                requirement: 10
            },
            {
                id: 'perfect_score',
                title: 'Perfectionist',
                description: 'Get a perfect score on any lesson',
                xpReward: 100,
                type: 'perfect',
                requirement: 100
            }
        ];
    }
    
    loadProgress() {
        this.progress = storage.get('daily_challenge_progress') || {
            date: null,
            completed: [],
            stats: { lessons: 0, time: 0, messages: 0 }
        };
    }
    
    saveProgress() {
        storage.set('daily_challenge_progress', this.progress);
    }
    
    checkDailyReset() {
        const today = new Date().toDateString();
        
        if (this.progress.date !== today) {
            // New day, reset progress
            this.progress = {
                date: today,
                completed: [],
                stats: { lessons: 0, time: 0, messages: 0 }
            };
            this.saveProgress();
        }
    }
    
    updateStats(type, value) {
        this.progress.stats[type] += value;
        this.saveProgress();
        this.checkChallenges();
    }
    
    checkChallenges() {
        this.challenges.forEach(challenge => {
            if (this.progress.completed.includes(challenge.id)) return;
            
            let completed = false;
            
            switch (challenge.type) {
                case 'time':
                    completed = this.progress.stats.time >= challenge.requirement;
                    break;
                case 'lessons':
                    completed = this.progress.stats.lessons >= challenge.requirement;
                    break;
                case 'messages':
                    completed = this.progress.stats.messages >= challenge.requirement;
                    break;
            }
            
            if (completed) {
                this.completeChallenge(challenge);
            }
        });
    }
    
    completeChallenge(challenge) {
        this.progress.completed.push(challenge.id);
        this.saveProgress();
        
        // Dispatch event
        document.dispatchEvent(new CustomEvent('challengeCompleted', {
            detail: challenge
        }));
    }
    
    getTodayChallenge() {
        const dayOfYear = Math.floor((new Date() - new Date(new Date().getFullYear(), 0, 0)) / 86400000);
        return this.challenges[dayOfYear % this.challenges.length];
    }
}

// Leaderboard
class Leaderboard {
    constructor() {
        this.init();
    }
    
    init() {
        this.loadData();
    }
    
    loadData() {
        this.data = storage.get('leaderboard_data') || this.getDefaultData();
    }
    
    getDefaultData() {
        return [
            { rank: 1, name: 'LanguagePro', xp: 15000, level: 15, avatar: '👨‍🏫' },
            { rank: 2, name: 'Polyglot123', xp: 12500, level: 13, avatar: '👩‍💻' },
            { rank: 3, name: 'WordMaster', xp: 10000, level: 10, avatar: '🧑‍🎓' },
            { rank: 4, name: 'FluentFox', xp: 8500, level: 9, avatar: '🦊' },
            { rank: 5, name: 'LinguaLion', xp: 7000, level: 7, avatar: '🦁' }
        ];
    }
    
    getUserRank(xp) {
        const sorted = [...this.data].sort((a, b) => b.xp - a.xp);
        return sorted.findIndex(user => xp >= user.xp) + 1;
    }
    
    getTopUsers(limit = 5) {
        return this.data.slice(0, limit);
    }
}

// Initialize gamification
document.addEventListener('DOMContentLoaded', function() {
    window.gamification = new Gamification();
    window.dailyChallenge = new DailyChallenge();
    window.leaderboard = new Leaderboard();
});

// Export
window.Gamification = Gamification;
window.DailyChallenge = DailyChallenge;
window.Leaderboard = Leaderboard;