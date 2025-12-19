from apps.ai.router.classifier import IntentRouter
from src.services.project_service import ProjectService

def main():
    print("--- OWASP NestBot PoC (Arkadii Demo Version) ---")
    print("[System] Initializing Layer 1 (Router)...")
    router = IntentRouter()
    
    print("[System] Initializing Layer 2 (Services)...")
    project_service = ProjectService()
    
    print("\n✅ Bot Ready. Type 'exit' to quit.")
    
    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        # --- LAYER 1: ROUTING ---
        # Currently returns "STATIC" or "DYNAMIC" (String)
        intent = router.get_intent(user_input)
        
        # --- LAYER 2: EXECUTION ---
        if intent == "STATIC":
            print(f"[Debug] Router identified STATIC intent. Routing to ProjectService.")
            
            # Temporary Adapter: 
            # Since Router doesn't extract args yet, we extract the key manually for the demo.
            # We assume the last word is the project key (e.g., "Who leads ZAP")
            key = user_input.split()[-1]
            
            result = project_service.get_project_details(key)
            
            if result:
                # Success: We got structured data back from your Service Layer
                print(f"\n🤖 Bot: Here is the info for {result.name}:")
                print(f"   • Leader: {result.leader}")
                print(f"   • URL: {result.url}")
                print(f"   • Description: {result.description}")
            else:
                print(f"\n🤖 Bot: I know that is a project query, but I couldn't find '{key}' in the database.")

        elif intent == "DYNAMIC":
            print(f"[Debug] Router identified DYNAMIC intent.")
            print("\n🤖 Bot: (Placeholder) I would send this to the LLM/RAG chain now.")
            
        else:
            print("[Error] Unknown intent received.")

if __name__ == "__main__":
    main()