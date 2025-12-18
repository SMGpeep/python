import requests
import json
def chat_with_lm_studio(prompt, system_prompt="", max_tokens=100):
    """
    Kommunikation mit LM Studio über lokale API
    """
    url = "http://localhost:1234/v1/chat/completions"
    
    headers = {"Content-Type": "application/json"}
    
    data = {
    "messages": [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": prompt}
    ],
    "max_tokens": max_tokens,
    "temperature": 0.7
    } 
    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Fehler: {e}"

def code_erklären(code_snippet, sprache="Python"):
    """
    Erklärt ein Code-Snippet in einfachen Worten mithilfe von LM Studio.
    
    Args:
        code_snippet (str): Der zu erklärende Code.
        sprache (str, optional): Die Programmiersprache des Codes. Standard ist "Python".
    
    Returns:
        str: Erklärung des Codes.
    """
    system_prompt = f"Du bist ein hilfreicher Code-Erklärer für die Sprache {sprache}."
    prompt = f"Bitte erkläre den folgenden {sprache}-Code in einfachen Worten:\n\n{code_snippet}"
    return chat_with_lm_studio(prompt, system_prompt)



def beispiel_code_und_erklaerung():
    """
    Gibt ein Beispiel-Code-Snippet mit zugehöriger Erklärung zurück.
    """
    beispiel_code = '''
def addiere(a, b):
    return a + b

ergebnis = addiere(2, 3)
print(ergebnis)
'''
    erklaerung = code_erklären(beispiel_code, sprache="Python")
    return beispiel_code, erklaerung

beispiel_code_und_erklaerung()