# jurisdiction-classification — delta for add-aliyun-coverage

## MODIFIED Requirements

### Requirement: Region-specific endpoint resolution
Where a provider exposes region-specific endpoints, the system SHALL resolve the jurisdiction from
the specific endpoint that was detected.

#### Scenario: International versus mainland endpoint
- **WHEN** a detection matches `dashscope-intl.aliyuncs.com` and another matches `dashscope.aliyuncs.com`
- **THEN** the first resolves to `sg` and the second to `cn`

#### Scenario: Aliyun mainland and Hong Kong regional hosts
- **WHEN** a detection matches a PAI-EAS host carrying an Aliyun region token (for example `svc.cn-hangzhou.pai-eas.aliyuncs.com` or `svc.cn-hongkong.pai-eas.aliyuncs.com`)
- **THEN** the first resolves to `cn` and the second to `hk`

#### Scenario: Aliyun international regional host
- **WHEN** a detection matches a PAI-EAS host in an Aliyun international region (for example `svc.ap-southeast-1.pai-eas.aliyuncs.com`)
- **THEN** it resolves to that region's jurisdiction (`sg`)

#### Scenario: Unmapped Aliyun region token degrades to unknown
- **WHEN** a detection matches a PAI-EAS host whose region token is not in the Aliyun map
- **THEN** the jurisdiction resolves to `unknown`, never to a guessed jurisdiction
