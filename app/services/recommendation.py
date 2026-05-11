# app/services/recommendation.py

from app.services.comparator import compare_assessments
from app.services.retriever import search_assessments
from app.services.conversation import (
    detect_intent,
    generate_clarification
)




def filter_results(results, query):

    query_lower = query.lower()

    ranked_results = []

    for item in results:

        text = f"""
        {item['name']}
        {item['description']}
        {' '.join(item['categories'])}
        {' '.join(item['job_levels'])}
        """.lower()

      

        score = item["score"]

       
     

        if "java" in query_lower and "java" in text:
            score += 0.30

       

        if "personality" in query_lower:

            if (
                "personality" in text
                or "opq" in text
                or "behavior" in text
            ):
                score += 0.30

        

        if "communication" in query_lower:

            if "communication" in text:
                score += 0.20

      

        if "manager" in query_lower:

            if (
                "manager" in text
                or "leadership" in text
            ):
                score += 0.20

        

        if "developer" in query_lower:

            if (
                "developer" in text
                or "programming" in text
                or "coding" in text
            ):
                score += 0.20

     

        if "graduate" in query_lower:

            if "graduate" in text:
                score += 0.20


        item["score"] = score

        ranked_results.append(item)

   

    ranked_results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return ranked_results




def generate_recommendations(query):

   

    intent = detect_intent(query)

    print("\nQUERY:", query)
    print("INTENT:", intent)


    if intent == "clarify":

        return {
            "reply": generate_clarification(query),
            "recommendations": [],
            "end_of_conversation": False
        }

  

    if intent == "out_of_scope":

        return {
            "reply": "I can only help with SHL assessment recommendations.",
            "recommendations": [],
            "end_of_conversation": False
        }


    if intent == "compare":

        return compare_assessments(query)



    results = search_assessments(
        query=query,
        top_k=15
    )

  

    results = filter_results(results, query)

   

    results = results[:5]

    

    recommendations = []

    for item in results:

        recommendations.append({

            "name": item["name"],

            "url": item["url"],

            "test_type": ", ".join(item["categories"])

        })


    if not recommendations:

        return {
            "reply": "I could not find suitable SHL assessments for this requirement.",
            "recommendations": [],
            "end_of_conversation": False
        }


    return {
        "reply": f"I found {len(recommendations)} SHL assessments matching your requirements.",
        "recommendations": recommendations,
        "end_of_conversation": True
    }




if __name__ == "__main__":

    test_queries = [

        "I need assessment",

        "Hiring Java developer",

        "Hiring Java developer with communication skills",

        "Hiring Java developer add personality tests",

        "Hiring engineering manager",

        "difference between OPQ and Verify Numerical Ability",

        "Give immigration hiring advice"
    ]

    for query in test_queries:

        print("\n" + "=" * 80)

        response = generate_recommendations(query)

        print("\nFINAL RESPONSE:\n")

        print(response)

        print()