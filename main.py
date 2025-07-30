from tracker import HabitTracker
from storage import HabitStorage
from analytics import HabitAnalytics
from datetime import datetime, timedelta
import sys

def main():
    # Initialize tracker with saved data
    tracker = HabitStorage.load_from_file()
    
    while True:
        print("\nHabit Tracker Menu:")
        print("1. Add new habit")
        print("2. Mark habit complete")
        print("3. View all habits")
        print("4. View weekly summary")
        print("5. View analytics")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ")
        
        if choice == "1":
            add_new_habit(tracker)
        elif choice == "2":
            mark_habit_complete(tracker)
        elif choice == "3":
            view_all_habits(tracker)
        elif choice == "4":
            view_weekly_summary(tracker)
        elif choice == "5":
            view_analytics(tracker)
        elif choice == "6":
            HabitStorage.save_to_file(tracker)
            print("Data saved. Goodbye!")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

def add_new_habit(tracker):
    print("\nAdd New Habit")
    name = input("Enter habit name: ")
    description = input("Enter habit description (optional): ")
    
    while True:
        frequency = input("Enter frequency (daily/weekly): ").lower()
        if frequency in ['daily', 'weekly']:
            break
        print("Invalid frequency. Please enter 'daily' or 'weekly'.")
    
    try:
        tracker.add_habit(name, description, frequency)
        print(f"Habit '{name}' added successfully!")
    except ValueError as e:
        print(f"Error: {e}")

def mark_habit_complete(tracker):
    print("\nMark Habit Complete")
    habits = tracker.get_all_habits()
    
    if not habits:
        print("No habits to mark. Please add habits first.")
        return
    
    print("Select habit to mark complete:")
    for i, habit in enumerate(habits, 1):
        print(f"{i}. {habit.name} ({habit.frequency})")
    
    try:
        choice = int(input("Enter habit number: ")) - 1
        if 0 <= choice < len(habits):
            selected_habit = habits[choice]
            date_str = input("Enter completion date (YYYY-MM-DD) or leave blank for today: ")
            
            if date_str:
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%d").date()
                except ValueError:
                    print("Invalid date format. Using today's date.")
                    date = datetime.now().date()
            else:
                date = datetime.now().date()
            
            tracker.complete_habit(selected_habit.name, date)
            print(f"Marked '{selected_habit.name}' complete for {date}!")
        else:
            print("Invalid habit number.")
    except ValueError:
        print("Please enter a valid number.")

def view_all_habits(tracker):
    print("\nAll Habits:")
    habits = tracker.get_all_habits()
    
    if not habits:
        print("No habits being tracked. Add some habits first!")
        return
    
    for habit in habits:
        completion_rate = habit.get_completion_rate()
        print(f"\n{habit.name} ({habit.frequency})")
        print(f"Description: {habit.description}")
        print(f"Current streak: {habit.streak} days")
        print(f"Max streak: {habit.max_streak} days")
        print(f"Completion rate: {completion_rate:.1f}%")
        print(f"Created: {habit.creation_date}")

def view_weekly_summary(tracker):
    print("\nWeekly Summary:")
    summary = tracker.get_weekly_summary()
    
    if not summary:
        print("No habit data available for this week.")
        return
    
    current_week = datetime.now().date() - timedelta(days=datetime.now().weekday())
    print(f"Week starting: {current_week}")
    print("-" * 50)
    
    for habit, data in summary.items():
        target = data['target']
        completions = data['completions']
        percentage = (completions / target) * 100 if target > 0 else 0
        
        print(f"{habit}:")
        print(f"  Completions: {completions}/{target} ({percentage:.0f}%)")
        print(f"  Current streak: {data['streak']} days")
        print("-" * 50)

def view_analytics(tracker):
    print("\nAnalytics Options:")
    print("1. View completion rates")
    print("2. View streak analysis")
    print("3. View weekly history")
    print("4. Back to main menu")
    
    choice = input("Enter your choice (1-4): ")
    habits = tracker.get_all_habits()
    
    if not habits:
        print("No habits available for analytics. Add some habits first!")
        return
    
    if choice == "1":
        HabitAnalytics.plot_completion_rates(habits)
    elif choice == "2":
        HabitAnalytics.plot_streaks(habits)
    elif choice == "3":
        history = HabitAnalytics.weekly_completion_history(tracker)
        print("\nWeekly Completion History (last 8 weeks):")
        for week, data in history.items():
            print(f"\n{week}:")
            for habit, stats in data.items():
                print(f"  {habit}: {stats['completions']}/{stats['target']}")
    elif choice == "4":
        return
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()