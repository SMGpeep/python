import cv2
import numpy as np

def includecontour(contour):
    """
    Prüfe, ob die übergebene Kontur ein Kreis ist.
    Parameter: contour - die zu prüfende Kontur
    Rückgabewert: True genau dann, wenn die Kontur ein Kreis ist.

    Problem: Es werden oft auch Rechtecke ("rectangles") als Kreise erkannt!
    Warum kann das passieren?
        - Der Circularity-Threshold ist nicht hoch genug (z.B. 0.75 lässt auch regelmäßige Rechtecke zu)
        - Rechtecke können bei kleinen Größenverhältnissen ähnliche Circularity-Werte wie Kreise haben.
        - Die Approximationsart (CHAIN_APPROX_SIMPLE vs CHAIN_APPROX_NONE) beeinflusst die Details im contour.
        - Kleine, unförmige "Kreise" werden evtl. aussortiert, aber rechteckige Formen bleiben drin.

    Lösungsansätze:
        - Höheren Schwellwert für circularity, z.B. 0.85 oder 0.9 wählen.
        - Zusätzlich: Prüfen, ob die approximierte Kontur viele Ecken hat. Ein Rechteck hat 4, ein Kreis viel mehr!
        - Alternativ: cv2.approxPolyDP verwenden und nur Konturen durchlassen, deren Approximierung viele Punkte hat.

    """
    perimeter = cv2.arcLength(contour, True)
    area = cv2.contourArea(contour)
    if perimeter == 0:
        return False
    circularity = 4 * np.pi * area / (perimeter * perimeter)
    # Explanations:
    #   Rechtecke haben oft eine Circularity ~0.785 (bei perfekten Quadraten)
    #   Echte Kreise haben Circularity nahe 1.0
    #   Mit 0.75 werden die meisten Rechtecke noch als "Kreis" zugelassen.
    # Lösung: Schwelle erhöhen!
    if circularity < 0.84:  # Erhöhe für strengere Kreiserkennung!
        return False

    # Zweiter Test: Ist die Kontur ein Rechteck? Rechtecke rauswerfen, auch wenn sie "unförmig" sind!
    approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
    if len(approx) == 4:  # 4 Ecken -> Rechteck (auch wenn verzogen)
        return False
    # Damit erlauben wir auch unförmige, wellige Kreise (mit z.B. 6, 8, 20, ... Ecken), aber keine Rechtecke.


    # Wenn wir bis hier sind: Kreisartig und genug Punkte => vermutlich kein Rechteck!
    return True

# Open the webcam (default camera is 0)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to grayscale for edge detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    imagehsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # OTSU Threshold-Parameter sind automatisch und passen das Threshold dem Bildinhalt an,
    # was meist gute Ergebnisse bei gemischtem Licht und mehreren Farben liefert.
    # Für die gezielte Kreiserkennung kann aber auch ein fester Threshold sinnvoll sein.
    # Typische Werte liegen zwischen 50 und 100:
    #   - Ein niedriger Wert (z.B. 50) erkennt auch blasse/schwache Kreise, aber erhöht das Rauschen.
    #   - Ein hoher Wert (z.B. 100 oder mehr) filtert dunkle Ränder raus, kann aber schwache Kreise verlieren.
    # Für die meisten hellen Kreise oder starke Kontraste: 80-100 ist erfahrungsgemäß ein guter Startwert.
    # Im Zweifel einfach mal ausprobieren, z.B.:
    _, imagebitmap = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY)
    # Hier aber nutzen wir OTSU als Vergleich/Basis:
    #_, imagebitmap = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
    
    # Die unteren und oberen Grenzen für "grün" in HSV können angepasst werden!
    # colorlow: Der Farbtonbereich für die untere Grenze (erhöhe/senke die Werte, um unterschiedliche Grüntöne zu erfassen)
    # colorhigh: Die obere Grenze; insbesondere der Sättigungs- und Helligkeitsbereich kann angepasst werden,
    # um unterschiedliche Lichtverhältnisse auszugleichen.
    colorlow = np.array([40, 40, 40])  # H, S, V - kann angepasst werden
    colorhigh = np.array([80, 255, 255])  # H, S, V - kann angepasst werden
    imagefiltered = cv2.inRange(imagehsv, colorlow, colorhigh)
    
    # cv2.RETR_LIST und cv2.CHAIN_APPROX_SIMPLE können ggf. angepasst werden (bspw. andere Modi für andere Effekte)
    contours, _ = cv2.findContours(imagefiltered, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)#oder NONE, der gibt mehr konturen zurück
    
    # Die Filter-Logik für die Kreis-Konturen hängt von includecontour() ab (Threshold s.o.)
    circlecontours = list(filter(includecontour, contours))

    # Die Farbe (0,255,0) und Dicke (3) der gezeichneten Konturen kann angepasst werden
    cv2.drawContours(frame, circlecontours, -1, (0, 255, 0), 3)

    cv2.imshow('feed', frame)
    # Zum Debuggen: Zeige die Binärbilder, um die Wirkung der Filter zu testen
    # cv2.imshow('bitmap', imagebitmap)
    # cv2.imshow('greenstuff', imagefiltered)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        import os
        save_dir = os.path.join('python', 'playground', 'greenCircle')
        os.makedirs(save_dir, exist_ok=True)
        cv2.imwrite(os.path.join(save_dir, '01_gray.png'), gray)
        cv2.imwrite(os.path.join(save_dir, '02_imagehsv.png'), imagehsv)
        cv2.imwrite(os.path.join(save_dir, '03_imagebitmap.png'), imagebitmap)
        cv2.imwrite(os.path.join(save_dir, '04_imagefiltered.png'), imagefiltered)
        cv2.imwrite(os.path.join(save_dir, '05_frame.png'), frame)
        break

cap.release()
cv2.destroyAllWindows()
