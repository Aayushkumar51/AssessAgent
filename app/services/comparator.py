

import pickle
from pathlib import Path




BASE_DIR = Path(__file__).resolve().parent.parent

VECTORSTORE_DIR = BASE_DIR / "vectorstore"

METADATA_PATH = VECTORSTORE_DIR / "metadata.pkl"




print("\nLoading metadata for comparator...\n")

with open(METADATA_PATH, "rb") as f:
    metadata = pickle.load(f)

print("Comparator metadata loaded.\n")




def find_assessment(name):
    """
    Find best matching assessment from metadata.
    """

    name_lower = name.lower().strip()

    best_match = None

    for item in metadata:

        item_name = item.get("name", "").lower()

        

        if name_lower in item_name:
            return item


        if item_name in name_lower:
            return item

       

        first_word = name_lower.split()[0]

        if first_word in item_name:
            best_match = item

    return best_match



def extract_names(query):
    """
    Extract two assessment names from comparison query.
    """

    query = query.lower().strip()

   

    if "difference between" in query:

        cleaned = query.replace("difference between", "").strip()

        if " and " in cleaned:

            parts = cleaned.split(" and ")

            if len(parts) == 2:

                left = parts[0].strip()
                right = parts[1].strip()

                return left, right



    if "compare" in query:

        cleaned = query.replace("compare", "").strip()

        if " and " in cleaned:

            parts = cleaned.split(" and ")

            if len(parts) == 2:

                left = parts[0].strip()
                right = parts[1].strip()

                return left, right

    if " vs " in query:

        parts = query.split(" vs ")

        if len(parts) == 2:

            left = parts[0].strip()
            right = parts[1].strip()

            return left, right

   

    if " versus " in query:

        parts = query.split(" versus ")

        if len(parts) == 2:

            left = parts[0].strip()
            right = parts[1].strip()

            return left, right

    return None, None




def format_assessment(item):
    """
    Format assessment details cleanly.
    """

    return f"""
Assessment Name:
{item.get("name", "N/A")}

Description:
{item.get("description", "No description available.")}

Categories:
{", ".join(item.get("keys", []))}

Job Levels:
{", ".join(item.get("job_levels", []))}

Duration:
{item.get("duration", "N/A")}

Remote:
{item.get("remote", "N/A")}

Adaptive:
{item.get("adaptive", "N/A")}
""".strip()



def compare_assessments(query):
    """
    Compare two SHL assessments.
    """

   

    left_name, right_name = extract_names(query)

    print("\nCOMPARE QUERY:", query)

    print("LEFT:", left_name)
    print("RIGHT:", right_name)

    

    if not left_name or not right_name:

        return {
            "reply": "Please specify two SHL assessments to compare.",
            "recommendations": [],
            "end_of_conversation": False
        }

 
    left = find_assessment(left_name)
    right = find_assessment(right_name)

    print("\nLEFT MATCH:", left)
    print("\nRIGHT MATCH:", right)

   

    if not left or not right:

        return {
            "reply": "I could not find both assessments in the SHL catalog.",
            "recommendations": [],
            "end_of_conversation": False
        }

    

    comparison_text = f"""
Comparison between {left.get("name")} and {right.get("name")}:


----------------------------------------
ASSESSMENT 1
----------------------------------------

{format_assessment(left)}


----------------------------------------
ASSESSMENT 2
----------------------------------------

{format_assessment(right)}
"""


    recommendations = [

        {
            "name": left.get("name"),
            "url": left.get("link"),
            "test_type": ", ".join(left.get("keys", []))
        },

        {
            "name": right.get("name"),
            "url": right.get("link"),
            "test_type": ", ".join(right.get("keys", []))
        }
    ]


    return {
        "reply": comparison_text.strip(),
        "recommendations": recommendations,
        "end_of_conversation": False
    }



if __name__ == "__main__":

    test_queries = [

        "difference between OPQ and GSA",

        "compare Java 8 and Java Frameworks",

        "OPQ vs Verify Numerical Ability"
    ]

    for query in test_queries:

        print("\n" + "=" * 80)

        response = compare_assessments(query)

        print("\nFINAL RESPONSE:\n")

        print(response)