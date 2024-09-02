Hi, this is my thesi's project on Lenia.

# Roadmap

- [ ] play/stop
- [ ] reset

- [ ] Statistics:
    - [ ] FPS
    - [ ] mass
    - [ ] center of mass
    - [ ] velocity
    - [ ] angle
    - [ ] linear velocity
    - [ ] angular velocity
    - [ ] color

- [ ] save_stats (opzionale)

## Aquarium

- [ ] Undrstand how to create kernels -> b value !! mezzo capito
- [ ] Set up cycle on every kernel
- [ ] Represent channels as RGB values
- [ ] set up more stats to save as json: 
    density -> mass for every channel and divide by number of cells (there has to be three densities)
    

- annotazioni:
    - generato all'inizio file che non tenevano conto dell'average
    - data.csv sono file con 200 iterazioni senza average, solo con massa finale
    - results0/1/2/3.json sono validi solo come massa perché gli average sono stati calcolati sul totale dei frame in cui c'era massa e quindi non sempre su 200 frame che è la durata di tutto l'esperimento. 
    - masstestClassifier2.json ha i valori più completi in rapporto al numero di sample generati
    - masstestClassifier2_LowFiltered_200iterations ha valori di average filtrati con un passa basso e un'area della tabella x4 rispetto agli altri esperimenti. Ci mette troppo tempo a generare gli esperimenti.