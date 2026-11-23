## ADDED Requirements

### Requirement: Wave-12 providers resolve documented destinations

The bundled provider and sovereignty KBs SHALL classify Gnani as `speech` with
`api.vachana.ai`, residency `unknown`, and sovereignty `in`; Gradium as `speech` with its global,
EU, and US API hosts, default residency `unknown`, sovereignty `eu`, and endpoint residency `eu`
and `us` for the respective regional hosts; ResetData as `inference` with `api.resetdata.ai`,
residency and sovereignty `au`; and Vispark as `inference` with `api.lab.vispark.in` and
`api.vispark.in`, residency and sovereignty `in`. Documented SDK keys SHALL be included without
claiming OpenAI-compatible clients as provider-specific SDKs. Missing hosted residency SHALL NOT
be inferred from corporate domicile.

#### Scenario: Gnani public API does not inherit Indian residency
- **WHEN** a flow references `api.vachana.ai`
- **THEN** it resolves to Gnani with jurisdiction `unknown` and sovereignty `in`

#### Scenario: Gradium regional and global hosts remain distinct
- **WHEN** flows reference `api.gradium.ai`, `eu.api.gradium.ai`, and `us.api.gradium.ai`
- **THEN** their jurisdictions resolve respectively to `unknown`, `eu`, and `us`, all with
  sovereignty `eu`

#### Scenario: ResetData and Vispark resolve documented hosting
- **WHEN** flows reference `api.resetdata.ai` and `api.lab.vispark.in`
- **THEN** they resolve respectively to `au`/`au` and `in`/`in` residency/sovereignty

### Requirement: Wave-12 adjacent endpoint facts remain platform-specific

The Xiaomi MiMo KB SHALL recognize `token-plan-sgp.xiaomimimo.com` as `sg` and
`token-plan-ams.xiaomimimo.com` as `eu` while retaining the CN host as `cn`. The Zhipu KB SHALL
resolve `api.z.ai` to Singapore residency and distinguish Z.ai's Singapore-law/SIAC terms from the
domestic BigModel terms; this legal-forum correction SHALL NOT by itself change Zhipu's provider
sovereignty.

#### Scenario: Token Plan hosts resolve their documented regions
- **WHEN** flows reference the CN, SGP, and AMS Token Plan hosts
- **THEN** their jurisdictions resolve respectively to `cn`, `sg`, and `eu`

#### Scenario: International Z.ai processing is not described as China-resident
- **WHEN** a flow references `api.z.ai`
- **THEN** its jurisdiction resolves to `sg` and its provider note does not claim that Z.ai's cloud
  API is governed by Chinese law
