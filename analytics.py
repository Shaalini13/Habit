from datetime import datetime, timedelta
from typing import List, Dict
import matplotlib.pyplot as plt
from habit import Habit

class HabitAnalytics:
    @staticmethod
    def plot_completion_rates(habits: List[Habit]):
        """Plot completion rates for all habits."""
        names = [h.name for h in habits]
        rates = [h.get_completion_rate() for h in habits]
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(names, rates, color='skyblue')
        plt.title('Habit Completion Rates')
        plt.ylabel('Completion Rate (%)')
        plt.ylim(0, 100)
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                     f'{height:.1f}%',
                     ha='center', va='bottom')
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def plot_streaks(habits: List[Habit]):
        """Plot current and max streaks for all habits."""
        names = [h.name for h in habits]
        current_streaks = [h.streak for h in habits]
        max_streaks = [h.max_streak for h in habits]
        
        plt.figure(figsize=(10, 6))
        
        bar_width = 0.35
        index = range(len(names))
        
        bars1 = plt.bar(index, current_streaks, bar_width, label='Current Streak', color='lightgreen')
        bars2 = plt.bar([i + bar_width for i in index], max_streaks, bar_width, label='Max Streak', color='darkgreen')
        
        plt.title('Habit Streaks')
        plt.ylabel('Days')
        plt.xticks([i + bar_width / 2 for i in index], names, rotation=45, ha='right')
        plt.legend()
        
        # Add value labels on top of bars
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height,
                         f'{int(height)}',
                         ha='center', va='bottom')
        
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def weekly_completion_history(tracker, weeks: int = 8):
        """Generate weekly completion history for visualization."""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(weeks=weeks)
        
        # Group by week
        weekly_data = {}
        current_date = start_date
        
        while current_date <= end_date:
            week_start = current_date - timedelta(days=current_date.weekday())
            week_end = week_start + timedelta(days=6)
            week_key = f"{week_start.strftime('%Y-%m-%d')} to {week_end.strftime('%Y-%m-%d')}"
            
            weekly_data[week_key] = tracker.get_weekly_summary(week_start)
            current_date += timedelta(weeks=1)
        
        return weekly_data