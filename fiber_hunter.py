import csv
import os
from datetime import datetime

LEADS_FILE = "fiber_leads.csv"

HEADER = [
    "date_added",
    "name",
    "phone",
    "address",
    "city",
    "state",
    "zip_code",
    "provider",
    "status",
    "follow_up_date",
    "notes"
]

STATUS_OPTIONS = {
    "1": "Fiber Available",
    "2": "Internet Available - No Fiber",
    "3": "Not Available",
    "4": "Already Has Service",
    "5": "Not Interested",
    "6": "Follow Up",
    "7": "Sold"
}


def setup_file():
    if not os.path.exists(LEADS_FILE):
        with open(LEADS_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(HEADER)


def add_lead():
    print("\n=== Add New Fiber Lead ===")

    name = input("Customer name: ").strip()
    phone = input("Phone number: ").strip()
    address = input("Street address: ").strip()
    city = input("City: ").strip()
    state = input("State: ").strip()
    zip_code = input("ZIP code: ").strip()
    provider = input("Current provider: ").strip()

    print("\nStatus Options:")
    for key, value in STATUS_OPTIONS.items():
        print(f"{key}. {value}")

    choice = input("Choose status: ").strip()
    status = STATUS_OPTIONS.get(choice, "Unknown")

    follow_up_date = input("Follow-up date, if any: ").strip()
    notes = input("Notes: ").strip()

    with open(LEADS_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            name,
            phone,
            address,
            city,
            state,
            zip_code,
            provider,
            status,
            follow_up_date,
            notes
        ])

    print("\nLead saved successfully.")


def view_leads():
    print("\n=== Saved Fiber Leads ===")

    if not os.path.exists(LEADS_FILE):
        print("No leads found yet.")
        return

    with open(LEADS_FILE, "r") as file:
        reader = csv.DictReader(file)
        leads = list(reader)

    if not leads:
        print("No leads found yet.")
        return

    for i, lead in enumerate(leads, start=1):
        print("\n-------------------------")
        print(f"Lead #{i}")
        print(f"Date Added: {lead['date_added']}")
        print(f"Name: {lead['name']}")
        print(f"Phone: {lead['phone']}")
        print(f"Address: {lead['address']}, {lead['city']}, {lead['state']} {lead['zip_code']}")
        print(f"Provider: {lead['provider']}")
        print(f"Status: {lead['status']}")
        print(f"Follow Up: {lead['follow_up_date']}")
        print(f"Notes: {lead['notes']}")


def search_leads():
    print("\n=== Search Leads ===")
    search_term = input("Search by name, phone, address, city, ZIP, or status: ").lower().strip()

    with open(LEADS_FILE, "r") as file:
        reader = csv.DictReader(file)
        found = False

        for lead in reader:
            lead_text = " ".join(lead.values()).lower()

            if search_term in lead_text:
                found = True
                print("\n-------------------------")
                print(f"Name: {lead['name']}")
                print(f"Phone: {lead['phone']}")
                print(f"Address: {lead['address']}, {lead['city']}, {lead['state']} {lead['zip_code']}")
                print(f"Provider: {lead['provider']}")
                print(f"Status: {lead['status']}")
                print(f"Follow Up: {lead['follow_up_date']}")
                print(f"Notes: {lead['notes']}")

        if not found:
            print("No matching leads found.")


def lead_summary():
    print("\n=== Lead Summary ===")

    counts = {}

    with open(LEADS_FILE, "r") as file:
        reader = csv.DictReader(file)

        for lead in reader:
            status = lead["status"]
            counts[status] = counts.get(status, 0) + 1

    if not counts:
        print("No leads yet.")
        return

    for status, count in counts.items():
        print(f"{status}: {count}")


def main():
    setup_file()

    while True:
        print("\n==========================")
        print("      FIBER HUNTER")
        print("==========================")
        print("1. Add new lead")
        print("2. View all leads")
        print("3. Search leads")
        print("4. Lead summary")
        print("5. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            add_lead()
        elif choice == "2":
            view_leads()
        elif choice == "3":
            search_leads()
        elif choice == "4":
            lead_summary()
        elif choice == "5":
            print("Exiting Fiber Hunter.")
            break
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()