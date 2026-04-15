# Main branch for the P4 General Conference Webscrape. 
# Porter Collins, Sarah Walker, Jason Marks, and Juliana Merkley


# main.py done by Jason Marks

# This is the entry point for the program. It handles:
#   - The main menu (scrape or view summaries)
#   - The standard works dictionary template
#   - Part 1: orchestrating the scrape and saving to the database
#   - Part 2: loading data from the database and showing charts
 
import matplotlib.pyplot as plt
import database
import webscraping
 
standard_works_dict = {
    'Speaker_Name': '', 'Talk_Name': '', 'Kicker': '',
    'Matthew': 0, 'Mark': 0, 'Luke': 0, 'John': 0, 'Acts': 0,
    'Romans': 0, '1 Corinthians': 0, '2 Corinthians': 0, 'Galatians': 0,
    'Ephesians': 0, 'Philippians': 0, 'Colossians': 0,
    '1 Thessalonians': 0, '2 Thessalonians': 0, '1 Timothy': 0,
    '2 Timothy': 0, 'Titus': 0, 'Philemon': 0, 'Hebrews': 0,
    'James': 0, '1 Peter': 0, '2 Peter': 0, '1 John': 0, '2 John': 0,
    '3 John': 0, 'Jude': 0, 'Revelation': 0, 'Genesis': 0, 'Exodus': 0,
    'Leviticus': 0, 'Numbers': 0, 'Deuteronomy': 0, 'Joshua': 0,
    'Judges': 0, 'Ruth': 0, '1 Samuel': 0, '2 Samuel': 0,
    '1 Kings': 0, '2 Kings': 0, '1 Chronicles': 0, '2 Chronicles': 0,
    'Ezra': 0, 'Nehemiah': 0, 'Esther': 0, 'Job': 0, 'Psalm': 0,
    'Proverbs': 0, 'Ecclesiastes': 0, 'Song of Solomon': 0, 'Isaiah': 0,
    'Jeremiah': 0, 'Lamentations': 0, 'Ezekiel': 0, 'Daniel': 0,
    'Hosea': 0, 'Joel': 0, 'Amos': 0, 'Obadiah': 0, 'Jonah': 0,
    'Micah': 0, 'Nahum': 0, 'Habakkuk': 0, 'Zephaniah': 0,
    'Haggai': 0, 'Zechariah': 0, 'Malachi': 0, '1 Nephi': 0,
    '2 Nephi': 0, 'Jacob': 0, 'Enos': 0, 'Jarom': 0, 'Omni': 0,
    'Words of Mormon': 0, 'Mosiah': 0, 'Alma': 0, 'Helaman': 0,
    '3 Nephi': 0, '4 Nephi': 0, 'Mormon': 0, 'Ether': 0, 'Moroni': 0,
    'Doctrine and Covenants': 0, 'Moses': 0, 'Abraham': 0,
    'Joseph Smith---Matthew': 0, 'Joseph Smith---History': 0,
    'Articles of Faith': 0
}
 
 
def scrape_and_save():
    # Drop the table first so we don't get duplicate rows on re-runs
    database.drop_table()
 
    # Hand off to webscraping.py — it finds all valid talk URLs,
    # calls process_talk for each one, and saves the result to the DB.
    webscraping.loop_through_talks(standard_works_dict)
 
    print("\nYou've saved the scraped data to your postgres database.")
 
 

 
def show_summaries():
    while True:
        sub_choice = input(
            "\nYou selected to see summaries.\n "
            "Enter 1 to see a summary of all talks.\n "
            "Enter 2 to select a specific talk.\n "
            "Enter anything else to exit: "
        )

        if sub_choice == "1":
            df = database.load_all_data()
            if df is None:
                return

            df_refs = df.drop(columns=["Speaker_Name", "Talk_Name", "Kicker"])
            ref_totals = df_refs.sum()
            ref_totals = ref_totals[ref_totals > 2]

            plt.figure(figsize=(14, 6))
            ref_totals.plot(kind="bar")
            plt.title("Standard Works Referenced in General Conference")
            plt.xlabel("Standard Works Books")
            plt.ylabel("# Times Referenced")
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            plt.show()

        elif sub_choice == "2":
            talks = database.get_talk_list()
            if talks is None:
                return

            print("\nThe following are the names of speakers and their talks:")
            talk_lookup = {}

            for i, (idx, row) in enumerate(talks.iterrows(), start=1):
                print(f"{i}: {row['Speaker_Name']} - {row['Talk_Name']}")
                talk_lookup[i] = idx

            try:
                talk_num = int(input("\nPlease enter the number of the talk you want to see summarized: "))
                db_index = talk_lookup[talk_num]
            except (ValueError, KeyError):
                print("Invalid selection.")
                continue  # Loop back to sub-menu instead of returning

            talk_row = database.get_single_talk(db_index)
            if talk_row is None:
                return

            talk_name = talk_row["Talk_Name"]
            talk_refs = talk_row.drop(labels=["Speaker_Name", "Talk_Name", "Kicker"])
            talk_refs = talk_refs[talk_refs > 0]

            plt.figure(figsize=(12, 6))
            talk_refs.plot(kind="bar")
            plt.title(f"Standard Works Referenced in: {talk_name}")
            plt.xlabel("Standard Works Books")
            plt.ylabel("# Times Referenced")
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            plt.show()

        else:
            print("Returning to main menu.")
            break  # Exit the sub-menu loop, return to main menu
 
 
# Main menu

def main():
    while True:
        choice = input(
            "\nIf you want to scrape data, enter 1. "
            "If you want to see summaries of stored data, enter 2. "
            "Enter any other value to exit the program: "
        )

        if choice == "1":
            scrape_and_save()
        elif choice == "2":
            show_summaries()
        else:
            print("Closing the program.")
            break
 
 

main()
 