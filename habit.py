from datetime import datetime, timedelta

class Habit:
    def __init__(self, name, description, frequency="daily"):
        """
        Initialize a habit with name, description, and tracking frequency.
        
        Args:
            name (str): Name of the habit
            description (str): Description of what the habit entails
            frequency (str): Tracking frequency - 'daily' or 'weekly'
        """
        self.name = name
        self.description = description
        self.frequency = frequency
        self.creation_date = datetime.now().date()
        self.completion_dates = []  # Stores dates when habit was completed
        self.streak = 0
        self.max_streak = 0
    
    def mark_complete(self, date=None):
        """
        Mark the habit as completed for a specific date.
        
        Args:
            date (date, optional): Date of completion. Defaults to today.
        """
        if date is None:
            date = datetime.now().date()
        
        if date not in self.completion_dates:
            self.completion_dates.append(date)
            self._update_streak(date)
    
    def _update_streak(self, current_date):
        """Update the current and max streak based on new completion."""
        if not self.completion_dates:
            self.streak = 0
            return
        
        # Sort dates to ensure chronological order
        sorted_dates = sorted(self.completion_dates)
        
        current_streak = 1
        max_streak = 1
        
        for i in range(1, len(sorted_dates)):
            prev_date = sorted_dates[i-1]
            curr_date = sorted_dates[i]
            
            if self.frequency == "daily":
                expected_next_date = prev_date + timedelta(days=1)
            else:  # weekly
                expected_next_date = prev_date + timedelta(weeks=1)
            
            if curr_date == expected_next_date:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 1
        
        self.streak = current_streak
        self.max_streak = max_streak
    
    def is_complete(self, date=None):
        """Check if habit was completed on a specific date."""
        if date is None:
            date = datetime.now().date()
        return date in self.completion_dates
    
    def get_completion_rate(self):
        """Calculate completion rate as a percentage."""
        if not self.completion_dates:
            return 0.0
        
        days_active = (datetime.now().date() - self.creation_date).days + 1
        if self.frequency == "weekly":
            days_active = days_active // 7 or 1
        
        completion_count = len(self.completion_dates)
        return (completion_count / days_active) * 100
    
    def __str__(self):
        return f"{self.name} ({self.frequency}): Current streak: {self.streak}, Max streak: {self.max_streak}"