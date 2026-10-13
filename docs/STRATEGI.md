# Brf Knowledge – Strategi 1.0

**Status:** Fastställd  
**Datum:** 2026-10-13  
**Projekt:** Brf Barnängshusen / Brf Knowledge

> **Ledstjärna: Fungerande och användbart före tekniskt optimalt.**

## Syfte och vision

Brf Knowledge ska vara ett lokalt, integritetsmedvetet kunskapssystem som hjälper styrelsen att söka i och förstå föreningens dokument, historik, beslut, avtal, ekonomi och underhåll. Det ska ge begripliga svar på svenska med verifierbara hänvisningar till originalkällorna.

Systemet är ett beslutsstöd, inte en ersättning för styrelsens granskning och ansvar.

## Fastställda principer

1. **Nyttan först.** Leverera en enkel, fungerande lösning och börja använda den i verkliga styrelsefrågor innan avancerad optimering.
2. **Enkel arkitektur.** Använd RAG för att hitta relevanta dokument eller avsnitt. Läs större delar eller hela dokument i modellens kontext när frågan kräver det.
3. **Källor och osäkerhet.** Svar ska kunna verifieras i originaldokument. Systemet ska tydligt säga när underlaget saknas eller är motsägelsefullt och aldrig framställa antaganden som fattade beslut.
4. **Aktualitet utan historielöshet.** Prioritera normalt material från de senaste fem åren genom mjuk viktning, inte ett hårt filter. Äldre giltiga avtal och beslut ska kunna hittas oavsett ålder. Nyare dokument är inte automatiskt mer korrekta.
5. **Lokal hantering och skydd.** Dokument och frågebehandling ska i första hand ske lokalt på DGX Spark. Behörighet, informationsklassning, loggning och personuppgiftshantering behöver beaktas även vid lokal drift.
6. **Lär av användning.** Förbättra sökning, dokumenturval och kontext utifrån observerade fel och faktisk användarfeedback, inte enbart hypotetiska behov.
7. **Utbytbara delar utan överarkitektur.** Håll dokumentlagring, retrieval och svarsgenerering tillräckligt separerade för att kunna förbättras stegvis.

## Första användbara versionen

Prioritera att:

- importera dokument på ett repeterbart sätt;
- ställa frågor på svenska;
- söka fram relevanta dokument och generera begripliga svar;
- visa kontrollerbara källor och låta användaren öppna originalen;
- uttrycka osäkerhet när underlag saknas;
- fungera utan återkommande manuell felsökning.

Börja använda lösningen när dessa grundfunktioner fungerar tillräckligt bra. Prova initialt minst tio verkliga styrelsefrågor och granska svaren mot källorna. För ekonomiska, avtalsmässiga och andra betydelsefulla beslut krävs mänsklig kontroll.

## Förbättringar vid konstaterat behov

Möjliga förbättringar, **inte krav för version 1**:

- hybridsökning med fulltext/BM25 och embeddings;
- bättre dokumentindelning, metadata och tidsviktning;
- reranking och kontextuell indexering;
- utökad dokumentkontext och jämförelser mellan flera dokument;
- iterativ/agentisk sökning;
- strukturerat beslutsregister och kunskapsgraf.

Välj nästa förbättring efter vilken konkret brist den åtgärdar. Undvik att lägga till teknik utan visad nytta.

## Förhållande till långa kontextfönster

Den lokala Qwen-installationen är konfigurerad för upp till 256K tokens, men kapacitet, svarstid och kvalitet vid långa indata ska verifieras praktiskt. Fyll inte kontextfönstret bara för att det finns. Låt frågan och dokumentens relevans avgöra hur mycket material som skickas med.

## Enkel förbättringscykel

1. Ställ en verklig fråga.
2. Bedöm svaret: **Ja / Delvis / Nej** på om det var användbart.
3. Kontrollera källorna och notera saknad eller felaktig information.
4. Förbättra den del som orsakat problemet.
5. Testa samma fråga igen och fortsätt använda systemet.

Bygg successivt upp en liten uppsättning verifierade testfrågor, inklusive frågor utan svar och frågor med äldre eller motstridiga beslut.

## Utvecklingsbeslut

**Nu:** Färdigställ dokumentimport, grundläggande sökning, svar och källhänvisningar i befintliga `Brf_Knowledge`.

**Sedan:** Optimera utifrån verkliga brister och dokumenterade erfarenheter.

**Inte nu:** Avancerad agentorkestrering, GraphRAG/kunskapsgraf, automatiskt beslutsregister eller omfattande benchmark- och optimeringsarbete.

## Kunskapsgrund och vidare läsning

Dessa källor motiverar möjliga tekniker men innebär inte att samtliga ska implementeras direkt:

- [Anthropic – Contextual Retrieval](https://www.anthropic.com/engineering/contextual-retrieval)
- [Microsoft – Hybrid Search](https://learn.microsoft.com/en-us/azure/search/hybrid-search-overview)
- [Microsoft – Relevance and Ranking](https://learn.microsoft.com/en-us/azure/search/search-relevance-overview)
- [Lost in the Middle (TACL 2024)](https://aclanthology.org/2024.tacl-1.9/)

**Beslutsregel:** När systemet fungerar tillräckligt bra för verkligt styrelsearbete prioriterar vi användning och erfarenhetsinsamling framför ytterligare teknisk optimering.
