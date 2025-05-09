import webbrowser as wb

search_query = input("What do you wanna search? --> ")
engine = input("""What search engine?
               For Google, type G.
               For DuckDuckGo, type D.
               For Bing, type B.
               For Yahoo, type Y.
               --> """).upper()
query = search_query.replace("%", "%25")
query = query.replace("{", "%7B")
query = query.replace("}", "%7D")
query = query.replace("[", "%5B")
query = query.replace("]", "%5D")
query = query.replace("|", "%7C")
query = query.replace(":", "%3A")
query = query.replace(";", "%3B")
query = query.replace("'", "%27")
query = query.replace("`", "%60")
query = query.replace("+", "%2B")
query = query.replace(" ", "+")
query = query.replace("?", "%3F")
query = query.replace("!", "%21")
query = query.replace("$", "%24")
query = query.replace("(", "%28")
query = query.replace(")", "%29")
query = query.replace("=", "%3D")
query = query.replace(",", "%2C")
query = query.replace("/", "%2F")
query = query.replace("^", "%5E")
query = query.replace("!", "%21")
query = query.replace("#", "%23")
query = query.replace("@", "%40")
if engine == "G":
    page = f"google.com/search?surl=1&q={query}"
elif engine == "D":
    page = f"duckduckgo.com/?q={query}"
elif engine == "B":
    page = f"bing.com/search?q={query}"
elif engine == "Y":
    page = f"search.yahoo.com/search?p={query}"
else:
    print("Invalid entry. Defaulting to Google.")
    page = f"google.com/search?surl=1&q={query}"


print(f"\n{page}")


