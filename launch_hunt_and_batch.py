from agents.site_hunter import site_hunter_agent
from batch_launcher import run_batch

def run():
    query = input("🧠 Inserisci il settore/località da colpire: ")
    site_hunter_agent(query)
    run_batch()

if __name__ == "__main__":
    run()
