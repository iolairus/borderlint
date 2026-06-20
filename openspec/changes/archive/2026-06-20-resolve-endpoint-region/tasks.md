## 1. Region resolution

- [x] 1.1 Add `region_scheme` flags to AWS Bedrock and Azure OpenAI in the knowledge base
- [x] 1.2 Implement AWS/Azure region → ccTLD maps and region extraction in the KB resolver
- [x] 1.3 Resolve a region-coded host before falling back to `unknown`
- [x] 1.4 Tests: Bedrock `ap-east-1`→`hk`, `us-east-1`→`us`, `cn-north-1`→`cn`; dynamic region stays unknown; standard Azure host stays unknown
