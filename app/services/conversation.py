

COMPARE_KEYWORDS = [
    "difference",
    "compare",
    "vs",
    "versus"
]

REFINE_KEYWORDS = [
    "also",
    "add",
    "include",
    "instead",
    "change",
    "update"
]

OUT_OF_SCOPE_KEYWORDS = [
    "legal",
    "salary",
    "labor law",
    "court",
    "visa",
    "immigration"
]




def detect_intent(query: str):

    query_lower = query.lower()

    

    for word in COMPARE_KEYWORDS:
        if word in query_lower:
            return "compare"

    

    for word in REFINE_KEYWORDS:
        if word in query_lower:
            return "refine"

  

    for word in OUT_OF_SCOPE_KEYWORDS:
        if word in query_lower:
            return "out_of_scope"


    if len(query_lower.split()) < 4:
        return "clarify"

    vague_phrases = [
        "i need assessment",
        "suggest assessment",
        "need test",
        "help me hire"
    ]

    for phrase in vague_phrases:
        if phrase in query_lower:
            return "clarify"

  

    return "recommend"




def generate_clarification(query: str):

    query_lower = query.lower()

    if "developer" in query_lower:
        return "What seniority level are you hiring for?"

    if "manager" in query_lower:
        return "Do you want leadership, personality, or technical assessments?"

    return "Can you provide more details about the role and required skills?"




if __name__ == "__main__":

    test_queries = [

        "I need an assessment",

        "Hiring a Java developer with communication skills",

        "Also add personality tests",

        "What is the difference between OPQ and GSA?",

        "Give me legal hiring advice"
    ]

    for query in test_queries:

        intent = detect_intent(query)

        print("=" * 60)

        print(f"Query: {query}")

        print(f"Intent: {intent}")

        if intent == "clarify":
            print(generate_clarification(query))