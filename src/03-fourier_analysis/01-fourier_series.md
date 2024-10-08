## Fourier-Reihen

Sei $f(t)$ eine komplexwertige, periodische Funktion mit Periodenlänge $T$
(kurz: $T$-periodische Funktion):
$$
  \begin{align}
    f: \mathbb{R}/T &\to \mathbb{C} \\
    t &\mapsto f(t)\,.
  \end{align}
$$
Für diese Funktion gilt dann
$f(t+T) = f(t)$ für alle $t$. Weiterhin nehmen wir an, dass 
$f \in \mathcal{L}^2(\mathbb{R}/T)$, d.h. $f$ ist quadratintegrierbar
auf dem Intervall $[0,T]$ und damit auf jedem Intervall der Länge $T$.

Wir definieren den Durchschnitt dieser Funktion (über eine Periode) als
$$
  \bar{f} = \frac{1}{T} \int_{-T/2}^{T/2} f(t)\du t\,.
$$
Die Integrationsgrenzen sind aufgrund der Periodizität der Funktion
beliebig wählbar, solange die Länge des Integrationsintervalls $T$ beträgt.
Nun definieren wir den oszillierenden Anteil der Funktion als
$\widetilde{f}(t) = f(t) - \bar{f}$, womit $f(t) = \bar{f} + \widetilde{f}(t)$ gilt.
Der Mittelwert der oszillierenden Funktion ist offensichtlich null.

Nun betrachten wir die Summe aus beliebigen periodischen 
Funktionen mit verschwindendem Mittelwert, die wir hier
als Basisfunktionen bezeichnen. Aufgrund der $T$-Periodizität von 
$\widetilde{f}(t)$ können die Basisfunktionen nur Periodenlängen von $T/n$ haben,
wobei $n$ eine natürliche Zahl ist. Anders ausgedrückt, können die 
Basisfunktionen nur Winkelfrequenzen von $n\omega = 2\pi n/T$ besitzen.

Eine Familie solcher Basisfunktionen ist die komplexe Exponentialfunktion
$e_n(t) = \eu^{\iu n \omega t}$. Diese Funktionen sind $T$-periodisch und
haben den Mittelwert Null:
$$
  \bar{e}_n 
  = \frac{1}{T} \int_{-T/2}^{T/2} \eu^{\iu n \omega t}\du t
  = \frac{1}{T} \left[ \frac{\eu^{\iu n \omega t}}{\iu n \omega} \right]_{-T/2}^{T/2}
  = \frac{1}{\iu 2 \pi n} \left( \eu^{\iu n \pi} - \eu^{-\iu n \pi} \right)
  = 0\,.
$$
Da beide Eigenschaften ($T$-Periodizität und Mittelwert Null) unter 
skalarer Multiplikation und Addition erhalten bleiben, erfüllen alle
Linearkombinationen von $e_n(t)$ diese Eigenschaften ebenfalls.

Daher nehmen wir gewagt an, dass $\widetilde{f}(t)$ durch eine solche
Linearkombination ausgedrückt werden kann:
$$
  \widetilde{f}(t) = c_1 \eu^{\iu \omega t} + c_{-1} \eu^{-\iu \omega t} + c_2 \eu^{2\iu \omega t} + c_{-2} \eu^{-2\iu \omega t} + \cdots\,.
$$
Zusammen mit dem konstanten Anteil $\bar{f}$ ergibt sich dann
$$
  f(t) = \sum_{n=-\infty}^{\infty} c_n \eu^{\iu n \omega t}
  = c_0 + c_1 \eu^{\iu \omega t} + c_{-1} \eu^{-\iu \omega t} + c_2 \eu^{2\iu \omega t} + c_{-2} \eu^{-2\iu \omega t} + \cdots\,,
  {{numeq}}{eq:fourier_series}
$$
wobei $c_0 = \bar{f}$. Diese Reihe wird als *Fourier-Reihe* der Funktion $f(t)$ bezeichnet.
[Carleson und Hunt](https://de.wikipedia.org/wiki/Satz_von_Carleson_und_Hunt)
konnten zeigen, dass diese Reihendarstellung für alle 
$\mathcal{L}^2$-Funktionen möglich ist.

Wie können wir nun die Koeffizienten $c_n$ bestimmen? Wenn wir den einzig 
bekannten Koeffizienten $c_0$ betrachten, stellen wir fest, dass wir diesen
durch Mittelung der Funktion, d.h. Integration, erhalten haben. Der oszillierende Anteil
hebt sich bei der Mittelung auf, so dass nur der konstante Anteil übrig 
bleibt. Es wäre doch nützlich, wenn es eine Art von "Mittelung" auch für die anderen
Koeffizienten gäbe. 

Was passiert, wenn wir die Funktion $f(t)$ zuerst mit $\eu^{-\iu \omega t}$ 
multiplizieren und anschließend mitteln? Dann wird der $e_1$-Anteil konstant und die 
anderen Anteile, insb. der konstante Anteil, oszillieren. Die Mittelwertbildung 
würde jetzt also den Koeffizienten $c_1$ liefern. Auf diese Weise können wir 
alle Koeffizienten $c_n$ mit
$$
  c_n = \frac{1}{T} \int_{-T/2}^{T/2} f(t) \eu^{-\iu n \omega t}\du t
  {{numeq}}{eq:fourier_coeffs}
$$
bestimmen.

Wir sind also jetzt in der Lage, jede beliebige $T$-periodische $\mathcal{L}^2$-Funktion
in ihre (diskrete) Frequenzanteile zu zerlegen. Die Signale, die wir in der
Praxis messen, sind jedoch meistens nicht periodisch. Um solche Signale
analysieren zu können, führen wir im nächsten Abschnitt die *Fourier-Transformation* ein.

