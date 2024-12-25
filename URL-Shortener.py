import pyshorteners

def short_url():
    # Get the URL from the user
    url = input("Enter the URL to shorten: ")
    
    try:
        # Generate the shortened URL
        shortener = pyshorteners.Shortener()
        shortened_url = shortener.tinyurl.short(url)
        
        print(f"Shortened URL: {shortened_url}")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    while True:
        print("\nURL Shortener")
        print("1. Shorten a URL")
        print("2. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == "1":
            short_url()
        elif choice == "2":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
