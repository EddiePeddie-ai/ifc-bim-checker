# IFC BIM Checker

Dette repositoriet inneholder en GitHub Actions-basert arbeidsflyt for å validere IFC-modeller mot krav definert i en BIM‑instruksjon (PDF). Valideringen gjøres ved å opprette en issue med vedlagte filer, hvoretter en action henter filene, tolker kravene og genererer en rapport.

## Hvordan bruke

1. Gå til [GitHub Pages-siden](https://EddiePeddie-ai.github.io/ifc-bim-checker/) og trykk på knappen *Start validering*, eller opprett en ny issue direkte via `Issues` → `New issue` og velg malen **Validate**.
2. Fyll inn prosjektnavn og en kort beskrivelse.
3. Dra og slipp BIM‑instruksen (PDF) og én eller flere IFC‑filer som vedlegg i issue‑teksten. Den siste PDF‑filen tolkes som kravdokument; alle `.ifc`‑filer blir validert.
4. Send inn issuen. Når GitHub Action‑jobben har kjørt ferdig vil den poste en kort oppsummering som kommentar i issuen. Full rapport (HTML/JSON/SARIF) ligger som artefakt på jobben og som lenke i kommentaren.
5. Hvis du ønsker å kjøre valideringen på nytt (for eksempel etter at modellen er oppdatert), skriv en kommentar med `/run` i issuen.

## Rapport og artefakter

Handlingene genererer:
- **report.html** – en tabellarisk rapport som viser hvilke krav som ble testet mot hvilke objekter, status (pass/fail) og eventuelle avvik.
- **report.json** – samme data i JSON‑format.
- **report.sarif** – konvertert til SARIF for integrasjon med Code Scanning (Security tab).

Du finner disse under *Artifacts* i Action‑runnen og som lenker i issue‑kommentaren.

## Personvern og begrensninger

- **Filstørrelse**: GitHub tillater vedlegg opp til 10 MB per fil i issues. For større PDF‑filer bør du vurdere å splitte dokumentet. Store IFC‑filer kan forårsake lange kjøretider.
- **PDF‑kvalitet**: `extract_requirements.py` bruker enkel tekstuttrekking fra PDF. Dårlig kvalitet (skannede dokumenter) kan gi ufullstendige eller feil krav. Eventuelle feil må korrigeres manuelt.
- **Kravstøtte**: Den medfølgende koden er et utgangspunkt. Kompleks logikk, PSet‑navn eller enheter kan kreve videre utvikling.
- **Behandling av data**: Filene dine behandles bare i GitHub Actions‑jobben. Ingen data sendes videre.

## Utvikling

Se `.github/workflows/validate.yml` for detaljer om arbeidsflyten og `scripts/` for Python‑skriptene som tolker krav, validerer modeller og genererer rapporter.
