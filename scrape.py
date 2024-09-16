import requests
from bs4 import BeautifulSoup

def get_did_you_know(word):
    url = f"https://www.merriam-webster.com/dictionary/{word}"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        definition_div = soup.find('div', id='dictionary-entry-1')
        definition_div_inside = definition_div.find('div', class_='vg')
        did_you_know_div = soup.find('div', id="did-you-know")
        
        if definition_div_inside:
            definitions = definition_div_inside.find_all('div', recursive=False)
            
            print(f"Definitions for '{word}':")
            for i, definition in enumerate(definitions, 1):
                # Move the get_text call outside of the f-string
                definition_text = definition.get_text(strip=True, separator='\n')
                print(f"{i}. {definition_text}")
            
            if did_you_know_div:
                print('========================')
                print(did_you_know_div.get_text(strip=True, separator="\n"))
            else:
                print("No 'Did You Know?' section found for the word.")
        else:
            print(f"No definitions found for '{word}'.")
    else:
        print(f"Failed to retrieve the page for '{word}'. Status code: {response.status_code}")

if __name__ == "__main__":
    word = input("Enter a word: ")
    get_did_you_know(word)
