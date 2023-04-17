# hrlib

hrlib est une librairie Python qui permet de lire les fichiers du logiciel Heredis© de la société BSD concept. Ces fichiers portent l'extension .hr5, .hr7 et .hr8.

## Hebergement

Ce Projet [était hébergé par SourceForge.net](https://hrlib.sourceforge.net/). Je l'ai dupliqué ici sur github.

## Dépendances

Ce projet n'utilise que les modules standards.

## Download et CVS

~~Retrouvez les sur sourceforge et fejoz.net~~

## Documentation

voir le [format des fichiers heredis](http://loic.fejoz.free.fr/formatheredis/) et aussi la [documentation de hrlib](https://hrlib.sourceforge.net/doc.html)

## Examples

### Example 1: full list of persons

Print the full name of all persons in the file

```python
import sys
import hrlib

codecName = sys.getdefaultencoding()

def show(ch):
    print ch.encode(codecName,'replace')

hf = hrlib.open("fejoz.hr5")
for indi in hf.individuGenerator():
    show(indi.fullName)
    for event in indi.events:
        show("\t%s\t:\t%s" % (event.typeName,event.getSimpleDate()))

hf.close()
```

Result look like:

```txt
Joachim RICHON
Claude ROBERT
Jacques ROBERT
        décès   :       @#DGREGORIAN@ 26/8/1904
Pierre ROBERT
        naissance       :       @#DGREGORIAN@ 15/12/1704
Jacques TARTEL
        naissance       :       @#DGREGORIAN@ 8/6/1741
Claude TARTEL
Claude François TARTEL
        naissance       :       @#DGREGORIAN@ 30/11/1704
Jacqueline TOLLOMBERT
Catherin THOME
Joseph THOME
        naissance       :       @#DGREGORIAN@ 22/3/1692
        décès   :       @#DGREGORIAN@ 2/5/1750
```
