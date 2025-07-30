import json
from datetime import datetime
from typing import Dict, List
from habit import Habit

class HabitStorage:
    @staticmethod
    def save_to_file(tracker, filename: str = "habit_data.json"):
        """Save habit data to a JSON file."""
        data = {
            'habits': [],
            'metadata': {
                'last_saved': datetime.now().isoformat()
            }
        }
        
        for habit in tracker.get_all_habits():
            habit_data = {
                'name': habit.name,
                'description': habit.description,
                'frequency': habit.frequency,
                'creation_date': habit.creation_date.isoformat(),
                'completion_dates': [d.isoformat() for d in habit.completion_dates]
            }
            data['habits'].append(habit_data)
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    @staticmethod
    def load_from_file(filename: str = "habit_data.json"):
        """Load habit data from a JSON file."""
        from tracker import HabitTracker
        
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            return HabitTracker()
        
        tracker = HabitTracker()
        
        for habit_data in data['habits']:
            habit = tracker.add_habit(
                name=habit_data['name'],
                description=habit_data.get('description', ""),
                frequency=habit_data.get('frequency', "daily")
            )
            
            habit.creation_date = datetime.fromisoformat(habit_data['creation_date']).date()
            habit.completion_dates = [
                datetime.fromisoformat(d).date() 
                for d in habit_data['completion_dates']
            ]
            
            # Recalculate streaks
            if habit.completion_dates:
                habit._update_streak(max(habit.completion_dates))
        
        return tracker