def dfs(maze, x, y, end_x, end_y, path):
    pass

'''
- **`maze`**: Eine Liste von Listen, die das Labyrinth darstellt (zu Erläuterung siehe oben).
- **`x, y`**: Aktuelle Koordinaten im Labyrinth.
- **`end_x, end_y`**: Zielkoordinaten.
- **`path`**: Liste, die den Pfad speichert, der während der Suche gefunden wird.


**``maze[x][y]``**: Gibt den Wert der Zelle an der Position (x, y) im Labyrinth zurück. Dieser Wert kann anzeigen, ob es sich um eine Wand (``'#'``), einen freien Weg (``' '``) oder einen besuchten Punkt mit (``'.'``) handelt.

**``maze[x][y] = '.'``**: Setzt die Zelle an der Position (x, y) auf ``'.'``, was bedeutet, dass diese Zelle als bereits besuchte Zelle markiert wird.

**``path.append((x, y))``**:  Fügt das Tupel (x, y), welches die aktuelle Position repräsentiert, zur Liste `path` hinzu. Dies dient dazu, den zurückgelegten Weg zu verfolgen.

**``path.pop()``**:  Entfernt das zuletzt mit `append` hinzugefügte Element aus der Liste `path`. Dies wird typischerweise verwendet, um einen Schritt im Pfad rückgängig zu machen, wenn ein Rückzug (Backtracking) stattfindet, weil kein weiterer Fortschritt möglich ist.

**``len(maze)``**: gibt die Anzahl der Zeilen im Labyrinth zurück. Kann verwendet werden, um zu überprüfen, ob sich ``x`` innerhalb des Labyrinths befindet.

**``len(maze[0])``**: gibt die Länge des ersten Elements in der Liste zurück. Kann verwendet werden, um zu überprüfen, ob sich ``y`` innerhalb des Labyrinths befindet.


'''




# Überprüfe, ob die aktuelle Position außerhalb der Grenzen des Labyrinths liegt oder ob sie eine Wand ist, oder ob sie mit 'X' bereits markiert wurde
# Kein gültiger Zug => kehre zurück mit FALSCH

# Überprüfe, ob die aktuelle Position das Ziel ist
# Füge die Zielposition zum Pfad hinzu
# Das Ziel wurde erreicht => kehre zurück mit WAHR

# Überprüfe, ob die aktuelle Zelle schon Teil des Pfades ist oder als besucht markiert wurde mit '.' oder 'X'
# Die Zelle wurde bereits besucht => kehre zurück mit FALSCH

# Markiere die aktuelle Zelle als besucht, indem du sie mit '.' markierst
# Füge die aktuelle Position zum Pfad hinzu

# Rekursive DFS-Suche in alle vier Richtungen (unten, oben, rechts, links) // siehe 3.Rekursion und Backtracking
# Wenn einer der Aufrufe mit WAHR zurückkehrt, wurde ein zulässiger Weg gefunden => kehre zurück mit WAHR

# Entferne die aktuelle Position vom Pfad
# Ersetzt die aktuelle Zelle mit 'X', um sie als Sackgasse zu markieren
# Kehre zurück mit FALSCH, da kein Pfad durch diese Zelle führt
