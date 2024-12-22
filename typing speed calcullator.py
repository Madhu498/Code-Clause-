import time

def calculate_wpm(start_time, end_time, word_count):
    """Calculate Words Per Minute (WPM)."""
    elapsed_time = end_time - start_time
    minutes = elapsed_time / 60
    return round(word_count / minutes)

def calculate_accuracy(original_text, user_text):
    """Calculate accuracy percentage based on original and user text."""
    original_words = original_text.split()
    user_words = user_text.split()
    
    correct_words = sum(1 for o, u in zip(original_words, user_words) if o == u)
    return round((correct_words / len(original_words)) * 100, 2)

def typing_speed_test():
    print("Typing Speed Test\n")
    original_text = ("The quick brown fox jumps over the lazy dog. "
                     "This sentence includes all the letters of the alphabet.")
    print("Type the following text as quickly and accurately as possible:")
    print(f"\n{original_text}\n")

    input("Press Enter when ready to start...")

    # Record the start time
    start_time = time.time()
    
    # Get user input
    user_text = input("\nStart typing: \n")
    
    # Record the end time
    end_time = time.time()

    # Calculate WPM and accuracy
    word_count = len(original_text.split())
    wpm = calculate_wpm(start_time, end_time, word_count)
    accuracy = calculate_accuracy(original_text, user_text)

    # Provide feedback
    print("\nTyping Test Results")
    print(f"Words Per Minute (WPM): {wpm}")
    print(f"Accuracy: {accuracy}%")

    if accuracy == 100:
        print("Excellent accuracy! Keep practicing to maintain speed and precision.")
    elif accuracy > 80:
        print("Great job! Aim for higher accuracy and speed.")
    else:
        print("Keep practicing to improve your typing accuracy and speed.")

if __name__ == "__main__":
    typing_speed_test()
    