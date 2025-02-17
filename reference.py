import requests
import time

def get_bibtex_from_title(title):
    """
    Retrieves the BibTeX citation for a given paper title using the CrossRef API.
    
    Args:
        title (str): The title of the paper.
        
    Returns:
        str: The BibTeX citation or an error message if retrieval fails.
    """
    url = f"https://api.crossref.org/works?query.title={title}&rows=1"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if "message" in data and "items" in data["message"] and len(data["message"]["items"]) > 0:
            doi = data["message"]["items"][0].get("DOI", "")
            if doi:
                bibtex_url = f"https://doi.org/{doi}"
                headers = {"Accept": "application/x-bibtex"}
                bibtex_response = requests.get(bibtex_url, headers=headers)
                
                if bibtex_response.status_code == 200:
                    return bibtex_response.text
                else:
                    return None
        else:
            return None
    else:
        return None

def read_titles_from_file(filename):
    """
    Reads paper titles from a file.
    
    Args:
        filename (str): The filename containing titles.
        
    Returns:
        list: A list of titles.
    """
    with open(filename, "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]

def modify_bibtex_entry(bibtex, index):
    """
    Modifies the BibTeX entry by replacing its citation key with CNN-{index}.
    
    Args:
        bibtex (str): The original BibTeX entry.
        index (int): The citation number.
        
    Returns:
        str: The modified BibTeX entry.
    """
    lines = bibtex.split("\n")
    if lines:
        first_line = lines[0]
        modified_first_line = first_line.replace("{", "{HTrans-" + str(index) , 1)
        lines[0] = modified_first_line
    return "\n".join(lines)

if __name__ == "__main__":
    input_filename = "titles.txt"  # Make sure this file exists with one title per line
    
    # Read titles from file
    titles = read_titles_from_file(input_filename)
    
    if not titles:
        print("No titles found in the file.")
    else:
        for idx, title in enumerate(titles, start=1):
            #print(f"\nFetching BibTeX for title {idx}: {title}")
            bibtex = get_bibtex_from_title(title)
            if bibtex:
                modified_bibtex = modify_bibtex_entry(bibtex, idx)
                print("\n" + modified_bibtex)
            else:
                print(f"\nNo BibTeX entry found for: {title}")

            # Sleep for 1 second to avoid API rate limiting
            time.sleep(1)
