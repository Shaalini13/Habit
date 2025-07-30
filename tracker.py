from datetime import datetime, timedelta
from typing import Dict, List
from habit import Habit

class HabitTracker:
    def __init__(self):
        self.habits: Dict[str, Habit] = {}
    
    def add_habit(self, name: str, description: str = "", frequency: str = "daily") -> Habit:
        """Add a new habit to track."""
        if name in self.habits:
            raise ValueError(f"Habit '{name}' already exists")
        
        new_habit = Habit(name, description, frequency)
        self.habits[name] = new_habit
        return new_habit
    
    def remove_habit(self, name: str):
        """Remove a habit from tracking."""
        if name in self.habits:
            del self.habits[name]
    
    def complete_habit(self, name: str, date=None):
        """Mark a habit as completed for a specific date."""
        if name not in self.habits:
            raise ValueError(f"Habit '{name}' not found")
        
        self.habits[name].mark_complete(date)
    
    def get_habit(self, name: str) -> Habit:
        """Get a habit by name."""
        return self.habits.get(name)
    
    def get_all_habits(self) -> List[Habit]:
        """Get all habits being tracked."""
        return list(self.habits.values())
    
    def get_habits_by_frequency(self, frequency: str) -> List[Habit]:
        """Get habits filtered by tracking frequency."""
        return [h for h in self.habits.values() if h.frequency == frequency]
    
    def get_current_streaks(self) -> Dict[str, int]:
        """Get current streaks for all habits."""
        return {name: habit.streak for name, habit in self.habits.items()}
    
    def get_longest_streaks(self) -> Dict[str, int]:
        """Get longest streaks for all habits."""
        return {name: habit.max_streak for name, habit in self.habits.items()}
    
    def get_weekly_summary(self, week_start: datetime = None):
        """Generate a weekly summary of habit completion."""
        if week_start is None:
            week_start = datetime.now().date() - timedelta(days=datetime.now().weekday())
        
        week_end = week_start + timedelta(days=6)
        summary = {}
        
        for name, habit in self.habits.items():
            completions = [d for d in habit.completion_dates if week_start <= d <= week_end]
            summary[name] = {
                'completions': len(completions),
                'target': 1 if habit.frequency == "weekly" else 7,
                'streak': habit.streak
            }
        
        return summary