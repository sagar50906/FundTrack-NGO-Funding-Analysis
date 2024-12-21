import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import Tk, Label, Entry, Button, messagebox
import os

# File to store data
FUNDING_FILE = "ngo_funding.csv"

# Load existing data or create a new DataFrame
if os.path.exists(FUNDING_FILE):
    df = pd.read_csv(FUNDING_FILE)
else:
    df = pd.DataFrame(columns=["Year", "Source", "Amount"])

# Save the data to a CSV file
def save_data():
    df.to_csv(FUNDING_FILE, index=False)

# Add funding data interactively
def add_funding_data():
    def submit_data():
        year = entry_year.get()
        source = entry_source.get()
        amount = entry_amount.get()

        if not (year.isdigit() and amount.isdigit()):
            messagebox.showerror("Input Error", "Year and Amount must be numeric.")
            return

        global df
        df = pd.concat([df, pd.DataFrame({"Year": [int(year)], "Source": [source], "Amount": [float(amount)]})], ignore_index=True)
        save_data()
        messagebox.showinfo("Success", "Funding data added successfully!")
        root.destroy()

    root = Tk()
    root.title("Add Funding Data")

    Label(root, text="Year:").grid(row=0, column=0, padx=10, pady=10)
    entry_year = Entry(root)
    entry_year.grid(row=0, column=1, padx=10, pady=10)

    Label(root, text="Source:").grid(row=1, column=0, padx=10, pady=10)
    entry_source = Entry(root)
    entry_source.grid(row=1, column=1, padx=10, pady=10)

    Label(root, text="Amount:").grid(row=2, column=0, padx=10, pady=10)
    entry_amount = Entry(root)
    entry_amount.grid(row=2, column=1, padx=10, pady=10)

    Button(root, text="Submit", command=submit_data).grid(row=3, column=0, columnspan=2, pady=10)

    root.mainloop()

# Visualize the data
def visualize_data():
    if df.empty:
        print("No data to visualize.")
        return

    # Group data by year and source
    yearly_funding = df.groupby("Year")["Amount"].sum()
    funding_by_source = df.groupby("Source")["Amount"].sum()

    # Create subplots
    plt.figure(figsize=(20, 12))

    # Bar chart - Yearly funding
    plt.subplot(2, 3, 1)
    sns.barplot(x=yearly_funding.index, y=yearly_funding.values, palette="viridis")
    plt.title("Yearly Funding (Bar Chart)")
    plt.xlabel("Year")
    plt.ylabel("Total Amount")

    # Pie chart - Funding by source
    plt.subplot(2, 3, 2)
    funding_by_source.plot(kind="pie", autopct="%1.1f%%", startangle=90, cmap="coolwarm", legend=False)
    plt.title("Funding Distribution by Source (Pie Chart)")
    plt.ylabel("")

    # Line chart - Funding trend
    plt.subplot(2, 3, 3)
    plt.plot(yearly_funding.index, yearly_funding.values, marker="o", linestyle="-", color="green")
    plt.title("Funding Trend Over Years (Line Chart)")
    plt.xlabel("Year")
    plt.ylabel("Total Amount")

    # Histogram - Distribution of funding amounts
    plt.subplot(2, 3, 4)
    sns.histplot(df["Amount"], kde=True, color="purple", bins=10)
    plt.title("Distribution of Funding Amounts (Histogram)")
    plt.xlabel("Funding Amount")
    plt.ylabel("Frequency")

    # Scatterplot - Funding amount by year
    plt.subplot(2, 3, 5)
    sns.scatterplot(x=df["Year"], y=df["Amount"], hue=df["Source"], palette="deep")
    plt.title("Funding Amounts by Year and Source (Scatterplot)")
    plt.xlabel("Year")
    plt.ylabel("Amount")

    # Bar chart - Funding by source
    plt.subplot(2, 3, 6)
    sns.barplot(x=funding_by_source.index, y=funding_by_source.values, palette="pastel")
    plt.title("Funding by Source (Bar Chart)")
    plt.xlabel("Source")
    plt.ylabel("Total Amount")
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

# Main Menu
def main_menu():
    while True:
        print("\nNGO Funding Visualization")
        print("1. Add Funding Data")
        print("2. Visualize Funding Data")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_funding_data()
        elif choice == "2":
            visualize_data()
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
