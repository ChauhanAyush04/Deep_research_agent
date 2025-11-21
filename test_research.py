from crew import research_crew

def main():
    topic = "Quantum computing applications"
    print("Running research agent...")

    result = research_crew.kickoff(inputs={"topic": topic})

    print("\n\n=== FINAL REPORT OUTPUT ===")
    print(result)

if __name__ == "__main__":
    main()
